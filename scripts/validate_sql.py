"""
SQL 语法验证工具
验证生成的 SQL 是否合法

使用方法:
    python validate_sql.py "SELECT * FROM table"
"""

import sqlparse
import sys

def validate_sql(sql):
    """
    验证 SQL 语法
    
    返回：
    (is_valid, error_message)
    """
    # 1. 检查是否单个 SELECT
    select_count = sql.upper().count('SELECT')
    if select_count > 1:
        return False, f"Multiple SELECT statements detected ({select_count})"
    
    # 2. 使用 sqlparse 验证语法
    try:
        parsed = sqlparse.parse(sql)
        if not parsed:
            return False, "Empty SQL"
        
        # 检查是否是有效的 SQL 语句
        stmt = parsed[0]
        if stmt.get_type() not in ('SELECT', 'UNKNOWN'):
            return False, f"Invalid SQL type: {stmt.get_type()}"
        
        return True, None
    except Exception as e:
        return False, f"Parse error: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_sql.py \"SELECT * FROM table\"")
        sys.exit(1)
    
    sql = sys.argv[1]
    is_valid, error = validate_sql(sql)
    
    if is_valid:
        print("[OK] SQL is valid")
        sys.exit(0)
    else:
        print(f"[ERROR] {error}")
        sys.exit(1)
