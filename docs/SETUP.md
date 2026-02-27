# Text2SQL 项目 - 完整部署指南

> **版本**: v0.2.0  
> **更新日期**: 2026-02-27  
> **合并自**: CONFIGURATION.md + SETUP_GUIDE.md + QUICKSTART.md

---

## 📋 目录

1. [快速开始](#快速开始)
2. [环境配置](#环境配置)
3. [数据库配置](#数据库配置)
4. [Vanna AI 配置](#vanna-ai-配置)
5. [API 服务配置](#api-服务配置)
6. [n8n 工作流配置](#n8n-工作流配置)
7. [测试验证](#测试验证)
8. [故障排查](#故障排查)
9. [安全提示](#安全提示)

---

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/gaaiyun/text2sql-analysis.git
cd text2sql-analysis
```

### 2. 安装依赖

```bash
# Python 依赖
pip install -r requirements.txt

# n8n (全局安装)
npm install -g n8n
```

### 3. 配置环境变量

复制配置模板：

```bash
cp config.template.json config.json
cp .env.example .env
```

编辑 `.env` 文件：

```bash
# 阿里云百炼 API
DASHSCOPE_API_KEY=your-dashscope-api-key

# 数据库配置
DB_HOST=your-db-host
DB_PORT=3306
DB_NAME=your-db-name
DB_USER=your-db-user
DB_PASSWORD=your-db-password

# Vanna AI 配置
VANNA_API_KEY=your-vanna-api-key
VANNA_ORG=your-org-name
VANNA_MODEL=your-model-name
```

### 4. 启动服务

```bash
# 启动 Vanna API 服务
python api/vanna_server.py

# 启动 n8n
n8n start
```

---

## 环境配置

### 系统要求

- Python 3.8+
- MySQL 8.0+
- Node.js 16+ (用于 n8n)

### Python 依赖

```txt
# requirements.txt
vanna
mysql-connector-python
dashscope
flask
python-dotenv
```

### 安装命令

```bash
pip install -r requirements.txt
```

---

## 数据库配置

### 双数据库架构

系统使用两个 MySQL 数据库：

| 场景 | 主机 | 端口 | 数据库 | 用户名 | 说明 |
|------|------|------|--------|--------|------|
| 场景 1-3 | ${DB_HOST} | 3306 | Gaaiyun | Gaaiyun | 数据洞察、地区产业、行业分析 |
| 场景 4-5 | ${DB_HOST} | 3306 | gaaiyun_2 | gaaiyun_2 | 招商清单、企业尽调 |

### 核心表结构

#### 场景 1-3 核心表

**企业基本信息** (qcc_base_info)
```sql
CREATE TABLE qcc_base_info (
  eid varchar(255) PRIMARY KEY,
  credit_no varchar(255),
  format_name varchar(255),
  regist_capi_new varchar(255),
  start_date varchar(255),
  province_code varchar(255),
  district_code varchar(255),
  new_status_code varchar(255)
);
```

**投资事件** (investment_events)
```sql
CREATE TABLE investment_events (
  eid text,
  round text,
  amount double,
  round_date datetime,
  investor text
);
```

**企业行业分类** (industry_classification)
```sql
CREATE TABLE industry_classification (
  eid text,
  industry_code text,
  industry_name text
);
```

#### 场景 4-5 核心表

**企业信息** (enterprise_info)
```sql
CREATE TABLE enterprise_info (
  eid varchar(255) PRIMARY KEY,
  enterprise_name varchar(255),
  registered_capital decimal,
  establishment_date date,
  industry varchar(255),
  status varchar(255)
);
```

**知识产权** (intellectual_property)
```sql
CREATE TABLE intellectual_property (
  eid varchar(255),
  patent_count int,
  trademark_count int,
  software_copyright_count int
);
```

### 字符集处理

**重要**: JOIN 时必须使用 COLLATE

```sql
-- 正确的 JOIN 方式
SELECT * FROM table1 t1
JOIN table2 t2 
  ON t1.eid = t2.eid COLLATE utf8mb4_unicode_ci;
```

---

## Vanna AI 配置

### 什么是 Vanna AI？

Vanna AI 是一个开源的 Text2SQL 框架，通过训练让模型理解数据库 Schema，从而生成准确的 SQL 查询。

### 获取 Vanna API Key

1. 访问 [Vanna AI 官网](https://vanna.ai/)
2. 注册账号
3. 创建 Organization
4. 获取 API Key

### 训练步骤

#### 1. 连接数据库

```python
import vanna as vn

# MySQL 连接（使用环境变量）
import os
vn.connect_to_mysql(
    host=os.getenv('DB_HOST'),
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD')
)
```

#### 2. 训练 DDL

```python
# 训练表结构
ddl = """
CREATE TABLE qcc_base_info (
  eid varchar(255) PRIMARY KEY,
  format_name varchar(255),
  regist_capi_new varchar(255)
);
"""
vn.train(ddl=ddl)
```

#### 3. 训练示例查询

```python
# 添加示例查询帮助模型理解
vn.train(
    question="查询所有企业",
    sql="SELECT * FROM qcc_base_info"
)
```

#### 4. 运行训练脚本

```bash
python scripts/train_vanna.py
```

---

## API 服务配置

### 启动 API 服务

```bash
python api/vanna_server.py
```

服务将在 `http://localhost:5000` 启动

### API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 健康检查 |
| `/api/vanna/ask` | POST | Text2SQL 查询 |
| `/api/vanna/train` | POST | 训练模型 |

### 示例请求

```bash
curl -X POST http://localhost:5000/api/vanna/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "查询所有企业"}'
```

---

## n8n 工作流配置

### 导入工作流

1. 登录 n8n 管理界面
2. 进入 Settings → Workflows
3. 点击 Import
4. 选择 `n8n_workflow_text2sql.json`
5. 激活工作流

### 配置 Webhook

工作流将在 `http://localhost:5678/webhook/text2sql-query` 监听请求

### 测试工作流

```bash
curl -X POST http://localhost:5678/webhook/text2sql-query \
  -H "Content-Type: application/json" \
  -d '{"question": "查询注册资本大于 1000 万的企业"}'
```

---

## 测试验证

### 测试数据库连接

```bash
python tests/test_db_connection.py
```

### 测试 SQL 生成

```bash
python tests/test_vanna_sql.py
```

### 测试 API 服务

```bash
curl http://localhost:5000/
```

### 运行全部测试

```bash
python -m pytest tests/ -v
```

---

## 故障排查

### 问题 1: 无法连接数据库

```
Error: Can't connect to MySQL server
```

**解决方案**:
- 检查数据库主机是否可访问：`ping ${DB_HOST}`
- 确认用户名密码正确
- 检查防火墙设置

### 问题 2: Vanna API Key 无效

```
Error: Invalid API key
```

**解决方案**:
- 检查 API Key 是否正确复制
- 确认 Vanna 账号状态正常
- 联系 Vanna 支持

### 问题 3: SQL 生成失败

```
Error: No training data found
```

**解决方案**:
- 运行训练脚本：`python scripts/train_vanna.py`
- 检查 DDL 是否正确提取
- 添加更多示例查询

### 问题 4: 字符集错误

```
Error: Illegal mix of collations
```

**解决方案**:
- 确保 JOIN 时使用 COLLATE
- 检查数据库字符集设置

---

## 安全提示

### 1. 保护敏感信息

- ✅ **不要将 `config.json` 或 `.env` 上传到 Git**
- ✅ 已添加到 `.gitignore`
- ✅ 仅使用 `config.template.json` 作为模板

### 2. 定期更新凭证

- 建议每 3 个月更新一次 API Keys
- 如发现泄露立即更换

### 3. 数据库安全

- 生产环境使用只读数据库账号
- 限制查询范围
- 启用 SQL 注入防护

### 4. 网络安全

- 使用防火墙限制数据库访问
- API 服务使用 HTTPS
- 启用 n8n 认证

---

## 项目结构

```
text2sql/
├── api/                    # API 服务
│   ├── vanna_server.py    # Vanna API 服务器
│   └── server.py          # 主 API 服务器
├── scripts/                # 脚本工具
│   ├── train_vanna.py     # Vanna 训练脚本
│   └── extract_schema.py  # Schema 提取脚本
├── tests/                  # 测试文件
│   ├── test_db_connection.py
│   ├── test_vanna_sql.py
│   └── test_all_scenarios.py
├── docs/                   # 文档
│   ├── SETUP.md           # 本文件
│   └── SCHEMA.md          # Schema 文档
├── workflows/              # n8n 工作流
│   └── text2sql-query.json
├── config.template.json    # 配置模板
├── .env.example            # 环境变量模板
├── .gitignore              # Git 忽略文件
└── README.md               # 项目说明
```

---

## 获取帮助

- **项目文档**: README.md
- **测试报告**: TEST_REPORT.md
- **GitHub**: https://github.com/gaaiyun/text2sql-analysis
- **问题反馈**: GitHub Issues

---

<div align="center">

**Made with ❤️ by 派蒙 + Gaaiyun**

*2026-02-27*

</div>
