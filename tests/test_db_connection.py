"""
测试 1: 数据库连接测试
验证两个 MySQL 数据库的连接是否正常
"""

import pymysql
import sys

def test_database_connection():
    """测试数据库连接"""
    
    results = []
    
    # 场景 1-3 数据库
    db1_config = {
        'host': '8.134.9.77',
        'port': 3306,
        'user': 'Gaaiyun',
        'password': 'Why513338',
        'database': 'Gaaiyun'
    }
    
    # 场景 4-5 数据库
    db2_config = {
        'host': '8.134.9.77',
        'port': 3306,
        'user': 'gaaiyun_2',
        'password': 'Why513338',
        'database': 'gaaiyun_2'
    }
    
    print("=" * 60)
    print("Test 1: Database Connection Test")
    print("=" * 60)
    
    # 测试数据库 1
    print("\n[Test 1.1] Database Gaaiyun (Scenario 1-3)")
    try:
        conn = pymysql.connect(**db1_config)
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM information_schema.tables WHERE table_schema="Gaaiyun"')
        table_count = cur.fetchone()[0]
        cur.execute('SELECT table_name FROM information_schema.tables WHERE table_schema="Gaaiyun" LIMIT 10')
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
    try:
        conn = pymysql.connect(**db2_config)
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM information_schema.tables WHERE table_schema="gaaiyun_2"')
        table_count = cur.fetchone()[0]
        cur.execute('SELECT table_name FROM information_schema.tables WHERE table_schema="gaaiyun_2" LIMIT 10')
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
