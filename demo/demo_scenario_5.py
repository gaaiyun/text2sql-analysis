#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
场景5：企业尽调 - 完整流水线Demo
自然语言输入 → SQL生成 → 执行 → 多维度分析 → Word报告
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.config import Config
from src.utils.document_generator import word_from_sections
from openai import OpenAI
import pymysql
from datetime import datetime
import os

def generate_sql(question: str, config: Config) -> str:
    """使用LLM生成SQL"""
    api_key = config.get_api_key('dashscope')
    base_url = os.environ.get('DASHSCOPE_BASE_URL', 'https://coding.dashscope.aliyuncs.com/v1')
    
    schema_path = Path(__file__).parent.parent / "schema" / "gaaiyun_2_schema.md"
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema = f.read()
    
    client = OpenAI(api_key=api_key, base_url=base_url)
    
    prompt = f"""你是SQL专家。根据Schema生成MySQL查询。

## Schema
{schema[:3000]}

## 规则
1. 查询企业的完整信息：基本信息、知识产权、诉讼、投标、纳税等
2. 使用LEFT JOIN关联多个表
3. LIMIT 1

## 问题
{question}

## SQL
"""
    
    response = client.chat.completions.create(
        model="qwen3.5-plus",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.1
    )
    
    sql = response.choices[0].message.content.strip()
    sql = sql.replace('```sql', '').replace('```', '').strip()
    return sql

def execute_sql(sql: str, db_config: dict) -> tuple:
    """执行SQL查询"""
    conn = pymysql.connect(**db_config)
    cur = conn.cursor()
    cur.execute(sql)
    columns = [desc[0] for desc in cur.description]
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return columns, rows

def analyze_company(question: str, columns: list, rows: list, config: Config) -> str:
    """使用LLM分析企业"""
    api_key = config.get_api_key('dashscope')
    base_url = os.environ.get('DASHSCOPE_BASE_URL', 'https://coding.dashscope.aliyuncs.com/v1')
    
    if not rows:
        return "未查询到企业数据"
    
    data_dict = dict(zip(columns, rows[0]))
    
    client = OpenAI(api_key=api_key, base_url=base_url)
    
    prompt = f"""你是企业尽调专家。根据企业数据进行全面分析。

企业数据：
{data_dict}

请提供8个维度的尽调分析：
1. 基本信息
2. 经营状况
3. 知识产权
4. 法律风险
5. 财务健康
6. 招投标情况
7. 纳税情况
8. 综合评估

用中文回答，专业详细。"""
    
    response = client.chat.completions.create(
        model="qwen3.5-plus",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500,
        temperature=0.3
    )
    
    return response.choices[0].message.content.strip()

def main():
    question = "查询第一家企业的完整信息，进行全面尽职调查"
    
    print("\n" + "=" * 80)
    print("场景5：企业尽调")
    print("=" * 80)
    print(f"\n问题：{question}\n")
    
    try:
        # 1. 加载配置
        print("[1/5] 加载配置...")
        config = Config.load()
        db_config = config.get_database_config('scenario_4_5')
        
        # 2. 生成SQL
        print("[2/5] 生成SQL...")
        sql = generate_sql(question, config)
        print(f"生成的SQL:\n{sql}\n")
        
        # 3. 执行查询
        print("[3/5] 执行查询...")
        columns, rows = execute_sql(sql, db_config)
        print(f"查询结果：{len(rows)}条记录\n")
        
        # 4. LLM分析
        print("[4/5] 企业尽调分析...")
        analysis = analyze_company(question, columns, rows, config)
        print(f"分析完成\n")
        
        # 5. 生成Word报告
        print("[5/5] 生成Word报告...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        company_name = rows[0][0] if rows else "未知企业"
        
        sections = [
            {"heading": "企业基本信息", "content": f"企业名称：{company_name}"},
            {"heading": "尽职调查分析", "content": analysis},
            {"heading": "综合评估", "content": "基于以上分析，该企业整体情况良好。"},
        ]
        
        word_path = f"output/scenario_5_due_diligence_{timestamp}.docx"
        Path(word_path).parent.mkdir(parents=True, exist_ok=True)
        word_from_sections(sections, word_path, title=f"{company_name} 尽职调查报告")
        
        print(f"Word报告：{word_path}")
        
        print("\n" + "=" * 80)
        print("[OK] 场景5完成！")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n错误：{e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
