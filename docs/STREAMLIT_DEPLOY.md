# Streamlit Cloud 部署说明

## 入口

- 应用入口：`streamlit_app.py`
- 运行命令：`streamlit run streamlit_app.py`
- 主要数据库 profile：`znjz`
- 主要 API：`POST /api/agent/query`
- 默认 LLM provider：`volcengine_ark`
- 备用 LLM provider：`deepseek`

## 架构

```mermaid
flowchart LR
    User["用户浏览器"] --> Streamlit["Streamlit UI"]
    N8N["n8n Workflow"] --> API["FastAPI /api/agent/query"]
    Demo["旧 Demo / Pipeline"] --> Runtime["AgentRuntime"]
    Streamlit --> Runtime
    API --> Runtime
    Runtime --> Profile["DatabaseProfile: znjz"]
    Runtime --> SafeSQL["safe_sql.enforce_safe_sql"]
    Runtime --> LLM["OpenAI-compatible LLM Provider"]
    Runtime --> MySQL["MySQL znjz"]
    LLM --> Ark["Volcengine Ark glm-5.2"]
    LLM -. optional .-> DeepSeek["DeepSeek fallback"]
    Profile --> Schema["schema/znjz_text2sql_schema.md"]
```

## Agent 状态图

```mermaid
stateDiagram-v2
    [*] --> classify_intent
    classify_intent --> retrieve_schema
    retrieve_schema --> generate_sql
    generate_sql --> validate_sql
    validate_sql --> execute_sql: safe
    validate_sql --> [*]: rejected
    execute_sql --> profile_result: success
    execute_sql --> repair_sql: error and retries remain
    execute_sql --> [*]: error after 2 retries
    repair_sql --> validate_sql
    profile_result --> decide_chart_search_compute
    decide_chart_search_compute --> analyze
    analyze --> compose_report
    compose_report --> reflect_quality
    reflect_quality --> [*]
```

## Streamlit Cloud 配置

1. 将仓库同步到 GitHub。
2. 在 Streamlit Cloud 新建应用，选择本仓库和 `streamlit_app.py`。
3. 在 Advanced settings 的 Secrets 中填写以下配置：

```toml
LLM_PROVIDER = "volcengine_ark"
VOLCENGINE_ARK_BASE_URL = "https://ark.cn-beijing.volces.com/api/coding/v3"
VOLCENGINE_ARK_API_KEY = "your-volcengine-ark-api-key-here"
VOLCENGINE_ARK_MODEL = "glm-5.2"
MODEL_TEMPERATURE = "0.1"

# 可选备用 Provider。需要切换时把 LLM_PROVIDER 改成 "deepseek"。
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_API_KEY = "your-deepseek-api-key-here"
DEEPSEEK_MODEL = "deepseek-v4-flash"

APP_PASSWORD = "change-me"

DB_HOST_SCENARIO_1_3 = "your-db-host"
DB_PORT_SCENARIO_1_3 = "3306"
DB_NAME_SCENARIO_1_3 = "znjz"
DB_USER_SCENARIO_1_3 = "znjz"
DB_PASSWORD_SCENARIO_1_3 = "your-db-password"
```

## 安全要求

- 不提交 `.streamlit/secrets.toml`、`.env`、`config.json`。
- 生产部署前轮换任何曾在聊天、日志或截图中出现过的 API Key。
- 第一版使用 `APP_PASSWORD` 做简单访问口令，不做账号体系。
- Streamlit Cloud 没有稳定固定出口 IP 时，需要临时允许其访问 MySQL；后续建议改为数据库代理或云数据库白名单方案。

## 本地验证

```bash
python -m pytest tests/test_safe_sql.py tests/test_agent_runtime.py tests/test_api_agent_endpoint.py tests/test_deployment_contracts.py -q
python -m py_compile src/agent/llm.py src/agent/profiles.py src/agent/factory.py src/agent/runtime.py api_server.py streamlit_app.py demo/text2sql_utils.py
```

## Provider 切换

- 火山方舟：`LLM_PROVIDER=volcengine_ark`，使用 `VOLCENGINE_ARK_*` 配置。
- DeepSeek：`LLM_PROVIDER=deepseek`，使用 `DEEPSEEK_*` 配置。
- 两者都通过 OpenAI-compatible Chat Completions 调用，应用代码不直接依赖特定厂商 SDK。

## 参考链接

- Streamlit Community Cloud secrets: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management
- 火山方舟兼容 OpenAI SDK: https://www.volcengine.com/docs/82379/1330626
- DeepSeek API first call: https://api-docs.deepseek.com/
