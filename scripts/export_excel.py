"""
Excel 导出工具 - 场景 4 招商清单

使用方法:
    python export_excel.py data.json output.xlsx
"""

import pandas as pd
import json
import sys
from datetime import datetime

def export_to_excel(data, filename, sheet_name="招商清单"):
    """
    导出数据到 Excel
    
    参数:
        data: list of dict 或 DataFrame
        filename: 输出文件名
        sheet_name: 工作表名称
    
    返回:
        生成的文件路径列表
    """
    if isinstance(data, str):
        data = json.loads(data)
    
    df = pd.DataFrame(data)
    
    # 限制行数（超过 15 行分多个文件）
    if len(df) > 15:
        files = []
        chunks = [df[i:i+15] for i in range(0, len(df), 15)]
        
        for idx, chunk in enumerate(chunks, 1):
            part_filename = filename.replace('.xlsx', f'_part{idx}.xlsx')
            chunk.to_excel(part_filename, sheet_name=f'{sheet_name}_{idx}', index=False)
            files.append(part_filename)
            print(f"✅ 生成文件: {part_filename} ({len(chunk)} 行)")
        
        return files
    else:
        df.to_excel(filename, sheet_name=sheet_name, index=False)
        print(f"✅ 生成文件: {filename} ({len(df)} 行)")
        return [filename]

def create_investment_list(data):
    """
    创建招商清单 Excel（场景 4）
    
    评估维度:
    - 企业名称
    - 注册资本
    - 成立时间
    - 所属行业
    - 专利数量
    - 诉讼情况
    - 综合评分
    """
    df = pd.DataFrame(data)
    
    # 计算综合评分
    def calculate_score(row):
        score = 0
        # 注册资本评分 (≥1000万得 20 分)
        if row.get('注册资本', 0) >= 10000000:
            score += 20
        # 专利评分 (每项 5 分，最高 20 分)
        score += min(row.get('专利数量', 0) * 5, 20)
        # 存续时间评分 (≥5年得 10 分)
        if row.get('成立年限', 0) >= 5:
            score += 10
        # 无诉讼加分
        if row.get('诉讼数量', 0) == 0:
            score += 10
        return score
    
    df['综合评分'] = df.apply(calculate_score, axis=1)
    
    # 按评分排序
    df = df.sort_values('综合评分', ascending=False)
    
    return df

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python export_excel.py data.json output.xlsx")
        sys.exit(1)
    
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    files = export_to_excel(data, sys.argv[2])
    print(f"\n📊 共生成 {len(files)} 个文件")
