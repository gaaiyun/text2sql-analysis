#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简单数据库连接测试
使用 Config 类加载环境变量配置
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import pymysql
from src.utils.config import Config

def test_connection(db_name, config_dict):
    """测试数据库连接"""
    print(f"\n[测试] {db_name}")
    print(f"  Host: {config_dict['host']}")
    print(f"  Port: {config_dict['port']}")
    print(f"  User: {config_dict['user']}")
    print(f"  Database: {config_dict['database']}")
    
    try:
        conn = pymysql.connect(
            host=config_dict['host'],
            port=config_dict['port'],
            user=config_dict['user'],
            password=config_dict['password'],
            database=config_dict['database'],
            connect_timeout=10
        )
        
        cur = conn.cursor()
        
        # 测试查询
        cur.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %s", (config_dict['database'],))
        table_count = cur.fetchone()[0]
        
        cur.close()
        conn.close()
        
        print(f"  [OK] 连接成功！")
        print(f"  [INFO] 表数量: {table_count}")
        return True
        
    except Exception as e:
        print(f"  [ERROR] 连接失败: {e}")
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("数据库连接测试")
    print("=" * 60)
    
    # 加载配置
    try:
        config = Config.load()
    except Exception as e:
        print(f"[ERROR] 加载配置失败: {e}")
        return
    
    # 测试场景 1-3
    db1 = config.get_database_config('scenario_1_3')
    success1 = test_connection("场景 1-3 (Gaaiyun)", db1)
    
    # 测试场景 4-5
    db2 = config.get_database_config('scenario_4_5')
    success2 = test_connection("场景 4-5 (gaaiyun_2)", db2)
    
    # 总结
    print("\n" + "=" * 60)
    print("测试结果")
    print("=" * 60)
    print(f"场景 1-3: {'[OK]' if success1 else '[FAIL]'}")
    print(f"场景 4-5: {'[OK]' if success2 else '[FAIL]'}")
    print("=" * 60)
    
    if success1 and success2:
        print("[OK] 所有数据库连接正常！")
    else:
        print("[WARN] 部分数据库连接失败，请检查配置")


if __name__ == "__main__":
    main()
