#!/bin/bash

echo "🚀 推送到 GitHub"
echo ""
echo "请按照以下步骤操作："
echo ""
echo "1. 生成 Personal Access Token:"
echo "   访问: https://github.com/settings/tokens"
echo "   点击 'Generate new token (classic)'"
echo "   勾选 'repo' 权限"
echo "   点击 'Generate token'"
echo "   复制生成的 token（只显示一次！）"
echo ""
echo "2. 粘贴 token 到下面："
echo ""

read -sp "Token: " token
echo ""

if [ -z "$token" ]; then
    echo "❌ 未提供 token"
    exit 1
fi

echo ""
echo "正在推送..."

# 使用 token 推送
git push https://${token}@github.com/otzgary/gary_search.git main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 成功推送到 GitHub！"
    echo "📦 仓库地址: https://github.com/otzgary/gary_search"
else
    echo ""
    echo "❌ 推送失败，请检查："
    echo "   1. Token 是否正确"
    echo "   2. Token 是否有 'repo' 权限"
    echo "   3. 仓库是否存在"
fi

