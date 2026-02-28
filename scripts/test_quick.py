#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
快速测试 Demo - 测试完整的 Text2SQL 流水线
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.config import Config
import pymysql
from openai import OpenAI
import os

def test_llm_connection():
    """测试 LLM 连接"""
    print("\n" + "=" * 60)
    print("测试 LLM 连接")
    print("=" * 60)
    
    try:
        config = Config.load()
        api_key = config.get_api_key('dashscope')
        base_url = os.environ.get('DASHSCOPE_BASE_URL', 'https://coding.dashscope.aliyuncs.com/v1')
        
        print(f"API Key: {api_key[:20]}...")
        print(f"Base URL: {base_url}")
        
        client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        
        response = client.chat.completions.create(
            model="qwen3.5-plus",
            messages=[
                {"role": "user", "content": "你好，请回复'连接成功'"}
            ],
            max_tokens=50
        )
        
        result = response.choices[0].message.content
        print(f"[OK] LLM 响应: {result}")
        return True
        
    except Exception as e:
        print(f"[ERROR] LLM 连接失败: {e}")
        return False

def test_simple_query():
    """测试简单的 SQL 查询"""
    print("\n" + "=" * 60)
    print("测试简单 SQL 查询")
    print("=" * 60)
    
    try:
        config = Config.load()
        db_config = config.get_database_config('scenario_1_3')
        
        conn = pymysql.connect(**db_config)
        cur = conn.cursor()
        
        # 查询融资数据表的前5条记录
        sql = "SELECT eid, round_date, amount FROM 融资数据 LIMIT 5"
        print(f"SQL: {sql}")
        
        cur.execute(sql)
        results = cur.fetchall()
        
        print(f"[OK] 查询成功，返回 {len(results)} 条记录")
        for row in results:
            print(f"  {row}")
        
        cur.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"[ERROR] 查询失败: {e}")
        return False

def test_text2sql():
    """测试 Text2SQL 生成"""
    print("\n" + "=" * 60)
    print("测试 Text2SQL 生成")
    print("=" * 60)
    
    try:
        config = Config.load()
        api_key = config.get_api_key('dashscope')
        base_url = os.environ.get('DASHSCOPE_BASE_URL', 'https://coding.dashscope.aliyuncs.com/v1')
        
        client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        
        # 简单的 Text2SQL 提示
        prompt = """你是SQL专家。根据以下表结构生成SQL查询。

表：融资数据
字段：eid (企业ID), round_date (融资日期), amount (融资金额)

问题：查询2023年的融资记录，按金额降序排列，限制10条

只返回SQL语句，不要其他内容。"""
        
        response = client.chat.completions.create(
            model="qwen3.5-plus",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.1
        )
        
        sql = response.choices[0].message.content.strip()
        print(f"[OK] 生成的 SQL:\n{sql}")
        return True
        
    except Exception as e:
        print(f"[ERROR] Text2SQL 生成失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("Text2SQL 快速测试")
    print("=" * 60)
    
    results = {}
    
    # 测试 LLM 连接
    results['llm'] = test_llm_connection()
    
    # 测试简单查询
    results['query'] = test_simple_query()
    
    # 测试 Text2SQL
    results['text2sql'] = test_text2sql()
    
    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    print(f"LLM 连接: {'[OK]' if results['llm'] else '[FAIL]'}")
    print(f"数据库查询: {'[OK]' if results['query'] else '[FAIL]'}")
    print(f"Text2SQL 生成: {'[OK]' if results['text2sql'] else '[FAIL]'}")
    print("=" * 60)
    
    if all(results.values()):
        print("[OK] 所有测试通过！系统可以正常使用。")
    else:
        print("[WARN] 部分测试失败，请检查配置。")

if __name__ == "__main__":
    main()
