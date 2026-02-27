# Text2SQL 项目 - 配置指南

> **版本**: v0.1.0  
> **更新日期**: 2026-02-26

---

## 📋 目录

1. [快速开始](#快速开始)
2. [数据库配置](#数据库配置)
3. [Vanna AI 配置](#vanna-ai-配置)
4. [n8n 工作流配置](#n8n-工作流配置)
5. [环境变量配置](#环境变量配置)
6. [常见问题](#常见问题)

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
```

编辑 `config.json`：

```json
{
  "database": {
    "host": "YOUR_DB_HOST",
    "port": 3306,
    "user": "YOUR_DB_USER",
    "password": "YOUR_DB_PASSWORD",
    "database": "YOUR_DB_NAME"
  },
  "bailian": {
    "api_key": "YOUR_DASHSCOPE_API_KEY",
    "base_url": "https://coding.dashscope.aliyuncs.com/v1",
    "model": "qwen3.5-plus"
  },
  "vanna": {
    "api_key": "YOUR_VANNA_API_KEY",
    "org": "your-org"
  }
}
```

### 4. 启动服务

```bash
# 启动 Vanna API 服务
python api/vanna_server.py

# 启动 n8n
n8n start
```

---

## 数据库配置

### 双数据库架构

系统使用两个 MySQL 数据库：

| 场景 | 主机 | 端口 | 数据库 | 用户名 | 说明 |
|------|------|------|--------|--------|------|
| 场景 1-3 | 8.134.9.77 | 3306 | Gaaiyun | Gaaiyun | 数据洞察、地区产业、行业分析 |
| 场景 4-5 | 8.134.9.77 | 3306 | gaaiyun_2 | gaaiyun_2 | 招商清单、企业尽调 |

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

### 训练步骤

#### 1. 连接数据库

```python
import vanna as vn

# MySQL 连接
vn.connect_to_mysql(
    host='8.134.9.77',
    database='Gaaiyun',
    user='Gaaiyun',
    password='Why513338'
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

#### 3. 训练文档

```python
# 训练业务知识
documentation = """
企业基本信息表存储企业的核心信息，包括：
- eid: 企业唯一标识
- format_name: 企业名称
- regist_capi_new: 注册资本（单位：元）
"""
vn.train(documentation=documentation)
```

#### 4. 训练 SQL 示例

```python
# 训练 SQL 示例
sql = """
SELECT format_name, regist_capi_new 
FROM qcc_base_info 
WHERE province_code = '110000'
ORDER BY regist_capi_new DESC
LIMIT 10
"""
vn.train(sql=sql)
```

### 使用 Kiro 模型

如果使用 Kiro 的 Claude Opus 4.6：

```python
from scripts.setup_vanna_kiro import setup_vanna_kiro

vn = setup_vanna_kiro()
# 后续操作同上
```

---

## n8n 工作流配置

### 导入工作流

1. 启动 n8n:
   ```bash
   n8n start
   ```

2. 访问 http://localhost:5646

3. 点击 **Settings → Import from File**

4. 选择 `n8n_workflow_text2sql.json`

### 工作流节点说明

```
┌─────────────────────────────────────────────────────────────┐
│                    Text2SQL 工作流                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐                 │
│  │ 触发器  │ →  │ 任务分类 │ →  │ 批量获取 │                 │
│  │(Webhook)│    │(LLM)    │    │(MySQL)  │                 │
│  └─────────┘    └─────────┘    └─────────┘                 │
│                                    │                        │
│                                    ↓                        │
│                              ┌─────────┐                   │
│                              │ 集中处理 │                   │
│                              │(单 Agent)│                   │
│                              └─────────┘                   │
│                                    │                        │
│                    ┌───────────────┼───────────────┐       │
│                    ↓               ↓               ↓       │
│              ┌─────────┐    ┌─────────┐    ┌─────────┐     │
│              │知识库   │    │网络搜索 │    │数据分析 │     │
│              │(可选)   │    │(可选)   │    │(LLM)   │     │
│              └─────────┘    └─────────┘    └─────────┘     │
│                    │               │               │       │
│                    └───────────────┼───────────────┘       │
│                                    ↓                        │
│                              ┌─────────┐                   │
│                              │ Markdown│                   │
│                              │ 输出    │                   │
│                              └─────────┘                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 关键配置

#### 1. MySQL 节点

- **Host**: 8.134.9.77
- **Port**: 3306
- **Database**: Gaaiyun / gaaiyun_2
- **User**: Gaaiyun / gaaiyun_2

#### 2. LLM 节点

- **Model**: qwen3.5-plus
- **Base URL**: https://coding.dashscope.aliyuncs.com/v1
- **API Key**: 从阿里云百炼获取

#### 3. 代码节点

用于数据预处理和格式化：

```javascript
// 示例：格式化查询结果
const results = $input.all()[0].json;
return {
  json: {
    formatted_data: results.map(r => ({
      name: r.format_name,
      capital: parseFloat(r.regist_capi_new)
    }))
  }
};
```

---

## 环境变量配置

### .env 文件

创建 `.env` 文件：

```bash
# 数据库配置
DB_HOST=8.134.9.77
DB_PORT=3306
DB_USER_GAAIYUN=Gaaiyun
DB_PASS_GAAIYUN=Why513338
DB_NAME_GAAIYUN=Gaaiyun

DB_USER_GAAIYUN2=gaaiyun_2
DB_PASS_GAAIYUN2=Why513338
DB_NAME_GAAIYUN2=gaaiyun_2

# 阿里云百炼
DASHSCOPE_API_KEY=your_api_key_here

# Vanna AI
VANNA_API_KEY=your_vanna_key_here
VANNA_ORG=your_org

# Kiro (可选)
KIRO_API_KEY=your_kiro_key_here
KIRO_BASE_URL=https://kiro.singforge.dpdns.org:11128/v1
```

### 加载环境变量

```python
from dotenv import load_dotenv
import os

load_dotenv()

# 使用
api_key = os.getenv('DASHSCOPE_API_KEY')
```

---

## 常见问题

### Q1: SQL 生成错误

**问题**: 生成的 SQL 执行失败

**解决**:
1. 检查是否使用了 COLLATE
2. 验证表名和字段名是否正确
3. 查看 validate_sql.py 的验证结果

### Q2: 字符集冲突

**问题**: `Illegal mix of collations`

**解决**:
```sql
-- 在 JOIN 时添加 COLLATE
ON t1.eid = t2.eid COLLATE utf8mb4_unicode_ci
```

### Q3: Token 超限

**问题**: 提示词太长导致 token 超限

**解决**:
1. 使用精简版 Schema: `schema_gaaiyun_essential.md`
2. 只选择必要的表和字段
3. 分批处理大数据量查询

### Q4: n8n 连接失败

**问题**: 无法连接到 n8n

**解决**:
1. 检查 n8n 是否启动: `n8n start`
2. 确认端口 5646 未被占用
3. 查看 n8n 日志排查错误

### Q5: Vanna 训练失败

**问题**: Vanna 无法连接数据库

**解决**:
1. 检查数据库连接信息
2. 确认数据库可访问
3. 检查防火墙设置

---

## 相关文档

- [README.md](README.md) - 项目简介
- [TEST_REPORT.md](TEST_REPORT.md) - 测试报告
- [QUICKSTART.md](QUICKSTART.md) - 快速开始

---

<div align="center">

**配置指南完成！Made with ❤️ by 派蒙**

*2026-02-26*

</div>
