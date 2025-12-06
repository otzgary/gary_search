#!/bin/bash

echo "🚀 快速推送到 GitHub"
echo ""

# 检查是否已创建仓库
echo "⚠️  请确保你已经在 GitHub 创建了仓库："
echo "   https://github.com/new"
echo "   仓库名: gary_search"
echo "   不要初始化 README"
echo ""
read -p "已创建仓库？(y/n): " created

if [ "$created" != "y" ] && [ "$created" != "Y" ]; then
    echo "请先创建仓库，然后重新运行此脚本"
    exit 1
fi

echo ""
echo "选择认证方式："
echo "1. Personal Access Token (推荐，简单)"
echo "2. SSH (更安全，需要设置)"
read -p "选择 (1/2): " auth_choice

if [ "$auth_choice" = "1" ]; then
    echo ""
    echo "📝 生成 Personal Access Token:"
    echo "1. 访问: https://github.com/settings/tokens"
    echo "2. Generate new token (classic)"
    echo "3. 勾选 'repo' 权限"
    echo "4. 生成并复制 token"
    echo ""
    read -p "粘贴你的 token: " token
    
    if [ -n "$token" ]; then
        # 使用 token 推送
        git push https://${token}@github.com/otzgary/gary_search.git main
    else
        echo "❌ 未提供 token"
        exit 1
    fi
elif [ "$auth_choice" = "2" ]; then
    # 检查 SSH
    if [ ! -f ~/.ssh/id_ed25519.pub ] && [ ! -f ~/.ssh/id_rsa.pub ]; then
        echo ""
        echo "未找到 SSH 密钥，生成新的..."
        ssh-keygen -t ed25519 -C "gary_search" -f ~/.ssh/id_ed25519 -N ""
        echo ""
        echo "📋 请复制以下公钥并添加到 GitHub:"
        echo "   https://github.com/settings/keys"
        echo ""
        cat ~/.ssh/id_ed25519.pub
        echo ""
        read -p "已添加到 GitHub？(y/n): " added
        
        if [ "$added" != "y" ] && [ "$added" != "Y" ]; then
            echo "请先添加 SSH 密钥"
            exit 1
        fi
    fi
    
    # 切换到 SSH URL
    git remote set-url origin git@github.com:otzgary/gary_search.git
    git push -u origin main
else
    echo "❌ 无效选择"
    exit 1
fi

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 成功！"
    echo "📦 仓库地址: https://github.com/otzgary/gary_search"
else
    echo ""
    echo "❌ 推送失败，请检查错误信息"
fi

