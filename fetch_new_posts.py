"""
自动获取 Telegram 频道新帖子
使用 Telegram API 或导出文件来更新数据
"""
import json
import os
import requests
from datetime import datetime
from typing import List, Dict, Any
from search import load_all_items, TG_CHANNEL_USERNAME

# Telegram Bot API 配置
# 获取方法：1. 找 @BotFather 创建 bot 2. 获取 API token
TELEGRAM_BOT_TOKEN = ""  # 你的 bot token（可选，如果不使用 API）
TELEGRAM_API_URL = "https://api.telegram.org/bot{}/"


def fetch_via_export():
    """
    方法 1: 从新的导出文件获取（推荐，最简单）
    当你从 Telegram 导出新的聊天记录后，使用这个方法
    """
    print("📥 方法 1: 从导出文件获取新帖子")
    print("=" * 50)
    print("1. 在 Telegram 中导出频道聊天记录")
    print("2. 将导出的 JSON 文件放到项目目录")
    print("3. 运行: python3 update_data.py merge <文件路径>")
    print()


def fetch_via_api():
    """
    方法 2: 使用 Telegram Bot API 获取（需要设置）
    注意：Bot 只能获取它加入的频道消息
    """
    if not TELEGRAM_BOT_TOKEN:
        print("❌ 未配置 Telegram Bot Token")
        print("设置方法：")
        print("1. 在 Telegram 中找 @BotFather")
        print("2. 发送 /newbot 创建新 bot")
        print("3. 获取 token 并填入 TELEGRAM_BOT_TOKEN")
        return []
    
    print("📡 使用 Telegram API 获取新帖子...")
    
    # 获取频道信息
    channel_username = TG_CHANNEL_USERNAME.replace("@", "")
    
    try:
        # 注意：Telegram Bot API 有限制，bot 必须加入频道才能获取消息
        # 这里只是示例，实际使用需要 bot 加入频道
        
        # 获取更新
        url = TELEGRAM_API_URL.format(TELEGRAM_BOT_TOKEN) + "getUpdates"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("ok"):
                updates = data.get("result", [])
                print(f"获取到 {len(updates)} 条更新")
                # 处理更新...
                return []
            else:
                print(f"API 错误: {data.get('description')}")
        else:
            print(f"请求失败: {response.status_code}")
    
    except Exception as e:
        print(f"获取失败: {e}")
    
    return []


def fetch_via_telethon():
    """
    方法 3: 使用 Telethon 库（最强大，需要用户账号）
    可以获取所有你加入的频道消息
    """
    print("📱 方法 3: 使用 Telethon（需要安装和配置）")
    print("=" * 50)
    print("安装: pip3 install telethon")
    print("需要：")
    print("1. 你的 Telegram API ID 和 API Hash（从 https://my.telegram.org 获取）")
    print("2. 首次运行需要登录验证")
    print()
    print("这是最强大的方法，可以自动获取所有新帖子")
    print()


def show_current_status():
    """显示当前数据状态"""
    items = load_all_items()
    tg_items = [item for item in items if item.get("source") == "tg"]
    
    if tg_items:
        # 获取最新和最早的日期
        dates = [item.get("date", "") for item in tg_items if item.get("date")]
        dates.sort()
        
        print(f"📊 当前数据状态:")
        print(f"   - 总消息数: {len(tg_items)}")
        if dates:
            print(f"   - 最早消息: {dates[0]}")
            print(f"   - 最新消息: {dates[-1]}")
    else:
        print("📊 当前没有数据")


def main():
    print("🔍 Telegram 频道新帖子获取方法")
    print("=" * 50)
    print()
    
    show_current_status()
    print()
    
    print("可用方法：")
    print()
    print("1️⃣  导出文件方法（推荐，最简单）")
    print("   - 在 Telegram 中导出频道聊天记录")
    print("   - 运行: python3 update_data.py merge <文件路径>")
    print()
    
    print("2️⃣  Telegram Bot API（需要 bot token）")
    print("   - Bot 必须加入频道")
    print("   - 功能有限")
    print()
    
    print("3️⃣  Telethon 库（最强大，推荐高级用户）")
    print("   - 需要 API ID 和 API Hash")
    print("   - 可以自动获取所有新帖子")
    print("   - 需要安装: pip3 install telethon")
    print()
    
    choice = input("选择方法 (1/2/3) 或按回车查看详细说明: ").strip()
    
    if choice == "1":
        fetch_via_export()
    elif choice == "2":
        fetch_via_api()
    elif choice == "3":
        fetch_via_telethon()
    else:
        print("\n详细说明：")
        print("-" * 50)
        fetch_via_export()
        fetch_via_api()
        fetch_via_telethon()


if __name__ == "__main__":
    main()


