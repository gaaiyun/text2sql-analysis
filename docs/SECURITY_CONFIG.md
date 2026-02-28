# ============================================================================
# Text2SQL 安全配置指南
# ============================================================================
#
# ⚠️ 重要安全提示：
# 1. 永远不要将真实的密钥、密码提交到 Git
# 2. 使用环境变量或本地配置文件存储敏感信息
# 3. config.json 使用 ${VAR} 占位符，实际值从环境变量读取
#
# ============================================================================

## 配置方式

### 方式1：使用 .env 文件（推荐）

1. 复制 `.env.example` 为 `.env`
2. 填入真实配置值
3. .env 文件已在 .gitignore 中，不会被提交

### 方式2：设置系统环境变量

**Windows (PowerShell)**:
```powershell
$env:DASHSCOPE_API_KEY="your-api-key"
$env:DB_HOST_SCENARIO_1_3="your-db-host"
$env:DB_PASSWORD_SCENARIO_1_3="your-password"
```

**Linux/macOS**:
```bash
export DASHSCOPE_API_KEY="your-api-key"
export DB_HOST_SCENARIO_1_3="your-db-host"
export DB_PASSWORD_SCENARIO_1_3="your-password"
```

## 必需的环境变量

### 阿里云百炼 API
```
DASHSCOPE_API_KEY=sk-your-api-key-here
```

### 数据库配置 - 场景 1-3
```
DB_HOST_SCENARIO_1_3=your-db-host
DB_PORT_SCENARIO_1_3=3306
DB_NAME_SCENARIO_1_3=Gaaiyun
DB_USER_SCENARIO_1_3=your-username
DB_PASSWORD_SCENARIO_1_3=your-password
```

### 数据库配置 - 场景 4-5
```
DB_HOST_SCENARIO_4_5=your-db-host
DB_PORT_SCENARIO_4_5=3306
DB_NAME_SCENARIO_4_5=gaaiyun_2
DB_USER_SCENARIO_4_5=your-username
DB_PASSWORD_SCENARIO_4_5=your-password
```

## 验证配置

运行以下命令验证配置是否正确：

```bash
python -c "from src.utils.config import Config; c=Config.load(); print('配置加载成功' if c.validate()[0] else '配置有误')"
```

## 安全检查清单

- [ ] .env 文件已添加到 .gitignore
- [ ] config.json 不包含明文密码
- [ ] 所有脚本使用 Config 模块读取配置
- [ ] 测试文件不包含真实密钥
- [ ] 提交前运行 `git diff` 检查敏感信息

## 常见问题

**Q: 为什么 config.json 使用 ${VAR} 占位符？**
A: 这样可以将配置模板提交到 Git，而真实值从环境变量读取，保证安全。

**Q: 如何在不同环境使用不同配置？**
A: 创建 .env.dev、.env.prod 等文件，通过环境变量 ENV=dev 切换。

**Q: 忘记配置环境变量会怎样？**
A: 系统会提示缺少必需的配置，并拒绝启动。
