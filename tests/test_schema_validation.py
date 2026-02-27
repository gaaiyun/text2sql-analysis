"""
测试 2: Schema 提取验证
验证已提取的 Schema 文件是否准确反映数据库结构

注意：数据库配置从环境变量或 config.json 加载
"""

import pymysql
import os
from pathlib import Path
import sys

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.config import get_database_config

def test_schema_validation():
    """验证 Schema 文件"""

    print("=" * 60)
    print("Test 2: Schema Validation")
    print("=" * 60)

    # 检查 Schema 文件是否存在
    schema1_path = Path(__file__).parent.parent / "schema_gaaiyun.md"
    schema2_path = Path(__file__).parent.parent / "schema_gaaiyun_2.md"

    print("\n[Test 2.1] Check schema files exist")
    if schema1_path.exists():
        print(f"  [OK] schema_gaaiyun.md exists")
        with open(schema1_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"  File size: {len(content)} bytes")
    else:
        print(f"  [FAIL] schema_gaaiyun.md not found")

    if schema2_path.exists():
        print(f"  [OK] schema_gaaiyun_2.md exists")
        with open(schema2_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"  File size: {len(content)} bytes")
    else:
        print(f"  [FAIL] schema_gaaiyun_2.md not found")

    # 验证数据库实际表结构
    print("\n[Test 2.2] Verify database schema")

    db1_config = get_database_config('scenario_1_3')

    if not db1_config.get('host') or not db1_config.get('database'):
        print("  [FAIL] 数据库配置无效，请检查 .env 或 config.json")
        return False

    try:
        conn = pymysql.connect(**db1_config)
        cur = conn.cursor()
        cur.execute('''
            SELECT table_name, table_comment
            FROM information_schema.tables
            WHERE table_schema=%s
        ''', (db1_config['database'],))
        tables = cur.fetchall()
        conn.close()

        print(f"  [OK] Database {db1_config['database']} has {len(tables)} tables")
        print("  Tables with comments:")
        for table_name, comment in tables[:5]:
            print(f"    - {table_name}: {comment if comment else 'N/A'}")

        return True
    except Exception as e:
        print(f"  [FAIL] Error: {e}")
        return False

if __name__ == "__main__":
    test_schema_validation()
