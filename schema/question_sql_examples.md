# Question-SQL 示例配对

本文档提供5个场景的标准Question-SQL配对，用于LLM的Few-shot学习和Vanna训练。

---

## 场景1：数据洞察

### 示例1：融资趋势分析
**问题**：分析近五年的融资趋势
**SQL**：
```sql
SELECT 
    YEAR(round_date) AS 年份,
    COUNT(*) AS 融资次数,
    COALESCE(SUM(amount), 0) AS 总金额,
    COALESCE(AVG(amount), 0) AS 平均金额
FROM 融资数据
WHERE round_date >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
GROUP BY YEAR(round_date)
ORDER BY 年份
LIMIT 20
```

### 示例2：行业分布统计
**问题**：统计各行业的企业数量分布
**SQL**：
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

### 示例3：地区企业分析
**问题**：分析各省份的企业数量和平均注册资本
**SQL**：
```sql
SELECT 
    ac.admin_name AS 省份,
    COUNT(DISTINCT b.eid) AS 企业数量,
    AVG(CAST(REPLACE(REPLACE(b.regist_capi_new, '万', ''), '元', '') AS DECIMAL)) AS 平均注册资本
FROM 企业基本信息 b
LEFT JOIN 行政区划代码表 ac ON b.province_code = ac.type_code
WHERE b.start_date >= DATE_SUB(CURDATE(), INTERVAL 3 YEAR)
  AND ac.行政区划等级 = 1
GROUP BY ac.admin_name
ORDER BY 企业数量 DESC
LIMIT 20
```

### 示例4：融资轮次分布
**问题**：统计不同融资轮次的数量和金额
**SQL**：
```sql
SELECT 
    round AS 融资轮次,
    COUNT(*) AS 融资次数,
    COALESCE(SUM(amount), 0) AS 总金额
FROM 融资数据
WHERE round_date >= DATE_SUB(CURDATE(), INTERVAL 3 YEAR)
  AND round IS NOT NULL
GROUP BY round
ORDER BY 融资次数 DESC
LIMIT 20
```

### 示例5：企业成立趋势
**问题**：分析近年来企业成立数量的趋势
**SQL**：
```sql
SELECT 
    YEAR(start_date) AS 年份,
    COUNT(*) AS 成立企业数
FROM 企业基本信息
WHERE start_date >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
  AND status = '存续'
GROUP BY YEAR(start_date)
ORDER BY 年份
LIMIT 20
```

---

## 场景2：地区产业分析

### 示例1：北京市企业概况
**问题**：分析北京市的企业总体情况
**SQL**：
```sql
SELECT 
    COUNT(DISTINCT b.eid) AS 企业总数,
    COUNT(DISTINCT CASE WHEN b.status='存续' THEN b.eid END) AS 存续企业数,
    AVG(CAST(REPLACE(REPLACE(b.regist_capi_new, '万', ''), '元', '') AS DECIMAL)) AS 平均注册资本
FROM 企业基本信息 b
LEFT JOIN 行政区划代码表 ac ON b.province_code = ac.type_code
WHERE ac.admin_name = '北京市'
  AND ac.行政区划等级 = 1
LIMIT 1
```

### 示例2：地区主导产业
**问题**：查询广东省的主导产业分布
**SQL**：
```sql
SELECT 
    COALESCE(ic.name, '未分类') AS 行业,
    COUNT(DISTINCT b.eid) AS 企业数量
FROM 企业基本信息 b
LEFT JOIN 行政区划代码表 ac ON b.province_code = ac.type_code
LEFT JOIN 企业行业代码 ic ON b.eid = ic.eid COLLATE utf8mb4_unicode_ci
WHERE ac.admin_name = '广东省'
  AND ac.行政区划等级 = 1
  AND b.status = '存续'
GROUP BY ic.name
ORDER BY 企业数量 DESC
LIMIT 10
```

### 示例3：地区龙头企业
**问题**：查询上海市注册资本最高的企业
**SQL**：
```sql
SELECT 
    b.format_name AS 企业名称,
    b.regist_capi_new AS 注册资本,
    b.start_date AS 成立日期,
    b.industry AS 所属行业
FROM 企业基本信息 b
LEFT JOIN 行政区划代码表 ac ON b.province_code = ac.type_code
WHERE ac.admin_name = '上海市'
  AND ac.行政区划等级 = 1
  AND b.status = '存续'
ORDER BY CAST(REPLACE(REPLACE(b.regist_capi_new, '万', ''), '元', '') AS DECIMAL) DESC
LIMIT 20
```

### 示例4：地区融资情况
**问题**：分析浙江省的融资情况
**SQL**：
```sql
SELECT 
    COUNT(DISTINCT r.eid) AS 获投企业数,
    COUNT(*) AS 融资事件数,
    COALESCE(SUM(r.amount), 0) AS 融资总额
FROM 融资数据 r
LEFT JOIN 企业基本信息 b ON r.eid = b.eid COLLATE utf8mb4_unicode_ci
LEFT JOIN 行政区划代码表 ac ON b.province_code = ac.type_code
WHERE ac.admin_name = '浙江省'
  AND ac.行政区划等级 = 1
  AND r.round_date >= DATE_SUB(CURDATE(), INTERVAL 3 YEAR)
LIMIT 1
```

### 示例5：地区新兴产业
**问题**：查询深圳市近三年新成立企业的行业分布
**SQL**：
```sql
SELECT 
    COALESCE(ic.name, '未分类') AS 行业,
    COUNT(DISTINCT b.eid) AS 新成立企业数
FROM 企业基本信息 b
LEFT JOIN 行政区划代码表 ac ON b.district_code = ac.type_code
LEFT JOIN 企业行业代码 ic ON b.eid = ic.eid COLLATE utf8mb4_unicode_ci
WHERE ac.admin_name LIKE '%深圳%'
  AND b.start_date >= DATE_SUB(CURDATE(), INTERVAL 3 YEAR)
  AND b.status = '存续'
GROUP BY ic.name
ORDER BY 新成立企业数 DESC
LIMIT 10
```

---

## 场景3：行业分析

### 示例1：软件行业企业数量增长
**问题**：分析软件行业近年来的企业数量增长趋势
**SQL**：
```sql
SELECT 
    YEAR(b.start_date) AS 年份,
    COUNT(DISTINCT b.eid) AS 新成立企业数
FROM 企业基本信息 b
LEFT JOIN 企业行业代码 ic ON b.eid = ic.eid COLLATE utf8mb4_unicode_ci
WHERE ic.name LIKE '%软件%'
  AND b.start_date >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
  AND b.status = '存续'
GROUP BY YEAR(b.start_date)
ORDER BY 年份
LIMIT 20
```

### 示例2：行业空间分布
**问题**：查询人工智能行业的地域分布
**SQL**：
```sql
SELECT 
    ac.admin_name AS 省份,
    COUNT(DISTINCT b.eid) AS 企业数量
FROM 企业基本信息 b
LEFT JOIN 企业行业代码 ic ON b.eid = ic.eid COLLATE utf8mb4_unicode_ci
LEFT JOIN 行政区划代码表 ac ON b.province_code = ac.type_code
WHERE ic.name LIKE '%人工智能%'
  AND ac.行政区划等级 = 1
  AND b.status = '存续'
GROUP BY ac.admin_name
ORDER BY 企业数量 DESC
LIMIT 20
```

### 示例3：行业龙头企业
**问题**：查询新能源行业注册资本最高的企业
**SQL**：
```sql
SELECT 
    b.format_name AS 企业名称,
    b.regist_capi_new AS 注册资本,
    b.start_date AS 成立日期,
    ac.admin_name AS 所在省份
FROM 企业基本信息 b
LEFT JOIN 企业行业代码 ic ON b.eid = ic.eid COLLATE utf8mb4_unicode_ci
LEFT JOIN 行政区划代码表 ac ON b.province_code = ac.type_code
WHERE ic.name LIKE '%新能源%'
  AND b.status = '存续'
  AND ac.行政区划等级 = 1
ORDER BY CAST(REPLACE(REPLACE(b.regist_capi_new, '万', ''), '元', '') AS DECIMAL) DESC
LIMIT 20
```

### 示例4：行业融资情况
**问题**：分析生物医药行业的融资情况
**SQL**：
```sql
SELECT 
    YEAR(r.round_date) AS 年份,
    COUNT(*) AS 融资事件数,
    COALESCE(SUM(r.amount), 0) AS 融资总额,
    COALESCE(AVG(r.amount), 0) AS 平均融资额
FROM 融资数据 r
LEFT JOIN 企业基本信息 b ON r.eid = b.eid COLLATE utf8mb4_unicode_ci
LEFT JOIN 企业行业代码 ic ON b.eid = ic.eid COLLATE utf8mb4_unicode_ci
WHERE ic.name LIKE '%生物%' OR ic.name LIKE '%医药%'
  AND r.round_date >= DATE_SUB(CURDATE(), INTERVAL 3 YEAR)
GROUP BY YEAR(r.round_date)
ORDER BY 年份
LIMIT 20
```

### 示例5：行业投资热度
**问题**：统计各行业获得融资的企业数量
**SQL**：
```sql
SELECT 
    COALESCE(ic.name, '未分类') AS 行业,
    COUNT(DISTINCT r.eid) AS 获投企业数,
    COUNT(*) AS 融资事件数,
    COALESCE(SUM(r.amount), 0) AS 融资总额
FROM 融资数据 r
LEFT JOIN 企业基本信息 b ON r.eid = b.eid COLLATE utf8mb4_unicode_ci
LEFT JOIN 企业行业代码 ic ON b.eid = ic.eid COLLATE utf8mb4_unicode_ci
WHERE r.round_date >= DATE_SUB(CURDATE(), INTERVAL 3 YEAR)
GROUP BY ic.name
ORDER BY 获投企业数 DESC
LIMIT 20
```

---

## 场景4：招商清单

### 示例1：企业基本信息查询
**问题**：查询指定企业的基本信息
**SQL**：
```sql
SELECT 
    企业名称,
    注册资本,
    成立日期,
    DATEDIFF(CURDATE(), 成立日期)/365 AS 存续年限,
    企业状态,
    所属行业
FROM 企业信息
WHERE 企业名称 IN ('华为技术有限公司', '腾讯科技有限公司', '阿里巴巴集团')
LIMIT 100
```

### 示例2：知识产权统计
**问题**：统计企业的专利数量
**SQL**：
```sql
SELECT 
    e.企业名称,
    COUNT(DISTINCT p.专利ID) AS 专利总数,
    SUM(CASE WHEN p.专利类型='发明专利' THEN 1 ELSE 0 END) AS 发明专利数,
    SUM(CASE WHEN p.专利类型='实用新型' THEN 1 ELSE 0 END) AS 实用新型数
FROM 企业信息 e
LEFT JOIN 专利信息 p ON e.eid = p.eid COLLATE utf8mb4_unicode_ci
WHERE e.企业名称 IN ('华为技术有限公司', '腾讯科技有限公司')
  AND p.专利状态 = '有效'
GROUP BY e.eid
LIMIT 100
```

### 示例3：诉讼风险评估
**问题**：查询企业的诉讼情况
**SQL**：
```sql
SELECT 
    e.企业名称,
    COUNT(DISTINCT l.诉讼ID) AS 诉讼总数,
    SUM(CASE WHEN l.被告 LIKE CONCAT('%', e.企业名称, '%') THEN 1 ELSE 0 END) AS 作为被告次数,
    SUM(CASE WHEN l.案件状态='已结案' THEN 1 ELSE 0 END) AS 已结案数
FROM 企业信息 e
LEFT JOIN 诉讼信息 l ON e.eid = l.eid COLLATE utf8mb4_unicode_ci
WHERE e.企业名称 IN ('华为技术有限公司', '腾讯科技有限公司')
  AND l.立案日期 >= DATE_SUB(CURDATE(), INTERVAL 3 YEAR)
GROUP BY e.eid
LIMIT 100
```

### 示例4：招投标能力
**问题**：统计企业的投标和中标情况
**SQL**：
```sql
SELECT 
    e.企业名称,
    COUNT(DISTINCT b.投标ID) AS 投标次数,
    SUM(CASE WHEN b.中标状态='中标' THEN 1 ELSE 0 END) AS 中标次数,
    COALESCE(SUM(CASE WHEN b.中标状态='中标' THEN b.项目金额 ELSE 0 END), 0) AS 中标总金额
FROM 企业信息 e
LEFT JOIN 招投标 b ON e.eid = b.eid COLLATE utf8mb4_unicode_ci
WHERE e.企业名称 IN ('华为技术有限公司', '腾讯科技有限公司')
  AND b.发布时间 >= DATE_SUB(CURDATE(), INTERVAL 3 YEAR)
GROUP BY e.eid
LIMIT 100
```

### 示例5：综合评估
**问题**：对企业进行8维度综合评估
**SQL**：
```sql
SELECT 
    e.企业名称,
    CAST(REPLACE(REPLACE(e.注册资本, '万元', ''), '万', '') AS DECIMAL) AS 注册资本,
    DATEDIFF(CURDATE(), e.成立日期)/365 AS 存续年限,
    COUNT(DISTINCT p.专利ID) AS 专利数量,
    COUNT(DISTINCT l.诉讼ID) AS 诉讼次数,
    COUNT(DISTINCT b.投标ID) AS 投标次数,
    (CASE WHEN CAST(REPLACE(REPLACE(e.注册资本, '万元', ''), '万', '') AS DECIMAL) >= 1000 THEN 2 ELSE 0 END +
     CASE WHEN DATEDIFF(CURDATE(), e.成立日期)/365 >= 5 THEN 2 ELSE 0 END +
     CASE WHEN COUNT(DISTINCT p.专利ID) >= 10 THEN 2 ELSE 0 END +
     CASE WHEN COUNT(DISTINCT l.诉讼ID) = 0 THEN 2 ELSE 0 END) AS 综合评分
FROM 企业信息 e
LEFT JOIN 专利信息 p ON e.eid = p.eid COLLATE utf8mb4_unicode_ci
LEFT JOIN 诉讼信息 l ON e.eid = l.eid COLLATE utf8mb4_unicode_ci
LEFT JOIN 招投标 b ON e.eid = b.eid COLLATE utf8mb4_unicode_ci
WHERE e.企业名称 IN ('华为技术有限公司', '腾讯科技有限公司', '阿里巴巴集团')
GROUP BY e.eid
ORDER BY 综合评分 DESC
LIMIT 100
```

---

## 场景5：企业尽调

### 示例1：企业基本信息详查
**问题**：查询某企业的详细基本信息
**SQL**：
```sql
SELECT 
    企业名称,
    注册资本,
    成立日期,
    DATEDIFF(CURDATE(), 成立日期)/365 AS 存续年限,
    企业状态,
    所属行业,
    注册地址,
    经营范围
FROM 企业信息
WHERE 企业名称 = '华为技术有限公司'
LIMIT 1
```

### 示例2：知识产权详情
**问题**：查询企业的知识产权详细情况
**SQL**：
```sql
SELECT 
    '专利' AS 类型,
    COUNT(DISTINCT p.专利ID) AS 数量,
    SUM(CASE WHEN p.专利类型='发明专利' THEN 1 ELSE 0 END) AS 发明专利,
    SUM(CASE WHEN p.专利类型='实用新型' THEN 1 ELSE 0 END) AS 实用新型,
    SUM(CASE WHEN p.专利状态='有效' THEN 1 ELSE 0 END) AS 有效数量
FROM 企业信息 e
LEFT JOIN 专利信息 p ON e.eid = p.eid COLLATE utf8mb4_unicode_ci
WHERE e.企业名称 = '华为技术有限公司'
LIMIT 1
```

### 示例3：法律风险全面评估
**问题**：全面评估企业的法律风险
**SQL**：
```sql
SELECT 
    COUNT(DISTINCT l.诉讼ID) AS 诉讼案件数,
    SUM(CASE WHEN l.案件状态='审理中' THEN 1 ELSE 0 END) AS 审理中案件,
    SUM(CASE WHEN l.被告 LIKE CONCAT('%', e.企业名称, '%') THEN 1 ELSE 0 END) AS 作为被告次数,
    COUNT(DISTINCT ex.案件ID) AS 被执行案件数,
    COUNT(DISTINCT d.记录ID) AS 失信记录数
FROM 企业信息 e
LEFT JOIN 诉讼信息 l ON e.eid = l.eid COLLATE utf8mb4_unicode_ci
LEFT JOIN 被执行人 ex ON e.eid = ex.eid COLLATE utf8mb4_unicode_ci
LEFT JOIN 失信信息 d ON e.eid = d.eid COLLATE utf8mb4_unicode_ci
WHERE e.企业名称 = '华为技术有限公司'
LIMIT 1
```

### 示例4：经营能力分析
**问题**：分析企业的经营能力
**SQL**：
```sql
SELECT 
    COUNT(DISTINCT b.投标ID) AS 投标总数,
    SUM(CASE WHEN b.中标状态='中标' THEN 1 ELSE 0 END) AS 中标数量,
    ROUND(SUM(CASE WHEN b.中标状态='中标' THEN 1 ELSE 0 END) * 100.0 / COUNT(DISTINCT b.投标ID), 2) AS 中标率,
    COALESCE(SUM(CASE WHEN b.中标状态='中标' THEN b.项目金额 ELSE 0 END), 0) AS 中标总金额,
    t.纳税等级,
    t.纳税金额
FROM 企业信息 e
LEFT JOIN 招投标 b ON e.eid = b.eid COLLATE utf8mb4_unicode_ci
LEFT JOIN 纳税信息 t ON e.eid = t.eid COLLATE utf8mb4_unicode_ci
WHERE e.企业名称 = '华为技术有限公司'
  AND b.发布时间 >= DATE_SUB(CURDATE(), INTERVAL 3 YEAR)
GROUP BY e.eid, t.纳税等级, t.纳税金额
LIMIT 1
```

### 示例5：综合尽调报告数据
**问题**：获取企业尽调报告所需的全部数据
**SQL**：
```sql
SELECT 
    e.企业名称,
    e.注册资本,
    DATEDIFF(CURDATE(), e.成立日期)/365 AS 存续年限,
    e.企业状态,
    COUNT(DISTINCT p.专利ID) AS 专利数量,
    COUNT(DISTINCT l.诉讼ID) AS 诉讼数量,
    COUNT(DISTINCT b.投标ID) AS 投标数量,
    SUM(CASE WHEN b.中标状态='中标' THEN 1 ELSE 0 END) AS 中标数量,
    t.纳税等级,
    COUNT(DISTINCT f.融资ID) AS 融资次数
FROM 企业信息 e
LEFT JOIN 专利信息 p ON e.eid = p.eid COLLATE utf8mb4_unicode_ci
LEFT JOIN 诉讼信息 l ON e.eid = l.eid COLLATE utf8mb4_unicode_ci
LEFT JOIN 招投标 b ON e.eid = b.eid COLLATE utf8mb4_unicode_ci
LEFT JOIN 纳税信息 t ON e.eid = t.eid COLLATE utf8mb4_unicode_ci
LEFT JOIN 融资信息 f ON e.eid = f.eid COLLATE utf8mb4_unicode_ci
WHERE e.企业名称 = '华为技术有限公司'
GROUP BY e.eid, t.纳税等级
LIMIT 1
```

---

## 通用规则总结

### 必须遵守的SQL规则
1. **JOIN必须使用COLLATE**：`ON a.eid = b.eid COLLATE utf8mb4_unicode_ci`
2. **禁止SELECT ***：明确指定所有字段
3. **时间范围**：默认近3年 `WHERE date >= DATE_SUB(CURDATE(), INTERVAL 3 YEAR)`
4. **结果限制**：`LIMIT 1000`（最大限制）
5. **单个SELECT**：不允许多语句、避免复杂子查询
6. **NULL处理**：使用 `COALESCE(field, default_value)`
7. **去重统计**：使用 `COUNT(DISTINCT field)`
8. **数值转换**：文本字段转数值 `CAST(REPLACE(REPLACE(field, '万', ''), '元', '') AS DECIMAL)`

### 场景特定规则

**场景1-3（Gaaiyun数据库）**：
- 主要表：融资数据、企业基本信息、企业行业代码
- 关注时间趋势、地域分布、行业分类
- 输出格式：Markdown + 图表

**场景4-5（gaaiyun_2数据库）**：
- 主要表：企业信息、专利信息、诉讼信息、招投标、纳税信息
- 关注企业评估、风险分析、综合评分
- 输出格式：Excel（场景4）、Word（场景5）
