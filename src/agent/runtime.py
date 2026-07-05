from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Any, Callable, TypedDict

import pymysql

from src.utils.safe_sql import SafeSQLReport, enforce_safe_sql

from .llm import VolcengineArkProvider
from .profiles import DatabaseProfile, get_database_profile


SQLExecutor = Callable[[str], dict[str, Any]]


class AgentState(TypedDict, total=False):
    question: str
    scenario: str
    trace: list[dict[str, Any]]
    result: "AgentResult"
    intent: dict[str, Any]
    schema: str
    sql: str
    safety: SafeSQLReport
    attempt: int
    execution_ok: bool
    last_error: str | None


@dataclass
class AgentResult:
    question: str
    scenario: str
    success: bool
    sql: str | None = None
    safe_sql: str | None = None
    columns: list[str] = field(default_factory=list)
    rows: list[dict[str, Any]] = field(default_factory=list)
    row_count: int = 0
    analysis: str = ""
    report: str = ""
    chart: dict[str, Any] | None = None
    error: str | None = None
    safety: dict[str, Any] | None = None
    trace: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "question": self.question,
            "scenario": self.scenario,
            "success": self.success,
            "sql": self.sql,
            "safe_sql": self.safe_sql,
            "columns": self.columns,
            "rows": self.rows,
            "row_count": self.row_count,
            "analysis": self.analysis,
            "report": self.report,
            "chart": self.chart,
            "error": self.error,
            "safety": self.safety,
            "trace": self.trace,
        }


class AgentRuntime:
    """Unified Text2SQL Agent runtime used by API, Streamlit, Web, and demos."""

    node_names = (
        "classify_intent",
        "retrieve_schema",
        "generate_sql",
        "validate_sql",
        "execute_sql",
        "repair_sql",
        "profile_result",
        "decide_chart_search_compute",
        "analyze",
        "compose_report",
        "reflect_quality",
    )

    def __init__(
        self,
        *,
        profile: DatabaseProfile | None = None,
        llm: Any | None = None,
        sql_executor: SQLExecutor | None = None,
        db_config: dict[str, Any] | None = None,
        max_retries: int = 2,
        max_limit: int = 1000,
    ) -> None:
        self.profile = profile or get_database_profile("znjz")
        self.llm = llm or VolcengineArkProvider()
        self.sql_executor = sql_executor or self._build_sql_executor(db_config or {})
        self.max_retries = max_retries
        self.max_limit = max_limit
        self.workflow_backend = "linear"
        self._graph = self._build_langgraph()

    def query(self, question: str, *, scenario: str = "data_insight") -> AgentResult:
        if self._graph is not None:
            return self._query_graph(question, scenario=scenario)
        return self._query_linear(question, scenario=scenario)

    def _query_linear(self, question: str, *, scenario: str = "data_insight") -> AgentResult:
        trace: list[dict[str, Any]] = []
        result = AgentResult(question=question, scenario=scenario, success=False, trace=trace)

        intent = self._classify_intent(question, scenario, trace)
        schema = self._retrieve_schema(trace)
        sql = self._generate_sql(question, scenario, schema, intent, trace)
        result.sql = sql

        last_error: str | None = None
        for attempt in range(self.max_retries + 1):
            safety = self._validate_sql(sql, trace)
            result.safety = safety.to_dict()
            if not safety.is_safe:
                result.sql = sql
                result.safe_sql = None
                result.error = "; ".join(safety.errors) or "SQL安全校验未通过"
                return result

            result.safe_sql = safety.safe_sql
            try:
                query_result = self._execute_sql(safety.safe_sql or sql, trace)
                result.columns = list(query_result.get("columns") or [])
                result.rows = [dict(row) for row in query_result.get("rows") or []]
                result.row_count = int(query_result.get("row_count", len(result.rows)))
                self._profile_result(result, trace)
                self._decide_chart_search_compute(result, trace)
                result.analysis = self._analyze(question, scenario, result, trace)
                result.report = self._compose_report(result, trace)
                self._reflect_quality(result, trace)
                result.success = True
                result.error = None
                result.sql = sql
                return result
            except Exception as exc:
                last_error = str(exc)
                trace.append({"node": "execute_sql", "status": "error", "error": last_error, "attempt": attempt + 1})
                if attempt >= self.max_retries:
                    result.error = f"SQL执行失败，已重试{self.max_retries}次：{last_error}"
                    return result
                sql = self._repair_sql(question, scenario, schema, sql, last_error, trace)
                result.sql = sql

        result.error = last_error or "Agent执行失败"
        return result

    def _query_graph(self, question: str, *, scenario: str = "data_insight") -> AgentResult:
        trace: list[dict[str, Any]] = []
        result = AgentResult(question=question, scenario=scenario, success=False, trace=trace)
        state = self._graph.invoke(
            {
                "question": question,
                "scenario": scenario,
                "trace": trace,
                "result": result,
                "attempt": 0,
                "last_error": None,
                "execution_ok": False,
            }
        )
        return state["result"]

    def _build_langgraph(self) -> Any | None:
        try:
            from langgraph.graph import END, StateGraph
        except Exception:
            return None

        graph = StateGraph(AgentState)
        graph.add_node("classify_intent", self._graph_classify_intent)
        graph.add_node("retrieve_schema", self._graph_retrieve_schema)
        graph.add_node("generate_sql", self._graph_generate_sql)
        graph.add_node("validate_sql", self._graph_validate_sql)
        graph.add_node("execute_sql", self._graph_execute_sql)
        graph.add_node("repair_sql", self._graph_repair_sql)
        graph.add_node("profile_result", self._graph_profile_result)
        graph.add_node("decide_chart_search_compute", self._graph_decide_chart_search_compute)
        graph.add_node("analyze", self._graph_analyze)
        graph.add_node("compose_report", self._graph_compose_report)
        graph.add_node("reflect_quality", self._graph_reflect_quality)

        graph.set_entry_point("classify_intent")
        graph.add_edge("classify_intent", "retrieve_schema")
        graph.add_edge("retrieve_schema", "generate_sql")
        graph.add_edge("generate_sql", "validate_sql")
        graph.add_conditional_edges(
            "validate_sql",
            self._graph_after_validate,
            {"execute": "execute_sql", "end": END},
        )
        graph.add_conditional_edges(
            "execute_sql",
            self._graph_after_execute,
            {"profile": "profile_result", "repair": "repair_sql", "end": END},
        )
        graph.add_edge("repair_sql", "validate_sql")
        graph.add_edge("profile_result", "decide_chart_search_compute")
        graph.add_edge("decide_chart_search_compute", "analyze")
        graph.add_edge("analyze", "compose_report")
        graph.add_edge("compose_report", "reflect_quality")
        graph.add_edge("reflect_quality", END)

        self.workflow_backend = "langgraph"
        return graph.compile()

    def _graph_classify_intent(self, state: AgentState) -> AgentState:
        state["intent"] = self._classify_intent(state["question"], state["scenario"], state["trace"])
        return state

    def _graph_retrieve_schema(self, state: AgentState) -> AgentState:
        state["schema"] = self._retrieve_schema(state["trace"])
        return state

    def _graph_generate_sql(self, state: AgentState) -> AgentState:
        sql = self._generate_sql(
            state["question"],
            state["scenario"],
            state["schema"],
            state["intent"],
            state["trace"],
        )
        state["sql"] = sql
        state["result"].sql = sql
        return state

    def _graph_validate_sql(self, state: AgentState) -> AgentState:
        safety = self._validate_sql(state["sql"], state["trace"])
        state["safety"] = safety
        state["result"].safety = safety.to_dict()
        if not safety.is_safe:
            state["result"].sql = state["sql"]
            state["result"].safe_sql = None
            state["result"].error = "; ".join(safety.errors) or "SQL安全校验未通过"
        else:
            state["result"].safe_sql = safety.safe_sql
        return state

    def _graph_after_validate(self, state: AgentState) -> str:
        return "execute" if state["safety"].is_safe else "end"

    def _graph_execute_sql(self, state: AgentState) -> AgentState:
        state["attempt"] = int(state.get("attempt", 0)) + 1
        try:
            query_result = self._execute_sql(state["safety"].safe_sql or state["sql"], state["trace"])
            result = state["result"]
            result.columns = list(query_result.get("columns") or [])
            result.rows = [dict(row) for row in query_result.get("rows") or []]
            result.row_count = int(query_result.get("row_count", len(result.rows)))
            result.sql = state["sql"]
            result.error = None
            state["execution_ok"] = True
            state["last_error"] = None
        except Exception as exc:
            last_error = str(exc)
            state["execution_ok"] = False
            state["last_error"] = last_error
            state["trace"].append(
                {
                    "node": "execute_sql",
                    "status": "error",
                    "error": last_error,
                    "attempt": state["attempt"],
                }
            )
            if state["attempt"] > self.max_retries:
                state["result"].error = f"SQL执行失败，已重试{self.max_retries}次：{last_error}"
        return state

    def _graph_after_execute(self, state: AgentState) -> str:
        if state.get("execution_ok"):
            return "profile"
        return "repair" if int(state.get("attempt", 0)) <= self.max_retries else "end"

    def _graph_repair_sql(self, state: AgentState) -> AgentState:
        sql = self._repair_sql(
            state["question"],
            state["scenario"],
            state["schema"],
            state["sql"],
            state.get("last_error") or "",
            state["trace"],
        )
        state["sql"] = sql
        state["result"].sql = sql
        return state

    def _graph_profile_result(self, state: AgentState) -> AgentState:
        self._profile_result(state["result"], state["trace"])
        return state

    def _graph_decide_chart_search_compute(self, state: AgentState) -> AgentState:
        self._decide_chart_search_compute(state["result"], state["trace"])
        return state

    def _graph_analyze(self, state: AgentState) -> AgentState:
        state["result"].analysis = self._analyze(
            state["question"],
            state["scenario"],
            state["result"],
            state["trace"],
        )
        return state

    def _graph_compose_report(self, state: AgentState) -> AgentState:
        state["result"].report = self._compose_report(state["result"], state["trace"])
        return state

    def _graph_reflect_quality(self, state: AgentState) -> AgentState:
        self._reflect_quality(state["result"], state["trace"])
        state["result"].success = True
        state["result"].error = None
        return state

    def _classify_intent(self, question: str, scenario: str, trace: list[dict[str, Any]]) -> dict[str, Any]:
        intent = {"scenario": scenario, "needs_report": True}
        trace.append({"node": "classify_intent", "status": "ok", "intent": intent})
        return intent

    def _retrieve_schema(self, trace: list[dict[str, Any]]) -> str:
        schema = self.profile.load_schema()
        trace.append({"node": "retrieve_schema", "status": "ok", "profile": self.profile.name})
        return schema

    def _generate_sql(
        self,
        question: str,
        scenario: str,
        schema: str,
        intent: dict[str, Any],
        trace: list[dict[str, Any]],
    ) -> str:
        prompt = f"""你是一个严谨的 MySQL Text2SQL 专家。

## 当前数据库专用指南
{self.profile.sql_guidance}

## 数据库Schema和规则
{schema[:12000]}

## 场景
{scenario}

## 用户问题
{question}

## 强制要求
1. 只返回一条MySQL SELECT语句，不要解释，不要Markdown代码块。
2. 所有中文表名、视图名、特殊字段名必须使用反引号。
3. 优先使用兼容视图：`企业行业代码`、`融资数据`、`投资数据`、`招投标`、`标签数据`。
4. 禁止 SELECT *，必须明确列名。
5. 必须在SQL端聚合，避免拉取大量原始数据。
6. 必须包含 LIMIT，除非是 COUNT/SUM 这类单行聚合。
7. 输出前自检：所有字段必须存在于 Schema；所有表必须在白名单；不要把子查询别名当表；不要使用库中不存在的中文名称字段。
"""
        sql = self.llm.complete([{"role": "user", "content": prompt}], temperature=0.1, max_tokens=1500)
        trace.append({"node": "generate_sql", "status": "ok"})
        return self._apply_question_sql_constraints(self._strip_markdown(sql), question, scenario)

    def _validate_sql(self, sql: str, trace: list[dict[str, Any]]) -> SafeSQLReport:
        report = enforce_safe_sql(
            sql,
            allowed_tables=self.profile.allowed_tables,
            max_limit=self.max_limit,
        )
        trace.append(
            {
                "node": "validate_sql",
                "status": "ok" if report.is_safe else "rejected",
                "errors": list(report.errors),
                "modifications": list(report.modifications),
            }
        )
        return report

    def _execute_sql(self, sql: str, trace: list[dict[str, Any]]) -> dict[str, Any]:
        result = self.sql_executor(sql)
        trace.append({"node": "execute_sql", "status": "ok", "row_count": result.get("row_count", 0)})
        return result

    def _repair_sql(
        self,
        question: str,
        scenario: str,
        schema: str,
        sql: str,
        error: str,
        trace: list[dict[str, Any]],
    ) -> str:
        prompt = f"""SQL执行失败，请根据错误和Schema修复。

## 用户问题
{question}

## 场景
{scenario}

## 原SQL
{sql}

## 错误
{error}

## Schema
{schema[:12000]}

## 当前数据库专用指南
{self.profile.sql_guidance}

## 修复要求
1. 只修复为一条 MySQL SELECT。
2. 如果错误是 Unknown column，必须换成 Schema 中真实存在的字段。
3. 如果错误是非白名单表，必须改用白名单表或兼容视图。
4. 如果是企业详情类查询，优先使用企业主表 + 聚合子查询，避免多事实表直接 JOIN 放大行数。

只返回修复后的SQL，不要解释，不要Markdown代码块。
"""
        repaired = self.llm.complete([{"role": "user", "content": prompt}], temperature=0.1, max_tokens=1500)
        trace.append({"node": "repair_sql", "status": "ok", "error": error})
        return self._apply_question_sql_constraints(self._strip_markdown(repaired), question, scenario)

    def _profile_result(self, result: AgentResult, trace: list[dict[str, Any]]) -> None:
        trace.append({"node": "profile_result", "status": "ok", "rows": result.row_count, "columns": result.columns})

    def _decide_chart_search_compute(self, result: AgentResult, trace: list[dict[str, Any]]) -> None:
        result.chart = self._infer_chart(result)
        trace.append({"node": "decide_chart_search_compute", "status": "ok", "chart": result.chart})

    def _analyze(self, question: str, scenario: str, result: AgentResult, trace: list[dict[str, Any]]) -> str:
        if result.row_count == 0:
            analysis = "查询结果为空。请在报告中说明当前数据库没有返回对应数据，不要编造结论。"
            trace.append({"node": "analyze", "status": "empty"})
            return analysis

        preview = result.rows[:10]
        prompt = f"""你是地区产业发展分析专家。请基于真实查询结果生成简洁专业的数据解读。

问题：{question}
场景：{scenario}
SQL：{result.safe_sql}
字段：{result.columns}
行数：{result.row_count}
数据预览：{preview}

要求：
1. 所有结论必须基于数据预览和行数，不得编造。
2. 如果只看到预览数据，明确使用“当前返回结果显示”。
3. 输出Markdown，包含“核心发现”和“分析局限性”。
"""
        analysis = self.llm.complete([{"role": "user", "content": prompt}], temperature=0.2, max_tokens=1500)
        trace.append({"node": "analyze", "status": "ok"})
        analysis = analysis.strip()
        if not analysis:
            trace.append({"node": "analyze", "status": "fallback_empty_llm"})
            return self._fallback_analysis(result)
        return analysis

    def _compose_report(self, result: AgentResult, trace: list[dict[str, Any]]) -> str:
        rows_md = self._rows_to_markdown(result.columns, result.rows[:20])
        report = f"""# Text2SQL 分析报告

生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 用户问题
{result.question}

## 安全SQL
```sql
{result.safe_sql or ""}
```

## 查询结果
共返回 {result.row_count} 行。

{rows_md}

## 数据分析
{result.analysis}

## 安全校验
- 白名单表：{", ".join((result.safety or {}).get("referenced_tables", []))}
- 自动改写：{", ".join((result.safety or {}).get("modifications", [])) or "无"}
"""
        trace.append({"node": "compose_report", "status": "ok"})
        return report

    def _reflect_quality(self, result: AgentResult, trace: list[dict[str, Any]]) -> None:
        trace.append(
            {
                "node": "reflect_quality",
                "status": "ok",
                "notes": "empty result disclosed" if result.row_count == 0 else "result grounded in SQL output",
            }
        )

    @staticmethod
    def _strip_markdown(sql: str) -> str:
        cleaned = sql.strip()
        cleaned = re.sub(r"^```(?:sql)?", "", cleaned, flags=re.IGNORECASE).strip()
        cleaned = re.sub(r"```$", "", cleaned).strip()
        return cleaned

    @staticmethod
    def _is_single_company_detail_question(question: str, scenario: str) -> bool:
        if scenario != "due_diligence":
            return False
        keywords = ("一家", "单个", "某家", "企业详情", "基本信息")
        return any(keyword in question for keyword in keywords)

    def _apply_question_sql_constraints(self, sql: str, question: str, scenario: str) -> str:
        if self._is_single_company_detail_question(question, scenario):
            return self._force_limit(sql, 1)
        return sql

    @staticmethod
    def _force_limit(sql: str, limit: int) -> str:
        clean = sql.strip().rstrip(";")
        if re.search(r"\bLIMIT\s+\d+(?:\s*,\s*\d+)?\s*$", clean, re.IGNORECASE):
            return re.sub(
                r"\bLIMIT\s+\d+(?:\s*,\s*\d+)?\s*$",
                f"LIMIT {limit}",
                clean,
                flags=re.IGNORECASE,
            )
        return f"{clean} LIMIT {limit}"

    @staticmethod
    def _fallback_analysis(result: AgentResult) -> str:
        preview = result.rows[:3]
        return f"""### 核心发现

当前返回结果显示，本次查询返回 {result.row_count} 行，字段包括：{", ".join(result.columns)}。

数据预览：{preview}

### 分析局限性

模型分析返回为空，以上内容为系统基于 SQL 结果生成的兜底摘要；详细业务判断仍需结合完整结果、字段口径和外部背景进行复核。"""

    @staticmethod
    def _rows_to_markdown(columns: list[str], rows: list[dict[str, Any]]) -> str:
        if not rows:
            return "无数据。"
        header = "| " + " | ".join(columns) + " |"
        separator = "| " + " | ".join("---" for _ in columns) + " |"
        body = []
        for row in rows:
            body.append("| " + " | ".join(str(row.get(col, "")) for col in columns) + " |")
        return "\n".join([header, separator, *body])

    @staticmethod
    def _infer_chart(result: AgentResult) -> dict[str, Any] | None:
        if result.row_count == 0 or len(result.columns) < 2:
            return None
        numeric_cols = []
        for col in result.columns:
            if any(isinstance(row.get(col), (int, float, Decimal)) for row in result.rows[:20]):
                numeric_cols.append(col)
        if not numeric_cols:
            return None
        x_col = next((col for col in result.columns if col not in numeric_cols), result.columns[0])
        y_col = numeric_cols[0]
        chart_type = "line" if any(k in x_col.lower() for k in ("year", "date", "time", "年", "日期", "时间")) else "bar"
        return {"type": chart_type, "x": x_col, "y": y_col}

    @staticmethod
    def _build_sql_executor(db_config: dict[str, Any]) -> SQLExecutor:
        def execute(sql: str) -> dict[str, Any]:
            conn_params = {
                key: value
                for key, value in db_config.items()
                if key in {"host", "port", "user", "password", "database", "charset"} and value is not None
            }
            conn_params.setdefault("charset", "utf8mb4")
            conn = pymysql.connect(**conn_params)
            try:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    raw_rows = cursor.fetchall()
                    columns = [desc[0] for desc in cursor.description or []]
                rows = [dict(zip(columns, row)) for row in raw_rows]
                return {"columns": columns, "rows": rows, "row_count": len(rows)}
            finally:
                conn.close()

        return execute
