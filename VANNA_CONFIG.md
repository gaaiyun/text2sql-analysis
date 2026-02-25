# Vanna AI 配置文档

> **创建时间**: 2026-02-26  
> **数据库**: MySQL (8.134.9.77:3306)

---

## 📦 安装依赖

```bash
pip install vanna
pip install vanna[mysql]
pip install plotly pandas
```

---

## 🔧 Vanna 配置脚本

```python
import vanna as vn
from vanna.mysql import MySQLConnector

# 配置数据库连接
class MyDBConnector(MySQLConnector):
    def __init__(self, config=None):
        MySQLConnector.__init__(self, config=config)
    
    def connect(self):
        import pymysql
        conn = pymysql.connect(
            host='8.134.9.77',
            port=3306,
            user='Gaaiyun',
            password='Why513338',
            database='Gaaiyun',
            charset='utf8mb4'
        )
        return conn

# 初始化 Vanna
vn.setup(
    config={
        'api_key': 'sk-sp-0b28da8e3f404df182c05d3fd45787a5',
        'model': 'qwen-plus',
        'db_type': 'mysql'
    }
)

# 连接数据库
conn = MyDBConnector(config={})
vn.connect_to_database(conn)

# 训练数据
vn.train(
    question="查询所有企业的基本信息",
    sql="SELECT name, format_name, regist_capi, start_date, status FROM 企业信息表 LIMIT 10"
)

vn.train(
    question="查询企业的知识产权信息",
    sql="SELECT 专利数量，商标数量，著作权数量 FROM 企业标签 WHERE eid = 'xxx'"
)

vn.train(
    question="查询企业的诉讼信息",
    sql="SELECT 案件名称，法院，判决日期 FROM 法院诉讼 WHERE eid = 'xxx'"
)

# 测试查询
sql = vn.generate_sql("查询注册资本大于 1000 万的企业")
print(f"生成的 SQL: {sql}")

result = vn.run_sql(sql)
print(f"查询结果：{result}")
```

---

## 📝 训练数据模板

### 场景 1: 数据洞察
```python
vn.train(
    question="2026 年 2 月新增企业数量是多少？",
    sql="SELECT COUNT(*) FROM 企业信息表 WHERE start_date >= '2026-02-01'"
)
```

### 场景 2: 地区产业分析
```python
vn.train(
    question="某地区的主导产业有哪些？",
    sql="SELECT industry_code, COUNT(*) as cnt FROM 企业行业分类 GROUP BY industry_code ORDER BY cnt DESC"
)
```

### 场景 3: 特定行业分析
```python
vn.train(
    question="某行业的企业数量增长趋势？",
    sql="SELECT DATE_FORMAT(start_date, '%Y-%m') as month, COUNT(*) as cnt FROM 企业行业分类 WHERE industry_code = 'xxx' GROUP BY month"
)
```

### 场景 4: 招商清单
```python
vn.train(
    question="查询注册资本大于 1000 万且存续的企业",
    sql="SELECT name, regist_capi, status FROM 企业信息表 WHERE regist_capi_new >= 10000000 AND status = '存续'"
)
```

### 场景 5: 企业尽调
```python
vn.train(
    question="查询企业的完整信息",
    sql="SELECT * FROM 企业信息表 WHERE eid = 'xxx'"
)
```

---

## 🚀 快速开始

```bash
# 1. 安装依赖
pip install vanna vanna[mysql] plotly pandas

# 2. 运行配置脚本
python vanna_config.py

# 3. 测试查询
python -c "import vanna as vn; print(vn.ask('查询所有企业'))"
```

---

_创建者：执行派蒙 ⭐_
