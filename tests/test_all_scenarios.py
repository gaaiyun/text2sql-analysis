"""
Text2SQL 完整场景测试
测试 5 大场景的 SQL 生成能力

使用模型：Kiro Claude Opus 4.6

注意：API Key 和数据库配置从环境变量或 config.json 加载
"""

from openai import OpenAI
import pymysql
import json
from datetime import datetime
from pathlib import Path
import sys

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.config import get_kiro_config, get_database_config

# ============ 配置（从环境变量加载） ============
KIRO_CONFIG = get_kiro_config()

DB_CONFIG = {
    "scenario_1_3": get_database_config('scenario_1_3'),
    "scenario_4_5": get_database_config('scenario_4_5')
}

# ============ 5 大场景测试问题 ============
TEST_SCENARIOS = [
    {
        "id": 1,
        "name": "数据洞察",
        "question": "查询近 3 年企业融资趋势，按年份和融资轮次统计",
        "database": "scenario_1_3",
        "expected_tables": ["投资事件", "融资信息"]
    },
    {
        "id": 2,
        "name": "地区产业分析",
        "question": "分析北京市人工智能产业发展情况，包括企业数量、注册资本、融资情况",
        "database": "scenario_1_3",
        "expected_tables": ["企业基本信息", "企业行业分类"]
    },
    {
        "id": 3,
        "name": "行业分析",
        "question": "分析新能源汽车行业发展趋势，包括企业数量增长、融资轮次分布",
        "database": "scenario_1_3",
        "expected_tables": ["企业行业分类", "投资事件"]
    },
    {
        "id": 4,
        "name": "招商清单",
        "question": "查询注册资本超过 1000 万的企业，包括企业名称、注册资本、成立时间、所属行业",
        "database": "scenario_4_5",
        "expected_tables": ["企业信息"]
    },
    {
        "id": 5,
        "name": "企业尽调",
        "question": "查询企业的知识产权情况，包括专利数量、商标数量、软件著作权",
        "database": "scenario_4_5",
        "expected_tables": ["知识产权"]
    }
]

# ============ 工具函数 ============
def get_schema(db_config):
    """获取数据库 Schema"""
    conn = pymysql.connect(**db_config)
    cur = conn.cursor()

    cur.execute("""
        SELECT table_name, table_comment
        FROM information_schema.tables
        WHERE table_schema = %s
    """, (db_config["database"],))

    tables = cur.fetchall()

    schema = []
    for table_name, comment in tables:
        cur.execute(f"SHOW CREATE TABLE `{table_name}`")
        create_sql = cur.fetchone()[1]
        schema.append(f"-- {comment or table_name}\n{create_sql}")
        if len(schema) >= 10:  # 只取前 10 张表
            break

    conn.close()
    return "\n\n".join(schema)

def generate_sql(client, question, schema):
    """使用 LLM 生成 SQL"""
    prompt = f"""你是 SQL 专家。基于以下数据库表结构，为问题生成 MySQL 查询语句。

表结构：
{schema}

问题：{question}

要求：
1. 只返回 SQL 语句，不要解释
2. SQL 必须是有效的 MySQL 语法
3. 使用合适的 JOIN 和聚合函数
4. 添加必要的 WHERE 条件
5. **只生成单个 SELECT 语句**，禁止多个 SELECT
6. **JOIN 时必须使用 COLLATE**: `ON b.eid = ic.eid COLLATE utf8mb4_unicode_ci`

SQL:"""

    response = client.chat.completions.create(
        model=KIRO_CONFIG["model"],
        messages=[
            {"role": "system", "content": "你是 SQL 专家，擅长生成准确的 MySQL 查询语句。"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.3
    )

    sql = response.choices[0].message.content.strip()

    # 清理 Markdown 代码块
    if sql.startswith("```sql"):
        sql = sql[6:]
    if sql.startswith("```"):
        sql = sql[3:]
    if sql.endswith("```"):
        sql = sql[:-3]

    return sql.strip()

def test_sql(sql, db_config):
    """测试 SQL 执行"""
    try:
        conn = pymysql.connect(**db_config)
        cur = conn.cursor()

        cur.execute(sql)
        results = cur.fetchall()

        # 获取列名
        columns = [desc[0] for desc in cur.description]

        conn.close()

        return {
            "success": True,
            "row_count": len(results),
            "columns": columns,
            "sample": results[:3] if results else []
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# ============ 主测试流程 ============
def main():
    """主测试流程"""
    print("=" * 80)
    print("Text2SQL 完整场景测试")
    print("=" * 80)
    print(f"使用模型：{KIRO_CONFIG['model']}")
    print(f"数据库：2 个 ({DB_CONFIG['scenario_1_3']['database']} + {DB_CONFIG['scenario_4_5']['database']})")
    print(f"测试场景：5 个")
    print()

    # 验证配置
    if not KIRO_CONFIG.get('api_key'):
        print("[ERROR] KIRO_API_KEY 未设置，请在 .env 文件中配置")
        sys.exit(1)

    # 初始化 OpenAI 客户端
    client = OpenAI(
        base_url=KIRO_CONFIG["base_url"],
        api_key=KIRO_CONFIG["api_key"]
    )

    results = []

    for scenario in TEST_SCENARIOS:
        print(f"\n{'='*80}")
        print(f"场景 {scenario['id']}: {scenario['name']}")
        print(f"{'='*80}")
        print(f"问题：{scenario['question']}")
        print()

        # 1. 获取 Schema
        print("[1/3] 获取数据库 Schema...")
        db_config = DB_CONFIG[scenario["database"]]
        schema = get_schema(db_config)
        print(f"[OK] 获取到 {len(schema.split(chr(10)))} 行 Schema")

        # 2. 生成 SQL
        print()
        print("[2/3] 生成 SQL...")
        try:
            sql = generate_sql(client, scenario["question"], schema)
            print(f"[OK] SQL 生成成功")
            print(f"SQL: {sql[:200]}...")
        except Exception as e:
            print(f"[ERROR] SQL 生成失败：{e}")
            results.append({
                "scenario": scenario["name"],
                "success": False,
                "error": str(e),
                "sql": None
            })
            continue

        # 3. 测试 SQL 执行
        print()
        print("[3/3] 测试 SQL 执行...")
        test_result = test_sql(sql, db_config)

        if test_result["success"]:
            print(f"[OK] SQL 执行成功")
            print(f"  返回行数：{test_result['row_count']}")
            print(f"  列：{', '.join(test_result['columns'][:5])}...")
            if test_result["sample"]:
                print(f"  示例：{test_result['sample'][0]}")
        else:
            print(f"[ERROR] SQL 执行失败：{test_result['error']}")

        results.append({
            "scenario": scenario["name"],
            "success": test_result["success"],
            "sql": sql,
            "row_count": test_result.get("row_count", 0),
            "error": test_result.get("error")
        })

        print()

    # ============ 汇总报告 ============
    print("\n" + "=" * 80)
    print("测试汇总报告")
    print("=" * 80)
    print()

    success_count = sum(1 for r in results if r["success"])
    total_count = len(results)

    print(f"总场景数：{total_count}")
    print(f"成功：{success_count}")
    print(f"失败：{total_count - success_count}")
    print(f"成功率：{success_count/total_count*100:.1f}%")
    print()

    print("详细结果:")
    for r in results:
        status = "[OK]" if r["success"] else "[FAIL]"
        print(f"  {status} {r['scenario']}: {'成功' if r['success'] else '失败'} - {r.get('row_count', 0)} 行")
        if r.get("error"):
            print(f"     错误：{r['error'][:100]}")

    # 保存结果
    report = {
        "timestamp": datetime.now().isoformat(),
        "model": KIRO_CONFIG["model"],
        "total": total_count,
        "success": success_count,
        "failed": total_count - success_count,
        "success_rate": f"{success_count/total_count*100:.1f}%",
        "results": results
    }

    with open("test_results.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print()
    print(f"[OK] 测试结果已保存到：test_results.json")
    print()
    print("=" * 80)
    print("测试完成！")
    print("=" * 80)

if __name__ == "__main__":
    main()
