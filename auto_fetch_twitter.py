"""
自动获取 Twitter 新帖子
支持多种方式获取 Twitter 数据
"""
import os
from typing import List, Dict, Any
from update_data import load_existing_data, save_to_jsonl
from import_twitter import import_twitter_export, TWITTER_USERNAME
from search import extract_urls_from_text, should_exclude_url

try:
    import tweepy
    TWEEPY_AVAILABLE = True
except ImportError:
    TWEEPY_AVAILABLE = False

# Twitter API 配置（可选）
# 获取方法：https://developer.twitter.com
TWITTER_API_KEY = ""
TWITTER_API_SECRET = ""
TWITTER_ACCESS_TOKEN = ""
TWITTER_ACCESS_TOKEN_SECRET = ""
TWITTER_BEARER_TOKEN = ""


def fetch_via_export():
    """
    方法 1: 从新的导出文件获取（推荐，最简单）
    当你从 Twitter 导出新的数据后，使用这个方法
    """
    print("📥 方法 1: 从导出文件获取新帖子")
    print("=" * 50)
    print("1. 在 Twitter 设置中请求数据导出")
    print("2. 下载导出的 ZIP 文件")
    print("3. 运行: python3 import_twitter.py <文件路径>")
    print()
    
    # 交互式导入
    export_path = input("如果有新的导出文件，请输入路径（直接回车跳过）: ").strip()
    if export_path and os.path.exists(export_path):
        new_count = import_twitter_export(export_path)
        if new_count > 0:
            push = input("是否推送到 GitHub? (y/n): ").strip().lower()
            if push == "y":
                from update_data import push_to_github
                push_to_github()
    else:
        print("跳过导入")


def fetch_via_api():
    """
    方法 2: 使用 Twitter API 获取（需要 API 密钥）
    注意：Twitter API 现在需要付费订阅（$100/月起）
    """
    if not TWEEPY_AVAILABLE:
        print("❌ Tweepy 未安装")
        print("安装方法: pip3 install tweepy")
        print()
        print("⚠️  注意：Twitter API 现在需要付费订阅（$100/月起）")
        return []
    
    if not TWITTER_BEARER_TOKEN and not (TWITTER_API_KEY and TWITTER_API_SECRET):
        print("❌ 未配置 Twitter API 凭证")
        print("获取方法：")
        print("1. 访问 https://developer.twitter.com")
        print("2. 申请开发者账号（需要付费 $100/月）")
        print("3. 创建应用并获取 API 密钥")
        print("4. 填入 auto_fetch_twitter.py 中的配置")
        print()
        print("⚠️  注意：Twitter API 现在需要付费订阅")
        return []
    
    print("📡 使用 Twitter API 获取新帖子...")
    print("⚠️  需要 Twitter API 付费订阅（$100/月）")
    
    try:
        # 使用 Bearer Token（推荐）
        if TWITTER_BEARER_TOKEN:
            client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)
        else:
            # 使用 OAuth 1.0a
            auth = tweepy.OAuth1UserHandler(
                TWITTER_API_KEY,
                TWITTER_API_SECRET,
                TWITTER_ACCESS_TOKEN,
                TWITTER_ACCESS_TOKEN_SECRET
            )
            api = tweepy.API(auth)
            client = tweepy.Client(
                consumer_key=TWITTER_API_KEY,
                consumer_secret=TWITTER_API_SECRET,
                access_token=TWITTER_ACCESS_TOKEN,
                access_token_secret=TWITTER_ACCESS_TOKEN_SECRET
            )
        
        # 获取用户信息
        username = TWITTER_USERNAME or input("请输入 Twitter 用户名: ").strip()
        if not username:
            print("❌ 需要 Twitter 用户名")
            return []
        
        # 获取用户 ID
        user = client.get_user(username=username.replace("@", ""))
        user_id = user.data.id
        
        # 获取现有数据，找出最新的推文 ID
        existing = load_existing_data()
        twitter_items = [item for item in existing.values() if item.get("source") == "twitter"]
        latest_id = None
        if twitter_items:
            # 找到最新的推文 ID（假设 ID 是数字）
            latest_ids = [item.get("id") for item in twitter_items if isinstance(item.get("id"), int)]
            if latest_ids:
                latest_id = max(latest_ids)
        
        print(f"📊 当前最新推文 ID: {latest_id}")
        print("📥 正在获取新推文...")
        
        # 获取推文（最多 100 条）
        new_items = []
        tweets = client.get_users_tweets(
            id=user_id,
            max_results=100,
            since_id=latest_id,
            tweet_fields=['created_at', 'public_metrics', 'entities']
        )
        
        if tweets.data:
            for tweet in tweets.data:
                # 提取链接（从 entities 中提取）
                content_urls = []
                if tweet.entities and 'urls' in tweet.entities:
                    urls = tweet.entities['urls']
                    for url_obj in urls:
                        url = url_obj.get('expanded_url', '') or url_obj.get('url', '')
                        if url and not should_exclude_url(url) and url not in content_urls:
                            content_urls.append(url)
                
                # 从纯文本中提取 URL（补充提取，已包含过滤）
                if tweet.text:
                    urls_from_text = extract_urls_from_text(tweet.text)
                    for url in urls_from_text:
                        if url not in content_urls:
                            content_urls.append(url)
                
                # 生成 Twitter 链接
                twitter_link = f"https://twitter.com/{username}/status/{tweet.id}"
                
                item = {
                    "source": "twitter",
                    "type": "tweet",
                    "title": "Twitter Post",
                    "content": tweet.text,
                    "url": content_urls[0] if content_urls else "",  # 第一个链接（向后兼容）
                    "urls": content_urls,  # 所有链接列表
                    "tg_link": twitter_link,
                    "date": tweet.created_at.isoformat() if tweet.created_at else "",
                    "id": int(tweet.id)
                }
                new_items.append(item)
                print(f"  ✓ 获取推文 {tweet.id}: {tweet.text[:50]}...")
        
        print(f"\n✅ 获取到 {len(new_items)} 条新推文")
        return new_items
        
    except Exception as e:
        print(f"❌ 获取失败: {e}")
        return []


def show_current_status():
    """显示当前 Twitter 数据状态"""
    existing = load_existing_data()
    twitter_items = [item for item in existing.values() if item.get("source") == "twitter"]
    
    if twitter_items:
        # 获取最新和最早的日期
        dates = [item.get("date", "") for item in twitter_items if item.get("date")]
        dates.sort()
        
        print(f"📊 当前 Twitter 数据状态:")
        print(f"   - 总推文数: {len(twitter_items)}")
        if dates:
            print(f"   - 最早推文: {dates[0]}")
            print(f"   - 最新推文: {dates[-1]}")
    else:
        print("📊 当前没有 Twitter 数据")


def main():
    print("🐦 Twitter 新帖子获取方法")
    print("=" * 50)
    print()
    
    show_current_status()
    print()
    
    print("可用方法：")
    print()
    print("1️⃣  导出文件方法（推荐，最简单，免费）")
    print("   - 在 Twitter 设置中导出数据")
    print("   - 运行: python3 import_twitter.py <文件路径>")
    print()
    
    print("2️⃣  Twitter API（需要付费 $100/月）")
    print("   - 需要申请 Twitter Developer 账号")
    print("   - 需要配置 API 密钥")
    print("   - 可以自动获取新推文")
    print()
    
    choice = input("选择方法 (1/2) 或按回车查看详细说明: ").strip()
    
    if choice == "1":
        fetch_via_export()
    elif choice == "2":
        new_items = fetch_via_api()
        if new_items:
            # 更新数据库
            existing = load_existing_data()
            for item in new_items:
                existing[item["id"]] = item
            save_to_jsonl(list(existing.values()))
            
            print(f"✅ 已更新数据库，新增 {len(new_items)} 条推文")
            
            # 询问是否推送到 GitHub
            push = input("\n是否推送到 GitHub? (y/n): ").strip().lower()
            if push == "y":
                from update_data import push_to_github
                push_to_github()
    else:
        print("\n详细说明：")
        print("-" * 50)
        fetch_via_export()
        print()
        print("⚠️  关于 Twitter API：")
        print("Twitter API 现在需要付费订阅（$100/月），")
        print("对于个人用户，建议使用导出文件方式。")


if __name__ == "__main__":
    main()


