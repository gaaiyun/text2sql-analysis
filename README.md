# 🗂️ Text2SQL 行业分析报告生成系统

> 基于 Vanna AI + n8n 的智能 Text2SQL 行业分析平台

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-green.svg)
![n8n](https://img.shields.io/badge/n8n-1.0+-orange.svg)
![Vanna AI](https://img.shields.io/badge/Vanna%20AI-0.5+-red.svg)

---

## 📋 目录

- [项目简介](#项目简介)
- [核心功能](#核心功能)
- [系统架构](#系统架构)
- [快速开始](#快速开始)
- [使用指南](#使用指南)
- [API 文档](#api 文档)
- [配置说明](#配置说明)
- [应用场景](#应用场景)
- [贡献指南](#贡献指南)
- [致谢](#致谢)
- [许可证](#许可证)

---

## 📖 项目简介

Text2SQL 行业分析报告生成系统是一个基于 **Vanna AI** 和 **n8n 工作流** 的智能数据分析平台。系统能够将自然语言转换为 SQL 查询，自动执行数据库查询，生成数据可视化图表，并输出完整的行业分析报告。

### ✨ 核心优势

- 🎯 **训练式 Text2SQL** - 基于 Vanna AI，越用越准确
- 🔄 **可视化工作流** - 基于 n8n，灵活编排数据处理流程
- 📊 **自动图表生成** - 基于 Plotly，智能选择图表类型
- 📄 **多格式输出** - 支持 Markdown、HTML、PDF、Excel 等格式
- 🔒 **企业级安全** - 支持行级权限、审计日志、速率限制

---

## 🚀 核心功能

### 1. 数据洞察 (场景 1)
以数据库查询为基础，融合互联网信息检索和知识库检索，对数据进行深度分析洞察。

**输出格式**: Markdown / HTML / 图文融合

### 2. 地区产业分析 (场景 2)
查询地区相关数据，分析地区总体经济发展情况、主导产业、龙头企业、新兴产业变化等。

**输出格式**: HTML 报告 (含图表)

### 3. 特定行业分析 (场景 3)
查询行业相关数据，分析企业数量增长趋势、技术发展方向、空间分布、龙头企业等。

**输出格式**: HTML 报告 (含图表)

### 4. 招商清单生成 (场景 4)
用户提供企业清单，查询企业详细信息（注册资本、所属行业、知识产权、诉讼情况等），进行评估筛选。

**输出格式**: Excel (评估维度 + 综合评分)

### 5. 企业尽调报告 (场景 5)
给定企业，查询全维度信息，生成尽调报告。

**输出格式**: Word (含数据图表和表格)

---

## 🏗️ 系统架构

```
┌────────────────────────────────────────────────────────────┐
│                    Text2SQL 分析系统                        │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐                │
│  │ 用户输入 │ →  │ n8n     │ →  │ Vanna   │                │
│  │ (自然语言)│    │ Webhook │    │ Text2SQL│                │
│  └─────────┘    └─────────┘    └─────────┘                │
│                                    │                        │
│                                    ↓                        │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐                │
│  │ 报告导出 │ ←  │ 图表生成 │ ←  │ SQL     │                │
│  │ (PDF/HTML)│    │ (Plotly)│    │ 执行    │                │
│  └─────────┘    └─────────┘    └─────────┘                │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

### 技术栈

| 组件 | 技术 | 说明 |
|------|------|------|
| **Text2SQL 引擎** | Vanna AI | 训练式 Text2SQL，支持 RAG |
| **工作流引擎** | n8n | 可视化工作流编排 |
| **LLM** | Qwen3.5 Plus (百炼) | 通义千问，中文优化 |
| **数据库** | MySQL / PostgreSQL | 支持多种数据库 |
| **图表库** | Plotly | 交互式图表生成 |
| **报告模板** | Jinja2 | HTML/PDF 模板引擎 |

---

## 📦 快速开始

### 1. 环境要求

- Python 3.10+
- Node.js 18+
- MySQL / PostgreSQL
- n8n (自托管或 Cloud)

### 2. 安装依赖

```bash
# 安装 Vanna AI
pip install vanna
pip install vanna[mysql]  # 或 vanna[postgres]

# 安装其他依赖
pip install plotly pandas jinja2 weasyprint
```

### 3. 配置环境变量

```bash
# 复制配置模板
cp .env.example .env

# 编辑配置文件，填入你的 API Key 和数据库信息
vim .env
```

### 4. 部署 Vanna API 服务

```bash
# 启动 Vanna API 服务
python api_server.py
```

### 5. 导入 n8n 工作流

1. 登录 n8n 管理界面
2. 进入 Settings → Workflows
3. 点击 Import
4. 选择 `workflows/text2sql-query.json` 或 `workflows/industry-report.json`
5. 激活工作流

### 6. 测试查询

```bash
# 发送测试请求
curl -X POST http://localhost:5678/webhook/text2sql-query \
  -H "Content-Type: application/json" \
  -d '{"question": "查询注册资本大于 1000 万的企业"}'
```

---

## 📖 使用指南

### 基础查询

```python
import requests

response = requests.post(
    'http://localhost:5678/webhook/text2sql-query',
    json={'question': '2026 年 2 月新增企业数量是多少？'}
)

print(response.text)
```

### 生成行业报告

```python
response = requests.post(
    'http://localhost:5678/webhook/industry-report',
    json={
        'question': '生成 2026 年 2 月电子产品行业分析报告',
        'generate_chart': True
    }
)

# 保存 HTML 报告
with open('report.html', 'w') as f:
    f.write(response.text)
```

### 训练 Vanna AI

```python
import vanna as vn

# 配置 Vanna
vn.setup(api_key='your-api-key', model='qwen-plus')

# 训练数据
vn.train(
    question="查询所有企业的基本信息",
    sql="SELECT name, format_name, regist_capi FROM 企业信息表 LIMIT 10"
)

vn.train(
    question="查询企业的知识产权信息",
    sql="SELECT 专利数量，商标数量 FROM 企业标签 WHERE eid = 'xxx'"
)
```

---

## 🔌 API 文档

### Text2SQL 查询接口

**端点**: `POST /webhook/text2sql-query`

**请求体**:
```json
{
  "question": "查询注册资本大于 1000 万的企业"
}
```

**响应**:
```markdown
| 企业名称 | 注册资本 | 成立日期 | 状态 |
|----------|---------|---------|------|
| XX 公司 | 5000 万 | 2020-01-01 | 存续 |
```

### 行业报告接口

**端点**: `POST /webhook/industry-report`

**请求体**:
```json
{
  "question": "生成 2026 年 2 月电子产品行业分析报告",
  "generate_chart": true
}
```

**响应**: HTML 报告

---

## ⚙️ 配置说明

### 环境变量 (.env)

```bash
# Vanna AI 配置
VANNA_API_KEY=your_api_key_here
VANNA_MODEL=qwen-plus

# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=your_database

# n8n 配置
N8N_WEBHOOK_URL=http://localhost:5678/webhook

# 百炼 API 配置
DASHSCOPE_API_KEY=your_dashscope_key
```

### n8n 工作流配置

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `httpMethod` | Webhook 方法 | POST |
| `path` | Webhook 路径 | text2sql-query |
| `responseMode` | 响应模式 | lastNode |

---

## 🎯 应用场景

### 场景 1: 数据洞察
- **输入**: "2026 年 2 月销售额趋势如何？"
- **输出**: Markdown 数据报告 + 折线图

### 场景 2: 地区产业分析
- **输入**: "分析深圳市的产业结构"
- **输出**: HTML 报告 (含柱状图、饼图)

### 场景 3: 特定行业分析
- **输入**: "分析新能源汽车行业发展趋势"
- **输出**: HTML 报告 (含趋势图、竞争格局图)

### 场景 4: 招商清单
- **输入**: [企业清单 Excel]
- **输出**: Excel 评估报告 (含综合评分)

### 场景 5: 企业尽调
- **输入**: "生成 XX 公司尽调报告"
- **输出**: Word 尽调报告 (含财务图表)

---

## 🤝 贡献指南

欢迎贡献！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 🙏 致谢

本项目参考和使用了以下优秀的开源项目：

### 核心依赖

- **[Vanna AI](https://github.com/vanna-ai/vanna)** - 🤖 Chat with your SQL database via LLMs
  - License: MIT
  - 感谢 Vanna 团队提供的强大 Text2SQL 框架

- **[n8n](https://github.com/n8n-io/n8n)** - Fair-code workflow automation platform
  - License: Sustainable Use License
  - 感谢 n8n 团队提供的可视化工作流引擎

- **[LangChain](https://github.com/langchain-ai/langchain)** - 🦜🔗 The platform for reliable agents
  - License: MIT
  - 感谢 LangChain 团队的 Agent 框架启发

- **[Plotly](https://github.com/plotly/plotly.py)** - Interactive browser-based graphs for Python
  - License: MIT
  - 感谢 Plotly 团队提供的图表库

### 模型提供商

- **[阿里云百炼](https://bailian.console.aliyun.com/)** - Qwen3.5 Plus 模型支持
- **[通义千问](https://tongyi.aliyun.com/)** - 中文 LLM 支持

### 社区资源

- **[n8n 工作流社区](https://n8n.io/workflows/)** - 8464+ 工作流模板
- **[Vanna AI 文档](https://vanna.ai/docs/)** - 完整的 Vanna 使用指南

---

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

## 📞 联系方式

- **项目作者**: gaaiyun
- **项目链接**: https://github.com/gaaiyun/text2sql-analysis
- **问题反馈**: https://github.com/gaaiyun/text2sql-analysis/issues

---

## ⭐ 支持项目

如果这个项目对你有帮助，请给一个 ⭐ Star！

---

_最后更新：2026-02-26_
