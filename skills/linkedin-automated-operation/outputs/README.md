# 输出目录说明

此目录用于存储 LinkedIn 图文 Agent 运行产物。

## 目录结构

- `briefs/` - 热点提炼卡
- `scripts/` - 帖子文案（`*_post.md`）
- `images/` - 生成的图片素材（`*_image.png`）
- `logs/` - 运行日志与发布日志
- `pool/` - 热点数据池
- `reports/` - 生产报告（永久保留）

## 注意事项

- 除 `reports/` 外，其它目录会按策略定期清理
- 发布依赖 `scripts` 与 `images` 文件，请勿手动删除当天产物
