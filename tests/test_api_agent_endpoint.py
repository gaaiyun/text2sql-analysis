from __future__ import annotations

from fastapi.testclient import TestClient

import api_server
from src.agent.runtime import AgentResult


class FakeRuntime:
    workflow_backend = "test"

    def query(self, question: str, *, scenario: str = "data_insight") -> AgentResult:
        return AgentResult(
            question=question,
            scenario=scenario,
            success=True,
            sql="SELECT `status`, COUNT(*) AS cnt FROM `企业基本信息` GROUP BY `status`",
            safe_sql="SELECT `status`, COUNT(*) AS cnt FROM `企业基本信息` GROUP BY `status` LIMIT 1000",
            columns=["status", "cnt"],
            rows=[{"status": "存续", "cnt": 1}],
            row_count=1,
            analysis="当前返回结果显示：存续企业 1 家。",
            report="# Text2SQL 分析报告",
            chart={"type": "bar", "x": "status", "y": "cnt"},
            safety={"is_safe": True},
            trace=[{"node": "reflect_quality", "status": "ok"}],
        )


def test_agent_query_endpoint_returns_runtime_payload(monkeypatch):
    monkeypatch.delenv("APP_PASSWORD", raising=False)
    monkeypatch.setattr(api_server, "get_agent_runtime", lambda: FakeRuntime())

    client = TestClient(api_server.app)
    response = client.post(
        "/api/agent/query",
        json={"question": "统计企业经营状态分布", "scenario": "data_insight"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["safe_sql"].endswith("LIMIT 1000")
    assert payload["rows"] == [{"status": "存续", "cnt": 1}]
    assert payload["analysis"]
    assert payload["trace"][-1]["node"] == "reflect_quality"


def test_agent_query_endpoint_rejects_wrong_password(monkeypatch):
    monkeypatch.setenv("APP_PASSWORD", "correct-password")
    monkeypatch.setattr(api_server, "get_agent_runtime", lambda: FakeRuntime())

    client = TestClient(api_server.app)
    response = client.post(
        "/api/agent/query",
        json={"question": "统计企业经营状态分布", "password": "wrong-password"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "访问口令错误"
