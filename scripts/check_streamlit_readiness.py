from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path

REQUIRED_SECRET_KEYS = (
    "LLM_PROVIDER",
    "VOLCENGINE_ARK_BASE_URL",
    "VOLCENGINE_ARK_API_KEY",
    "VOLCENGINE_ARK_MODEL",
    "APP_PASSWORD",
    "DB_HOST_SCENARIO_1_3",
    "DB_PORT_SCENARIO_1_3",
    "DB_NAME_SCENARIO_1_3",
    "DB_USER_SCENARIO_1_3",
    "DB_PASSWORD_SCENARIO_1_3",
)

REQUIRED_FILES = (
    "streamlit_app.py",
    "requirements.txt",
    "schema/znjz_text2sql_schema.md",
    "docs/STREAMLIT_DEPLOY.md",
    ".streamlit/secrets.toml.example",
)

REQUIRED_REQUIREMENTS = ("streamlit", "langgraph", "openai", "pymysql")


@dataclass(frozen=True)
class CheckResult:
    name: str
    ok: bool
    detail: str


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def run_checks(repo_root: Path) -> list[CheckResult]:
    repo_root = repo_root.resolve()
    results: list[CheckResult] = []

    for rel_path in REQUIRED_FILES:
        path = repo_root / rel_path
        results.append(
            CheckResult(
                name=f"file:{rel_path}",
                ok=path.exists(),
                detail="exists" if path.exists() else "missing",
            )
        )

    gitignore = _read(repo_root / ".gitignore")
    for pattern in (".streamlit/secrets.toml", ".env", "output/"):
        results.append(
            CheckResult(
                name=f"gitignore:{pattern}",
                ok=pattern in gitignore,
                detail="ignored" if pattern in gitignore else "not ignored",
            )
        )

    requirements = _read(repo_root / "requirements.txt").lower()
    for package in REQUIRED_REQUIREMENTS:
        results.append(
            CheckResult(
                name=f"requirement:{package}",
                ok=package in requirements,
                detail="declared" if package in requirements else "missing",
            )
        )

    secret_template = _read(repo_root / ".streamlit" / "secrets.toml.example")
    deploy_doc = _read(repo_root / "docs" / "STREAMLIT_DEPLOY.md")
    env_example = _read(repo_root / ".env.example")
    for key in REQUIRED_SECRET_KEYS:
        present = key in secret_template and key in deploy_doc and key in env_example
        results.append(
            CheckResult(
                name=f"secret:{key}",
                ok=present,
                detail="documented" if present else "missing from template/doc/env",
            )
        )

    deployment_doc_requirements = {
        "deploy_branch_main": "Branch 选择 `main`",
        "deploy_entrypoint_no_leading_slash": "不要填写 `/streamlit_app.py`",
        "deploy_mermaid_flow": "flowchart TD",
    }
    for name, required_text in deployment_doc_requirements.items():
        results.append(
            CheckResult(
                name=name,
                ok=required_text in deploy_doc,
                detail="documented" if required_text in deploy_doc else "missing",
            )
        )

    local_secret = repo_root / ".streamlit" / "secrets.toml"
    results.append(
        CheckResult(
            name="local_secret_not_committed",
            ok=not local_secret.exists(),
            detail="absent" if not local_secret.exists() else "present locally",
        )
    )

    streamlit_source = _read(repo_root / "streamlit_app.py")
    for key in REQUIRED_SECRET_KEYS:
        results.append(
            CheckResult(
                name=f"streamlit_reads:{key}",
                ok=key in streamlit_source,
                detail="read by app" if key in streamlit_source else "not read by app",
            )
        )

    return results


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check Streamlit Cloud deployment readiness without reading real secrets."
    )
    parser.add_argument(
        "--repo-root",
        default=str(Path(__file__).resolve().parents[1]),
        help="Repository root. Defaults to this script's parent repo.",
    )
    parser.add_argument(
        "--json", action="store_true", help="Print machine-readable JSON."
    )
    args = parser.parse_args()

    results = run_checks(Path(args.repo_root))
    if args.json:
        print(
            json.dumps(
                [asdict(result) for result in results], ensure_ascii=False, indent=2
            )
        )
    else:
        for result in results:
            status = "PASS" if result.ok else "FAIL"
            print(f"[{status}] {result.name}: {result.detail}")

    return 0 if all(result.ok for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
