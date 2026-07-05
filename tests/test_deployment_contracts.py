from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_env_example_documents_streamlit_and_ark_secrets():
    env_example = (REPO_ROOT / ".env.example").read_text(encoding="utf-8")

    for key in [
        "LLM_PROVIDER",
        "VOLCENGINE_ARK_BASE_URL",
        "VOLCENGINE_ARK_API_KEY",
        "VOLCENGINE_ARK_MODEL",
        "APP_PASSWORD",
        "DB_HOST_SCENARIO_1_3",
        "DB_NAME_SCENARIO_1_3=znjz",
    ]:
        assert key in env_example


def test_n8n_workflows_use_unified_agent_endpoint():
    workflow_paths = [
        REPO_ROOT / "n8n_workflow_text2sql.json",
        REPO_ROOT / "workflows" / "text2sql-query.json",
        REPO_ROOT / "workflows" / "industry-report.json",
    ]

    for path in workflow_paths:
        workflow = json.loads(path.read_text(encoding="utf-8"))
        workflow_text = json.dumps(workflow, ensure_ascii=False)
        assert "/api/agent/query" in workflow_text
        assert "/api/vanna/query" not in workflow_text
        assert "/api/v0/generate_sql" not in workflow_text
