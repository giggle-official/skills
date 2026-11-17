import { readFile } from "node:fs/promises"
import { fileURLToPath } from "node:url"
import { Client, StreamableHTTPClientTransport } from "@modelcontextprotocol/client"
import { createGiggleOAuth } from "./oauth.js"

export const name = "giggle-ai-director"
export const inject = ["authorization", "credentials", "skills", "tools"]

const defaultEndpoint = "https://giggle.pro/mcp"
const textOutput = {
  schema: { type: "string" },
  render: (_args, value) => [{ type: "text", text: value }],
}

async function registerSkills(ctx) {
  for (const category of ["canvas", "image", "video", "audio"]) {
    const path = new URL(`./skills/ai-director-${category}/SKILL.md`, import.meta.url)
    const document = await readFile(path, "utf8")
    // These bundled files share the same single-line metadata as the other Giggle plugins.
    const [, skillName, description, content] =
      /^---\r?\nname: ([^\r\n]+)\r?\ndescription: ([^\r\n]+)\r?\n---\r?\n([\s\S]+)$/.exec(document) ?? []
    if (!skillName) throw new Error(`Invalid bundled Giggle skill: ${category}`)
    ctx.skills.register({
      name: skillName,
      description,
      content: content.trim(),
      source: "runtime",
      resourceBase: fileURLToPath(new URL("./", path)),
    })
  }
}

export async function apply(ctx, config = {}) {
  const endpoint = config.mcpUrl ?? defaultEndpoint
  const oauth = createGiggleOAuth(ctx.credentials, endpoint)
  const lifetime = new AbortController()
  const disposers = []
  let loadingTools
  let loaded = false

  async function withClient(callback, signal) {
    const stop = AbortSignal.any([lifetime.signal, ...(signal ? [signal] : [])])
    const accessToken = await oauth.accessToken(stop)
    const transport = new StreamableHTTPClientTransport(new URL(endpoint), {
      fetch: oauth.fetch,
      requestInit: { headers: { Authorization: `Bearer ${accessToken}` } },
    })
    const client = new Client({ name: "giggle-ai-director-dsh", version: "0.1.0" })
    const close = () => { void transport.close().catch(() => {}) }
    stop.addEventListener("abort", close, { once: true })
    try {
      stop.throwIfAborted()
      await client.connect(transport, { signal: stop, timeout: 30_000 })
      return await callback(client, stop)
    } finally {
      stop.removeEventListener("abort", close)
      await client.close()
    }
  }

  function loadTools() {
    if (loaded) return Promise.resolve()
    loadingTools ??= withClient((client, signal) => client.listTools({}, { signal }))
      .then(({ tools }) => {
        lifetime.signal.throwIfAborted()
        if (!tools.length) throw new Error("Giggle returned an empty MCP tool list")
        try {
          for (const tool of tools) {
            if (!/^[A-Za-z][A-Za-z0-9_]{0,63}$/.test(tool.name)) {
              throw new Error("Invalid Giggle MCP tool name")
            }
            disposers.push(ctx.tools.register({
              name: `mcp__giggle_director__${tool.name}`,
              description: tool.description ?? tool.name,
              parameters: tool.inputSchema,
              output: textOutput,
              async execute(args, execution) {
                const result = await withClient(
                  (client, signal) => client.callTool({ name: tool.name, arguments: args }, { signal }),
                  execution?.signal
                )
                const text = result.structuredContent
                  ? JSON.stringify(result.structuredContent)
                  : result.content.filter((part) => part.type === "text").map((part) => part.text).join("\n")
                if (result.isError) throw new Error(text || "Giggle MCP call failed")
                return text
              },
            }))
          }
          loaded = true
        } catch (error) {
          for (const dispose of disposers.splice(0).reverse()) dispose()
          throw error
        }
      }).finally(() => { loadingTools = undefined })
    return loadingTools
  }

  ctx.effect(() => () => {
    lifetime.abort()
    for (const dispose of disposers.splice(0).reverse()) dispose()
  })

  ctx.authorization.registerFlow({
    key: oauth.key,
    label: "Giggle AI 导演",
    methods: [{ id: "oauth", label: "使用 Giggle 账户授权" }],
    async run(session) {
      await oauth.signIn(session, lifetime.signal)
      // The credential was committed. A temporary MCP failure can be retried separately.
      await loadTools().catch(() => {})
    },
  })

  ctx.tools.register({
    name: "giggle_connection_status",
    description: "Check Giggle AI Director. Use authorize=true only to start a sign-in the user requested. Does not generate content.",
    parameters: {
      type: "object",
      properties: { authorize: { type: "boolean", description: "Start an interactive Giggle account sign-in" } },
      additionalProperties: false,
    },
    output: textOutput,
    async execute({ authorize = false } = {}) {
      if (ctx.authorization.describe(oauth.key)?.inFlight) {
        return "Giggle 授权正在进行。请在浏览器中确认授权；若未看到页面，请使用之前返回的授权链接。"
      }
      if (authorize) {
        const { promise, resolve, reject } = Promise.withResolvers()
        void ctx.authorization.begin({
          key: oauth.key,
          method: "oauth",
          signal: lifetime.signal,
          interaction: {
            notify: ({ message, url }) => resolve(`${message}\n授权链接：${url}`),
            prompt: async () => { throw new Error("Giggle uses a browser callback") },
          },
        }).then(
          () => resolve("Giggle 授权已结束，可再次查询连接状态。"),
          reject
        )
        return promise
      }
      if (!await oauth.savedGrant()) {
        return "尚未授权 Giggle。用户准备登录时，可以使用 authorize=true 获取浏览器授权链接。"
      }
      await oauth.accessToken(lifetime.signal)
      await loadTools()
      return "Giggle AI 导演工具已加载。可调用 list_models 和 list_canvases 验证，安装检查无需生成。"
    },
  })

  await registerSkills(ctx)
  if (await oauth.savedGrant()) {
    // Do not block Harness startup when an external connection is unavailable.
    void loadTools().catch(() => {})
  }
}
