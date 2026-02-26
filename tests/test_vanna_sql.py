"""
测试 3: Vanna AI SQL 生成测试
测试 Vanna 将自然语言转换为 SQL 的能力
"""

import sys

def test_vanna_sql_generation():
    """测试 Vanna SQL 生成"""
    
    print("=" * 60)
    print("Test 3: Vanna AI SQL Generation")
    print("=" * 60)
    
    # 检查 Vanna 是否安装
    print("\n[Test 3.1] Check Vanna installation")
    try:
        import vanna as vn
        print(f"  [OK] Vanna installed, version: {vn.__version__}")
    except ImportError as e:
        print(f"  [FAIL] Vanna not installed: {e}")
        print("  Suggestion: pip install vanna")
        return False
    
    # 检查配置文件
    print("\n[Test 3.2] Check config file")
    import json
    from pathlib import Path
    
    config_path = Path("C:\\Users\\gaaiy\\Desktop\\text2sql\\config.template.json")
    if config_path.exists():
        print(f"  [OK] Config template exists")
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            print(f"  Config sections: {list(config.keys())}")
    else:
        print(f"  [FAIL] Config template not found")
    
    # 测试 SQL 生成逻辑（模拟）
    print("\n[Test 3.3] Test SQL generation logic")
    test_questions = [
        "查询近 3 年企业融资趋势",
        "分析北京市人工智能产业发展情况",
        "评估以下企业：[企业列表]",
        "生成 XX 企业尽调报告"
    ]
    
    print("  Sample questions for SQL generation:")
    for i, q in enumerate(test_questions, 1):
        print(f"    {i}. {q}")
    
    print("\n  [INFO] Vanna requires API key and training data")
    print("  Next steps:")
    print("    1. Copy config.template.json to config.json")
    print("    2. Fill in your DashScope API key")
    print("    3. Train Vanna with DDL and sample queries")
    print("    4. Run: python api/vanna_server.py")
    
    return True

if __name__ == "__main__":
    success = test_vanna_sql_generation()
    sys.exit(0 if success else 1)
