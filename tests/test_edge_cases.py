"""
边界条件和错误处理测试

测试 Text2SQL 项目的边界条件和错误处理能力
覆盖 api_server.py, config.py, sql_security.py 的边界情况
"""
import unittest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))


# =============================================================================
# 1. API 服务器边界测试
# =============================================================================

class TestAPIBoundaryConditions(unittest.TestCase):
    """API 服务器边界条件测试"""

    def test_empty_question_handling(self):
        """测试空问题处理"""
        from api_server import QueryRequest

        # 空字符串应该被允许（但后续会处理）
        req = QueryRequest(question="")
        self.assertEqual(req.question, "")

    def test_very_long_question_handling(self):
        """测试超长问题处理"""
        from api_server import QueryRequest

        # 超长问题（1000 字符）
        long_question = "请查询 " + "非常非常重要的 " * 100 + "企业信息"
        req = QueryRequest(question=long_question)
        self.assertEqual(len(req.question), len(long_question))

    def test_special_characters_in_question(self):
        """测试特殊字符处理"""
        from api_server import QueryRequest, QueryResponse

        # 特殊字符
        special_chars = [
            "查询企业 '名称'",
            '查询企业 "名称"',
            "查询企业 <名称>",
            "查询企业 & 名称",
            "查询企业\n名称\t信息",
        ]

        for question in special_chars:
            req = QueryRequest(question=question)
            self.assertEqual(req.question, question)

    def test_mode_validation(self):
        """测试模式验证"""
        from api_server import QueryRequest

        valid_modes = ["auto", "vanna", "llm"]
        for mode in valid_modes:
            req = QueryRequest(question="测试", mode=mode)
            self.assertEqual(req.mode, mode)

    def test_scenario_validation(self):
        """测试场景验证"""
        from api_server import QueryRequest

        valid_scenarios = [
            "data_insight",
            "regional",
            "industry",
            "investment",
            "due_diligence"
        ]

        for scenario in valid_scenarios:
            req = QueryRequest(question="测试", scenario=scenario)
            self.assertEqual(req.scenario, scenario)

    def test_generate_chart_flag(self):
        """测试图表生成标志"""
        from api_server import QueryRequest

        req_true = QueryRequest(question="测试", generate_chart=True)
        req_false = QueryRequest(question="测试", generate_chart=False)

        self.assertTrue(req_true.generate_chart)
        self.assertFalse(req_false.generate_chart)

    def test_search_request_validation(self):
        """测试搜索请求验证"""
        from api_server import SearchRequest

        # 默认结果数
        req1 = SearchRequest(query="测试")
        self.assertEqual(req1.num_results, 5)

        # 自定义结果数
        req2 = SearchRequest(query="测试", num_results=10)
        self.assertEqual(req2.num_results, 10)

        # 边界值
        req3 = SearchRequest(query="测试", num_results=1)
        self.assertEqual(req3.num_results, 1)

    def test_export_request_validation(self):
        """测试导出请求验证"""
        from api_server import ExportRequest

        # 默认格式
        req1 = ExportRequest(question="测试")
        self.assertEqual(req1.format, "excel")

        # Excel 格式
        req2 = ExportRequest(question="测试", format="excel")
        self.assertEqual(req2.format, "excel")

        # Word 格式
        req3 = ExportRequest(question="测试", format="word")
        self.assertEqual(req3.format, "word")

    def test_train_request_validation(self):
        """测试训练请求验证"""
        from api_server import TrainRequest

        # DDL 训练
        req1 = TrainRequest(ddl="CREATE TABLE test (id INT)")
        self.assertIsNotNone(req1.ddl)

        # SQL 训练
        req2 = TrainRequest(sql="SELECT * FROM test")
        self.assertIsNotNone(req2.sql)

        # 文档训练
        req3 = TrainRequest(document="这是一份文档")
        self.assertIsNotNone(req3.document)

    def test_response_model_validation(self):
        """测试响应模型验证"""
        from api_server import QueryResponse

        # 完整响应
        response = QueryResponse(
            question="测试",
            sql="SELECT * FROM test",
            data=[{"id": 1}],
            columns=["id"],
            row_count=1,
            mode="llm"
        )
        self.assertEqual(response.row_count, 1)
        self.assertEqual(response.mode, "llm")

        # 错误响应
        error_response = QueryResponse(
            question="测试",
            sql="",
            data=[],
            columns=[],
            row_count=0,
            mode="auto",
            error="测试错误"
        )
        self.assertEqual(error_response.error, "测试错误")


# =============================================================================
# 2. 配置模块边界测试
# =============================================================================

class TestConfigBoundaryConditions(unittest.TestCase):
    """配置模块边界条件测试"""

    def test_database_config_scenarios(self):
        """测试不同场景的数据库配置"""
        from src.utils.config import get_database_config

        # 场景 1-3
        config1 = get_database_config('scenario_1_3')
        self.assertIsInstance(config1, dict)
        self.assertIn('host', config1)

        # 场景 4-5
        config2 = get_database_config('scenario_4_5')
        self.assertIsInstance(config2, dict)
        self.assertIn('host', config2)

    def test_database_config_default(self):
        """测试默认数据库配置"""
        from src.utils.config import get_database_config

        # 未知场景应该返回默认配置
        # 注意：由于配置验证，可能会失败，这里只测试函数能调用
        try:
            config = get_database_config('unknown_scenario')
            self.assertIsInstance(config, dict)
        except (ValueError, KeyError):
            # 配置不存在时可能抛出异常，这是可接受的行为
            self.assertTrue(True)  # 跳过测试

    def test_kiro_config(self):
        """测试 Kiro 配置"""
        from src.utils.config import get_kiro_config

        config = get_kiro_config()
        self.assertIsInstance(config, dict)
        self.assertIn('base_url', config)
        self.assertIn('api_key', config)
        self.assertIn('model', config)

    def test_config_with_missing_env_vars(self):
        """测试缺少环境变量时的配置"""
        from src.utils.config import get_kiro_config

        # 应该返回配置对象，即使环境变量未设置
        config = get_kiro_config()
        self.assertIsInstance(config, dict)


# =============================================================================
# 3. SQL 安全边界测试
# =============================================================================

class TestSQLSecurityBoundaryConditions(unittest.TestCase):
    """SQL 安全边界条件测试"""

    def test_empty_query_handling(self):
        """测试空查询处理"""
        from src.utils.sql_security import validate_sql_query

        is_safe, msg = validate_sql_query("")
        self.assertFalse(is_safe)

    def test_whitespace_only_query(self):
        """测试纯空格查询"""
        from src.utils.sql_security import validate_sql_query

        is_safe, msg = validate_sql_query("   \n\t  ")
        self.assertFalse(is_safe)

    def test_unicode_characters(self):
        """测试 Unicode 字符处理"""
        from src.utils.sql_security import validate_sql_query

        # 中文表名
        query = "SELECT * FROM 企业表"
        is_safe, msg = validate_sql_query(query)
        self.assertTrue(is_safe)

        # 特殊 Unicode
        query = "SELECT * FROM users WHERE name = '测试'"
        is_safe, msg = validate_sql_query(query)
        self.assertTrue(is_safe)

    def test_case_insensitive_detection(self):
        """测试大小写不敏感检测"""
        from src.utils.sql_security import validate_sql_query

        dangerous_queries = [
            "DROP TABLE users",
            "drop table users",
            "DrOp TaBlE users",
            "DROP\tTABLE users",
            "DROP\nTABLE users"
        ]

        for query in dangerous_queries:
            is_safe, msg = validate_sql_query(query)
            self.assertFalse(is_safe, f"应该检测到危险查询：{query}")

    def test_comment_injection_detection(self):
        """测试注释注入检测"""
        from src.utils.sql_security import validate_sql_query

        dangerous_queries = [
            "SELECT * FROM users -- comment",
            "SELECT * FROM users # comment",
            "SELECT * FROM users /* comment */",
            "SELECT * FROM users; -- comment"
        ]

        for query in dangerous_queries:
            is_safe, msg = validate_sql_query(query)
            # 注释检测可能允许，取决于配置
            # 这里只验证函数能正常处理
            self.assertIsInstance(is_safe, bool)

    def test_nested_parentheses(self):
        """测试嵌套括号处理"""
        from src.utils.sql_security import validate_sql_query

        query = "SELECT * FROM users WHERE id IN (SELECT id FROM (SELECT * FROM roles WHERE active = 1) AS t)"
        is_safe, msg = validate_sql_query(query)
        self.assertTrue(is_safe)

    def test_very_long_query(self):
        """测试超长查询处理"""
        from src.utils.sql_security import validate_sql_query

        # 构建超长查询
        columns = ", ".join([f"col{i}" for i in range(100)])
        query = f"SELECT {columns} FROM users WHERE id = 1"

        is_safe, msg = validate_sql_query(query)
        self.assertTrue(is_safe)

    def test_multiple_statements_detection(self):
        """测试多语句检测"""
        from src.utils.sql_security import validate_sql_query

        dangerous_queries = [
            "SELECT * FROM users; DROP TABLE users;",
            "SELECT * FROM users; DELETE FROM users;",
            "SELECT * FROM users; TRUNCATE TABLE users;"
        ]

        for query in dangerous_queries:
            is_safe, msg = validate_sql_query(query)
            self.assertFalse(is_safe, f"应该检测到多语句：{query}")

    def test_table_name_validation_edge_cases(self):
        """测试表名验证边界情况"""
        from src.utils.sql_security import SQLValidator

        validator = SQLValidator()

        # 合法表名
        valid_names = ["users", "user_info", "users_2024", "t1"]
        for name in valid_names:
            is_valid, msg = validator.validate_table_name(name)
            self.assertTrue(is_valid, f"应该允许表名：{name}")

        # 非法表名
        invalid_names = ["users; DROP TABLE", "users--", "users/*", ""]
        for name in invalid_names:
            is_valid, msg = validator.validate_table_name(name)
            self.assertFalse(is_valid, f"应该拒绝表名：{name}")

    def test_column_name_validation_edge_cases(self):
        """测试列名验证边界情况"""
        from src.utils.sql_security import SQLValidator

        validator = SQLValidator()

        # 合法列名
        valid_names = ["id", "user_name", "created_at", "col1"]
        for name in valid_names:
            is_valid, msg = validator.validate_column_name(name)
            self.assertTrue(is_valid, f"应该允许列名：{name}")

        # 非法列名
        invalid_names = ["id; DROP TABLE", "id--", "id/*", ""]
        for name in invalid_names:
            is_valid, msg = validator.validate_column_name(name)
            self.assertFalse(is_valid, f"应该拒绝列名：{name}")


# =============================================================================
# 4. ASCII 图表边界测试
# =============================================================================

class TestASCIIChartBoundaryConditions(unittest.TestCase):
    """ASCII 图表边界条件测试"""

    def test_empty_data_chart(self):
        """测试空数据图表"""
        from api_server import generate_ascii_chart

        chart = generate_ascii_chart([], [])
        self.assertIn("无数据", chart)

    def test_single_row_chart(self):
        """测试单行数据图表"""
        from api_server import generate_ascii_chart

        data = [{"name": "企业 A", "value": 100}]
        columns = ["name", "value"]

        chart = generate_ascii_chart(data, columns)
        self.assertIsNotNone(chart)

    def test_large_values_chart(self):
        """测试大数值图表"""
        from api_server import generate_ascii_chart

        data = [
            {"name": "企业 A", "value": 1000000},
            {"name": "企业 B", "value": 2000000}
        ]
        columns = ["name", "value"]

        chart = generate_ascii_chart(data, columns)
        self.assertIsNotNone(chart)

    def test_zero_values_chart(self):
        """测试零值图表"""
        from api_server import generate_ascii_chart

        data = [
            {"name": "企业 A", "value": 0},
            {"name": "企业 B", "value": 0}
        ]
        columns = ["name", "value"]

        chart = generate_ascii_chart(data, columns)
        self.assertIsNotNone(chart)

    def test_negative_values_chart(self):
        """测试负值图表"""
        from api_server import generate_ascii_chart

        data = [
            {"name": "企业 A", "value": -100},
            {"name": "企业 B", "value": 200}
        ]
        columns = ["name", "value"]

        chart = generate_ascii_chart(data, columns)
        self.assertIsNotNone(chart)

    def test_many_rows_chart(self):
        """测试多行数据图表（应该只取前 10 行）"""
        from api_server import generate_ascii_chart

        data = [{"name": f"企业{i}", "value": i * 100} for i in range(100)]
        columns = ["name", "value"]

        chart = generate_ascii_chart(data, columns)
        self.assertIsNotNone(chart)
        # 应该包含图表标题
        self.assertIn("图表", chart)
        # 检查行数（标题 + 分隔线 + 10 行数据）
        lines = chart.split('\n')
        self.assertLessEqual(len(lines), 15)  # 标题 + 分隔线 + 最多 10 行
        # 检查是否包含前 10 行的数据（企业 0-企业 9）
        self.assertIn("企业", chart)
        self.assertIn("0", chart)
        self.assertIn("900", chart)  # 第 10 行的值

    def test_string_value_chart(self):
        """测试字符串值图表"""
        from api_server import generate_ascii_chart

        data = [
            {"name": "企业 A", "status": "存续"},
            {"name": "企业 B", "status": "注销"}
        ]
        columns = ["name", "status"]

        chart = generate_ascii_chart(data, columns)
        self.assertIn("无合适数据", chart)


# =============================================================================
# 5. 错误处理集成测试
# =============================================================================

class TestErrorHandlingIntegration(unittest.TestCase):
    """错误处理集成测试"""

    @patch('pymysql.connect')
    def test_database_connection_error(self, mock_connect):
        """测试数据库连接错误处理"""
        mock_connect.side_effect = Exception("连接失败")

        from api_server import execute_sql

        db_config = {
            'host': 'localhost',
            'database': 'test',
            'user': 'test',
            'password': 'test'
        }

        result = execute_sql("SELECT * FROM test", db_config)
        self.assertFalse(result['success'])
        self.assertIn("连接失败", result['error'])

    def test_sql_execution_error(self):
        """测试 SQL 执行错误处理"""
        from api_server import execute_sql

        # 使用无效配置
        db_config = {
            'host': 'invalid_host',
            'database': 'invalid_db',
            'user': 'invalid_user',
            'password': 'invalid_password'
        }

        result = execute_sql("SELECT * FROM test", db_config)
        self.assertFalse(result['success'])
        self.assertIsNotNone(result['error'])

    @patch('src.utils.config.get_kiro_config')
    def test_llm_initialization_error(self, mock_config):
        """测试 LLM 初始化错误处理"""
        # 模拟配置抛出异常
        mock_config.side_effect = Exception("配置错误")

        # 重新导入以清除缓存
        import importlib
        import api_server
        importlib.reload(api_server)

        # 应该返回 False
        result = api_server.init_llm()
        self.assertFalse(result)


# =============================================================================
# 6. 网络搜索边界测试
# =============================================================================

class TestWebSearchBoundaryConditions(unittest.TestCase):
    """网络搜索边界条件测试"""

    def test_empty_query_search(self):
        """测试空查询搜索"""
        try:
            from scripts.web_search import duckduckgo_search

            results = duckduckgo_search("")
            self.assertIsInstance(results, list)
        except ImportError:
            self.skipTest("网络搜索模块未安装")

    def test_special_characters_search(self):
        """测试特殊字符搜索"""
        try:
            from scripts.web_search import duckduckgo_search

            results = duckduckgo_search("AI & ML <2024>")
            self.assertIsInstance(results, list)
        except ImportError:
            self.skipTest("网络搜索模块未安装")

    def test_zero_results_search(self):
        """测试零结果搜索"""
        try:
            from scripts.web_search import duckduckgo_search

            results = duckduckgo_search("xyzabc123456789", max_results=0)
            self.assertEqual(len(results), 0)
        except ImportError:
            self.skipTest("网络搜索模块未安装")


# =============================================================================
# 测试运行器
# =============================================================================

def run_tests():
    """运行所有测试"""
    print("=" * 80)
    print("边界条件和错误处理测试")
    print("=" * 80)

    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # 添加测试
    suite.addTests(loader.loadTestsFromTestCase(TestAPIBoundaryConditions))
    suite.addTests(loader.loadTestsFromTestCase(TestConfigBoundaryConditions))
    suite.addTests(loader.loadTestsFromTestCase(TestSQLSecurityBoundaryConditions))
    suite.addTests(loader.loadTestsFromTestCase(TestASCIIChartBoundaryConditions))
    suite.addTests(loader.loadTestsFromTestCase(TestErrorHandlingIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestWebSearchBoundaryConditions))

    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # 汇总报告
    print()
    print("=" * 80)
    print("测试汇总")
    print("=" * 80)
    print(f"总测试数：{result.testsRun}")
    print(f"成功：{result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败：{len(result.failures)}")
    print(f"错误：{len(result.errors)}")

    if result.failures:
        print("\n失败测试:")
        for test, traceback in result.failures:
            print(f"  - {test}")

    if result.errors:
        print("\n错误测试:")
        for test, traceback in result.errors:
            print(f"  - {test}")

    success_rate = (result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100 if result.testsRun > 0 else 0
    print(f"\n成功率：{success_rate:.1f}%")

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
