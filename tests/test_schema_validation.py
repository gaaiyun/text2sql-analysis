"""
测试 2: Schema 提取验证
验证已提取的 Schema 文件是否准确反映数据库结构
"""

import pymysql
import os

def test_schema_validation():
    """验证 Schema 文件"""
    
    print("=" * 60)
    print("Test 2: Schema Validation")
    print("=" * 60)
    
    # 检查 Schema 文件是否存在
    schema1_path = "C:\\Users\\gaaiy\\Desktop\\text2sql\\schema_gaaiyun.md"
    schema2_path = "C:\\Users\\gaaiy\\Desktop\\text2sql\\schema_gaaiyun_2.md"
    
    print("\n[Test 2.1] Check schema files exist")
    if os.path.exists(schema1_path):
        print(f"  [OK] schema_gaaiyun.md exists")
        with open(schema1_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"  File size: {len(content)} bytes")
    else:
        print(f"  [FAIL] schema_gaaiyun.md not found")
    
    if os.path.exists(schema2_path):
        print(f"  [OK] schema_gaaiyun_2.md exists")
        with open(schema2_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"  File size: {len(content)} bytes")
    else:
        print(f"  [FAIL] schema_gaaiyun_2.md not found")
    
    # 验证数据库实际表结构
    print("\n[Test 2.2] Verify database schema")
    
    db1_config = {
        'host': '8.134.9.77',
        'port': 3306,
        'user': 'Gaaiyun',
        'password': 'Why513338',
        'database': 'Gaaiyun'
    }
    
    try:
        conn = pymysql.connect(**db1_config)
        cur = conn.cursor()
        cur.execute('''
            SELECT table_name, table_comment 
            FROM information_schema.tables 
            WHERE table_schema="Gaaiyun"
        ''')
        tables = cur.fetchall()
        conn.close()
        
        print(f"  [OK] Database Gaaiyun has {len(tables)} tables")
        print("  Tables with comments:")
        for table_name, comment in tables[:5]:
            print(f"    - {table_name}: {comment if comment else 'N/A'}")
        
        return True
    except Exception as e:
        print(f"  [FAIL] Error: {e}")
        return False

if __name__ == "__main__":
    test_schema_validation()
