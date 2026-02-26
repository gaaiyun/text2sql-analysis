"""
Vanna AI 训练脚本
用于训练 Vanna 模型理解数据库 Schema 和查询模式

使用方法:
    python scripts/train_vanna.py

前提条件:
    1. 已配置 config.json 文件
    2. 已安装 vanna 和相关依赖
"""

import json
import pymysql
from pathlib import Path
import vanna as vn

# 配置路径
CONFIG_PATH = Path(__file__).parent.parent / "config.json"
SCHEMA_PATH_1 = Path(__file__).parent.parent / "schema_gaaiyun.md"
SCHEMA_PATH_2 = Path(__file__).parent.parent / "schema_gaaiyun_2.md"


def load_config():
    """加载配置文件"""
    if not CONFIG_PATH.exists():
        print(f"[ERROR] Config file not found: {CONFIG_PATH}")
        print("Please copy config.template.json to config.json and fill in your API keys.")
        return None
    
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def connect_to_database(db_config):
    """连接到数据库"""
    try:
        conn = pymysql.connect(
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )
        print(f"[OK] Connected to {db_config['database']}")
        return conn
    except Exception as e:
        print(f"[FAIL] Connection failed: {e}")
        return None


def extract_ddl(conn, database):
    """从数据库提取 DDL"""
    ddl_statements = []
    
    try:
        cur = conn.cursor()
        cur.execute(f"""
            SELECT table_name, create_table 
            FROM information_schema.tables 
            WHERE table_schema = '{database}'
        """)
        
        for table_name, create_table in cur.fetchall():
            ddl_statements.append(f"-- Table: {table_name}\n{create_table}")
        
        cur.close()
        print(f"[OK] Extracted DDL for {len(ddl_statements)} tables")
        return ddl_statements
    except Exception as e:
        print(f"[FAIL] DDL extraction failed: {e}")
        return []


def train_vanna_with_ddl(ddl_statements, scenario_name):
    """使用 DDL 训练 Vanna"""
    print(f"\n[Training] {scenario_name}")
    print("-" * 60)
    
    for i, ddl in enumerate(ddl_statements, 1):
        try:
            status = vn.train(ddl=ddl)
            print(f"  [{i}/{len(ddl_statements)}] Trained: {status}")
        except Exception as e:
            print(f"  [{i}/{len(ddl_statements)}] Failed: {e}")


def generate_sample_questions(scenario):
    """生成示例问题"""
    questions = {
        'scenario_1_3': [
            "查询近 3 年企业融资趋势",
            "分析投资事件最多的行业",
            "统计各行业的融资轮次分布",
            "查询注册资本超过 1000 万的企业"
        ],
        'scenario_4_5': [
            "评估以下企业：[企业名称]",
            "生成 XX 企业的尽调报告",
            "查询企业的知识产权情况",
            "分析企业的法律诉讼记录"
        ]
    }
    return questions.get(scenario, [])


def train_vanna_with_questions(questions):
    """使用示例问题训练 Vanna"""
    print("\n[Training] Sample Questions")
    print("-" * 60)
    
    for i, question in enumerate(questions, 1):
        # 这里需要实际的 SQL 查询来训练
        # 由于没有实际 SQL，暂时跳过
        print(f"  [{i}/{len(questions)}] Question: {question}")
        print(f"    [INFO] Manual SQL training required")


def main():
    """主函数"""
    print("=" * 60)
    print("Vanna AI Training Script")
    print("=" * 60)
    
    # 加载配置
    config = load_config()
    if not config:
        return
    
    # 初始化 Vanna
    vanna_config = config.get('vanna', {})
    vn.api_key = vanna_config.get('api_key', '')
    vn.org = vanna_config.get('org', 'default')
    
    print(f"\n[INFO] Vanna Org: {vn.org}")
    print(f"[INFO] Vanna API Key: {'*' * 20}")
    
    # 训练场景 1-3
    print("\n" + "=" * 60)
    print("Phase 1: Training Scenario 1-3 (Gaaiyun Database)")
    print("=" * 60)
    
    db1_config = config.get('database', {}).get('scenario_1_3', {})
    conn1 = connect_to_database(db1_config)
    
    if conn1:
        ddl1 = extract_ddl(conn1, db1_config['database'])
        train_vanna_with_ddl(ddl1, "Scenario 1-3: Gaaiyun")
        conn1.close()
        
        # 训练示例问题
        questions1 = generate_sample_questions('scenario_1_3')
        train_vanna_with_questions(questions1)
    
    # 训练场景 4-5
    print("\n" + "=" * 60)
    print("Phase 2: Training Scenario 4-5 (gaaiyun_2 Database)")
    print("=" * 60)
    
    db2_config = config.get('database', {}).get('scenario_4_5', {})
    conn2 = connect_to_database(db2_config)
    
    if conn2:
        ddl2 = extract_ddl(conn2, db2_config['database'])
        train_vanna_with_ddl(ddl2, "Scenario 4-5: gaaiyun_2")
        conn2.close()
        
        # 训练示例问题
        questions2 = generate_sample_questions('scenario_4_5')
        train_vanna_with_questions(questions2)
    
    # 完成
    print("\n" + "=" * 60)
    print("Training Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Review training data in Vanna dashboard")
    print("  2. Test SQL generation: python tests/test_vanna_sql.py")
    print("  3. Start API server: python api/vanna_server.py")


if __name__ == "__main__":
    main()
