# 认证与密钥

封装接口使用请求头 **`x-auth`** 传递 API 密钥。

## API Key

1. 打开 [giggle.pro](https://giggle.pro/) 并登录。  
2. 左侧边栏进入 **API Key**（界面亦可能显示为 **API 密钥**）。  
3. 创建或复制密钥，在运行脚本前设置环境变量：

```bash
export GIGGLE_API_KEY="<你的密钥>"
```

若未设置，`tv_avatar_video.py` 会打印简短提示并退出。

可选 **`python-dotenv`**：在项目目录放置 `.env`（勿提交到版本库），例如：

```
GIGGLE_API_KEY=...
GIGGLE_API_BASE=https://giggle.pro
```

## 网关地址

| 变量 | 说明 |
|------|------|
| `GIGGLE_API_BASE` | 可选，默认 `https://giggle.pro`。本地或私有化网关联调时改为对应 origin（无末尾 `/`）。 |

脚本会请求：

- `POST {GIGGLE_API_BASE}/api/v1/generation/tv-avatar-video`
- `GET {GIGGLE_API_BASE}/api/v1/generation/task/query?task_id=...`
