"""
Vanna AI 配置脚本 - 使用 Kiro OpenAI 兼容 API
无需 Vanna API Key，直接使用 Kiro 反代

使用方法:
    python scripts/setup_vanna_kiro.py

注意：API Key 和数据库密码从环境变量或 config.json 加载
"""

import os
from pathlib import Path
import sys

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.config import get_kiro_config, get_database_config

# Kiro 配置（从环境变量加载）
KIRO_CONFIG = get_kiro_config()
KIRO_BASE_URL = KIRO_CONFIG['base_url']
KIRO_API_KEY = KIRO_CONFIG['api_key']
KIRO_MODEL = KIRO_CONFIG['model']

# 数据库配置（从环境变量加载）
DB_CONFIG = {
    'scenario_1_3': get_database_config('scenario_1_3'),
    'scenario_4_5': get_database_config('scenario_4_5')
}

def check_installation():
    """检查必要的包是否已安装"""
    print("=" * 60)
    print("Vanna AI 配置检查")
    print("=" * 60)
    print()

    required_packages = {
        'vanna': 'Vanna AI 核心',
        'openai': 'OpenAI 兼容 API',
        'fastapi': 'FastAPI 服务',
        'uvicorn': 'ASGI 服务器',
        'pymysql': 'MySQL 驱动'
    }

    missing = []
    for package, desc in required_packages.items():
        try:
            __import__(package)
            print(f"[OK] {package} - {desc}")
        except ImportError:
            print(f"[MISSING] {package} - {desc}")
            missing.append(package)

    if missing:
        print()
        print("[WARN] 缺少必要的包，请安装:")
        print(f"  pip install {' '.join(missing)}")
        print()
        print("或者安装完整依赖:")
        print("  pip install 'vanna[fastapi,openai]' pymysql")
        return False

    print()
    print("[OK] 所有必要的包已安装")
    return True

def create_vanna_config():
    """创建 Vanna 配置文件"""
    print()
    print("=" * 60)
    print("创建 Vanna 配置文件")
    print("=" * 60)
    print()

    config_content = f'''
"""
Vanna AI 配置 - 使用 Kiro OpenAI 兼容 API
基于官方文档：https://vanna.ai/docs/configure/openai/sqlite

注意：API Key 和数据库密码从环境变量或 config.json 加载
"""

import os
from pathlib import Path
import sys

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from src.utils.config import get_kiro_config, get_database_config

# 获取配置
KIRO_CONFIG = get_kiro_config()
DB_CONFIG = {{
    'scenario_1_3': get_database_config('scenario_1_3'),
    'scenario_4_5': get_database_config('scenario_4_5')
}}

from vanna.integrations.openai import OpenAILlmService
from vanna.tools import RunSqlTool
from vanna.integrations.mysql import MysqlRunner
from vanna import Agent
from vanna.core.registry import ToolRegistry
from vanna.servers.fastapi import VannaFastAPIServer

# ============ 1. 配置 LLM（使用 Kiro OpenAI 兼容 API） ============
llm = OpenAILlmService(
    model=KIRO_CONFIG["model"],
    api_base=KIRO_CONFIG["base_url"],
    api_key=KIRO_CONFIG["api_key"]
)

# ============ 2. 配置数据库（场景 1-3: Gaaiyun） ============
db_tool_scenario_1_3 = RunSqlTool(
    sql_runner=MysqlRunner(
        host=DB_CONFIG['scenario_1_3']['host'],
        port=DB_CONFIG['scenario_1_3']['port'],
        user=DB_CONFIG['scenario_1_3']['user'],
        password=DB_CONFIG['scenario_1_3']['password'],
        database=DB_CONFIG['scenario_1_3']['database']
    )
)

# ============ 3. 配置数据库（场景 4-5: gaaiyun_2） ============
db_tool_scenario_4_5 = RunSqlTool(
    sql_runner=MysqlRunner(
        host=DB_CONFIG['scenario_4_5']['host'],
        port=DB_CONFIG['scenario_4_5']['port'],
        user=DB_CONFIG['scenario_4_5']['user'],
        password=DB_CONFIG['scenario_4_5']['password'],
        database=DB_CONFIG['scenario_4_5']['database']
    )
)

# ============ 4. 创建 Agent ============
tools = ToolRegistry()

# 注册数据库工具
tools.register_local_tool(db_tool_scenario_1_3, access_groups=['admin', 'user'])
tools.register_local_tool(db_tool_scenario_4_5, access_groups=['admin', 'user'])

# 创建 Agent
agent = Agent(
    llm_service=llm,
    tool_registry=tools
)

# ============ 5. 运行服务器 ============
if __name__ == "__main__":
    server = VannaFastAPIServer(agent)
    server.run()  # 访问 http://localhost:8000
'''

    config_path = Path("vanna_kiro_config.py")
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(config_content)

    print(f"[OK] 配置文件已创建：{config_path}")
    print()
    return config_path

def create_simple_test():
    """创建简单测试脚本"""
    print()
    print("=" * 60)
    print("创建测试脚本")
    print("=" * 60)
    print()

    test_content = f'''
"""
Vanna AI 简单测试 - 使用 Kiro API
注意：API Key 和数据库密码从环境变量或 config.json 加载
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.config import get_kiro_config, get_database_config

from vanna.integrations.openai import OpenAILlmService
import pymysql

# 获取配置
KIRO_CONFIG = get_kiro_config()
DB_CONFIG = get_database_config('scenario_1_3')

# 配置 Kiro API
llm = OpenAILlmService(
    model=KIRO_CONFIG["model"],
    api_base=KIRO_CONFIG["base_url"],
    api_key=KIRO_CONFIG["api_key"]
)

# 测试数据库连接
print(f"[INFO] 尝试连接数据库：{{DB_CONFIG['database']}} @ {{DB_CONFIG['host']}}")
try:
    conn = pymysql.connect(
        host=DB_CONFIG['host'],
        port=DB_CONFIG['port'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database']
    )
    print("[OK] 数据库连接成功！")

    # 获取表结构
    cur = conn.cursor()
    cur.execute("SHOW TABLES")
    tables = [row[0] for row in cur.fetchall()]
    print(f"[INFO] 数据库包含 {{len(tables)}} 张表")

    # 测试 LLM
    print()
    print("[INFO] 测试 LLM...")
    try:
        response = llm.generate("SELECT * FROM", max_tokens=50)
        print(f"[OK] LLM 响应：{{response[:100]}}...")
    except Exception as e:
        print(f"[ERROR] LLM 测试失败：{{e}}")

    conn.close()
except Exception as e:
    print(f"[ERROR] 数据库连接失败：{{e}}")
    print("[INFO] 请检查 .env 文件中的数据库配置")
'''

    test_path = Path("test_vanna_kiro.py")
    with open(test_path, 'w', encoding='utf-8') as f:
        f.write(test_content)

    print(f"[OK] 测试脚本已创建：{test_path}")
    print()

def main():
    """主函数"""
    print()
    print("[INFO] 基于官方文档配置 Vanna")
    print("   https://vanna.ai/docs/configure/openai/sqlite")
    print()

    # 检查安装
    if not check_installation():
        return

    # 创建配置
    create_vanna_config()

    # 创建测试
    create_simple_test()

    print()
    print("=" * 60)
    print("[OK] 配置完成！")
    print("=" * 60)
    print()
    print("下一步:")
    print("  1. 安装依赖（如果还没安装）:")
    print("     pip install 'vanna[fastapi,openai]' pymysql")
    print()
    print("  2. 配置环境变量（创建 .env 文件）:")
    print("     KIRO_API_KEY=your-api-key")
    print("     DB_HOST=your-db-host")
    print("     DB_NAME=your-db-name")
    print("     DB_USER=your-db-user")
    print("     DB_PASSWORD=your-db-password")
    print()
    print("  3. 测试配置:")
    print("     python test_vanna_kiro.py")
    print()
    print("  4. 启动 Vanna API 服务:")
    print("     python vanna_kiro_config.py")
    print()
    print("  5. 访问 Web 界面:")
    print("     http://localhost:8000")
    print()

if __name__ == "__main__":
    main()
