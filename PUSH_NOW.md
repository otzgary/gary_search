# 🚀 立即推送 - 3 步完成

## 步骤 1：生成 Personal Access Token（2 分钟）

1. 打开：https://github.com/settings/tokens
2. 点击 **"Generate new token"** → **"Generate new token (classic)"**
3. 填写：
   - **Note**: `gary_search`
   - **Expiration**: 选择你想要的期限（建议 90 天或 No expiration）
   - **勾选 `repo` 权限** ✅
4. 点击 **"Generate token"**
5. **立即复制 token**（只显示一次！）📋

## 步骤 2：推送代码

在终端运行：

```bash
cd /Users/gary/Documents/gary_search
git push -u origin main
```

当提示输入时：
- **Username**: `otzgary`
- **Password**: **粘贴你的 token**（不是 GitHub 密码！）

## 步骤 3：验证

推送成功后，访问：
👉 https://github.com/otzgary/gary_search

你应该能看到所有文件！

---

## 💡 提示

如果不想每次输入 token，可以配置 Git credential helper：

```bash
git config --global credential.helper osxkeychain
```

这样 token 会保存在 macOS 钥匙串中。


