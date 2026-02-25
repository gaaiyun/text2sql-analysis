# 数据库 Schema 文档

**数据库**: gaaiyun
**生成时间**: 2026-02-26

---

## 📊 表：ipo进程

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 披露日期 | datetime | YES |  | NULL |  |
| 当前状态 | text | YES |  | NULL |  |
| 所属领域 | text | YES |  | NULL |  |
| 拟发行市场 | text | YES |  | NULL |  |
| 保荐机构 | text | YES |  | NULL |  |

## 📊 表：一般纳税人资格

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 纳税人识别号 | text | YES |  | NULL |  |
| 纳税人资格类型 | text | YES |  | NULL |  |
| 主管税务机关 | text | YES |  | NULL |  |
| 登记时间 | datetime | YES |  | NULL |  |
| 有效期起 | text | YES |  | NULL |  |
| 有效期止 | text | YES |  | NULL |  |

## 📊 表：专利信息_大陆

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 专利名称 | text | YES |  | NULL |  |
| 专利类型 | text | YES |  | NULL |  |
| 注册地区 | text | YES |  | NULL |  |
| 授权状态 | text | YES |  | NULL |  |
| 法律状态_新_ | text | YES |  | NULL |  |
| 专利申请号 | text | YES |  | NULL |  |
| 专利申请日 | text | YES |  | NULL |  |
| 申请公布号 | text | YES |  | NULL |  |
| 申请公布日 | text | YES |  | NULL |  |
| 授权公告号 | text | YES |  | NULL |  |
| 授权公告日 | text | YES |  | NULL |  |
| 申请_专利权_人 | text | YES |  | NULL |  |
| 分类号 | text | YES |  | NULL |  |
| 专利代理机构 | text | YES |  | NULL |  |
| 法律状态 | text | YES |  | NULL |  |

## 📊 表：专利信息_香港

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 专利名称 | text | YES |  | NULL |  |
| 专利类型 | text | YES |  | NULL |  |
| 注册地区 | text | YES |  | NULL |  |
| 法律状态 | text | YES |  | NULL |  |
| 专利号 | text | YES |  | NULL |  |
| 申请编号 | bigint | YES |  | NULL |  |
| 注册编号 | text | YES |  | NULL |  |
| 发表编号 | text | YES |  | NULL |  |
| 分类 | text | YES |  | NULL |  |
| 诉讼语言 | text | YES |  | NULL |  |
| 欧洲专利申请提交日期 | datetime | YES |  | NULL |  |
| 专利所有人 | text | YES |  | NULL |  |
| 发明人 | text | YES |  | NULL |  |
| 代理商 | text | YES |  | NULL |  |
| 代理商地址 | text | YES |  | NULL |  |
| 批予专利日期 | datetime | YES |  | NULL |  |
| 联合王国专利局批予日期 | datetime | YES |  | NULL |  |
| 提交注册日期 | datetime | YES |  | NULL |  |
| 专利说明书首次发表日期 | datetime | YES |  | NULL |  |
| 认定提交日期 | datetime | YES |  | NULL |  |
| 提交日期 | datetime | YES |  | NULL |  |
| 优先权申请编号 | double | YES |  | NULL |  |
| 优先权日期 | datetime | YES |  | NULL |  |
| 优先权国家_地区 | text | YES |  | NULL |  |
| 文件发表时间_文件说明_文件类型 | datetime | YES |  | NULL |  |
| 指定专利局 | text | YES |  | NULL |  |
| 指定专利专利发表编号 | text | YES |  | NULL |  |
| 指定专利批予专利日期 | datetime | YES |  | NULL |  |
| 指定专利申请发表日期 | datetime | YES |  | NULL |  |
| 指定专利申请发表编号 | text | YES |  | NULL |  |
| 指定专利申请编号 | text | YES |  | NULL |  |
| 指定专利申请提交日期 | datetime | YES |  | NULL |  |
| 国际发表编号 | text | YES |  | NULL |  |
| 国际发表日期 | datetime | YES |  | NULL |  |
| 国际申请编号 | text | YES |  | NULL |  |
| 国际申请提交日期 | datetime | YES |  | NULL |  |
| 变更信息_标题_时间_内容_ | datetime | YES |  | NULL |  |

## 📊 表：严重违法失信

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 类别 | text | YES |  | NULL |  |
| 列入严重违法失信企业名单_黑名单_原因 | text | YES |  | NULL |  |
| 列入日期 | datetime | YES |  | NULL |  |
| 作出决定机关_列入_ | text | YES |  | NULL |  |
| 移出严重违法失信企业名单_黑名单_原因 | text | YES |  | NULL |  |
| 移出日期 | datetime | YES |  | NULL |  |
| 作出决定机关_移出_ | text | YES |  | NULL |  |

## 📊 表：严重违法失信_历史_

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 类别 | text | YES |  | NULL |  |
| 列入严重违法失信企业名单_黑名单_原因 | text | YES |  | NULL |  |
| 列入日期 | datetime | YES |  | NULL |  |
| 作出决定机关_列入_ | text | YES |  | NULL |  |
| 移出严重违法失信企业名单_黑名单_原因 | text | YES |  | NULL |  |
| 移出日期 | datetime | YES |  | NULL |  |
| 作出决定机关_移出_ | text | YES |  | NULL |  |

## 📊 表：主体评级

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 主体评级 | text | YES |  | NULL |  |
| 评级公司 | text | YES |  | NULL |  |
| 评级日期 | datetime | YES |  | NULL |  |
| 评级展望 | text | YES |  | NULL |  |
| 披露日期 | datetime | YES |  | NULL |  |

## 📊 表：主要人员_历史__工商公示

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 姓名 | text | YES |  | NULL |  |
| 职务 | text | YES |  | NULL |  |
| 持股比例 | text | YES |  | NULL |  |
| 是否历史主要人员 | text | YES |  | NULL |  |
| 任职日期 | datetime | YES |  | NULL |  |
| 卸任日期 | datetime | YES |  | NULL |  |
| 主要人员对外投资 | text | YES |  | NULL |  |

## 📊 表：主要人员_历史__最新公示

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 姓名 | text | YES |  | NULL |  |
| 职务 | text | YES |  | NULL |  |
| 任职日期 | datetime | YES |  | NULL |  |
| 卸任日期 | datetime | YES |  | NULL |  |
| 卸任原因 | text | YES |  | NULL |  |
| 个人简介 | text | YES |  | NULL |  |

## 📊 表：主要人员_工商公示

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 姓名 | text | YES |  | NULL |  |
| 职务 | text | YES |  | NULL |  |
| 持股比例 | text | YES |  | NULL |  |
| 是否历史主要人员 | text | YES |  | NULL |  |
| 任职日期 | datetime | YES |  | NULL |  |
| 卸任日期 | datetime | YES |  | NULL |  |
| 主要人员对外投资 | text | YES |  | NULL |  |

## 📊 表：主要人员_最新公示

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 姓名 | text | YES |  | NULL |  |
| 性别 | text | YES |  | NULL |  |
| 学历 | text | YES |  | NULL |  |
| 职务 | text | YES |  | NULL |  |
| 薪酬_税前元_ | text | YES |  | NULL |  |
| 持股数 | text | YES |  | NULL |  |
| 持股比例 | text | YES |  | NULL |  |
| 最终受益股份 | text | YES |  | NULL |  |
| 任职日期 | datetime | YES |  | NULL |  |
| 公告日期 | datetime | YES |  | NULL |  |
| 个人简介 | text | YES |  | NULL |  |

## 📊 表：企业信息表

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| eid | text | YES |  | NULL |  |
| id | bigint | YES |  | NULL |  |
| reg_no | text | YES |  | NULL |  |
| credit_no | text | YES |  | NULL |  |
| org_no | text | YES |  | NULL |  |
| name | text | YES |  | NULL |  |
| format_name | text | YES |  | NULL |  |
| econ_kind | text | YES |  | NULL |  |
| regist_capi | text | YES |  | NULL |  |
| actual_capi | double | YES |  | NULL |  |
| scope | text | YES |  | NULL |  |
| term_start | datetime | YES |  | NULL |  |
| term_end | text | YES |  | NULL |  |
| check_date | datetime | YES |  | NULL |  |
| belong_org | text | YES |  | NULL |  |
| oper_name | text | YES |  | NULL |  |
| oper_type | text | YES |  | NULL |  |
| oper_name_id | text | YES |  | NULL |  |
| start_date | datetime | YES |  | NULL |  |
| status | text | YES |  | NULL |  |
| title | text | YES |  | NULL |  |
| longitude | double | YES |  | NULL |  |
| latitude | double | YES |  | NULL |  |
| gd_longitude | double | YES |  | NULL |  |
| gd_latitude | double | YES |  | NULL |  |
| collegues_num | text | YES |  | NULL |  |
| created_time | datetime | YES |  | NULL |  |
| logo_url | text | YES |  | NULL |  |
| econ_type | double | YES |  | NULL |  |
| department | double | YES |  | NULL |  |
| url | text | YES |  | NULL |  |
| row_update_time | datetime | YES |  | NULL |  |
| province_code | bigint | YES |  | NULL |  |
| district_code | bigint | YES |  | NULL |  |
| title_code | text | YES |  | NULL |  |
| econ_kind_code | double | YES |  | NULL |  |
| regist_capi_new | double | YES |  | NULL |  |
| currency_unit | text | YES |  | NULL |  |
| revoke_reason | text | YES |  | NULL |  |
| revoke_date | datetime | YES |  | NULL |  |
| logout_reason | text | YES |  | NULL |  |
| logout_date | datetime | YES |  | NULL |  |
| revoked_certificates | double | YES |  | NULL |  |
| new_status_code | bigint | YES |  | NULL |  |
| type_new | bigint | YES |  | NULL |  |
| category_new | bigint | YES |  | NULL |  |
| merge_data_time | datetime | YES |  | NULL |  |
| industry_code | text | YES |  | NULL |  |
| province_name | text | YES |  | NULL |  |
| city_name | text | YES |  | NULL |  |
| district_name | text | YES |  | NULL |  |
| menlei_name | text | YES |  | NULL |  |
| dalei_name | text | YES |  | NULL |  |
| zhonglei_name | text | YES |  | NULL |  |
| xiaolei_name | text | YES |  | NULL |  |
| brief | text | YES |  | NULL |  |
| address | text | YES |  | NULL |  |
| tags | text | YES |  | NULL |  |
| shangshi | text | YES |  | NULL |  |

## 📊 表：供应商

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 供应商名称 | text | YES |  | NULL |  |
| 统一社会信用代码 | text | YES |  | NULL |  |
| 合作总次数 | bigint | YES |  | NULL |  |
| 合作总金额_万元_ | text | YES |  | NULL |  |
| 最近合作时间 | datetime | YES |  | NULL |  |
| 最新合作项目 | text | YES |  | NULL |  |
| 最近合作金额_万元_ | text | YES |  | NULL |  |
| 最新合作数据来源 | text | YES |  | NULL |  |
| 中标联系人姓名_来源于招投标公告_ | text | YES |  | NULL |  |
| 中标人电话_来源于招投标公告_ | text | YES |  | NULL |  |
| 中标人地址_来源于招投标公告_ | text | YES |  | NULL |  |
| 地区 | text | YES |  | NULL |  |
| 地址_全部_ | text | YES |  | NULL |  |
| 经营状态 | text | YES |  | NULL |  |
| 注册资本 | text | YES |  | NULL |  |
| 成立日期 | datetime | YES |  | NULL |  |
| 行业_一级_ | text | YES |  | NULL |  |
| 行业_二级_ | text | YES |  | NULL |  |
| 电话_全部_ | text | YES |  | NULL |  |
| 资本背景 | text | YES |  | NULL |  |
| 企业规模 | text | YES |  | NULL |  |
| 资质标签_科技认定_ | text | YES |  | NULL |  |

## 📊 表：债券信息

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 债券简称 | text | YES |  | NULL |  |
| 债券代码 | text | YES |  | NULL |  |
| 债券类型 | text | YES |  | NULL |  |
| 发行日期 | datetime | YES |  | NULL |  |
| 上市日期 | datetime | YES |  | NULL |  |
| 到期日期 | datetime | YES |  | NULL |  |
| 募集方式 | text | YES |  | NULL |  |
| 发行价格_元_ | double | YES |  | NULL |  |
| 发行规模_亿元_ | double | YES |  | NULL |  |
| 计息方式 | text | YES |  | NULL |  |
| 付息方式 | text | YES |  | NULL |  |
| 交易场所 | text | YES |  | NULL |  |
| 是否历史 | text | YES |  | NULL |  |

## 📊 表：公司产品

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 产品名称 | text | YES |  | NULL |  |
| 产品类型 | text | YES |  | NULL |  |
| 产品简介 | text | YES |  | NULL |  |

## 📊 表：减资公告_历史_

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 做出决定日期 | datetime | YES |  | NULL |  |
| 公告日期 | datetime | YES |  | NULL |  |
| 公告期限 | text | YES |  | NULL |  |
| 联系地址 | text | YES |  | NULL |  |
| 联系人 | text | YES |  | NULL |  |
| 联系电话 | text | YES |  | NULL |  |
| 公告内容 | text | YES |  | NULL |  |

## 📊 表：动产抵押

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 登记编号 | text | YES |  | NULL |  |
| 登记机关 | text | YES |  | NULL |  |
| 抵押物 | text | YES |  | NULL |  |
| 被担保债权种类 | text | YES |  | NULL |  |
| 被担保债权数额 | text | YES |  | NULL |  |
| 状态 | text | YES |  | NULL |  |
| 登记日期 | datetime | YES |  | NULL |  |
| 债务人履行债务的期限 | text | YES |  | NULL |  |
| 担保范围 | text | YES |  | NULL |  |

## 📊 表：动产抵押_历史_

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 登记编号 | text | YES |  | NULL |  |
| 登记机关 | text | YES |  | NULL |  |
| 抵押物 | text | YES |  | NULL |  |
| 被担保债权种类 | text | YES |  | NULL |  |
| 被担保债权数额 | text | YES |  | NULL |  |
| 状态 | text | YES |  | NULL |  |
| 登记日期 | datetime | YES |  | NULL |  |
| 债务人履行债务的期限 | text | YES |  | NULL |  |
| 担保范围 | text | YES |  | NULL |  |

## 📊 表：双随机抽查

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 抽查计划编号 | text | YES |  | NULL |  |
| 抽查计划名称 | text | YES |  | NULL |  |
| 抽查任务编号 | text | YES |  | NULL |  |
| 抽查任务名称 | text | YES |  | NULL |  |
| 抽查类型 | text | YES |  | NULL |  |
| 抽查机关 | text | YES |  | NULL |  |
| 抽查完成日期 | datetime | YES |  | NULL |  |

## 📊 表：双随机抽查_历史_

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 抽查计划编号 | text | YES |  | NULL |  |
| 抽查计划名称 | text | YES |  | NULL |  |
| 抽查任务编号 | text | YES |  | NULL |  |
| 抽查任务名称 | text | YES |  | NULL |  |
| 抽查类型 | text | YES |  | NULL |  |
| 抽查机关 | text | YES |  | NULL |  |
| 抽查完成日期 | datetime | YES |  | NULL |  |

## 📊 表：发票抬头

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 企业税号 | text | YES |  | NULL |  |

## 📊 表：受益所有人

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 受益所有人 | text | YES |  | NULL |  |
| 持股比例 | text | YES |  | NULL |  |
| 持股路径数量 | bigint | YES |  | NULL |  |
| 判断原因 | text | YES |  | NULL |  |
| 路径 | text | YES |  | NULL |  |

## 📊 表：司法协助

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 被执行人 | text | YES |  | NULL |  |
| 股权数额 | text | YES |  | NULL |  |
| 执行法院 | text | YES |  | NULL |  |
| 执行通知文书号 | text | YES |  | NULL |  |
| 类型 | text | YES |  | NULL |  |
| 状态 | text | YES |  | NULL |  |
| 是否历史 | text | YES |  | NULL |  |

## 📊 表：司法协助_历史_

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 被执行人 | text | YES |  | NULL |  |
| 股权数额 | text | YES |  | NULL |  |
| 执行法院 | text | YES |  | NULL |  |
| 执行通知文书号 | text | YES |  | NULL |  |
| 类型 | text | YES |  | NULL |  |
| 状态 | text | YES |  | NULL |  |
| 是否历史 | text | YES |  | NULL |  |

## 📊 表：司法拍卖

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 案号 | text | YES |  | NULL |  |
| 拍卖标的 | text | YES |  | NULL |  |
| 起拍价 | text | YES |  | NULL |  |
| 评估价 | text | YES |  | NULL |  |
| 拍卖日期 | datetime | YES |  | NULL |  |
| 处置法院 | text | YES |  | NULL |  |
| 拍卖阶段 | text | YES |  | NULL |  |
| 拍卖结果 | text | YES |  | NULL |  |
| 是否历史 | text | YES |  | NULL |  |

## 📊 表：司法案件_案件串联

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 案件名称 | text | YES |  | NULL |  |
| 案件类型 | text | YES |  | NULL |  |
| 案件身份 | text | YES |  | NULL |  |
| 案由 | text | YES |  | NULL |  |
| 案号 | text | YES |  | NULL |  |
| 法院 | text | YES |  | NULL |  |
| 最新审理程序 | text | YES |  | NULL |  |

## 📊 表：司法案件_诉讼关系

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 对方当事人 | text | YES |  | NULL |  |
| 司法案件数量 | bigint | YES |  | NULL |  |
| 关联风险数量 | bigint | YES |  | NULL |  |

## 📊 表：合作持股股东

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 合作持股股东 | text | YES |  | NULL |  |
| 共同持股企业数 | bigint | YES |  | NULL |  |
| 共同持股企业 | text | YES |  | NULL |  |
| 统一社会信用代码 | text | YES |  | NULL |  |
| 法定代表人_负责人 | text | YES |  | NULL |  |
| 经营状态 | text | YES |  | NULL |  |
| 省份 | text | YES |  | NULL |  |
| 市 | text | YES |  | NULL |  |
| 区域 | text | YES |  | NULL |  |
| 行业 | text | YES |  | NULL |  |
| 注册资本 | text | YES |  | NULL |  |
| 成立时间 | datetime | YES |  | NULL |  |
| 资本背景 | text | YES |  | NULL |  |
| 企业规模 | text | YES |  | NULL |  |
| 注册地址_全部_ | text | YES |  | NULL |  |
| 最新注册地址 | text | YES |  | NULL |  |
| 最新年报地址 | text | YES |  | NULL |  |
| 企业网址 | text | YES |  | NULL |  |
| 经营范围 | text | YES |  | NULL |  |
| 企业简介 | text | YES |  | NULL |  |
| 是否历史数据 | text | YES |  | NULL |  |

## 📊 表：同联系方式企业

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 企业名称 | text | YES |  | NULL |  |
| 法定代表人 | text | YES |  | NULL |  |
| 注册资本 | text | YES |  | NULL |  |
| 行业 | text | YES |  | NULL |  |
| 成立日期 | datetime | YES |  | NULL |  |
| 经营状态 | text | YES |  | NULL |  |
| 启信分 | text | YES |  | NULL |  |
| 相同联系方式 | text | YES |  | NULL |  |

## 📊 表：启信指数

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 启信分值 | text | YES |  | NULL |  |
| 启信分值详情 | text | YES |  | NULL |  |
| 行业排名 | text | YES |  | NULL |  |
| 启信分等级 | text | YES |  | NULL |  |
| 空壳指数 | text | YES |  | NULL |  |
| 空壳风险 | text | YES |  | NULL |  |
| 空壳等级 | text | YES |  | NULL |  |
| 合同违约指数 | text | YES |  | NULL |  |
| 违约等级 | text | YES |  | NULL |  |
| 合同违约风险 | text | YES |  | NULL |  |
| 科创评分 | text | YES |  | NULL |  |
| 科创评分详情 | text | YES |  | NULL |  |
| 科创等级 | text | YES |  | NULL |  |
| 科创标签 | text | YES |  | NULL |  |
| 涉诉案件数量 | bigint | YES |  | NULL |  |
| 涉诉总金额 | text | YES |  | NULL |  |
| 涉诉数量行业排名 | text | YES |  | NULL |  |

## 📊 表：商标信息_大陆

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 商标名称 | text | YES |  | NULL |  |
| 国际分类 | text | YES |  | NULL |  |
| 商标类型 | text | YES |  | NULL |  |
| 商标共有人 | text | YES |  | NULL |  |
| 专用权期限 | text | YES |  | NULL |  |
| 申请人名称 | text | YES |  | NULL |  |
| 申请人地址 | text | YES |  | NULL |  |
| 初审公告期号 | text | YES |  | NULL |  |
| 初审公告日期 | datetime | YES |  | NULL |  |
| 注册公告期号 | text | YES |  | NULL |  |
| 注册公告日期 | datetime | YES |  | NULL |  |
| 代理_办理机构 | text | YES |  | NULL |  |
| 国际注册日期 | datetime | YES |  | NULL |  |
| 后期指定日期 | datetime | YES |  | NULL |  |
| 优先权日期 | datetime | YES |  | NULL |  |
| 简单法律状态 | text | YES |  | NULL |  |
| 商标图片 | text | YES |  | NULL |  |

## 📊 表：商标信息_香港

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 商标名称 | text | YES |  | NULL |  |
| 是否系列商标 | text | YES |  | NULL |  |
| 申请人 | text | YES |  | NULL |  |
| 申请人地址 | text | YES |  | NULL |  |
| 提交日期 | datetime | YES |  | NULL |  |
| 注册日期 | datetime | YES |  | NULL |  |
| 公布获接纳注册申请日期 | datetime | YES |  | NULL |  |
| 实际注册日期 | datetime | YES |  | NULL |  |
| 注册届满日期 | datetime | YES |  | NULL |  |
| 商标描述 | text | YES |  | NULL |  |
| 代理机构信息 | text | YES |  | NULL |  |
| 优先权 | text | YES |  | NULL |  |
| 相关事项 | text | YES |  | NULL |  |
| 商标图片 | text | YES |  | NULL |  |

## 📊 表：土地抵押

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 土地位置 | text | YES |  | NULL |  |
| 抵押面积_公顷_ | double | YES |  | NULL |  |
| 土地用途 | text | YES |  | NULL |  |
| 起止时间 | datetime | YES |  | NULL |  |
| 土地抵押人 | text | YES |  | NULL |  |
| 土地抵押权人 | text | YES |  | NULL |  |

## 📊 表：域名信息

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 网站名称 | text | YES |  | NULL |  |
| 网址 | text | YES |  | NULL |  |
| 域名 | text | YES |  | NULL |  |
| 网站备案_许可证号 | text | YES |  | NULL |  |
| 登记批准日期 | datetime | YES |  | NULL |  |
| 是否历史 | text | YES |  | NULL |  |

## 📊 表：域名信息_历史_

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 网站名称 | text | YES |  | NULL |  |
| 网址 | text | YES |  | NULL |  |
| 域名 | text | YES |  | NULL |  |
| 网站备案_许可证号 | text | YES |  | NULL |  |
| 登记批准日期 | datetime | YES |  | NULL |  |
| 是否历史 | text | YES |  | NULL |  |

## 📊 表：大股东_上市公司

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 大股东名称 | text | YES |  | NULL |  |
| 股东类型 | text | YES |  | NULL |  |
| 股份类型 | text | YES |  | NULL |  |
| 持股比例 | text | YES |  | NULL |  |
| 持股数量 | text | YES |  | NULL |  |
| 最终受益股份 | text | YES |  | NULL |  |

## 📊 表：大股东_非上市公司

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 大股东名称 | text | YES |  | NULL |  |
| 股东类型 | text | YES |  | NULL |  |
| 持股比例 | text | YES |  | NULL |  |
| 认缴出资 | text | YES |  | NULL |  |
| 实缴出资 | text | YES |  | NULL |  |
| 最终受益股份 | text | YES |  | NULL |  |

## 📊 表：失信被执行人

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 立案日期 | datetime | YES |  | NULL |  |
| 发布日期 | datetime | YES |  | NULL |  |
| 执行标的 | text | YES |  | NULL |  |
| 执行法院 | text | YES |  | NULL |  |
| 被执行人履行情况 | text | YES |  | NULL |  |
| 案号 | text | YES |  | NULL |  |
| 是否历史记录 | text | YES |  | NULL |  |

## 📊 表：失信被执行人_历史_

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 立案日期 | datetime | YES |  | NULL |  |
| 发布日期 | datetime | YES |  | NULL |  |
| 执行标的 | text | YES |  | NULL |  |
| 执行法院 | text | YES |  | NULL |  |
| 被执行人履行情况 | text | YES |  | NULL |  |
| 案号 | text | YES |  | NULL |  |
| 是否历史记录 | text | YES |  | NULL |  |

## 📊 表：实控企业

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 控制企业名称 | text | YES |  | NULL |  |
| 投资比例 | text | YES |  | NULL |  |
| 统一社会信用代码 | text | YES |  | NULL |  |
| 法定代表人_负责人_执行事务合伙人 | text | YES |  | NULL |  |
| 经营状态 | text | YES |  | NULL |  |
| 省份 | text | YES |  | NULL |  |
| 市 | text | YES |  | NULL |  |
| 区域 | text | YES |  | NULL |  |
| 行业 | text | YES |  | NULL |  |
| 注册资本 | text | YES |  | NULL |  |
| 成立时间 | datetime | YES |  | NULL |  |
| 资本背景 | text | YES |  | NULL |  |
| 企业规模 | text | YES |  | NULL |  |
| 注册地址_全部_ | text | YES |  | NULL |  |
| 最新注册地址 | text | YES |  | NULL |  |
| 最新年报地址 | text | YES |  | NULL |  |
| 企业网址 | text | YES |  | NULL |  |
| 经营范围 | text | YES |  | NULL |  |
| 企业简介 | text | YES |  | NULL |  |
| 是否历史数据 | text | YES |  | NULL |  |

## 📊 表：实际控制人

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 疑似实际控制人 | text | YES |  | NULL |  |
| 层级股比 | text | YES |  | NULL |  |
| 路径 | text | YES |  | NULL |  |

## 📊 表：客户

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 客户名称 | text | YES |  | NULL |  |
| 统一社会信用代码 | text | YES |  | NULL |  |
| 合作总次数 | bigint | YES |  | NULL |  |
| 合作总金额_万元_ | text | YES |  | NULL |  |
| 最近合作时间 | datetime | YES |  | NULL |  |
| 最新合作项目 | text | YES |  | NULL |  |
| 最近合作金额_万元_ | text | YES |  | NULL |  |
| 最新合作数据来源 | text | YES |  | NULL |  |
| 招标联系人姓名_来源于招投标公告_ | text | YES |  | NULL |  |
| 招标人电话_来源于招投标公告_ | text | YES |  | NULL |  |
| 招标人地址_来源于招投标公告_ | text | YES |  | NULL |  |
| 地区 | text | YES |  | NULL |  |
| 地址_全部_ | text | YES |  | NULL |  |
| 经营状态 | text | YES |  | NULL |  |
| 注册资本 | text | YES |  | NULL |  |
| 成立日期 | datetime | YES |  | NULL |  |
| 行业_一级_ | text | YES |  | NULL |  |
| 行业_二级_ | text | YES |  | NULL |  |
| 电话_全部_ | text | YES |  | NULL |  |
| 资本背景 | text | YES |  | NULL |  |
| 企业规模 | text | YES |  | NULL |  |
| 资质标签_科技认定_ | text | YES |  | NULL |  |

## 📊 表：对外投资

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 被投资企业 | text | YES |  | NULL |  |
| 投资数额 | text | YES |  | NULL |  |
| 投资比列 | text | YES |  | NULL |  |
| 统一社会信用代码 | text | YES |  | NULL |  |
| 法定代表人_负责人_执行事务合伙人 | text | YES |  | NULL |  |
| 经营状态 | text | YES |  | NULL |  |
| 省份 | text | YES |  | NULL |  |
| 市 | text | YES |  | NULL |  |
| 区域 | text | YES |  | NULL |  |
| 行业 | text | YES |  | NULL |  |
| 注册资本 | text | YES |  | NULL |  |
| 成立日期 | datetime | YES |  | NULL |  |
| 资本背景 | text | YES |  | NULL |  |
| 企业规模 | text | YES |  | NULL |  |
| 注册地址_全部_ | text | YES |  | NULL |  |
| 最新注册地址 | text | YES |  | NULL |  |
| 最新年报地址 | text | YES |  | NULL |  |
| 企业网址 | text | YES |  | NULL |  |
| 经营范围 | text | YES |  | NULL |  |
| 企业简介 | text | YES |  | NULL |  |
| 是否历史数据 | text | YES |  | NULL |  |

## 📊 表：对外投资_历史_

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 被投资企业 | text | YES |  | NULL |  |
| 投资数额 | text | YES |  | NULL |  |
| 投资比列 | text | YES |  | NULL |  |
| 统一社会信用代码 | text | YES |  | NULL |  |
| 法定代表人_负责人_执行事务合伙人 | text | YES |  | NULL |  |
| 经营状态 | text | YES |  | NULL |  |
| 省份 | text | YES |  | NULL |  |
| 市 | text | YES |  | NULL |  |
| 区域 | text | YES |  | NULL |  |
| 行业 | text | YES |  | NULL |  |
| 注册资本 | text | YES |  | NULL |  |
| 成立日期 | datetime | YES |  | NULL |  |
| 资本背景 | text | YES |  | NULL |  |
| 企业规模 | text | YES |  | NULL |  |
| 注册地址_全部_ | text | YES |  | NULL |  |
| 最新注册地址 | text | YES |  | NULL |  |
| 最新年报地址 | text | YES |  | NULL |  |
| 企业网址 | text | YES |  | NULL |  |
| 经营范围 | text | YES |  | NULL |  |
| 企业简介 | text | YES |  | NULL |  |
| 是否历史数据 | text | YES |  | NULL |  |

## 📊 表：尽调结果

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 启信分值 | text | YES |  | NULL |  |
| 启信分值详情 | text | YES |  | NULL |  |
| 行业排名 | text | YES |  | NULL |  |
| 启信分等级 | text | YES |  | NULL |  |
| 空壳指数 | text | YES |  | NULL |  |
| 空壳风险 | text | YES |  | NULL |  |
| 空壳等级 | text | YES |  | NULL |  |
| 合同违约指数 | text | YES |  | NULL |  |
| 违约等级 | text | YES |  | NULL |  |
| 合同违约风险 | text | YES |  | NULL |  |
| 科创评分 | text | YES |  | NULL |  |
| 科创评分详情 | text | YES |  | NULL |  |
| 科创等级 | text | YES |  | NULL |  |
| 科创标签 | text | YES |  | NULL |  |
| 涉诉案件数量 | bigint | YES |  | NULL |  |
| 涉诉总金额 | text | YES |  | NULL |  |
| 涉诉数量行业排名 | text | YES |  | NULL |  |
| 实际控制人 | text | YES |  | NULL |  |
| 受益所有人 | bigint | YES |  | NULL |  |
| 工商股东 | bigint | YES |  | NULL |  |
| 最新公示股东 | bigint | YES |  | NULL |  |
| 大股东 | text | YES |  | NULL |  |
| 间接股东 | bigint | YES |  | NULL |  |
| 实控企业 | bigint | YES |  | NULL |  |
| 间接持股企业 | bigint | YES |  | NULL |  |
| 合作持股股东 | bigint | YES |  | NULL |  |
| 对外投资 | bigint | YES |  | NULL |  |
| 主要人员_工商公示 | bigint | YES |  | NULL |  |
| 主要人员_最新公示 | bigint | YES |  | NULL |  |
| 总公司 | text | YES |  | NULL |  |
| 供应商 | bigint | YES |  | NULL |  |
| 客户 | bigint | YES |  | NULL |  |
| 疑似关系 | bigint | YES |  | NULL |  |
| 同联系方式企业 | text | YES |  | NULL |  |
| 司法案件 | bigint | YES |  | NULL |  |
| 立案信息 | bigint | YES |  | NULL |  |
| 开庭公告 | bigint | YES |  | NULL |  |
| 法院公告 | bigint | YES |  | NULL |  |
| 送达公告 | bigint | YES |  | NULL |  |
| 裁判文书 | bigint | YES |  | NULL |  |
| 被执行人_数量 | bigint | YES |  | NULL |  |
| 被执行人_金额_元_ | bigint | YES |  | NULL |  |
| 失信被执行人 | bigint | YES |  | NULL |  |
| 股权冻结 | bigint | YES |  | NULL |  |
| 限制高消费 | bigint | YES |  | NULL |  |
| 终本案件 | bigint | YES |  | NULL |  |
| 司法协助 | bigint | YES |  | NULL |  |
| 司法拍卖 | bigint | YES |  | NULL |  |
| 询价评估 | bigint | YES |  | NULL |  |
| 经营异常 | bigint | YES |  | NULL |  |
| 严重违法失信 | bigint | YES |  | NULL |  |
| 行政处罚 | bigint | YES |  | NULL |  |
| 违法违规建设 | bigint | YES |  | NULL |  |
| 环保处罚 | bigint | YES |  | NULL |  |
| 破产案件 | bigint | YES |  | NULL |  |
| 强制清算 | bigint | YES |  | NULL |  |
| 清算信息 | bigint | YES |  | NULL |  |
| 股权出质 | bigint | YES |  | NULL |  |
| 动产抵押 | bigint | YES |  | NULL |  |
| 欠税信息_数量 | bigint | YES |  | NULL |  |
| 欠税信息_金额_元_ | double | YES |  | NULL |  |
| 土地抵押 | bigint | YES |  | NULL |  |
| 重大税收违法 | bigint | YES |  | NULL |  |
| 非正常户 | bigint | YES |  | NULL |  |
| 知识产权出质 | bigint | YES |  | NULL |  |
| 简易注销 | bigint | YES |  | NULL |  |
| 涉嫌冒用他人身份登记信息 | bigint | YES |  | NULL |  |
| 注销备案 | bigint | YES |  | NULL |  |
| 股权质押 | bigint | YES |  | NULL |  |
| 黑名单 | bigint | YES |  | NULL |  |
| 财务信息 | text | YES |  | NULL |  |
| 融资信息 | bigint | YES |  | NULL |  |
| 担保信息 | bigint | YES |  | NULL |  |
| 招聘信息 | bigint | YES |  | NULL |  |
| 行政许可 | bigint | YES |  | NULL |  |
| 资质认证 | bigint | YES |  | NULL |  |
| 一般纳税人资格 | text | YES |  | NULL |  |
| 税务评级 | text | YES |  | NULL |  |
| 排污许可 | bigint | YES |  | NULL |  |
| 电信许可 | bigint | YES |  | NULL |  |
| 抽查信息 | bigint | YES |  | NULL |  |
| 双随机抽查 | bigint | YES |  | NULL |  |
| 发票抬头 | text | YES |  | NULL |  |
| 票据承兑 | bigint | YES |  | NULL |  |
| IPO进程 | text | YES |  | NULL |  |
| 主体评级 | text | YES |  | NULL |  |
| 股票信息 | text | YES |  | NULL |  |
| 债券信息 | bigint | YES |  | NULL |  |
| 进出口信用 | text | YES |  | NULL |  |
| 公司产品 | bigint | YES |  | NULL |  |
| 新闻舆情 | bigint | YES |  | NULL |  |
| 域名信息 | bigint | YES |  | NULL |  |
| 专利信息 | bigint | YES |  | NULL |  |
| 商标信息 | bigint | YES |  | NULL |  |
| 著作权 | bigint | YES |  | NULL |  |
| 软件著作权 | bigint | YES |  | NULL |  |
| 政府奖励项目 | bigint | YES |  | NULL |  |
| 工商变更_历史_ | bigint | YES |  | NULL |  |
| 主要人员_历史__工商公示 | bigint | YES |  | NULL |  |
| 主要人员_历史__最新公示 | bigint | YES |  | NULL |  |
| 减资公告_历史_ | bigint | YES |  | NULL |  |
| 对外投资_历史_ | bigint | YES |  | NULL |  |
| 立案信息_历史_ | bigint | YES |  | NULL |  |
| 开庭公告_历史_ | bigint | YES |  | NULL |  |
| 被执行人_历史__数量 | bigint | YES |  | NULL |  |
| 被执行人_历史__金额_元_ | bigint | YES |  | NULL |  |
| 失信被执行人_历史_ | bigint | YES |  | NULL |  |
| 股权冻结_历史_ | bigint | YES |  | NULL |  |
| 限制高消费_历史_ | bigint | YES |  | NULL |  |
| 终本案件_历史_ | bigint | YES |  | NULL |  |
| 司法协助_历史_ | bigint | YES |  | NULL |  |
| 经营异常_历史_ | bigint | YES |  | NULL |  |
| 严重违法失信_历史_ | bigint | YES |  | NULL |  |
| 破产案件_历史_ | bigint | YES |  | NULL |  |
| 强制清算_历史_ | bigint | YES |  | NULL |  |
| 股权出质_历史_ | bigint | YES |  | NULL |  |
| 动产抵押_历史_ | bigint | YES |  | NULL |  |
| 欠税信息_历史__数量 | bigint | YES |  | NULL |  |
| 欠税信息_历史__金额_元_ | double | YES |  | NULL |  |
| 知识产权出质_历史_ | bigint | YES |  | NULL |  |
| 抽查信息_历史_ | bigint | YES |  | NULL |  |
| 双随机抽查_历史_ | bigint | YES |  | NULL |  |
| 电信许可_历史_ | bigint | YES |  | NULL |  |
| 质权人_历史_ | bigint | YES |  | NULL |  |
| 票据承兑_历史_ | bigint | YES |  | NULL |  |
| 工商股东_历史_ | bigint | YES |  | NULL |  |
| 最新公示股东_历史_ | bigint | YES |  | NULL |  |
| 行政处罚_历史_ | bigint | YES |  | NULL |  |
| 行政许可_历史_ | bigint | YES |  | NULL |  |
| 资质认证_历史_ | bigint | YES |  | NULL |  |
| 排污许可_历史_ | bigint | YES |  | NULL |  |
| 域名信息_历史_ | bigint | YES |  | NULL |  |

## 📊 表：工商变更_历史_

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 变更日期 | datetime | YES |  | NULL |  |
| 是否历史记录 | text | YES |  | NULL |  |
| 变更事项 | text | YES |  | NULL |  |
| 变更前 | text | YES |  | NULL |  |
| 变更后 | text | YES |  | NULL |  |

## 📊 表：工商股东

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 股东名称 | text | YES |  | NULL |  |
| 统一社会信用代码 | text | YES |  | NULL |  |
| 地区 | text | YES |  | NULL |  |
| 经营状态 | text | YES |  | NULL |  |
| 股东类型 | text | YES |  | NULL |  |
| 持股比例 | text | YES |  | NULL |  |
| 认缴出资金额 | text | YES |  | NULL |  |
| 认缴出资明细 | text | YES |  | NULL |  |
| 实缴出资金额 | text | YES |  | NULL |  |
| 实缴出资明细 | text | YES |  | NULL |  |

## 📊 表：工商股东_历史_

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 股东名称 | text | YES |  | NULL |  |
| 统一社会信用代码 | text | YES |  | NULL |  |
| 地区 | text | YES |  | NULL |  |
| 经营状态 | text | YES |  | NULL |  |
| 股东类型 | text | YES |  | NULL |  |
| 持股比例 | text | YES |  | NULL |  |
| 认缴出资金额 | text | YES |  | NULL |  |
| 认缴出资明细 | text | YES |  | NULL |  |
| 实缴出资金额 | text | YES |  | NULL |  |
| 实缴出资明细 | text | YES |  | NULL |  |

## 📊 表：开庭公告

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 案号 | text | YES |  | NULL |  |
| 身份 | text | YES |  | NULL |  |
| 当事人 | text | YES |  | NULL |  |
| 开庭时间 | datetime | YES |  | NULL |  |
| 案由 | text | YES |  | NULL |  |
| 是否历史消息 | text | YES |  | NULL |  |

## 📊 表：开庭公告_历史_

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 案号 | text | YES |  | NULL |  |
| 身份 | text | YES |  | NULL |  |
| 当事人 | text | YES |  | NULL |  |
| 开庭时间 | datetime | YES |  | NULL |  |
| 案由 | text | YES |  | NULL |  |
| 是否历史消息 | text | YES |  | NULL |  |

## 📊 表：强制清算

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 案号 | text | YES |  | NULL |  |
| 案件类型 | text | YES |  | NULL |  |
| 申请人 | text | YES |  | NULL |  |
| 公开日期 | datetime | YES |  | NULL |  |

## 📊 表：强制清算_历史_

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 案号 | text | YES |  | NULL |  |
| 案件类型 | text | YES |  | NULL |  |
| 申请人 | text | YES |  | NULL |  |
| 公开日期 | datetime | YES |  | NULL |  |

## 📊 表：总公司

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 企业名称 | text | YES |  | NULL |  |
| 法定代表人 | text | YES |  | NULL |  |
| 注册资本 | text | YES |  | NULL |  |
| 成立日期 | datetime | YES |  | NULL |  |
| 经营状态 | text | YES |  | NULL |  |

## 📊 表：抽查信息

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 检查实施机关 | text | YES |  | NULL |  |
| 类型 | text | YES |  | NULL |  |
| 日期 | datetime | YES |  | NULL |  |
| 结果 | text | YES |  | NULL |  |

## 📊 表：抽查信息_历史_

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 检查实施机关 | text | YES |  | NULL |  |
| 类型 | text | YES |  | NULL |  |
| 日期 | datetime | YES |  | NULL |  |
| 结果 | text | YES |  | NULL |  |

## 📊 表：担保信息

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 担保方 | text | YES |  | NULL |  |
| 被担保方 | text | YES |  | NULL |  |
| 担保方式 | text | YES |  | NULL |  |
| 担保金额 | text | YES |  | NULL |  |
| 履行状态 | text | YES |  | NULL |  |
| 公告日期 | datetime | YES |  | NULL |  |
| 报告期 | text | YES |  | NULL |  |
| 担保期限 | text | YES |  | NULL |  |

## 📊 表：招聘信息

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 发布时间 | datetime | YES |  | NULL |  |
| 职位 | text | YES |  | NULL |  |
| 薪资 | text | YES |  | NULL |  |
| 学历 | text | YES |  | NULL |  |
| 地区 | text | YES |  | NULL |  |
| 经验 | text | YES |  | NULL |  |

## 📊 表：排污许可

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 证书编号 | text | YES |  | NULL |  |
| 有效期 | text | YES |  | NULL |  |
| 发证时间 | datetime | YES |  | NULL |  |
| 发证单位 | text | YES |  | NULL |  |

## 📊 表：排污许可_历史_

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 证书编号 | text | YES |  | NULL |  |
| 有效期 | text | YES |  | NULL |  |
| 发证时间 | datetime | YES |  | NULL |  |
| 发证单位 | text | YES |  | NULL |  |

## 📊 表：政府奖励项目

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 奖励名称 | text | YES |  | NULL |  |
| 奖励等级 | text | YES |  | NULL |  |
| 奖励项目名称 | text | YES |  | NULL |  |
| 奖励年份 | bigint | YES |  | NULL |  |
| 发布时间 | datetime | YES |  | NULL |  |
| 相关人员 | text | YES |  | NULL |  |

## 📊 表：新闻舆情

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 刊发媒体 | text | YES |  | NULL |  |
| 标题 | text | YES |  | NULL |  |
| 摘要 | text | YES |  | NULL |  |
| 情感属性 | text | YES |  | NULL |  |
| 日期 | datetime | YES |  | NULL |  |
| 内容分类 | text | YES |  | NULL |  |
| 链接 | text | YES |  | NULL |  |

## 📊 表：最新公示股东_上市公司

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 股东名称 | text | YES |  | NULL |  |
| 统一社会信用代码 | text | YES |  | NULL |  |
| 地区 | text | YES |  | NULL |  |
| 经营状态 | text | YES |  | NULL |  |
| 股东类型 | text | YES |  | NULL |  |
| 股份类型 | text | YES |  | NULL |  |
| 持股比例 | text | YES |  | NULL |  |
| 持股数_股_ | text | YES |  | NULL |  |
| 是否历史记录 | text | YES |  | NULL |  |

## 📊 表：最新公示股东_历史__上市公司

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 股东名称 | text | YES |  | NULL |  |
| 统一社会信用代码 | text | YES |  | NULL |  |
| 地区 | text | YES |  | NULL |  |
| 经营状态 | text | YES |  | NULL |  |
| 股东类型 | text | YES |  | NULL |  |
| 股份类型 | text | YES |  | NULL |  |
| 持股比例 | text | YES |  | NULL |  |
| 持股数_股_ | text | YES |  | NULL |  |
| 是否历史记录 | text | YES |  | NULL |  |

## 📊 表：最新公示股东_历史__非上市公司

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 股东名称 | text | YES |  | NULL |  |
| 统一社会信用代码 | text | YES |  | NULL |  |
| 地区 | text | YES |  | NULL |  |
| 经营状态 | text | YES |  | NULL |  |
| 股东类型 | text | YES |  | NULL |  |
| 持股比例 | text | YES |  | NULL |  |
| 认缴出资金额 | text | YES |  | NULL |  |
| 认缴出资时间 | datetime | YES |  | NULL |  |
| 实际出资金额 | text | YES |  | NULL |  |
| 是否历史记录 | text | YES |  | NULL |  |

## 📊 表：最新公示股东_历史_上市公司

**注释**: 最新公示股东(历史)-上市公司数据

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | int | NO | PRI | NULL | 导入唯一标识ID |
| 批量上传公司名称 | varchar(255) | NO |  | NULL | 批量上传的公司名称 |
| 系统匹配公司名称 | varchar(255) | YES |  | NULL | 系统匹配的公司名称 |
| 股东名称 | varchar(255) | NO |  | NULL | 股东姓名或机构名称 |
| 统一社会信用代码 | varchar(50) | YES |  | NULL | 股东的统一社会信用代码 |
| 地区 | varchar(100) | YES |  | NULL | 股东所在地区 |
| 经营状态 | varchar(50) | YES |  | NULL | 股东经营状态 |
| 股东类型 | varchar(50) | YES |  | NULL | 股东类型（如个人、机构、证券投资基金等） |
| 股份类型 | varchar(50) | YES |  | NULL | 股份类型（如流通A股、限售股等） |
| 持股比例 | decimal(10,4) | YES |  | NULL | 持股比例（%） |
| 持股数_股_ | bigint | YES |  | NULL | 持股数量（股），用BIGINT支持大数值 |
| 是否历史记录 | varchar(10) | YES |  | NULL | 是否为历史记录（是/否） |

## 📊 表：最新公示股东_历史_非上市公司

**注释**: 最新公示股东(历史)-非上市公司数据表

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | int | NO | PRI | NULL | 导入唯一标识ID（主键） |
| 批量上传公司名称 | varchar(255) | NO |  | NULL | 批量上传时的公司名称 |
| 系统匹配公司名称 | varchar(255) | YES |  | NULL | 系统自动匹配的公司名称 |
| 股东名称 | varchar(255) | NO |  | NULL | 股东姓名（个人）或机构名称 |
| 统一社会信用代码 | varchar(50) | YES |  | NULL | 股东的统一社会信用代码 |
| 地区 | varchar(100) | YES |  | NULL | 股东所在省/市/区 |
| 经营状态 | varchar(50) | YES |  | NULL | 股东经营状态 |
| 股东类型 | varchar(50) | YES |  | NULL | 股东类型（个人/机构等） |
| 认缴出资额 | decimal(20,4) | YES |  | NULL | 认缴出资额 |
| 认缴出资日期 | date | YES |  | NULL | 认缴出资日期 |
| 实缴出资额 | decimal(20,4) | YES |  | NULL | 实缴出资额 |
| 实缴出资日期 | date | YES |  | NULL | 实缴出资日期 |
| 出资比例 | decimal(10,4) | YES |  | NULL | 出资比例（%） |
| 是否历史记录 | varchar(10) | YES |  | NULL | 是否为历史数据（是/否） |

## 📊 表：最新公示股东_非上市公司

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 股东名称 | text | YES |  | NULL |  |
| 统一社会信用代码 | text | YES |  | NULL |  |
| 地区 | text | YES |  | NULL |  |
| 经营状态 | text | YES |  | NULL |  |
| 股东类型 | text | YES |  | NULL |  |
| 持股比例 | text | YES |  | NULL |  |
| 认缴出资金额 | text | YES |  | NULL |  |
| 认缴出资时间 | datetime | YES |  | NULL |  |
| 实际出资金额 | text | YES |  | NULL |  |
| 是否历史记录 | text | YES |  | NULL |  |

## 📊 表：欠税信息

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 纳税人识别号 | text | YES |  | NULL |  |
| 欠税税种 | text | YES |  | NULL |  |
| 欠税金额_元_ | double | YES |  | NULL |  |
| 当前新发生的欠税额 | double | YES |  | NULL |  |
| 发布时间 | datetime | YES |  | NULL |  |
| 发布单位 | text | YES |  | NULL |  |
| 是否历史数据 | text | YES |  | NULL |  |

## 📊 表：欠税信息_历史_

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 纳税人识别号 | text | YES |  | NULL |  |
| 欠税税种 | text | YES |  | NULL |  |
| 欠税金额_元_ | double | YES |  | NULL |  |
| 当前新发生的欠税额 | double | YES |  | NULL |  |
| 发布时间 | datetime | YES |  | NULL |  |
| 发布单位 | text | YES |  | NULL |  |
| 是否历史数据 | text | YES |  | NULL |  |

## 📊 表：法院公告

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 公告类型 | text | YES |  | NULL |  |
| 身份 | text | YES |  | NULL |  |
| 当事人 | text | YES |  | NULL |  |
| 发布时间 | datetime | YES |  | NULL |  |
| 公告内容 | text | YES |  | NULL |  |

## 📊 表：注销备案

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 清算组备案日期 | datetime | YES |  | NULL |  |
| 清算组成立日期 | datetime | YES |  | NULL |  |
| 注销原因 | text | YES |  | NULL |  |
| 状态 | text | YES |  | NULL |  |
| 清算组负责人 | text | YES |  | NULL |  |
| 清算组成员 | text | YES |  | NULL |  |
| 债权人公告期 | text | YES |  | NULL |  |
| 公告内容 | text | YES |  | NULL |  |

## 📊 表：涉嫌冒用他人身份登记信息

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 冒名登记事项 | text | YES |  | NULL |  |
| 冒名登记时间 | datetime | YES |  | NULL |  |
| 登记机关联系方式 | text | YES |  | NULL |  |
| 公告期自 | text | YES |  | NULL |  |
| 公告期至 | text | YES |  | NULL |  |
| 处理结果 | text | YES |  | NULL |  |

## 📊 表：清算信息

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 清算组负责人 | text | YES |  | NULL |  |
| 清算组成员 | text | YES |  | NULL |  |

## 📊 表：环保处罚

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 处罚日期 | datetime | YES |  | NULL |  |
| 决定书文号 | text | YES |  | NULL |  |
| 违法行为类型 | text | YES |  | NULL |  |
| 处罚内容 | text | YES |  | NULL |  |
| 罚款金额 | text | YES |  | NULL |  |
| 做出处罚决定机关名称 | text | YES |  | NULL |  |
| 公示日期 | datetime | YES |  | NULL |  |
| 处罚依据 | text | YES |  | NULL |  |
| 是否历史 | text | YES |  | NULL |  |

## 📊 表：电信许可

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 许可证号 | text | YES |  | NULL |  |
| 业务种类 | text | YES |  | NULL |  |
| 覆盖范围 | text | YES |  | NULL |  |

## 📊 表：电信许可_历史_

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 许可证号 | text | YES |  | NULL |  |
| 业务种类 | text | YES |  | NULL |  |
| 覆盖范围 | text | YES |  | NULL |  |

## 📊 表：疑似关系

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 疑似关系企业 | text | YES |  | NULL |  |
| 法定代表人_负责人 | text | YES |  | NULL |  |
| 注册资本 | text | YES |  | NULL |  |
| 成立日期 | datetime | YES |  | NULL |  |
| 疑似关联类型 | text | YES |  | NULL |  |
| 疑似关联详情 | text | YES |  | NULL |  |

## 📊 表：知识产权出质

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 出质人 | text | YES |  | NULL |  |
| 质权人 | text | YES |  | NULL |  |
| 状态 | text | YES |  | NULL |  |
| 公示日期 | datetime | YES |  | NULL |  |

## 📊 表：知识产权出质_历史_

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 出质人 | text | YES |  | NULL |  |
| 质权人 | text | YES |  | NULL |  |
| 状态 | text | YES |  | NULL |  |
| 公示日期 | datetime | YES |  | NULL |  |

## 📊 表：破产案件

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 案号 | text | YES |  | NULL |  |
| 案件类型 | text | YES |  | NULL |  |
| 经办法院 | text | YES |  | NULL |  |
| 被申请人 | text | YES |  | NULL |  |
| 申请人 | text | YES |  | NULL |  |
| 公开日期 | datetime | YES |  | NULL |  |

## 📊 表：破产案件_历史_

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 案号 | text | YES |  | NULL |  |
| 案件类型 | text | YES |  | NULL |  |
| 经办法院 | text | YES |  | NULL |  |
| 被申请人 | text | YES |  | NULL |  |
| 申请人 | text | YES |  | NULL |  |
| 公开日期 | datetime | YES |  | NULL |  |

## 📊 表：票据承兑

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 披露信息时点日期 | datetime | YES |  | NULL |  |
| 承兑人开户机构名称 | text | YES |  | NULL |  |
| 累计承兑发生额_元_ | text | YES |  | NULL |  |
| 承兑余额_元_ | text | YES |  | NULL |  |
| 累计逾期发生额_元_ | text | YES |  | NULL |  |
| 逾期余额_元_ | text | YES |  | NULL |  |
| 票据介质 | text | YES |  | NULL |  |
| 披露日期 | datetime | YES |  | NULL |  |
| 系统备注 | text | YES |  | NULL |  |
| 企业备注 | text | YES |  | NULL |  |

## 📊 表：税务评级

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 评价年度 | bigint | YES |  | NULL |  |
| 纳税人识别号 | text | YES |  | NULL |  |
| 纳税信用等级 | text | YES |  | NULL |  |
| 纳税人名称 | text | YES |  | NULL |  |

## 📊 表：立案信息

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 案号 | text | YES |  | NULL |  |
| 身份 | text | YES |  | NULL |  |
| 当事人 | text | YES |  | NULL |  |
| 案由 | text | YES |  | NULL |  |
| 立案时间 | datetime | YES |  | NULL |  |
| 开庭时间 | datetime | YES |  | NULL |  |
| 结束时间 | datetime | YES |  | NULL |  |
| 案件状态 | text | YES |  | NULL |  |
| 是否历史消息 | text | YES |  | NULL |  |

## 📊 表：立案信息_历史_

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 案号 | text | YES |  | NULL |  |
| 身份 | text | YES |  | NULL |  |
| 当事人 | text | YES |  | NULL |  |
| 案由 | text | YES |  | NULL |  |
| 立案时间 | datetime | YES |  | NULL |  |
| 开庭时间 | datetime | YES |  | NULL |  |
| 结束时间 | datetime | YES |  | NULL |  |
| 案件状态 | text | YES |  | NULL |  |
| 是否历史消息 | text | YES |  | NULL |  |

## 📊 表：简易注销

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 公告日期 | datetime | YES |  | NULL |  |
| 异议申请人_异议时间_异议内容 | datetime | YES |  | NULL |  |
| 简易注销结果 | text | YES |  | NULL |  |
| 公告申请日期 | datetime | YES |  | NULL |  |

## 📊 表：终本案件

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 终本时间 | datetime | YES |  | NULL |  |
| 执行标的 | text | YES |  | NULL |  |
| 未履行金额 | text | YES |  | NULL |  |
| 立案时间 | datetime | YES |  | NULL |  |
| 执行法院 | text | YES |  | NULL |  |
| 履行状态 | text | YES |  | NULL |  |
| 终本案号 | text | YES |  | NULL |  |
| 是否历史记录 | text | YES |  | NULL |  |

## 📊 表：终本案件_历史_

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 终本时间 | datetime | YES |  | NULL |  |
| 执行标的 | text | YES |  | NULL |  |
| 未履行金额 | text | YES |  | NULL |  |
| 立案时间 | datetime | YES |  | NULL |  |
| 执行法院 | text | YES |  | NULL |  |
| 履行状态 | text | YES |  | NULL |  |
| 终本案号 | text | YES |  | NULL |  |
| 是否历史记录 | text | YES |  | NULL |  |

## 📊 表：经营异常

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 做出决定机关 | text | YES |  | NULL |  |
| 列入经营异常名录原因 | text | YES |  | NULL |  |
| 列入日期 | datetime | YES |  | NULL |  |
| 移出经营异常名录原因 | text | YES |  | NULL |  |
| 移出日期 | datetime | YES |  | NULL |  |
| 是否历史数据 | text | YES |  | NULL |  |

## 📊 表：经营异常_历史_

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 做出决定机关 | text | YES |  | NULL |  |
| 列入经营异常名录原因 | text | YES |  | NULL |  |
| 列入日期 | datetime | YES |  | NULL |  |
| 移出经营异常名录原因 | text | YES |  | NULL |  |
| 移出日期 | datetime | YES |  | NULL |  |
| 是否历史数据 | text | YES |  | NULL |  |

## 📊 表：股权冻结

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 执行通知书文号 | text | YES |  | NULL |  |
| 被执行人 | text | YES |  | NULL |  |
| 冻结股权的标的企业 | text | YES |  | NULL |  |
| 股权数额 | text | YES |  | NULL |  |
| 执行法院 | text | YES |  | NULL |  |
| 状态 | text | YES |  | NULL |  |
| 起止日期 | datetime | YES |  | NULL |  |
| 公示时间 | datetime | YES |  | NULL |  |

## 📊 表：股权冻结_历史_

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 执行通知书文号 | text | YES |  | NULL |  |
| 被执行人 | text | YES |  | NULL |  |
| 冻结股权的标的企业 | text | YES |  | NULL |  |
| 股权数额 | text | YES |  | NULL |  |
| 执行法院 | text | YES |  | NULL |  |
| 状态 | text | YES |  | NULL |  |
| 起止日期 | datetime | YES |  | NULL |  |
| 公示时间 | datetime | YES |  | NULL |  |

## 📊 表：股权出质

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 登记日期 | datetime | YES |  | NULL |  |
| 公示日期 | datetime | YES |  | NULL |  |
| 登记编号 | text | YES |  | NULL |  |
| 出质人 | text | YES |  | NULL |  |
| 出质股权数额 | text | YES |  | NULL |  |
| 出质人证件号码 | text | YES |  | NULL |  |
| 质权人 | text | YES |  | NULL |  |
| 质权人证件号码 | text | YES |  | NULL |  |
| 状态 | text | YES |  | NULL |  |
| 出质股权标的企业 | text | YES |  | NULL |  |
| 备注 | text | YES |  | NULL |  |
| 是否历史数据 | text | YES |  | NULL |  |
| 是否下架 | text | YES |  | NULL |  |

## 📊 表：股权出质_历史_

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 登记日期 | datetime | YES |  | NULL |  |
| 公示日期 | datetime | YES |  | NULL |  |
| 登记编号 | text | YES |  | NULL |  |
| 出质人 | text | YES |  | NULL |  |
| 出质股权数额 | text | YES |  | NULL |  |
| 出质人证件号码 | text | YES |  | NULL |  |
| 质权人 | text | YES |  | NULL |  |
| 质权人证件号码 | text | YES |  | NULL |  |
| 状态 | text | YES |  | NULL |  |
| 出质股权标的企业 | text | YES |  | NULL |  |
| 备注 | text | YES |  | NULL |  |
| 是否历史数据 | text | YES |  | NULL |  |
| 是否下架 | text | YES |  | NULL |  |

## 📊 表：股权质押_上市公司

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 股东名称 | text | YES |  | NULL |  |
| 质押权人 | text | YES |  | NULL |  |
| 本次质押股数 | text | YES |  | NULL |  |
| 剩余未解押数 | text | YES |  | NULL |  |
| 占持股比 | text | YES |  | NULL |  |
| 占总股比 | text | YES |  | NULL |  |
| 当前进度 | text | YES |  | NULL |  |
| 质押原因 | text | YES |  | NULL |  |
| 质押目的 | text | YES |  | NULL |  |
| 质押日期 | datetime | YES |  | NULL |  |
| 解押日期 | datetime | YES |  | NULL |  |
| 更新日期 | datetime | YES |  | NULL |  |
| 是否历史 | text | YES |  | NULL |  |

## 📊 表：股权质押_非上市公司

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 质押人 | text | YES |  | NULL |  |
| 质押人参股企业 | text | YES |  | NULL |  |
| 质押权人 | text | YES |  | NULL |  |
| 本次质押股数 | text | YES |  | NULL |  |
| 剩余未解押数 | text | YES |  | NULL |  |
| 占持股比 | text | YES |  | NULL |  |
| 占总股比 | text | YES |  | NULL |  |
| 当前进度 | text | YES |  | NULL |  |
| 质押原因 | text | YES |  | NULL |  |
| 质押目的 | text | YES |  | NULL |  |
| 质押日期 | datetime | YES |  | NULL |  |
| 解押日期 | datetime | YES |  | NULL |  |
| 更新日期 | datetime | YES |  | NULL |  |
| 是否历史 | text | YES |  | NULL |  |

## 📊 表：股票信息

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 股票名称 | text | YES |  | NULL |  |
| 股票类型 | text | YES |  | NULL |  |
| 代码 | bigint | YES |  | NULL |  |
| 简称 | text | YES |  | NULL |  |
| 上市日期 | datetime | YES |  | NULL |  |
| 发行方式 | text | YES |  | NULL |  |
| 昨日收盘价 | text | YES |  | NULL |  |
| 今日开盘价 | text | YES |  | NULL |  |
| 网上申购日期 | datetime | YES |  | NULL |  |
| 发行量_万股_ | text | YES |  | NULL |  |
| 更新日期 | datetime | YES |  | NULL |  |

## 📊 表：著作权

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 作品名称 | text | YES |  | NULL |  |
| 登记号 | text | YES |  | NULL |  |
| 类别 | text | YES |  | NULL |  |
| 创作完成日期 | datetime | YES |  | NULL |  |
| 登记日期 | datetime | YES |  | NULL |  |
| 首次发布日期 | datetime | YES |  | NULL |  |
| 作者 | text | YES |  | NULL |  |
| 著作权人_所属公司 | text | YES |  | NULL |  |

## 📊 表：融资信息

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 融资时间 | datetime | YES |  | NULL |  |
| 融资轮次 | text | YES |  | NULL |  |
| 投资方 | text | YES |  | NULL |  |
| 融资额 | text | YES |  | NULL |  |

## 📊 表：行业代码表

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| industry_code | text | YES |  | NULL |  |
| 门类代码 | text | YES |  | NULL |  |
| 门类名称 | text | YES |  | NULL |  |
| 大类行业代码 | text | YES |  | NULL |  |
| 大类代码 | bigint | YES |  | NULL |  |
| 大类名称 | text | YES |  | NULL |  |
| 中类行业代码 | text | YES |  | NULL |  |
| 中类代码 | bigint | YES |  | NULL |  |
| 中类名称 | text | YES |  | NULL |  |
| 小类代码 | bigint | YES |  | NULL |  |
| 小类名称 | text | YES |  | NULL |  |

## 📊 表：行政区划代码表

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| type_code | bigint | YES |  | NULL |  |
| admin_name | text | YES |  | NULL |  |
| short_name | text | YES |  | NULL |  |
| 行政区划等级 | bigint | YES |  | NULL |  |

## 📊 表：行政处罚

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 行政处罚决定书文号 | text | YES |  | NULL |  |
| 违法行为类型 | text | YES |  | NULL |  |
| 处罚内容 | text | YES |  | NULL |  |
| 处罚金额 | text | YES |  | NULL |  |
| 作出行政处罚决定机关名称 | text | YES |  | NULL |  |
| 作出行政处罚决定日期 | datetime | YES |  | NULL |  |
| 处罚依据 | text | YES |  | NULL |  |
| 是否历史数据 | text | YES |  | NULL |  |

## 📊 表：行政处罚_历史_

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 行政处罚决定书文号 | text | YES |  | NULL |  |
| 违法行为类型 | text | YES |  | NULL |  |
| 处罚内容 | text | YES |  | NULL |  |
| 处罚金额 | text | YES |  | NULL |  |
| 作出行政处罚决定机关名称 | text | YES |  | NULL |  |
| 作出行政处罚决定日期 | datetime | YES |  | NULL |  |
| 处罚依据 | text | YES |  | NULL |  |
| 是否历史数据 | text | YES |  | NULL |  |

## 📊 表：行政许可

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 许可文件编号 | text | YES |  | NULL |  |
| 许可文件名称 | text | YES |  | NULL |  |
| 有效期自 | text | YES |  | NULL |  |
| 有效期至 | text | YES |  | NULL |  |
| 许可机关 | text | YES |  | NULL |  |
| 登记状态 | text | YES |  | NULL |  |
| 内容 | text | YES |  | NULL |  |

## 📊 表：行政许可_历史_

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 许可文件编号 | text | YES |  | NULL |  |
| 许可文件名称 | text | YES |  | NULL |  |
| 有效期自 | text | YES |  | NULL |  |
| 有效期至 | text | YES |  | NULL |  |
| 许可机关 | text | YES |  | NULL |  |
| 登记状态 | text | YES |  | NULL |  |
| 内容 | text | YES |  | NULL |  |

## 📊 表：被执行人

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 立案日期 | datetime | YES |  | NULL |  |
| 执行标的 | text | YES |  | NULL |  |
| 执行法院 | text | YES |  | NULL |  |
| 案件状态 | text | YES |  | NULL |  |
| 案号 | text | YES |  | NULL |  |
| 是否历史记录 | text | YES |  | NULL |  |

## 📊 表：被执行人_历史_

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 立案日期 | datetime | YES |  | NULL |  |
| 执行标的 | text | YES |  | NULL |  |
| 执行法院 | text | YES |  | NULL |  |
| 案件状态 | text | YES |  | NULL |  |
| 案号 | text | YES |  | NULL |  |
| 是否历史记录 | text | YES |  | NULL |  |

## 📊 表：裁判文书

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 当事人 | text | YES |  | NULL |  |
| 身份_攻方_ | text | YES |  | NULL |  |
| 身份_守方_ | text | YES |  | NULL |  |
| 身份_其他_ | text | YES |  | NULL |  |
| 冻结信息 | text | YES |  | NULL |  |
| 案由 | text | YES |  | NULL |  |
| 案号 | text | YES |  | NULL |  |
| 审判流程 | text | YES |  | NULL |  |
| 案件类型 | text | YES |  | NULL |  |
| 文书类型 | text | YES |  | NULL |  |
| 涉诉金额 | double | YES |  | NULL |  |
| 发布日期 | datetime | YES |  | NULL |  |
| 判决时间 | datetime | YES |  | NULL |  |
| 判决结果 | mediumtext | YES |  | NULL |  |

## 📊 表：询价评估_评估结果

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 标的物 | text | YES |  | NULL |  |
| 标的物所有人 | text | YES |  | NULL |  |
| 询价结果_元_ | text | YES |  | NULL |  |
| 案号 | text | YES |  | NULL |  |
| 法院名称 | text | YES |  | NULL |  |
| 发布日期 | datetime | YES |  | NULL |  |

## 📊 表：询价评估_选定评估机构

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 标的物 | text | YES |  | NULL |  |
| 财产类型 | text | YES |  | NULL |  |
| 当事人 | text | YES |  | NULL |  |
| 案号 | text | YES |  | NULL |  |
| 法院名称 | text | YES |  | NULL |  |
| 选定评估机构 | text | YES |  | NULL |  |
| 摇号日期 | datetime | YES |  | NULL |  |

## 📊 表：财务信息

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 营业收入 | text | YES |  | NULL |  |
| 总资产 | text | YES |  | NULL |  |
| 归母净利润 | text | YES |  | NULL |  |
| 报告期 | text | YES |  | NULL |  |

## 📊 表：质权人_历史_

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 登记日期 | datetime | YES |  | NULL |  |
| 登记编号 | text | YES |  | NULL |  |
| 出质人 | text | YES |  | NULL |  |
| 质权人 | text | YES |  | NULL |  |
| 状态 | text | YES |  | NULL |  |

## 📊 表：资质认证

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 证书名称 | text | YES |  | NULL |  |
| 证书类型 | text | YES |  | NULL |  |
| 证书编号 | text | YES |  | NULL |  |
| 发证日期 | datetime | YES |  | NULL |  |
| 截止日期 | datetime | YES |  | NULL |  |
| 状态 | text | YES |  | NULL |  |

## 📊 表：资质认证_历史_

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 证书名称 | text | YES |  | NULL |  |
| 证书类型 | text | YES |  | NULL |  |
| 证书编号 | text | YES |  | NULL |  |
| 发证日期 | datetime | YES |  | NULL |  |
| 截止日期 | datetime | YES |  | NULL |  |
| 状态 | text | YES |  | NULL |  |

## 📊 表：软件著作权

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 软件名称 | text | YES |  | NULL |  |
| 登记号 | text | YES |  | NULL |  |
| 版本号 | text | YES |  | NULL |  |
| 分类号 | text | YES |  | NULL |  |
| 登记批准日期 | datetime | YES |  | NULL |  |
| 软件简称 | text | YES |  | NULL |  |

## 📊 表：进出口信用

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 海关编码 | text | YES |  | NULL |  |
| 注册日期 | datetime | YES |  | NULL |  |
| 注册海关 | text | YES |  | NULL |  |
| 经营类别 | text | YES |  | NULL |  |
| 行政区划 | text | YES |  | NULL |  |
| 经济区划 | text | YES |  | NULL |  |
| 海关信用等级 | text | YES |  | NULL |  |
| 特殊贸易区域 | text | YES |  | NULL |  |
| 行业种类 | text | YES |  | NULL |  |
| 报关有效期 | text | YES |  | NULL |  |
| 海关注销标志 | text | YES |  | NULL |  |
| 年报情况 | text | YES |  | NULL |  |
| 跨境贸易电子商务类型 | text | YES |  | NULL |  |

## 📊 表：违法违规建设

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 项目名称 | text | YES |  | NULL |  |
| 生产状况 | text | YES |  | NULL |  |
| 开工建设时间 | datetime | YES |  | NULL |  |
| 存在问题 | text | YES |  | NULL |  |
| 清理措施 | text | YES |  | NULL |  |
| 拟完成时限 | text | YES |  | NULL |  |
| 责任单位 | text | YES |  | NULL |  |
| 完成情况 | text | YES |  | NULL |  |

## 📊 表：送达公告

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 案号 | text | YES |  | NULL |  |
| 案由 | text | YES |  | NULL |  |
| 当事人 | text | YES |  | NULL |  |
| 法院 | text | YES |  | NULL |  |
| 发布日期 | datetime | YES |  | NULL |  |

## 📊 表：重大税收违法

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 案件性质 | text | YES |  | NULL |  |
| 违法事实 | text | YES |  | NULL |  |
| 法律依据及处罚 | text | YES |  | NULL |  |
| 检查机关 | text | YES |  | NULL |  |
| 公示税务机关 | text | YES |  | NULL |  |
| 公布时间 | datetime | YES |  | NULL |  |

## 📊 表：间接持股企业

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 间接持股企业名称 | text | YES |  | NULL |  |
| 间接持股比例 | text | YES |  | NULL |  |
| 统一社会信用代码 | text | YES |  | NULL |  |
| 法定代表人_负责人 | text | YES |  | NULL |  |
| 经营状态 | text | YES |  | NULL |  |
| 省份 | text | YES |  | NULL |  |
| 市 | text | YES |  | NULL |  |
| 区域 | text | YES |  | NULL |  |
| 行业 | text | YES |  | NULL |  |
| 注册资本 | text | YES |  | NULL |  |
| 成立时间 | datetime | YES |  | NULL |  |
| 资本背景 | text | YES |  | NULL |  |
| 企业规模 | text | YES |  | NULL |  |
| 注册地址_全部_ | text | YES |  | NULL |  |
| 最新注册地址 | text | YES |  | NULL |  |
| 最新年报地址 | text | YES |  | NULL |  |
| 企业网址 | text | YES |  | NULL |  |
| 经营范围 | text | YES |  | NULL |  |
| 企业简介 | text | YES |  | NULL |  |
| 是否历史数据 | text | YES |  | NULL |  |

## 📊 表：间接股东

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 间接股东名称 | text | YES |  | NULL |  |
| 间接股东标签 | text | YES |  | NULL |  |
| 股东类型 | text | YES |  | NULL |  |
| 间接持股层级 | bigint | YES |  | NULL |  |
| 间接持股比例 | text | YES |  | NULL |  |
| 持股路径 | mediumtext | YES |  | NULL |  |

## 📊 表：限制高消费

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 限制令发布日期 | datetime | YES |  | NULL |  |
| 限制消费类型 | text | YES |  | NULL |  |
| 立案时间 | datetime | YES |  | NULL |  |
| 案号 | text | YES |  | NULL |  |
| 是否历史记录 | text | YES |  | NULL |  |

## 📊 表：限制高消费_历史_

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 限制令发布日期 | datetime | YES |  | NULL |  |
| 限制消费类型 | text | YES |  | NULL |  |
| 立案时间 | datetime | YES |  | NULL |  |
| 案号 | text | YES |  | NULL |  |
| 是否历史记录 | text | YES |  | NULL |  |

## 📊 表：非正常户

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 认定日期 | datetime | YES |  | NULL |  |
| 公告日期 | datetime | YES |  | NULL |  |
| 纳税人识别号 | text | YES |  | NULL |  |
| 欠税税种 | text | YES |  | NULL |  |
| 欠税金额_元_ | text | YES |  | NULL |  |
| 认定单位 | text | YES |  | NULL |  |
| 认定单位地址 | text | YES |  | NULL |  |
| 认定原因 | text | YES |  | NULL |  |
| 是否历史 | text | YES |  | NULL |  |

## 📊 表：黑名单

**注释**: 无

| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |
|--------|------|------|-----|--------|------|
| import_id | bigint | NO | PRI | NULL |  |
| 批量上传公司名称 | text | YES |  | NULL |  |
| 系统匹配公司名称 | text | YES |  | NULL |  |
| 黑名单类型 | text | YES |  | NULL |  |
| 黑名单名称 | text | YES |  | NULL |  |
| 黑名单认定依据 | text | YES |  | NULL |  |
| 认定部门 | text | YES |  | NULL |  |
| 认定等级 | text | YES |  | NULL |  |
| 列入日期 | datetime | YES |  | NULL |  |
| 内容 | text | YES |  | NULL |  |
| 处罚结果 | text | YES |  | NULL |  |

