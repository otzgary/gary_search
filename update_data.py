"""
更新数据库脚本
支持从新的 Telegram 导出文件更新数据，或从 GitHub 拉取最新数据
"""
import json
import os
import shutil
from datetime import datetime
from typing import List, Dict, Any
from search import load_tg_messages, extract_text_from_message

# 数据文件路径
TG_DATA_FILE = "ChatExport_2025-12-06/result.json"
DATA_FILE = "data.jsonl"
TG_CHANNEL_USERNAME = "gary10x"


def load_existing_data() -> Dict[int, Dict[str, Any]]:
    """加载现有数据，返回以消息 ID 为键的字典"""
    existing = {}
    
    # 从 JSONL 加载
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    item = json.loads(line)
                    if item.get("source") == "tg" and item.get("id"):
                        existing[item["id"]] = item
                except json.JSONDecodeError:
                    continue
    
    # 从 Telegram JSON 加载
    tg_items = load_tg_messages()
    for item in tg_items:
        if item.get("id"):
            existing[item["id"]] = item
    
    return existing


def merge_new_telegram_export(new_export_path: str) -> int:
    """合并新的 Telegram 导出文件"""
    if not os.path.exists(new_export_path):
        print(f"错误: 文件 {new_export_path} 不存在")
        return 0
    
    existing = load_existing_data()
    new_count = 0
    
    with open(new_export_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        messages = data.get("messages", [])
        channel_name = data.get("name", "Unknown")
        channel_id = data.get("id", "")
        
        for msg in messages:
            if msg.get("type") != "message":
                continue
            
            message_id = msg.get("id", 0)
            if not message_id or message_id in existing:
                continue  # 已存在，跳过
            
            text = extract_text_from_message(msg.get("text", ""))
            if not text.strip():
                continue
            
            # 生成 Telegram 链接
            tg_link = f"https://t.me/{TG_CHANNEL_USERNAME}/{message_id}" if TG_CHANNEL_USERNAME else ""
            
            # 提取内容中的链接
            content_url = ""
            text_entities = msg.get("text_entities", [])
            for entity in text_entities:
                if entity.get("type") == "link":
                    content_url = entity.get("text", "")
                    break
            
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
                "url": content_url,
                "tg_link": tg_link,
                "date": msg.get("date", ""),
                "id": message_id
            }
            
            existing[message_id] = item
            new_count += 1
    
    # 保存到 JSONL
    save_to_jsonl(list(existing.values()))
    
    # 更新 Telegram JSON 文件（可选，备份最新版本）
    if new_count > 0:
        backup_path = f"ChatExport_{datetime.now().strftime('%Y-%m-%d')}/result.json"
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
        shutil.copy2(new_export_path, backup_path)
        print(f"已备份最新导出文件到: {backup_path}")
    
    return new_count


def save_to_jsonl(items: List[Dict[str, Any]]):
    """保存数据到 JSONL 文件"""
    # 按日期排序
    items.sort(key=lambda x: x.get("date", ""), reverse=True)
    
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


def update_from_github():
    """从 GitHub 拉取最新数据"""
    import subprocess
    
    try:
        # 拉取最新数据
        result = subprocess.run(
            ["git", "pull", "origin", "main"],
            capture_output=True,
            text=True,
            check=True
        )
        print("已从 GitHub 拉取最新数据")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Git 操作失败: {e.stderr}")
        return False
    except FileNotFoundError:
        print("Git 未安装或未初始化仓库")
        return False


def push_to_github():
    """推送数据到 GitHub"""
    import subprocess
    
    try:
        # 添加文件
        subprocess.run(["git", "add", DATA_FILE, TG_DATA_FILE], check=True)
        
        # 提交
        commit_msg = f"更新数据 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        
        # 推送
        result = subprocess.run(
            ["git", "push", "origin", "main"],
            capture_output=True,
            text=True,
            check=True
        )
        print("已推送到 GitHub")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Git 操作失败: {e.stderr}")
        return False
    except FileNotFoundError:
        print("Git 未安装或未初始化仓库")
        return False


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "merge":
            # 合并新的导出文件
            if len(sys.argv) > 2:
                new_file = sys.argv[2]
                print(f"正在合并新文件: {new_file}")
                new_count = merge_new_telegram_export(new_file)
                print(f"新增 {new_count} 条消息")
                
                # 询问是否推送到 GitHub
                if new_count > 0:
                    push = input("是否推送到 GitHub? (y/n): ").strip().lower()
                    if push == "y":
                        push_to_github()
            else:
                print("用法: python3 update_data.py merge <新导出文件路径>")
        
        elif command == "pull":
            # 从 GitHub 拉取
            update_from_github()
        
        elif command == "push":
            # 推送到 GitHub
            push_to_github()
        
        else:
            print("可用命令:")
            print("  merge <文件路径>  - 合并新的 Telegram 导出文件")
            print("  pull             - 从 GitHub 拉取最新数据")
            print("  push             - 推送数据到 GitHub")
    else:
        print("用法:")
        print("  python3 update_data.py merge <新导出文件路径>")
        print("  python3 update_data.py pull")
        print("  python3 update_data.py push")

