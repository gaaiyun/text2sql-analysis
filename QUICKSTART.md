# 快速开始指南

## 1. 安装依赖

```bash
pip install -r requirements.txt
```

## 2. 配置环境变量

```bash
# 复制配置模板
cp .env.example .env

# 编辑配置文件
vim .env
```

**必填配置**:
- `VANNA_API_KEY` - Vanna AI API Key
- `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` - 数据库配置
- `DASHSCOPE_API_KEY` - 阿里云百炼 API Key

## 3. 启动 API 服务

```bash
python api_server.py
```

服务将在 `http://localhost:8000` 启动

## 4. 导入 n8n 工作流

1. 登录 n8n 管理界面
2. 进入 Settings → Workflows
3. 点击 Import
4. 选择 `workflows/text2sql-query.json`
5. 激活工作流

## 5. 测试查询

```bash
curl -X POST http://localhost:8000/api/vanna/query \
  -H "Content-Type: application/json" \
  -d '{"question": "查询所有企业"}'
```

## 6. 测试 n8n 工作流

```bash
curl -X POST http://localhost:5678/webhook/text2sql-query \
  -H "Content-Type: application/json" \
  -d '{"question": "查询注册资本大于 1000 万的企业"}'
```

---

详细文档请查看 [README.md](README.md)
