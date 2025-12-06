# 内容搜索系统

一个用于搜索 Telegram 和 Twitter 内容的 Web 应用。

## 功能特性

- 🔍 全文搜索 Telegram 频道消息
- 🌐 现代化的 Web 界面
- 🔗 点击直接跳转到 Telegram 消息
- ☁️ 支持 GitHub 存储数据

## 安装

1. 克隆仓库：
```bash
git clone <your-repo-url>
cd gary_search
```

2. 安装依赖：
```bash
pip3 install -r requirements.txt
```

## 使用方法

### 启动 Web 应用

```bash
python3 app.py
```

然后在浏览器打开：http://127.0.0.1:5000

### 更新数据

#### 方法 1: 合并新的 Telegram 导出文件

当你从 Telegram 导出新的聊天记录后：

```bash
python3 update_data.py merge <新导出文件路径>
```

例如：
```bash
python3 update_data.py merge ChatExport_2025-12-07/result.json
```

#### 方法 2: 从 GitHub 拉取最新数据

```bash
python3 update_data.py pull
```

#### 方法 3: 推送数据到 GitHub

```bash
python3 update_data.py push
```

## 配置

在 `search.py` 中配置你的 Telegram 频道用户名：

```python
TG_CHANNEL_USERNAME = "gary10x"  # 你的频道用户名
```

## 数据结构

数据存储在 `data.jsonl` 文件中，每行一个 JSON 对象：

```json
{
  "source": "tg",
  "title": "频道名称",
  "content": "消息内容",
  "url": "消息中的链接",
  "tg_link": "https://t.me/gary10x/123",
  "date": "2025-11-19T12:50:25",
  "id": 123
}
```

## GitHub 设置

### 快速设置（推荐）

1. 在 GitHub 创建新仓库（不要初始化 README）

2. 运行设置脚本：
```bash
./setup_github.sh
```

脚本会引导你完成所有设置。

### 手动设置

1. 在 GitHub 创建新仓库

2. 初始化 Git 仓库：
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

详细步骤请查看 [SETUP_GITHUB.md](SETUP_GITHUB.md)

### 更新数据到 GitHub

```bash
# 合并新数据后推送到 GitHub
python3 update_data.py merge <新文件路径>
python3 update_data.py push
```

## 自动化更新（可选）

你可以设置定时任务来自动拉取最新数据。例如，使用 cron：

```bash
# 编辑 crontab
crontab -e

# 添加每天凌晨 2 点拉取数据的任务
0 2 * * * cd /path/to/gary_search && python3 update_data.py pull
```

## 文件说明

- `app.py` - Flask Web 应用
- `search.py` - 搜索逻辑和数据加载
- `update_data.py` - 数据更新脚本
- `data.jsonl` - 统一的数据存储文件
- `templates/index.html` - Web 界面

## 许可证

MIT

