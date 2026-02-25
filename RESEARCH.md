# 🗂️ Text2SQL 项目调研报告

> **创建时间**: 2026-02-26  
> **调研者**: 派蒙 ⭐  
> **项目位置**: `C:\Users\gaaiy\Desktop\text2sql`

---

## 📋 目录

1. [工作流平台调研](#工作流平台调研)
2. [Text2SQL 开源项目调研](#text2sql-开源项目调研)
3. [AI Agent 框架调研](#ai-agent-框架调研)
4. [技术选型建议](#技术选型建议)
5. [开发计划](#开发计划)

---

## 🔍 工作流平台调研

### 1. n8n

**GitHub**: https://github.com/n8n-io/n8n  
**Stars**: 40k+  
**许可证**: Fair-code (Sustainable Use License)

#### 核心特性
- ✅ **可视化工作流编辑器** - Node-based UI
- ✅ **400+ 集成** - 数据库、API、SaaS 服务
- ✅ **AI-Native** - 基于 LangChain 的 AI 工作流
- ✅ **代码扩展** - JavaScript/Python 自定义代码
- ✅ **自托管** - Docker/npm 一键部署
- ✅ **企业级** - 高级权限、SSO、气隙部署

#### 部署方式
```bash
# npx 快速启动
npx n8n

# Docker 部署
docker volume create n8n_data
docker run -it --rm --name n8n -p 5678:5678 -v n8n_data:/home/node/.n8n docker.n8n.io/n8nio/n8n
```

#### Text2SQL 相关工作流
- 数据库查询自动化
- AI + SQL 生成
- API 到数据库的桥接

---

### 2. Dify

**GitHub**: https://github.com/langgenius/dify  
**类型**: AI 应用开发平台  
**特点**: LLM 应用编排、RAG、Agent 工作流

#### 核心特性
- ✅ **可视化编排** - LLM 应用工作流
- ✅ **RAG 引擎** - 知识库检索增强
- ✅ **Agent 框架** - 多 Agent 协作
- ✅ **API 发布** - 一键发布为 API
- ✅ **自托管** - Docker 部署

---

### 3. LangFlow

**GitHub**: https://github.com/langflow-ai/langflow  
**类型**: LangChain 可视化编辑器  
**特点**: 拖拽式 AI 工作流构建

#### 核心特性
- ✅ **拖拽界面** - 无需编码
- ✅ **LangChain 兼容** - 所有 LangChain 组件
- ✅ **Python 后端** - 易于扩展
- ✅ **快速原型** - 分钟级构建 AI 应用

---

## 🗄️ Text2SQL 开源项目调研

### 1. LangChain Text2SQL

**文档**: https://python.langchain.com/docs/use_cases/sql/

#### 核心组件
```python
from langchain.chains import SQLDatabaseChain
from langchain_community.utilities import SQLDatabase

db = SQLDatabase.from_uri("sqlite:///example.db")
chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)
```

#### 特性
- ✅ 支持多种数据库 (SQLite, PostgreSQL, MySQL, etc.)
- ✅ 自动 schema 提取
- ✅ SQL 验证和执行
- ✅ 结果格式化

---

### 2. Vanna AI

**GitHub**: https://github.com/vanna-ai/vanna  
**类型**: Text2SQL Python 库  
**特点**: 训练式 Text2SQL，支持 RAG

#### 核心特性
- ✅ **训练机制** - 用历史查询训练模型
- ✅ **RAG 支持** - 检索增强生成
- ✅ **多数据库** - PostgreSQL, Snowflake, BigQuery 等
- ✅ **Web UI** - 内置问答界面

#### 使用示例
```python
import vanna as vn

vn.train(question="What are the top customers?", sql="SELECT customer, SUM(amount) FROM orders GROUP BY customer")
vn.ask("Show me the top 5 customers")
```

---

### 3. Defog SQLCoder

**GitHub**: https://github.com/defog-ai/sqlcoder  
**类型**: Text2SQL 微调模型  
**特点**: 基于 StarCoder 微调，SOTA 性能

#### 模型版本
- **sqlcoder-7b** - 7B 参数，高精度
- **sqlcoder-34b** - 34B 参数，SOTA
- **sqlcoder-70b** - 70B 参数，最佳性能

#### 特性
- ✅ **开源模型** - HuggingFace 可下载
- ✅ **本地运行** - 无需 API
- ✅ **高精度** - 超越 GPT-4 在某些基准
- ✅ **多数据库** - PostgreSQL, MySQL, SQLite

---

### 4. Chat2DB

**GitHub**: https://github.com/chat2db/Chat2DB  
**类型**: 智能数据库客户端  
**特点**: Text2SQL + 数据库管理

#### 核心特性
- ✅ **Text2SQL** - 自然语言查询
- ✅ **数据库管理** - 连接管理、表结构
- ✅ **智能推荐** - SQL 自动补全
- ✅ **多数据库** - MySQL, PostgreSQL, Oracle, etc.
- ✅ **桌面应用** - Electron 跨平台

---

## 🤖 AI Agent 框架调研

### 1. LangChain Agents

**文档**: https://python.langchain.com/docs/modules/agents/

#### Agent 类型
- **Zero-shot ReAct** - 通用推理
- **SQL Agent** - 专门用于数据库查询
- **Tool-using Agents** - 使用自定义工具

#### SQL Agent 示例
```python
from langchain.agents import create_sql_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit

agent = create_sql_agent(llm=llm, toolkit=toolkit, verbose=True)
agent.run("List the top 10 customers by revenue")
```

---

### 2. Microsoft AutoGen

**GitHub**: https://github.com/microsoft/autogen  
**类型**: 多 Agent 协作框架

#### 核心特性
- ✅ **多 Agent 对话** - Agent 间自主协作
- ✅ **代码执行** - 自动执行生成的代码
- ✅ **人类参与** - 支持人类介入
- ✅ **灵活配置** - 自定义 Agent 角色

#### Text2SQL 应用场景
```python
# DBA Agent - 负责数据库查询
# Analyst Agent - 负责数据分析
# Validator Agent - 负责 SQL 验证

agents = [
    ConversableAgent("DBA_Agent"),
    ConversableAgent("Analyst_Agent"),
    ConversableAgent("Validator_Agent"),
]
```

---

### 3. CrewAI

**GitHub**: https://github.com/joaomdmoura/crewai  
**类型**: Agent 编排框架  
**特点**: 角色定义、任务分配、流程编排

#### 核心特性
- ✅ **角色定义** - 明确每个 Agent 的职责
- ✅ **任务编排** - 顺序/并行执行
- ✅ **工具集成** - 丰富的工具库
- ✅ **流程控制** - 条件分支、循环

---

## 🎯 技术选型建议

### 推荐架构

```
┌─────────────────────────────────────────────────────┐
│                  Text2SQL 工作流                      │
├─────────────────────────────────────────────────────┤
│  ┌─────────┐    ┌─────────┐    ┌─────────┐         │
│  │ 用户输入 │ →  │ LLM     │ →  │ SQL     │         │
│  │ (自然语言)│    │ (Qwen)  │    │ 生成器  │         │
│  └─────────┘    └─────────┘    └─────────┘         │
│                                  │                   │
│                                  ↓                   │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐         │
│  │ 结果返回 │ ←  │ 执行器  │ ←  │ SQL     │         │
│  │ (JSON)  │    │ (DB)    │    │ 验证器  │         │
│  └─────────┘    └─────────┘    └─────────┘         │
└─────────────────────────────────────────────────────┘
```

### 技术栈选择

| 组件 | 推荐方案 | 备选方案 |
|------|---------|---------|
| **工作流引擎** | n8n (自托管) | Dify / LangFlow |
| **LLM** | Qwen3.5 Plus (百炼) | Kimi K2.5 / MiniMax |
| **Text2SQL 框架** | LangChain SQL Agent | Vanna AI |
| **数据库** | SQLite (开发) / PostgreSQL (生产) | MySQL |
| **前端界面** | n8n Web UI | 自定义 Streamlit |
| **API 发布** | n8n Webhook | FastAPI |

---

## 📝 开发计划

### 阶段 1: 环境搭建 (Day 1)

- [ ] 安装 n8n (Docker/npm)
- [ ] 配置百炼 API (Qwen3.5 Plus)
- [ ] 设置开发数据库 (SQLite)
- [ ] 创建项目结构

### 阶段 2: 核心功能 (Day 2-3)

- [ ] LangChain SQL Agent 配置
- [ ] n8n 工作流设计
- [ ] Text2SQL 节点开发
- [ ] SQL 验证器实现

### 阶段 3: 测试优化 (Day 4-5)

- [ ] 单元测试
- [ ] 集成测试
- [ ] 性能优化
- [ ] 错误处理

### 阶段 4: 部署发布 (Day 6-7)

- [ ] Docker 容器化
- [ ] API 文档
- [ ] 用户手册
- [ ] 演示视频

---

## 📚 参考资源

### n8n 资源
- 官方文档：https://docs.n8n.io
- 工作流模板：https://n8n.io/workflows
- 社区论坛：https://community.n8n.io

### Text2SQL 资源
- LangChain SQL: https://python.langchain.com/docs/use_cases/sql/
- Vanna AI: https://github.com/vanna-ai/vanna
- SQLCoder: https://github.com/defog-ai/sqlcoder

### AI Agent 资源
- LangChain Agents: https://python.langchain.com/docs/modules/agents/
- AutoGen: https://github.com/microsoft/autogen
- CrewAI: https://github.com/joaomdmoura/crewai

---

_报告生成时间：2026-02-26 02:05_  
_调研者：派蒙 ⭐_
