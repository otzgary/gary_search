# 简单推送指南

## 方法 1：使用脚本（最简单）

```bash
./push_with_token.sh
```

脚本会要求你输入 Personal Access Token。

## 方法 2：手动推送

### 步骤 1：生成 Token

1. 访问：https://github.com/settings/tokens
2. 点击 "Generate new token" → "Generate new token (classic)"
3. 名称：`gary_search`
4. **勾选 `repo` 权限**（重要！）
5. 点击 "Generate token"
6. **立即复制 token**（只显示一次！）

### 步骤 2：推送

运行：
```bash
git push -u origin main
```

然后输入：
- **Username**: `otzgary`
- **Password**: 粘贴你的 **token**（不是 GitHub 密码！）

## 方法 3：使用 Token 直接推送（无需交互）

```bash
# 替换 YOUR_TOKEN 为你的实际 token
git push https://YOUR_TOKEN@github.com/otzgary/gary_search.git main
```

## 验证

推送成功后，访问：
https://github.com/otzgary/gary_search

你应该能看到所有文件，包括 `data.jsonl`。

