from __future__ import annotations

import os
from typing import Any

import pandas as pd
import streamlit as st

from src.agent.factory import build_agent_runtime


SECRET_KEYS = [
    "LLM_PROVIDER",
    "VOLCENGINE_ARK_BASE_URL",
    "VOLCENGINE_ARK_API_KEY",
    "VOLCENGINE_ARK_MODEL",
    "DEEPSEEK_BASE_URL",
    "DEEPSEEK_API_KEY",
    "DEEPSEEK_MODEL",
    "MODEL_TEMPERATURE",
    "APP_PASSWORD",
    "DB_HOST_SCENARIO_1_3",
    "DB_PORT_SCENARIO_1_3",
    "DB_NAME_SCENARIO_1_3",
    "DB_USER_SCENARIO_1_3",
    "DB_PASSWORD_SCENARIO_1_3",
]


SCENARIOS = {
    "数据洞察": "data_insight",
    "地区产业分析": "regional",
    "行业分析": "industry",
    "招商清单": "investment",
    "企业尽调": "due_diligence",
}


SAMPLE_QUESTIONS = [
    "统计企业经营状态分布",
    "按行业统计企业数量 Top 10",
    "统计各融资轮次的企业数量",
    "按年份统计招投标数量",
    "统计商标资质的申请年份分布",
    "统计企业地区分布 Top 20",
    "按成立年份统计企业数量趋势",
    "统计对外投资数量最多的企业 Top 10",
    "按注册资本区间统计企业数量",
    "查询一家企业的基本信息、融资、投资和招投标情况",
]


def get_secret_value(key: str, default: str = "") -> Any:
    try:
        value = st.secrets.get(key)
    except Exception:
        value = None
    if value is not None:
        return value
    return os.environ.get(key, default)


def collect_config() -> dict[str, Any]:
    return {key: get_secret_value(key) for key in SECRET_KEYS if get_secret_value(key, "") != ""}


@st.cache_resource(show_spinner=False)
def get_runtime(config_items: tuple[tuple[str, Any], ...]):
    config = dict(config_items)
    return build_agent_runtime(config, profile_name="znjz", scenario_key="scenario_1_3")


def require_password() -> bool:
    expected = str(get_secret_value("APP_PASSWORD", "") or "")
    if not expected:
        return True

    if st.session_state.get("authenticated"):
        return True

    with st.form("login_form"):
        password = st.text_input("访问口令", type="password")
        submitted = st.form_submit_button("进入")

    if submitted:
        if password == expected:
            st.session_state["authenticated"] = True
            st.rerun()
        st.error("访问口令错误")
    return False


def render_chart(chart: dict[str, Any] | None, rows: list[dict[str, Any]]) -> None:
    if not chart or not rows:
        return

    df = pd.DataFrame(rows)
    x_col = chart.get("x")
    y_col = chart.get("y")
    if x_col not in df.columns or y_col not in df.columns:
        return

    chart_df = df[[x_col, y_col]].dropna()
    if chart_df.empty:
        return

    chart_df = chart_df.set_index(x_col)
    if chart.get("type") == "line":
        st.line_chart(chart_df)
    else:
        st.bar_chart(chart_df)


def main() -> None:
    st.set_page_config(page_title="智能制造 Text2SQL Agent", layout="wide")
    st.title("智能制造 Text2SQL Agent")

    if not require_password():
        return

    with st.sidebar:
        scenario_label = st.selectbox("场景", list(SCENARIOS.keys()), index=0)
        sample = st.selectbox("样例问题", [""] + SAMPLE_QUESTIONS, index=0)
        st.caption("数据库：znjz")

    default_question = sample or "按行业统计企业数量 Top 10"

    with st.form("query_form"):
        question = st.text_area("问题", value=default_question, height=120)
        submitted = st.form_submit_button("查询", type="primary")

    if not submitted:
        return

    if not question.strip():
        st.warning("请输入问题")
        return

    config = collect_config()
    try:
        runtime = get_runtime(tuple(sorted(config.items())))
    except Exception as exc:
        st.error(f"Runtime 初始化失败：{exc}")
        return

    with st.spinner("查询中..."):
        result = runtime.query(question.strip(), scenario=SCENARIOS[scenario_label])

    if not result.success:
        st.error(result.error or "查询失败")
        with st.expander("Trace", expanded=False):
            st.json(result.trace)
        if result.safety:
            with st.expander("安全报告", expanded=True):
                st.json(result.safety)
        return

    left, right = st.columns([1, 1])
    left.metric("返回行数", result.row_count)
    right.metric("工作流", runtime.workflow_backend)

    tab_report, tab_data, tab_sql, tab_trace = st.tabs(["报告", "数据", "SQL", "Trace"])

    with tab_report:
        st.markdown(result.analysis or "无分析内容")
        render_chart(result.chart, result.rows)
        st.download_button(
            "下载 Markdown",
            data=result.report,
            file_name="text2sql_report.md",
            mime="text/markdown",
        )

    with tab_data:
        st.dataframe(pd.DataFrame(result.rows), use_container_width=True, hide_index=True)

    with tab_sql:
        st.code(result.safe_sql or result.sql or "", language="sql")
        if result.safety:
            st.json(result.safety)

    with tab_trace:
        st.json(result.trace)


if __name__ == "__main__":
    main()
