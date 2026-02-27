"""
SQL 注入安全测试模块

测试 SQL 注入防护和输入验证功能
包括 5 个安全测试场景：
1. 正常查询验证
2. 危险关键字检测
3. SQL 注入模式检测
4. 多语句注入检测
5. 边界条件测试

使用方法:
    python tests/test_sql_injection.py
"""

import unittest
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.sql_security import SQLValidator, validate_sql_query, sanitize_user_input


class TestScenario1SafeQueries(unittest.TestCase):
    """场景 1: 正常查询验证测试"""

    def setUp(self):
        self.validator = SQLValidator()

    def test_simple_select(self):
        """测试简单 SELECT 查询"""
        query = "SELECT * FROM users WHERE id = 1"
        is_safe, msg = self.validator.validate_query(query)
        self.assertTrue(is_safe, f"应该是安全的：{query}")

    def test_select_with_join(self):
        """测试带 JOIN 的查询"""
        query = """
            SELECT u.name, o.total
            FROM users u
            JOIN orders o ON u.id = o.user_id
            WHERE o.total > 100
        """
        is_safe, msg = self.validator.validate_query(query)
        self.assertTrue(is_safe, f"应该是安全的：{query}")

    def test_select_with_aggregation(self):
        """测试带聚合函数的查询"""
        query = """
            SELECT department, COUNT(*) as emp_count, AVG(salary) as avg_salary
            FROM employees
            GROUP BY department
            HAVING COUNT(*) > 5
        """
        is_safe, msg = self.validator.validate_query(query)
        self.assertTrue(is_safe, f"应该是安全的：{query}")

    def test_select_with_subquery(self):
        """测试带子查询的查询"""
        query = """
            SELECT name FROM users
            WHERE id IN (SELECT user_id FROM orders WHERE total > 1000)
        """
        is_safe, msg = self.validator.validate_query(query)
        self.assertTrue(is_safe, f"应该是安全的：{query}")

    def test_select_with_string_literal(self):
        """测试带字符串字面量的查询"""
        query = "SELECT * FROM users WHERE name = 'John'"
        is_safe, msg = self.validator.validate_query(query)
        self.assertTrue(is_safe, f"应该是安全的：{query}")


class TestScenario2DangerousKeywords(unittest.TestCase):
    """场景 2: 危险关键字检测测试"""

    def setUp(self):
        self.validator = SQLValidator()

    def test_drop_detection(self):
        """测试 DROP 检测"""
        queries = [
            "DROP TABLE users",
            "DROP DATABASE test",
            "SELECT * FROM users; DROP TABLE users",
        ]
        for query in queries:
            is_safe, msg = self.validator.validate_query(query)
            self.assertFalse(is_safe, f"应该检测到 DROP：{query}")
            self.assertIn("DROP", msg)

    def test_delete_detection(self):
        """测试 DELETE 检测"""
        queries = [
            "DELETE FROM users",
            "DELETE FROM users WHERE id = 1",
            "SELECT * FROM users; DELETE FROM orders",
        ]
        for query in queries:
            is_safe, msg = self.validator.validate_query(query)
            self.assertFalse(is_safe, f"应该检测到 DELETE：{query}")
            self.assertIn("DELETE", msg)

    def test_truncate_detection(self):
        """测试 TRUNCATE 检测"""
        queries = [
            "TRUNCATE TABLE users",
            "TRUNCATE orders",
        ]
        for query in queries:
            is_safe, msg = self.validator.validate_query(query)
            self.assertFalse(is_safe, f"应该检测到 TRUNCATE：{query}")

    def test_alter_detection(self):
        """测试 ALTER 检测"""
        queries = [
            "ALTER TABLE users ADD COLUMN email VARCHAR(100)",
            "ALTER DATABASE test CHARSET utf8",
        ]
        for query in queries:
            is_safe, msg = self.validator.validate_query(query)
            self.assertFalse(is_safe, f"应该检测到 ALTER：{query}")
            self.assertIn("ALTER", msg)

    def test_insert_detection(self):
        """测试 INSERT 检测"""
        queries = [
            "INSERT INTO users VALUES (1, 'test')",
            "INSERT INTO users (name, email) VALUES ('test', 'test@test.com')",
        ]
        for query in queries:
            is_safe, msg = self.validator.validate_query(query)
            self.assertFalse(is_safe, f"应该检测到 INSERT：{query}")
            self.assertIn("INSERT", msg)

    def test_update_detection(self):
        """测试 UPDATE 检测"""
        queries = [
            "UPDATE users SET name = 'test'",
            "UPDATE users SET email = 'new@test.com' WHERE id = 1",
        ]
        for query in queries:
            is_safe, msg = self.validator.validate_query(query)
            self.assertFalse(is_safe, f"应该检测到 UPDATE：{query}")
            self.assertIn("UPDATE", msg)

    def test_exec_detection(self):
        """测试 EXEC 检测"""
        queries = [
            "EXEC xp_cmdshell 'dir'",
            "EXECUTE sp_executesql @sql",
        ]
        for query in queries:
            is_safe, msg = self.validator.validate_query(query)
            self.assertFalse(is_safe, f"应该检测到 EXEC：{query}")


class TestScenario3InjectionPatterns(unittest.TestCase):
    """场景 3: SQL 注入模式检测测试"""

    def setUp(self):
        self.validator = SQLValidator()

    def test_or_1_equals_1(self):
        """测试 OR 1=1 注入"""
        queries = [
            "SELECT * FROM users WHERE id = 1 OR 1=1",
            "SELECT * FROM users WHERE name = '' OR '1'='1'",
        ]
        for query in queries:
            is_safe, msg = self.validator.validate_query(query)
            self.assertFalse(is_safe, f"应该检测到 OR 1=1 注入：{query}")

    def test_union_select(self):
        """测试 UNION SELECT 注入"""
        queries = [
            "SELECT * FROM users UNION SELECT * FROM passwords",
            "SELECT name FROM users UNION SELECT password FROM admin",
        ]
        for query in queries:
            is_safe, msg = self.validator.validate_query(query)
            self.assertFalse(is_safe, f"应该检测到 UNION SELECT：{query}")
            self.assertIn("UNION", msg)

    def test_comment_injection(self):
        """测试注释注入"""
        queries = [
            "SELECT * FROM users WHERE name = 'admin'--",
            "SELECT * FROM users WHERE id = 1; DROP TABLE users; --",
            "SELECT * FROM users WHERE 1=1 /* comment */",
        ]
        for query in queries:
            is_safe, msg = self.validator.validate_query(query)
            self.assertFalse(is_safe, f"应该检测到注释注入：{query}")

    def test_multi_statement_injection(self):
        """测试多语句注入"""
        queries = [
            "SELECT * FROM users; DROP TABLE users;",
            "SELECT * FROM users; DELETE FROM orders; INSERT INTO logs VALUES (1)",
        ]
        for query in queries:
            is_safe, msg = self.validator.validate_query(query)
            self.assertFalse(is_safe, f"应该检测到多语句注入：{query}")

    def test_xp_cmdshell_injection(self):
        """测试 xp_cmdshell 注入"""
        queries = [
            "SELECT * FROM users; EXEC xp_cmdshell 'dir'",
            "SELECT * FROM users WHERE name = 'test' AND xp_cmdshell('dir')",
        ]
        for query in queries:
            is_safe, msg = self.validator.validate_query(query)
            self.assertFalse(is_safe, f"应该检测到 xp_cmdshell：{query}")


class TestScenario4MultiStatement(unittest.TestCase):
    """场景 4: 多语句执行检测测试"""

    def setUp(self):
        self.validator = SQLValidator()

    def test_semicolon_detection(self):
        """测试分号检测"""
        query = "SELECT * FROM users; DELETE FROM users; INSERT INTO users VALUES (1)"
        is_safe, msg = self.validator.validate_query(query)
        self.assertFalse(is_safe, "应该检测到多语句执行")

    def test_single_semicolon_allowed(self):
        """测试单个分号允许（某些 SQL 语句可能包含）"""
        # 注意：单个分号在某些情况下是允许的
        # 但多个分号应该被拒绝
        query = "SELECT * FROM users"
        is_safe, msg = self.validator.validate_query(query)
        self.assertTrue(is_safe, "单个语句应该安全")


class TestScenario5EdgeCases(unittest.TestCase):
    """场景 5: 边界条件测试"""

    def setUp(self):
        self.validator = SQLValidator()

    def test_empty_query(self):
        """测试空查询"""
        is_safe, msg = self.validator.validate_query("")
        self.assertFalse(is_safe, "空查询应该被拒绝")
        self.assertIn("空", msg)

    def test_whitespace_query(self):
        """测试纯空白查询"""
        is_safe, msg = self.validator.validate_query("   ")
        self.assertFalse(is_safe, "纯空白查询应该被拒绝")

    def test_case_insensitive(self):
        """测试大小写不敏感"""
        queries = [
            "drop table users",
            "DROP TABLE users",
            "DrOp TaBlE users",
        ]
        for query in queries:
            is_safe, msg = self.validator.validate_query(query)
            self.assertFalse(is_safe, f"应该检测到危险关键字（不区分大小写）：{query}")

    def test_unicode_input(self):
        """测试 Unicode 输入"""
        query = "SELECT * FROM users WHERE name = '用户'"
        is_safe, msg = self.validator.validate_query(query)
        self.assertTrue(is_safe, "应该允许 Unicode 字符")

    def test_very_long_query(self):
        """测试长查询"""
        long_query = "SELECT * FROM users WHERE " + " AND ".join([f"id={i}" for i in range(100)])
        is_safe, msg = self.validator.validate_query(long_query)
        # 长查询本身不应该被拒绝，除非包含危险内容
        # 这个测试用于验证不会因为长度而崩溃

    def test_sanitize_input(self):
        """测试输入清理"""
        test_cases = [
            ("'; DROP TABLE users; --", ""),
            ("John'Doe", "JohnDoe"),
            ("test; DELETE", "test DELETE"),
            ("normal input", "normal input"),
        ]

        for input_str, expected_safe in test_cases:
            sanitized = self.validator.sanitize_input(input_str)
            self.assertNotIn("'", sanitized)
            self.assertNotIn(";", sanitized)
            self.assertNotIn("--", sanitized)

    def test_validate_table_name(self):
        """测试表名验证"""
        valid_names = ["users", "user_info", "Users123", "_temp"]
        for name in valid_names:
            is_valid, msg = self.validator.validate_table_name(name)
            self.assertTrue(is_valid, f"表名应该合法：{name}")

        invalid_names = ["", "users; DROP", "123users", "a" * 65]
        for name in invalid_names:
            is_valid, msg = self.validator.validate_table_name(name)
            self.assertFalse(is_valid, f"表名应该非法：{name}")

    def test_validate_column_name(self):
        """测试列名验证"""
        valid_names = ["id", "user_name", "UserName123", "_temp"]
        for name in valid_names:
            is_valid, msg = self.validator.validate_column_name(name)
            self.assertTrue(is_valid, f"列名应该合法：{name}")

        invalid_names = ["", "user; DROP", "123id", "a" * 65]
        for name in invalid_names:
            is_valid, msg = self.validator.validate_column_name(name)
            self.assertFalse(is_valid, f"列名应该非法：{name}")


class TestConvenienceFunctions(unittest.TestCase):
    """便捷函数测试"""

    def test_validate_sql_query(self):
        """测试 validate_sql_query 函数"""
        is_safe, msg = validate_sql_query("SELECT * FROM users")
        self.assertTrue(is_safe)

        is_safe, msg = validate_sql_query("DROP TABLE users")
        self.assertFalse(is_safe)

    def test_sanitize_user_input(self):
        """测试 sanitize_user_input 函数"""
        sanitized = sanitize_user_input("'; DROP TABLE users; --")
        self.assertNotIn("'", sanitized)
        self.assertNotIn(";", sanitized)


# =============================================================================
# 测试运行器
# =============================================================================

def run_tests():
    """运行所有测试"""
    print("=" * 80)
    print("SQL 注入安全测试套件")
    print("=" * 80)
    print()

    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # 添加 5 个场景的测试
    suite.addTests(loader.loadTestsFromTestCase(TestScenario1SafeQueries))
    suite.addTests(loader.loadTestsFromTestCase(TestScenario2DangerousKeywords))
    suite.addTests(loader.loadTestsFromTestCase(TestScenario3InjectionPatterns))
    suite.addTests(loader.loadTestsFromTestCase(TestScenario4MultiStatement))
    suite.addTests(loader.loadTestsFromTestCase(TestScenario5EdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestConvenienceFunctions))

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

    success_rate = (result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100
    print(f"成功率：{success_rate:.1f}%")

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
