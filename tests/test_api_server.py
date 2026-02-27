"""
API 服务测试

测试 api_server.py 中的 API 端点
"""
import unittest
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestAPIServer(unittest.TestCase):
    """API 服务器模块测试"""

    def test_api_server_imports(self):
        """测试 API 服务器可以导入"""
        try:
            # 测试主要导入
            from fastapi import FastAPI
            from pydantic import BaseModel
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"API 服务器依赖导入失败：{e}")

    def test_request_models(self):
        """测试请求模型"""
        from api_server import (
            QueryRequest, QueryResponse,
            SearchRequest, SearchResponse,
            ExportRequest, ExportResponse,
            ReportRequest, ReportResponse,
            TrainRequest, TrainResponse
        )

        # 测试 QueryRequest
        query_req = QueryRequest(question="测试查询")
        self.assertEqual(query_req.question, "测试查询")
        self.assertEqual(query_req.mode, "auto")

        # 测试 SearchRequest
        search_req = SearchRequest(query="测试搜索")
        self.assertEqual(search_req.query, "测试搜索")

        # 测试 ExportRequest
        export_req = ExportRequest(question="导出测试", format="excel")
        self.assertEqual(export_req.format, "excel")

        # 测试 TrainRequest
        train_req = TrainRequest(sql="SELECT * FROM test")
        self.assertEqual(train_req.sql, "SELECT * FROM test")

    def test_response_models(self):
        """测试响应模型"""
        from api_server import QueryResponse

        # 测试 QueryResponse
        response = QueryResponse(
            question="测试",
            sql="SELECT * FROM test",
            data=[{"id": 1, "name": "测试"}],
            columns=["id", "name"],
            row_count=1,
            mode="llm"
        )
        self.assertEqual(response.question, "测试")
        self.assertEqual(response.sql, "SELECT * FROM test")
        self.assertEqual(response.row_count, 1)

    def test_ascii_chart_generator(self):
        """测试 ASCII 图表生成"""
        from api_server import generate_ascii_chart

        # 测试数据
        data = [
            {"name": "企业 A", "value": 100},
            {"name": "企业 B", "value": 200},
            {"name": "企业 C", "value": 150}
        ]
        columns = ["name", "value"]

        chart = generate_ascii_chart(data, columns)
        self.assertIsNotNone(chart)
        self.assertIn("企业 A", chart)
        self.assertIn("图表", chart)

    def test_ascii_chart_empty_data(self):
        """测试空数据的 ASCII 图表"""
        from api_server import generate_ascii_chart

        chart = generate_ascii_chart([], [])
        self.assertIn("无数据", chart)

    def test_ascii_chart_no_numeric(self):
        """测试无数值列的 ASCII 图表"""
        from api_server import generate_ascii_chart

        data = [
            {"name": "企业 A", "status": "存续"},
            {"name": "企业 B", "status": "存续"}
        ]
        columns = ["name", "status"]

        chart = generate_ascii_chart(data, columns)
        self.assertIn("无合适数据", chart)


class TestConfigIntegration(unittest.TestCase):
    """配置集成测试"""

    def test_config_module_available(self):
        """测试配置模块可用"""
        try:
            from src.utils.config import get_kiro_config, get_database_config
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"配置模块导入失败：{e}")

    def test_vanna_module_available(self):
        """测试 Vanna 模块可用"""
        try:
            import vanna as vn
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Vanna 模块导入失败：{e}")

    def test_pymysql_available(self):
        """测试 PyMySQL 可用"""
        try:
            import pymysql
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"PyMySQL 导入失败：{e}")


class TestSQLSecurityIntegration(unittest.TestCase):
    """SQL 安全集成测试"""

    def test_sql_security_module_available(self):
        """测试 SQL 安全模块可用"""
        try:
            from src.utils.sql_security import validate_sql_query
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"SQL 安全模块导入失败：{e}")

    def test_dangerous_query_detection(self):
        """测试危险查询检测"""
        from src.utils.sql_security import validate_sql_query

        dangerous_queries = [
            "DROP TABLE users",
            "DELETE FROM users WHERE 1=1",
            "'; DROP TABLE users; --"
        ]

        for query in dangerous_queries:
            is_safe, msg = validate_sql_query(query)
            self.assertFalse(is_safe, f"应该检测到危险查询：{query}")

    def test_safe_query_detection(self):
        """测试安全查询检测"""
        from src.utils.sql_security import validate_sql_query

        safe_queries = [
            "SELECT * FROM users WHERE id = 1",
            "SELECT name, COUNT(*) FROM users GROUP BY name"
        ]

        for query in safe_queries:
            is_safe, msg = validate_sql_query(query)
            self.assertTrue(is_safe, f"应该允许安全查询：{query}")


# =============================================================================
# 测试运行器
# =============================================================================

def run_tests():
    """运行所有测试"""
    print("=" * 80)
    print("API 服务测试")
    print("=" * 80)

    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # 添加测试
    suite.addTests(loader.loadTestsFromTestCase(TestAPIServer))
    suite.addTests(loader.loadTestsFromTestCase(TestConfigIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestSQLSecurityIntegration))

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

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
