# 首次运行自动获取

## ✅ API 已配置完成

你的 API ID 和 API Hash 已经配置好了！

## 🚀 现在运行自动获取

在终端运行：

```bash
cd /Users/gary/Documents/gary_search
python3 auto_fetch.py
```

## 📱 首次登录步骤

首次运行会要求你：

1. **输入手机号**：
   - 输入你的 Telegram 手机号（带国家代码）
   - 例如：`+8613800138000` 或 `+1234567890`

2. **输入验证码**：
   - Telegram 会发送验证码到你的手机
   - 输入收到的验证码

3. **输入密码**（如果设置了）：
   - 如果你的账号设置了两步验证密码，需要输入

4. **完成**：
   - 登录信息会保存在 `gary_search_session.session` 文件中
   - 之后运行就不需要再登录了

## ✅ 运行成功后

- 会自动获取频道 @gary10x 的新消息
- 新消息会添加到 `data.jsonl` 文件中
- 可以选择推送到 GitHub

## 🔄 后续使用

之后直接运行：

```bash
python3 auto_fetch.py
```

不需要再登录了！

## ⚙️ 设置定时任务（可选）

如果想每天自动获取，可以设置 cron：

```bash
# 编辑 crontab
crontab -e

# 添加每天凌晨 2 点自动获取
0 2 * * * cd /Users/gary/Documents/gary_search && /usr/bin/python3 auto_fetch.py
```

## ❓ 遇到问题？

- **连接失败**：检查网络，可能需要代理
- **验证码收不到**：检查手机号格式是否正确（需要国家代码）
- **权限错误**：确保你的账号有访问频道 @gary10x 的权限

