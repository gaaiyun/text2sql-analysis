# Vanna AI 配置指南 - 使用 Kiro OpenAI 兼容 API

> **基于官方文档**: https://vanna.ai/docs/configure/openai/sqlite  
> **创建时间**: 2026-02-26  
> **关键**: 无需 Vanna API Key，直接使用 Kiro 反代！

---

## 🎯 核心思路

**使用 Kiro 的 OpenAI 兼容 API 代替 Vanna API**

- ✅ 无需 Vanna API Key
- ✅ 无需注册 Vanna
- ✅ 直接使用 Kiro 反代
- ✅ 支持 MySQL 数据库

---

## 📋 配置步骤

### 步骤 1: 安装依赖

```bash
pip install 'vanna[fastapi,openai]' pymysql
```

**需要的包**:
- `vanna` - Vanna AI 核心
- `openai` - OpenAI 兼容 API
- `fastapi` - FastAPI 服务
- `uvicorn` - ASGI 服务器
- `pymysql` - MySQL 驱动

---

### 步骤 2: 运行配置脚本

```bash
cd C:\Users\gaaiy\Desktop\text2sql
python scripts/setup_vanna_kiro.py
```

**脚本会创建**:
1. `vanna_kiro_config.py` - Vanna 配置文件
2. `test_vanna_kiro.py` - 测试脚本

---

### 步骤 3: 测试配置

```bash
python test_vanna_kiro.py
```

**预期输出**:
```
[OK] 数据库连接成功！
[INFO] 数据库包含 9 张表
[INFO] 测试 LLM...
[OK] LLM 响应：...
```

---

### 步骤 4: 启动 Vanna API 服务

```bash
python vanna_kiro_config.py
```

**访问**: http://localhost:8000

---

## 🔧 完整配置代码

### 1. 配置 LLM（使用 Kiro OpenAI 兼容 API）

```python
from vanna.integrations.openai import OpenAILlmService

llm = OpenAILlmService(
    model="claude-sonnet-4.6",  # Kiro 模型
    api_base="https://kiro.singforge.dpdns.org:11128/v1",  # Kiro Base URL
    api_key="kp-b7b71ffe429782691c981878c10bd1a16404ade12a0b3523"  # Kiro API Key
)
```

**关键点**:
- ✅ 使用 `OpenAILlmService`（OpenAI 兼容）
- ✅ `api_base` 指向 Kiro
- ✅ `api_key` 使用 Kiro Key
- ✅ `model` 使用 Kiro 可用模型

---

### 2. 配置数据库（MySQL）

```python
from vanna.tools import RunSqlTool
from vanna.integrations.mysql import MysqlRunner

# 场景 1-3: Gaaiyun 数据库
db_tool_1_3 = RunSqlTool(
    sql_runner=MysqlRunner(
        host='8.134.9.77',
        port=3306,
        user='Gaaiyun',
        password='Why513338',
        database='Gaaiyun'
    )
)

# 场景 4-5: gaaiyun_2 数据库
db_tool_4_5 = RunSqlTool(
    sql_runner=MysqlRunner(
        host='8.134.9.77',
        port=3306,
        user='gaaiyun_2',
        password='Why513338',
        database='gaaiyun_2'
    )
)
```

---

### 3. 创建 Agent

```python
from vanna import Agent
from vanna.core.registry import ToolRegistry

tools = ToolRegistry()

# 注册数据库工具
tools.register_local_tool(db_tool_1_3, access_groups=['admin', 'user'])
tools.register_local_tool(db_tool_4_5, access_groups=['admin', 'user'])

# 创建 Agent
agent = Agent(
    llm_service=llm,
    tool_registry=tools
)
```

---

### 4. 运行服务器

```python
from vanna.servers.fastapi import VannaFastAPIServer

server = VannaFastAPIServer(agent)
server.run()  # 访问 http://localhost:8000
```

---

## 🎯 可用 Kiro 模型

| 模型 | 适用场景 | 推荐度 |
|------|---------|--------|
| `claude-sonnet-4.6` | 日常任务（推荐） | ⭐⭐⭐ |
| `claude-opus-4.6` | 复杂推理 | ⭐⭐ |
| `claude-sonnet-4.5` | 日常任务 | ⭐⭐ |
| `claude-opus-4.5` | 复杂任务 | ⭐⭐ |
| `claude-sonnet-4` | 简单任务 | ⭐ |
| `claude-haiku-4.5` | 快速响应 | ⭐ |

---

## 📊 与官方文档对比

| 配置项 | 官方示例 | 我们的配置 |
|--------|---------|-----------|
| LLM | OpenAI GPT-5 | Kiro Claude Sonnet 4.6 |
| API Base | https://api.openai.com/v1 | https://kiro.singforge.dpdns.org:11128/v1 |
| API Key | sk-... | kp-... |
| 数据库 | SQLite | MySQL |
| Agent Memory | DemoAgentMemory | 可选 |
| 用户认证 | SimpleUserResolver | 可选 |

---

## 🚀 快速测试

### 测试 1: 数据库连接

```python
import pymysql

conn = pymysql.connect(
    host='8.134.9.77',
    user='Gaaiyun',
    password='Why513338',
    database='Gaaiyun'
)

cur = conn.cursor()
cur.execute("SHOW TABLES")
tables = [row[0] for row in cur.fetchall()]
print(f"数据库包含 {len(tables)} 张表")

conn.close()
```

---

### 测试 2: LLM 连接

```python
from vanna.integrations.openai import OpenAILlmService

llm = OpenAILlmService(
    model="claude-sonnet-4.6",
    api_base="https://kiro.singforge.dpdns.org:11128/v1",
    api_key="kp-b7b71ffe429782691c981878c10bd1a16404ade12a0b3523"
)

response = llm.generate("SELECT * FROM", max_tokens=50)
print(f"LLM 响应：{response}")
```

---

### 测试 3: 完整流程

```python
# 1. 连接数据库
conn = pymysql.connect(...)

# 2. 获取表结构
cur = conn.cursor()
cur.execute("SHOW CREATE TABLE 企业基本信息")
schema = cur.fetchone()[1]

# 3. 让 LLM 生成 SQL
question = "查询近 3 年企业融资趋势"
prompt = f"""基于以下表结构，生成 SQL 查询：
{schema}

问题：{question}

SQL:"""

sql = llm.generate(prompt, max_tokens=500)
print(f"生成的 SQL: {sql}")

# 4. 执行 SQL
cur.execute(sql)
results = cur.fetchall()
print(f"查询结果：{len(results)} 条")

conn.close()
```

---

## ⚠️ 注意事项

### 1. API Key 安全
- 不要将 `vanna_kiro_config.py` 上传到 GitHub
- 已添加到 `.gitignore`
- 定期更换 Kiro Key

### 2. 数据库安全
- 使用只读账号（生产环境）
- 限制查询权限
- 避免 DROP/DELETE 等操作

### 3. 性能优化
- 添加查询超时限制
- 使用连接池
- 缓存常用查询

---

## 🐛 故障排查

### 问题 1: 无法连接数据库
```bash
# 检查网络
ping 8.134.9.77

# 检查端口
telnet 8.134.9.77 3306

# 检查账号权限
mysql -h 8.134.9.77 -u Gaaiyun -p
```

### 问题 2: LLM 返回错误
```python
# 检查 API Key
print(f"API Key: {api_key[:10]}...{api_key[-5:]}")

# 检查 Base URL
print(f"Base URL: {api_base}")

# 测试连接
import httpx
response = httpx.get(api_base, timeout=5)
print(f"状态码：{response.status_code}")
```

### 问题 3: SQL 生成错误
```python
# 打印完整 prompt
print(f"Prompt: {prompt}")

# 打印生成的 SQL
print(f"SQL: {sql}")

# 手动执行 SQL 验证
cur.execute(sql)
```

---

## 📞 参考文档

- **Vanna 官方文档**: https://vanna.ai/docs/configure/openai/sqlite
- **Vanna GitHub**: https://github.com/vanna-ai/vanna
- **OpenAI 兼容 API**: https://platform.openai.com/docs/api-reference
- **Kiro 配置**: `C:\Users\gaaiy\.openclaw\KIRO_QUICK_GUIDE.md`

---

## 🎯 下一步

1. ✅ 安装依赖
2. ✅ 运行配置脚本
3. ✅ 测试数据库连接
4. ✅ 测试 LLM 连接
5. ✅ 启动 Vanna API 服务
6. ⏳ 测试 SQL 生成
7. ⏳ 集成到 Text2SQL 项目

---

<div align="center">

**配置指南完成！Made with ❤️ by 派蒙**

*基于 Vanna 官方文档 + Kiro OpenAI 兼容 API*

2026-02-26

</div>
