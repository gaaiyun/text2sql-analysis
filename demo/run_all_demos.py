#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
运行所有5个场景的Demo
"""

import sys
from pathlib import Path
import subprocess

def run_demo(demo_file: str, scenario_name: str):
    """运行单个demo"""
    print("\n" + "=" * 100)
    print(f"开始运行：{scenario_name}")
    print("=" * 100)
    
    try:
        result = subprocess.run(
            [sys.executable, demo_file],
            cwd=Path(__file__).parent,
            capture_output=False,
            text=True
        )
        
        if result.returncode == 0:
            print(f"\n[OK] {scenario_name} 完成")
        else:
            print(f"\n[FAIL] {scenario_name} 失败")
            
    except Exception as e:
        print(f"\n[ERROR] {scenario_name} 错误：{e}")

def main():
    print("\n" + "=" * 100)
    print("Text2SQL 系统 - 运行所有场景Demo")
    print("=" * 100)
    
    demos = [
        ("demo_scenario_1.py", "场景1：数据洞察"),
        ("demo_scenario_2.py", "场景2：地区产业分析"),
        ("demo_scenario_3.py", "场景3：行业分析"),
        ("demo_scenario_4.py", "场景4：招商清单"),
        ("demo_scenario_5.py", "场景5：企业尽调"),
    ]
    
    for demo_file, scenario_name in demos:
        run_demo(demo_file, scenario_name)
    
    print("\n" + "=" * 100)
    print("所有场景Demo运行完成！")
    print("=" * 100)
    print("\n请查看 output/ 目录下的生成文件")

if __name__ == "__main__":
    main()
