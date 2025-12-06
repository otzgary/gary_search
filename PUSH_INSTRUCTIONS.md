# 推送到 GitHub 的步骤

## 重要：首先创建 GitHub 仓库

1. 访问：https://github.com/new
2. Repository name: `gary_search`
3. 选择 Public 或 Private
4. **不要**勾选任何初始化选项（README、.gitignore、license）
5. 点击 "Create repository"

## 认证方式选择

### 方式 1：使用 Personal Access Token（推荐）

1. 生成 Token：
   - 访问：https://github.com/settings/tokens
   - 点击 "Generate new token" → "Generate new token (classic)"
   - 名称：`gary_search`
   - 勾选 `repo` 权限
   - 点击 "Generate token"
   - **复制 token**（只显示一次！）

2. 推送代码：
   ```bash
   git push -u origin main
   ```
   - Username: `otzgary`
   - Password: **粘贴你的 token**（不是密码）

### 方式 2：使用 SSH（更安全，推荐长期使用）

1. 检查是否有 SSH 密钥：
   ```bash
   ls -la ~/.ssh/id_*.pub
   ```

2. 如果没有，生成 SSH 密钥：
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   # 按回车使用默认路径
   # 可以设置密码或直接回车
   ```

3. 复制公钥：
   ```bash
   cat ~/.ssh/id_ed25519.pub
   # 或
   cat ~/.ssh/id_rsa.pub
   ```

4. 添加到 GitHub：
   - 访问：https://github.com/settings/keys
   - 点击 "New SSH key"
   - Title: `MacBook Air`
   - Key: 粘贴刚才复制的公钥
   - 点击 "Add SSH key"

5. 更改远程 URL 为 SSH：
   ```bash
   git remote set-url origin git@github.com:otzgary/gary_search.git
   ```

6. 推送：
   ```bash
   git push -u origin main
   ```

### 方式 3：使用 GitHub CLI（如果已安装）

```bash
gh auth login
git push -u origin main
```

## 验证

推送成功后，访问：
https://github.com/otzgary/gary_search

你应该能看到所有文件，包括 `data.jsonl` 中的 151 条数据。

## 后续使用

更新数据后推送到 GitHub：
```bash
python3 update_data.py merge <新文件路径>
python3 update_data.py push
```

