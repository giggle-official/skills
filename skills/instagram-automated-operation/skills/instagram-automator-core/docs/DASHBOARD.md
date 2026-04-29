# Dashboard 数据说明

## 数据更新机制

Dashboard 数据通过 `dashboard_integration.py` 脚本自动更新：

- **自动更新**：每次完整生产任务完成后（步骤 B5.5）
- **手动更新**：`python3 skills/instagram-automator-core/scripts/dashboard_integration.py update`

## 数据展示范围

### 最近发布视频

- **展示范围**：最近 10 天的所有发布记录
- **排序方式**：按发布时间倒序（最新的在前）
- **数据来源**：`outputs/logs/*_publish_log.json`
- **字段**：
  - 标题
  - 发布时间
  - 状态（✅/❌）
  - PostID
  - Instagram链接
  - 发布内容（脚本中的 Instagram 发布文案）
  - 视频文件路径

### KPI 指标

1. **累计生产视频**
   - 统计所有发布日志中的视频总数
   - 数据来源：`outputs/logs/*_publish_log.json`

2. **今日采集热点**
   - 统计今天数据池中的热点总数
   - 数据来源：`outputs/pool/{YYYYMMDD}_trend_pool.json`

3. **待处理评论**
   - 统计所有监控帖子的新评论数
   - 数据来源：`comment_monitor.json`

### 7天生产趋势

- **展示范围**：最近 7 天
- **数据**：每天发布的视频数量
- **图表类型**：折线图

### 赛道分布

- **数据来源**：最近一次的 Top 3 热点
- **分类**：
  - 科技数码（AI、Android、开发等关键词）
  - 职场成长（职场、经理等关键词）
  - 其他
- **图表类型**：饼图

### 最新评论

- **展示范围**：最新 10 条评论
- **数据来源**：`comment_monitor.json`
- **字段**：
  - 帖子标题
  - 评论者
  - 评论内容（截取前 50 字）
  - 评论时间

### 运营统计

- 平均耗时：约 76 分钟（固定值）
- 成功率：100%（基于最近发布记录）
- 风格指纹：学习中

## 修改历史

### v1.1.0 (2026-04-27)

- **修改内容**：最近发布视频从"只显示最新 3 条"改为"显示最近 10 天的全部数据"
- **修改文件**：`skills/instagram-automator-core/scripts/dashboard_integration.py`
- **影响**：Dashboard 现在会显示更完整的历史记录，方便用户查看过去 10 天的所有发布内容

## 故障排查

### Dashboard 无法访问

1. **检查服务状态**：
   ```bash
   python3 skills/instagram-automator-core/scripts/dashboard_integration.py check
   ```

2. **重启服务**：
   ```python
   from src.hub import manager
   manager.stop_hub()
   manager.start_hub()
   manager.stop_tunnel()
   manager.start_tunnel()
   ```

3. **检查本地访问**：
   ```bash
   curl http://localhost:3000
   ```

### Dashboard 数据不更新

1. **手动更新**：
   ```bash
   python3 skills/instagram-automator-core/scripts/dashboard_integration.py update
   ```

2. **检查数据文件**：
   - 发布日志：`outputs/logs/*_publish_log.json`
   - 数据池：`outputs/pool/{YYYYMMDD}_trend_pool.json`
   - 评论监控：`comment_monitor.json`

### 路径问题

如果遇到 `ModuleNotFoundError: No module named 'src.hub'`，检查：

1. `dashboard_integration.py` 中的 skill 路径是否正确
2. claw-dashboard skill 是否已安装
3. 路径应该指向 `skills/claw-dashboard-skill-main/`
