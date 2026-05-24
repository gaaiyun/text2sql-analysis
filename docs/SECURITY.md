# SQL Security Layers

Text2SQL 给 LLM 自动生成的 SQL 直接喂给数据库执行，必须假设
**LLM 输出 = untrusted input**。本仓库分两层 fail-closed 保护：

## Layer 1: `src/utils/sql_security.py` (v1)

正则黑名单：拦 `DROP / DELETE / INSERT / UPDATE / ALTER / CREATE / TRUNCATE
/ GRANT / EXEC / XP_ / SP_` 等 DDL/DML 关键字 + 经典注入模式（`OR 1=1`、
`UNION SELECT`、`-- 注释截断`、`; DROP` 多语句、`xp_cmdshell`、`/* */`
块注释）。

测试：`tests/test_sql_injection.py` (31 测试) + `tests/test_sql_security.py`
(12 测试)。

**适用**：粗粒度第一道防线，对应用层（用户输入字符串拼接进 SQL）的
SQLi 攻击向量足够。

**不适用**：LLM 自动生成的合法 SELECT 也可能引用敏感表（如 `users`、
`audit_log`）或漏写 LIMIT 拖回全表 —— Layer 1 拦不到。

## Layer 2: `src/utils/safe_sql.py` (v2 新增)

**Schema-aware safety + 自动改写**，用 `sqlparse` 真解析 + 五道检查：

| # | 检查 | 做什么 |
|---|---|---|
| 1 | 多语句 | sqlparse 拆出 >1 个 statement → reject（除非 `allow_multistatement=True`） |
| 2 | 语句类型 | 只允许 `SELECT` 或 `WITH ... SELECT`，其它 reject |
| 3 | Denylist 关键字 | 即使 sqlparse 把恶意字符串识别成 Identifier 也兜底拦 |
| 4 | 表白名单 | 提取 FROM/JOIN 后的表名，与 `allowed_tables` 比对 |
| 5 | 强制 LIMIT | 缺 LIMIT 自动注入 `LIMIT max_limit`；已有但超上限 → 截断 |

返回 `SafeSQLReport`：
- `is_safe`: True/False
- `safe_sql`: 改写后的安全 SQL（None 表示 reject）
- `errors`: 拒绝原因
- `referenced_tables`: 提取出的表名列表
- `modifications`: 改写动作（如"自动添加 LIMIT 1000"）

### 使用

```python
from src.utils.safe_sql import enforce_safe_sql

report = enforce_safe_sql(
    sql=llm_output,
    allowed_tables=["users", "orders", "products"],
    max_limit=1000,
)

if not report.is_safe:
    raise ValueError(f"unsafe SQL: {report.errors}")

# 用改写后的 safe_sql 去查询
cursor.execute(report.safe_sql)
```

### 测试

```bash
pytest tests/test_safe_sql.py
# 38 测试通过：基础 SELECT / 拒绝 DML / 多语句 / 白名单 / LIMIT 改写 /
# WITH CTE / 边界 / 注入风格
```

## 设计原则

1. **Fail-closed**：检查不通过就拒绝，不"修一修"放过。
2. **不替换 sql_security**：Layer 1 仍是第一道防线，Layer 2 是 schema-aware
   补充。生产环境建议两层都跑。
3. **白名单优于黑名单**：表白名单 + SELECT-only 这两个加起来，能挡住绝大
   部分"LLM 瞎编"型攻击面。
4. **不假设数据库会保护自己**：哪怕用了只读账户，业务侧仍要兜这层 ——
   职责分离。

## 已知局限

- `safe_sql` 不防"语义 SQL 注入"（如 `SELECT * FROM users WHERE id = 1 OR 1=1`
  这种合法 SELECT 但泄露全表）。如果业务允许参数化查询，应优先用参数化
  而不是字符串拼接。
- `_extract_tables` 用 sqlparse 启发式，复杂嵌套（如 LATERAL JOIN / VALUES
  子查询）可能漏识别 —— 这种 SQL 通常 LLM 也很少生成。
- 不防资源耗尽（如 `SELECT FLOOR(RAND()*1e9) FROM t`）—— 那是 query
  timeout / row limit 层的事。
