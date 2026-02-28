"""
Vanna AI 训练脚本
为5个场景训练Vanna模型，包含Question-SQL配对

使用方法:
    python scripts/train_vanna.py
"""

import json
import pymysql
from pathlib import Path
import vanna as vn
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CONFIG_PATH = Path(__file__).parent.parent / "config.json"


def load_config():
    """加载配置"""
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def init_vanna(config, database_key):
    """初始化Vanna"""
    vanna_config = config.get('vanna', {})
    db_config = config.get('database', {}).get(database_key, {})
    
    vn.api_key = vanna_config.get('api_key', '')
    vn.org = vanna_config.get('org', 'gaaiyun')
    
    vn.connect_to_mysql(
        host=db_config.get('host'),
        database=db_config.get('database'),
        user=db_config.get('user'),
        password=db_config.get('password'),
        port=db_config.get('port', 3306)
    )
    logger.info(f"Vanna初始化成功: {database_key}")


# 场景1-3训练数据（Gaaiyun数据库）
SCENARIO_1_3_TRAINING = [
    # 场景1: 数据洞察 - 融资趋势
    {
        "question": "分析2023-2024年融资趋势",
        "sql": """SELECT 
            YEAR(round_date) as 年份,
            COUNT(*) as 融资次数,
            SUM(amount) as 总金额,
            AVG(amount) as 平均金额,
            MAX(amount) as 最大金额
        FROM 融资数据
        WHERE round_date >= '2023-01-01' AND round_date < '2025-01-01'
        GROUP BY YEAR(round_date)
        ORDER BY 年份"""
    },
    {
        "question": "查询近3年各行业融资情况",
        "sql": """SELECT 
            industry as 行业,
            COUNT(*) as 融资次数,
            SUM(amount) as 总金额
        FROM 融资数据
        WHERE round_date >= DATE_SUB(CURDATE(), INTERVAL 3 YEAR)
        GROUP BY industry
        ORDER BY 总金额 DESC
        LIMIT 10"""
    },
    {
        "question": "统计各融资轮次分布",
        "sql": """SELECT 
            round_name as 融资轮次,
            COUNT(*) as 数量,
            AVG(amount) as 平均金额
        FROM 融资数据
        WHERE round_date >= DATE_SUB(CURDATE(), INTERVAL 3 YEAR)
        GROUP BY round_name
        ORDER BY 数量 DESC"""
    },
    {
        "question": "查询注册资本超过1000万的企业",
        "sql": """SELECT 
            company_name as 企业名称,
            registered_capital as 注册资本,
            industry as 行业,
            established_date as 成立日期
        FROM 企业基本信息
        WHERE registered_capital >= 10000000
        ORDER BY registered_capital DESC
        LIMIT 100"""
    },
    {
        "question": "分析投资事件的地域分布",
        "sql": """SELECT 
            province as 省份,
            city as 城市,
            COUNT(*) as 投资次数,
            SUM(amount) as 总金额
        FROM 投资事件
        WHERE event_date >= DATE_SUB(CURDATE(), INTERVAL 3 YEAR)
        GROUP BY province, city
        ORDER BY 投资次数 DESC
        LIMIT 20"""
    },
    # 场景2: 地区产业分析
    {
        "question": "分析北京市企业行业分布",
        "sql": """SELECT 
            industry as 行业,
            COUNT(*) as 企业数量,
            AVG(registered_capital) as 平均注册资本
        FROM 企业基本信息
        WHERE province = '北京市' OR city = '北京市'
        GROUP BY industry
        ORDER BY 企业数量 DESC
        LIMIT 10"""
    },
    {
        "question": "查询上海市近3年新注册企业趋势",
        "sql": """SELECT 
            YEAR(established_date) as 年份,
            COUNT(*) as 新注册企业数,
            AVG(registered_capital) as 平均注册资本
        FROM 企业基本信息
        WHERE (province = '上海市' OR city = '上海市')
            AND established_date >= DATE_SUB(CURDATE(), INTERVAL 3 YEAR)
        GROUP BY YEAR(established_date)
        ORDER BY 年份"""
    },
    {
        "question": "统计深圳市获得投资的企业",
        "sql": """SELECT 
            e.company_name as 企业名称,
            e.industry as 行业,
            COUNT(i.id) as 投资次数,
            SUM(i.amount) as 总投资金额
        FROM 企业基本信息 e
        JOIN 投资事件 i ON e.id = i.company_id COLLATE utf8mb4_unicode_ci
        WHERE (e.province = '广东省' AND e.city = '深圳市')
            AND i.event_date >= DATE_SUB(CURDATE(), INTERVAL 3 YEAR)
        GROUP BY e.company_name, e.industry
        ORDER BY 总投资金额 DESC
        LIMIT 20"""
    },
    # 场景3: 行业分析
    {
        "question": "分析人工智能行业企业数量增长",
        "sql": """SELECT 
            YEAR(established_date) as 年份,
            COUNT(*) as 新增企业数
        FROM 企业基本信息
        WHERE industry LIKE '%人工智能%' OR industry LIKE '%AI%'
        GROUP BY YEAR(established_date)
        ORDER BY 年份 DESC
        LIMIT 10"""
    },
    {
        "question": "查询新能源汽车行业龙头企业",
        "sql": """SELECT 
            company_name as 企业名称,
            registered_capital as 注册资本,
            established_date as 成立日期,
            province as 省份,
            city as 城市
        FROM 企业基本信息
        WHERE industry LIKE '%新能源%' AND industry LIKE '%汽车%'
        ORDER BY registered_capital DESC
        LIMIT 10"""
    },
    {
        "question": "统计生物医药行业融资情况",
        "sql": """SELECT 
            YEAR(round_date) as 年份,
            COUNT(*) as 融资次数,
            SUM(amount) as 总金额,
            AVG(amount) as 平均金额
        FROM 融资数据
        WHERE industry LIKE '%生物%' OR industry LIKE '%医药%' OR industry LIKE '%医疗%'
        GROUP BY YEAR(round_date)
        ORDER BY 年份 DESC"""
    }
]

# 场景4-5训练数据（gaaiyun_2数据库）
SCENARIO_4_5_TRAINING = [
    # 场景4: 招商清单
    {
        "question": "查询企业的基本信息和知识产权",
        "sql": """SELECT 
            e.企业名称,
            e.注册资本,
            e.成立日期,
            e.企业状态,
            COUNT(DISTINCT p.专利号) as 专利数量,
            COUNT(DISTINCT CASE WHEN p.专利类型 = '发明专利' THEN p.专利号 END) as 发明专利数
        FROM 企业信息 e
        LEFT JOIN 知识产权 p ON e.eid = p.eid COLLATE utf8mb4_unicode_ci
        WHERE e.企业名称 IN ('企业A', '企业B', '企业C')
        GROUP BY e.企业名称, e.注册资本, e.成立日期, e.企业状态"""
    },
    {
        "question": "查询企业的诉讼情况",
        "sql": """SELECT 
            e.企业名称,
            COUNT(l.id) as 诉讼次数,
            SUM(CASE WHEN l.身份 = '原告' THEN 1 ELSE 0 END) as 作为原告,
            SUM(CASE WHEN l.身份 = '被告' THEN 1 ELSE 0 END) as 作为被告
        FROM 企业信息 e
        LEFT JOIN 诉讼信息 l ON e.eid = l.eid COLLATE utf8mb4_unicode_ci
        WHERE e.企业名称 IN ('企业A', '企业B')
        GROUP BY e.企业名称"""
    },
    {
        "question": "查询企业的招投标记录",
        "sql": """SELECT 
            e.企业名称,
            COUNT(b.id) as 中标次数,
            SUM(b.中标金额) as 总中标金额,
            AVG(b.中标金额) as 平均中标金额
        FROM 企业信息 e
        LEFT JOIN 招投标 b ON e.eid = b.eid COLLATE utf8mb4_unicode_ci
        WHERE e.企业名称 IN ('企业A', '企业B', '企业C')
            AND b.中标日期 >= DATE_SUB(CURDATE(), INTERVAL 3 YEAR)
        GROUP BY e.企业名称"""
    },
    {
        "question": "评估企业综合实力",
        "sql": """SELECT 
            e.企业名称,
            e.注册资本,
            TIMESTAMPDIFF(YEAR, e.成立日期, CURDATE()) as 存续年限,
            COUNT(DISTINCT p.专利号) as 专利数量,
            COUNT(DISTINCT l.id) as 诉讼次数,
            COUNT(DISTINCT b.id) as 中标次数
        FROM 企业信息 e
        LEFT JOIN 知识产权 p ON e.eid = p.eid COLLATE utf8mb4_unicode_ci
        LEFT JOIN 诉讼信息 l ON e.eid = l.eid COLLATE utf8mb4_unicode_ci
        LEFT JOIN 招投标 b ON e.eid = b.eid COLLATE utf8mb4_unicode_ci
        WHERE e.企业名称 IN ('企业A', '企业B', '企业C')
        GROUP BY e.企业名称, e.注册资本, e.成立日期
        LIMIT 100"""
    },
    # 场景5: 企业尽调
    {
        "question": "查询企业的完整基本信息",
        "sql": """SELECT 
            企业名称,
            统一社会信用代码,
            注册资本,
            成立日期,
            法定代表人,
            注册地址,
            企业状态,
            经营范围
        FROM 企业信息
        WHERE 企业名称 = '目标企业'
        LIMIT 1"""
    },
    {
        "question": "查询企业的股权结构",
        "sql": """SELECT 
            股东名称,
            持股比例,
            认缴出资额,
            实缴出资额
        FROM 股东信息
        WHERE eid = (SELECT eid FROM 企业信息 WHERE 企业名称 = '目标企业')
        ORDER BY 持股比例 DESC"""
    },
    {
        "question": "查询企业的知识产权详情",
        "sql": """SELECT 
            专利类型,
            专利名称,
            申请日期,
            授权日期,
            专利状态
        FROM 知识产权
        WHERE eid = (SELECT eid FROM 企业信息 WHERE 企业名称 = '目标企业')
        ORDER BY 申请日期 DESC
        LIMIT 50"""
    },
    {
        "question": "查询企业的融资历史",
        "sql": """SELECT 
            融资轮次,
            融资日期,
            融资金额,
            投资方
        FROM 融资信息
        WHERE eid = (SELECT eid FROM 企业信息 WHERE 企业名称 = '目标企业')
        ORDER BY 融资日期 DESC"""
    },
    {
        "question": "查询企业的行政处罚记录",
        "sql": """SELECT 
            处罚日期,
            处罚事由,
            处罚机关,
            处罚结果
        FROM 行政处罚
        WHERE eid = (SELECT eid FROM 企业信息 WHERE 企业名称 = '目标企业')
        ORDER BY 处罚日期 DESC"""
    },
    {
        "question": "查询企业的经营异常记录",
        "sql": """SELECT 
            列入日期,
            列入原因,
            移出日期,
            移出原因
        FROM 经营异常
        WHERE eid = (SELECT eid FROM 企业信息 WHERE 企业名称 = '目标企业')
        ORDER BY 列入日期 DESC"""
    }
]


def train_scenario_1_3(config):
    """训练场景1-3"""
    logger.info("=" * 60)
    logger.info("训练场景1-3（Gaaiyun数据库）")
    logger.info("=" * 60)
    
    init_vanna(config, "scenario_1_3")
    
    success = 0
    failed = 0
    
    for i, item in enumerate(SCENARIO_1_3_TRAINING, 1):
        try:
            status = vn.train(
                question=item["question"],
                sql=item["sql"]
            )
            logger.info(f"[{i}/{len(SCENARIO_1_3_TRAINING)}] ✓ {item['question'][:30]}...")
            success += 1
        except Exception as e:
            logger.error(f"[{i}/{len(SCENARIO_1_3_TRAINING)}] ✗ {item['question'][:30]}... - {e}")
            failed += 1
    
    logger.info(f"\n场景1-3训练完成: 成功 {success}, 失败 {failed}")


def train_scenario_4_5(config):
    """训练场景4-5"""
    logger.info("\n" + "=" * 60)
    logger.info("训练场景4-5（gaaiyun_2数据库）")
    logger.info("=" * 60)
    
    init_vanna(config, "scenario_4_5")
    
    success = 0
    failed = 0
    
    for i, item in enumerate(SCENARIO_4_5_TRAINING, 1):
        try:
            status = vn.train(
                question=item["question"],
                sql=item["sql"]
            )
            logger.info(f"[{i}/{len(SCENARIO_4_5_TRAINING)}] ✓ {item['question'][:30]}...")
            success += 1
        except Exception as e:
            logger.error(f"[{i}/{len(SCENARIO_4_5_TRAINING)}] ✗ {item['question'][:30]}... - {e}")
            failed += 1
    
    logger.info(f"\n场景4-5训练完成: 成功 {success}, 失败 {failed}")


def main():
    """主函数"""
    logger.info("=" * 60)
    logger.info("Vanna AI 训练脚本")
    logger.info("=" * 60)
    
    config = load_config()
    
    # 训练场景1-3
    train_scenario_1_3(config)
    
    # 训练场景4-5
    train_scenario_4_5(config)
    
    logger.info("\n" + "=" * 60)
    logger.info("训练完成！")
    logger.info("=" * 60)
    logger.info("\n下一步:")
    logger.info("  1. 启动Vanna服务器: python api/vanna_server.py")
    logger.info("  2. 测试SQL生成: curl http://localhost:5000/api/v0/generate_sql")
    logger.info("  3. 运行demo: python demo/run_all_scenarios.py")


if __name__ == "__main__":
    main()
