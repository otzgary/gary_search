# 自动获取新帖子指南

## 当前状态

**目前系统无法自动获取新帖子**，需要手动操作。

## 获取新帖子的方法

### 方法 1：导出文件（最简单，推荐）⭐

1. **在 Telegram 中导出频道聊天记录**：
   - 打开你的频道 @gary10x
   - 点击频道设置 → 导出聊天记录
   - 选择 JSON 格式
   - 下载文件

2. **合并新数据**：
   ```bash
   python3 update_data.py merge <导出文件路径>
   ```

3. **推送到 GitHub**（可选）：
   ```bash
   python3 update_data.py push
   ```

### 方法 2：使用 Telethon 自动获取（高级）🤖

可以自动从 Telegram API 获取新帖子，无需手动导出。

#### 设置步骤：

1. **安装 Telethon**：
   ```bash
   pip3 install telethon
   ```

2. **获取 API 凭证**：
   - 访问：https://my.telegram.org
   - 登录你的 Telegram 账号
   - 在 "API development tools" 中获取：
     - **API ID**
     - **API Hash**

3. **配置 auto_fetch.py**：
   打开 `auto_fetch.py`，填入：
   ```python
   API_ID = "你的 API ID"
   API_HASH = "你的 API Hash"
   ```

4. **运行自动获取**：
   ```bash
   python3 auto_fetch.py
   ```
   
   首次运行会要求你登录验证（输入手机号和验证码）

5. **设置定时任务**（可选）：
   ```bash
   # 编辑 crontab
   crontab -e
   
   # 添加每天凌晨 2 点自动获取
   0 2 * * * cd /Users/gary/Documents/gary_search && python3 auto_fetch.py
   ```

## 推荐工作流程

### 日常使用（简单方式）：
1. 每周或每月从 Telegram 导出一次
2. 运行 `python3 update_data.py merge <文件路径>`
3. 运行 `python3 update_data.py push` 推送到 GitHub

### 自动化（高级方式）：
1. 设置 Telethon（只需一次）
2. 设置定时任务每天自动获取
3. 自动推送到 GitHub

## 注意事项

- **Telethon 方法**需要你的 Telegram 账号登录
- 首次使用 Telethon 需要验证码验证
- 建议定期备份数据到 GitHub
- 如果频道是私有的，确保你的账号有访问权限

## 故障排除

### Telethon 连接失败
- 检查 API ID 和 API Hash 是否正确
- 确保网络可以访问 Telegram
- 检查是否需要代理

### 导出文件合并失败
- 确保文件路径正确
- 检查文件格式是否为 JSON
- 查看错误信息


