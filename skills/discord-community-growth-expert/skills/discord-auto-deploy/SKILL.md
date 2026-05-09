---
name: discord-auto-deploy
description: "Auto-deploy a Discord AI bot connected to OpenClaw Gateway. Handles Node.js bot setup, PM2 process management, and Gateway API integration. Use when the user has completed Discord Bot onboarding and needs the bot deployed and running."
version: "1.0.2"
author: discord-community-growth-expert
license: MIT

category: deployment
tags:
  - discord
  - bot
  - deployment
  - automation
  - pm2
  - nodejs

capabilities:
  - bot_deployment
  - process_management
  - gateway_integration
  - auto_restart

languages:
  - zh
  - en
---

# Discord Auto-Deploy Skill

This skill handles the full deployment of a Discord AI bot after onboarding is complete.

## When to Use

Load and follow this skill when:
- User has completed the onboarding flow (bot_config.json exists with `onboarding_complete: true`)
- User asks to deploy, start, or restart the Discord bot
- Bot is not responding and needs to be fixed or redeployed

## Deployment Steps

When triggered, execute the following steps **in order**. Do not skip any step.

### Step 1 — Read Configuration

Read `outputs/bot_config.json` and extract:
- `server_id`
- `channel_ids[0]` (primary channel)
- `token_provided` (must be true)

Also read `discord-bot/.env` to check if DISCORD_TOKEN is already set.

### Step 2 — Enable Gateway API

Run the following commands:

```bash
openclaw config set gateway.http.endpoints.chatCompletions.enabled true
```

Then restart the gateway:

```bash
openclaw gateway restart
```

Wait 5 seconds, then verify:

```bash
curl -s http://localhost:18789/v1/models \
  -H "Authorization: Bearer $(cat ~/.openclaw/gateway-password.txt)"
```

Expected: JSON response containing `openclaw/discord-community-growth-expert`.

If verification fails, wait 5 more seconds and retry once.

### Step 3 — Create Bot Directory

Create the directory structure:

```bash
mkdir -p <workspace>/discord-bot
```

Where `<workspace>` is the agent workspace root.

### Step 4 — Write Bot Files

Write the following files to `discord-bot/`:

**package.json** — use template at `templates/package.json`

**.env** — write with actual values:
```
DISCORD_TOKEN=<token_from_user>
DISCORD_CHANNEL_ID=<channel_id_from_config>
```

**index.js** — use template at `templates/index.js`

### Step 5 — Install Dependencies

```bash
cd <workspace>/discord-bot
npm install discord.js dotenv
```

### Step 6 — Start with PM2

Stop any existing instance first:
```bash
npx pm2 delete discord-bot 2>/dev/null || true
```

Start fresh:
```bash
npx pm2 start index.js --name discord-bot
```

Enable auto-restart on system reboot:
```bash
npx pm2 startup 2>/dev/null || true
npx pm2 save
```

### Step 7 — Verify

Wait 3 seconds, then check status:

```bash
npx pm2 list | grep discord-bot
```

Expected: status shows `online`.

Also check logs for startup confirmation:
```bash
npx pm2 logs discord-bot --lines 5 --nostream
```

Expected output includes:
```
✅ Bot 已上线: <bot-name>
📡 监听频道 ID: <channel-id>
```

### Step 8 — Confirm to User

Send this message (in user's language):

**中文：**
> **Bot 部署完成！🎉**
>
> 现在去你的 Discord 服务器测试一下：
> 1. 在配置的频道里发一条消息
> 2. 或者 @你的 Bot
>
> Bot 会用 AI 自动回复 👀
>
> **管理命令：**
> - 查看状态：`npx pm2 list`
> - 查看日志：`npx pm2 logs discord-bot`
> - 重启 Bot：`npx pm2 restart discord-bot`
> - 停止 Bot：`npx pm2 stop discord-bot`

**English:**
> **Bot deployed successfully! 🎉**
>
> Go test it in your Discord server:
> 1. Send a message in the configured channel
> 2. Or @mention your Bot
>
> The Bot will reply automatically with AI 👀
>
> **Management commands:**
> - Check status: `npx pm2 list`
> - View logs: `npx pm2 logs discord-bot`
> - Restart: `npx pm2 restart discord-bot`
> - Stop: `npx pm2 stop discord-bot`

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Gateway API returns 404 | Endpoint not enabled | Re-run Step 2 |
| Bot status is `errored` in PM2 | Code or .env error | Check `npx pm2 logs discord-bot --err` |
| Bot online but no reply in Discord | Wrong Channel ID | Verify DISCORD_CHANNEL_ID in .env |
| Bot replies "抱歉，我现在有点忙" | AI call failed | Check Gateway is running: `openclaw gateway status` |
| Session lock timeout in logs | Concurrent requests | Wait 30s, run `npx pm2 restart discord-bot` |
| "Invalid token" error | Token wrong or expired | Get new token from Discord Developer Portal → Bot → Reset Token |

---

## Management Commands Reference

```bash
# Status
npx pm2 list

# Logs (live)
npx pm2 logs discord-bot

# Logs (errors only)
npx pm2 logs discord-bot --err

# Restart
npx pm2 restart discord-bot

# Stop
npx pm2 stop discord-bot

# Delete (full remove)
npx pm2 delete discord-bot

# Re-deploy from scratch
bash <workspace>/scripts/deploy-bot.sh
```
