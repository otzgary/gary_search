"""
更新现有数据的 type 字段
为旧数据添加类型标识
"""
from search import load_all_items
from update_data import save_to_jsonl

def update_data_types():
    """为现有数据添加 type 字段"""
    print("🔄 更新数据类型...")
    
    items = load_all_items()
    updated_count = 0
    
    for item in items:
        source = item.get("source", "")
        current_type = item.get("type", "")
        
        # 如果已经有 type，跳过
        if current_type:
            continue
        
        # 根据 source 和 title 判断类型
        if source == "twitter":
            # 检查是否是回复
            if "Reply" in item.get("title", ""):
                item["type"] = "reply"
            else:
                item["type"] = "tweet"
            updated_count += 1
        elif source == "tg":
            item["type"] = "post"
            updated_count += 1
    
    if updated_count > 0:
        save_to_jsonl(items)
        print(f"✅ 已更新 {updated_count} 条数据的类型")
    else:
        print("ℹ️  所有数据已有类型标识")
    
    # 统计
    twitter_tweets = len([i for i in items if i.get("source") == "twitter" and i.get("type") == "tweet"])
    twitter_replies = len([i for i in items if i.get("source") == "twitter" and i.get("type") == "reply"])
    tg_posts = len([i for i in items if i.get("source") == "tg" and i.get("type") == "post"])
    
    print(f"\n📊 数据统计:")
    print(f"  🐦 Twitter 推文: {twitter_tweets} 条")
    print(f"  💬 Twitter 回复: {twitter_replies} 条")
    print(f"  📱 Telegram 帖子: {tg_posts} 条")
    print(f"  📦 总计: {len(items)} 条")


if __name__ == "__main__":
    update_data_types()

