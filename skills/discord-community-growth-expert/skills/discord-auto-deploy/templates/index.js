import 'dotenv/config';
import { Client, GatewayIntentBits } from 'discord.js';
import { readFileSync, existsSync } from 'fs';
import Database from 'better-sqlite3';
import { homedir } from 'os';
import { join } from 'path';

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
    GatewayIntentBits.DirectMessages,
  ],
});

const CHANNEL_ID = process.env.DISCORD_CHANNEL_ID;
const GATEWAY_PASSWORD = process.env.GATEWAY_PASSWORD;
const GATEWAY_URL = 'http://localhost:18789/v1/chat/completions';
const MODEL = 'openclaw/default';  // Use default model instead of agent session

// Dynamic paths - works across different users and workspace names
const WORKSPACE_ROOT = process.env.WORKSPACE_ROOT || join(homedir(), '.openclaw', 'workspace-discord-community-growth-expert');
const PROFILE_PATH = join(WORKSPACE_ROOT, 'outputs', 'user_profile.json');
const DASHBOARD_CONFIG_PATH = join(WORKSPACE_ROOT, 'outputs', 'dashboard_config.json');
const DB_PATH = join(homedir(), '.claw', 'shared', 'shared.db');

console.log('🔑 GATEWAY_PASSWORD loaded:', GATEWAY_PASSWORD ? GATEWAY_PASSWORD.slice(0, 4) + '...' : 'MISSING');

function loadProfile() {
  try {
    if (existsSync(PROFILE_PATH)) return JSON.parse(readFileSync(PROFILE_PATH, 'utf-8'));
  } catch (e) { console.error('Could not load user profile:', e.message); }
  return {};
}

function loadDashboardConfig() {
  try {
    if (existsSync(DASHBOARD_CONFIG_PATH)) return JSON.parse(readFileSync(DASHBOARD_CONFIG_PATH, 'utf-8'));
  } catch (e) { console.error('Could not load dashboard config:', e.message); }
  return null;
}

// Parse structured output from Agent — extract only the 推荐回复 section for the user
function parseAgentOutput(text) {
  const result = { reply: '', intent: '', tags: [], highIntent: false, feedback: '' };

  const replyMatch = text.match(/###\s*推荐回复\s*\n([\s\S]*?)(?=\n###|$)/);
  if (replyMatch) result.reply = replyMatch[1].trim();

  const intentMatch = text.match(/###\s*用户意图判断\s*\n([\s\S]*?)(?=\n###|$)/);
  if (intentMatch) result.intent = intentMatch[1].trim().split('\n')[0];

  const tagsMatch = text.match(/###\s*粉丝标签\s*\n([\s\S]*?)(?=\n###|$)/);
  if (tagsMatch) {
    result.tags = tagsMatch[1]
      .split('\n')
      .map(l => l.replace(/^[-*]\s*/, '').trim())
      .filter(Boolean);
  }

  const hiMatch = text.match(/###\s*是否高意向\s*\n([\s\S]*?)(?=\n###|$)/);
  if (hiMatch) result.highIntent = /^yes/i.test(hiMatch[1].trim());

  const fbMatch = text.match(/###\s*需要反馈给团队的问题\s*\n([\s\S]*?)(?=\n###|$)/);
  if (fbMatch) result.feedback = fbMatch[1].trim();

  return result;
}

// Update dashboard widgets with new interaction data (synchronous better-sqlite3)
function updateDashboard(parsed, username) {
  const cfg = loadDashboardConfig();
  if (!cfg || !cfg.enabled || !cfg.module_id) return;

  try {
    const db = new Database(DB_PATH);
    const now = new Date().toISOString().slice(0, 16).replace('T', ' ');

    // Dynamically fetch widget IDs by title — never rely on hardcoded IDs
    const widgetRows = db.prepare('SELECT id, title FROM dashboard_widgets WHERE module_id = ?').all(cfg.module_id);
    const w = {};
    for (const row of widgetRows) {
      if (row.title.includes('高频问题'))      w.frequent_questions  = row.id;
      if (row.title.includes('高意向用户'))    w.high_intent_users   = row.id;
      if (row.title.includes('需要反馈'))      w.feedback_issues     = row.id;
      if (row.title.includes('用户意图分布'))  w.intent_distribution = row.id;
      if (row.title.includes('粉丝标签'))      w.tag_distribution    = row.id;
      if (row.title.includes('关键指标'))      w.key_metrics         = row.id;
    }

    const getWidget = db.prepare('SELECT data FROM dashboard_widgets WHERE id = ?');
    const setWidget = db.prepare("UPDATE dashboard_widgets SET data = ?, updated_at = datetime('now') WHERE id = ?");

    // Intent distribution (pie chart)
    const intentLabels = ['咋询', '夸赞', '质疑', '求资料', '合作', '投诉', '购买'];
    const intentIdx = intentLabels.findIndex(k => parsed.intent.includes(k));
    if (intentIdx >= 0 && w.intent_distribution) {
      const row = getWidget.get(w.intent_distribution);
      if (row) {
        const data = JSON.parse(row.data);
        data[intentIdx] = (data[intentIdx] || 0) + 1;
        setWidget.run(JSON.stringify(data), w.intent_distribution);
      }
    }

    // High-intent users table
    if (parsed.highIntent && w.high_intent_users) {
      const row = getWidget.get(w.high_intent_users);
      if (row) {
        let data = JSON.parse(row.data);
        if (data.length === 1 && data[0].User === '待收集...') data = [];
        data.unshift({ User: username, Intent: parsed.intent, Tags: parsed.tags.slice(0, 2).join(', '), Time: now });
        if (data.length > 20) data = data.slice(0, 20);
        setWidget.run(JSON.stringify(data), w.high_intent_users);
      }
    }

    // Feedback issues table
    if (parsed.feedback && !parsed.feedback.startsWith('暂无') && w.feedback_issues) {
      const row = getWidget.get(w.feedback_issues);
      if (row) {
        let data = JSON.parse(row.data);
        if (data.length === 1 && data[0].Issue === '待收集...') data = [];
        data.unshift({ Issue: parsed.feedback.slice(0, 80), Type: parsed.intent, Priority: parsed.highIntent ? '高' : '普通', Time: now });
        if (data.length > 20) data = data.slice(0, 20);
        setWidget.run(JSON.stringify(data), w.feedback_issues);
      }
    }

    // Key metrics — increment total messages and high-intent count
    if (w.key_metrics) {
      const row = getWidget.get(w.key_metrics);
      if (row) {
        const data = JSON.parse(row.data);
        const totalIdx = data.findIndex(d => d.label === '总消息数');
        const hiIdx = data.findIndex(d => d.label === '高意向用户');
        if (totalIdx >= 0) data[totalIdx].value = String(parseInt(data[totalIdx].value || '0') + 1);
        if (hiIdx >= 0 && parsed.highIntent) data[hiIdx].value = String(parseInt(data[hiIdx].value || '0') + 1);
        setWidget.run(JSON.stringify(data), w.key_metrics);
      }
    }

    db.close();
    console.log(`📊 Dashboard updated — intent: ${parsed.intent}, highIntent: ${parsed.highIntent}`);
  } catch (e) {
    console.error('Dashboard update failed:', e.message);
  }
}

client.on('ready', () => {
  console.log(`✅ Bot logged in as ${client.user.tag}`);
  console.log(`📡 Listening on channel: ${CHANNEL_ID}`);
});

client.on('messageCreate', async (message) => {
  if (message.author.bot || message.webhookId) return;

  const isDM = message.channel.type === 1;
  if (message.channelId !== CHANNEL_ID && !isDM) return;

  console.log(`📨 Message from ${message.author.username}: ${message.content.slice(0, 80)}`);

  try { await message.channel.sendTyping(); } catch (_) {}

  const profile = loadProfile();
  const systemPrompt = `你是一个 Discord 社群增长助手，专注于大模型动态社群的运营。

用户画像：
- 内容方向：${profile.content_focus || '大模型动态'}
- 回复风格：${profile.reply_style || '硬核技术派'}
- 目标受众：${profile.target_audience || '开发者'}
- 社群规则：${profile.community_rules || '禁止广告、互相尊重、不水群'}

请按以下格式输出（每个 ### 标题都必须包含）：

### 用户意图判断
[咋询 / 夸赞 / 质疑 / 求资料 / 合作 / 投诉 / 购买 中选一个，可加括号补充]

### 粉丝标签
- [标签1]
- [标签2]
- [标签3]

### 推荐回复
[直接发给用户的消息。结构：先回应问题 → 补充有用信息 → 给出轻行动。风格自然，不生硬，不硬推产品]

### 下一步引导
[引导用户进入下一步]

### 是否高意向
[Yes 或 No] — [一句话原因]

### 需要反馈给团队的问题
[高频问题 / 内容空白 / 高意向线索，如无则写"暂无"]`;

  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 60000);

    const response = await fetch(GATEWAY_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${GATEWAY_PASSWORD}`,
      },
      body: JSON.stringify({
        model: MODEL,
        messages: [
          { role: 'system', content: systemPrompt },
          { role: 'user', content: message.content },
        ],
        max_tokens: 1000,
        temperature: 0.8,
      }),
      signal: controller.signal,
    });

    clearTimeout(timeout);

    if (!response.ok) {
      const errText = await response.text();
      console.error(`Gateway error ${response.status}:`, errText);
      return;
    }

    const data = await response.json();
    const fullOutput = data.choices?.[0]?.message?.content?.trim();

    if (!fullOutput) {
      console.warn('Empty reply from gateway');
      return;
    }

    console.log('📝 Full agent output:\n' + fullOutput.slice(0, 300));

    // Parse and extract only the 推荐回复 for the user
    const parsed = parseAgentOutput(fullOutput);

    if (parsed.reply) {
      const trimmed = parsed.reply.length > 2000 ? parsed.reply.slice(0, 1997) + '...' : parsed.reply;
      await message.reply(trimmed);
      console.log(`✅ Replied to ${message.author.username} (intent: ${parsed.intent})`);
    } else {
      // Fallback: Agent didn't follow format, make a second call with simpler prompt
      console.warn(`⚠️ Parse failed, retrying with simple prompt for ${message.author.username}`);
      
      const simplePrompt = `你是一个 Discord 社群助手。用户画像：${profile.reply_style || '硬核技术派'}风格，面向${profile.target_audience || '开发者'}。\n\n直接回复用户的消息，不要输出任何分析或标签，只输出可以直接发送的回复内容。`;
      
      const fallbackResponse = await fetch(GATEWAY_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${GATEWAY_PASSWORD}`,
        },
        body: JSON.stringify({
          model: MODEL,
          messages: [
            { role: 'system', content: simplePrompt },
            { role: 'user', content: message.content },
          ],
          max_tokens: 500,
          temperature: 0.8,
        }),
        signal: AbortSignal.timeout(60000),
      });
      
      if (fallbackResponse.ok) {
        const fallbackData = await fallbackResponse.json();
        const fallbackReply = fallbackData.choices?.[0]?.message?.content?.trim();
        if (fallbackReply) {
          const trimmed = fallbackReply.length > 2000 ? fallbackReply.slice(0, 1997) + '...' : fallbackReply;
          await message.reply(trimmed);
          console.log(`✅ Replied with fallback for ${message.author.username}`);
        }
      } else {
        console.error('Fallback call also failed');
      }
    }

    // Update dashboard in background
    updateDashboard(parsed, message.author.username);

  } catch (err) {
    if (err.name === 'AbortError') {
      console.error('Gateway request timed out after 30s');
    } else {
      console.error('Error handling message:', err.message);
    }
  }
});

client.on('error', (err) => {
  console.error('Discord client error:', err);
});

client.login(process.env.DISCORD_TOKEN).catch((err) => {
  console.error('Failed to login:', err.message);
  process.exit(1);
});
