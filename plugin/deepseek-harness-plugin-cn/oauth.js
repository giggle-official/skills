import { execFile } from "node:child_process"
import { randomBytes } from "node:crypto"
import { once } from "node:events"
import { createServer } from "node:http"
import { auth, UnauthorizedError } from "@modelcontextprotocol/client"

const scope = "director:mcp"
const key = "giggle-ai-director/account"

async function openAuthorizationPage(url, signal) {
  const commands = {
    darwin: ["/usr/bin/open", []],
    win32: ["rundll32.exe", ["url.dll,FileProtocolHandler"]],
    linux: ["xdg-open", []],
  }
  const command = commands[process.platform]
  if (!command || signal.aborted) return false
  const [file, args] = command
  return new Promise((resolve) => {
    execFile(file, [...args, url.href], { signal, timeout: 3_000, windowsHide: true }, (error) => {
      resolve(!error)
    })
  })
}

function sameOriginFetch(origin, signal) {
  return (input, init = {}) => {
    const target = new URL(typeof input === "string" || input instanceof URL ? input : input.url)
    if (target.origin !== origin || target.username || target.password) {
      throw new Error("Unexpected Giggle server origin")
    }
    const signals = [signal, init.signal, AbortSignal.timeout(30_000)].filter(Boolean)
    return fetch(input, { ...init, redirect: "error", signal: AbortSignal.any(signals) })
  }
}

function createProvider(redirectUrl, state, saved, onRedirect) {
  let client = saved?.client
  let tokens = saved?.tokens
  let expiresAt = saved?.expiresAt
  let verifier
  let discovery
  return {
    redirectUrl,
    clientMetadata: {
      client_name: "Giggle AI Director for DeepSeek Harness",
      redirect_uris: [redirectUrl],
      grant_types: ["authorization_code", "refresh_token"],
      response_types: ["code"],
      token_endpoint_auth_method: "none",
      scope,
    },
    state: () => state,
    clientInformation: () => client,
    saveClientInformation: (value) => { client = value },
    tokens: () => tokens,
    saveTokens: (value) => {
      tokens = value
      expiresAt = Date.now() + (value.expires_in ?? 3600) * 1000
    },
    saveCodeVerifier: (value) => { verifier = value },
    codeVerifier: () => verifier,
    saveDiscoveryState: (value) => { discovery = value },
    discoveryState: () => discovery,
    redirectToAuthorization: onRedirect,
    result: () => ({ redirectUrl, client, tokens, expiresAt }),
  }
}

export function createGiggleOAuth(credentials, endpoint) {
  const serverUrl = new URL(endpoint)
  if (serverUrl.protocol !== "https:" || serverUrl.username || serverUrl.password ||
      serverUrl.search || serverUrl.hash) {
    throw new Error("Giggle MCP requires an HTTPS endpoint without credentials, query, or fragment")
  }
  const origin = serverUrl.origin
  let refreshPromise

  async function savedGrant() {
    const record = await credentials.readRecord(key)
    return record?.kind === "grant" && record.payload.endpoint === endpoint ? record.payload : undefined
  }

  async function signIn(session, lifetime) {
    const signal = AbortSignal.any([session.signal, lifetime, AbortSignal.timeout(5 * 60_000)])
    const state = randomBytes(32).toString("base64url")
    const server = createServer()
    const { promise, resolve, reject } = Promise.withResolvers()
    // Registration can fail before the browser is opened.
    void promise.catch(() => {})
    const abort = () => reject(signal.reason)
    signal.addEventListener("abort", abort, { once: true })
    try {
      const listening = once(server, "listening", { signal })
      server.listen(0, "127.0.0.1")
      await listening
      const callback = new URL(`http://127.0.0.1:${server.address().port}/callback`)
      server.on("request", (request, response) => {
        const url = URL.parse(request.url ?? "/", callback.origin)
        const valid = request.method === "GET" && request.headers.host === callback.host &&
          url?.origin === callback.origin && url.pathname === callback.pathname &&
          url.searchParams.get("state") === state
        response.setHeader("Content-Type", "text/plain; charset=utf-8")
        response.setHeader("Cache-Control", "no-store")
        response.setHeader("Referrer-Policy", "no-referrer")
        if (!valid) {
          response.writeHead(400).end("Invalid Giggle authorization callback.")
          return
        }
        const code = url.searchParams.get("code")
        if (!code || url.searchParams.has("error")) {
          response.writeHead(400).end("Giggle authorization was not completed.")
          reject(new Error("Giggle authorization was declined or failed"))
          return
        }
        response.end("Giggle authorization received. Return to DeepSeek Harness to see the result.")
        resolve({ authorizationCode: code, iss: url.searchParams.get("iss") ?? undefined })
      })
      const provider = createProvider(callback.href, state, undefined, async (authorizationUrl) => {
        if (authorizationUrl.protocol !== "https:" || authorizationUrl.origin !== origin ||
            authorizationUrl.username || authorizationUrl.password) {
          throw new Error("Unexpected Giggle authorization origin")
        }
        const opened = await openAuthorizationPage(authorizationUrl, signal)
        signal.throwIfAborted()
        const message = opened
          ? "已请求默认浏览器打开 Giggle 授权页。若未看到页面，请手动打开授权链接。"
          : "无法自动打开浏览器，请手动打开链接并确认 Giggle 授权。"
        session.notify({ message, url: authorizationUrl.href })
      })
      const options = { serverUrl, scope, fetchFn: sameOriginFetch(origin, signal) }
      if (await auth(provider, options) !== "REDIRECT") throw new Error("Giggle did not request authorization")
      const result = await promise
      if (await auth(provider, { ...options, ...result }) !== "AUTHORIZED") throw new UnauthorizedError()
      signal.throwIfAborted()
      await credentials.modifyRecord(key, () => ({ kind: "grant", payload: { endpoint, ...provider.result() } }))
    } finally {
      signal.removeEventListener("abort", abort)
      server.close()
      server.closeAllConnections()
    }
  }

  async function accessToken(signal) {
    const saved = await savedGrant()
    if (!saved?.tokens) throw new UnauthorizedError("请在 Harness 的凭证设置中授权 Giggle AI 导演")
    if (saved.expiresAt > Date.now() + 60_000) return saved.tokens.access_token
    refreshPromise ??= credentials.modifyRecord(key, async (record) => {
      const latest = record?.payload
      if (!latest || latest.endpoint !== endpoint) throw new UnauthorizedError()
      if (latest.expiresAt > Date.now() + 60_000) return record
      const provider = createProvider(latest.redirectUrl, undefined, latest, () => {
        throw new UnauthorizedError("Giggle 授权已过期，请在凭证设置中重新连接")
      })
      if (await auth(provider, { serverUrl, scope, fetchFn: sameOriginFetch(origin) }) !== "AUTHORIZED") {
        throw new UnauthorizedError("Giggle 授权已过期，请在凭证设置中重新连接")
      }
      return { kind: "grant", payload: { endpoint, ...provider.result() } }
    }).finally(() => { refreshPromise = undefined })
    const record = await refreshPromise
    signal?.throwIfAborted()
    return record.payload.tokens.access_token
  }

  return { key, signIn, savedGrant, accessToken, fetch: sameOriginFetch(origin) }
}
