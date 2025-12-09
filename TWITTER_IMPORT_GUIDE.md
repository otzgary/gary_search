# Twitter 历史帖子导入指南

## 🎯 目标

获取你所有的 Twitter 历史帖子，解决 Twitter 搜索功能不好用的问题（特别是改过用户名后）。

## 📥 步骤 1：从 Twitter 导出数据

### 方法 1：通过 Twitter 设置（推荐）

1. **登录 Twitter**：https://twitter.com
2. **进入设置**：
   - 点击左侧菜单的 "更多" (More)
   - 选择 "设置和隐私" (Settings and privacy)
   - 点击 "你的账号" (Your account)
   - 找到 "下载你的数据" (Download an archive of your data)

3. **请求数据导出**：
   - 点击 "下载数据存档" (Download archive)
   - 选择 "推文" (Tweets) 或 "全部" (All)
   - 输入密码确认
   - Twitter 会发送邮件通知

4. **下载数据**：
   - 收到邮件后，点击下载链接
   - 下载 ZIP 文件（可能需要几天时间处理）

### 方法 2：如果找不到导出选项

Twitter 可能已经更改了界面，尝试：
- 访问：https://twitter.com/settings/download_your_data
- 或搜索 "Twitter data export"

## 📦 步骤 2：导入到系统

### 方法 1：使用导入脚本（推荐）

```bash
python3 import_twitter.py <Twitter导出ZIP文件路径>
```

例如：
```bash
python3 import_twitter.py ~/Downloads/twitter-2025-12-06.zip
```

### 方法 2：交互式导入

```bash
python3 import_twitter.py
```

然后输入文件路径。

## ⚙️ 配置 Twitter 用户名（可选）

如果你改过用户名，可以在 `import_twitter.py` 中设置：

```python
TWITTER_USERNAME = "你的当前用户名"  # 用于生成正确的 Twitter 链接
```

如果不设置，系统会尝试从导出文件中提取。

## ✅ 步骤 3：验证导入

导入完成后：

1. **检查数据**：
   ```bash
   python3 -c "from search import load_all_items; items = [i for i in load_all_items() if i.get('source') == 'twitter']; print(f'Twitter 推文: {len(items)} 条')"
   ```

2. **启动 Web 应用测试**：
   ```bash
   python3 app.py
   ```
   然后搜索你的 Twitter 内容。

## 🔍 搜索功能

导入后，你可以在搜索系统中：
- ✅ 搜索所有 Twitter 历史推文
- ✅ 点击推文跳转到 Twitter
- ✅ 和 Telegram 内容一起搜索

## 📝 注意事项

1. **文件格式**：
   - 支持 ZIP 文件（Twitter 标准导出格式）
   - 也支持 JSON 文件

2. **文件结构**：
   - Twitter 导出通常是 ZIP 文件
   - 包含 `data/tweets.js` 或 `tweets.js` 文件
   - 脚本会自动查找这些文件

3. **数据量**：
   - 如果推文很多，导入可能需要一些时间
   - 系统会自动去重，不会重复导入

4. **推文链接**：
   - 如果改过用户名，链接可能指向旧用户名
   - 可以在代码中设置当前用户名来生成正确的链接

## 🚀 推送到 GitHub

导入完成后，可以选择推送到 GitHub：

```bash
python3 update_data.py push
```

## ❓ 常见问题

### Q: 找不到 tweets.js 文件？
A: 检查 ZIP 文件结构，可能在不同位置。脚本会自动搜索。

### Q: 导入后搜索不到？
A: 确保推文内容不为空，系统会跳过空推文。

### Q: 链接不正确？
A: 在 `import_twitter.py` 中设置 `TWITTER_USERNAME` 为你的当前用户名。

### Q: 导入很慢？
A: 如果推文很多（几千条），可能需要几分钟。请耐心等待。

## 🎉 完成

导入完成后，你就可以：
- 搜索所有 Twitter 历史推文
- 不再依赖 Twitter 的搜索功能
- 所有内容都在你的控制下

