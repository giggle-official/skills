# Giggle Pro Skill - Setup Guide

Complete installation guide for the Giggle Pro AI short drama production skill.

## Prerequisites

- Node.js 18+
- ffmpeg (for video quality check frame extraction)

```bash
# Install ffmpeg (Ubuntu/Debian)
sudo apt install ffmpeg

# Install ffmpeg (macOS)
brew install ffmpeg
```

## Installation

### 1. Copy the skill to your workspace

```bash
cp -r giggle-pro /path/to/your/clawd/skills/
```

### 2. Configure API Keys

Copy the example config and fill in your credentials:

```bash
cd skills/giggle-pro
cp config.example.json config.json
```

Edit `config.json`:

```json
{
  "apiKey": "sk_prod_YOUR_GIGGLE_API_KEY",
  "apiBase": "https://giggle.pro",
  "anthropicApiKey": "sk-ant-YOUR_ANTHROPIC_API_KEY",
  "qcModel": "claude-sonnet-4-20250514",
  "qcThreshold": 80
}
```

Or use the CLI:

```bash
node scripts/giggle-api.js set-key YOUR_GIGGLE_API_KEY
```

## Configuration Reference

| Field | Required | Description | Default |
|-------|----------|-------------|---------|
| `apiKey` | ✅ Yes | Giggle/AIDirector API key. Get from [giggle.pro](https://giggle.pro) dashboard. Format: `sk_prod_...` | - |
| `apiBase` | No | API base URL | `https://giggle.pro` |
| `anthropicApiKey` | No* | Anthropic API key for quality check. Format: `sk-ant-...` | - |
| `qcModel` | No | Claude model for quality scoring | `claude-sonnet-4-20250514` |
| `qcThreshold` | No | Minimum passing score (0-100) | `80` |

\* Required only if you want to use the quality check feature.

### Environment Variables

API keys can also be set via environment variables (takes precedence over config.json):

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

## Verify Installation

```bash
# Test Giggle API connection
node scripts/giggle-api.js list-projects

# Test quality check setup (if configured)
node scripts/quality-check.js --help
```

## Quality Check Models

The quality check feature uses Claude's vision capability. Supported models:

| Model | Cost | Speed | Accuracy |
|-------|------|-------|----------|
| `claude-sonnet-4-20250514` | ~$0.01/shot | Fast | Good |
| `claude-opus-4-20250514` | ~$0.05/shot | Slower | Best |

Change model in `config.json`:
```json
{
  "qcModel": "claude-opus-4-20250514"
}
```

Or per-run:
```bash
node scripts/quality-check.js <project_id> --model opus
```

## Troubleshooting

### "ANTHROPIC_API_KEY not set"

Add your Anthropic API key to `config.json`:
```json
{
  "anthropicApiKey": "sk-ant-api03-<REDACTED>..."
}
```

Or set the environment variable:
```bash
export ANTHROPIC_API_KEY=sk-ant-api03-<REDACTED>...
```

### "Authentication failed" on Giggle API

1. Check your API key format: should start with `sk_prod_`
2. Verify the key in your Giggle dashboard
3. Run `node scripts/giggle-api.js set-key <key>` to reset

### Quality check fails to extract frames

Install ffmpeg:
```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows
choco install ffmpeg
```

## File Structure

```
giggle-pro/
├── SKILL.md              # Main skill documentation
├── SETUP.md              # This file
├── config.json           # Your configuration (git-ignored)
├── config.example.json   # Example configuration template
├── scripts/
│   ├── giggle-api.js     # Main API wrapper
│   └── quality-check.js  # Video quality evaluation
├── references/
│   ├── api-docs.md       # API documentation
│   └── quality-scoring.md # Scoring criteria
└── output/               # Generated reports (git-ignored)
```

## Next Steps

Once setup is complete, see [SKILL.md](./SKILL.md) for the full production workflow.
