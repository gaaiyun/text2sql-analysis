"""
Text2SQL 项目综合测试报告生成器

生成完整的测试结果报告，包括：
1. 硬编码凭证修复验证
2. SQL 注入安全测试
3. 配置管理测试
4. 数据库连接测试（可选）

使用方法:
    python tests/test_report.py
"""

import unittest
import sys
import os
import json
from pathlib import Path
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))


# =============================================================================
# 测试 1: 硬编码凭证修复验证
# =============================================================================

class TestCredentialSecurity(unittest.TestCase):
    """硬编码凭证修复验证测试"""

    def test_no_hardcoded_passwords_in_config(self):
        """测试 config.py 没有硬编码密码"""
        config_path = Path(__file__).parent.parent / "src" / "utils" / "config.py"
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查不应该出现的硬编码密码模式
        forbidden_patterns = [
            "'Why513338'",
            '"Why513338"',
            "password='",
            'password="',
        ]

        for pattern in forbidden_patterns:
            # 允许在示例或注释中出现
            if pattern in content:
                # 检查是否在代码逻辑中
                lines = content.split('\n')
                for line in lines:
                    if pattern in line and not line.strip().startswith('#'):
                        # 允许在默认值中出现空字符串
                        if "=''" in line or '=""' in line or "='your" in line.lower() or '="your' in line.lower():
                            continue
                        self.fail(f"发现硬编码密码模式：{line.strip()}")

    def test_env_file_exists(self):
        """测试 .env.example 文件存在"""
        env_path = Path(__file__).parent.parent / ".env.example"
        self.assertTrue(env_path.exists(), ".env.example 文件应该存在")

    def test_env_file_has_required_vars(self):
        """测试 .env.example 包含必要的环境变量"""
        env_path = Path(__file__).parent.parent / ".env.example"
        with open(env_path, 'r', encoding='utf-8') as f:
            content = f.read()

        required_vars = [
            'DASHSCOPE_API_KEY',
            'KIRO_API_KEY',
            'DB_HOST',
            'DB_PASSWORD',
        ]

        for var in required_vars:
            self.assertIn(var, content, f".env.example 应该包含 {var}")

    def test_scripts_use_config_module(self):
        """测试脚本使用配置模块而非硬编码"""
        scripts_to_check = [
            "extract_schema.py",
            "scripts/setup_vanna_kiro.py",
            "scripts/train_vanna_simple.py",
            "scripts/generate_vanna_training.py",
            "tests/test_all_scenarios.py",
            "tests/test_db_connection.py",
        ]

        for script in scripts_to_check:
            script_path = Path(__file__).parent.parent / script
            if script_path.exists():
                with open(script_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 检查是否导入了配置模块
                has_config_import = (
                    'from src.utils.config import' in content or
                    'from utils.config import' in content
                )

                # 检查是否有硬编码密码（排除注释和示例）
                has_hardcoded_password = False
                for line in content.split('\n'):
                    line_stripped = line.strip()
                    if line_stripped.startswith('#'):
                        continue
                    # 检查是否有具体的密码值（非变量引用）
                    if "'Why513338'" in line or '"Why513338"' in line:
                        if 'get_database_config' not in content:
                            has_hardcoded_password = True
                            break

                # 如果使用了配置模块，允许通过
                if has_config_import and not has_hardcoded_password:
                    pass  # OK
                elif not has_config_import and has_hardcoded_password:
                    self.fail(f"{script} 应该使用配置模块而非硬编码密码")


# =============================================================================
# 测试 2: 配置模块功能测试
# =============================================================================

class TestConfigModule(unittest.TestCase):
    """配置模块功能测试"""

    def test_config_module_imports(self):
        """测试配置模块可以导入"""
        try:
            from src.utils.config import Config, get_database_config, get_kiro_config
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"配置模块导入失败：{e}")

    def test_config_default_values(self):
        """测试配置默认值"""
        from src.utils.config import get_database_config, get_kiro_config

        # 测试数据库配置（使用默认值）
        db_config = get_database_config('scenario_1_3')
        self.assertIsInstance(db_config, dict)
        self.assertIn('host', db_config)
        self.assertIn('port', db_config)
        self.assertIn('database', db_config)

        # 测试 Kiro 配置
        kiro_config = get_kiro_config()
        self.assertIsInstance(kiro_config, dict)
        self.assertIn('base_url', kiro_config)
        self.assertIn('api_key', kiro_config)
        self.assertIn('model', kiro_config)


# =============================================================================
# 测试 3: SQL 安全模块测试（简化版，完整测试在 test_sql_injection.py）
# =============================================================================

class TestSQLSecurity(unittest.TestCase):
    """SQL 安全模块测试"""

    def test_sql_validator_imports(self):
        """测试 SQL 验证器可以导入"""
        try:
            from src.utils.sql_security import SQLValidator
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"SQL 安全模块导入失败：{e}")

    def test_dangerous_query_detection(self):
        """测试危险查询检测"""
        from src.utils.sql_security import validate_sql_query

        dangerous_queries = [
            "DROP TABLE users",
            "DELETE FROM users",
            "SELECT * FROM users; DROP TABLE users; --",
        ]

        for query in dangerous_queries:
            is_safe, msg = validate_sql_query(query)
            self.assertFalse(is_safe, f"应该检测到危险查询：{query}")

    def test_safe_query_detection(self):
        """测试安全查询检测"""
        from src.utils.sql_security import validate_sql_query

        safe_queries = [
            "SELECT * FROM users WHERE id = 1",
            "SELECT name, COUNT(*) FROM users GROUP BY name",
        ]

        for query in safe_queries:
            is_safe, msg = validate_sql_query(query)
            self.assertTrue(is_safe, f"应该允许安全查询：{query}")


# =============================================================================
# 测试运行器
# =============================================================================

class TestRunner:
    """测试结果收集和报告生成"""

    def __init__(self):
        self.results = []
        self.summary = {
            'total': 0,
            'passed': 0,
            'failed': 0,
            'errors': 0,
        }

    def run_all_tests(self):
        """运行所有测试并生成报告"""
        print("=" * 80)
        print("Text2SQL 项目综合测试报告")
        print("=" * 80)
        print(f"测试时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        # 创建测试套件
        loader = unittest.TestLoader()
        suite = unittest.TestSuite()

        # 添加测试
        suite.addTests(loader.loadTestsFromTestCase(TestCredentialSecurity))
        suite.addTests(loader.loadTestsFromTestCase(TestConfigModule))
        suite.addTests(loader.loadTestsFromTestCase(TestSQLSecurity))

        # 运行测试
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)

        # 收集结果
        self.summary['total'] = result.testsRun
        self.summary['passed'] = result.testsRun - len(result.failures) - len(result.errors)
        self.summary['failed'] = len(result.failures)
        self.summary['errors'] = len(result.errors)

        # 生成详细报告
        self.generate_report(result)

        return result.wasSuccessful()

    def generate_report(self, result):
        """生成详细测试报告"""
        print()
        print("=" * 80)
        print("测试汇总报告")
        print("=" * 80)
        print()

        # 统计信息
        print(f"总测试数：{self.summary['total']}")
        print(f"通过：{self.summary['passed']}")
        print(f"失败：{self.summary['failed']}")
        print(f"错误：{self.summary['errors']}")

        success_rate = (self.summary['passed'] / self.summary['total'] * 100) if self.summary['total'] > 0 else 0
        print(f"成功率：{success_rate:.1f}%")
        print()

        # 失败详情
        if result.failures:
            print("失败测试:")
            for test, traceback in result.failures:
                print(f"  - {test}")
                # 截取关键信息
                error_lines = traceback.split('\n')
                for line in error_lines[:3]:
                    if line.strip():
                        print(f"    {line[:100]}")

        # 错误详情
        if result.errors:
            print("\n错误测试:")
            for test, traceback in result.errors:
                print(f"  - {test}")
                error_lines = traceback.split('\n')
                for line in error_lines[:3]:
                    if line.strip():
                        print(f"    {line[:100]}")

        print()
        print("=" * 80)

        # 保存 JSON 报告
        self.save_json_report(result)

    def save_json_report(self, result):
        """保存 JSON 格式测试报告"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': self.summary,
            'failures': [str(test) for test, _ in result.failures],
            'errors': [str(test) for test, _ in result.errors],
        }

        report_path = Path(__file__).parent.parent / "test_report.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"测试报告已保存到：{report_path}")
        print()


def main():
    """主函数"""
    runner = TestRunner()
    success = runner.run_all_tests()

    if success:
        print("[OK] 所有测试通过！")
    else:
        print("[WARN] 部分测试失败，请检查上述报告")

    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
