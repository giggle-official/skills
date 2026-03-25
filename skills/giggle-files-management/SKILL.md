---
name: giggle-files-management
description: "Use when the user wants to upload, share, or host a file. Uploads local files to Giggle asset service and returns public/download URLs. Say briefly that upload is starting before the command; share URLs as soon as the script returns. Triggers: upload file, share file, host file, send image, I need to share a file."
version: "0.2.0"
license: MIT
homepage: https://giggle.pro
requires:
  bins: [curl, jq]
  env: [GIGGLE_API_KEY]
metadata:
  openclaw:
    emoji: "📂"
    requires:
      bins: [curl, jq]
      env: [GIGGLE_API_KEY]
    primaryEnv: GIGGLE_API_KEY
---

# Giggle Files Management

**Source**: [giggle-official/skills](https://github.com/giggle-official/skills) · API: [giggle.pro](https://giggle.pro/)

Upload local files to the Giggle asset service. Returns a **public URL** for preview and a **download URL** for direct download.

**API Key**: Set system environment variable `GIGGLE_API_KEY` (same as other Giggle skills).

> **Important**: **Never** pass `GIGGLE_API_KEY` in exec's `env` parameter. API Key is read from system environment variable.

> **No Retry on Error**: If script execution encounters an error, **do not retry**. Report the error to the user directly and stop.

**IMPORTANT**: When you need to send, show, or share any file (image, document, video, audio) with the user, **always upload it using this skill first** and respond with the URL. Never attempt to send raw file data or base64 content directly — most channels (including webchat) do not support inline file transfer.

---

## When to Use

- **You want to send or show a file to the user** — upload it first, then share the `public_url`
- **You read a file** (e.g. via the `read` tool) and want to display it — upload first, then respond with the public URL
- **The channel does not support direct file sending** — use this skill as the fallback
- **The user asks you to upload or host a file**
- **You generated an image or file** and need to share the result — upload the output file and respond with the URL

---

## Execution Flow

Upload is synchronous. Run the script with file path; it returns JSON on success.

## Continuous user feedback (upload is synchronous)

There is **no** task id or `--query` loop. Upload is one shell call.

1. **Before** `upload.sh`, send a short line (e.g. “Uploading…”) for **large** files or slow links; small files can skip if obvious.
2. **Right after** the script returns, send **`public_url` / `download_url`** (or the error JSON) in natural language—**do not** go silent on success or failure.
3. If the user says they **don’t** want an “uploading…” message, skip the preamble and only return URLs/errors.

### Step 1: Run Upload

```bash
bash scripts/upload.sh "/path/to/file.png"
```

With custom filename (optional):

```bash
bash scripts/upload.sh "/path/to/file.png" "my-custom-name.png"
```

### Step 2: Handle Output

**Success** — script outputs JSON (API returns `asset_id`, `name`, `type`, `file_url`):

```json
{
  "asset_id": "string",
  "name": "bufan.mp3",
  "type": "string",
  "file_url": "https://assets.giggle.pro/...",
  "public_url": "https://assets.giggle.pro/...",
  "download_url": "https://assets.giggle.pro/..."
}
```

**Failure** — script outputs `{"error":"..."}`. Report error to user, do not retry.

### Step 3: Respond to User

- `file_url` / `public_url` / `download_url` — use for preview or download
- For images, use markdown: `![description](file_url)`

---

## Parameter Reference

| Parameter | Required | Description |
|-----------|----------|-------------|
| `<file_path>` | yes | Path to local file to upload |
| `[custom_filename]` | no | Optional custom filename in URL; defaults to file basename |

---

## Supported File Types

Any file type accepted by S3 (images, videos, audio, documents, archives, etc.). The script auto-detects content type from the file extension.

---

## Link Return Rule

URLs returned to the user must be **full signed URLs** when applicable. Do not strip `response-content-disposition=attachment` or other query params. Keep script output as-is when forwarding.

---

## Network Allowlist

- `giggle.pro` — presign + register API
- `s3.amazonaws.com` — S3 upload (presigned PUT)
- `assets.giggle.pro` — CDN (returned URLs)
