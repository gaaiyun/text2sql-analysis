# gaaiyun_2 数据库 Schema（场景4-5）

**数据库**：gaaiyun_2 | **字符集**：utf8mb4_unicode_ci | **表数量**：125张（精简到20张核心表）

---

## 核心表概览

### 企业基础信息类
1. 企业信息 (company_info) - 企业基本资料
2. 企业变更 (company_change) - 变更记录
3. 股东信息 (shareholder) - 股权结构

### 知识产权类
4. 专利信息 (patent) - 专利数据
5. 商标信息 (trademark) - 商标数据
6. 软件著作权 (software_copyright) - 软著数据

### 法律风险类
7. 诉讼信息 (lawsuit) - 法律诉讼
8. 被执行人 (executed_person) - 执行案件
9. 失信信息 (dishonest) - 失信记录

### 经营能力类
10. 招投标 (bidding) - 招投标项目
11. 中标信息 (winning_bid) - 中标记录
12. 纳税信息 (tax) - 纳税数据

### 财务健康类
13. 年报数据 (annual_report) - 企业年报
14. 融资信息 (financing) - 融资记录

---

## 1. 企业信息 (company_info)

**用途**：企业核心信息，场景4-5的中心表 | **主键**：eid

**核心字段**：
- `eid` (varchar) - 企业唯一标识
- `企业名称` (varchar) - 标准企业名称
- `注册资本` (varchar) - 注册资本，文本格式
- `成立日期` (date) - 成立时间
- `企业状态` (varchar) - 存续/注销/吊销
- `所属行业` (varchar) - 行业分类
- `注册地址` (varchar) - 注册地址
- `经营范围` (text) - 经营范围描述

**数值转换**：
```sql
-- 注册资本转数值（单位：万元）
CAST(REPLACE(REPLACE(注册资本, '万元', ''), '万', '') AS DECIMAL)

-- 存续年限
DATEDIFF(CURDATE(), 成立日期)/365
```

**JOIN基础**：所有表通过 `eid` 关联，必须使用 `COLLATE utf8mb4_unicode_ci`

---

## 2. 专利信息 (patent)

**用途**：企业专利数据，评估创新能力

**核心字段**：
- `eid` (varchar) - 企业ID
- `专利ID` (varchar) - 专利唯一标识
- `专利名称` (varchar) - 专利标题
- `专利类型` (varchar) - 发明/实用新型/外观设计
- `申请日期` (date) - 申请时间
- `授权日期` (date) - 授权时间
- `专利状态` (varchar) - 有效/失效

**统计示例**：
```sql
SELECT 
    e.企业名称,
    COUNT(DISTINCT p.专利ID) AS 专利数量,
    SUM(CASE WHEN p.专利类型='发明专利' THEN 1 ELSE 0 END) AS 发明专利数
FROM 企业信息 e
LEFT JOIN 专利信息 p ON e.eid = p.eid COLLATE utf8mb4_unicode_ci
WHERE p.专利状态 = '有效'
GROUP BY e.eid
```

---

## 3. 诉讼信息 (lawsuit)

**用途**：法律诉讼记录，评估法律风险

**核心字段**：
- `eid` (varchar) - 企业ID
- `诉讼ID` (varchar) - 案件标识
- `案由` (varchar) - 案件类型
- `案件状态` (varchar) - 已结案/审理中
- `立案日期` (date) - 立案时间
- `原告` (varchar) - 原告方
- `被告` (varchar) - 被告方

**风险评估**：
```sql
SELECT 
    e.企业名称,
    COUNT(DISTINCT l.诉讼ID) AS 诉讼次数,
    SUM(CASE WHEN l.被告 LIKE CONCAT('%', e.企业名称, '%') THEN 1 ELSE 0 END) AS 作为被告次数
FROM 企业信息 e
LEFT JOIN 诉讼信息 l ON e.eid = l.eid COLLATE utf8mb4_unicode_ci
WHERE l.立案日期 >= DATE_SUB(CURDATE(), INTERVAL 3 YEAR)
GROUP BY e.eid
```

---

## 4. 招投标 (bidding)

**用途**：招投标项目，评估经营能力

**核心字段**：
- `eid` (varchar) - 企业ID
- `投标ID` (varchar) - 项目标识
- `项目名称` (varchar) - 项目标题
- `发布时间` (date) - 公告时间
- `项目金额` (decimal) - 项目金额，单位：万元
- `中标状态` (varchar) - 中标/未中标

**统计示例**：
```sql
SELECT 
    e.企业名称,
    COUNT(DISTINCT b.投标ID) AS 投标次数,
    SUM(CASE WHEN b.中标状态='中标' THEN 1 ELSE 0 END) AS 中标次数,
    COALESCE(SUM(CASE WHEN b.中标状态='中标' THEN b.项目金额 ELSE 0 END), 0) AS 中标总金额
FROM 企业信息 e
LEFT JOIN 招投标 b ON e.eid = b.eid COLLATE utf8mb4_unicode_ci
WHERE b.发布时间 >= DATE_SUB(CURDATE(), INTERVAL 3 YEAR)
GROUP BY e.eid
```

---

## 5. 纳税信息 (tax)

**用途**：纳税数据，评估财务健康

**核心字段**：
- `eid` (varchar) - 企业ID
- `纳税年度` (varchar) - 年份
- `纳税等级` (varchar) - A/B/C/D级
- `纳税金额` (decimal) - 纳税额，单位：万元

---

## 场景4：招商清单 - 8维度评估

### 评估维度与SQL模板

**维度1：注册资本**
```sql
SELECT 
    企业名称,
    CAST(REPLACE(REPLACE(注册资本, '万元', ''), '万', '') AS DECIMAL) AS 注册资本数值,
    CASE 
        WHEN CAST(REPLACE(REPLACE(注册资本, '万元', ''), '万', '') AS DECIMAL) >= 1000 THEN 2
        WHEN CAST(REPLACE(REPLACE(注册资本, '万元', ''), '万', '') AS DECIMAL) >= 500 THEN 1
        ELSE 0
    END AS 注册资本评分
FROM 企业信息
WHERE 企业名称 IN ('企业A', '企业B', '企业C')
```

**维度2：存续时间**
```sql
SELECT 
    企业名称,
    DATEDIFF(CURDATE(), 成立日期)/365 AS 存续年限,
    CASE 
        WHEN DATEDIFF(CURDATE(), 成立日期)/365 >= 5 THEN 2
        WHEN DATEDIFF(CURDATE(), 成立日期)/365 >= 3 THEN 1
        ELSE 0
    END AS 存续时间评分
FROM 企业信息
WHERE 企业名称 IN ('企业A', '企业B', '企业C')
```

**维度3：知识产权**
```sql
SELECT 
    e.企业名称,
    COUNT(DISTINCT p.专利ID) AS 专利数量,
    CASE 
        WHEN COUNT(DISTINCT p.专利ID) >= 10 THEN 2
        WHEN COUNT(DISTINCT p.专利ID) >= 5 THEN 1
        ELSE 0
    END AS 知识产权评分
FROM 企业信息 e
LEFT JOIN 专利信息 p ON e.eid = p.eid COLLATE utf8mb4_unicode_ci
WHERE e.企业名称 IN ('企业A', '企业B', '企业C')
  AND p.专利状态 = '有效'
GROUP BY e.eid
```

**维度4：诉讼风险**
```sql
SELECT 
    e.企业名称,
    COUNT(DISTINCT l.诉讼ID) AS 诉讼次数,
    CASE 
        WHEN COUNT(DISTINCT l.诉讼ID) = 0 THEN 2
        WHEN COUNT(DISTINCT l.诉讼ID) <= 2 THEN 1
        ELSE 0
    END AS 诉讼风险评分
FROM 企业信息 e
LEFT JOIN 诉讼信息 l ON e.eid = l.eid COLLATE utf8mb4_unicode_ci
WHERE e.企业名称 IN ('企业A', '企业B', '企业C')
  AND l.立案日期 >= DATE_SUB(CURDATE(), INTERVAL 3 YEAR)
GROUP BY e.eid
```

**维度5-8：投标、纳税、行业地位、成长性**（类似结构）

### 综合评估SQL
```sql
SELECT 
    e.企业名称,
    e.注册资本,
    DATEDIFF(CURDATE(), e.成立日期)/365 AS 存续年限,
    COUNT(DISTINCT p.专利ID) AS 专利数量,
    COUNT(DISTINCT l.诉讼ID) AS 诉讼次数,
    COUNT(DISTINCT b.投标ID) AS 投标次数,
    -- 综合评分
    (CASE WHEN CAST(REPLACE(REPLACE(e.注册资本, '万元', ''), '万', '') AS DECIMAL) >= 1000 THEN 2 ELSE 0 END +
     CASE WHEN DATEDIFF(CURDATE(), e.成立日期)/365 >= 5 THEN 2 ELSE 0 END +
     CASE WHEN COUNT(DISTINCT p.专利ID) >= 10 THEN 2 ELSE 0 END +
     CASE WHEN COUNT(DISTINCT l.诉讼ID) = 0 THEN 2 ELSE 0 END) AS 综合评分
FROM 企业信息 e
LEFT JOIN 专利信息 p ON e.eid = p.eid COLLATE utf8mb4_unicode_ci
LEFT JOIN 诉讼信息 l ON e.eid = l.eid COLLATE utf8mb4_unicode_ci
LEFT JOIN 招投标 b ON e.eid = b.eid COLLATE utf8mb4_unicode_ci
WHERE e.企业名称 IN ('企业A', '企业B', '企业C')
GROUP BY e.eid
HAVING 综合评分 >= 6
ORDER BY 综合评分 DESC
LIMIT 1000
```

---

## 场景5：企业尽调 - 8大维度

### 尽调维度结构

**维度1：基本信息**
- 企业名称、注册资本、成立日期、企业状态、所属行业、注册地址

**维度2：经营状况**
- 经营范围、年报数据、纳税情况

**维度3：知识产权**
- 专利、商标、软著数量和类型

**维度4：法律风险**
- 诉讼、被执行、失信记录

**维度5：财务健康**
- 注册资本、纳税等级、融资记录

**维度6：招投标**
- 投标次数、中标率、中标金额

**维度7：纳税情况**
- 纳税等级、纳税金额

**维度8：综合评估**
- 基于以上维度的综合评分和建议

---

## 重要规则

1. **JOIN必须COLLATE**：`ON a.eid = b.eid COLLATE utf8mb4_unicode_ci`
2. **禁止SELECT ***：明确指定字段
3. **时间范围**：默认近3年
4. **结果限制**：`LIMIT 1000`
5. **NULL处理**：`COALESCE(field, 0)` 或 `COALESCE(field, '未知')`
6. **数值转换**：注册资本等文本字段需要CAST转换
7. **去重统计**：使用 `COUNT(DISTINCT field)`
8. **评分逻辑**：使用CASE WHEN实现分段评分
