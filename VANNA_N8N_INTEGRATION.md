# Vanna AI + n8n 集成方案

> **创建时间**: 2026-02-26  
> **目标**: Text2SQL → 图表 → 行业分析报告

---

## 📋 目录

1. [Vanna AI 安装配置](#vanna-ai-安装配置)
2. [n8n 工作流设计](#n8n-工作流设计)
3. [API 集成示例](#api-集成示例)
4. [图表生成](#图表生成)
5. [报告导出](#报告导出)

---

## 🔧 Vanna AI 安装配置

### 安装
```bash
pip install vanna
pip install vanna[postgres]  # PostgreSQL 支持
pip install vanna[duckdb]    # DuckDB 支持
```

### 快速开始
```python
import vanna as vn

# 配置 LLM (百炼 API)
vn.set_api_key("sk-sp-0b28da8e3f404df182c05d3fd45787a5")
vn.set_model("qwen-plus")

# 配置数据库
from vanna.duckdb import DuckDB
vn.connect_to_duckdb("duckdb:///:memory:")

# 训练数据
vn.train(
    question="2026 年 2 月销售额是多少？",
    sql="SELECT SUM(amount) FROM orders WHERE date >= '2026-02-01'"
)

vn.train(
    question="哪个产品销量最好？",
    sql="SELECT product, SUM(quantity) as total FROM orders GROUP BY product ORDER BY total DESC LIMIT 1"
)

# 查询
result = vn.ask("2026 年 2 月销售额是多少？")
print(result)
```

---

## 🔄 n8n 工作流配置

### 工作流 JSON (可导入 n8n)

```json
{
  "name": "Text2SQL 行业报告生成",
  "nodes": [
    {
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "parameters": {
        "httpMethod": "POST",
        "path": "text2sql-report"
      }
    },
    {
      "name": "Vanna AI Query",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "method": "POST",
        "url": "http://localhost:8080/api/vanna/query",
        "body": {
          "question": "={{ $json.question }}"
        }
      }
    },
    {
      "name": "Generate Chart",
      "type": "n8n-nodes-base.code",
      "parameters": {
        "code": """
import plotly.express as px
import pandas as pd

df = pd.DataFrame($input.all()[0].json.data)
fig = px.bar(df, x='category', y='value', title='行业分析')
fig.write_html('report_chart.html')
return {'chart': 'report_chart.html'}
"""
      }
    },
    {
      "name": "Generate Report",
      "type": "n8n-nodes-base.html",
      "parameters": {
        "template": """
<h1>行业分析报告</h1>
<p>问题：{{ $json.question }}</p>
<h2>查询结果</h2>
{{ $json.sql_result }}
<h2>图表</h2>
<img src="{{ $json.chart }}" />
"""
      }
    }
  ]
}
```

---

## 🌐 API 集成示例

### Vanna REST API 部署

```python
from fastapi import FastAPI
from vanna import Vanna
from vanna.remote import VannaDefault

app = FastAPI()

# 配置 Vanna
vn = VannaDefault(model="qwen-plus", api_key="your-api-key")
vn.connect_to_duckdb("duckdb:///:memory:")

@app.post("/api/vanna/query")
async def query(question: str):
    sql = vn.generate_sql(question)
    result = vn.run_sql(sql)
    chart = vn.generate_plotly_code(result)
    
    return {
        "question": question,
        "sql": sql,
        "data": result,
        "chart": chart
    }

@app.post("/api/vanna/train")
async def train(question: str, sql: str):
    vn.train(question=question, sql=sql)
    return {"status": "ok"}
```

### n8n HTTP Request 配置

```json
{
  "method": "POST",
  "url": "http://localhost:8000/api/vanna/query",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "question": "={{ $json.question }}"
  }
}
```

---

## 📊 图表生成

### Plotly 图表配置

```python
import plotly.express as px
import plotly.graph_objects as go

# 柱状图
fig = px.bar(df, x='category', y='value', title='行业对比')

# 折线图
fig = px.line(df, x='date', y='revenue', title='收入趋势')

# 饼图
fig = px.pie(df, values='market_share', names='company', title='市场份额')

# 保存为 HTML
fig.write_html('chart.html')

# 保存为图片
fig.write_image('chart.png')
```

### n8n 图表节点

```json
{
  "name": "Generate Chart",
  "type": "n8n-nodes-base.code",
  "parameters": {
    "language": "python",
    "code": """
import plotly.express as px
import pandas as pd
import json

# 从输入获取数据
data = json.loads($input.all()[0].json.data)
df = pd.DataFrame(data)

# 生成图表
fig = px.bar(df, x='category', y='value', title='行业分析')
fig.update_layout(template='plotly_white')

# 保存
fig.write_html('output/chart.html')
fig.write_image('output/chart.png')

return {'chart_html': 'output/chart.html', 'chart_png': 'output/chart.png'}
"""
  }
}
```

---

## 📄 报告导出

### HTML 报告模板

```html
<!DOCTYPE html>
<html>
<head>
    <title>行业分析报告</title>
    <style>
        body { font-family: Arial; margin: 40px; }
        h1 { color: #2c3e50; }
        .chart { margin: 20px 0; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; }
        th { background-color: #3498db; color: white; }
    </style>
</head>
<body>
    <h1>行业分析报告</h1>
    <p><strong>生成时间:</strong> {{ timestamp }}</p>
    <p><strong>问题:</strong> {{ question }}</p>
    
    <h2>SQL 查询</h2>
    <pre><code>{{ sql }}</code></pre>
    
    <h2>数据结果</h2>
    <table>
        {{ table_html }}
    </table>
    
    <h2>可视化图表</h2>
    <div class="chart">
        {{ chart_html }}
    </div>
    
    <h2>分析总结</h2>
    <p>{{ summary }}</p>
</body>
</html>
```

### PDF 导出

```python
from weasyprint import HTML

# HTML → PDF
HTML(filename='report.html').write_pdf('report.pdf')

# 添加样式
HTML(
    filename='report.html',
    base_url='.'
).write_pdf(
    'report.pdf',
    stylesheets=['style.css']
)
```

---

## 🚀 完整示例：行业分析报告生成

### 1. 用户输入
```
"帮我生成 2026 年 2 月电子产品行业分析报告，包括销售额、市场份额、趋势图表"
```

### 2. Vanna Text2SQL
```python
question = "2026 年 2 月电子产品销售额和市场份额"

sql = vn.generate_sql(question)
# 输出：
# SELECT 
#     category,
#     SUM(sales) as total_sales,
#     COUNT(*) as market_share
# FROM sales_data
# WHERE date >= '2026-02-01' AND category LIKE '%电子产品%'
# GROUP BY category
# ORDER BY total_sales DESC

result = vn.run_sql(sql)
```

### 3. 图表生成
```python
fig = px.bar(
    result, 
    x='category', 
    y='total_sales',
    title='2026 年 2 月电子产品销售额',
    labels={'category': '产品类别', 'total_sales': '销售额 (万元)'}
)
fig.write_html('chart_sales.html')
```

### 4. 报告组装
```python
from jinja2 import Template

template = Template(open('report_template.html').read())
report = template.render(
    timestamp=datetime.now(),
    question=question,
    sql=sql,
    table_html=result.to_html(),
    chart_html=open('chart_sales.html').read(),
    summary="2026 年 2 月电子产品销售额同比增长 15%..."
)

with open('report.html', 'w') as f:
    f.write(report)
```

### 5. n8n 工作流输出
- ✅ HTML 报告 → 发送邮件/保存到存储
- ✅ PDF 报告 → 下载链接
- ✅ 图表 → 嵌入网页/分享链接

---

## 📦 依赖安装

```bash
# Vanna AI
pip install vanna
pip install vanna[duckdb]
pip install vanna[postgres]

# 图表
pip install plotly
pip install pandas
pip install kaleido  # 图片导出

# 报告
pip install jinja2
pip install weasyprint  # PDF 导出

# API 服务
pip install fastapi
pip install uvicorn
```

---

## 🎯 下一步

1. **安装 Vanna AI** - `pip install vanna`
2. **配置训练数据** - 导入历史查询
3. **部署 API 服务** - FastAPI + Vanna
4. **创建 n8n 工作流** - 导入 JSON 配置
5. **测试报告生成** - 端到端测试

---

_创建时间：2026-02-26_  
_派蒙 ⭐_
