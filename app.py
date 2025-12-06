from flask import Flask, render_template, request, jsonify
from search import load_all_items, search_items
import os

app = Flask(__name__)

# 全局变量存储加载的数据
_items = None

def get_items():
    """懒加载数据，只在第一次使用时加载"""
    global _items
    if _items is None:
        _items = load_all_items()
    return _items

@app.route('/')
def index():
    """主页"""
    items = get_items()
    return render_template('index.html', total_count=len(items))

@app.route('/api/search')
def search():
    """搜索 API"""
    query = request.args.get('q', '').strip()
    
    if not query:
        return jsonify({'results': [], 'count': 0})
    
    items = get_items()
    results = search_items(items, query)
    
    # 格式化结果用于 JSON 返回
    formatted_results = []
    for item in results:
        formatted_results.append({
            'source': item.get('source', 'unknown'),
            'title': item.get('title', ''),
            'content': item.get('content', ''),
            'url': item.get('url', ''),  # 消息内容中的链接
            'tg_link': item.get('tg_link', ''),  # Telegram 消息链接
            'date': item.get('date', '')
        })
    
    return jsonify({
        'results': formatted_results,
        'count': len(formatted_results)
    })

if __name__ == '__main__':
    print("正在加载数据...")
    items = get_items()
    print(f"已载入 {len(items)} 条内容")
    print("\n启动 Web 服务器...")
    print("访问 http://127.0.0.1:5000 来使用搜索功能")
    app.run(debug=True, host='127.0.0.1', port=5000)

