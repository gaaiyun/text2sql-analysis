from __future__ import annotations

import os
from collections.abc import Mapping
from typing import Any

from .llm import DeepSeekProvider, LLMSettings, VolcengineArkProvider
from .profiles import get_database_profile
from .runtime import AgentRuntime, SQLExecutor


def _get_value(source: Mapping[str, Any] | None, key: str, default: Any = "") -> Any:
    if source is not None and key in source:
        return source[key]
    return os.environ.get(key, default)


def db_config_from_mapping(
    source: Mapping[str, Any] | None = None,
    *,
    scenario_key: str = "scenario_1_3",
) -> dict[str, Any]:
    suffix = "SCENARIO_4_5" if scenario_key == "scenario_4_5" else "SCENARIO_1_3"
    port = _get_value(source, f"DB_PORT_{suffix}", 3306)
    return {
        "host": str(_get_value(source, f"DB_HOST_{suffix}", "localhost")),
        "port": int(port),
        "user": str(_get_value(source, f"DB_USER_{suffix}", "root")),
        "password": str(_get_value(source, f"DB_PASSWORD_{suffix}", "")),
        "database": str(_get_value(source, f"DB_NAME_{suffix}", "znjz" if suffix == "SCENARIO_1_3" else "")),
        "charset": "utf8mb4",
    }


def build_agent_runtime(
    source: Mapping[str, Any] | None = None,
    *,
    profile_name: str = "znjz",
    scenario_key: str = "scenario_1_3",
    llm: Any | None = None,
    sql_executor: SQLExecutor | None = None,
) -> AgentRuntime:
    profile = get_database_profile(profile_name)
    settings = LLMSettings.from_mapping(source)
    provider_cls = DeepSeekProvider if settings.provider == "deepseek" else VolcengineArkProvider
    provider = llm or provider_cls(settings=settings)
    return AgentRuntime(
        profile=profile,
        llm=provider,
        sql_executor=sql_executor,
        db_config=db_config_from_mapping(source, scenario_key=scenario_key),
    )
