# Discord Community Growth Expert

> AI-powered Discord community management agent with automatic reply, user intent analysis, lead tracking, and real-time dashboard.

---

## ✨ Features

- ✅ **Auto-reply** to Discord messages with AI-generated responses
- 🏷️ **User tagging** based on intent and behavior
- 🚩 **High-intent lead flagging** for sales follow-up
- 📊 **Real-time Dashboard** with 6 widgets (optional)
- 🎯 **Customizable persona** (content focus, reply style, target audience)
- 📈 **Analytics** (intent distribution, tag distribution, frequent questions)

---

## 🚀 Quick Start

### Prerequisites

- OpenClaw installed and running
- Discord account with server admin access
- Node.js 18+ (included with OpenClaw)
- Python 3.10+ (for Dashboard updates)

### Installation

1. **Install this agent from TalentHub:**
   ```bash
   # Agent will be automatically installed to:
   # ~/.openclaw/workspace-discord-community-growth-expert/
   ```

2. **Start the onboarding flow:**
   
   The agent will automatically guide you through 8 steps:
   - Create Discord Application
   - Create Bot and copy Token
   - Enable required Intents
   - Generate invite link and add Bot to server
   - Get Server ID and Channel IDs
   - Provide Bot Token
   - Configure user profile (content focus, reply style, audience)
   - (Optional) Setup Dashboard
   - Auto-deploy Bot service

3. **Test in Discord:**
   - Send a message in your configured channel
   - Or @mention your Bot
   - Bot will reply automatically with AI-generated responses

---

## 📊 Dashboard (Optional)

If you enabled Dashboard during onboarding, you'll get a real-time web interface with:

- 📊 **高频问题 Top 10** — Most asked questions
- 🎯 **高意向用户** — High-intent leads
- 📢 **需要反馈的问题** — Issues to escalate
- 📈 **用户意图分布** — Intent distribution (pie chart)
- 🏷️ **粉丝标签 Top 10** — Tag distribution (bar chart)
- 📊 **关键指标** — Key metrics (total messages, high-intent count, etc.)

Dashboard is accessible via:
- **Public URL**: `https://device-xxx.clawln.app` (accessible from anywhere)
- **Local URL**: `http://localhost:3000`

---

## ⚙️ Configuration

### Customize Reply Style

Edit `outputs/user_profile.json`:

```json
{
  "content_focus": "AI tools review + LLM news",
  "reply_style": "hardcore technical",
  "target_audience": "developers, entrepreneurs",
  "product_service": "Your product name",
  "community_rules": "No ads, be respectful, tech topics only"
}
```

### Customize Persona

Edit `SOUL.md` to change the Bot's personality and communication style.

### Add Custom Rules

Edit `AGENTS.md` → `Mandatory Behavior Rules` section.

---

## 🛠️ Management Commands

### Check Bot Status
```bash
cd ~/.openclaw/workspace-discord-community-growth-expert/discord-bot
npx pm2 list
```

### View Logs
```bash
npx pm2 logs discord-bot
```

### Restart Bot
```bash
npx pm2 restart discord-bot
```

### Stop Bot
```bash
npx pm2 stop discord-bot
```

### Update Bot Code
After editing `discord-bot/index.js`:
```bash
npx pm2 restart discord-bot
```

---

## 🏗️ Architecture

```
User sends message in Discord
    ↓
Bot (discord.js) receives message
    ↓
Bot analyzes intent & tags (咋询/夸赞/质疑/求资料/合作/投诉/购买)
    ↓
Bot calls OpenClaw Gateway API
    ↓
Gateway routes to discord-community-growth-expert agent
    ↓
Agent generates reply (3-part structure: answer → value add → light action)
    ↓
Bot sends reply back to Discord
    ↓
Bot updates Dashboard (if enabled) via Python script
```

---

## 🐛 Troubleshooting

### Bot shows offline in Discord
- Check PM2 status: `npx pm2 list`
- Check logs: `npx pm2 logs discord-bot --err`
- Verify Token in `.env` file

### Bot doesn't reply
- Verify Channel ID in `.env` matches your Discord channel
- Check Gateway API is enabled:
  ```bash
  curl -s http://localhost:18789/v1/models \
    -H "Authorization: Bearer $(cat ~/.openclaw/gateway-password.txt)"
  ```
- Should return JSON with `openclaw/discord-community-growth-expert`

### "Not Found" error in logs
- Gateway OpenAI API endpoint not enabled
- Run:
  ```bash
  openclaw config set gateway.http.endpoints.chatCompletions.enabled true
  openclaw gateway restart
  ```

### Request timeout
- Gateway is busy processing another request
- Wait 30 seconds and try again
- Or restart Bot: `npx pm2 restart discord-bot`

### Dashboard not updating
- Check if Dashboard is enabled: `cat outputs/dashboard_config.json`
- Verify Python 3 is installed: `python3 --version`
- Check Dashboard DB exists: `ls ~/.claw/shared/shared.db`

---

## 📁 File Structure

```
~/.openclaw/workspace-discord-community-growth-expert/
├── AGENTS.md              # Operational rules and onboarding flow
├── SOUL.md                # Bot personality and communication style
├── USER.md                # Target audience and use case
├── IDENTITY.md            # Agent identity
├── TOOLS.md               # Environment-specific notes
├── HEARTBEAT.md           # Periodic tasks (empty by default)
├── outputs/
│   ├── bot_config.json    # Saved configuration (no Token)
│   ├── user_profile.json  # User persona and reply rules
│   └── dashboard_config.json  # Dashboard config (if enabled)
├── discord-bot/
│   ├── package.json       # Node.js dependencies
│   ├── index.js           # Bot main program
│   └── .env               # Token and Channel ID (DO NOT COMMIT)
└── skills/
    ├── discord-auto-deploy/  # Auto-deployment skill
    ├── dashboard/            # Dashboard skill
    └── ...                   # Other skills
```

---

## 🔒 Security Notes

- **Never commit `.env` file** to version control
- **Never share Bot Token** publicly
- **Reset Token immediately** if leaked (Discord Developer Portal → Bot → Reset Token)
- Bot runs locally on your machine, no data sent to third parties
- Gateway API uses password auth (stored in `~/.openclaw/gateway-password.txt`)

---

## 🎨 Customization Examples

### Change reply language
Edit `AGENTS.md` → Rule 5:
```markdown
5. **Match the user's language.** Reply in the same language the user wrote in.
```

### Add welcome message for new members
Edit `discord-bot/index.js` → add event listener:
```javascript
client.on('guildMemberAdd', async (member) => {
  const channel = member.guild.channels.cache.get(CHANNEL_ID);
  await channel.send(`Welcome ${member}! 🌱`);
});
```

### Monitor multiple channels
Edit `discord-bot/.env`:
```
DISCORD_CHANNEL_ID=123456789,987654321
```

Then update `index.js` to check multiple channels.

---

## 📚 Documentation

- OpenClaw Docs: https://docs.openclaw.ai
- Community: https://discord.com/invite/clawd
- Issues: https://github.com/openclaw/openclaw/issues

---

## 📝 License

MIT

---

## 🙏 Credits

Built with:
- [discord.js](https://discord.js.org/) — Discord API wrapper
- [OpenClaw](https://openclaw.ai/) — AI Agent platform
- [PM2](https://pm2.keymetrics.io/) — Process manager
- [Cloudflared](https://github.com/cloudflare/cloudflared) — Tunnel for Dashboard

---

## 🆘 Support

If you encounter any issues:

1. Check the Troubleshooting section above
2. Review logs: `npx pm2 logs discord-bot`
3. Join OpenClaw Discord: https://discord.com/invite/clawd
4. Open an issue on GitHub

---

**Version**: 1.0.0  
**Last Updated**: 2026-05-09
