"""
导入 Twitter 历史帖子
支持 Twitter 数据导出文件
"""
import json
import os
import zipfile
from typing import List, Dict, Any
from update_data import load_existing_data, save_to_jsonl
from search import extract_urls_from_text, should_exclude_url

# Twitter 配置
TWITTER_USERNAME = ""  # 你的 Twitter 用户名（可选，用于生成链接）


def extract_twitter_zip(zip_path: str, extract_to: str = "twitter_export") -> str:
    """解压 Twitter 导出 ZIP 文件"""
    if not os.path.exists(zip_path):
        raise FileNotFoundError(f"文件不存在: {zip_path}")
    
    # 创建解压目录
    os.makedirs(extract_to, exist_ok=True)
    
    # 解压文件
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    
    print(f"✅ 已解压到: {extract_to}")
    return extract_to


def parse_twitter_json(json_path: str) -> List[Dict[str, Any]]:
    """解析 Twitter JSON 文件"""
    items = []
    
    with open(json_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
        # Twitter 导出文件可能是 JavaScript 格式，需要处理
        # 格式通常是: window.YTD.tweets.part0 = [ ... ];
        if 'window.YTD.tweets.part' in content:
            # 提取 JSON 部分
            start = content.find('[')
            end = content.rfind(']') + 1
            if start != -1 and end != 0:
                json_str = content[start:end]
                data = json.loads(json_str)
            else:
                print("⚠️  无法解析 Twitter 导出文件格式")
                return []
        else:
            # 标准 JSON 格式
            data = json.load(f)
    
    # 处理数据
    for tweet_data in data:
        # Twitter 导出格式: { "tweet": { ... } }
        if isinstance(tweet_data, dict) and 'tweet' in tweet_data:
            tweet = tweet_data['tweet']
        elif isinstance(tweet_data, dict):
            tweet = tweet_data
        else:
            continue
        
        # 提取推文信息
        full_text = tweet.get('full_text', '') or tweet.get('text', '')
        if not full_text:
            continue
        
        # 提取日期
        created_at = tweet.get('created_at', '')
        
        # 提取推文 ID
        tweet_id = tweet.get('id_str') or str(tweet.get('id', ''))
        
        # 提取链接（从 entities 中提取）
        content_urls = []
        entities = tweet.get('entities', {})
        urls = entities.get('urls', [])
        for url_obj in urls:
            # 优先使用展开的 URL
            url = url_obj.get('expanded_url') or url_obj.get('url', '')
            if url and not should_exclude_url(url) and url not in content_urls:
                content_urls.append(url)
        
        # 从纯文本中提取 URL（补充提取，已包含过滤）
        urls_from_text = extract_urls_from_text(full_text)
        for url in urls_from_text:
            if url not in content_urls:
                content_urls.append(url)
        
        # 生成 Twitter 链接
        username = TWITTER_USERNAME or tweet.get('user', {}).get('screen_name', '')
        twitter_link = f"https://twitter.com/{username}/status/{tweet_id}" if username and tweet_id else ""
        
        # 判断推文类型
        in_reply_to_status_id = tweet.get('in_reply_to_status_id_str')
        is_reply = bool(in_reply_to_status_id)
        
        # 检查是否是转发（retweeted_status 字段存在）
        is_retweet = 'retweeted_status' in tweet
        
        # 检查是否是引用推文（quoted_status 字段存在）
        is_quote = 'quoted_status' in tweet
        
        # 检查内容是否以 RT @ 开头（手动转发）
        is_manual_rt = full_text.strip().startswith('RT @')
        
        # 确定类型
        if is_retweet:
            tweet_type = "retweet"
            title_suffix = " (Retweet)"
        elif is_quote:
            tweet_type = "quote"
            title_suffix = " (Quote)"
        elif is_manual_rt:
            tweet_type = "retweet"  # 手动转发也归类为 retweet
            title_suffix = " (Retweet)"
        elif is_reply:
            tweet_type = "reply"
            title_suffix = " (Reply)"
        else:
            tweet_type = "tweet"
            title_suffix = ""
        
        item = {
            "source": "twitter",
            "type": tweet_type,  # tweet, reply, retweet, quote
            "title": f"Twitter Post{title_suffix}",
            "content": full_text,
            "url": content_urls[0] if content_urls else "",  # 第一个链接（向后兼容）
            "urls": content_urls,  # 所有链接列表
            "tg_link": twitter_link,  # 复用字段存储 Twitter 链接
            "date": created_at,
            "id": int(tweet_id) if tweet_id.isdigit() else hash(tweet_id)
        }
        
        items.append(item)
    
    return items


def import_twitter_export(export_path: str) -> int:
    """导入 Twitter 导出文件"""
    print(f"📥 正在导入 Twitter 数据: {export_path}")
    
    # 检查文件类型
    if export_path.endswith('.zip'):
        # 解压 ZIP 文件
        extract_dir = extract_twitter_zip(export_path)
        
        # 查找 tweets.js 或 tweets.json 文件
        tweets_file = None
        for root, dirs, files in os.walk(extract_dir):
            for file in files:
                if file.startswith('tweet') and (file.endswith('.js') or file.endswith('.json')):
                    tweets_file = os.path.join(root, file)
                    break
            if tweets_file:
                break
        
        if not tweets_file:
            # 尝试查找 data/tweets.js
            possible_paths = [
                os.path.join(extract_dir, 'data', 'tweets.js'),
                os.path.join(extract_dir, 'data', 'tweets.json'),
                os.path.join(extract_dir, 'tweets.js'),
                os.path.join(extract_dir, 'tweets.json'),
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    tweets_file = path
                    break
        
        if not tweets_file:
            print("❌ 未找到 tweets.js 或 tweets.json 文件")
            print("请检查导出文件结构")
            return 0
        
        print(f"📄 找到推文文件: {tweets_file}")
    else:
        # 直接是 JSON 文件
        tweets_file = export_path
    
    # 解析推文
    print("📖 正在解析推文...")
    new_items = parse_twitter_json(tweets_file)
    
    if not new_items:
        print("❌ 未找到推文数据")
        return 0
    
    print(f"✅ 解析到 {len(new_items)} 条推文")
    
    # 加载现有数据
    existing = load_existing_data()
    
    # 合并数据（去重）
    new_count = 0
    for item in new_items:
        item_id = item.get("id", 0)
        if item_id and item_id not in existing:
            existing[item_id] = item
            new_count += 1
    
    # 保存
    save_to_jsonl(list(existing.values()))
    
    print(f"✅ 已导入 {new_count} 条新推文（共 {len(existing)} 条）")
    
    return new_count


def main():
    import sys
    
    print("🐦 Twitter 历史帖子导入工具")
    print("=" * 50)
    print()
    
    if len(sys.argv) > 1:
        export_path = sys.argv[1]
    else:
        export_path = input("请输入 Twitter 导出文件路径（ZIP 或 JSON）: ").strip()
        if not export_path:
            print("❌ 未提供文件路径")
            return
    
    if not os.path.exists(export_path):
        print(f"❌ 文件不存在: {export_path}")
        return
    
    # 导入数据
    new_count = import_twitter_export(export_path)
    
    if new_count > 0:
        print()
        push = input("是否推送到 GitHub? (y/n): ").strip().lower()
        if push == "y":
            from update_data import push_to_github
            push_to_github()
    
    print()
    print("✅ 完成！现在可以在搜索系统中搜索 Twitter 内容了")


if __name__ == "__main__":
    main()

