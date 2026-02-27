# Vanna AI 配置指南

> 本指南帮助你快速配置 Vanna AI 和 Text2SQL 系统

---

## 📋 配置步骤

### 步骤 1: 复制配置文件

```bash
cd C:\Users\gaaiy\Desktop\text2sql
copy config.template.json config.json
```

### 步骤 2: 填写 API Keys

编辑 `config.json`，填写以下必需配置：

```json
{
  "database": {
    "scenario_1_3": {
      "host": "8.134.9.77",
      "port": 3306,
      "user": "Gaaiyun",
      "password": "Why513338",
      "database": "Gaaiyun"
    },
    "scenario_4_5": {
      "host": "8.134.9.77",
      "port": 3306,
      "user": "gaaiyun_2",
      "password": "Why513338",
      "database": "gaaiyun_2"
    }
  },
  
  "bailian": {
    "api_key": "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "base_url": "https://coding.dashscope.aliyuncs.com/v1",
    "model": "qwen3.5-plus"
  },
  
  "vanna": {
    "api_key": "your-vanna-api-key",
    "org": "your-org-name",
    "model": "your-model-name"
  }
}
```

### 步骤 3: 获取 Vanna API Key

1. 访问 [Vanna AI 官网](https://vanna.ai/)
2. 注册账号
3. 创建 Organization
4. 获取 API Key

### 步骤 4: 训练 Vanna

```bash
python scripts/train_vanna.py
```

### 步骤 5: 启动 API 服务

```bash
python api/vanna_server.py
```

服务将在 `http://localhost:5000` 启动。

---

## 🔧 测试配置

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

---

## 📝 配置说明

### 数据库配置

| 字段 | 说明 | 示例 |
|------|------|------|
| host | 数据库主机地址 | 8.134.9.77 |
| port | 数据库端口 | 3306 |
| user | 数据库用户名 | Gaaiyun |
| password | 数据库密码 | Why513338 |
| database | 数据库名称 | Gaaiyun |

### 阿里云百炼配置

| 字段 | 说明 | 获取方式 |
|------|------|---------|
| api_key | DashScope API Key | [阿里云百炼控制台](https://bailian.console.aliyun.com/) |
| base_url | API 基础 URL | https://coding.dashscope.aliyuncs.com/v1 |
| model | 模型名称 | qwen3.5-plus |

### Vanna 配置

| 字段 | 说明 | 获取方式 |
|------|------|---------|
| api_key | Vanna API Key | Vanna AI 官网 |
| org | 组织名称 | 创建组织时设定 |
| model | 模型名称 | 创建模型时设定 |

---

## ⚠️ 安全提示

1. **不要将 `config.json` 上传到 GitHub**
   - 已添加到 `.gitignore`
   - 仅使用 `config.template.json` 作为模板

2. **定期更新 API Keys**
   - 建议每 3 个月更新一次
   - 如发现泄露立即更换

3. **使用只读数据库账号**
   - 生产环境使用只读权限
   - 限制查询范围

---

## 🐛 故障排查

### 问题 1: 无法连接数据库

```
Error: Can't connect to MySQL server
```

**解决方案**:
- 检查数据库主机是否可访问
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

---

## 📞 获取帮助

- **项目文档**: README.md
- **测试报告**: FINAL_TEST_REPORT.md
- **GitHub**: https://github.com/gaaiyun/text2sql-analysis

---

<div align="center">

**Made with ❤️ by 派蒙 + Gaaiyun**

*2026-02-26*

</div>
