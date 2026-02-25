# 🚀 Text2SQL 项目执行计划

> **创建时间**: 2026-02-26 03:40  
> **执行模式**: ReAct 自我监督  
> **执行官**: 派蒙

---

## 📊 任务总览

| 阶段 | 任务 | 预计时间 | 状态 |
|------|------|---------|------|
| **阶段 1** | 连接数据库，获取 Schema | 10 分钟 | ⏳ 进行中 |
| **阶段 2** | 配置 Vanna AI | 15 分钟 | ⏳ 等待中 |
| **阶段 3** | 创建 n8n 工作流 | 20 分钟 | ⏳ 等待中 |
| **阶段 4** | 生成提示词模板 | 15 分钟 | ⏳ 等待中 |

---

## 🎯 阶段 1: 连接数据库获取 Schema

### 任务清单
- [ ] 安装 PyMySQL 库
- [ ] 连接 MySQL 数据库 (场景 1-3: Gaaiyun)
- [ ] 提取所有表名
- [ ] 提取每个表的核心字段
- [ ] 生成精简 Schema 文档

### 数据库信息
```
Host: 8.134.9.77
Port: 3306
User: Gaaiyun
Password: Why513338
Database: Gaaiyun
```

### 输出文件
- `schema_gaaiyun.md` - 精简 Schema 文档
- `schema_gaaiyun_2.md` - 场景 4-5 Schema

---

## 🎯 阶段 2: 配置 Vanna AI

### 任务清单
- [ ] 安装 Vanna AI + MySQL 支持
- [ ] 配置百炼 API (Qwen3.5 Plus)
- [ ] 连接数据库
- [ ] 导入训练数据 (基于 Schema)
- [ ] 测试 Text2SQL 查询

### 配置信息
```
API Key: sk-sp-0b28da8e3f404df182c05d3fd45787a5
Model: qwen-plus
```

### 输出文件
- `vanna_config.py` - Vanna 配置脚本
- `vanna_train.py` - 训练数据导入脚本

---

## 🎯 阶段 3: 创建 n8n 工作流

### 任务清单
- [ ] 设计工作流架构 (单 Agent 模式)
- [ ] 创建工作流 JSON
- [ ] 配置 Webhook 节点
- [ ] 配置 HTTP Request 节点 (Vanna API)
- [ ] 配置 Code 节点 (数据处理)
- [ ] 配置 Markdown 输出节点
- [ ] 测试工作流

### 工作流架构
```
Webhook → 任务分类 → 批量 SQL 查询 → 数据处理 → Markdown 输出
```

### 输出文件
- `n8n_workflow.json` - 可导入的工作流配置

---

## 🎯 阶段 4: 生成提示词模板

### 任务清单
- [ ] 场景 1: 数据洞察提示词
- [ ] 场景 2: 地区产业分析提示词
- [ ] 场景 3: 特定行业分析提示词
- [ ] 场景 4: 招商清单提示词
- [ ] 场景 5: 企业尽调报告提示词

### 每个模板包含
- 系统提示词 (分析维度定义)
- SQL 查询模板 (表→字段→规则)
- 风险处理规则 (数据缺失/插件失败)

### 输出文件
- `prompts/scene1_data_insight.md`
- `prompts/scene2_region_analysis.md`
- `prompts/scene3_industry_analysis.md`
- `prompts/scene4_investment_list.md`
- `prompts/scene5_due_diligence.md`

---

## 👁️ 监督派蒙检查点

### 检查频率
- 每完成 1 个阶段 → 更新进度
- 遇到问题 → 立即报告
- 完成所有任务 → 生成总结报告

### 进度追踪
```
[2026-02-26 03:40] ✅ ReAct 系统启动
[2026-02-26 03:40] ⏳ 阶段 1: 连接数据库 (进行中)
[2026-02-26 ??:??] ⏳ 阶段 2: 配置 Vanna AI (等待中)
[2026-02-26 ??:??] ⏳ 阶段 3: 创建 n8n 工作流 (等待中)
[2026-02-26 ??:??] ⏳ 阶段 4: 生成提示词模板 (等待中)
```

---

_创建者：指挥官派蒙 ⭐_
