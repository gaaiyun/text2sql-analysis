"""
SQL 安全验证模块

提供 SQL 注入防护和输入验证功能
"""

import re
from typing import Tuple, List


class SQLSecurityError(Exception):
    """SQL 安全异常"""
    pass


class SQLValidator:
    """SQL 验证器"""
    
    # 危险关键字列表
    DANGEROUS_KEYWORDS = [
        'DROP', 'DELETE', 'TRUNCATE', 'ALTER', 'CREATE',
        'INSERT', 'UPDATE', 'REPLACE', 'GRANT', 'REVOKE',
        'EXEC', 'EXECUTE', 'XP_', 'SP_'
    ]
    
    # SQL 注入模式
    INJECTION_PATTERNS = [
        r"OR\s+1\s*=\s*1",           # OR 1=1
        r"OR\s+'1'\s*=\s*'1'",       # OR '1'='1'
        r"UNION\s+SELECT",           # UNION SELECT
        r"--\s*$",                   # 注释注入
        r";\s*DROP",                 # 多语句注入
        r";\s*DELETE",               # 多语句注入
        r"'\s*OR\s*'",               # ' OR '
        r"'\s*;\s*--",               # '; --
        r"xp_cmdshell",              # SQL Server 命令执行
        r"/\*.*\*/",                 # 块注释注入
    ]
    
    def __init__(self):
        self.compiled_patterns = [
            re.compile(pattern, re.IGNORECASE)
            for pattern in self.INJECTION_PATTERNS
        ]
    
    def validate_query(self, query: str) -> Tuple[bool, str]:
        """
        验证 SQL 查询是否安全
        
        Args:
            query: SQL 查询语句
            
        Returns:
            (is_safe, message): 是否安全及消息
        """
        if not query or not query.strip():
            return False, "查询不能为空"
        
        # 检查危险关键字
        for keyword in self.DANGEROUS_KEYWORDS:
            if re.search(rf"\b{keyword}\b", query, re.IGNORECASE):
                return False, f"检测到危险关键字：{keyword}"
        
        # 检查注入模式
        for pattern in self.compiled_patterns:
            if pattern.search(query):
                return False, f"检测到 SQL 注入模式：{pattern.pattern}"
        
        # 检查多语句执行
        if ';' in query and query.count(';') > 1:
            return False, "检测到多语句执行"
        
        return True, "查询通过验证"
    
    def sanitize_input(self, user_input: str) -> str:
        """
        清理用户输入
        
        Args:
            user_input: 用户输入
            
        Returns:
            清理后的输入
        """
        if not user_input:
            return ""
        
        # 移除危险字符
        dangerous_chars = ["'", '"', ";", "--", "/*", "*/"]
        sanitized = user_input
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, "")
        
        return sanitized.strip()
    
    def validate_table_name(self, table_name: str) -> Tuple[bool, str]:
        """
        验证表名是否合法
        
        Args:
            table_name: 表名
            
        Returns:
            (is_valid, message)
        """
        if not table_name:
            return False, "表名不能为空"
        
        # 只允许字母、数字、下划线
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', table_name):
            return False, "表名只能包含字母、数字和下划线"
        
        # 检查长度
        if len(table_name) > 64:
            return False, "表名过长（最大 64 字符）"
        
        return True, "表名合法"
    
    def validate_column_name(self, column_name: str) -> Tuple[bool, str]:
        """
        验证列名是否合法
        
        Args:
            column_name: 列名
            
        Returns:
            (is_valid, message)
        """
        if not column_name:
            return False, "列名不能为空"
        
        # 只允许字母、数字、下划线
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', column_name):
            return False, "列名只能包含字母、数字和下划线"
        
        # 检查长度
        if len(column_name) > 64:
            return False, "列名过长（最大 64 字符）"
        
        return True, "列名合法"


def validate_sql_query(query: str) -> Tuple[bool, str]:
    """
    便捷函数：验证 SQL 查询
    
    Args:
        query: SQL 查询语句
        
    Returns:
        (is_safe, message)
    """
    validator = SQLValidator()
    return validator.validate_query(query)


def sanitize_user_input(user_input: str) -> str:
    """
    便捷函数：清理用户输入
    
    Args:
        user_input: 用户输入
        
    Returns:
        清理后的输入
    """
    validator = SQLValidator()
    return validator.sanitize_input(user_input)


# 使用示例
if __name__ == "__main__":
    validator = SQLValidator()
    
    # 测试安全查询
    safe_query = "SELECT * FROM users WHERE id = 1"
    is_safe, msg = validator.validate_query(safe_query)
    print(f"安全查询：{is_safe}, {msg}")
    
    # 测试危险查询
    dangerous_query = "SELECT * FROM users; DROP TABLE users; --"
    is_safe, msg = validator.validate_query(dangerous_query)
    print(f"危险查询：{is_safe}, {msg}")
    
    # 测试注入查询
    injection_query = "SELECT * FROM users WHERE id = 1 OR 1=1"
    is_safe, msg = validator.validate_query(injection_query)
    print(f"注入查询：{is_safe}, {msg}")
