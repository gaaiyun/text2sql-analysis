#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
场景1：数据洞察 - 完整流水线Demo
自然语言输入 → SQL生成 → 执行 → 图表 → 网络搜索 → PDF/Word报告
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from text2sql_utils import Text2SQLPipeline

def main():
    # 自然语言输入
    question = "分析2023-2024年融资趋势，按行业统计融资金额和融资数量"
    
    print("\n" + "=" * 80)
    print("场景1：数据洞察")
    print("=" * 80)
    
    try:
        # 创建流水线
        pipeline = Text2SQLPipeline('scenario_1_3')
        
        # 运行完整流水线
        results = pipeline.run(question, output_prefix="scenario_1_data_insight")
        
        print(f"\n生成的文件：")
        for key, path in results.items():
            print(f"  {key}: {path}")
            
    except Exception as e:
        print(f"\n错误：{e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
