from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.agent.factory import build_agent_runtime

STANDARD_QUESTIONS = [
    ("01_经营状态", "统计企业经营状态分布", "data_insight"),
    ("02_行业Top", "按行业统计企业数量 Top 10", "industry"),
    ("03_融资轮次", "统计各融资轮次的企业数量和融资金额", "data_insight"),
    ("04_招投标年度", "按年份统计招投标数量", "data_insight"),
    ("05_资质年份", "统计商标资质的申请年份分布", "data_insight"),
    ("06_地区分布", "统计企业地区分布 Top 20", "regional"),
    ("07_成立趋势", "按成立年份统计企业数量趋势", "regional"),
    ("08_投资Top", "统计对外投资数量最多的企业 Top 10", "investment"),
    ("09_注册资本区间", "按注册资本区间统计企业数量", "data_insight"),
    ("10_企业详情", "查询一家企业的基本信息、融资、投资和招投标情况", "due_diligence"),
]


def json_default(value: Any) -> Any:
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    return str(value)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run znjz AgentRuntime acceptance questions."
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Output directory. Default: output/agent_acceptance_<timestamp>",
    )
    parser.add_argument(
        "--limit", type=int, default=None, help="Only run the first N questions."
    )
    args = parser.parse_args()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(args.output_dir or f"output/agent_acceptance_{timestamp}")
    output_dir.mkdir(parents=True, exist_ok=True)

    runtime = build_agent_runtime(profile_name="znjz", scenario_key="scenario_1_3")
    selected = STANDARD_QUESTIONS[: args.limit] if args.limit else STANDARD_QUESTIONS

    index_lines = [
        "# Text2SQL Agent znjz 验收记录",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- Workflow backend：{runtime.workflow_backend}",
        f"- 问题数量：{len(selected)}",
        "",
        "| 序号 | 问题 | 场景 | 状态 | 行数 | 产物 |",
        "|---|---|---|---|---:|---|",
    ]

    for name, question, scenario in selected:
        result = runtime.query(question, scenario=scenario)
        payload = result.to_dict()
        payload_path = output_dir / f"{name}.json"
        report_path = output_dir / f"{name}.md"

        payload_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, default=json_default),
            encoding="utf-8",
        )

        report = (
            result.report or f"# {question}\n\n执行失败：{result.error or '未知错误'}\n"
        )
        write_text(report_path, report)

        status = "success" if result.success else "failed"
        index_lines.append(
            f"| {name} | {question} | {scenario} | {status} | {result.row_count} | "
            f"[JSON]({payload_path.name}) / [报告]({report_path.name}) |"
        )

    write_text(output_dir / "index.md", "\n".join(index_lines) + "\n")
    print(output_dir.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
