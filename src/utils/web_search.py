#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
网络搜索模块

封装 Tavily（首选）与 DuckDuckGo（备选，免费无需 API Key），
返回结构化结果，供 API 服务器与报告增强使用。
"""

import os
from typing import List, Dict, Any, Optional


def search(
    query: str,
    max_results: int = 5,
    time_range: str = "year",
    use_tavily: bool = True,
) -> List[Dict[str, Any]]:
    """
    执行网络搜索，优先 Tavily，无 key 时回退 DuckDuckGo。

    Args:
        query: 搜索关键词
        max_results: 返回条数（默认 5）
        time_range: 时间范围（day/week/month/year），DuckDuckGo 用
        use_tavily: 是否优先尝试 Tavily

    Returns:
        [{"title": "", "snippet": "", "url": "", "source": ""}, ...]
    """
    if not (query or "").strip():
        return []

    # 1. 尝试 Tavily（需环境变量 TAVILY_API_KEY）
    if use_tavily:
        api_key = os.environ.get("TAVILY_API_KEY", "").strip()
        if api_key:
            try:
                return _tavily_search(query, max_results=max_results)
            except Exception:
                pass

    # 2. 回退 DuckDuckGo（免费）
    try:
        return _duckduckgo_search(query, max_results=max_results, time_range=time_range)
    except Exception:
        return []


def _tavily_search(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """Tavily API（专为 AI 设计，结果质量高）"""
    try:
        from tavily import TavilyClient
    except ImportError:
        raise ImportError("tavily-python not installed")
    client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))
    response = client.search(query, max_results=max_results)
    results = []
    for r in getattr(response, "results", []) or []:
        results.append({
            "title": getattr(r, "title", "") or "",
            "snippet": getattr(r, "content", "") or getattr(r, "snippet", "") or "",
            "url": getattr(r, "url", "") or "",
            "source": _domain_from_url(getattr(r, "url", "") or ""),
        })
    return results[:max_results]


def _domain_from_url(url: str) -> str:
    if not url:
        return ""
    try:
        from urllib.parse import urlparse
        return urlparse(url).netloc or ""
    except Exception:
        return ""


def _duckduckgo_search(
    query: str,
    max_results: int = 5,
    time_range: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """DuckDuckGo 文本搜索（免费，无需 API key）。time_range: d/w/m/y 或 None 表示不限制"""
    try:
        from duckduckgo_search import DDGS
    except ImportError:
        raise ImportError("duckduckgo-search not installed")
    kwargs = {"max_results": max_results}
    if time_range in ("d", "w", "m", "y"):
        kwargs["timelimit"] = time_range
    elif time_range == "day":
        kwargs["timelimit"] = "d"
    elif time_range == "week":
        kwargs["timelimit"] = "w"
    elif time_range == "month":
        kwargs["timelimit"] = "m"
    elif time_range == "year":
        kwargs["timelimit"] = "y"
    with DDGS() as ddgs:
        raw = list(ddgs.text(query, **kwargs))
    results = []
    for r in raw:
        results.append({
            "title": r.get("title", ""),
            "snippet": r.get("body", ""),
            "url": r.get("href", ""),
            "source": _domain_from_url(r.get("href", "")),
        })
    return results


def search_news(query: str, max_results: int = 3) -> List[Dict[str, Any]]:
    """新闻搜索（DuckDuckGo 新闻）"""
    if not (query or "").strip():
        return []
    try:
        from duckduckgo_search import DDGS
    except ImportError:
        return []
    try:
        with DDGS() as ddgs:
            raw = list(ddgs.news(query, max_results=max_results))
        return [
            {
                "title": r.get("title", ""),
                "snippet": r.get("body", ""),
                "url": r.get("url", ""),
                "source": r.get("source", ""),
                "date": r.get("date", ""),
            }
            for r in raw
        ]
    except Exception:
        return []


def duckduckgo_search(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    对外兼容名：仅使用 DuckDuckGo 搜索。
    供 api_server 与旧脚本调用。
    """
    return _duckduckgo_search(query, max_results=max_results)
