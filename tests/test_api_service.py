"""
测试 10: API 服务测试
验证 Vanna API 服务的配置和启动准备
"""

import os
import sys
from pathlib import Path

def test_api_service():
    """测试 API 服务"""
    
    print("=" * 60)
    print("Test 10: API Service Readiness")
    print("=" * 60)
    
    api_file = Path("C:\\Users\\gaaiy\\Desktop\\text2sql\\api\\vanna_server.py")
    config_template = Path("C:\\Users\\gaaiy\\Desktop\\text2sql\\config.template.json")
    
    # 测试 10.1: API 文件存在性
    print("\n[Test 10.1] Check API server file")
    if api_file.exists():
        print(f"  [OK] vanna_server.py exists")
        file_size = api_file.stat().st_size
        print(f"  File size: {file_size:,} bytes")
    else:
        print(f"  [FAIL] vanna_server.py not found")
        return False
    
    # 测试 10.2: 配置文件存在性
    print("\n[Test 10.2] Check config template")
    if config_template.exists():
        print(f"  [OK] config.template.json exists")
    else:
        print(f"  [FAIL] config.template.json not found")
        return False
    
    # 测试 10.3: 依赖检查
    print("\n[Test 10.3] Check required dependencies")
    required_packages = {
        'fastapi': 'FastAPI framework',
        'uvicorn': 'ASGI server',
        'pydantic': 'Data validation',
        'vanna': 'Text2SQL engine',
        'pymysql': 'MySQL driver'
    }
    
    missing_packages = []
    for package, desc in required_packages.items():
        try:
            __import__(package)
            print(f"  [OK] {package} ({desc})")
        except ImportError:
            missing_packages.append(package)
            print(f"  [MISSING] {package} ({desc})")
    
    if missing_packages:
        print(f"\n  Suggestion: pip install {' '.join(missing_packages)}")
    
    # 测试 10.4: API 端点检查
    print("\n[Test 10.4] Check API endpoints")
    
    with open(api_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    endpoints = {
        '@app.get("/")': 'Health check',
        '@app.post("/api/v0/generate_sql")': 'SQL generation',
        '@app.post("/api/v0/train")': 'Model training',
        '@app.get("/api/v0/schema")': 'Get schema'
    }
    
    for endpoint, desc in endpoints.items():
        if endpoint in content:
            print(f"  [OK] {endpoint} ({desc})")
        else:
            print(f"  [WARN] {endpoint} ({desc}) - May be missing")
    
    # 测试 10.5: 启动脚本检查
    print("\n[Test 10.5] Check startup script")
    if 'if __name__ == "__main__":' in content and 'uvicorn.run' in content:
        print(f"  [OK] Startup code present")
        print(f"  Command: python api/vanna_server.py")
        print(f"  Default port: 5000")
    else:
        print(f"  [WARN] Startup code may be missing")
    
    # 测试 10.6: 配置要求
    print("\n[Test 10.6] Configuration requirements")
    print("  Required config in config.json:")
    print("    - database.host")
    print("    - database.user")
    print("    - database.password")
    print("    - database.database")
    print("    - bailian.api_key")
    print("    - vanna.api_key")
    print("    - vanna.org")
    
    # 汇总
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    if missing_packages:
        print(f"  Status: [WARN] Missing packages: {', '.join(missing_packages)}")
        print(f"  Action: Install missing dependencies")
    else:
        print(f"  Status: [PASS] API service ready")
        print(f"  Next: Copy config.template.json to config.json and fill in API keys")
        print(f"  Then: python api/vanna_server.py")
    
    return len(missing_packages) == 0

if __name__ == "__main__":
    success = test_api_service()
    sys.exit(0 if success else 1)
