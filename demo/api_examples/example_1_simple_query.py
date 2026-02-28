#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简单API调用示例 - 基础查询

演示如何调用Text2SQL API进行基础查询
"""
import requests
import json

API_BASE = "http://localhost:8000"

def example_simple_query():
    """示例1：简单查询"""
    print("=" * 60)
    print("示例1：简单查询 - 分析近五年融资趋势")
    print("=" * 60)
    
    response = requests.post(
        f"{API_BASE}/api/query",
        json={
            "question": "分析近五年融资趋势",
            "scenario": "data_insight",
            "mode": "llm"  # 使用LLM模式
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✓ 查询成功")
        print(f"生成的SQL:\n{result['sql']}\n")
        print(f"返回行数: {result['row_count']}")
        print(f"列名: {result['columns']}")
        print(f"\n前3行数据:")
        for i, row in enumerate(result['data'][:3], 1):
            print(f"  {i}. {row}")
    else:
        print(f"\n✗ 查询失败: {response.status_code}")
        print(response.text)

def example_with_scenario():
    """示例2：指定场景查询"""
    print("\n" + "=" * 60)
    print("示例2：场景查询 - 统计各行业企业数量")
    print("=" * 60)
    
    response = requests.post(
        f"{API_BASE}/api/query",
        json={
            "question": "统计各行业的企业数量分布",
            "scenario": "data_insight",
            "mode": "auto"  # 自动选择模式
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✓ 查询成功 (模式: {result['mode']})")
        print(f"生成的SQL:\n{result['sql']}\n")
        print(f"返回行数: {result['row_count']}")
        print(f"\n前5行数据:")
        for i, row in enumerate(result['data'][:5], 1):
            print(f"  {i}. {row}")
    else:
        print(f"\n✗ 查询失败: {response.status_code}")

def example_vanna_fallback():
    """示例3：Vanna兜底"""
    print("\n" + "=" * 60)
    print("示例3：Vanna兜底 - 查询地区企业分布")
    print("=" * 60)
    
    response = requests.post(
        f"{API_BASE}/api/query",
        json={
            "question": "查询各省份的企业数量",
            "scenario": "regional",
            "mode": "vanna"  # 强制使用Vanna
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✓ 查询成功 (模式: {result['mode']})")
        print(f"生成的SQL:\n{result['sql']}\n")
        print(f"返回行数: {result['row_count']}")
    else:
        print(f"\n✗ 查询失败: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Text2SQL API 简单调用示例")
    print("=" * 60)
    print(f"API地址: {API_BASE}")
    print("确保API服务已启动: python api_server.py")
    print("=" * 60)
    
    try:
        # 检查API健康状态
        health = requests.get(f"{API_BASE}/health", timeout=5)
        if health.status_code == 200:
            status = health.json()
            print(f"\n✓ API服务正常")
            print(f"  - LLM: {'✓' if status.get('llm') else '✗'}")
            print(f"  - Vanna: {'✓' if status.get('vanna') else '✗'}")
        else:
            print(f"\n✗ API服务异常")
            exit(1)
    except Exception as e:
        print(f"\n✗ 无法连接到API服务: {e}")
        print("请先启动API服务: python api_server.py")
        exit(1)
    
    # 运行示例
    example_simple_query()
    example_with_scenario()
    example_vanna_fallback()
    
    print("\n" + "=" * 60)
    print("示例运行完成")
    print("=" * 60)
