#!/bin/bash
# x2c-real-dashboard setup guide
# Shown automatically when X2C_API_KEY is not configured

cat << 'EOF'
────────────────────────────────────────
  📊 x2c-real-dashboard · 初次设置向导
────────────────────────────────────────

要使用 X2C 数据看板，请完成以下 3 步：

① 注册 / 登录 X2C 平台
   👉 https://www.x2creel.ai

② 获取你的 API Key
   进入「个人中心 → 总览 → API KEY」
   复制格式为 x2c_sk_xxx 的密钥

③ 配置到 OpenClaw
   编辑 ~/.openclaw/openclaw.json，添加：

   {
     "skills": {
       "entries": {
         "x2c-real-dashboard": {
           "enabled": true,
           "apiKey": "x2c_sk_你的KEY"
         }
       }
     }
   }

   或直接设置环境变量：
   export X2C_API_KEY=x2c_sk_你的KEY

完成后重启 OpenClaw / 开启新会话即可使用 🎉
────────────────────────────────────────
EOF

exit 1
