"""safe_sql.py 测试 —— schema-aware SQL 安全 + 改写。"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.utils.safe_sql import SafeSQLEnforcer, SafeSQLReport, enforce_safe_sql


# --- 基础 SELECT 通过 ---------------------------------------------------

def test_simple_select_allowed():
    rep = enforce_safe_sql("SELECT id, name FROM users")
    assert rep.is_safe is True
    assert "LIMIT" in rep.safe_sql


def test_select_with_existing_limit_passes_through():
    rep = enforce_safe_sql("SELECT * FROM orders LIMIT 50",
                            allowed_tables=["orders"])
    assert rep.is_safe is True
    assert "LIMIT 50" in rep.safe_sql


def test_select_with_where_clause():
    rep = enforce_safe_sql(
        "SELECT id FROM users WHERE created_at > '2024-01-01'",
        allowed_tables=["users"])
    assert rep.is_safe is True


def test_select_with_join():
    rep = enforce_safe_sql(
        "SELECT u.id FROM users u JOIN orders o ON u.id = o.user_id",
        allowed_tables=["users", "orders"])
    assert rep.is_safe is True
    assert "users" in rep.referenced_tables
    assert "orders" in rep.referenced_tables


def test_select_with_aggregate():
    rep = enforce_safe_sql("SELECT COUNT(*) FROM events GROUP BY date",
                            allowed_tables=["events"])
    assert rep.is_safe is True


# --- 拒绝 DML 修改语句 ------------------------------------------------

def test_reject_insert():
    rep = enforce_safe_sql("INSERT INTO users (name) VALUES ('hack')")
    assert rep.is_safe is False
    assert any("INSERT" in e or "SELECT" in e for e in rep.errors)


def test_reject_update():
    rep = enforce_safe_sql("UPDATE users SET name='x' WHERE id=1")
    assert rep.is_safe is False


def test_reject_delete():
    rep = enforce_safe_sql("DELETE FROM users WHERE id=1")
    assert rep.is_safe is False


def test_reject_drop():
    rep = enforce_safe_sql("DROP TABLE users")
    assert rep.is_safe is False
    assert any("DROP" in e for e in rep.errors)


def test_reject_truncate():
    rep = enforce_safe_sql("TRUNCATE TABLE users")
    assert rep.is_safe is False


def test_reject_alter():
    rep = enforce_safe_sql("ALTER TABLE users ADD COLUMN x INT")
    assert rep.is_safe is False


def test_reject_create():
    rep = enforce_safe_sql("CREATE TABLE x (id INT)")
    assert rep.is_safe is False


def test_reject_grant():
    rep = enforce_safe_sql("GRANT SELECT ON users TO admin")
    assert rep.is_safe is False


# --- 多语句拒绝 -------------------------------------------------------

def test_reject_multiple_statements():
    rep = enforce_safe_sql("SELECT * FROM users; DROP TABLE users;")
    assert rep.is_safe is False
    # 应至少报多语句或 DROP
    assert any("多语句" in e or "DROP" in e for e in rep.errors)


def test_single_trailing_semicolon_ok():
    """单语句末尾分号不应被当多语句。"""
    rep = enforce_safe_sql("SELECT * FROM users;",
                            allowed_tables=["users"])
    assert rep.is_safe is True


def test_two_selects_rejected():
    rep = enforce_safe_sql(
        "SELECT * FROM a; SELECT * FROM b;",
        allowed_tables=["a", "b"])
    assert rep.is_safe is False


def test_allow_multistatement_explicit():
    enforcer = SafeSQLEnforcer(allow_multistatement=True,
                                allowed_tables=["a", "b"])
    rep = enforcer.check("SELECT * FROM a; SELECT * FROM b;")
    # 即使允许多 stmt，仍只走第一个 + 强制 SELECT-only
    # 实测：sqlparse 拆出 2 个，第一个是 SELECT 通过
    assert rep.is_safe is True or "多语句" not in " ".join(rep.errors)


# --- 表白名单 ---------------------------------------------------------

def test_reject_non_whitelisted_table():
    rep = enforce_safe_sql("SELECT * FROM secrets",
                            allowed_tables=["users", "orders"])
    assert rep.is_safe is False
    assert any("非白名单" in e for e in rep.errors)


def test_allowed_tables_none_no_filtering():
    """allowed_tables=None 时不做表过滤。"""
    rep = enforce_safe_sql("SELECT * FROM whatever_table")
    assert rep.is_safe is True


def test_empty_allowed_tables_rejects_everything():
    rep = enforce_safe_sql("SELECT * FROM any_table", allowed_tables=[])
    assert rep.is_safe is False


def test_table_whitelist_case_insensitive():
    """白名单匹配应该大小写不敏感。"""
    rep = enforce_safe_sql("SELECT * FROM Users",
                            allowed_tables=["users"])
    assert rep.is_safe is True


# --- LIMIT 强制 + 截断 ----------------------------------------------

def test_no_limit_auto_added():
    rep = enforce_safe_sql("SELECT * FROM users",
                            allowed_tables=["users"], max_limit=500)
    assert "LIMIT 500" in rep.safe_sql
    assert any("自动添加" in m for m in rep.modifications)


def test_existing_limit_under_max_kept():
    rep = enforce_safe_sql("SELECT * FROM users LIMIT 100",
                            allowed_tables=["users"], max_limit=1000)
    assert "LIMIT 100" in rep.safe_sql
    # 没改 → modifications 应为空 / 不含"自动添加"
    assert not any("自动添加" in m for m in rep.modifications)


def test_existing_limit_over_max_truncated():
    rep = enforce_safe_sql("SELECT * FROM users LIMIT 999999",
                            allowed_tables=["users"], max_limit=1000)
    assert "LIMIT 1000" in rep.safe_sql
    assert any("截到 1000" in m or "1000" in m for m in rep.modifications)


def test_mysql_style_limit_offset():
    """MySQL LIMIT offset, count 风格识别 count。"""
    rep = enforce_safe_sql("SELECT * FROM users LIMIT 100, 50",
                            allowed_tables=["users"], max_limit=1000)
    assert rep.is_safe is True


def test_require_limit_false_skips_injection():
    enforcer = SafeSQLEnforcer(allowed_tables=["users"], require_limit=False)
    rep = enforcer.check("SELECT * FROM users")
    assert rep.is_safe is True
    # 没强制 → LIMIT 不该被自动加
    assert "LIMIT" not in rep.safe_sql.upper()


# --- WITH / CTE -------------------------------------------------------

def test_with_cte_select_allowed():
    sql = ("WITH active AS (SELECT id FROM users WHERE active=1) "
           "SELECT * FROM active LIMIT 10")
    rep = enforce_safe_sql(sql, allowed_tables=["users", "active"])
    assert rep.is_safe is True


def test_with_cte_disallowed_if_flag_off():
    enforcer = SafeSQLEnforcer(allow_with_cte=False,
                                allowed_tables=["users"])
    rep = enforcer.check("WITH x AS (SELECT 1) SELECT * FROM x")
    assert rep.is_safe is False


def test_with_terminating_in_insert_rejected():
    """WITH ... INSERT ... 应该被拒。"""
    sql = ("WITH x AS (SELECT 1) "
           "INSERT INTO users SELECT * FROM x")
    rep = enforce_safe_sql(sql)
    assert rep.is_safe is False


# --- 边界 + 错误处理 ---------------------------------------------------

def test_empty_sql_rejected():
    rep = enforce_safe_sql("")
    assert rep.is_safe is False
    assert any("空" in e for e in rep.errors)


def test_whitespace_only_rejected():
    rep = enforce_safe_sql("   \n   ")
    assert rep.is_safe is False


def test_referenced_tables_extracted():
    rep = enforce_safe_sql(
        "SELECT * FROM a JOIN b ON a.id = b.aid JOIN c ON b.id = c.bid",
        allowed_tables=["a", "b", "c"])
    assert set(rep.referenced_tables) == {"a", "b", "c"}


def test_referenced_tables_db_prefix_stripped():
    """`db.table` 风格只取表名。"""
    rep = enforce_safe_sql("SELECT * FROM mydb.users",
                            allowed_tables=["users"])
    # 至少不应该因为 mydb. 前缀被拒
    assert "users" in rep.referenced_tables or rep.is_safe


def test_to_dict_serializable():
    import json
    rep = enforce_safe_sql("SELECT * FROM users", allowed_tables=["users"])
    json.dumps(rep.to_dict())


# --- 显式 Enforcer 配置测试 ----------------------------------------

def test_custom_max_limit():
    enforcer = SafeSQLEnforcer(allowed_tables=["users"], max_limit=42)
    rep = enforcer.check("SELECT * FROM users")
    assert "LIMIT 42" in rep.safe_sql


def test_report_dataclass_fields():
    rep = SafeSQLReport(original="x", safe_sql=None, is_safe=False)
    assert rep.errors == []
    assert rep.warnings == []
    assert rep.referenced_tables == []
    assert rep.modifications == []


# --- 注入风格的恶意 ---------------------------------------------------

def test_or_1_equals_1_in_where_passes_select_check():
    """OR 1=1 是 application-level 注入，但 SQL 仍然是合法 SELECT。

    safe_sql 不替 sql_security 处理 application-level 注入（那是 v1
    sql_security.SQLValidator 的责任），但应该至少能拒掉 ; DROP 这类。
    """
    rep = enforce_safe_sql(
        "SELECT * FROM users WHERE id = 1 OR 1=1",
        allowed_tables=["users"])
    # safe_sql 不防 OR 1=1（语法合法的 SELECT），但加 LIMIT
    assert rep.is_safe is True


def test_comment_injection_drop_caught():
    """注释 + DROP 应该被关键字 denylist 拦。"""
    rep = enforce_safe_sql(
        "SELECT * FROM users; -- DROP TABLE users",
        allowed_tables=["users"])
    # ; DROP 经过 denylist 应被拒
    assert rep.is_safe is False
