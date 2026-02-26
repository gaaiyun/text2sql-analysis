"""
测试 5-7: 提示词模板验证
验证 5 个场景的提示词模板文件完整性和质量
"""

import os
from pathlib import Path

def test_prompt_templates():
    """测试提示词模板"""
    
    print("=" * 60)
    print("Test 5-7: Prompt Template Validation")
    print("=" * 60)
    
    prompts_dir = Path("C:\\Users\\gaaiy\\Desktop\\text2sql\\prompts")
    
    scenarios = {
        'scenario_1_data_insight.md': '场景 1: 数据洞察',
        'scenario_2_regional_industry.md': '场景 2: 地区产业分析',
        'scenario_3_industry_analysis.md': '场景 3: 特定行业分析',
        'scenario_4_investment_list.md': '场景 4: 招商清单',
        'scenario_5_due_diligence.md': '场景 5: 企业尽调报告'
    }
    
    results = []
    
    # 测试每个提示词文件
    for filename, scenario_name in scenarios.items():
        print(f"\n[Test] {scenario_name}")
        print("-" * 60)
        
        file_path = prompts_dir / filename
        
        # 测试 1: 文件存在性
        if not file_path.exists():
            print(f"  [FAIL] File not found: {filename}")
            results.append((scenario_name, 'FAIL', 'File not found'))
            continue
        
        print(f"  [OK] File exists")
        
        # 测试 2: 文件大小
        file_size = file_path.stat().st_size
        print(f"  File size: {file_size:,} bytes")
        
        if file_size < 500:
            print(f"  [WARN] File too small, may be incomplete")
        
        # 测试 3: 内容检查
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查必需章节
        required_sections = {
            '角色定位': 'Role definition',
            '核心任务': 'Core task',
            '分析维度': 'Analysis dimensions',
            'SQL 查询规则': 'SQL query rules',
            '输出格式': 'Output format',
            '风险控制': 'Risk control'
        }
        
        print(f"  Required sections:")
        missing_sections = []
        for section, desc in required_sections.items():
            if section in content:
                print(f"    [OK] {section} ({desc})")
            else:
                missing_sections.append(section)
                print(f"    [MISSING] {section} ({desc})")
        
        # 测试 4: 特殊场景检查
        if 'scenario_4' in filename:
            # 场景 4 需要评估维度和 Excel 输出
            if '评估维度' in content or '评估' in content:
                print(f"  [OK] Evaluation dimensions present")
            else:
                print(f"  [WARN] Evaluation dimensions may be missing")
            
            if 'Excel' in content or 'excel' in content:
                print(f"  [OK] Excel output format specified")
            else:
                print(f"  [WARN] Excel output format may be missing")
        
        if 'scenario_5' in filename:
            # 场景 5 需要尽调维度和 Word 输出
            if '尽调' in content or '尽职调查' in content:
                print(f"  [OK] Due diligence dimensions present")
            
            if 'Word' in content or 'word' in content or 'Markdown' in content:
                print(f"  [OK] Output format specified")
        
        # 汇总
        if missing_sections:
            status = 'WARN'
            detail = f'Missing: {", ".join(missing_sections)}'
        else:
            status = 'PASS'
            detail = 'All sections present'
        
        results.append((scenario_name, status, detail))
        print(f"  Status: [{status}] {detail}")
    
    # 总体汇总
    print("\n" + "=" * 60)
    print("Overall Summary")
    print("=" * 60)
    
    pass_count = sum(1 for r in results if r[1] == 'PASS')
    warn_count = sum(1 for r in results if r[1] == 'WARN')
    fail_count = sum(1 for r in results if r[1] == 'FAIL')
    
    print(f"  Total templates: {len(results)}")
    print(f"  PASS: {pass_count}")
    print(f"  WARN: {warn_count}")
    print(f"  FAIL: {fail_count}")
    
    if fail_count == 0:
        print(f"  Overall: [PASS] All templates valid")
        return True
    else:
        print(f"  Overall: [FAIL] {fail_count} templates missing")
        return False

if __name__ == "__main__":
    success = test_prompt_templates()
    exit(0 if success else 1)
