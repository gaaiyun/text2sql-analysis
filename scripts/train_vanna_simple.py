"""
Vanna AI 训练脚本（简化版）
直接使用 Schema 文件进行训练

使用方法:
    python scripts/train_vanna_simple.py

注意：数据库配置从环境变量或 config.json 加载
"""

import sys
import pymysql
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.config import get_database_config

# 尝试导入 vanna
try:
    import vanna as vn
    print("[OK] Vanna 已导入")
except ImportError:
    print("[ERROR] Vanna 未安装，请先安装：pip install vanna")
    sys.exit(1)

# 配置（从环境变量加载）
DB_CONFIG = get_database_config('scenario_1_3')

def extract_ddl():
    """从数据库提取 DDL"""
    print("\n[1/3] 提取 DDL...")

    if not DB_CONFIG.get('host') or not DB_CONFIG.get('database'):
        print("  [ERROR] 数据库配置无效，请检查 .env 或 config.json")
        return []

    try:
        conn = pymysql.connect(**DB_CONFIG)
        cur = conn.cursor()

        # 获取所有表
        cur.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = %s
        """, (DB_CONFIG['database'],))
        tables = [row[0] for row in cur.fetchall()]
        print(f"  找到 {len(tables)} 张表")

        # 提取每张表的 DDL
        ddls = []
        for table in tables[:5]:  # 只取前 5 张表
            cur.execute(f"SHOW CREATE TABLE `{table}`")
            result = cur.fetchone()
            if result:
                ddls.append(result[1])
                print(f "  ✅ {table}")

        conn.close()
        return ddls

    except Exception as e:
        print(f"  [ERROR] {e}")
        return []

def train_with_ddl(ddls):
    """使用 DDL 训练 Vanna"""
    print("\n[2/3] 训练 Vanna...")

    if not ddls:
        print("  [WARN] 没有 DDL 可训练")
        return

    for i, ddl in enumerate(ddls, 1):
        try:
            # 注意：这里需要实际的 Vanna API 配置
            # status = vn.train(ddl=ddl)
            print(f"  [{i}/{len(ddls)}] 准备训练：{ddl[:50]}...")
            # print(f"  ✅ 训练成功：{status}")
        except Exception as e:
            print(f"  [ERROR] {e}")

def generate_sample_questions():
    """生成示例问题"""
    print("\n[3/3] 示例问题（供参考）...")

    questions = [
        "查询近 3 年企业融资趋势",
        "分析投资事件最多的行业",
        "统计各行业的融资轮次分布",
        "查询注册资本超过 1000 万的企业",
        "查询有知识产权的企业列表"
    ]

    for i, q in enumerate(questions, 1):
        print(f"  {i}. {q}")

def main():
    """主函数"""
    print("=" * 60)
    print("Vanna AI 训练脚本（简化版）")
    print("=" * 60)
    print()

    # 检查 Vanna 配置
    print("[INFO] 检查 Vanna 配置...")
    # print(f"  API Key: {vn.api_key[:20]}..." if vn.api_key else "  [WARN] 未设置 API Key")
    # print(f"  Org: {vn.org}" if vn.org else "  [WARN] 未设置 Org")
    print("  [INFO] 需要配置 Vanna API Key 和 Org")
    print("  请访问 https://vanna.ai/ 获取")
    print()

    # 提取 DDL
    ddls = extract_ddl()

    # 训练
    train_with_ddl(ddls)

    # 示例问题
    generate_sample_questions()

    print("\n" + "=" * 60)
    print("训练完成！")
    print("=" * 60)
    print("\n下一步:")
    print("  1. 获取 Vanna API Key: https://vanna.ai/")
    print("  2. 配置 config.json 中的 vanna 部分")
    print("  3. 重新运行此脚本进行实际训练")
    print("  4. 启动 API: python api/vanna_server.py")

if __name__ == "__main__":
    main()
