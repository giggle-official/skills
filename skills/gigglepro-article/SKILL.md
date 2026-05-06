---
name: gigglepro-article
description: 使用用户 API Key 完成文章投稿、文章列表翻页/筛选、文章详情查询、以及投稿统计查询。适用于用户要求投稿或查看自己的文章相关信息的场景。
---

# 文章用户 API（投稿/列表/详情/统计）合一 Skill

## 1) 统一前置校验（必须先过）

1. 任何接口调用前，必须先拿到 `X-User-Api-Key`（对用户统一称为 `appKey`）。
2. 若缺失、格式错误、或接口返回 `invalid_user_api_key`，必须先提示并引导用户配置：
   - 请先配置有效的 appKey（即 `X-User-Api-Key`）
   - 配置入口：https://www.gigglepro.com/profile ，进入「我的文章」查看并生成 API Key
3. Key 格式要求：`uak_` + 32 位十六进制字符（正则：`^uak_[0-9a-fA-F]{32}$`）。
4. 必须先验证 key 有效性：调用 `article/categories`，仅当 `code === 0` 才允许进入后续业务流程。
5. 当前会话内已验证成功的 key 要复用；除非再次失效，不要重复要求配置。
6. 硬性门禁：未配置或未验证通过时，禁止进入任何业务参数收集（包括标题、`article_id`、分页参数等）。

### Key 验证请求与成功响应（标准示例）

请求：
```json
{
  "action": "article/categories"
}
```

成功响应（示例）：
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "categories": [
      { "label": "Technology", "value": "technology" },
      { "label": "Business", "value": "business" }
    ]
  }
}
```

校验与缓存规则：
- 必须缓存 `data.categories[].value` 作为投稿分类枚举源。
- 若 `categories` 为空数组，禁止进入投稿流程，并提示用户稍后重试。

## 2) 统一接口契约（生产约束）

- Endpoint：`POST https://swwgusxefvtbdwyoppir.supabase.co/functions/v1/open-api`
- Headers：
  - `Content-Type: application/json; charset=utf-8`
  - `X-User-Api-Key: <appKey>`
- 请求体：统一 JSON；禁止 query 拼参、禁止 `x-www-form-urlencoded`
- 字符编码：统一 UTF-8
- 成功判定：`code === 0`
- 失败判定：`code !== 0`
- 通用响应结构（目标约束）：
  - `code`: number
  - `message`: string
  - `data`: object | null

## 3) 参数类型总表（执行前统一归一化）

- `action`: string，必填
- `title`: string，必填，`1..50` 字符
- `category`: string，必填，必须命中 `categories[].value`
- `summary`: string，可选，`0..200` 字符
- `content`: string，必填，HTML 原文
- `page`: integer，可选，默认 `1`，最小 `1`
- `page_size`: integer，可选，默认 `10`，范围 `1..50`
- `approval_status`: string，可选，枚举 `pending|approved|rejected`
- `article_id`: string，必填，不可空

归一化规则：
- 除 `page`、`page_size` 外，文本字段在发起请求前都转换为 string。
- 禁止对 `content` 做二次 URL 编码或 HTML 转义。
- 可选字段未提供时，不传该字段（不要传空对象或错误类型）。

## 4) 执行状态机（必须遵循）

1. `S0 收到用户意图`
2. `S1 校验 appKey 是否存在且格式合法`
3. `S2 调用 article/categories 验证 key 并缓存分类`
4. `S3 意图路由`：投稿 / 列表 / 详情 / 统计
5. `S4 参数收集与归一化`
6. `S5 发起业务请求`
7. `S6 输出结果（成功字段或失败建议）`

禁止跳步：
- 未到 `S2` 通过前，禁止进入 `S4` 参数收集。
- `invalid_user_api_key` 时，必须回退到 `S1`。

## 5) 业务路由（key 验证成功后执行）

若用户意图不清，先确认要执行：
1) 文章投稿 2) 文章列表 3) 文章详情 4) 文章统计

---

## A. 文章投稿流程（article/submit）

1. 收集参数：
   - 标题（必填）：`请输入文章标题（最多50字）`
   - 分类（必填）：必须从缓存的 `categories[].value` 选择
   - 摘要（选填）：`请填写摘要（简短描述文章内容，最多200字）`
   - 正文（必填）：`请输入富文本正文（HTML）`
2. 参数校验：
   - `title` 不可空，长度 `<= 50`
   - `category` 必须命中分类枚举
   - `summary` 若提供，长度 `<= 200`
   - `content` 不可空，且为 HTML 原文
3. 请求：
```json
{
  "action": "article/submit",
  "title": "<title>",
  "category": "<category>",
  "summary": "<summary>",
  "content": "<html_content>"
}
```
4. 成功响应（示例）：
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "article": {
      "id": "art_123",
      "approval_status": "pending",
      "created_at": "2026-04-29T09:00:00Z"
    }
  }
}
```
5. 输出给用户：
   - 必须输出：`article.id`、`approval_status`、`created_at`

---

## B. 文章列表流程（article/list）

1. 收集参数：
   - `page`（可选，整数，默认 `1`）
   - `page_size`（可选，整数，默认 `10`，最大 `50`）
   - `approval_status`（可选，`pending|approved|rejected`）
2. 非法值处理：
   - `page < 1` 或非整数：提示修正并重问；用户未明确修正则回退 `1`
   - `page_size` 越界或非整数：提示修正并重问；用户未明确修正则回退 `10`
   - `approval_status` 非枚举值：提示可选值并重问；未提供则不传
3. 请求：
```json
{
  "action": "article/list",
  "page": 1,
  "page_size": 10,
  "approval_status": "pending"
}
```
4. 成功响应（示例）：
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "page": 1,
    "page_size": 10,
    "total": 23,
    "items": [
      {
        "id": "art_123",
        "title": "Title",
        "category": "technology",
        "approval_status": "approved",
        "points_awarded": 30,
        "created_at": "2026-04-28T08:00:00Z"
      }
    ]
  }
}
```
5. 输出给用户：
   - 分页：`page`、`page_size`、`total`
   - 列表项：`id`、`title`、`category`、`approval_status`、`points_awarded`、`created_at`

---

## C. 文章详情流程（article/detail）

1. 收集参数：
   - `article_id`（必填，string，不可空）
2. 非法值处理：
   - 空值或无效格式时，提示重新提供，不得直接请求
3. 请求：
```json
{
  "action": "article/detail",
  "article_id": "<article_id>"
}
```
4. 成功响应（示例）：
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": "art_123",
    "title": "Title",
    "category": "technology",
    "summary": "Summary",
    "approval_status": "rejected",
    "rejection_reason": "reason text",
    "points_awarded": 0,
    "created_at": "2026-04-28T08:00:00Z",
    "updated_at": "2026-04-28T10:00:00Z",
    "content": "<p>HTML content</p>"
  }
}
```
5. 输出给用户：
   - `id`、`title`、`category`、`summary`
   - `approval_status`、`rejection_reason`、`points_awarded`
   - `created_at`、`updated_at`、`content`

---

## D. 文章统计流程（article/stats）

1. 请求：
```json
{
  "action": "article/stats"
}
```
2. 成功响应（示例）：
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "total": 23,
    "pending": 2,
    "approved": 18,
    "rejected": 3,
    "points_awarded_total": 260
  }
}
```
3. 输出给用户：
   - `total`、`pending`、`approved`、`rejected`、`points_awarded_total`

---

## 6) 统一错误处理（执行前后都适用）

- `invalid_user_api_key`：
  - 提示去「我的文章」重新生成/复制 appKey
  - 强制回到 key 校验流程（先 `article/categories` 验证）
- `invalid_category`：
  - 重新拉取 `article/categories`
  - 要求用户从最新枚举值重新选择
- `article_not_found`：
  - 提示文章不存在或不属于当前 key 对应用户
- 其他业务错误：
  - 原样输出 API `message`
  - 提供下一步建议（重试、修正参数、稍后再试）

重试策略（标准化）：
- 网络抖动/超时类错误：自动重试 1 次（指数退避 1s）
- 参数校验类错误：不自动重试，必须修正参数
- `invalid_user_api_key`：不自动重试业务接口，必须先完成 key 重新验证

## 7) 标准输出模板（面向用户）

- 成功输出：
  - `操作结果：成功`
  - `关键字段：<按各接口要求输出>`
- 失败输出：
  - `操作结果：失败`
  - `失败原因：<message 或标准错误码解释>`
  - `下一步建议：<可执行动作>`

