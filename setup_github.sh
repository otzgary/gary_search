#!/bin/bash

# GitHub 设置脚本

echo "🚀 设置 GitHub 仓库..."
echo ""

# 检查是否已初始化 Git
if [ ! -d ".git" ]; then
    echo "初始化 Git 仓库..."
    git init
    echo "✅ Git 已初始化"
else
    echo "✅ Git 已存在"
fi

# 检查是否有远程仓库
if git remote | grep -q "origin"; then
    echo "✅ 远程仓库已配置"
    git remote -v
else
    echo ""
    echo "请提供你的 GitHub 仓库 URL:"
    echo "例如: https://github.com/你的用户名/gary_search.git"
    read -p "GitHub URL: " repo_url
    
    if [ -n "$repo_url" ]; then
        git remote add origin "$repo_url"
        echo "✅ 已添加远程仓库: $repo_url"
    else
        echo "❌ 未提供 URL，跳过"
    fi
fi

echo ""
echo "添加文件到 Git..."
git add .

echo ""
echo "提交更改..."
git commit -m "Initial commit: 搜索系统" || echo "⚠️  没有新更改需要提交"

echo ""
echo "设置主分支..."
git branch -M main

echo ""
echo "是否要推送到 GitHub? (y/n)"
read -p "> " push_confirm

if [ "$push_confirm" = "y" ] || [ "$push_confirm" = "Y" ]; then
    echo "推送到 GitHub..."
    git push -u origin main
    echo "✅ 完成！"
else
    echo "跳过推送。稍后可以运行: git push -u origin main"
fi

echo ""
echo "📝 后续使用:"
echo "  更新数据: python3 update_data.py merge <新文件路径>"
echo "  推送到 GitHub: python3 update_data.py push"
echo "  从 GitHub 拉取: python3 update_data.py pull"

