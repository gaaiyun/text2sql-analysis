"""
Vanna AI 训练数据生成器
使用 Claude Opus 4.6 生成高质量的 DDL 和示例查询

使用方法:
    python scripts/generate_vanna_training.py

注意：API Key 从环境变量或 config.json 加载
"""

import json
import sys
from pathlib import Path
import httpx

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.config import get_kiro_config

# 配置（从环境变量加载）
KIRO_CONFIG = get_kiro_config()
KIRO_BASE_URL = KIRO_CONFIG['base_url']
KIRO_API_KEY = KIRO_CONFIG['api_key']
MODEL = KIRO_CONFIG['model']

# Schema 文件 (使用绝对路径)
SCRIPT_DIR = Path(__file__).parent
SCHEMA_PATH_1 = SCRIPT_DIR.parent / "schema_gaaiyun.md"
SCHEMA_PATH_2 = SCRIPT_DIR.parent / "schema_gaaiyun_2.md"

def load_schema(schema_path):
    """加载 Schema 文件"""
    if not schema_path.exists():
        print(f"[ERROR] Schema 文件不存在：{schema_path}")
        return None

    with open(schema_path, 'r', encoding='utf-8') as f:
        return f.read()

def generate_training_data(schema, scenario_name):
    """使用 Claude 生成训练数据"""
    print(f"\n[INFO] 正在为 {scenario_name} 生成训练数据...")

    prompt = f"""你是 Text2SQL 专家。基于以下数据库 Schema，生成 Vanna AI 训练数据。

Schema:
{schema[:5000]}  # 限制长度

请生成:
1. 5 个典型的 DDL 语句（CREATE TABLE）
2. 10 个示例问题和对应的 SQL 查询
3. 3 个文档说明（表关系、业务规则等）

格式要求:
- DDL: 完整的 CREATE TABLE 语句
- 问题：自然语言问题
- SQL: 可执行的 SQL 查询
- 文档：简洁的业务说明

输出格式 (JSON):
{{
  "ddls": ["CREATE TABLE ...", ...],
  "examples": [
    {{"question": "问题 1", "sql": "SELECT ..."}},
    ...
  ],
  "documents": ["文档 1", "文档 2", ...]
}}
"""

    try:
        response = httpx.post(
            f"{KIRO_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {KIRO_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": "你是 Text2SQL 专家，擅长生成训练数据。"},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 4096,
                "temperature": 0.7
            },
            timeout=120
        )

        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']

            # 尝试解析 JSON
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                training_data = json.loads(json_match.group())
                print(f"[OK] 生成成功!")
                print(f"  DDL: {len(training_data.get('ddls', []))} 个")
                print(f"  示例：{len(training_data.get('examples', []))} 个")
                print(f"  文档：{len(training_data.get('documents', []))} 个")
                return training_data
            else:
                print(f"[WARN] 无法解析 JSON，返回原始内容")
                return {"raw": content}
        else:
            print(f"[ERROR] API 调用失败：{response.status_code}")
            print(f"  {response.text[:200]}")
            return None

    except Exception as e:
        print(f"[ERROR] 生成失败：{e}")
        return None

def save_training_data(data, output_path):
    """保存训练数据"""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"[OK] 训练数据已保存到：{output_path}")

def main():
    """主函数"""
    print("=" * 60)
    print("Vanna AI 训练数据生成器")
    print("=" * 60)
    print(f"使用模型：{MODEL}")
    print(f"API: {KIRO_BASE_URL}")
    print()

    # 场景 1-3
    schema1 = load_schema(SCHEMA_PATH_1)
    if schema1:
        data1 = generate_training_data(schema1, "场景 1-3 (Gaaiyun)")
        if data1:
            save_training_data(data1, Path("vanna_training_gaaiyun.json"))

    print()

    # 场景 4-5
    schema2 = load_schema(SCHEMA_PATH_2)
    if schema2:
        # 只取前 10000 字符
        data2 = generate_training_data(schema2[:10000], "场景 4-5 (gaaiyun_2)")
        if data2:
            save_training_data(data2, Path("vanna_training_gaaiyun_2.json"))

    print("\n" + "=" * 60)
    print("生成完成！")
    print("=" * 60)
    print("\n下一步:")
    print("  1. 检查生成的训练数据")
    print("  2. 运行：python scripts/train_vanna.py")
    print("  3. 启动 API: python api/vanna_server.py")

if __name__ == "__main__":
    main()
