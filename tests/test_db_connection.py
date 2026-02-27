"""
测试 1: 数据库连接测试
验证两个 MySQL 数据库的连接是否正常

注意：数据库配置从环境变量或 config.json 加载
"""

import pymysql
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.config import get_database_config

def test_database_connection():
    """测试数据库连接"""

    results = []

    # 从配置加载数据库配置
    db1_config = get_database_config('scenario_1_3')
    db2_config = get_database_config('scenario_4_5')

    print("=" * 60)
    print("Test 1: Database Connection Test")
    print("=" * 60)

    # 测试数据库 1
    print("\n[Test 1.1] Database Gaaiyun (Scenario 1-3)")
    print(f"  Host: {db1_config.get('host', 'N/A')}")
    print(f"  Database: {db1_config.get('database', 'N/A')}")
    try:
        conn = pymysql.connect(**db1_config)
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM information_schema.tables WHERE table_schema=%s', (db1_config['database'],))
        table_count = cur.fetchone()[0]
        cur.execute('SELECT table_name FROM information_schema.tables WHERE table_schema=%s LIMIT 10', (db1_config['database'],))
        tables = [row[0] for row in cur.fetchall()]
        conn.close()
        print(f"  Status: [OK] Connected")
        print(f"  Table count: {table_count}")
        print(f"  Sample tables: {', '.join(tables)}")
        results.append(('Database Gaaiyun', 'PASS', f'{table_count} tables'))
    except Exception as e:
        print(f"  Status: [FAIL] Connection failed")
        print(f"  Error: {e}")
        results.append(('Database Gaaiyun', 'FAIL', str(e)))

    # 测试数据库 2
    print("\n[Test 1.2] Database gaaiyun_2 (Scenario 4-5)")
    print(f"  Host: {db2_config.get('host', 'N/A')}")
    print(f"  Database: {db2_config.get('database', 'N/A')}")
    try:
        conn = pymysql.connect(**db2_config)
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM information_schema.tables WHERE table_schema=%s', (db2_config['database'],))
        table_count = cur.fetchone()[0]
        cur.execute('SELECT table_name FROM information_schema.tables WHERE table_schema=%s LIMIT 10', (db2_config['database'],))
        tables = [row[0] for row in cur.fetchall()]
        conn.close()
        print(f"  Status: [OK] Connected")
        print(f"  Table count: {table_count}")
        print(f"  Sample tables: {', '.join(tables)}")
        results.append(('Database gaaiyun_2', 'PASS', f'{table_count} tables'))
    except Exception as e:
        print(f"  Status: [FAIL] Connection failed")
        print(f"  Error: {e}")
        results.append(('Database gaaiyun_2', 'FAIL', str(e)))

    # 汇总
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    for name, status, detail in results:
        icon = "[OK]" if status == 'PASS' else "[FAIL]"
        print(f"  {icon} {name}: {status} - {detail}")

    return all(r[1] == 'PASS' for r in results)

if __name__ == "__main__":
    success = test_database_connection()
    sys.exit(0 if success else 1)
