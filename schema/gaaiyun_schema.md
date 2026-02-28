# Gaaiyun 数据库 Schema（场景1-3）

**数据库**：Gaaiyun | **字符集**：utf8mb4_unicode_ci | **表数量**：9张

---

## 1. 融资数据 (round_financing)

**用途**：融资趋势分析 | **主键**：import_id | **数据量**：165条

**核心字段**：
- `eid` (varchar) - 企业ID，关联企业基本信息
- `round_date` (datetime) - 融资时间，用于趋势分析
- `round` (varchar) - 融资轮次（天使/A轮/B轮）
- `amount` (double) - 融资金额，单位：万元，可为NULL
- `estimated_amount` (double) - 估算金额，amount为空时使用
- `investors` (text) - 投资方，逗号分隔

**JOIN写法**：
```sql
LEFT JOIN 企业基本信息 b ON 融资数据.eid = b.eid COLLATE utf8mb4_unicode_ci
```

**注意**：使用 `COALESCE(amount, estimated_amount, 0)` 处理NULL

---

## 2. 企业基本信息 (basic_info)

**用途**：企业核心信息，中心关联表 | **主键**：eid

**核心字段**：
- `eid` (varchar) - 企业唯一标识，主键
- `format_name` (varchar) - 企业名称
- `start_date` (date) - 成立日期，计算存续时间
- `regist_capi_new` (varchar) - 注册资本，文本格式如"5000万"
- `province_code` (varchar) - 省份代码，关联行政区划表
- `district_code` (varchar) - 区县代码
- `status` (varchar) - 企业状态（存续/注销/吊销）
- `industry` (varchar) - 所属行业

**数值转换**：
```sql
-- 注册资本转数值
CAST(REPLACE(REPLACE(regist_capi_new, '万', ''), '元', '') AS DECIMAL)

-- 存续年限
DATEDIFF(CURDATE(), start_date)/365
```

---

## 3. 企业行业代码 (industry_code)

**用途**：企业行业分类 | **主键**：import_id | **数据量**：898,079条

**核心字段**：
- `eid` (varchar) - 企业ID
- `name` (varchar) - 行业名称，可为NULL
- `industry_code` (varchar) - 国标行业代码

**JOIN写法**：
```sql
LEFT JOIN 企业行业代码 ic ON b.eid = ic.eid COLLATE utf8mb4_unicode_ci
```

**注意**：一个企业可能有多条记录，统计时用 `COUNT(DISTINCT eid)`，name使用 `COALESCE(name, '未分类')`

---

## 4. 投资数据 (investment)

**用途**：企业对外投资 | **主键**：import_id

**核心字段**：
- `eid` (varchar) - 投资方企业ID
- `invest_eid` (varchar) - 被投资企业ID
- `stock_percent` (varchar) - 持股比例，文本格式
- `invest_name` (varchar) - 被投资企业名称

---

## 5. 招投标 (bidding)

**用途**：招投标项目信息

**核心字段**：
- `eid` (varchar) - 企业ID
- `title` (varchar) - 项目标题
- `publish_time` (datetime) - 发布时间
- `notice_type_main` (varchar) - 公告类型（中标公告等）

---

## 6. 产品数据 (product)

**用途**：企业产品信息 | **主键**：import_id

**核心字段**：
- `eid` (varchar) - 企业ID
- `pro_name` (varchar) - 产品名称
- `kind` (varchar) - 产品类型

---

## 7. 标签数据 (tags)

**用途**：企业标签和资质

**核心字段**：
- `eid` (varchar) - 企业ID
- `name` (varchar) - 标签名称（如"高新技术企业"）
- `type` (varchar) - 标签类型

---

## 8. 行业代码表 (industry_code_table)

**用途**：国标行业分类体系（门类/大类/中类/小类）

**核心字段**：
- `industry_code` (varchar) - 完整行业代码
- `门类名称` (varchar) - 一级分类
- `大类名称` (varchar) - 二级分类
- `中类名称` (varchar) - 三级分类

**JOIN写法**：
```sql
LEFT JOIN 行业代码表 ict ON ic.industry_code = ict.industry_code
```

---

## 9. 行政区划代码表 (admin_division)

**用途**：省市区三级行政区划 | **主键**：import_id

**核心字段**：
- `type_code` (bigint) - 行政区划代码（6位）
- `admin_name` (varchar) - 行政区划全称
- `行政区划等级` (bigint) - 1省/2市/3区县

**JOIN写法**：
```sql
LEFT JOIN 行政区划代码表 ac ON b.province_code = ac.type_code
WHERE ac.行政区划等级 = 1  -- 省级
```

---

## 常用查询模式

### 融资趋势分析
```sql
SELECT 
    YEAR(round_date) AS 年份,
    COUNT(*) AS 融资次数,
    COALESCE(SUM(amount), 0) AS 总金额
FROM 融资数据
WHERE round_date >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
GROUP BY YEAR(round_date)
ORDER BY 年份
LIMIT 20
```

### 行业分布统计
```sql
SELECT 
    COALESCE(ic.name, '未分类') AS 行业,
    COUNT(DISTINCT b.eid) AS 企业数量
FROM 企业基本信息 b
LEFT JOIN 企业行业代码 ic ON b.eid = ic.eid COLLATE utf8mb4_unicode_ci
WHERE b.start_date >= DATE_SUB(CURDATE(), INTERVAL 3 YEAR)
GROUP BY ic.name
ORDER BY 企业数量 DESC
LIMIT 20
```

### 地区企业分析
```sql
SELECT 
    ac.admin_name AS 省份,
    COUNT(DISTINCT b.eid) AS 企业数量
FROM 企业基本信息 b
LEFT JOIN 行政区划代码表 ac ON b.province_code = ac.type_code
WHERE ac.行政区划等级 = 1
GROUP BY ac.admin_name
ORDER BY 企业数量 DESC
LIMIT 20
```

---

## 重要规则

1. **JOIN必须COLLATE**：`ON a.eid = b.eid COLLATE utf8mb4_unicode_ci`
2. **禁止SELECT ***：明确指定字段
3. **时间范围**：默认近3年 `WHERE date >= DATE_SUB(CURDATE(), INTERVAL 3 YEAR)`
4. **结果限制**：`LIMIT 1000`
5. **单个SELECT**：不允许多语句
6. **NULL处理**：`COALESCE(field, default)`
7. **去重统计**：`COUNT(DISTINCT eid)`
