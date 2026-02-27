# Text2SQL 项目 - 完整 Schema 文档

> **合并自**: schema_gaaiyun.md + schema_gaaiyun_2.md + schema_gaaiyun_essential.md  
> **更新日期**: 2026-02-27

---

## 📊 数据库概览

系统使用两个 MySQL 数据库：

| 数据库 | 主机 | 端口 | 用途 |
|--------|------|------|------|
| Gaaiyun | ${DB_HOST} | 3306 | 场景 1-3（数据洞察、地区产业、行业分析） |
| gaaiyun_2 | ${DB_HOST} | 3306 | 场景 4-5（招商清单、企业尽调） |

---

## 📋 场景 1-3 核心表（Gaaiyun 数据库）

### 1. 企业基本信息 (qcc_base_info)

**用途**: 企业基础信息查询

| 字段名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| eid | varchar(255) | 企业唯一标识（主键） | "1234567890" |
| credit_no | varchar(255) | 统一社会信用代码 | "91110000MA00000000" |
| format_name | varchar(255) | 企业名称 | "某某科技有限公司" |
| regist_capi_new | varchar(255) | 注册资本 | "1000 万人民币" |
| start_date | varchar(255) | 成立日期 | "2020-01-01" |
| province_code | varchar(255) | 省份代码 | "110000" |
| district_code | varchar(255) | 区县代码 | "110100" |
| new_status_code | varchar(255) | 企业状态 | "存续" |

**示例查询**:
```sql
SELECT format_name, regist_capi_new, start_date
FROM qcc_base_info
WHERE province_code = '110000'
LIMIT 10;
```

---

### 2. 投资事件 (investment_events)

**用途**: 投融资数据分析

| 字段名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| eid | text | 企业唯一标识 | "1234567890" |
| round | text | 融资轮次 | "A 轮" |
| amount | double | 融资金额（万元） | 5000.0 |
| round_date | datetime | 融资日期 | "2023-06-15" |
| investor | text | 投资方 | "某某创投" |

**示例查询**:
```sql
SELECT 
  YEAR(round_date) AS 年份，
  `round` AS 融资轮次，
  COUNT(*) AS 融资次数，
  SUM(amount) AS 融资金额
FROM investment_events
WHERE round_date >= DATE_SUB(CURDATE(), INTERVAL 3 YEAR)
GROUP BY YEAR(round_date), `round`
ORDER BY 年份 DESC;
```

---

### 3. 企业行业分类 (industry_classification)

**用途**: 行业分析

| 字段名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| eid | text | 企业唯一标识 | "1234567890" |
| industry_code | text | 行业代码 | "I6510" |
| industry_name | text | 行业名称 | "软件开发" |

**示例查询**:
```sql
SELECT 
  ic.industry_name AS 行业，
  COUNT(*) AS 企业数量，
  SUM(CASE WHEN qb.regist_capi_new LIKE '%万%' 
      THEN CAST(REPLACE(qb.regist_capi_new, '万人民币', '') AS DECIMAL)
      ELSE 0 END) AS 总注册资本
FROM industry_classification ic
JOIN qcc_base_info qb ON ic.eid = qb.eid COLLATE utf8mb4_unicode_ci
GROUP BY ic.industry_name
ORDER BY 企业数量 DESC
LIMIT 20;
```

---

## 📋 场景 4-5 核心表（gaaiyun_2 数据库）

### 1. 企业信息 (enterprise_info)

**用途**: 企业尽调和招商清单

| 字段名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| eid | varchar(255) | 企业唯一标识（主键） | "1234567890" |
| enterprise_name | varchar(255) | 企业名称 | "某某科技有限公司" |
| registered_capital | decimal | 注册资本（元） | 10000000.00 |
| establishment_date | date | 成立日期 | "2020-01-01" |
| industry | varchar(255) | 所属行业 | "软件和信息技术服务业" |
| status | varchar(255) | 企业状态 | "存续" |

**示例查询**:
```sql
SELECT 
  enterprise_name,
  registered_capital,
  establishment_date,
  industry
FROM enterprise_info
WHERE registered_capital >= 10000000
  AND status = '存续'
ORDER BY registered_capital DESC
LIMIT 15;
```

---

### 2. 知识产权 (intellectual_property)

**用途**: 专利、商标、软著查询

| 字段名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| eid | varchar(255) | 企业唯一标识 | "1234567890" |
| patent_count | int | 专利数量 | 50 |
| trademark_count | int | 商标数量 | 20 |
| software_copyright_count | int | 软著数量 | 30 |

**示例查询**:
```sql
SELECT 
  e.enterprise_name AS 企业名称，
  ip.patent_count AS 专利数量，
  ip.trademark_count AS 商标数量，
  ip.software_copyright_count AS 软著数量
FROM enterprise_info e
LEFT JOIN intellectual_property ip ON e.eid = ip.eid COLLATE utf8mb4_unicode_ci
WHERE ip.patent_count > 10
ORDER BY ip.patent_count DESC;
```

---

### 3. 诉讼信息 (litigation)

**用途**: 司法风险查询

| 字段名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| eid | varchar(255) | 企业唯一标识 | "1234567890" |
| case_type | varchar(255) | 案件类型 | "民事案件" |
| case_date | date | 立案日期 | "2023-01-15" |
| case_status | varchar(255) | 案件状态 | "已结案" |

**示例查询**:
```sql
SELECT 
  e.enterprise_name AS 企业名称，
  l.case_type AS 案件类型，
  l.case_date AS 立案日期，
  l.case_status AS 案件状态
FROM enterprise_info e
JOIN litigation l ON e.eid = l.eid COLLATE utf8mb4_unicode_ci
WHERE l.case_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
ORDER BY l.case_date DESC;
```

---

### 4. 招投标 (bidding)

**用途**: 商业活动查询

| 字段名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| eid | varchar(255) | 企业唯一标识 | "1234567890" |
| bid_type | varchar(255) | 招标/中标 | "中标" |
| bid_date | date | 日期 | "2023-06-01" |
| bid_amount | decimal | 金额（元） | 5000000.00 |

**示例查询**:
```sql
SELECT 
  e.enterprise_name AS 企业名称，
  b.bid_type AS 类型，
  b.bid_date AS 日期，
  b.bid_amount AS 金额
FROM enterprise_info e
JOIN bidding b ON e.eid = b.eid COLLATE utf8mb4_unicode_ci
WHERE b.bid_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
ORDER BY b.bid_amount DESC
LIMIT 20;
```

---

### 5. 融资信息 (financing)

**用途**: 资本情况查询

| 字段名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| eid | varchar(255) | 企业唯一标识 | "1234567890" |
| financing_round | varchar(255) | 融资轮次 | "B 轮" |
| financing_amount | decimal | 融资金额（元） | 100000000.00 |
| financing_date | date | 融资日期 | "2023-03-20" |

**示例查询**:
```sql
SELECT 
  e.enterprise_name AS 企业名称，
  f.financing_round AS 轮次，
  f.financing_amount AS 金额，
  f.financing_date AS 日期
FROM enterprise_info e
JOIN financing f ON e.eid = f.eid COLLATE utf8mb4_unicode_ci
WHERE f.financing_date >= DATE_SUB(CURDATE(), INTERVAL 2 YEAR)
ORDER BY f.financing_amount DESC;
```

---

## 🔗 表关联关系

### 场景 1-3 关联
```
企业基本信息 (qcc_base_info)
  ├─ 投资事件 (investment_events) ON eid
  └─ 企业行业分类 (industry_classification) ON eid
```

### 场景 4-5 关联
```
企业信息 (enterprise_info)
  ├─ 知识产权 (intellectual_property) ON eid
  ├─ 诉讼信息 (litigation) ON eid
  ├─ 招投标 (bidding) ON eid
  └─ 融资信息 (financing) ON eid
```

---

## ⚠️ 重要注意事项

### 1. 字符集处理

**JOIN 时必须使用 COLLATE**:
```sql
-- 正确的 JOIN 方式
SELECT * FROM table1 t1
JOIN table2 t2 ON t1.eid = t2.eid COLLATE utf8mb4_unicode_ci;

-- 错误的 JOIN 方式（可能导致字符集冲突）
SELECT * FROM table1 t1
JOIN table2 t2 ON t1.eid = t2.eid;
```

### 2. 金额单位

- **投资事件**: amount 单位为**万元**
- **场景 4-5**: registered_capital、financing_amount 单位为**元**

### 3. 日期格式

- 所有日期字段使用 `DATE` 或 `DATETIME` 类型
- 查询时使用 `DATE_SUB(CURDATE(), INTERVAL X YEAR/MONTH/DAY)`

### 4. 文本字段

- `round` 是 MySQL 保留字，查询时需要用反引号：`` `round` ``
- 所有 text 字段注意字符集兼容性

---

## 📝 常用 SQL 模板

### 场景 1: 数据洞察
```sql
SELECT 
  YEAR(round_date) AS 年份，
  `round` AS 融资轮次，
  COUNT(*) AS 融资次数，
  SUM(amount) AS 融资金额（万元）
FROM investment_events
WHERE round_date >= DATE_SUB(CURDATE(), INTERVAL 3 YEAR)
GROUP BY YEAR(round_date), `round`
ORDER BY 年份 DESC, 融资次数 DESC;
```

### 场景 2: 地区产业分析
```sql
SELECT 
  qb.province_code AS 省份，
  ic.industry_name AS 行业，
  COUNT(*) AS 企业数量
FROM qcc_base_info qb
JOIN industry_classification ic ON qb.eid = ic.eid COLLATE utf8mb4_unicode_ci
WHERE qb.province_code = '110000'
GROUP BY qb.province_code, ic.industry_name
ORDER BY 企业数量 DESC
LIMIT 20;
```

### 场景 3: 行业对比分析
```sql
SELECT 
  ic.industry_name AS 行业，
  COUNT(DISTINCT qb.eid) AS 企业数量，
  AVG(CAST(REPLACE(qb.regist_capi_new, '万人民币', '') AS DECIMAL)) AS 平均注册资本
FROM industry_classification ic
JOIN qcc_base_info qb ON ic.eid = qb.eid COLLATE utf8mb4_unicode_ci
WHERE ic.industry_name IN ('软件开发', '人工智能', '大数据')
GROUP BY ic.industry_name
ORDER BY 平均注册资本 DESC;
```

### 场景 4: 招商清单
```sql
SELECT 
  e.enterprise_name AS 企业名称，
  e.registered_capital AS 注册资本，
  e.establishment_date AS 成立时间，
  e.industry AS 所属行业，
  ip.patent_count AS 专利数量
FROM enterprise_info e
LEFT JOIN intellectual_property ip ON e.eid = ip.eid COLLATE utf8mb4_unicode_ci
WHERE e.enterprise_name IN ({企业清单})
  AND e.registered_capital >= 10000000
ORDER BY e.registered_capital DESC
LIMIT 15;
```

### 场景 5: 企业尽调
```sql
SELECT 
  e.enterprise_name AS 企业名称，
  e.registered_capital AS 注册资本，
  e.establishment_date AS 成立时间，
  ip.patent_count AS 专利，
  ip.trademark_count AS 商标，
  COUNT(DISTINCT l.eid) AS 诉讼数量，
  COUNT(DISTINCT b.eid) AS 招投标数量
FROM enterprise_info e
LEFT JOIN intellectual_property ip ON e.eid = ip.eid COLLATE utf8mb4_unicode_ci
LEFT JOIN litigation l ON e.eid = l.eid COLLATE utf8mb4_unicode_ci
LEFT JOIN bidding b ON e.eid = b.eid COLLATE utf8mb4_unicode_ci
WHERE e.eid = '{目标企业 ID}'
GROUP BY e.eid, e.enterprise_name, e.registered_capital, e.establishment_date,
         ip.patent_count, ip.trademark_count;
```

---

<div align="center">

**文档合并完成** | 2026-02-27

</div>
