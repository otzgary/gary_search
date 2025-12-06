# GitHub 设置指南

## 步骤 1: 在 GitHub 创建仓库

1. 登录 GitHub
2. 点击右上角的 "+" → "New repository"
3. 仓库名称：`gary_search`（或你喜欢的名字）
4. 选择 Public 或 Private
5. **不要**初始化 README、.gitignore 或 license（我们已经有了）
6. 点击 "Create repository"

## 步骤 2: 初始化本地 Git 仓库

在项目目录下运行：

```bash
# 初始化 Git
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: 搜索系统"

# 添加远程仓库（替换为你的仓库 URL）
git remote add origin https://github.com/你的用户名/gary_search.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

## 步骤 3: 配置 .gitignore

`.gitignore` 文件已经创建好了。如果你**想要**将数据文件也存储在 GitHub 上，需要修改 `.gitignore`：

```bash
# 编辑 .gitignore，注释掉这两行：
# ChatExport_*/
# data.jsonl
```

## 步骤 4: 日常使用

### 更新数据并推送到 GitHub

```bash
# 1. 合并新的 Telegram 导出文件
python3 update_data.py merge ChatExport_新日期/result.json

# 2. 推送到 GitHub
python3 update_data.py push
```

### 从 GitHub 拉取最新数据

```bash
python3 update_data.py pull
```

## 步骤 5: 在其他设备上使用

```bash
# 克隆仓库
git clone https://github.com/你的用户名/gary_search.git
cd gary_search

# 安装依赖
pip3 install -r requirements.txt

# 拉取最新数据
python3 update_data.py pull

# 启动应用
python3 app.py
```

## 注意事项

1. **数据隐私**：如果频道内容包含敏感信息，建议使用 Private 仓库
2. **文件大小**：如果数据文件很大，GitHub 有 100MB 单文件限制
3. **自动同步**：可以设置 GitHub Actions 或 cron 任务自动同步

## 故障排除

### 如果推送失败

```bash
# 先拉取最新版本
git pull origin main

# 解决冲突后再次推送
git push origin main
```

### 如果忘记密码

使用 Personal Access Token：
1. GitHub Settings → Developer settings → Personal access tokens
2. 生成新 token
3. 使用 token 作为密码

