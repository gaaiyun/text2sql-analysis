# Text2SQL 多工作流协作智能体系统

<div align="center">

**基于 LLM 的自然语言到 SQL 查询生成与智能报告系统**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![阿里云百炼](https://img.shields.io/badge/阿里云百炼-Coding_Plan-orange.svg)](https://dashscope.console.aliyun.com/)

[快速开始](#快速开始) • [功能特性](#功能特性) • [技术架构](#技术架构) • [使用文档](#使用文档) • [API文档](#api文档)

</div>

---

## 📖 项目简介

Text2SQL 是一个企业级的自然语言到 SQL 查询生成系统，能够将用户的自然语言问题自动转换为 SQL 查询，执行查询后生成包含数据分析、图表可视化和网络信息补充的多模态智能报告。

**最新更新 (v2.2)**:
- ✅ 专业化Web界面（移除emoji，现代化设计）
- ✅ 图表优化（专业配色，高清输出，正确嵌入文档）
- ✅ Word/PDF文档格式修复（正确解析Markdown）
- ✅ 智能网络搜索（LLM提取关键词，时间范围优化）
- ✅ SQL质量提升（清理双逗号，优化字段命名）

### 核心价值

- **零 SQL 门槛**：业务人员无需编写 SQL，用自然语言即可查询数据
- **智能分析**：自动生成数据洞察、趋势分析和业务建议
- **多模态输出**：支持 Markdown、PDF、Excel、Word 等多种格式
- **企业级应用**：支持 5 大业务场景，覆盖数据洞察、产业分析、招商清单、企业尽调等

### 应用场景

| 场景 | 功能描述 | 输出格式 | 适用对象 |
|------|---------|---------|---------|
| **场景1：数据洞察** | 融资趋势、行业分布、地区分析等数据洞察 | Markdown + PDF + 图表 | 投资分析师、数据分析师 |
| **场景2：地区产业分析** | 地区经济、主导产业、龙头企业、投资来源分析 | Markdown + PDF + 图表 | 政府部门、招商人员 |
| **场景3：行业分析** | 行业趋势、技术方向、空间分布、企业生命周期 | Markdown + PDF + 图表 | 行业研究员、投资机构 |
| **场景4：招商清单** | 企业多维度评估、优质企业筛选 | Excel | 招商部门、园区管理 |
| **场景5：企业尽调** | 企业全面尽职调查报告 | Word | 投资机构、风控部门 |

---

## ✨ 功能特性

### 🎯 核心功能

- **真正的 Text2SQL**
  - 100% 动态生成 SQL（无硬编码）
  - LLM 为主、Vanna AI 兜底的双引擎架构
  - 基于完整 Schema 工程的高质量生成

- **完整的报告流水线**
  ```
  自然语言问题 → SQL生成 → 执行查询 → 数据分析 → 图表生成 → 网络搜索 → 多模态报告
  ```

- **智能图表生成**
  - 自动推断图表类型（折线图、柱状图、饼图、分组柱状图）
  - 根据数据特征智能选择最佳可视化方式
  - 支持自定义图表样式和配色

- **网络信息补充**
  - 自动搜索相关行业动态和新闻
  - 补充最新的市场信息和政策解读
  - 增强报告的时效性和完整性

- **多模态输出**
  - Markdown：适合在线查看和分享
  - PDF：适合打印和存档
  - Excel：适合数据分析和筛选
  - Word：适合正式报告和文档

### 🔧 技术特性

- **Schema 工程**
  - 完整的表结构、字段说明、关系定义
  - Few-shot 示例库（25+ 标准 Question-SQL 配对）
  - 单一事实来源，确保一致性

- **专业图表生成**
  - 现代化配色方案（专业蓝色系）
  - 高清输出（300 DPI，适合打印）
  - 自动推断最佳图表类型
  - 支持柱状图、折线图、饼图、分组柱状图
  - 图表正确嵌入Word和PDF文档

- **智能网络搜索**
  - LLM自动提取关键词
  - 添加时间范围提升相关性
  - 搜索结果融合到数据分析

- **安全配置**
  - 环境变量管理敏感信息
  - 无明文密码和密钥
  - 自动安全检查脚本

- **高性能**
  - 完整流程：10-15 秒
  - SQL生成：2-5 秒
  - 支持并发处理

- **可扩展**
  - 模块化设计，易于扩展新场景
  - 支持自定义提示词和 SQL 模板
  - 兼容多种 LLM 模型

---

## 🏗️ 技术架构

### 系统架构图

```
┌─────────────────────────────────────────────────────────────┐
│                        用户层                                │
│  Web界面 / API调用 / n8n工作流 / 命令行工具                  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      API服务层                               │
│  ┌──────────────┐              ┌──────────────┐            │
│  │ API Server   │              │ Vanna Server │            │
│  │ (8000端口)   │              │ (5000端口)   │            │
│  │ LLM + Vanna  │              │ Vanna专用    │            │
│  └──────────────┘              └──────────────┘            │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    核心处理层                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Text2SQL引擎 │  │ 数据分析模块 │  │ 图表生成模块 │     │
│  │ LLM/Vanna   │  │ LLM分析     │  │ 自动推断     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ 网络搜索模块 │  │ 文档生成模块 │  │ Schema工程   │     │
│  │ DuckDuckGo  │  │ MD/PDF/Excel │  │ 表结构/示例  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      数据层                                  │
│  ┌──────────────┐              ┌──────────────┐            │
│  │ MySQL数据库  │              │ 阿里云百炼   │            │
│  │ 场景1-3/4-5  │              │ LLM API     │            │
│  └──────────────┘              └──────────────┘            │
└─────────────────────────────────────────────────────────────┘
```

### 技术栈

**后端框架**
- Python 3.8+
- FastAPI（API 服务）
- Flask（Vanna 服务）

**AI 模型**
- 阿里云百炼 Coding Plan
  - qwen3.5-plus（推荐，支持图片理解）
  - kimi-k2.5（支持图片理解）
  - glm-5、MiniMax-M2.5
- Vanna AI（Text2SQL 兜底）

**数据库**
- MySQL 8.0+
- PyMySQL（数据库连接）

**数据处理与可视化**
- Pandas（数据处理）
- Matplotlib（图表生成）
- Seaborn（高级可视化）

**文档生成**
- ReportLab（PDF 生成）
- python-docx（Word 生成）
- openpyxl（Excel 生成）
- Markdown（文本格式）

**其他工具**
- DuckDuckGo（网络搜索）
- n8n（工作流编排，可选）

### SQL 生成策略

**双引擎架构**：LLM 为主、Vanna 兜底

```python
def generate_sql(question, scenario):
    # 1. 加载 Schema 和 Few-shot 示例
    schema = load_schema(scenario)
    examples = load_examples(scenario)
    
    # 2. LLM 生成（主力）
    sql = llm_generate(question, schema, examples)
    
    # 3. 验证 SQL
    if validate_sql(sql):
        return sql
    
    # 4. Vanna 兜底
    sql = vanna_generate(question)
    
    # 5. 再次验证
    if validate_sql(sql):
        return sql
    
    # 6. 返回错误
    raise SQLGenerationError()
```

**优势**：
- LLM 模式：基于详细 Schema + Few-shot，生成质量高
- Vanna 兜底：预训练模型，响应快，保证可用性
- 无硬编码：所有 SQL 均动态生成，灵活性强

---

## 🚀 快速开始

### 前置要求

- Python 3.8 或更高版本
- MySQL 8.0 或更高版本
- 阿里云百炼 Coding Plan 订阅（[订阅地址](https://dashscope.console.aliyun.com/)）

### 安装步骤

#### 1. 克隆项目

```bash
git clone https://github.com/your-repo/text2sql.git
cd text2sql
```

#### 2. 安装依赖

```bash
pip install -r requirements.txt
```

#### 3. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入真实配置
# - DASHSCOPE_API_KEY: 阿里云百炼 API Key（格式：sk-sp-xxxxx）
# - DB_PASSWORD_SCENARIO_1_3: 场景1-3数据库密码
# - DB_PASSWORD_SCENARIO_4_5: 场景4-5数据库密码
```

**重要**：`.env` 文件包含敏感信息，已在 `.gitignore` 中，不会被提交到 Git。

#### 4. 验证配置

```bash
# 测试数据库连接
python scripts/test_db_simple.py

# 测试完整功能（LLM + 数据库 + Text2SQL）
python scripts/test_quick.py
```

#### 5. 启动服务

**方式一：Web应用（推荐）**

```bash
# Windows
python web_app.py

# Linux/macOS
python web_app.py
```

Web应用启动后访问：http://localhost:7860

**方式二：API服务**

```bash
# Windows
scripts\deploy.bat

# Linux/macOS
bash scripts/deploy.sh
```

服务启动后：
- API 服务：http://localhost:8000
- Vanna 服务：http://localhost:5000
- API 文档：http://localhost:8000/docs

---

## 📚 使用文档

### Web应用使用（推荐）

启动Web应用后，访问 http://localhost:7860

**使用步骤**：
1. 选择业务场景（场景1-5）
2. 输入自然语言问题
3. 点击"生成报告"
4. 查看结果：
   - SQL查询语句
   - 查询结果数据
   - 数据可视化图表
   - AI数据分析
   - 网络信息补充
   - 下载报告（Markdown/PDF/Word）

**示例问题**：
- 场景1：分析2023-2024年融资趋势，按行业统计融资金额和融资数量
- 场景2：分析广东省深圳市的产业分布，统计各行业企业数量
- 场景3：分析科技行业近5年的发展趋势

详细使用指南：[WEB_APP_GUIDE.md](WEB_APP_GUIDE.md)

### API 调用示例

#### Python 调用

```python
import requests

# 简单查询
response = requests.post(
    "http://localhost:8000/api/query",
    json={
        "question": "分析2023-2024年融资趋势",
        "scenario": "data_insight",
        "mode": "auto"  # auto: 自动选择, llm: LLM模式, vanna: Vanna模式
    }
)

result = response.json()
print(f"生成的SQL: {result['sql']}")
print(f"查询结果: {result['data']}")
```

#### cURL 调用

```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "分析融资趋势",
    "scenario": "data_insight"
  }'
```

### Demo 示例

#### 场景1：数据洞察

```bash
python demo/scenario_1_data_insight.py
```

生成报告包含：
- 生成的 SQL 查询
- 数据概览表格
- 趋势图表（自动推断类型）
- LLM 数据分析与解读
- 网络信息补充
- 业务建议与结论

输出文件：
- `demo/output/scenario_1_data_insight_YYYYMMDD_HHMMSS.md`
- `demo/output/scenario_1_data_insight_YYYYMMDD_HHMMSS.pdf`
- `demo/output/scenario_1_data_insight_YYYYMMDD_HHMMSS.docx`

#### 场景2-3：地区产业分析、行业分析

```bash
python demo/scenario_2_regional_industry.py
python demo/scenario_3_industry_analysis.py
```

---

## 🔧 配置说明

### 环境变量配置

`.env` 文件配置项：

```bash
# 阿里云百炼 API
DASHSCOPE_API_KEY=sk-sp-xxxxx  # Coding Plan 专属 API Key
DASHSCOPE_BASE_URL=https://coding.dashscope.aliyuncs.com/v1

# 数据库配置 - 场景 1-3
DB_HOST_SCENARIO_1_3=your-host
DB_PORT_SCENARIO_1_3=3306
DB_NAME_SCENARIO_1_3=Gaaiyun
DB_USER_SCENARIO_1_3=your-user
DB_PASSWORD_SCENARIO_1_3=your-password

# 数据库配置 - 场景 4-5
DB_HOST_SCENARIO_4_5=your-host
DB_PORT_SCENARIO_4_5=3306
DB_NAME_SCENARIO_4_5=gaaiyun_2
DB_USER_SCENARIO_4_5=your-user
DB_PASSWORD_SCENARIO_4_5=your-password

# 模型配置
MODEL_NAME=qwen3.5-plus  # 推荐模型
MODEL_TEMPERATURE=0.1
```

### 支持的模型

**阿里云百炼 Coding Plan 支持的模型**：

| 模型 | 特点 | 适用场景 |
|------|------|---------|
| qwen3.5-plus | 推荐，支持图片理解 | 通用场景 |
| kimi-k2.5 | 支持图片理解 | 长文本处理 |
| glm-5 | 高性能 | 复杂推理 |
| MiniMax-M2.5 | 平衡性能 | 通用场景 |

**切换模型**：修改 `.env` 文件中的 `MODEL_NAME` 参数。

---

## 📖 API 文档

### 核心接口

#### 1. 查询接口

**POST** `/api/query`

生成 SQL 并执行查询。

**请求参数**：
```json
{
  "question": "分析2023年融资趋势",
  "scenario": "data_insight",
  "mode": "auto"
}
```

**响应**：
```json
{
  "sql": "SELECT ...",
  "data": {
    "columns": ["年份", "融资金额"],
    "rows": [[2023, 1000000]]
  },
  "execution_time": 2.5
}
```

#### 2. 报告接口

**POST** `/api/report`

生成完整的分析报告。

**请求参数**：
```json
{
  "question": "分析融资趋势",
  "scenario": "data_insight",
  "format": "markdown"
}
```

**响应**：
```json
{
  "report": "# 报告内容...",
  "charts": ["chart1.png"],
  "format": "markdown"
}
```

完整 API 文档：http://localhost:8000/docs

---

## 🗂️ 项目结构

```
text2sql/
├── web_app.py                 # Web应用主程序（推荐使用）
├── api_server.py              # API服务（8000端口）
├── api/
│   └── vanna_server.py        # Vanna服务（5000端口）
├── schema/                    # Schema工程（核心）
│   ├── gaaiyun_schema.md      # 场景1-3表结构（9张表）
│   ├── gaaiyun_2_schema.md    # 场景4-5表结构（20张表）
│   └── question_sql_examples.md  # Few-shot示例（25+配对）
├── demo/                      # Demo示例
│   ├── text2sql_utils.py      # 核心工具函数
│   ├── scenario_1_data_insight.py      # 场景1示例
│   ├── scenario_2_regional_industry.py # 场景2示例
│   ├── scenario_3_industry_analysis.py # 场景3示例
│   └── output/                # Demo输出目录
├── src/
│   └── utils/                 # 核心工具模块
│       ├── config.py          # 配置管理
│       ├── chart_generator.py # 图表生成（专业样式）
│       ├── web_search.py      # 网络搜索（智能关键词提取）
│       └── document_generator.py  # 文档生成（MD/PDF/Word）
├── scripts/                   # 工具脚本
│   ├── deploy.bat/sh          # API服务部署脚本
│   ├── start_web.bat/sh       # Web应用启动脚本
│   ├── test_db_simple.py      # 数据库连接测试
│   ├── test_quick.py          # 完整功能测试
│   └── check_security.py      # 安全检查脚本
├── docs/                      # 项目文档
│   ├── SECURITY_CONFIG.md     # 安全配置指南
│   ├── SECURITY_CHECKLIST.md  # 安全检查清单
│   └── n8n_integration.md     # n8n工作流集成指南
├── prompts/                   # 优化的提示词模板
│   ├── scenario_1_data_insight_optimized.md
│   └── scenario_4_investment_list_optimized.md
├── .env                       # 本地配置（不提交到Git）
├── .env.example               # 配置模板
├── .gitignore                 # Git忽略规则
├── requirements.txt           # Python依赖列表
├── README.md                  # 项目说明文档
├── WEB_APP_GUIDE.md          # Web应用使用指南
├── TEST_RESULTS.md           # 测试报告
└── FINAL_OPTIMIZATION.md     # 最终优化报告
```

### 核心文件说明

**应用入口**：
- `web_app.py` - Web界面应用（推荐，端口7860）
- `api_server.py` - RESTful API服务（端口8000）

**核心模块**：
- `demo/text2sql_utils.py` - Text2SQL核心逻辑
- `src/utils/` - 工具模块（图表、搜索、文档生成）

**Schema工程**：
- `schema/` - 数据库表结构和Few-shot示例

**配置文件**：
- `.env` - 本地环境变量（敏感信息，不提交）
- `.env.example` - 配置模板（可提交）

---

## 🔒 安全说明

### 重要提醒

⚠️ **永远不要将 `.env` 文件提交到 Git**

本项目使用环境变量管理敏感信息（API 密钥、数据库密码），确保安全性。

### 安全检查

提交代码前运行安全检查：

```bash
python scripts/check_security.py
```

### 安全最佳实践

1. **配置管理**
   - 使用 `.env` 文件存储敏感信息
   - 使用 `Config` 类加载配置
   - 不在代码中硬编码密码和密钥

2. **Git 提交**
   - 提交前运行 `check_security.py`
   - 检查 `git diff` 内容
   - 确认 `.env` 不在提交列表中

3. **密钥管理**
   - 定期更换 API 密钥
   - 使用最小权限原则
   - 不分享 `.env` 文件

详细安全指南：[docs/SECURITY_CONFIG.md](docs/SECURITY_CONFIG.md)

---

## 📊 性能指标

| 指标 | 数值 | 说明 |
|------|------|------|
| SQL 生成时间 | 2-5 秒 | LLM 模式 |
| SQL 生成时间 | 1-3 秒 | Vanna 模式 |
| 查询执行时间 | 0.5-2 秒 | 取决于数据量 |
| 报告生成时间 | 5-10 秒 | 包含图表和网络搜索 |
| 并发支持 | 10+ | 同时处理多个请求 |

---

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出建议！

### 贡献流程

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 开发规范

- 遵循 PEP 8 代码规范
- 添加必要的注释和文档
- 提交前运行安全检查
- 编写单元测试

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 📞 联系方式

- 项目主页：https://github.com/gaaiyun/text2sql-analysis
- 问题反馈：https://github.com/gaaiyun/text2sql-analysis/issues
- 作者：gaaiyun

---

## 🙏 致谢

- [阿里云百炼](https://dashscope.console.aliyun.com/) - 提供 LLM API 服务
- [Vanna AI](https://vanna.ai/) - Text2SQL 引擎
- [n8n](https://n8n.io/) - 工作流编排工具

---

<div align="center">

**⭐ 如果这个项目对您有帮助，请给我们一个 Star！**

Made with ❤️ by gaaiyun

</div>
