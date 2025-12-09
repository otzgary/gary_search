#!/bin/bash

echo "🤖 设置自动获取和推送"
echo "=" | head -c 50; echo ""

# 获取当前脚本目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHON_PATH=$(which python3)

echo "📁 项目目录: $SCRIPT_DIR"
echo "🐍 Python 路径: $PYTHON_PATH"
echo ""

# 创建 cron 任务
CRON_JOB="0 */6 * * * cd $SCRIPT_DIR && $PYTHON_PATH auto_fetch.py >> $SCRIPT_DIR/auto_fetch.log 2>&1"

echo "⏰ 设置定时任务：每 6 小时自动获取一次"
echo ""
echo "Cron 任务："
echo "$CRON_JOB"
echo ""

# 询问用户
read -p "是否添加到 crontab? (y/n): " confirm

if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
    # 检查是否已存在
    (crontab -l 2>/dev/null | grep -v "auto_fetch.py" ; echo "$CRON_JOB") | crontab -
    echo ""
    echo "✅ 已添加到 crontab"
    echo ""
    echo "📋 当前 crontab 任务："
    crontab -l | grep auto_fetch
    echo ""
    echo "📝 日志文件: $SCRIPT_DIR/auto_fetch.log"
    echo ""
    echo "💡 管理定时任务："
    echo "  查看: crontab -l"
    echo "  编辑: crontab -e"
    echo "  删除: crontab -r"
else
    echo ""
    echo "手动添加方法："
    echo "1. 运行: crontab -e"
    echo "2. 添加以下行："
    echo "   $CRON_JOB"
    echo "3. 保存并退出"
fi

