from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = REPO_ROOT / "schema"


@dataclass(frozen=True)
class DatabaseProfile:
    name: str
    scenario_key: str
    schema_path: Path
    allowed_tables: tuple[str, ...]
    compatibility_views: tuple[str, ...]
    sql_guidance: str

    def load_schema(self) -> str:
        return self.schema_path.read_text(encoding="utf-8")


ZNJZ_ALLOWED_TABLES = (
    "企业基本信息",
    "企业基本信息_行业代码",
    "企业融资信息",
    "企业投资股东信息",
    "招投标信息",
    "商标资质信息",
    "企业行业代码",
    "融资数据",
    "投资数据",
    "招投标",
    "标签数据",
)

ZNJZ_COMPATIBILITY_VIEWS = (
    "企业行业代码",
    "融资数据",
    "投资数据",
    "招投标",
    "标签数据",
)

ZNJZ_SQL_GUIDANCE = """## znjz 专用 SQL 编写指南

### 白名单对象
只能引用以下表或视图，不要引用任何其他对象：
`企业基本信息`、`企业基本信息_行业代码`、`企业融资信息`、`企业投资股东信息`、`招投标信息`、`商标资质信息`、`企业行业代码`、`融资数据`、`投资数据`、`招投标`、`标签数据`。

### 字段与口径
- 禁止虚构字段。只能使用 Schema 中明确存在的字段。
- 企业主键统一使用 `eid`，企业名称使用 `name`。
- 企业经营状态使用 `企业基本信息`.`status`。
- 注册资本数值使用 `企业基本信息`.`regist_capi_new`。
- 成立时间使用 `企业基本信息`.`start_date`。
- 登记地区使用 `企业基本信息`.`district_code`；当前库没有地区名称表，只能返回地区代码。
- 行业聚合使用 `企业行业代码`.`industry_code`，当前库没有行业名称表，只能返回行业代码。
- 融资分析优先使用 `融资数据`：`round`、`round_date`、`amount`、`estimated_amount`、`currency`、`investors`。
- 投资分析优先使用 `投资数据`：`eid` 为投资主体，`invest_eid`/`invest_name` 为被投资企业。
- 招投标分析优先使用 `招投标`：`title`、`publish_time`、`area_code`、`project_bid_money`。
- 资质/商标分析优先使用 `标签数据`：`year`、`publish_date`、`level`、`state`、`district_code`；如需原始字段可用 `商标资质信息`.`ct_year`。

### 标准问题模板
- 经营状态：`SELECT `status`, COUNT(*) AS cnt FROM `企业基本信息` GROUP BY `status` ORDER BY cnt DESC LIMIT 100`
- 行业 Top：`SELECT `industry_code`, COUNT(*) AS enterprise_count FROM `企业行业代码` WHERE `industry_code` IS NOT NULL GROUP BY `industry_code` ORDER BY enterprise_count DESC LIMIT 20`
- 融资轮次：`SELECT `round`, COUNT(DISTINCT `eid`) AS enterprise_count, SUM(`amount`) AS total_amount FROM `融资数据` GROUP BY `round` ORDER BY enterprise_count DESC LIMIT 100`
- 招投标年度：`SELECT YEAR(`publish_time`) AS year, COUNT(*) AS bid_count FROM `招投标` WHERE `publish_time` IS NOT NULL GROUP BY YEAR(`publish_time`) ORDER BY year DESC LIMIT 100`
- 企业详情：从 `企业基本信息` 选一家公司，再 LEFT JOIN `企业行业代码`、`融资数据`、`投资数据`、`招投标` 的聚合子查询；子查询别名只能作为别名，不要把别名当表名。

### JOIN 与子查询规则
- 跨表关联统一使用 `eid`：`base`.`eid` = `view`.`eid`。
- 对一对多事实表做企业详情时，先在子查询内按 `eid` 聚合，再 JOIN 到企业主表，避免笛卡尔积。
- 不要使用 `SELECT *`。
- GROUP BY 和 ORDER BY 优先使用原始字段或表达式，避免依赖中文别名。
- 所有中文表名、视图名、字段名和保留字字段如 `round` 必须加反引号。
"""


def get_database_profile(name: str = "znjz") -> DatabaseProfile:
    normalized = (name or "znjz").lower()
    if normalized not in {"znjz", "scenario_1_3"}:
        raise ValueError(f"Unsupported database profile: {name}")
    return DatabaseProfile(
        name="znjz",
        scenario_key="scenario_1_3",
        schema_path=SCHEMA_DIR / "znjz_text2sql_schema.md",
        allowed_tables=ZNJZ_ALLOWED_TABLES,
        compatibility_views=ZNJZ_COMPATIBILITY_VIEWS,
        sql_guidance=ZNJZ_SQL_GUIDANCE,
    )
