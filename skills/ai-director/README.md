# Giggle Pro External - 完整的AI短剧生成解决方案

这是一个独立的、可导出的 skill，集成了账号管理、编剧和视频生产三大功能。

---

## 📦 项目结构

```
giggle-pro-external/
├── README.md                      # 本文件
├── SKILL.md                       # 完整使用文档
├── X2C-API-REQUIREMENTS.md        # X2C API接口规格
├── config.json                    # 配置文件（存储API keys）
├── config.example.json            # 配置文件模板
│
├── scripts/                       # 核心脚本
│   ├── ad-account-manager.js      # 账号管理模块
│   ├── ad-writer.js               # 编剧模块
│   ├── ad-producer.js             # 视频生产模块
│   ├── auto-generate.js           # 一键全流程
│   ├── quality-check.js           # 质量检查
│   ├── estimate-cost.js           # 成本估算
│   ├── drama_manager.py           # 编剧Python脚本
│   └── ad-writer-requirements.txt # Python依赖
│
└── references/                    # API文档
    ├── api-docs.md
    ├── QUALITY-AND-RETRY.md
    ├── quality-scoring.md
    └── ...
```

---

## 🚀 三大核心模块

### 1️⃣ Ad Account Manager（账号管理）

**文件:** `scripts/ad-account-manager.js`

**功能:**
- ✅ X2C账号绑定/解绑
- ✅ 余额查询
- ✅ API key验证
- ✅ 积分扣除（内部调用）

**独立使用:**
```bash
# 绑定账号
node scripts/ad-account-manager.js bind

# 查询余额
node scripts/ad-account-manager.js balance

# 查看账号信息
node scripts/ad-account-manager.js info

# 解绑账号
node scripts/ad-account-manager.js unbind
```

**依赖:** 无（完全独立）

---

### 2️⃣ Ad Writer（编剧）

**文件:** `scripts/ad-writer.js` + `scripts/drama_manager.py`

**功能:**
- ✅ 从创意点子生成完整剧本
- ✅ 斯皮尔伯格温情风格
- ✅ 工业化短剧结构
- ✅ 三线并行叙事

**使用示例:**
```bash
node scripts/ad-writer.js "一个程序员意外拯救了CEO" --episode 1
```

**依赖:** 
- ⚠️ 需要先绑定X2C账号
- 📦 Python 3.x + 依赖（见 ad-writer-requirements.txt）

**成本:** ~100 credits/剧本

---

### 3️⃣ Ad Producer（视频生产）

**文件:** `scripts/ad-producer.js`

**功能:**
- ✅ 7步完整workflow（剧本→视频）
- ✅ 质量检查与智能重试
- ✅ 多模型支持（wan25, kling25, minimax等）
- ✅ 项目管理（列表、状态查询）

**使用示例:**
```bash
# 创建项目
node scripts/ad-producer.js create-project "我的短剧" --aspect 9:16

# 生成剧本
node scripts/ad-producer.js generate-script <project_id> "剧本内容"

# 生成视频（7步完整流程）
node scripts/ad-producer.js generate-characters <project_id>
node scripts/ad-producer.js generate-storyboard <project_id>
node scripts/ad-producer.js generate-images <project_id>
node scripts/ad-producer.js generate-videos <project_id>
node scripts/ad-producer.js export <project_id>

# 查看所有项目
node scripts/ad-producer.js list-projects
```

**依赖:** 
- ⚠️ 需要先绑定X2C账号

**成本:** ~1200 credits/12镜头视频

---

## 🔐 账号绑定要求

**重要:** ad-writer 和 ad-producer 在使用前会自动检查账号绑定状态。

### 如果未绑定：

执行 `ad-writer` 或 `ad-producer` 时会显示：

```
═══════════════════════════════════════════════════════════
❌ X2C Account Not Bound
═══════════════════════════════════════════════════════════

You must bind your X2C account before using this module.

Please run:
  node scripts/ad-account-manager.js bind

Or visit: https://x2creel.ai to get your API key
```

### 绑定流程：

```bash
# 方法1：交互式绑定
node scripts/ad-account-manager.js bind

# 方法2：直接提供key
node scripts/ad-account-manager.js bind --key "sk_x2c_your_key_here"
```

---

## 💰 成本估算

| 模块 | 操作 | 成本 |
|------|------|------|
| Ad Writer | 生成1集剧本 | ~100 credits ($1.00) |
| Ad Producer | 生成12镜头视频 | ~1200 credits ($12.00) |
| **总计** | 完整短剧（剧本+视频） | **~1300 credits ($13.00)** |

**注意:**
- 余额不足时会自动提示充值
- 失败操作不扣费
- 扣费发生在操作成功完成后

---

## 🎯 使用场景

### 场景A：只需要剧本

```bash
# 1. 绑定账号（首次）
node scripts/ad-account-manager.js bind

# 2. 生成剧本
node scripts/ad-writer.js "你的创意点子" --episode 1

# 输出：完整剧本（文本）
```

### 场景B：只需要视频（已有剧本）

```bash
# 1. 绑定账号（首次）
node scripts/ad-account-manager.js bind

# 2. 创建项目并生成视频
node scripts/ad-producer.js create-project "剧名" --aspect 9:16
node scripts/ad-producer.js generate-script <proj_id> "你的剧本"
# ... 后续7步

# 输出：视频下载链接
```

### 场景C：全流程自动化

```bash
# 1. 绑定账号（首次）
node scripts/ad-account-manager.js bind

# 2. 一键生成
node scripts/auto-generate.js "剧名" "创意点子" \
  --aspect 9:16 \
  --duration 60 \
  --quality-check \
  --auto-retry

# 输出：完整剧本 + 视频下载链接
```

---

## 🛠️ 安装与配置

### 1. Python 环境（ad-writer需要）

```bash
cd scripts
pip3 install -r ad-writer-requirements.txt
```

### 2. 配置文件

复制模板：
```bash
cp config.example.json config.json
```

编辑 `config.json`:
```json
{
  "x2cApiKey": "",  // 通过 ad-account-manager bind 自动填充
  "apiKey": "sk_prod_...",  // Giggle API key（视频生产）
  "anthropicApiKey": "sk-ant-..."  // Claude API key（质量检查，可选）
}
```

### 3. 绑定X2C账号

```bash
node scripts/ad-account-manager.js bind
```

---

## 🔄 模块交互流程

```
用户输入创意
     ↓
[1] ad-account-manager: 检查账号绑定 ✅
     ↓
[2] ad-writer: 生成剧本 📝
     ├── 检查余额 (100 credits)
     ├── 调用 drama_manager.py
     ├── 扣费 (-100 credits)
     └── 返回剧本
     ↓
[3] ad-producer: 生成视频 🎬
     ├── 检查余额 (~1200 credits)
     ├── 7步workflow (create → script → characters → storyboard → images → videos → export)
     ├── 扣费 (-1200 credits)
     └── 返回视频链接
     ↓
最终输出：剧本 + 视频
```

---

## 📋 导出为独立 Skill

这个 `giggle-pro-external` 文件夹可以直接作为一个独立的 skill 导出：

```bash
# 打包
tar -czf giggle-pro-external.tar.gz giggle-pro-external/

# 或复制到新环境
cp -r giggle-pro-external /path/to/new/environment/skills/
```

**包含:**
- ✅ 三个核心模块（account + writer + producer）
- ✅ 完整文档（SKILL.md + X2C-API-REQUIREMENTS.md）
- ✅ 所有依赖脚本
- ✅ 配置模板

**不包含:**
- ❌ API keys（需要用户自己绑定）
- ❌ Python虚拟环境（需要用户安装依赖）

---

## 🔍 常见问题

### Q: ad-writer 和 ad-producer 可以单独使用吗？

A: 可以，但都需要先通过 `ad-account-manager` 绑定账号。

### Q: ad-account-manager 必须使用吗？

A: 是的，所有扣费操作都通过它进行。它是整个系统的认证和计费中心。

### Q: 如果X2C API还没部署怎么办？

A: Skill会自动进入"模拟模式"：接受格式正确的API key，显示警告，允许操作继续（不实际扣费）。

### Q: 如何重置账号？

```bash
# 解绑当前账号
node scripts/ad-account-manager.js unbind

# 绑定新账号
node scripts/ad-account-manager.js bind --key "新key"
```

---

## 📖 更多文档

- **使用指南**: `SKILL.md`
- **X2C API规格**: `X2C-API-REQUIREMENTS.md`
- **质量检查**: `references/QUALITY-AND-RETRY.md`
- **Giggle API**: `references/api-docs.md`

---

## 📞 技术支持

遇到问题？
1. 检查账号绑定: `node scripts/ad-account-manager.js info`
2. 检查余额: `node scripts/ad-account-manager.js balance`
3. 查看日志: `output/<project_id>/`
4. 查阅文档: `SKILL.md`

---

**版本:** 1.0.0  
**适用场景:** 商业化树莓派部署、B端创作工具、付费短剧生成服务
