# 数据库 Schema - 精简版（仅核心表）

**数据库**: gaaiyun (场景 1-3) / gaaiyun_2 (场景 4-5)
**生成时间**: 2026-02-26

---

## 📊 场景 1-3 核心表

### 1. 企业基本信息 (qcc_base_info)
**用途**: 企业基础信息查询

| 字段名 | 类型 | 说明 |
|--------|------|------|
| eid | varchar(255) | 企业唯一标识（主键） |
| credit_no | varchar(255) | 统一社会信用代码 |
| format_name | varchar(255) | 企业名称 |
| regist_capi_new | varchar(255) | 注册资本 |
| start_date | varchar(255) | 成立日期 |
| province_code | varchar(255) | 省份代码 |
| district_code | varchar(255) | 区县代码 |
| new_status_code | varchar(255) | 企业状态 |

### 2. 投资事件 (investment_events)
**用途**: 投融资数据分析

| 字段名 | 类型 | 说明 |
|--------|------|------|
| eid | text | 企业唯一标识 |
| round | text | 融资轮次 |
| amount | double | 融资金额 |
| round_date | datetime | 融资日期 |
| investor | text | 投资方 |

### 3. 企业行业分类 (industry_classification)
**用途**: 行业分析

| 字段名 | 类型 | 说明 |
|--------|------|------|
| eid | text | 企业唯一标识 |
| industry_code | text | 行业代码 |
| industry_name | text | 行业名称 |

---

## 📊 场景 4-5 核心表

### 1. 企业信息 (enterprise_info)
**用途**: 企业尽调和招商清单

| 字段名 | 类型 | 说明 |
|--------|------|------|
| eid | varchar(255) | 企业唯一标识（主键） |
| enterprise_name | varchar(255) | 企业名称 |
| registered_capital | decimal | 注册资本 |
| establishment_date | date | 成立日期 |
| industry | varchar(255) | 所属行业 |
| status | varchar(255) | 企业状态 |

### 2. 知识产权 (intellectual_property)
**用途**: 专利、商标、软著查询

| 字段名 | 类型 | 说明 |
|--------|------|------|
| eid | varchar(255) | 企业唯一标识 |
| patent_count | int | 专利数量 |
| trademark_count | int | 商标数量 |
| software_copyright_count | int | 软著数量 |

### 3. 诉讼信息 (litigation)
**用途**: 司法风险查询

| 字段名 | 类型 | 说明 |
|--------|------|------|
| eid | varchar(255) | 企业唯一标识 |
| case_type | varchar(255) | 案件类型 |
| case_date | date | 立案日期 |
| case_status | varchar(255) | 案件状态 |

### 4. 招投标 (bidding)
**用途**: 商业活动查询

| 字段名 | 类型 | 说明 |
|--------|------|------|
| eid | varchar(255) | 企业唯一标识 |
| bid_type | varchar(255) | 招标/中标 |
| bid_date | date | 日期 |
| bid_amount | decimal | 金额 |

### 5. 融资信息 (financing)
**用途**: 资本情况查询

| 字段名 | 类型 | 说明 |
|--------|------|------|
| eid | varchar(255) | 企业唯一标识 |
| financing_round | varchar(255) | 融资轮次 |
| financing_amount | decimal | 融资金额 |
| financing_date | date | 融资日期 |

---

## 🔗 表关联关系

```
场景 1-3:
企业基本信息.eid = 投资事件.eid
企业基本信息.eid = 企业行业分类.eid

场景 4-5:
企业信息.eid = 知识产权.eid
企业信息.eid = 诉讼信息.eid
企业信息.eid = 招投标.eid
企业信息.eid = 融资信息.eid
```

## ⚠️ 字符集处理

**JOIN 时必须使用 COLLATE**:
```sql
ON b.eid = ic.eid COLLATE utf8mb4_unicode_ci
```

## 📝 SQL 模板

### 场景 1: 数据洞察
```sql
SELECT 
  YEAR(round_date) AS 年份,
  `round` AS 融资轮次,
  COUNT(*) AS 融资次数,
  SUM(amount) AS 融资金额
FROM investment_events
WHERE round_date >= DATE_SUB(CURDATE(), INTERVAL 3 YEAR)
GROUP BY YEAR(round_date), `round`
ORDER BY 年份 DESC, 融资次数 DESC
```

### 场景 4: 招商清单
```sql
SELECT 
  e.enterprise_name AS 企业名称,
  e.registered_capital AS 注册资本,
  e.establishment_date AS 成立时间,
  e.industry AS 所属行业,
  ip.patent_count AS 专利数量
FROM enterprise_info e
LEFT JOIN intellectual_property ip 
  ON e.eid = ip.eid COLLATE utf8mb4_unicode_ci
WHERE e.enterprise_name IN ({企业清单})
  AND e.registered_capital >= 10000000
ORDER BY e.registered_capital DESC
LIMIT 15
```
