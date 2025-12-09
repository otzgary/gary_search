# 自动化设置指南

## ✅ 已完成的自动化

现在 `auto_fetch.py` 已经配置为：
- ✅ 自动获取新帖子
- ✅ 自动更新数据库
- ✅ **自动推送到 GitHub**（无需手动确认）

## 🚀 设置定时任务

### 方法 1：使用自动设置脚本（推荐）

```bash
./setup_auto.sh
```

脚本会：
- 自动检测 Python 路径
- 设置每 6 小时自动运行一次
- 添加日志记录

### 方法 2：手动设置

```bash
# 编辑 crontab
crontab -e

# 添加以下行（每 6 小时运行一次）
0 */6 * * * cd /Users/gary/Documents/gary_search && /usr/bin/python3 auto_fetch.py >> /Users/gary/Documents/gary_search/auto_fetch.log 2>&1
```

### 其他时间间隔选项

```bash
# 每小时运行一次
0 * * * * cd /Users/gary/Documents/gary_search && /usr/bin/python3 auto_fetch.py >> /Users/gary/Documents/gary_search/auto_fetch.log 2>&1

# 每天凌晨 2 点运行
0 2 * * * cd /Users/gary/Documents/gary_search && /usr/bin/python3 auto_fetch.py >> /Users/gary/Documents/gary_search/auto_fetch.log 2>&1

# 每 12 小时运行一次
0 */12 * * * cd /Users/gary/Documents/gary_search && /usr/bin/python3 auto_fetch.py >> /Users/gary/Documents/gary_search/auto_fetch.log 2>&1
```

## 📋 管理定时任务

### 查看当前任务
```bash
crontab -l
```

### 编辑任务
```bash
crontab -e
```

### 删除所有任务
```bash
crontab -r
```

### 查看日志
```bash
tail -f auto_fetch.log
```

## 🔍 测试自动化

手动运行一次，确认一切正常：

```bash
python3 auto_fetch.py
```

应该会：
1. 获取新消息
2. 更新数据库
3. 自动推送到 GitHub（无需确认）

## ⚙️ 工作原理

1. **定时任务触发** → 运行 `auto_fetch.py`
2. **获取新消息** → 从 Telegram API 获取
3. **更新数据库** → 保存到 `data.jsonl`
4. **自动推送** → 推送到 GitHub（无需确认）

## 📝 注意事项

- 确保电脑保持开机（或使用服务器）
- 如果使用 Mac，确保不会进入深度睡眠
- 日志文件会记录每次运行的结果
- 如果推送失败，数据仍会保存在本地

## 🐛 故障排除

### 任务没有运行
- 检查 cron 服务是否运行：`ps aux | grep cron`
- 查看系统日志：`grep CRON /var/log/syslog`（Linux）或 `log show --predicate 'process == "cron"'`（macOS）

### 推送失败
- 检查网络连接
- 检查 Git 配置
- 查看日志文件：`cat auto_fetch.log`

### 需要手动运行
```bash
python3 auto_fetch.py
```

