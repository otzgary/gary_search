"""
更新 Twitter 推文链接
为已导入的 Twitter 推文生成正确的链接
"""
from search import load_all_items
from update_data import save_to_jsonl

# 配置你的 Twitter 用户名
TWITTER_USERNAME = "garyintern"  # 或 "otzgary"，根据你的账号


def update_twitter_links():
    """更新所有 Twitter 推文的链接"""
    print("🔗 更新 Twitter 推文链接...")
    
    items = load_all_items()
    twitter_items = [item for item in items if item.get("source") == "twitter"]
    
    if not twitter_items:
        print("❌ 没有找到 Twitter 推文")
        return
    
    print(f"📊 找到 {len(twitter_items)} 条 Twitter 推文")
    
    updated_count = 0
    for item in twitter_items:
        tweet_id = item.get("id", 0)
        if tweet_id and TWITTER_USERNAME:
            # 生成 Twitter 链接
            twitter_link = f"https://twitter.com/{TWITTER_USERNAME}/status/{tweet_id}"
            if item.get("tg_link") != twitter_link:
                item["tg_link"] = twitter_link
                updated_count += 1
    
    # 保存更新
    if updated_count > 0:
        save_to_jsonl(items)
        print(f"✅ 已更新 {updated_count} 条推文的链接")
    else:
        print("ℹ️  所有链接已是最新")
    
    # 显示示例
    if twitter_items:
        sample = twitter_items[0]
        print(f"\n示例链接: {sample.get('tg_link', '无')}")


if __name__ == "__main__":
    print("🐦 Twitter 链接更新工具")
    print("=" * 50)
    print()
    print(f"当前配置的用户名: {TWITTER_USERNAME}")
    print()
    
    choice = input("是否使用此用户名更新链接? (y/n): ").strip().lower()
    if choice == "y":
        update_twitter_links()
    else:
        new_username = input("请输入你的 Twitter 用户名: ").strip().replace("@", "")
        if new_username:
            TWITTER_USERNAME = new_username
            update_twitter_links()

