"""
Text2SQL 5 场景综合测试套件

测试 5 大场景的 SQL 生成和執行能力：
1. 数据洞察
2. 地区产业分析
3. 行业分析
4. 招商清单
5. 企业尽调

使用方法:
    python tests/test_5_scenarios.py

注意：需要配置环境变量（.env 文件）
- KIRO_API_KEY: Kiro API 密钥
- DB_HOST, DB_NAME, DB_USER, DB_PASSWORD: 数据库配置
"""

import unittest
import sys
import os
from pathlib import Path
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.config import get_kiro_config, get_database_config
from openai import OpenAI
import pymysql


# =============================================================================
# 测试配置
# =============================================================================

class TestConfig:
    """测试配置类"""
    KIRO_CONFIG = get_kiro_config()
    DB_CONFIG = {
        'scenario_1_3': get_database_config('scenario_1_3'),
        'scenario_4_5': get_database_config('scenario_4_5')
    }

    # 5 大场景测试问题
    SCENARIOS = [
        {
            "id": 1,
            "name": "数据洞察",
            "question": "查询近 3 年企业融资趋势，按年份和融资轮次统计",
            "database": "scenario_1_3",
        },
        {
            "id": 2,
            "name": "地区产业分析",
            "question": "分析北京市人工智能产业发展情况，包括企业数量、注册资本、融资情况",
            "database": "scenario_1_3",
        },
        {
            "id": 3,
            "name": "行业分析",
            "question": "分析新能源汽车行业发展趋势，包括企业数量增长、融资轮次分布",
            "database": "scenario_1_3",
        },
        {
            "id": 4,
            "name": "招商清单",
            "question": "查询注册资本超过 1000 万的企业，包括企业名称、注册资本、成立时间",
            "database": "scenario_4_5",
        },
        {
            "id": 5,
            "name": "企业尽调",
            "question": "查询企业的知识产权情况，包括专利、商标、软件著作权数量",
            "database": "scenario_4_5",
        }
    ]


# =============================================================================
# 工具函数
# =============================================================================

def get_schema(db_config):
    """获取数据库 Schema"""
    try:
        conn = pymysql.connect(**db_config)
        cur = conn.cursor()

        cur.execute("""
            SELECT table_name, table_comment
            FROM information_schema.tables
            WHERE table_schema = %s
        """, (db_config["database"],))

        tables = cur.fetchall()
        schema = []

        for table_name, comment in tables[:10]:  # 只取前 10 张表
            cur.execute(f"SHOW CREATE TABLE `{table_name}`")
            create_sql = cur.fetchone()[1]
            schema.append(f"-- {comment or table_name}\n{create_sql}")

        conn.close()
        return "\n\n".join(schema)
    except Exception as e:
        return f"ERROR: {e}"


def generate_sql(client, question, schema):
    """使用 LLM 生成 SQL"""
    prompt = f"""你是 SQL 专家。基于以下数据库表结构，为问题生成 MySQL 查询语句。

表结构：
{schema[:5000]}  # 限制长度

问题：{question}

要求：
1. 只返回 SQL 语句，不要解释
2. SQL 必须是有效的 MySQL 语法
3. 使用合适的 JOIN 和聚合函数
4. 添加必要的 WHERE 条件

SQL:"""

    response = client.chat.completions.create(
        model=TestConfig.KIRO_CONFIG["model"],
        messages=[
            {"role": "system", "content": "你是 SQL 专家，擅长生成准确的 MySQL 查询语句。"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.3
    )

    sql = response.choices[0].message.content.strip()

    # 清理 Markdown 代码块
    for prefix in ["```sql", "```"]:
        if sql.startswith(prefix):
            sql = sql[len(prefix):]
    if sql.endswith("```"):
        sql = sql[:-3]

    return sql.strip()


def execute_sql(sql, db_config):
    """执行 SQL 并返回结果"""
    try:
        conn = pymysql.connect(**db_config)
        cur = conn.cursor()
        cur.execute(sql)
        results = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        conn.close()
        return {
            "success": True,
            "row_count": len(results),
            "columns": columns,
            "data": results[:5]  # 只返回前 5 行
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# =============================================================================
# 测试用例
# =============================================================================

class TestScenario1DataInsight(unittest.TestCase):
    """场景 1: 数据洞察测试"""

    @classmethod
    def setUpClass(cls):
        cls.client = OpenAI(
            base_url=TestConfig.KIRO_CONFIG["base_url"],
            api_key=TestConfig.KIRO_CONFIG["api_key"]
        )
        cls.db_config = TestConfig.DB_CONFIG["scenario_1_3"]
        cls.schema = get_schema(cls.db_config)

    def test_financing_trend_query(self):
        """测试融资趋势查询"""
        question = "查询近 3 年企业融资趋势，按年份和融资轮次统计"
        sql = generate_sql(self.client, question, self.schema)
        self.assertIsNotNone(sql)
        self.assertIn("SELECT", sql.upper())

        result = execute_sql(sql, self.db_config)
        self.assertTrue(result["success"], f"SQL 执行失败：{result.get('error')}")
        self.assertGreater(result["row_count"], 0, "查询结果应为空")


class TestScenario2RegionalAnalysis(unittest.TestCase):
    """场景 2: 地区产业分析测试"""

    @classmethod
    def setUpClass(cls):
        cls.client = OpenAI(
            base_url=TestConfig.KIRO_CONFIG["base_url"],
            api_key=TestConfig.KIRO_CONFIG["api_key"]
        )
        cls.db_config = TestConfig.DB_CONFIG["scenario_1_3"]
        cls.schema = get_schema(cls.db_config)

    def test_regional_industry_query(self):
        """测试地区产业查询"""
        question = "分析北京市人工智能产业发展情况，包括企业数量、注册资本"
        sql = generate_sql(self.client, question, self.schema)
        self.assertIsNotNone(sql)
        self.assertIn("SELECT", sql.upper())

        result = execute_sql(sql, self.db_config)
        self.assertTrue(result["success"], f"SQL 执行失败：{result.get('error')}")


class TestScenario3IndustryAnalysis(unittest.TestCase):
    """场景 3: 行业分析测试"""

    @classmethod
    def setUpClass(cls):
        cls.client = OpenAI(
            base_url=TestConfig.KIRO_CONFIG["base_url"],
            api_key=TestConfig.KIRO_CONFIG["api_key"]
        )
        cls.db_config = TestConfig.DB_CONFIG["scenario_1_3"]
        cls.schema = get_schema(cls.db_config)

    def test_industry_trend_query(self):
        """测试行业趋势查询"""
        question = "分析新能源汽车行业发展趋势，包括企业数量增长、融资轮次分布"
        sql = generate_sql(self.client, question, self.schema)
        self.assertIsNotNone(sql)
        self.assertIn("SELECT", sql.upper())

        result = execute_sql(sql, self.db_config)
        self.assertTrue(result["success"], f"SQL 执行失败：{result.get('error')}")


class TestScenario4InvestmentList(unittest.TestCase):
    """场景 4: 招商清单测试"""

    @classmethod
    def setUpClass(cls):
        cls.client = OpenAI(
            base_url=TestConfig.KIRO_CONFIG["base_url"],
            api_key=TestConfig.KIRO_CONFIG["api_key"]
        )
        cls.db_config = TestConfig.DB_CONFIG["scenario_4_5"]
        cls.schema = get_schema(cls.db_config)

    def test_investment_list_query(self):
        """测试招商清单查询"""
        question = "查询注册资本超过 1000 万的企业，包括企业名称、注册资本、成立时间"
        sql = generate_sql(self.client, question, self.schema)
        self.assertIsNotNone(sql)
        self.assertIn("SELECT", sql.upper())

        result = execute_sql(sql, self.db_config)
        self.assertTrue(result["success"], f"SQL 执行失败：{result.get('error')}")
        self.assertGreater(result["row_count"], 0, "查询结果应为空")


class TestScenario5DueDiligence(unittest.TestCase):
    """场景 5: 企业尽调测试"""

    @classmethod
    def setUpClass(cls):
        cls.client = OpenAI(
            base_url=TestConfig.KIRO_CONFIG["base_url"],
            api_key=TestConfig.KIRO_CONFIG["api_key"]
        )
        cls.db_config = TestConfig.DB_CONFIG["scenario_4_5"]
        cls.schema = get_schema(cls.db_config)

    def test_due_diligence_query(self):
        """测试企业尽调查询"""
        question = "查询企业的知识产权情况，包括专利、商标、软件著作权数量"
        sql = generate_sql(self.client, question, self.schema)
        self.assertIsNotNone(sql)
        self.assertIn("SELECT", sql.upper())

        result = execute_sql(sql, self.db_config)
        self.assertTrue(result["success"], f"SQL 执行失败：{result.get('error')}")


class TestDatabaseConnection(unittest.TestCase):
    """数据库连接测试"""

    def test_scenario_1_3_connection(self):
        """测试场景 1-3 数据库连接"""
        db_config = TestConfig.DB_CONFIG["scenario_1_3"]
        try:
            conn = pymysql.connect(**db_config)
            conn.close()
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"数据库连接失败：{e}")

    def test_scenario_4_5_connection(self):
        """测试场景 4-5 数据库连接"""
        db_config = TestConfig.DB_CONFIG["scenario_4_5"]
        try:
            conn = pymysql.connect(**db_config)
            conn.close()
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"数据库连接失败：{e}")


# =============================================================================
# 测试运行器
# =============================================================================

def run_tests():
    """运行所有测试"""
    print("=" * 80)
    print("Text2SQL 5 场景综合测试")
    print("=" * 80)
    print(f"测试时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"使用模型：{TestConfig.KIRO_CONFIG['model']}")
    print(f"API: {TestConfig.KIRO_CONFIG['base_url']}")
    print()

    # 检查配置
    if not TestConfig.KIRO_CONFIG.get('api_key') or TestConfig.KIRO_CONFIG['api_key'].startswith('kp-your'):
        print("[WARN] KIRO_API_KEY 未配置或使用默认值，测试可能失败")
    print()

    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # 添加测试
    suite.addTests(loader.loadTestsFromTestCase(TestDatabaseConnection))
    suite.addTests(loader.loadTestsFromTestCase(TestScenario1DataInsight))
    suite.addTests(loader.loadTestsFromTestCase(TestScenario2RegionalAnalysis))
    suite.addTests(loader.loadTestsFromTestCase(TestScenario3IndustryAnalysis))
    suite.addTests(loader.loadTestsFromTestCase(TestScenario4InvestmentList))
    suite.addTests(loader.loadTestsFromTestCase(TestScenario5DueDiligence))

    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # 汇总报告
    print()
    print("=" * 80)
    print("测试汇总报告")
    print("=" * 80)
    print(f"总测试数：{result.testsRun}")
    print(f"成功：{result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败：{len(result.failures)}")
    print(f"错误：{len(result.errors)}")
    print(f"成功率：{(result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100:.1f}%")

    if result.failures:
        print("\n失败测试:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback[:200]}")

    if result.errors:
        print("\n错误测试:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback[:200]}")

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
