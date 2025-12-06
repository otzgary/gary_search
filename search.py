import json
import os
from typing import List, Dict, Any

# 数据文件路径
TG_DATA_FILE = "ChatExport_2025-12-06/result.json"
DATA_FILE = "data.jsonl"

# Telegram 频道配置
# 如果频道是公开的，请在这里设置频道用户名（例如: "yourchannel" 或 "@yourchannel"）
# 如果频道是私有的，留空即可，会自动使用频道 ID
TG_CHANNEL_USERNAME = "gary10x"  # 公开频道用户名


def extract_text_from_message(text_field: Any) -> str:
    """从消息的 text 字段提取纯文本内容"""
    if isinstance(text_field, str):
        return text_field
    elif isinstance(text_field, list):
        result = []
        for item in text_field:
            if isinstance(item, str):
                result.append(item)
            elif isinstance(item, dict):
                # 如果是链接或其他实体，提取文本
                if "text" in item:
                    result.append(item["text"])
        return "".join(result)
    return ""


def load_tg_messages() -> List[Dict[str, Any]]:
    """从 Telegram 导出的 JSON 文件加载消息"""
    if not os.path.exists(TG_DATA_FILE):
        return []
    
    items = []
    with open(TG_DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        messages = data.get("messages", [])
        channel_name = data.get("name", "Unknown")
        channel_id = data.get("id", "")
        channel_type = data.get("type", "")
        channel_username = data.get("username", "")  # 尝试获取用户名
        
        for msg in messages:
            # 只处理普通消息，跳过服务消息
            if msg.get("type") != "message":
                continue
            
            text = extract_text_from_message(msg.get("text", ""))
            if not text.strip():
                continue
            
            message_id = msg.get("id", 0)
            
            # 生成 Telegram 消息链接
            # 对于公开频道且有用户名: https://t.me/{username}/{message_id}
            # 对于私有频道或无用户名: https://t.me/c/-100{channel_id}/{message_id}
            tg_link = ""
            if channel_id and message_id:
                # 优先使用配置的用户名
                username_to_use = TG_CHANNEL_USERNAME.strip() if TG_CHANNEL_USERNAME else (channel_username.strip() if channel_username else "")
                
                # 如果 channel_id 是字符串且以 "channel" 开头，提取数字部分
                if isinstance(channel_id, str) and channel_id.startswith("channel"):
                    channel_id = channel_id.replace("channel", "")
                
                # 如果有用户名，使用公开频道格式
                if username_to_use:
                    # 移除 @ 符号（如果有）
                    username = username_to_use.replace("@", "").strip()
                    tg_link = f"https://t.me/{username}/{message_id}"
                else:
                    # 使用私有频道格式，需要 -100 前缀
                    try:
                        channel_id_int = int(channel_id)
                        # Telegram 私有频道 ID 需要转换为 -100{id} 格式
                        tg_link = f"https://t.me/c/-100{channel_id_int}/{message_id}"
                    except (ValueError, TypeError):
                        # 如果转换失败，尝试直接使用
                        tg_link = f"https://t.me/c/{channel_id}/{message_id}"
            
            # 提取消息内容中的链接（如果有）
            content_url = ""
            text_entities = msg.get("text_entities", [])
            for entity in text_entities:
                if entity.get("type") == "link":
                    content_url = entity.get("text", "")
                    break
            
            # 如果没有从 text_entities 找到，从 text 字段中提取
            if not content_url:
                text_field = msg.get("text", "")
                if isinstance(text_field, list):
                    for item in text_field:
                        if isinstance(item, dict) and item.get("type") == "link":
                            content_url = item.get("text", "")
                            break
            
            item = {
                "source": "tg",
                "title": channel_name,
                "content": text,
                "url": content_url,  # 消息内容中的链接
                "tg_link": tg_link,  # Telegram 消息链接
                "date": msg.get("date", ""),
                "id": message_id
            }
            items.append(item)
    
    return items


def load_jsonl_items() -> List[Dict[str, Any]]:
    """从 JSONL 文件加载数据"""
    if not os.path.exists(DATA_FILE):
        return []
    
    items = []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                items.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return items


def load_all_items() -> List[Dict[str, Any]]:
    """加载所有数据源"""
    items = []
    
    # 优先从 JSONL 加载（统一数据源）
    jsonl_items = load_jsonl_items()
    if jsonl_items:
        items.extend(jsonl_items)
    else:
        # 如果 JSONL 为空，从 Telegram JSON 加载（兼容旧数据）
        tg_items = load_tg_messages()
        items.extend(tg_items)
    
    # 去重（基于 ID）
    seen_ids = set()
    unique_items = []
    for item in items:
        item_id = item.get("id", 0)
        if item_id and item_id not in seen_ids:
            seen_ids.add(item_id)
            unique_items.append(item)
    
    return unique_items


def search_items(items: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
    """搜索内容"""
    if not query:
        return []
    
    q = query.lower()
    results = []
    
    for item in items:
        # 搜索标题和内容
        title = item.get("title", "").lower()
        content = item.get("content", "").lower()
        
        if q in title or q in content:
            results.append(item)
    
    return results


def format_result(item: Dict[str, Any], index: int) -> str:
    """格式化搜索结果"""
    source = item.get("source", "unknown")
    title = item.get("title", "")
    content = item.get("content", "")
    url = item.get("url", "")
    date = item.get("date", "")
    
    # 截断过长的内容
    content_preview = content[:300] + "..." if len(content) > 300 else content
    
    result = f"{index}. [{source.upper()}] {title}\n"
    if date:
        result += f"   日期: {date}\n"
    result += f"   {content_preview}\n"
    if url:
        result += f"   链接: {url}\n"
    
    return result


if __name__ == "__main__":
    print("正在加载数据...")
    items = load_all_items()
    print(f"已载入 {len(items)} 条内容")
    print("（输入空行退出）\n")
    
    while True:
        query = input("🔍 搜索: ").strip()
        if not query:
            print("再见！")
            break
        
        results = search_items(items, query)
        print(f"\n找到 {len(results)} 条结果：\n")
        
        if results:
            for i, item in enumerate(results, start=1):
                print("-" * 60)
                print(format_result(item, i))
        else:
            print("没有找到相关结果")
        
        print()
