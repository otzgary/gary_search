"""
自动获取 Telegram 频道新帖子
使用 Telethon 库从 Telegram API 获取
"""
import json
import os
from datetime import datetime
from typing import List, Dict, Any
from search import TG_CHANNEL_USERNAME, extract_urls_from_text, should_exclude_url
from update_data import load_existing_data, save_to_jsonl

try:
    from telethon import TelegramClient
    from telethon.tl.types import Message
    TELETHON_AVAILABLE = True
except ImportError:
    TELETHON_AVAILABLE = False

# Telegram API 配置
# 获取方法：访问 https://my.telegram.org
# 登录后，在 "API development tools" 中获取
API_ID = "38433790"  # 你的 API ID
API_HASH = "89cd257ba28bc25edf5dbcfa863e047f"  # 你的 API Hash
SESSION_NAME = "gary_search_session"

# 频道配置
CHANNEL_USERNAME = TG_CHANNEL_USERNAME or "gary10x"


def fetch_new_messages_telethon() -> List[Dict[str, Any]]:
    """使用 Telethon 获取新消息"""
    if not TELETHON_AVAILABLE:
        print("❌ Telethon 未安装")
        print("安装方法: pip3 install telethon")
        return []
    
    if not API_ID or not API_HASH:
        print("❌ 未配置 API ID 和 API Hash")
        print("获取方法：")
        print("1. 访问 https://my.telegram.org")
        print("2. 登录你的 Telegram 账号")
        print("3. 在 'API development tools' 中获取 API ID 和 API Hash")
        print("4. 填入 auto_fetch.py 中的 API_ID 和 API_HASH")
        return []
    
    print("📡 正在连接 Telegram...")
    
    try:
        # 创建客户端
        client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
        
        print("📱 正在登录...")
        print("提示：")
        print("  - 输入手机号时，需要包含国家代码（例如：+8613800138000）")
        print("  - 输入密码时，字符不会显示（这是正常的安全行为）")
        print("  - 直接输入密码后按回车即可")
        print()
        
        # 使用交互式登录
        client.start(
            phone=lambda: input('请输入手机号（带国家代码，如 +8613800138000）: '),
            password=lambda: input('请输入两步验证密码（输入时不会显示，直接输入后按回车）: '),
            code_callback=lambda: input('请输入验证码: ')
        )
        
        print("✅ 登录成功")
        print(f"📥 正在获取频道 @{CHANNEL_USERNAME} 的消息...")
        
        # 获取现有数据，找出最新的消息 ID
        existing = load_existing_data()
        latest_id = max([item.get("id", 0) for item in existing.values()], default=0)
        
        print(f"📊 当前最新消息 ID: {latest_id}")
        
        # 获取频道消息
        new_items = []
        async def fetch_messages():
            async for message in client.iter_messages(CHANNEL_USERNAME, min_id=latest_id):
                if not message.text:
                    continue
                
                # 提取链接（从实体中提取）
                content_urls = []
                if message.entities:
                    for entity in message.entities:
                        if hasattr(entity, 'url') and entity.url:
                            url = entity.url
                            if url and not should_exclude_url(url) and url not in content_urls:
                                content_urls.append(url)
                
                # 从纯文本中提取 URL（补充提取，已包含过滤）
                urls_from_text = extract_urls_from_text(message.text)
                for url in urls_from_text:
                    if url not in content_urls:
                        content_urls.append(url)
                
                # 生成 Telegram 链接
                tg_link = f"https://t.me/{CHANNEL_USERNAME}/{message.id}"
                
                item = {
                    "source": "tg",
                    "type": "post",
                    "title": CHANNEL_USERNAME,
                    "content": message.text,
                    "url": content_urls[0] if content_urls else "",  # 第一个链接（向后兼容）
                    "urls": content_urls,  # 所有链接列表
                    "tg_link": tg_link,
                    "date": message.date.isoformat() if message.date else "",
                    "id": message.id
                }
                new_items.append(item)
                print(f"  ✓ 获取消息 {message.id}: {message.text[:50]}...")
        
        # 运行异步函数
        with client:
            client.loop.run_until_complete(fetch_messages())
        
        print(f"\n✅ 获取到 {len(new_items)} 条新消息")
        return new_items
        
    except Exception as e:
        print(f"❌ 获取失败: {e}")
        return []


def update_with_new_messages(new_items: List[Dict[str, Any]]):
    """将新消息合并到数据库"""
    if not new_items:
        print("没有新消息需要更新")
        return
    
    existing = load_existing_data()
    
    # 添加新消息
    for item in new_items:
        existing[item["id"]] = item
    
    # 保存
    save_to_jsonl(list(existing.values()))
    
    print(f"✅ 已更新数据库，新增 {len(new_items)} 条消息")


def main():
    print("🤖 自动获取 Telegram 频道新帖子")
    print("=" * 50)
    print()
    
    if not TELETHON_AVAILABLE:
        print("📦 需要安装 Telethon 库")
        print("运行: pip3 install telethon")
        print()
        print("或者使用导出文件方法：")
        print("  python3 update_data.py merge <导出文件路径>")
        return
    
    # 获取新消息
    new_items = fetch_new_messages_telethon()
    
    if new_items:
        # 更新数据库
        update_with_new_messages(new_items)
        
        # 自动推送到 GitHub
        print("\n📤 正在推送到 GitHub...")
        try:
            from update_data import push_to_github
            if push_to_github():
                print("✅ 已成功推送到 GitHub")
            else:
                print("⚠️  推送到 GitHub 失败，但数据已更新到本地")
        except Exception as e:
            print(f"⚠️  推送到 GitHub 时出错: {e}")
            print("数据已更新到本地，可以稍后手动推送")
    else:
        print("✅ 没有新消息，数据库已是最新")


if __name__ == "__main__":
    main()

