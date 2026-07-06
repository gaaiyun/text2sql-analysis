from __future__ import annotations

from dataclasses import dataclass

import pytest

from src.agent.factory import db_config_from_mapping
from src.agent.llm import DeepSeekProvider, LLMSettings, VolcengineArkProvider
from src.agent.profiles import get_database_profile
from src.agent.runtime import AgentResult, AgentRuntime


def test_volcengine_provider_settings_from_env():
    settings = LLMSettings.from_mapping(
        {
            "LLM_PROVIDER": "volcengine_ark",
            "VOLCENGINE_ARK_BASE_URL": "https://ark.cn-beijing.volces.com/api/coding/v3",
            "VOLCENGINE_ARK_API_KEY": "test-key",
            "VOLCENGINE_ARK_MODEL": "glm-5.2",
        }
    )

    assert settings.provider == "volcengine_ark"
    assert settings.base_url == "https://ark.cn-beijing.volces.com/api/coding/v3"
    assert settings.api_key == "test-key"
    assert settings.model == "glm-5.2"

    provider = VolcengineArkProvider(
        settings=settings, client_factory=lambda **kwargs: kwargs
    )
    assert provider.client["base_url"] == settings.base_url
    assert provider.client["api_key"] == settings.api_key


def test_deepseek_provider_settings_from_env():
    settings = LLMSettings.from_mapping(
        {
            "LLM_PROVIDER": "deepseek",
            "DEEPSEEK_BASE_URL": "https://api.deepseek.com",
            "DEEPSEEK_API_KEY": "test-key",
            "DEEPSEEK_MODEL": "deepseek-v4-flash",
        }
    )

    assert settings.provider == "deepseek"
    assert settings.base_url == "https://api.deepseek.com"
    assert settings.api_key == "test-key"
    assert settings.model == "deepseek-v4-flash"

    provider = DeepSeekProvider(
        settings=settings, client_factory=lambda **kwargs: kwargs
    )
    assert provider.client["base_url"] == settings.base_url
    assert provider.client["api_key"] == settings.api_key


def test_db_config_from_streamlit_secret_names():
    db_config = db_config_from_mapping(
        {
            "DB_HOST_SCENARIO_1_3": "8.134.9.77",
            "DB_PORT_SCENARIO_1_3": "3306",
            "DB_NAME_SCENARIO_1_3": "znjz",
            "DB_USER_SCENARIO_1_3": "znjz",
            "DB_PASSWORD_SCENARIO_1_3": "secret",
        }
    )

    assert db_config == {
        "host": "8.134.9.77",
        "port": 3306,
        "user": "znjz",
        "password": "secret",
        "database": "znjz",
        "charset": "utf8mb4",
    }


def test_znjz_profile_exposes_schema_and_allowed_tables():
    profile = get_database_profile("znjz")

    assert profile.name == "znjz"
    assert "企业基本信息" in profile.allowed_tables
    assert "融资数据" in profile.allowed_tables
    assert "招投标" in profile.allowed_tables
    assert "企业详情" in profile.sql_guidance
    assert "禁止虚构字段" in profile.sql_guidance
    assert "高频字段地图" in profile.sql_guidance
    assert "容易写错的字段名" in profile.sql_guidance
    assert "industry_name" in profile.sql_guidance
    assert "company_name" in profile.sql_guidance
    assert "Text2SQL 必须遵守的查询规则" in profile.load_schema()


@dataclass
class FakeLLM:
    sql: str
    analysis: str = "基于查询结果，数据返回正常。"

    def complete(self, messages, *, temperature=0.1, max_tokens=1500):
        prompt = messages[-1]["content"]
        if "只返回修复后的SQL" in prompt:
            return self.sql
        if "只返回一条MySQL SELECT语句" in prompt:
            return self.sql
        return self.analysis


class CapturingLLM(FakeLLM):
    def __init__(self, sql: str):
        super().__init__(sql=sql)
        self.prompts = []

    def complete(self, messages, *, temperature=0.1, max_tokens=1500):
        self.prompts.append(messages[-1]["content"])
        return super().complete(
            messages, temperature=temperature, max_tokens=max_tokens
        )


def test_agent_runtime_generates_safe_sql_and_executes_with_limit():
    executed = {}

    def fake_executor(sql: str):
        executed["sql"] = sql
        return {
            "columns": ["status", "cnt"],
            "rows": [{"status": "存续（在营、开业、在册）", "cnt": 17477}],
            "row_count": 1,
        }

    runtime = AgentRuntime(
        profile=get_database_profile("znjz"),
        llm=FakeLLM(
            "SELECT `status`, COUNT(*) AS cnt FROM `企业基本信息` GROUP BY `status`"
        ),
        sql_executor=fake_executor,
    )

    result = runtime.query("统计企业经营状态分布", scenario="data_insight")

    assert result.success is True
    assert "LIMIT 1000" in result.safe_sql
    assert executed["sql"] == result.safe_sql
    assert result.rows[0]["cnt"] == 17477
    assert result.trace[-1]["node"] == "reflect_quality"


def test_generate_sql_prompt_contains_znjz_sql_guidance():
    def fake_executor(sql: str):
        return {"columns": ["cnt"], "rows": [{"cnt": 1}], "row_count": 1}

    llm = CapturingLLM("SELECT COUNT(*) AS cnt FROM `企业基本信息`")
    runtime = AgentRuntime(
        profile=get_database_profile("znjz"),
        llm=llm,
        sql_executor=fake_executor,
    )

    runtime.query(
        "查询一家企业的基本信息、融资、投资和招投标情况", scenario="due_diligence"
    )

    sql_prompt = llm.prompts[0]
    assert "禁止虚构字段" in sql_prompt
    assert "企业详情" in sql_prompt
    assert "`融资数据`" in sql_prompt
    assert "`投资数据`" in sql_prompt
    assert "`招投标`" in sql_prompt
    assert "高频字段地图" in sql_prompt
    assert "不要使用 `industry_name`" in sql_prompt
    assert "COUNT(DISTINCT `eid`)" in sql_prompt
    assert "企业详情必须先聚合子查询再 JOIN" in sql_prompt


def test_agent_runtime_rejects_non_whitelisted_tables_before_execution():
    def fake_executor(sql: str):
        raise AssertionError("unsafe SQL must not execute")

    runtime = AgentRuntime(
        profile=get_database_profile("znjz"),
        llm=FakeLLM("SELECT id FROM `users`"),
        sql_executor=fake_executor,
    )

    result = runtime.query("查一下用户表", scenario="data_insight")

    assert result.success is False
    assert result.safe_sql is None
    assert "非白名单" in result.error
    assert any(step["node"] == "validate_sql" for step in result.trace)


def test_agent_runtime_can_repair_sql_after_execution_error():
    attempts = []

    class RepairingLLM(FakeLLM):
        def complete(self, messages, *, temperature=0.1, max_tokens=1500):
            prompt = messages[-1]["content"]
            if "只返回修复后的SQL" in prompt:
                return "SELECT `industry_code`, COUNT(*) AS cnt FROM `企业行业代码` GROUP BY `industry_code`"
            return super().complete(
                messages, temperature=temperature, max_tokens=max_tokens
            )

    def fake_executor(sql: str):
        attempts.append(sql)
        if len(attempts) == 1:
            raise RuntimeError("Unknown column 'industry_name'")
        return {
            "columns": ["industry_code", "cnt"],
            "rows": [{"industry_code": "M7519", "cnt": 1877}],
            "row_count": 1,
        }

    runtime = AgentRuntime(
        profile=get_database_profile("znjz"),
        llm=RepairingLLM(
            "SELECT `industry_name`, COUNT(*) AS cnt FROM `企业行业代码` GROUP BY `industry_name`"
        ),
        sql_executor=fake_executor,
        max_retries=2,
    )

    result = runtime.query("统计行业分布", scenario="industry")

    assert result.success is True
    assert len(attempts) == 2
    assert "industry_code" in result.safe_sql
    assert any(step["node"] == "repair_sql" for step in result.trace)


def test_agent_runtime_empty_result_report_discloses_no_data():
    def fake_executor(sql: str):
        return {"columns": ["name", "cnt"], "rows": [], "row_count": 0}

    runtime = AgentRuntime(
        profile=get_database_profile("znjz"),
        llm=FakeLLM(
            "SELECT `name`, COUNT(*) AS cnt FROM `企业行业代码` GROUP BY `name`"
        ),
        sql_executor=fake_executor,
    )

    result = runtime.query("查询不存在的行业", scenario="industry")

    assert result.success is True
    assert result.row_count == 0
    assert "查询结果为空" in result.analysis
    assert "无数据" in result.report


def test_agent_runtime_caps_single_company_detail_query_to_one_row():
    executed = {}

    def fake_executor(sql: str):
        executed["sql"] = sql
        return {"columns": ["name"], "rows": [{"name": "测试企业"}], "row_count": 1}

    runtime = AgentRuntime(
        profile=get_database_profile("znjz"),
        llm=FakeLLM("SELECT `name` FROM `企业基本信息` LIMIT 1000"),
        sql_executor=fake_executor,
    )

    result = runtime.query(
        "查询一家企业的基本信息、融资、投资和招投标情况", scenario="due_diligence"
    )

    assert result.success is True
    assert result.safe_sql.endswith("LIMIT 1")
    assert executed["sql"].endswith("LIMIT 1")


def test_agent_runtime_uses_fallback_analysis_when_llm_returns_empty():
    def fake_executor(sql: str):
        return {"columns": ["name"], "rows": [{"name": "测试企业"}], "row_count": 1}

    runtime = AgentRuntime(
        profile=get_database_profile("znjz"),
        llm=FakeLLM("SELECT `name` FROM `企业基本信息` LIMIT 1", analysis=""),
        sql_executor=fake_executor,
    )

    result = runtime.query("查询一家企业详情", scenario="due_diligence")

    assert result.success is True
    assert "当前返回结果显示" in result.analysis
    assert "分析局限性" in result.analysis


def test_agent_result_serializes_public_api_contract():
    result = AgentResult(
        question="统计企业经营状态分布",
        scenario="data_insight",
        success=True,
        sql="SELECT 1",
        safe_sql="SELECT 1 LIMIT 1000",
        columns=["cnt"],
        rows=[{"cnt": 1}],
        row_count=1,
        analysis="ok",
        report="# ok",
        chart={"type": "bar"},
        safety={"is_safe": True},
        trace=[{"node": "reflect_quality"}],
    )

    payload = result.to_dict()

    assert payload["safe_sql"] == "SELECT 1 LIMIT 1000"
    assert payload["rows"] == [{"cnt": 1}]
    assert payload["analysis"] == "ok"
    assert payload["trace"][-1]["node"] == "reflect_quality"
