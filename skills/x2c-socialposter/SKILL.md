---
name: x2c-socialposter
description: "Social media publishing, analytics, messaging and content tools via X2C Open API. Use when the user needs to: (1) Publish text/media posts to TikTok, Instagram, Facebook, YouTube, LinkedIn, Twitter, etc. (2) Schedule or auto-schedule posts for best engagement time. (3) Manage comments and replies. (4) Upload media files (up to 5GB). (5) View post history and account analytics. (6) Get AI-generated post text and hashtag suggestions. (7) Send/list direct messages on IG/FB/X. (8) Create trackable short links. (9) Check Google Business reviews. (10) Look up brand info. Triggers: post to social media, publish post, social media, schedule post, auto-schedule, upload media, social accounts, comment, analytics, hashtags, generate post, DM, short link, brand lookup, GMB reviews."
version: "0.2.0"
license: MIT
author: storyclaw-official
homepage: https://github.com/storyclaw-official/skills
repository: https://github.com/storyclaw-official/skills
requires:
  bins: [python3]
  env: [X2C_API_KEY]
  pip: [requests]
metadata:
  {
    "openclaw": {
      "emoji": "📱",
      "requires": {
        "bins": ["python3"],
        "env": ["X2C_API_KEY"],
        "pip": ["requests"]
      },
      "primaryEnv": "X2C_API_KEY",
      "installSpec": {
        "bins": ["python3"],
        "env": ["X2C_API_KEY"],
        "pip": ["requests"]
      }
    }
  }
---

[简体中文](./SKILL.zh-CN.md) | English

# X2C Social Poster

**Source**: [storyclaw-official/skills](https://github.com/storyclaw-official/skills) · Dashboard: [x2cpool.com](https://x2cpool.com/)

Publish posts, manage comments, run analytics, send DMs, and generate AI content across 13+ social platforms via X2C Open API.

---

## Installation Requirements

| Requirement | Value |
|-------------|-------|
| **Binary** | `python3` |
| **Environment** | `X2C_API_KEY` (required; obtain from [X2C Dashboard](https://x2cpool.com/)) |
| **Pip** | `requests` |

---

## First-Time Setup Guide

### Step 0: Check API Key

```bash
python3 scripts/x2c_social.py --action check-key
```

- Key is set → proceed to Step 1.
- Key is NOT set → guide the user:

```
🔑 X2C API Key is not configured yet. Let's set it up:

1. Go to https://x2cpool.com and sign up / log in
2. Click "Link Account" to connect your social media accounts
3. Go to Developer → API Keys, create a new key
4. Paste the key here and I'll save it for you
```

### Step 1: Verify Linked Accounts

```bash
python3 scripts/x2c_social.py --action status
```

If no accounts are linked:
```
⚠️ No social accounts linked yet.
Please visit https://x2cpool.com to link your accounts.
```

After showing linked accounts, **proactively offer**:
> "Want to see your account analytics (followers, trends)? I can pull them now. [Yes / Skip]"

---

## Platform Requirements Quick Reference

| Platform | ID | Media Required | Text Limit | Max Media | Supported Types | Key Constraints |
|----------|-----|:---:|---:|:---:|---|---|
| YouTube | `youtube` | ✅ (video) | title:100 desc:5,000 | 1 video | MP4, MOV, AVI, WMV | `--title` auto-generated if missing (max 100 chars). Default visibility = public. |
| Instagram | `instagram` | ✅ | 2,200 | 10 (carousel) | JPEG, PNG, MP4 | Must be Business/Creator. No text-only. Max 5 hashtags, 3 @mentions. |
| TikTok | `tiktok` | ✅ | 2,200 | 1 video or 35 images | MP4, JPG, JPEG, WEBP | Images & video can't mix. **No PNG**. No `\n` in text. AI content must mark `--ai-generated`. |
| X (Twitter) | `twitter` | ❌ | 280 | 4 images or 1 video | JPEG, PNG, GIF, MP4 | Images and videos can't mix. BYO API keys required. |
| Facebook | `facebook` | ❌ | 63,206 | 10+ | JPEG, PNG, MP4 | Must be a Page (not personal). |
| LinkedIn | `linkedin` | ❌ | 3,000 | 9 | JPEG, PNG, GIF, MP4 | Personal or Company page. |
| Pinterest | `pinterest` | ✅ | 500 | 5 (carousel) | JPEG, PNG | Image required. Video requires `--thumbnail`. |
| Reddit | `reddit` | ❌ | title:300 post:40,000 | 1 | JPEG, PNG, GIF, MP4 | `--title` required. `--subreddit` required. |
| GMB | `gmb` | ❌ | 1,500 | 1 | JPEG, PNG, MP4 | Verified business. No phone numbers in text. |
| Bluesky | `bluesky` | ❌ | 300 | 4 | JPEG, PNG, MP4 | 300 chars including links. |
| Threads | `threads` | ❌ | 500 | 10 (carousel) | JPEG, PNG, MP4 | Linked to Instagram account. |
| Snapchat | `snapchat` | ✅ | 160 | 1 | JPEG, PNG, MP4 | Exactly 1 media item. |
| Telegram | `telegram` | ❌ | 4,096 | 1 | JPEG, PNG, GIF, MP4 | Bot + Channel/Group. |

### ⚠️ Multi-Platform Posting Caveat

When posting to multiple platforms simultaneously, the **shortest character limit wins** across all platforms. Use separate publish calls for different text per platform.

---

## Commands

### Existing Commands

#### 1. Check Linked Accounts

```bash
python3 scripts/x2c_social.py --action status
```

#### 2. Publish Post

```bash
# Text-only
python3 scripts/x2c_social.py --action publish \
  --platforms twitter facebook \
  --post "Hello world! 🚀"

# With local file (auto-uploaded, any size up to 5GB)
python3 scripts/x2c_social.py --action publish \
  --platforms tiktok instagram \
  --post "Watch this! 🎬" \
  --media-files /path/to/video.mp4

# With remote URL
python3 scripts/x2c_social.py --action publish \
  --platforms tiktok \
  --post "Watch this! 🎬" \
  --media-urls "https://example.com/video.mp4"

# YouTube (title auto-generated if omitted)
python3 scripts/x2c_social.py --action publish \
  --platforms youtube \
  --post "Video description here" \
  --title "My YouTube Video" \
  --visibility public \
  --media-files /path/to/video.mp4

# Reddit
python3 scripts/x2c_social.py --action publish \
  --platforms reddit \
  --post "Post body text" \
  --title "Discussion: AI in 2026" \
  --subreddit technology

# TikTok with AI content flag
python3 scripts/x2c_social.py --action publish \
  --platforms tiktok \
  --post "AI generated content" \
  --ai-generated \
  --media-files /path/to/video.mp4

# Scheduled post
python3 scripts/x2c_social.py --action publish \
  --platforms tiktok instagram \
  --post "Coming soon! ⏰" \
  --media-files /path/to/video.mp4 \
  --schedule "2026-04-01T12:00:00Z"
```

#### 3. Post History

```bash
python3 scripts/x2c_social.py --action posts
python3 scripts/x2c_social.py --action posts --platform tiktok
```

#### 4. Delete Post

```bash
python3 scripts/x2c_social.py --action delete-post --post-id post_abc123
python3 scripts/x2c_social.py --action delete-post --post-id post_abc123 --bulk
```

#### 5–8. Comments

```bash
# Post a comment
python3 scripts/x2c_social.py --action comment \
  --post-id post_abc123 --platforms tiktok --comment "🔥"

# List comments
python3 scripts/x2c_social.py --action comments --post-id post_abc123 --platform tiktok

# Reply to a comment
python3 scripts/x2c_social.py --action reply \
  --comment-id cmt_xyz --comment "Thanks!"

# Delete a comment
python3 scripts/x2c_social.py --action delete-comment --comment-id cmt_xyz
```

#### 9. Upload Media (standalone)

```bash
python3 scripts/x2c_social.py --action upload --file /path/to/file.mp4 --folder videos
```

---

### New Commands (v2.0)

#### 10. AI Post Generation

Generate platform-optimized post text from a topic or prompt.

```bash
# Basic generation
python3 scripts/x2c_social.py --action generate \
  --gen-prompt "Promote a new AI short drama episode about time loops" \
  --platform tiktok \
  --gen-hashtags \
  --gen-emojis \
  --tone energetic \
  --max-chars 2200

# For Twitter (respects 280-char limit)
python3 scripts/x2c_social.py --action generate \
  --gen-prompt "Launch announcement for X2C social tool" \
  --platform twitter \
  --gen-hashtags \
  --max-chars 280
```

Options: `--tone` accepts `energetic`, `casual`, `professional`, `inspiring`, etc. `--language` accepts `en`, `zh`, `ja`, etc.

#### 11. Hashtag Recommendations

Get AI-ranked hashtags for a topic or post text.

```bash
python3 scripts/x2c_social.py --action hashtags \
  --text "AI generated short drama about time travel" \
  --platform instagram \
  --max-tags 10 \
  --language en
```

#### 12. Auto-Schedule (Best Time)

Publish at the next optimal engagement time — no need to guess the best hour.

```bash
python3 scripts/x2c_social.py --action auto-schedule \
  --platforms tiktok instagram \
  --post "New episode is live! 🎬" \
  --media-files /path/to/video.mp4
```

#### 13. Post Analytics (Published via X2C)

```bash
# Analytics for a specific post
python3 scripts/x2c_social.py --action analytics-post \
  --post-id post_abc123 \
  --platforms instagram tiktok

# With platform-native ID lookup
python3 scripts/x2c_social.py --action analytics-post \
  --post-id native_id_123 \
  --platforms youtube \
  --search-platform-id
```

Analytics availability notes:
- TikTok: 24–48 h delay
- Pinterest: 24–72 h delay
- Instagram: requires ≥ 100 followers
- Facebook: requires ≥ 100 page likes

#### 14. External Post Analytics

Analytics for posts NOT published via X2C.

```bash
# By URL
python3 scripts/x2c_social.py --action analytics-social \
  --platform youtube \
  --url "https://youtube.com/watch?v=VIDEO_ID"

# By native ID
python3 scripts/x2c_social.py --action analytics-social \
  --platform tiktok \
  --ext-id "7123456789"
```

Supported: `youtube`, `tiktok`, `instagram`, `facebook`, `twitter`, `linkedin`.

#### 15. Account Analytics

Followers, audience demographics, and historical trends.

```bash
# Basic account analytics
python3 scripts/x2c_social.py --action analytics-account \
  --platforms instagram youtube tiktok

# With daily trends and 60-day window
python3 scripts/x2c_social.py --action analytics-account \
  --platforms instagram \
  --daily \
  --period-60
```

#### 16. Full Post History

```bash
# All platforms, last 30 days
python3 scripts/x2c_social.py --action history --last-days 30

# Specific platform, last 50 records, successful only
python3 scripts/x2c_social.py --action history \
  --platform instagram \
  --last-records 50 \
  --history-status success
```

#### 17. Platform Feed / Timeline

```bash
python3 scripts/x2c_social.py --action feed \
  --platform twitter \
  --last-records 20
```

#### 18. Direct Messages

```bash
# List DMs
python3 scripts/x2c_social.py --action messages --platform instagram

# Send a DM
python3 scripts/x2c_social.py --action send-message \
  --platform instagram \
  --recipient-id ig_user_id_123 \
  --message "Thanks for watching! 😊"

# Reply in a conversation
python3 scripts/x2c_social.py --action send-message \
  --platform instagram \
  --conversation-id conv_abc \
  --message "Great question!"

# DM with media
python3 scripts/x2c_social.py --action send-message \
  --platform twitter \
  --recipient-id twitter_user_id \
  --message "Check this out!" \
  --media-url "https://cdn.example.com/image.jpg"
```

Supported platforms: `instagram`, `facebook`, `twitter`.

#### 19. Short Links with UTM Tracking

```bash
# Create a trackable short link
python3 scripts/x2c_social.py --action links \
  --link-url "https://x2creel.ai/episode/123" \
  --utm-source instagram \
  --utm-medium bio \
  --utm-campaign drama_s2

# Get click analytics for existing short link
python3 scripts/x2c_social.py --action links \
  --link-id short_link_abc123
```

#### 20. Google Business Reviews

```bash
# Last 30 days of reviews
python3 scripts/x2c_social.py --action reviews --last-days 30
```

#### 21. Brand Lookup

```bash
python3 scripts/x2c_social.py --action brand --domain x2creel.ai
```

Returns brand colors, logo, social links, and description.

---

## Parameter Reference

| Parameter | Actions | Description |
|-----------|---------|-------------|
| `--action` | all | Action to perform |
| `--post` | publish, auto-schedule | Post text content |
| `--platforms` | publish, auto-schedule, analytics-post, analytics-account | Space-separated platform IDs |
| `--platform` | posts, comments, messages, feed, history, analytics-social | Single platform |
| `--media-urls` | publish, auto-schedule | Remote URLs or local paths (auto-uploaded) |
| `--media-files` | publish, auto-schedule | Local file paths to auto-upload |
| `--schedule` | publish | ISO 8601 scheduled publish time |
| `--shorten-links` | publish | Shorten URLs in post text |
| `--title` | publish | Title (YouTube auto-gen if omitted; required for Reddit) |
| `--subreddit` | publish | Target subreddit without `r/` |
| `--visibility` | publish | `public`/`unlisted`/`private` (YouTube) or TikTok equivalents |
| `--thumbnail` | publish | Thumbnail URL for Pinterest video |
| `--ai-generated` | publish | Mark as AI-generated (TikTok) |
| `--post-id` | comment, comments, delete-post, analytics-post | Ayrshare post ID |
| `--comment-id` | reply, delete-comment | Comment ID |
| `--comment` | comment, reply | Comment or reply text |
| `--bulk` | delete-post | Delete from all platforms |
| `--file` | upload | Local file path |
| `--folder` | upload, publish | Upload subfolder (default: `uploads`) |
| `--ext-id` | analytics-social | External platform post/video ID |
| `--url` | analytics-social | Post URL for external analytics |
| `--search-platform-id` | analytics-post | Search by platform native ID |
| `--daily` | analytics-account | Include daily trends |
| `--quarters` | analytics-account | Quarterly aggregation (YouTube) |
| `--period-60` | analytics-account | 60-day rolling window |
| `--last-message-id` | messages | Pagination cursor |
| `--message` | send-message | DM text |
| `--recipient-id` | send-message | Recipient user ID |
| `--conversation-id` | send-message | Conversation ID |
| `--media-url` | send-message | Media URL to attach to DM |
| `--last-records` | history, feed | Max records to return |
| `--last-days` | history, reviews | Look-back window in days |
| `--history-status` | history | Filter: `success` / `failed` / `scheduled` |
| `--text` | hashtags | Topic/text for hashtag recommendations |
| `--max-tags` | hashtags | Max hashtags (default 10) |
| `--language` | hashtags, generate | Language code (en, zh, ja, …) |
| `--auto-schedule-type` | auto-schedule | Strategy: `next` (default) |
| `--gen-prompt` | generate | Topic/prompt for AI generation |
| `--gen-hashtags` | generate | Include hashtags in generated text |
| `--gen-emojis` | generate | Include emojis in generated text |
| `--tone` | generate | Tone: energetic / casual / professional / inspiring |
| `--max-chars` | generate | Max characters for generated text |
| `--link-url` | links | URL to shorten and track |
| `--link-id` | links | Existing short link ID for analytics |
| `--utm-source` | links | UTM source |
| `--utm-medium` | links | UTM medium |
| `--utm-campaign` | links | UTM campaign |
| `--domain` | brand | Domain for brand info lookup |

---

## Interaction Guide

**This is the most important section.** When handling user requests, always follow these principles:

### Core Principle: Lead With a Proposal

Never ask vague questions. Always present a **concrete plan based on what you already know**, then let the user accept, modify, or skip.

| ❌ Don't | ✅ Do instead |
|---------|--------------|
| "Do you want hashtags?" | Run hashtags API and present: "Suggested: `#AIDrama #TikTok #ShortFilm` — add them? [All / Pick / Skip]" |
| "When do you want to post?" | "I'll auto-schedule for best engagement time. [Confirm / Post now / Set time manually: ___]" |
| "Do you want analytics?" | After publish: "Post published! I noted the post ID. TikTok analytics ready in ~24h — ask me to check." |
| "What tone?" | Based on the platform + topic, propose: "I'll use an energetic tone for TikTok. OK? [Yes / Change to: ___]" |

---

### Smart Publishing Flow

When a user wants to create a post, run through this sequence. **Skip steps that the user has already covered.**

#### Phase 1 — Onboarding (once per session)

```bash
python3 scripts/x2c_social.py --action check-key
python3 scripts/x2c_social.py --action status
```

Show linked platforms. After status, proactively offer:
> "You're linked to: TikTok, Instagram, YouTube. Want account analytics too? [Yes / Skip]"

#### Phase 2 — Content Creation

If the user describes a topic but hasn't written the post yet:

```bash
python3 scripts/x2c_social.py --action generate \
  --gen-prompt "[user's topic]" \
  --platform [primary platform] \
  --gen-hashtags --gen-emojis \
  --tone [inferred from context, default: energetic] \
  --language [inferred from user language, default: en]
```

Present 2-3 variations (or the top result) and let the user pick or edit. Do not wait for the user to ask for AI generation — proactively offer it.

#### Phase 3 — Hashtag Suggestions

After the post text is confirmed, **automatically** run:

```bash
python3 scripts/x2c_social.py --action hashtags \
  --text "[confirmed post text]" \
  --platform [primary platform] \
  --max-tags 8
```

Present the top suggestions immediately:
> "Suggested hashtags: `#AIDrama` (high) `#ShortFilm` (high) `#TikTok` (medium). Add all? [Yes / Pick some / Skip]"

If the user says "add all" or picks some, append them to the post text directly.

#### Phase 4 — Platform Checks

Based on the confirmed platforms:
- **YouTube**: confirm title (or show the auto-generated one) and visibility (`public` default).
- **Reddit**: confirm `--title` and `--subreddit`.
- **Instagram/TikTok/Snapchat**: remind media is required; ask for file if not provided.
- **TikTok + AI content**: suggest `--ai-generated`.

#### Phase 5 — Scheduling

Present the scheduling choice **with auto-schedule as the recommended default**:

> "When should I post?
> ✨ **Auto-schedule** — I'll pick the best time for each platform (recommended)
> ⚡ **Post now**
> 🕐 **Set a time** — e.g. 2026-05-01T18:00:00Z
>
> [Auto-schedule] [Now] [Set time]"

- If auto-schedule: use `--action auto-schedule`
- If specific time: use `--action publish --schedule "ISO8601"`
- If now: use `--action publish`

#### Phase 6 — Post-Publish Smart Offers

After a successful publish, **always** offer these in one compact block:

```
✅ Published to [platforms]! Post ID: post_abc123

Quick actions — pick any, or skip all:
🔗 Create trackable short link  → yes/no
📊 Analytics: [platform-specific timing note, e.g. "TikTok ready in ~24h"]
💬 Check/reply to comments?    → yes/no
```

If the post text contained a URL, **auto-propose** creating a short link:
> "Your post includes a URL. Want me to create a trackable short link with UTM tags? I'll use `utm_source=[platform]` automatically. [Yes / No]"

---

### Context-Triggered Proactive Suggestions

Run these checks based on context — no need for the user to ask:

| Context | What to offer | Command |
|---------|--------------|---------|
| After `status` shows linked accounts | "Want account analytics? I can show followers & trends." | `analytics-account --platforms [all linked]` |
| After `posts` / `history` lists results | "Want analytics for any of these? [show post IDs as options]" | `analytics-post --post-id [selected]` |
| GMB is in linked platforms | "You have Google Business linked — want to check recent reviews?" | `reviews --last-days 30` |
| User mentions a website or brand | "Want me to look up brand info for [domain]? Logo, colors, social links." | `brand --domain [domain]` |
| IG, FB, or Twitter is linked | "Want to check your DMs?" | `messages --platform [platform]` |
| User asks for "post history" | Offer full history with filters | `history --last-days 30` |
| Post contains a URL | "Want a trackable short link?" | `links --link-url [url] --utm-source [platform]` |

---

### Determine Intent (when request is vague)

```
What would you like to do?

📝 Create & publish a post      → Smart publishing flow (Phase 1–6 above)
🤖 Generate post ideas          → AI generation + hashtag suggestions
⏰ Auto-schedule a post         → Best-time publishing
📊 Check analytics              → Post or account analytics
💬 Manage comments/DMs          → Comments, replies, or DMs
📜 Browse post history          → Full history with filters
📤 Upload media                 → Standalone upload
🔗 Create a short link          → Link creation + UTM
⭐ Check GMB reviews            → Google Business reviews
🔍 Look up brand info           → Brand lookup
🔗 Check linked accounts        → Status
```

---

## Error Handling

| Code | Meaning | Action |
|------|---------|--------|
| 400 | Missing/invalid parameters | Check platform requirements and fix |
| 401 | Invalid API key | Guide user to verify/reset key at x2cpool.com |
| 402 | Social subscription required | Guide user to check subscription at x2cpool.com |
| 429 | Rate limited | Retry after 5 min |
| 500 | Server error | Retry or inform user |

Analytics delay notes (set expectations proactively):
- **TikTok**: 24–48 h data delay
- **Pinterest**: 24–72 h data delay
- **Instagram**: account analytics require ≥ 100 followers
- **Facebook**: page analytics require ≥ 100 page likes
