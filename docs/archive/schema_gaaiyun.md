# 数据库 Schema 文档

**数据库**: gaaiyun.md
**生成时间**: 2026-02-26

---

## 📊 表：产品数据

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| eid | text | YES |  | NULL |  |
| id | double | YES |  | NULL |  |
| proj_id | text | YES |  | NULL |  |
| ename | text | YES |  | NULL |  |
| pro_name | text | YES |  | NULL |  |
| kind | text | YES |  | NULL |  |
| description | text | YES |  | NULL |  |
| domain | text | YES |  | NULL |  |
| links | text | YES |  | NULL |  |

## 📊 表：企业基本信息

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| eid | varchar(255) | NO |  | NULL |  |
| id | varchar(255) | NO |  | NULL |  |
| credit_no | varchar(255) | YES |  | NULL |  |
| format_name | varchar(255) | YES |  | NULL |  |
| actual_capi | varchar(255) | YES |  | NULL |  |
| scope | text | YES |  | NULL |  |
| start_date | varchar(255) | YES |  | NULL |  |
| province_code | varchar(255) | YES |  | NULL |  |
| district_code | varchar(255) | YES |  | NULL |  |
| regist_capi_new | varchar(255) | YES |  | NULL |  |
| revoke_date | varchar(255) | YES |  | NULL |  |
| logout_date | varchar(255) | YES |  | NULL |  |
| new_status_code | varchar(255) | YES |  | NULL |  |

## 📊 表：企业行业代码

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| eid | text | YES |  | NULL |  |
| name | text | YES |  | NULL |  |
| industry_code | text | YES |  | NULL |  |
| import_id | bigint | NO | PRI | NULL |  |

## 📊 表：投资数据

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| eid | varchar(255) | YES |  | NULL |  |
| id | varchar(255) | YES | MUL | NULL |  |
| name | varchar(255) | YES |  | NULL |  |
| invest_eid | varchar(255) | YES |  | NULL |  |
| stock_percent | varchar(255) | YES |  | NULL |  |
| invest_name | varchar(255) | YES |  | NULL |  |
| invest_credit_no | varchar(255) | YES |  | NULL |  |
| invest_reg_no | varchar(255) | YES |  | NULL |  |
| invest_status | varchar(255) | YES |  | NULL |  |
| invest_regist_capi | varchar(255) | YES |  | NULL |  |
| invest_start_date | varchar(255) | YES |  | NULL |  |
| stock_num | varchar(255) | YES |  | NULL |  |
| invest_quote_status | varchar(255) | YES |  | NULL |  |
| real_capi | varchar(255) | YES |  | NULL |  |
| import_id | bigint | NO | PRI | NULL |  |

## 📊 表：招投标

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| eid | varchar(255) | YES |  | NULL |  |
| u_id | varchar(255) | YES |  | NULL |  |
| id | varchar(255) | YES |  | NULL |  |
| title | text | YES |  | NULL |  |
| publish_time | varchar(255) | YES |  | NULL |  |
| area_code | varchar(255) | YES |  | NULL |  |
| notice_type_main | varchar(255) | YES |  | NULL |  |
| notice_type_sub | varchar(255) | YES |  | NULL |  |
| industry_code | varchar(255) | YES |  | NULL |  |
| project_number | varchar(255) | YES |  | NULL |  |
| project_bid_money | varchar(255) | YES |  | NULL |  |
| create_time | varchar(255) | YES |  | NULL |  |
| row_update_time | varchar(255) | YES |  | NULL |  |
| merge_data_time | varchar(255) | YES |  | NULL |  |

## 📊 表：标签数据

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| eid | varchar(255) | YES |  | NULL |  |
| id | varchar(255) | YES |  | NULL |  |
| _id | varchar(255) | YES |  | NULL |  |
| name | varchar(255) | YES |  | NULL |  |
| district | varchar(255) | YES |  | NULL |  |
| district_code | varchar(255) | YES |  | NULL |  |
| register_no | varchar(255) | YES |  | NULL |  |
| type | varchar(255) | YES |  | NULL |  |
| year | varchar(255) | YES |  | NULL |  |
| publish_date | varchar(255) | YES |  | NULL |  |
| level | varchar(255) | YES |  | NULL |  |
| end_date | varchar(255) | YES |  | NULL |  |
| valid_start | varchar(255) | YES |  | NULL |  |
| valid_end | varchar(255) | YES |  | NULL |  |
| state | varchar(255) | YES |  | NULL |  |

## 📊 表：融资数据

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| eid | text | YES |  | NULL |  |
| id | double | YES |  | NULL |  |
| ename | text | YES |  | NULL |  |
| round_date | datetime | YES |  | NULL |  |
| round | text | YES |  | NULL |  |
| round_type | double | YES |  | NULL |  |
| amount | double | YES |  | NULL |  |
| estimated_amount | double | YES |  | NULL |  |
| currency | text | YES |  | NULL |  |
| investors | text | YES |  | NULL |  |
| investors_json | text | YES |  | NULL |  |
| publish_date | datetime | YES |  | NULL |  |

## 📊 表：行业代码表

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| f1 | varchar(255) | YES |  | NULL |  |
| industry_code | varchar(255) | YES |  | NULL |  |
| 门类代码 | varchar(255) | YES |  | NULL |  |
| 门类名称 | varchar(255) | YES |  | NULL |  |
| 大类行业代码 | varchar(255) | YES |  | NULL |  |
| 大类代码 | varchar(255) | YES |  | NULL |  |
| 大类名称 | varchar(255) | YES |  | NULL |  |
| 中类行业代码 | varchar(255) | YES |  | NULL |  |
| 中类代码 | varchar(255) | YES |  | NULL |  |
| 中类名称 | varchar(255) | YES |  | NULL |  |
| 小类行业代码 | varchar(255) | YES |  | NULL |  |
| 小类名称 | varchar(255) | YES |  | NULL |  |

## 📊 表：行政区划代码表

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| type_code | bigint | YES |  | NULL |  |
| admin_name | text | YES |  | NULL |  |
| short_name | text | YES |  | NULL |  |
| 行政区划等级 | bigint | YES |  | NULL |  |

