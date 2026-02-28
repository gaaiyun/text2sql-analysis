# ============================================================================
# Text2SQL 安全配置检查清单
# ============================================================================
#
# 在提交代码到 Git 之前，请确保完成以下检查：
#
# ============================================================================

## 提交前检查清单

### 1. 敏感文件检查
- [ ] .env 文件不在提交列表中
- [ ] .env.local 文件不在提交列表中
- [ ] config.json 只包含 ${VAR} 占位符，无明文密码
- [ ] 所有 *.local.json 文件不在提交列表中

### 2. 代码检查
- [ ] 代码中无硬编码的 API 密钥
- [ ] 代码中无硬编码的数据库密码
- [ ] 代码中无硬编码的 IP 地址（除非是示例）
- [ ] 测试文件中无真实的密钥和密码

### 3. Git 检查命令

运行以下命令检查即将提交的内容：

```bash
# 查看即将提交的文件
git status

# 查看文件内容差异
git diff

# 搜索可能的敏感信息
git diff | grep -i "password\|secret\|key\|token"
```

### 4. 自动检查脚本

创建 pre-commit hook（可选）：

```bash
# .git/hooks/pre-commit
#!/bin/bash

# 检查是否包含敏感文件
if git diff --cached --name-only | grep -E "\.env$|\.env\.local$|config\.json$"; then
    echo "错误：不能提交敏感配置文件"
    exit 1
fi

# 检查是否包含明文密码
if git diff --cached | grep -i "password.*=.*[^$]"; then
    echo "警告：可能包含明文密码"
    exit 1
fi

exit 0
```

## 常见错误

### 错误1：不小心提交了 .env 文件

**解决方法**：
```bash
# 从 Git 历史中删除
git rm --cached .env
git commit -m "Remove .env from git"

# 如果已经推送到远程，需要强制推送（谨慎）
git push --force
```

### 错误2：config.json 包含明文密码

**解决方法**：
```bash
# 修改 config.json，使用 ${VAR} 占位符
# 然后提交修复
git add config.json
git commit -m "Fix: use environment variables in config.json"
```

### 错误3：代码中硬编码了密码

**解决方法**：
```bash
# 修改代码，使用配置模块
from src.utils.config import Config
config = Config.load()
password = config.get_database_config('scenario_1_3')['password']

# 提交修复
git add <file>
git commit -m "Fix: remove hardcoded password"
```

## 安全最佳实践

1. **永远不要**在代码中硬编码密码和密钥
2. **永远不要**提交 .env 文件到 Git
3. **定期更换**API 密钥和数据库密码
4. **使用**环境变量或配置文件管理敏感信息
5. **检查** .gitignore 是否正确配置
6. **审查**每次提交的内容
7. **使用** pre-commit hooks 自动检查

## 紧急情况

如果不小心泄露了密钥：

1. **立即更换**泄露的密钥
2. **检查**是否有未授权访问
3. **通知**相关人员
4. **从 Git 历史中删除**敏感信息（使用 git filter-branch 或 BFG Repo-Cleaner）

## 联系方式

如有安全问题，请联系项目维护者。
