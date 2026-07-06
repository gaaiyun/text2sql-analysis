# scripts 目录说明

这个目录混合了当前维护脚本和历史兼容脚本。第一版 Streamlit Cloud + `znjz` Agent Runtime 只依赖当前维护脚本；legacy 脚本保留是为了兼容旧工作流和旧测试，不代表当前主路径。

新增脚本前先判断它属于哪一类：部署检查、验收、数据导入、一次性排查，还是 legacy 兼容。能写成测试的就优先写测试；确实需要脚本时，要在本文件登记用途和常用命令。

## 当前维护脚本

| 脚本 | 用途 | 常用命令 |
| --- | --- | --- |
| `check_streamlit_readiness.py` | 检查 Streamlit 部署入口、依赖、secrets 模板、`.gitignore` 和文档契约 | `python scripts/check_streamlit_readiness.py` |
| `run_agent_acceptance.py` | 用 `znjz` 跑 10 个标准验收问题，保存 JSON 和 Markdown 报告 | `python scripts/run_agent_acceptance.py` |
| `check_security.py` | 提交前敏感信息扫描 | `python scripts/check_security.py` |
| `test_db_simple.py` | 数据库连通性辅助检查 | `python scripts/test_db_simple.py` |

## Legacy / 兼容脚本

| 脚本 | 状态 |
| --- | --- |
| `train_vanna.py`、`train_vanna_simple.py`、`generate_vanna_training.py`、`setup_vanna_kiro.py` | Vanna/旧训练链路保留，非第一版强依赖 |
| `extract_schema.py`、`extract_schema_essential.py` | 早期 schema 提取辅助工具 |
| `export_excel.py`、`export_word.py`、`web_search.py` | 旧 API 周边能力，保留兼容 |
| `deploy.bat`、`deploy.sh`、`start_web.bat`、`start_web.sh` | 旧 Web/API 启动脚本，不用于 Streamlit Cloud |
| `test_quick.py`、`validate_sql.py`、`langchain_config.md` | 早期手动检查或配置记录 |

## 新脚本放置规则

- 不要把一次性脚本放到仓库根目录。
- 和 Streamlit 部署、Agent 验收、安全检查相关的脚本放在 `scripts/` 并登记到“当前维护脚本”。
- 只为迁移、排查或复现旧链路服务的脚本，优先放入 `scripts/legacy/` 或在表格里标注 legacy。
- 脚本不要写死 API Key、数据库密码、本机绝对路径或公网白名单信息。
- 脚本输出的报告、JSON 和截图默认放 `output/`，不要散落在根目录。

## 清理原则

不要直接删除 legacy 脚本。先确认：

1. 没有 README、docs 或测试引用它。
2. 旧入口不再需要兼容。
3. 对应测试已更新。
4. 全量 `python -m pytest -q` 通过。

确认后再移动到 `scripts/legacy/` 或删除。
