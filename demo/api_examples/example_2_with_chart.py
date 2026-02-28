#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
API调用示例 - 带图表生成

演示如何调用API并生成图表
"""
import requests
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from src.utils.chart_generator import generate_chart_auto

API_BASE = "http://localhost:8000"
OUTPUT_DIR = Path(__file__).parent.parent.parent / "output"

def example_with_chart():
    """示例：查询并生成图表"""
    print("=" * 60)
    print("示例：查询 + 自动生成图表")
    print("=" * 60)
    
    # 1. 调用API查询
    print("\n[1/3] 调用API查询...")
    response = requests.post(
        f"{API_BASE}/api/query",
        json={
            "question": "分析近五年融资趋势",
            "scenario": "data_insight",
            "mode": "llm"
        }
    )
    
    if response.status_code != 200:
        print(f"✗ 查询失败: {response.status_code}")
        return
    
    result = response.json()
    print(f"✓ 查询成功")
    print(f"  SQL: {result['sql'][:80]}...")
    print(f"  返回行数: {result['row_count']}")
    
    # 2. 自动生成图表
    print("\n[2/3] 自动生成图表...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    chart_path = OUTPUT_DIR / "example_chart.png"
    
    chart_file = generate_chart_auto(
        columns=result['columns'],
        rows=result['data'],
        output_path=str(chart_path),
        title="融资趋势分析"
    )
    
    if chart_file:
        print(f"✓ 图表已生成: {chart_file}")
    else:
        print("✗ 图表生成失败（数据可能不适合可视化）")
    
    # 3. 显示数据摘要
    print("\n[3/3] 数据摘要:")
    for i, row in enumerate(result['data'][:5], 1):
        print(f"  {i}. {row}")
    
    print("\n" + "=" * 60)
    print("完成！")
    print("=" * 60)

def example_industry_distribution():
    """示例：行业分布饼图"""
    print("\n" + "=" * 60)
    print("示例：行业分布 + 饼图")
    print("=" * 60)
    
    # 1. 查询
    print("\n[1/2] 查询行业分布...")
    response = requests.post(
        f"{API_BASE}/api/query",
        json={
            "question": "统计各行业的企业数量，只显示前10个",
            "scenario": "industry",
            "mode": "llm"
        }
    )
    
    if response.status_code != 200:
        print(f"✗ 查询失败")
        return
    
    result = response.json()
    print(f"✓ 查询成功，返回 {result['row_count']} 行")
    
    # 2. 生成图表
    print("\n[2/2] 生成图表...")
    chart_path = OUTPUT_DIR / "industry_distribution.png"
    
    chart_file = generate_chart_auto(
        columns=result['columns'],
        rows=result['data'],
        output_path=str(chart_path),
        title="行业分布"
    )
    
    if chart_file:
        print(f"✓ 图表已生成: {chart_file}")
    else:
        print("✗ 图表生成失败")

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Text2SQL API + 图表生成示例")
    print("=" * 60)
    
    try:
        health = requests.get(f"{API_BASE}/health", timeout=5)
        if health.status_code != 200:
            print("✗ API服务异常")
            exit(1)
        print("✓ API服务正常")
    except Exception as e:
        print(f"✗ 无法连接到API: {e}")
        exit(1)
    
    example_with_chart()
    example_industry_distribution()
    
    print(f"\n图表保存在: {OUTPUT_DIR}")
