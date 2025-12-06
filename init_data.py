"""
初始化数据脚本
将现有的 Telegram 导出数据转换为统一的 JSONL 格式
"""
from search import load_tg_messages
import json

def init_data():
    """初始化数据，将 Telegram 数据转换为 JSONL"""
    print("正在加载 Telegram 数据...")
    tg_items = load_tg_messages()
    
    if not tg_items:
        print("没有找到 Telegram 数据")
        return
    
    print(f"找到 {len(tg_items)} 条消息")
    print("正在保存到 data.jsonl...")
    
    # 按日期排序
    tg_items.sort(key=lambda x: x.get("date", ""), reverse=True)
    
    with open("data.jsonl", "w", encoding="utf-8") as f:
        for item in tg_items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    
    print(f"✅ 已成功初始化 {len(tg_items)} 条数据到 data.jsonl")
    print("\n下一步:")
    print("1. 检查 data.jsonl 文件")
    print("2. 运行: python3 update_data.py push  # 推送到 GitHub")

if __name__ == "__main__":
    init_data()

