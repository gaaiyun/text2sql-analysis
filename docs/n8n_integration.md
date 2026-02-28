# n8n 工作流集成指南（已更新：LLM主力+Vanna兜底）

本文档说明如何将 Text2SQL 与 n8n 集成：导入工作流、配置节点与凭证、测试方法。

## 前置条件

1. **Vanna 服务**运行在 `http://localhost:5000`
   - 启动：`python -m api.vanna_server` 或 `uvicorn api.vanna_server:app --host 0.0.0.0 --port 5000`
2. **API 服务**（可选，用于完整功能）运行在 `http://localhost:8000`
3. n8n 已安装并可访问

## 工作流导入步骤

1. 打开 n8n 界面，进入 **Workflows**
2. 点击 **Import from File** 或 **Import from URL**
3. 选择项目根目录下的 **`n8n_workflow_text2sql.json`**
4. 导入后工作流会包含以下节点（按执行顺序）：
   - **Webhook Trigger**：接收 POST 请求
   - **Task Classifier**：根据问题关键词识别场景（数据洞察/地区产业/行业分析/招商清单/尽调报告）
   - **Vanna SQL Generator**：调用 Vanna 服务 `POST /api/v0/generate_sql`
   - **Data Processor**：解析 SQL 结果，判断是否需要 LLM 分析
   - **LLM Analysis**：调用大模型做深度分析（需配置凭证）
   - **Markdown Formatter**：组装 Markdown 报告
   - **Response Webhook**：返回最终结果

## 节点配置说明

### Webhook Trigger

- **Path**: `text2sql`（可改）
- **Method**: POST
- 请求体示例：`{ "query": "分析近三年融资趋势" }` 或 `{ "body": { "query": "..." } }`
- 下游通过 `$json.query` 或 `$json.body.query` 获取用户问题

### Task Classifier（Code 节点）

- 从输入中取 `query` 或 `body.query` 作为 `originalQuery`
- 根据关键词匹配场景，输出 `originalQuery`、`scenario`（中文场景名）、`timestamp`

### Vanna SQL Generator（HTTP Request）

- **URL**: `http://localhost:5000/api/v0/generate_sql`
- **Method**: POST
- **Content-Type**: application/json
- **Body**:
  - `question`: 用户自然语言问题（来自 Task Classifier 的 `originalQuery`）
  - `scenario`: 场景标识（data_insight / regional / industry / investment / due_diligence）
  - `database`: 数据库键（scenario_1_3 或 scenario_4_5，招商/尽调用 4_5）
- 返回字段：`sql`、`question`、`scenario`、`confidence`、`error`（可选）

### LLM Analysis

- 需配置 **OpenAI 兼容 API** 凭证（如百炼、Kiro 等）
- 若使用百炼：在 n8n 中创建凭证，类型选 “OpenAI API”，填写 Base URL 与 API Key
- 节点中 `credentials.openAiApi` 指向该凭证的 ID

### Response Webhook

- 使用 **Respond to Webhook** 将 Markdown 或 JSON 返回给调用方
- 当前为 JSON 响应，包含 `output`（Markdown 文本）、`format`、`scenario`

## 凭证设置

1. **Vanna 服务**：无需在 n8n 中配置凭证，仅需保证 5000 端口可访问
2. **LLM（可选）**：
   - 类型：OpenAI API 兼容
   - Base URL：如 `https://coding.dashscope.aliyuncs.com/v1`（百炼）
   - API Key：从对应平台获取
   - 在 “LLM Analysis” 节点中选择该凭证

## 测试方法

### 1. 健康检查

```bash
curl http://localhost:5000/health
```

应返回 `{"status":"ok","vanna_initialized":true,...}`

### 2. 直接调用 Vanna 生成 SQL

```bash
curl -X POST http://localhost:5000/api/v0/generate_sql \
  -H "Content-Type: application/json" \
  -d "{\"question\":\"分析近三年融资趋势\",\"scenario\":\"data_insight\",\"database\":\"scenario_1_3\"}"
```

应返回包含 `sql` 字段的 JSON。

### 3. 在 n8n 中测试工作流

- 保存工作流后，打开 **Webhook Trigger** 节点，复制 “Test URL”
- 使用 Postman 或 curl 向该 URL 发送 POST：
  - Body (JSON): `{ "query": "分析近三年融资趋势" }`
- 检查执行结果：Data Processor 应得到 `sql`，LLM Analysis 输出分析内容，Response 返回完整报告

### 4. 场景与数据库对应关系

| 场景     | scenario 值      | database 值     |
|----------|------------------|-----------------|
| 数据洞察 | data_insight     | scenario_1_3    |
| 地区产业 | regional         | scenario_1_3    |
| 行业分析 | industry         | scenario_1_3    |
| 招商清单 | investment       | scenario_4_5    |
| 尽调报告 | due_diligence    | scenario_4_5    |

Vanna 服务会根据 `database` 在双库（Gaaiyun / gaaiyun_2）间切换连接。

## 故障排查

- **503 Vanna 服务未就绪**：检查 5000 端口进程、config.json 中 database.scenario_1_3 配置及 Vanna API Key
- **SQL 生成为空**：查看 Vanna 服务日志；可先运行 `scripts/train_vanna.py` 做一次训练
- **n8n 调用超时**：确认 n8n 与 Vanna 在同一网络或将 URL 改为可访问的 host
