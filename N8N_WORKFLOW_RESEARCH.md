# n8n 工作流模板调研报告

> **调研时间**: 2026-02-26  
> **来源**: n8n 官方社区 (https://n8n.io/workflows/)

---

## 📊 n8n 社区概览

| 类别 | 工作流数量 |
|------|-----------|
| **总计** | 8,464 个 |
| **AI 相关** | 5,771 个 |
| **Sales** | 未知 |
| **IT Ops** | 未知 |
| **Marketing** | 未知 |
| **Document Ops** | 未知 |

---

## 🔍 相关模板分类

### 1. AI + Database 工作流

**适用场景**: Text2SQL、数据查询、报告生成

**典型节点组合**:
```
Webhook → AI Agent (LLM) → MySQL/PostgreSQL → Code (数据处理) → Markdown/HTML
```

**推荐模板**:
- AI 驱动的数据查询
- 自然语言到 SQL 转换
- 自动生成数据报告

---

### 2. HTTP Request + Database 工作流

**适用场景**: API 调用 + 数据库查询

**典型节点组合**:
```
Webhook → HTTP Request (调用 API) → Function (数据转换) → Database → Output
```

**推荐模板**:
- REST API 数据同步到数据库
- Webhook 触发数据查询
- 多数据源聚合

---

### 3. Report Generation 工作流

**适用场景**: 报告生成、数据导出

**典型节点组合**:
```
Schedule Trigger → Database Query → Code (图表生成) → HTML/PDF → Email/Storage
```

**推荐模板**:
- 定时数据报告
- PDF/Excel 导出
- 邮件自动发送

---

## 🎯 推荐工作流架构

基于 n8n 社区最佳实践，派蒙推荐以下架构：

### 架构 1: 单 Agent 集中处理 (推荐)

```json
{
  "name": "Text2SQL 数据洞察",
  "nodes": [
    {
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "parameters": {
        "httpMethod": "POST",
        "path": "text2sql-query"
      }
    },
    {
      "name": "任务分类",
      "type": "n8n-nodes-base.switch",
      "parameters": {
        "dataType": "string",
        "value1": "={{ $json.question }}",
        "rules": [
          {"value2": ".*企业.*", "output": 1},
          {"value2": ".*行业.*", "output": 2},
          {"value2": ".*地区.*", "output": 3}
        ]
      }
    },
    {
      "name": "HTTP Request - Vanna API",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "method": "POST",
        "url": "http://localhost:8000/api/vanna/query",
        "body": {
          "question": "={{ $json.question }}"
        }
      }
    },
    {
      "name": "Code - 数据处理",
      "type": "n8n-nodes-base.code",
      "parameters": {
        "language": "python",
        "code": """
import json
import pandas as pd

data = json.loads($input.all()[0].json.data)
df = pd.DataFrame(data)

# 生成 Markdown 表格
markdown_table = df.to_markdown(index=False)

return {
    'markdown': markdown_table,
    'data': data
}
"""
      }
    },
    {
      "name": "Markdown 输出",
      "type": "n8n-nodes-base.respondToWebhook",
      "parameters": {
        "respondWith": "text",
        "responseBody": "={{ $json.markdown }}"
      }
    }
  ]
}
```

---

### 架构 2: 报告生成工作流

```json
{
  "name": "行业分析报告生成",
  "nodes": [
    {
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook"
    },
    {
      "name": "HTTP Request - Vanna Query",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "method": "POST",
        "url": "http://localhost:8000/api/vanna/query"
      }
    },
    {
      "name": "Code - 图表生成",
      "type": "n8n-nodes-base.code",
      "parameters": {
        "language": "python",
        "code": """
import plotly.express as px
import pandas as pd
import json

data = json.loads($input.all()[0].json.data)
df = pd.DataFrame(data)

# 生成图表
fig = px.bar(df, x='category', y='value', title='行业分析')
fig.write_html('/tmp/chart.html')

return {'chart_path': '/tmp/chart.html'}
"""
      }
    },
    {
      "name": "HTML 报告组装",
      "type": "n8n-nodes-base.code",
      "parameters": {
        "language": "python",
        "code": """
html_template = '''
<!DOCTYPE html>
<html>
<head><title>行业分析报告</title></head>
<body>
<h1>行业分析报告</h1>
<h2>数据结果</h2>
{{table}}
<h2>图表</h2>
{{chart}}
</body>
</html>
'''

with open('/tmp/chart.html', 'r') as f:
    chart_html = f.read()

return {
    'html': html_template.replace('{{chart}}', chart_html)
}
"""
      }
    },
    {
      "name": "保存文件",
      "type": "n8n-nodes-base.writeBinaryFile",
      "parameters": {
        "filePath": "/tmp/report.html"
      }
    }
  ]
}
```

---

## 📦 关键节点说明

### 1. Webhook 节点
- **作用**: 接收外部请求
- **配置**: POST 方法，自定义路径
- **适用**: 所有场景的入口

### 2. HTTP Request 节点
- **作用**: 调用 Vanna API
- **配置**: POST + JSON Body
- **适用**: Text2SQL 查询

### 3. Code 节点 (Python)
- **作用**: 数据处理、图表生成
- **配置**: Python 代码
- **适用**: 数据转换、可视化

### 4. Switch 节点
- **作用**: 任务分类路由
- **配置**: 正则表达式匹配
- **适用**: 多场景分流

### 5. Write Binary File 节点
- **作用**: 保存报告文件
- **配置**: 文件路径
- **适用**: HTML/PDF导出

---

## 🎨 社区最佳实践

### 1. 错误处理
```json
{
  "name": "Error Handler",
  "type": "n8n-nodes-base.errorTrigger",
  "parameters": {
    "errorMessage": "={{ $json.error }}"
  }
}
```

### 2. 重试机制
```json
{
  "name": "Retry Policy",
  "parameters": {
    "retries": 3,
    "waitBetweenTries": 1000
  }
}
```

### 3. 速率限制
```json
{
  "name": "Rate Limit",
  "parameters": {
    "maxRequests": 10,
    "timeWindow": 60
  }
}
```

---

## 🔗 相关资源

### n8n 官方资源
- **工作流库**: https://n8n.io/workflows/
- **AI 工作流**: https://n8n.io/workflows/categories/ai/
- **文档**: https://docs.n8n.io
- **社区论坛**: https://community.n8n.io

### 第三方资源
- **n8n 模板市场**: https://creators.n8n.io/hub
- **GitHub 仓库**: https://github.com/n8n-io/n8n
- **Discord 社区**: https://discord.gg/n8n

---

## 📝 派蒙的建议

基于 n8n 社区最佳实践，派蒙建议：

### ✅ 采用方案
1. **单 Agent 集中处理** - 避免多分支冗余
2. **Webhook 入口** - 统一接收请求
3. **HTTP Request 调用 API** - 解耦 Vanna 服务
4. **Code 节点处理数据** - 灵活的数据转换
5. **Markdown 输出** - 稳定性高

### ⚠️ 注意事项
1. **错误处理** - 添加 Error Trigger 节点
2. **重试机制** - API 调用失败自动重试
3. **速率限制** - 避免频繁调用数据库
4. **日志记录** - 记录每次查询便于调试

---

_调研者：派蒙 ⭐_  
_调研时间：2026-02-26_
