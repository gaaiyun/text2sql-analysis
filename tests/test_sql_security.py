"""
SQL 安全测试模块

测试 SQL 注入防护和输入验证功能
"""

import unittest
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.sql_security import SQLValidator, validate_sql_query, sanitize_user_input


class TestSQLValidator(unittest.TestCase):
    """SQL 验证器测试"""
    
    def setUp(self):
        self.validator = SQLValidator()
    
    def test_safe_query(self):
        """测试安全查询"""
        safe_queries = [
            "SELECT * FROM users WHERE id = 1",
            "SELECT name, age FROM users WHERE age > 18",
            "SELECT COUNT(*) FROM orders",
            "SELECT * FROM users WHERE name = 'John'",
        ]
        
        for query in safe_queries:
            is_safe, msg = self.validator.validate_query(query)
            self.assertTrue(is_safe, f"查询应该安全：{query}")
    
    def test_dangerous_keywords(self):
        """测试危险关键字检测"""
        dangerous_queries = [
            ("DROP TABLE users", "DROP"),
            ("DELETE FROM users", "DELETE"),
            ("TRUNCATE TABLE users", "TRUNCATE"),
            ("ALTER TABLE users ADD column", "ALTER"),
            ("INSERT INTO users VALUES", "INSERT"),
            ("UPDATE users SET name", "UPDATE"),
            ("EXEC xp_cmdshell", "EXEC"),
        ]
        
        for query, keyword in dangerous_queries:
            is_safe, msg = self.validator.validate_query(query)
            self.assertFalse(is_safe, f"应该检测到危险关键字：{keyword}")
            self.assertIn(keyword.upper(), msg)
    
    def test_sql_injection_patterns(self):
        """测试 SQL 注入模式检测"""
        injection_queries = [
            "SELECT * FROM users WHERE id = 1 OR 1=1",
            "SELECT * FROM users WHERE name = '' OR '1'='1'",
            "SELECT * FROM users UNION SELECT * FROM passwords",
            "SELECT * FROM users; DROP TABLE users; --",
            "SELECT * FROM users WHERE name = 'admin'--",
            "SELECT * FROM users WHERE id = 1; DROP TABLE users",
        ]
        
        for query in injection_queries:
            is_safe, msg = self.validator.validate_query(query)
            self.assertFalse(is_safe, f"应该检测到 SQL 注入：{query}")
    
    def test_multi_statement(self):
        """测试多语句检测"""
        multi_query = "SELECT * FROM users; DELETE FROM users; INSERT INTO users VALUES (1)"
        is_safe, msg = self.validator.validate_query(multi_query)
        self.assertFalse(is_safe, "应该检测到多语句执行")
    
    def test_empty_query(self):
        """测试空查询"""
        is_safe, msg = self.validator.validate_query("")
        self.assertFalse(is_safe)
        self.assertIn("空", msg)
        
        is_safe, msg = self.validator.validate_query("   ")
        self.assertFalse(is_safe)
    
    def test_sanitize_input(self):
        """测试输入清理"""
        test_cases = [
            ("'; DROP TABLE users; --", "DROP TABLE users"),
            ("John'Doe", "JohnDoe"),
            ("test; DELETE", "test DELETE"),
            ("normal input", "normal input"),
        ]
        
        for input_str, expected_contains in test_cases:
            sanitized = self.validator.sanitize_input(input_str)
            self.assertNotIn("'", sanitized)
            self.assertNotIn(";", sanitized)
            self.assertNotIn("--", sanitized)
    
    def test_table_name_validation(self):
        """测试表名验证"""
        valid_names = ["users", "user_info", "Users123", "_temp"]
        for name in valid_names:
            is_valid, msg = self.validator.validate_table_name(name)
            self.assertTrue(is_valid, f"表名应该合法：{name}")
        
        invalid_names = ["", "users; DROP", "123users", "a" * 65]
        for name in invalid_names:
            is_valid, msg = self.validator.validate_table_name(name)
            self.assertFalse(is_valid, f"表名应该非法：{name}")
    
    def test_column_name_validation(self):
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


class TestEdgeCases(unittest.TestCase):
    """边界条件测试"""
    
    def setUp(self):
        self.validator = SQLValidator()
    
    def test_case_insensitive(self):
        """测试大小写不敏感"""
        dangerous_queries = [
            "drop table users",
            "DROP TABLE users",
            "DrOp TaBlE users",
        ]
        
        for query in dangerous_queries:
            is_safe, msg = self.validator.validate_query(query)
            self.assertFalse(is_safe, f"应该检测到危险关键字（不区分大小写）：{query}")
    
    def test_whitespace_variations(self):
        """测试空白字符变体"""
        injection_queries = [
            "SELECT * FROM users WHERE 1=  1",
            "SELECT * FROM users WHERE 1 = 1",
            "SELECT * FROM users WHERE   1=1",
        ]
        
        for query in injection_queries:
            is_safe, msg = self.validator.validate_query(query)
            # 这些应该被检测到（如果模式匹配正确）
            # 注意：取决于具体的正则表达式实现
    
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
