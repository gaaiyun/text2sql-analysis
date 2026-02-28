#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
场景4：招商清单 - 完整流水线Demo
自然语言输入 → SQL生成 → 执行 → 多维度评估 → Excel报告
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.config import Config
from openai import OpenAI
import pymysql
import pandas as pd
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
1. 查询企业的8个维度：注册资本、成立时间、知识产权、诉讼、投标、纳税、高管、分支机构
2. 使用LEFT JOIN关联多个表
3. LIMIT 20

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

def execute_sql(sql: str, db_config: dict) -> pd.DataFrame:
    """执行SQL并返回DataFrame"""
    conn = pymysql.connect(**db_config)
    df = pd.read_sql(sql, conn)
    conn.close()
    return df

def evaluate_companies(df: pd.DataFrame) -> pd.DataFrame:
    """企业多维度评估"""
    # 简化评分逻辑
    df['注册资本评分'] = df.apply(lambda x: 2 if pd.notna(x.get('注册资本')) and float(str(x.get('注册资本', 0)).replace('万', '')) >= 1000 else 0, axis=1)
    df['综合评分'] = df['注册资本评分']  # 简化版
    df['评级'] = df['综合评分'].apply(lambda x: '优秀' if x >= 8 else ('良好' if x >= 5 else '一般'))
    return df

def main():
    question = "查询注册资本超过1000万的企业，统计其基本信息、知识产权和诉讼情况"
    
    print("\n" + "=" * 80)
    print("场景4：招商清单")
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
        df = execute_sql(sql, db_config)
        print(f"查询结果：{len(df)}条记录\n")
        
        # 4. 多维度评估
        print("[4/5] 多维度评估...")
        df = evaluate_companies(df)
        print(f"评估完成\n")
        
        # 5. 生成Excel
        print("[5/5] 生成Excel报告...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        excel_path = f"output/scenario_4_investment_list_{timestamp}.xlsx"
        Path(excel_path).parent.mkdir(parents=True, exist_ok=True)
        
        with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='招商清单', index=False)
        
        print(f"Excel报告：{excel_path}")
        
        print("\n" + "=" * 80)
        print("[OK] 场景4完成！")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n错误：{e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
