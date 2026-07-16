"""Schema-aware safe-SQL enforcer。

v1 的 ``sql_security.py`` 只做 regex 黑名单（拦 DROP/DELETE/UPDATE 等关键字）。
对真实 text2sql 场景这不够 —— 还需要：

1. **白名单表**：LLM 可能瞎编不存在的表名 / 引用敏感表（如 users / 含 PII 的表）
2. **强制 SELECT-only**：不只看关键字，还要看真实 statement type（sqlparse）
3. **自动加 LIMIT**：防止 LLM 漏写 LIMIT 把 100M 行拖回前端
4. **单语句**：防止多语句注入混入"; DROP TABLE"

本模块用 sqlparse 解析 + 白名单 + 改写，把 LLM 输出的不安全 SQL 改写成
"安全可执行" 形态，或者明确 reject。

设计原则：**fail-closed** —— 不能确定安全就 reject，不要"修一修"放过。
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List, Optional, Sequence, Set

import sqlparse
from sqlparse.sql import Identifier, IdentifierList, Parenthesis, Statement, TokenList
from sqlparse.tokens import DML, Keyword, Name


@dataclass
class SafeSQLReport:
    """安全检查 + 改写报告。"""
    original: str
    safe_sql: Optional[str]      # 改写后；None = 拒绝
    is_safe: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    referenced_tables: List[str] = field(default_factory=list)
    modifications: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "original": self.original,
            "safe_sql": self.safe_sql,
            "is_safe": bool(self.is_safe),
            "errors": list(self.errors),
            "warnings": list(self.warnings),
            "referenced_tables": list(self.referenced_tables),
            "modifications": list(self.modifications),
        }


class SafeSQLEnforcer:
    """Schema-aware SQL safety + 改写器。

    主要 API：``check(sql) -> SafeSQLReport``。

    Parameters
    ----------
    allowed_tables : 白名单表（小写）。``None`` 表示不限制（只做语句类型 +
        LIMIT 检查）；空集合 = 任何表都拒绝。
    max_limit : 自动注入的 LIMIT 上限。默认 1000。如 SQL 已有 LIMIT N，N
        被截到 max_limit。
    require_limit : 是否强制 LIMIT。True 时缺 LIMIT 会自动注入。
    allow_with_cte : 是否允许 WITH ... SELECT。默认 True。
    allow_multistatement : 是否允许多 statement（"; 分隔"）。默认 False。
    """

    READ_ONLY_DML = {"SELECT"}     # 只允许 SELECT
    DENYLIST_KEYWORDS = {
        "DROP", "DELETE", "TRUNCATE", "ALTER", "CREATE",
        "INSERT", "UPDATE", "REPLACE", "GRANT", "REVOKE",
        "EXEC", "EXECUTE", "MERGE", "CALL", "HANDLER",
        "LOCK", "UNLOCK", "RENAME",
        # MySQL permits file-system access inside otherwise valid SELECTs.
        "OUTFILE", "DUMPFILE", "LOAD_FILE",
    }

    def __init__(self, *,
                 allowed_tables: Optional[Sequence[str]] = None,
                 max_limit: int = 1000,
                 require_limit: bool = True,
                 allow_with_cte: bool = True,
                 allow_multistatement: bool = False):
        self.allowed_tables: Optional[Set[str]] = (
            {t.lower() for t in allowed_tables}
            if allowed_tables is not None else None
        )
        self.max_limit = max_limit
        self.require_limit = require_limit
        self.allow_with_cte = allow_with_cte
        self.allow_multistatement = allow_multistatement

    # --- 主入口 -------------------------------------------------------

    def check(self, sql: str) -> SafeSQLReport:
        report = SafeSQLReport(original=sql, safe_sql=None, is_safe=False)
        if not sql or not sql.strip():
            report.errors.append("空查询")
            return report

        # 1) 多语句检查
        parsed = sqlparse.parse(sql.strip().rstrip(";"))
        non_empty = [s for s in parsed if str(s).strip()]
        if len(non_empty) > 1 and not self.allow_multistatement:
            report.errors.append(
                f"检测到 {len(non_empty)} 个 statement，拒绝多语句"
            )
            return report
        if not non_empty:
            report.errors.append("解析失败")
            return report

        stmt: Statement = non_empty[0]

        # 2) 语句类型检查（必须是 SELECT 或允许的 WITH...SELECT）
        stmt_type = self._statement_type(stmt)
        if stmt_type not in self.READ_ONLY_DML:
            if stmt_type == "WITH" and self.allow_with_cte:
                # WITH x AS (SELECT ...) SELECT ... —— 视情况允许
                if not self._with_terminates_in_select(stmt):
                    report.errors.append("WITH 必须以 SELECT 结尾")
                    return report
            else:
                report.errors.append(
                    f"只允许 SELECT 类型；解析到 {stmt_type}"
                )
                return report

        # 3) Denylist 关键字（防 sqlparse 把恶意混入解析成 Identifier）
        upper = sql.upper()
        for kw in self.DENYLIST_KEYWORDS:
            if re.search(rf"\b{kw}\b", upper):
                report.errors.append(f"检测到禁用关键字：{kw}")
                return report

        # 4) 表白名单
        tables = self._extract_tables(stmt)
        report.referenced_tables = sorted(set(tables))
        if self.allowed_tables is not None:
            disallowed = [t for t in tables if t.lower() not in self.allowed_tables]
            if disallowed:
                report.errors.append(
                    f"引用了非白名单表：{sorted(set(disallowed))}"
                )
                return report

        # 5) 强制 LIMIT
        sql_clean = str(stmt).strip().rstrip(";")
        existing_limit = self._find_limit(sql_clean)
        if existing_limit is None and self.require_limit:
            sql_clean = f"{sql_clean} LIMIT {self.max_limit}"
            report.modifications.append(f"自动添加 LIMIT {self.max_limit}")
        elif existing_limit is not None and existing_limit > self.max_limit:
            sql_clean = self._replace_limit(sql_clean, self.max_limit)
            report.modifications.append(
                f"LIMIT {existing_limit} 超过上限，截到 {self.max_limit}"
            )

        # 6) 通过
        report.safe_sql = sql_clean
        report.is_safe = True
        return report

    # --- 内部辅助 -----------------------------------------------------

    @staticmethod
    def _statement_type(stmt: Statement) -> str:
        """获取 statement 的"主类型"（SELECT / INSERT / WITH 等）。"""
        for tok in stmt.tokens:
            if tok.is_whitespace or tok.ttype is sqlparse.tokens.Comment:
                continue
            value = tok.value.upper()
            # DML 类
            if tok.ttype is DML:
                return value
            # WITH / EXPLAIN 等关键字
            if tok.ttype is Keyword and value in ("WITH", "EXPLAIN", "DESC", "DESCRIBE", "SHOW"):
                return value
            # 首 token 是 SELECT 名识别
            if value in ("SELECT", "WITH"):
                return value
            break
        return stmt.get_type() or "UNKNOWN"

    @staticmethod
    def _with_terminates_in_select(stmt: Statement) -> bool:
        """检查 WITH ... 是否以 SELECT 结尾（而非 INSERT/UPDATE/DELETE）。"""
        text_upper = str(stmt).upper()
        # 简单启发式：最后一个 SELECT 必须存在，且不能有 INSERT/UPDATE/DELETE
        bad_kws = ["INSERT", "UPDATE", "DELETE", "REPLACE", "MERGE"]
        for kw in bad_kws:
            if re.search(rf"\b{kw}\b", text_upper):
                return False
        return "SELECT" in text_upper

    @staticmethod
    def _extract_tables(stmt: Statement) -> List[str]:
        """从 statement 抽出表名（FROM / JOIN 后跟的 Identifier）。

        不用 flatten —— Identifier 是子树，flatten 后 ``mydb.users`` 会被拆成
        ``mydb`` / ``.`` / ``users`` 三个 token，取第一个就成了 ``mydb``。
        改成走非 flatten 的 ``stmt.tokens``，看 Identifier 子树，用
        ``get_real_name()`` 取真实表名。
        """
        tables: List[str] = []

        def _identifier_name(ident) -> Optional[str]:
            if hasattr(ident, "get_real_name"):
                name = ident.get_real_name()
                if name:
                    return name.strip("`\"")
            raw = str(ident).strip()
            raw = raw.split(" ")[0].split(".")[-1].strip("`\"")
            return raw or None

        def _contains_parenthesized_select(ident: Identifier) -> bool:
            for child in getattr(ident, "tokens", []):
                if isinstance(child, Parenthesis) and "SELECT" in child.value.upper():
                    return True
            return False

        def _walk(tok_list: TokenList) -> None:
            seen_from_or_join = False
            for tok in tok_list.tokens:
                if tok.is_whitespace or tok.ttype is sqlparse.tokens.Comment:
                    continue
                val_upper = tok.value.upper().strip()
                if (tok.ttype is Keyword
                        and val_upper in ("FROM", "JOIN", "INNER JOIN",
                                           "LEFT JOIN", "RIGHT JOIN",
                                           "FULL JOIN", "CROSS JOIN")):
                    seen_from_or_join = True
                    continue
                if seen_from_or_join:
                    if isinstance(tok, IdentifierList):
                        for ident in tok.get_identifiers():
                            if isinstance(ident, Identifier) and _contains_parenthesized_select(ident):
                                _walk(ident)
                                continue
                            name = _identifier_name(ident)
                            if name:
                                tables.append(name)
                    elif isinstance(tok, Identifier):
                        if _contains_parenthesized_select(tok):
                            _walk(tok)
                        else:
                            name = _identifier_name(tok)
                            if name:
                                tables.append(name)
                    elif tok.ttype is Name:
                        tables.append(tok.value.strip("`\""))
                    # ( 或子查询：不计入表，仍要递归找内部
                    seen_from_or_join = False
                if hasattr(tok, "tokens") and not isinstance(
                        tok, (Identifier, IdentifierList)):
                    _walk(tok)

        _walk(stmt)
        return tables

    @staticmethod
    def _find_limit(sql: str) -> Optional[int]:
        """从 SQL 末尾找 LIMIT N；返回 N 或 None。"""
        m = re.search(r"\bLIMIT\s+(\d+)(?:\s*,\s*(\d+))?\s*$",
                       sql, re.IGNORECASE)
        if not m:
            return None
        # MySQL 风格 LIMIT offset, count
        if m.group(2):
            return int(m.group(2))
        return int(m.group(1))

    @staticmethod
    def _replace_limit(sql: str, new_limit: int) -> str:
        return re.sub(r"\bLIMIT\s+\d+(?:\s*,\s*\d+)?\s*$",
                       f"LIMIT {new_limit}", sql, flags=re.IGNORECASE)


# --- 便捷函数 --------------------------------------------------------------

def enforce_safe_sql(sql: str, *,
                     allowed_tables: Optional[Sequence[str]] = None,
                     max_limit: int = 1000) -> SafeSQLReport:
    """一行调用：检查 + 可能改写 SQL。"""
    enforcer = SafeSQLEnforcer(
        allowed_tables=allowed_tables,
        max_limit=max_limit,
    )
    return enforcer.check(sql)
