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
    filter_type = request.args.get('type', '').strip()  # 筛选类型: tweet, reply, post, all
    
    if not query:
        return jsonify({'results': [], 'count': 0})
    
    items = get_items()
    results = search_items(items, query)
    
    # 按类型筛选
    if filter_type and filter_type != 'all':
        if filter_type == 'tweet':
            results = [r for r in results if r.get('source') == 'twitter' and r.get('type') == 'tweet']
        elif filter_type == 'reply':
            results = [r for r in results if r.get('source') == 'twitter' and r.get('type') == 'reply']
        elif filter_type == 'retweet':
            results = [r for r in results if r.get('source') == 'twitter' and r.get('type') == 'retweet']
        elif filter_type == 'quote':
            results = [r for r in results if r.get('source') == 'twitter' and r.get('type') == 'quote']
        elif filter_type == 'post':
            results = [r for r in results if r.get('source') == 'tg']
    
    # 格式化结果用于 JSON 返回
    formatted_results = []
    for item in results:
        # 获取所有链接（优先使用 urls 列表，如果没有则使用单个 url）
        urls = item.get('urls', [])
        if not urls and item.get('url'):
            urls = [item.get('url')]
        
        formatted_results.append({
            'source': item.get('source', 'unknown'),
            'type': item.get('type', 'unknown'),  # tweet, reply, post
            'title': item.get('title', ''),
            'content': item.get('content', ''),
            'url': item.get('url', ''),  # 第一个链接（向后兼容）
            'urls': urls,  # 所有链接列表
            'tg_link': item.get('tg_link', ''),  # Telegram 消息链接或 Twitter 链接
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
    print("访问 http://127.0.0.1:8080 来使用搜索功能")
    app.run(debug=True, host='127.0.0.1', port=8080)

