# 🚀 快速开始指南

## 本地部署步骤

### 1. 环境准备

**系统要求**
- Python 3.8+
- MySQL 5.7+ 或 8.0+
- 4GB+ RAM
- 网络连接（用于LLM API调用）

**克隆项目**
```bash
git clone https://github.com/gaaiyun/text2sql-analysis.git
cd text2sql-analysis
```

### 2. 安装依赖

```bash
# 创建虚拟环境（推荐）
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 配置环境变量

创建 `.env` 文件：

```bash
# 阿里云百炼API配置
DASHSCOPE_API_KEY=your_api_key_here

# MySQL数据库配置
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=gaaiyun

# 可选：网络搜索API
SERPER_API_KEY=your_serper_key  # 或使用DuckDuckGo（无需key）
```

### 4. 准备数据库

```bash
# 导入示例数据（如果有SQL文件）
mysql -u root -p gaaiyun < data/sample_data.sql

# 或手动创建数据库
mysql -u root -p
CREATE DATABASE gaaiyun CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. 启动应用

**方式1：Web界面（推荐）**
```bash
python web_app.py
```
访问：http://localhost:7860

**方式2：API服务**
```bash
python api_server.py
```
API文档：http://localhost:8000/docs

**方式3：命令行Demo**
```bash
python demo/demo_scenario_1.py
```

### 6. 验证安装

运行快速测试：
```bash
python scripts/test_quick.py
```

---

## 常见问题

### Q1: 依赖安装失败
```bash
# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q2: MySQL连接失败
- 检查MySQL服务是否启动
- 确认用户名密码正确
- 检查防火墙设置

### Q3: API Key无效
- 访问 https://dashscope.console.aliyun.com/ 获取API Key
- 确保账户有足够余额

### Q4: 端口被占用
```bash
# 修改端口
python web_app.py --port 8080
```

---

## 目录结构

```
text2sql/
├── web_app.py              # Web应用入口
├── api_server.py           # API服务入口
├── .env                    # 环境变量配置
├── requirements.txt        # Python依赖
├── schema/                 # 数据库Schema定义
│   ├── gaaiyun_schema.md
│   └── question_sql_examples.md
├── demo/                   # 示例代码
│   ├── demo_scenario_*.py
│   └── api_examples/
├── src/utils/              # 核心工具
│   ├── chart_generator.py
│   ├── document_generator.py
│   └── web_search.py
└── outputs/                # 生成的报告和图表
```

---

## 下一步

- 📖 阅读 [WEB_APP_GUIDE.md](WEB_APP_GUIDE.md) 了解Web界面使用
- 🔧 查看 [demo/](demo/) 目录学习API调用
- 🚀 参考 [AGENT_UPGRADE.md](AGENT_UPGRADE.md) 了解Agent化升级方案
- 📊 运行 `demo/run_all_demos.py` 查看完整示例

---

Made with ❤️ by gaaiyun
