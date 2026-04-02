# 🎬 News-to-Video Monetizer (x2c自动化)

一键将全网热点新闻变成可以赚钱的短视频。

## 它能做什么

- **自动采集** — 实时抓取抖音、微博、B站等平台热搜
- **智能筛选** — 按你设定的赛道和关键词匹配最有价值的话题
- **AI制作** — 自动生成剧本、角色、分镜、渲染视频（10-20分钟）
- **自动发布** — 视频完成后直接发布到 X2C 平台
- **流量变现** — 审核通过即获得流量分成，收益每日释放

## 前置条件

1. **OpenClaw** 已安装并运行
2. **X2C 账号** — 在 https://www.x2creel.ai 注册，获取 API Key
3. **积分** — 每个60秒视频消耗约 309 积分（$3.09）

## 安装

### 1. 安装依赖 Skills

```bash
openclaw skill install dailyhot-api
openclaw skill install storyclaw-x2c-ai-director
openclaw skill install storyclaw-x2c-publish
```

### 2. 创建 Agent

```bash
openclaw agent create news-to-video-monetizer
```

### 3. 首次对话

直接和 agent 说话，它会自动引导你完成：
1. 绑定 X2C API Key
2. 设置内容方向（赛道 + 关键词 + 受众）
3. 设置视频参数（风格 + 分类 + 时长）

## 使用

| 说这个 | 它会做这个 |
|--------|-----------|
| 一键制作 | 全流程：采集 → 筛选 → 制作 → 发布 |
| 查看热点 | 展示全网实时热搜 |
| 做一个关于 [话题] 的视频 | 指定话题制作 |
| 查看今日任务 | 所有任务状态 |
| 查看收益 | 账户余额 + 流水 |
| 修改配置 | 调整赛道 / 关键词 / 视频参数 |
| draft mode | 只制作不发布 |

## 成本

| 项目 | 积分 | 价格 |
|------|------|------|
| 剧本（短视频） | 10 | $0.10 |
| 视频 60秒 | 299 | $2.99 |
| 视频 120秒 | 599 | $5.99 |
| 视频 180秒 | 799 | $7.99 |
| 视频 300秒 | 999 | $9.99 |

## 技术架构

```
用户 → x2c自动化 Agent
           │
           ├── dailyhot-api (本地服务)
           │     └── 热点采集 (抖音/微博/B站/头条/快手...)
           │
           ├── storyclaw-x2c-ai-director (X2C Cloud API)
           │     ├── script/generate → AI 编剧
           │     ├── video/produce → 视频渲染
           │     └── video/query → 进度查询
           │
           └── storyclaw-x2c-publish (X2C Cloud API)
                 ├── distribution/publish → 发布
                 ├── distribution/query → 审核状态
                 ├── wallet/balance → 余额
                 └── wallet/transactions → 流水
```

### Task 生命周期（5 节点）

```
采集 → 筛选 → 制作 → 发布 → 审核 ✅ 完成
```

- 收益为账户级数据，不绑定单个 Task
- 视频存储在 X2C 云端，本地只保存 Task 元数据
- 核心流程零模型依赖（不需要 OpenAI / Gemini 等 API Key）

## 文件结构

```
workspace-news-to-video-monetizer/
├── README.md              # 本文件
├── AGENTS.md              # Agent 操作规则
├── BOOTSTRAP.md           # 首次启动引导
├── SOUL.md                # 人格定义
├── IDENTITY.md            # 身份标识
├── USER.md                # 用户指令手册
├── TOOLS.md               # 环境特定配置
├── config.json            # 运行时配置
├── config.template.json   # 配置模板（首次安装用）
├── schemas/
│   └── task-schema.json   # Task 生命周期定义
└── tasks/
    ├── TASK-*.json        # 活跃任务记录
    └── archive/           # 过期任务归档
```

## License

MIT
