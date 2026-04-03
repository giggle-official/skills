# Giggle Pro External - 部署指南

这份指南帮助你在树莓派或其他设备上部署 giggle-pro-external skill。

---

## 📦 文件清单

导出前确保包含以下文件：

```
giggle-pro-external/
├── README.md                      ✅ 快速开始
├── SKILL.md                       ✅ 完整文档
├── DEPLOYMENT-GUIDE.md            ✅ 本文件
├── X2C-API-REQUIREMENTS.md        ✅ API规格（给X2C团队）
├── config.example.json            ✅ 配置模板
│
├── scripts/
│   ├── ad-account-manager.js      ✅ 账号管理
│   ├── ad-writer.js               ✅ 编剧
│   ├── ad-producer.js             ✅ 视频生产
│   ├── auto-generate.js           ✅ 全流程
│   ├── quality-check.js           ✅ 质量检查
│   ├── estimate-cost.js           ✅ 成本估算
│   ├── drama_manager.py           ✅ Python编剧脚本
│   └── ad-writer-requirements.txt ✅ Python依赖
│
└── references/                    ✅ API文档
    ├── api-docs.md
    ├── QUALITY-AND-RETRY.md
    ├── quality-scoring.md
    └── ...
```

---

## 🚀 树莓派部署流程

### 1. 系统要求

**硬件:**
- Raspberry Pi 4 (4GB+ RAM 推荐)
- SD卡 32GB+
- 网络连接

**软件:**
- Raspbian/Ubuntu (64-bit)
- Node.js 16+
- Python 3.8+
- ffmpeg（用于质量检查）

### 2. 安装依赖

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装 Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# 安装 Python 3
sudo apt install -y python3 python3-pip

# 安装 ffmpeg
sudo apt install -y ffmpeg

# 验证安装
node --version   # 应该 >= 16
python3 --version  # 应该 >= 3.8
ffmpeg -version
```

### 3. 部署 Skill

```bash
# 创建目录
mkdir -p /home/pi/clawd/skills
cd /home/pi/clawd/skills

# 复制文件（或从备份恢复）
tar -xzf giggle-pro-external.tar.gz

# 或直接 git clone（如果有仓库）
# git clone <repo_url> giggle-pro-external

cd giggle-pro-external
```

### 4. 安装 Python 依赖

```bash
cd scripts
pip3 install -r ad-writer-requirements.txt

# 如果遇到权限问题
pip3 install --user -r ad-writer-requirements.txt
```

### 5. 配置文件

```bash
# 复制配置模板
cp config.example.json config.json

# Giggle API key 已经包含在模板里（内部key）
# x2cApiKey 留空，用户首次使用时绑定
```

### 6. 设置权限

```bash
chmod +x scripts/ad-account-manager.js
chmod +x scripts/ad-writer.js
chmod +x scripts/ad-producer.js
chmod +x scripts/auto-generate.js
```

### 7. 测试运行

```bash
# 测试 ad-account-manager
node scripts/ad-account-manager.js help

# 测试 ad-writer（会提示绑定账号）
node scripts/ad-writer.js "测试创意"

# 测试 ad-producer（会提示绑定账号）
node scripts/ad-producer.js list-projects
```

---

## 👤 用户首次使用流程

用户拿到树莓派后，第一次使用流程：

### 方法A：通过 Clawdbot（推荐）

用户在 Telegram 里：

```
用户: 帮我生成一个短剧
Bot: 检测到你还没有绑定X2C账号...
     1. 访问 https://x2creel.ai 注册
     2. 获取你的API key
     3. 把key发给我

用户: sk_x2c_abc123...
Bot: ✅ 账号绑定成功！
     当前余额: 1000 credits ($10.00)
     可以开始生成短剧了~

用户: 生成一个关于程序员救CEO的短剧
Bot: ✍️ 正在生成剧本...
     🎬 正在生成视频...
     [25分钟后]
     ✅ 完成！视频链接: https://...
```

Bot 背后的逻辑：
1. 收到生成请求
2. 调用 `ad-account-manager.checkBinding()`
3. 如果未绑定 → 引导用户注册绑定
4. 如果已绑定 → 调用 `ad-writer` + `ad-producer`

### 方法B：直接命令行

如果用户可以SSH到树莓派：

```bash
# 1. 绑定账号
node scripts/ad-account-manager.js bind

# 2. 生成短剧
node scripts/auto-generate.js "剧名" "创意" --aspect 9:16
```

---

## 🔐 X2C账号注册流程

**前提:** X2C平台 (https://x2creel.ai) 已部署

### 用户注册步骤：

1. **访问网站**  
   https://x2creel.ai

2. **注册账号**
   - 邮箱 + 密码
   - 或社交登录（Google/GitHub等）

3. **充值**
   - 新用户赠送1000 credits（可选）
   - 或购买套餐（如 5000 credits = $50）

4. **生成API Key**
   - 导航到 Settings → API Keys
   - 点击 "Generate New Key"
   - 复制 key（格式: `sk_x2c_...`）

5. **绑定到设备**
   - 在Telegram告诉Bot
   - 或在树莓派运行: `node scripts/ad-account-manager.js bind --key "sk_x2c_..."`

---

## 💰 计费逻辑

### 扣费时机

1. **ad-writer** - 剧本生成完成后
   - 成本: 100 credits
   - 失败不扣费

2. **ad-producer** - 视频生成完成后
   - 成本: 按实际成功镜头数计算
   - 示例: 12镜头 × 88 credits = 1056 credits
   - 失败镜头不扣费

### 余额不足处理

当余额不足时：
1. 操作前检查余额
2. 如果不足，显示错误并退出
3. 引导用户充值: https://x2creel.ai
4. 用户充值后可继续

### 退款机制（可选）

如果生成严重失败（如全部镜头都失败）：
- 可以通过X2C平台申请退款
- 或自动回退积分（需要X2C API支持 refund endpoint）

---

## 🛡️ 安全考虑

### API Key 安全

- ✅ 存储在本地 `config.json`（仅用户可读）
- ✅ 显示时自动脱敏（前6位+后6位）
- ✅ 不记录到日志
- ✅ HTTPS传输

### 文件权限

```bash
# config.json 仅用户可读写
chmod 600 config.json

# 脚本可执行
chmod 755 scripts/*.js
chmod 644 scripts/*.py
```

### 网络安全

- 所有API调用使用 HTTPS
- X2C API: https://api.x2creel.ai
- Giggle API: https://giggle.pro

---

## 📊 监控与日志

### 用户使用统计

可以通过X2C平台查看：
- 每日生成次数
- 消费金额
- 余额变化
- 错误率

### 本地日志

生成过程中的日志保存在：
```
output/<project_id>/
├── qc-report.json      # 质量检查报告
└── generation.log      # 生成日志
```

---

## 🔄 更新与维护

### Skill 更新

```bash
cd /home/pi/clawd/skills/giggle-pro-external

# 备份配置
cp config.json config.json.bak

# 更新文件
tar -xzf giggle-pro-external-v1.1.0.tar.gz

# 恢复配置
cp config.json.bak config.json

# 重启服务（如果有）
sudo systemctl restart clawdbot
```

### Python 依赖更新

```bash
cd scripts
pip3 install --upgrade -r ad-writer-requirements.txt
```

---

## 🧪 测试清单

部署后测试：

```bash
# 1. 测试账号管理
node scripts/ad-account-manager.js bind --key "sk_x2c_test123"
node scripts/ad-account-manager.js balance
node scripts/ad-account-manager.js info
node scripts/ad-account-manager.js unbind

# 2. 测试编剧（需要真实账号）
node scripts/ad-account-manager.js bind --key "你的真实key"
node scripts/ad-writer.js "一个简单的测试剧本" --episode 1

# 3. 测试视频生产（需要真实账号+余额）
node scripts/ad-producer.js list-projects

# 4. 测试全流程（需要充足余额）
node scripts/auto-generate.js "测试短剧" "一个简单的故事" --aspect 9:16 --duration 60
```

---

## ❓ 故障排查

### 问题1: Python 模块找不到

```bash
# 检查 Python 路径
which python3

# 重新安装依赖
cd scripts
pip3 install --user -r ad-writer-requirements.txt
```

### 问题2: 权限被拒绝

```bash
chmod +x scripts/*.js
chmod 644 scripts/*.py
chmod 600 config.json
```

### 问题3: X2C API 连接失败

- 检查网络连接
- 检查 X2C API 是否部署
- 查看错误信息中的 API endpoint

### 问题4: 余额不足

```bash
# 查看当前余额
node scripts/ad-account-manager.js balance

# 引导用户充值
echo "Please top up at: https://x2creel.ai"
```

---

## 📞 技术支持

**内部团队:**
- Stone: 技术负责人
- Roger Wu: 大老板

**文档:**
- 用户文档: `SKILL.md`
- API文档: `X2C-API-REQUIREMENTS.md`
- 本文件: `DEPLOYMENT-GUIDE.md`

**日志位置:**
- Skill日志: `output/<project_id>/`
- 系统日志: `/var/log/clawdbot/`（如果有）

---

## ✅ 部署完成检查

- [ ] Node.js 安装成功 (v16+)
- [ ] Python 安装成功 (v3.8+)
- [ ] ffmpeg 安装成功
- [ ] Python 依赖安装成功
- [ ] config.json 配置正确
- [ ] 脚本权限设置正确
- [ ] 测试 ad-account-manager 成功
- [ ] 测试 ad-writer 成功（至少能检查绑定）
- [ ] 测试 ad-producer 成功（至少能检查绑定）
- [ ] X2C 网站可访问
- [ ] 用户可以注册并获取 API key

---

**版本:** 1.0.0  
**最后更新:** 2026-02-10  
**适用环境:** Raspberry Pi 4, Ubuntu 20.04+
