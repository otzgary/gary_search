#!/bin/bash

echo "🔗 连接 GitHub 仓库"
echo ""
echo "请提供你的 GitHub 信息："
echo ""

read -p "GitHub 用户名: " github_username
read -p "仓库名称 (默认: gary_search): " repo_name

if [ -z "$repo_name" ]; then
    repo_name="gary_search"
fi

repo_url="https://github.com/${github_username}/${repo_name}.git"

echo ""
echo "添加远程仓库: $repo_url"
git remote add origin "$repo_url" 2>/dev/null || git remote set-url origin "$repo_url"

echo ""
echo "推送到 GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 成功！你的代码已推送到 GitHub"
    echo "📦 仓库地址: https://github.com/${github_username}/${repo_name}"
else
    echo ""
    echo "❌ 推送失败。请检查："
    echo "1. GitHub 仓库是否已创建"
    echo "2. 仓库 URL 是否正确"
    echo "3. 是否有推送权限"
    echo ""
    echo "如果使用 Personal Access Token，请使用 token 作为密码"
fi

