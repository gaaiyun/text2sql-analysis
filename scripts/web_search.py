"""
网络搜索集成工具
融合互联网信息检索，补充数据库查询结果

使用方法:
    python web_search.py "人工智能行业发展趋势"
"""

from duckduckgo_search import DDGS
import json
import sys

def search_web(query, max_results=5, time_range='year'):
    """
    搜索网络信息
    
    参数:
        query: 搜索关键词
        max_results: 最大结果数（默认 5）
        time_range: 时间范围 ('day', 'week', 'month', 'year')
    
    返回:
        list of dict，包含标题、摘要、链接
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(
                query, 
                max_results=max_results,
                timelimit=time_range
            ))
        
        formatted_results = []
        for r in results:
            formatted_results.append({
                'title': r.get('title', ''),
                'snippet': r.get('body', ''),
                'url': r.get('href', ''),
                'source': r.get('href', '').split('/')[2] if r.get('href') else ''
            })
        
        return formatted_results
    except Exception as e:
        print(f"❌ 搜索失败: {e}")
        return []

def search_news(query, max_results=3):
    """搜索新闻"""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.news(query, max_results=max_results))
        
        formatted_results = []
        for r in results:
            formatted_results.append({
                'title': r.get('title', ''),
                'snippet': r.get('body', ''),
                'url': r.get('url', ''),
                'date': r.get('date', ''),
                'source': r.get('source', '')
            })
        
        return formatted_results
    except Exception as e:
        print(f"❌ 新闻搜索失败: {e}")
        return []

def enhance_analysis(db_data, search_query):
    """
    增强分析 - 结合数据库结果和网络搜索
    
    参数:
        db_data: 数据库查询结果
        search_query: 搜索关键词
    
    返回:
        dict 包含数据库数据 + 网络搜索结果 + 综合分析
    """
    print(f"🔍 搜索: {search_query}")
    
    # 执行网络搜索
    web_results = search_web(search_query, max_results=5)
    news_results = search_news(search_query, max_results=3)
    
    # 整合结果
    enhanced = {
        'database_data': db_data,
        'web_insights': web_results,
        'news_updates': news_results,
        'summary': generate_summary(db_data, web_results)
    }
    
    return enhanced

def generate_summary(db_data, web_results):
    """生成综合分析摘要"""
    summary = []
    
    # 从网络结果提取关键信息
    key_points = []
    for result in web_results[:3]:
        snippet = result.get('snippet', '')
        if len(snippet) > 50:
            key_points.append(snippet[:150] + '...')
    
    summary = {
        'key_findings': key_points,
        'data_sources': ['自有数据库', '互联网搜索'],
        'confidence': '高' if len(web_results) >= 3 else '中'
    }
    
    return summary

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python web_search.py \"搜索关键词\"")
        sys.exit(1)
    
    query = sys.argv[1]
    results = search_web(query)
    
    print(f"\n🔍 搜索结果 ({len(results)} 条):\n")
    for idx, r in enumerate(results, 1):
        print(f"{idx}. {r['title']}")
        print(f"   {r['snippet'][:100]}...")
        print(f"   来源: {r['source']}\n")
