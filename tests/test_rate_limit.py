"""
API 限流测试

测试 API 限流中间件的功能
"""
import unittest
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestRateLimiter(unittest.TestCase):
    """限流器测试"""

    def test_limiter_import(self):
        """测试限流器导入"""
        try:
            from slowapi import Limiter
            from slowapi.util import get_remote_address
            self.assertTrue(True)
        except ImportError:
            self.skipTest("slowapi 未安装")

    def test_limiter_creation(self):
        """测试限流器创建"""
        try:
            from slowapi import Limiter
            from slowapi.util import get_remote_address

            limiter = Limiter(key_func=get_remote_address)
            self.assertIsNotNone(limiter)
        except ImportError:
            self.skipTest("slowapi 未安装")

    def test_rate_limit_parser(self):
        """测试限流规则解析"""
        try:
            from slowapi import Limiter
            from slowapi.util import get_remote_address

            limiter = Limiter(key_func=get_remote_address)

            # 测试限流规则格式
            rules = [
                "100/minute",
                "60/minute",
                "30/minute",
                "20/minute",
                "10/second",
                "1000/hour"
            ]

            for rule in rules:
                # 规则格式检查
                self.assertIn("/", rule)
                parts = rule.split("/")
                self.assertEqual(len(parts), 2)

                count, period = parts
                self.assertTrue(int(count) > 0)
                self.assertIn(period, ["second", "minute", "hour"])

        except ImportError:
            self.skipTest("slowapi 未安装")


class TestRateLimitConfig(unittest.TestCase):
    """限流配置测试"""

    def test_api_rate_limits(self):
        """测试 API 限流配置"""
        # 读取 api_server.py 文件
        api_path = Path(__file__).parent.parent / "api_server.py"

        with open(api_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查限流装饰器是否存在
        rate_limits = {
            "/api/query": "100/minute",
            "/api/query/llm": "100/minute",
            "/api/query/vanna": "100/minute",
            "/api/search": "60/minute",
            "/api/export/excel": "30/minute",
            "/api/export/word": "30/minute",
            "/api/report": "30/minute",
            "/api/train": "20/minute",
            "/api/schema": "60/minute",
        }

        for endpoint, limit in rate_limits.items():
            # 检查端点是否存在
            self.assertIn(f'"{endpoint}"', content, f"端点 {endpoint} 应该存在")

            # 检查限流装饰器是否存在
            self.assertIn(
                f'@limiter.limit("{limit}")',
                content,
                f"端点 {endpoint} 应该有限流 {limit}"
            )

    def test_limiter_initialization(self):
        """测试限流器初始化"""
        api_path = Path(__file__).parent.parent / "api_server.py"

        with open(api_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查限流器初始化
        self.assertIn("from slowapi import Limiter", content)
        self.assertIn("Limiter(key_func=get_remote_address)", content)
        self.assertIn("app.state.limiter = limiter", content)
        self.assertIn("SlowAPIMiddleware", content)

    def test_rate_limit_exception_handler(self):
        """测试限流异常处理器"""
        api_path = Path(__file__).parent.parent / "api_server.py"

        with open(api_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查异常处理器
        self.assertIn("_rate_limit_exceeded_handler", content)
        self.assertIn("app.add_exception_handler(RateLimitExceeded", content)


class TestRateLimitIntegration(unittest.TestCase):
    """限流集成测试"""

    def test_fastapi_app_has_limiter(self):
        """测试 FastAPI 应用有限流器"""
        api_path = Path(__file__).parent.parent / "api_server.py"

        with open(api_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查限流器相关代码
        checks = [
            "limiter = Limiter",
            "app.state.limiter",
            "app.add_middleware(SlowAPIMiddleware)",
            "@limiter.limit",
        ]

        for check in checks:
            self.assertIn(check, content, f"应该包含：{check}")

    def test_request_parameter(self):
        """测试请求参数（限流需要）"""
        api_path = Path(__file__).parent.parent / "api_server.py"

        with open(api_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查端点函数签名包含 request: Request
        # 这是限流器必需的
        self.assertIn("request: Request", content)


# =============================================================================
# 测试运行器
# =============================================================================

def run_tests():
    """运行所有测试"""
    print("=" * 60)
    print("API 限流测试")
    print("=" * 60)

    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # 添加测试
    suite.addTests(loader.loadTestsFromTestCase(TestRateLimiter))
    suite.addTests(loader.loadTestsFromTestCase(TestRateLimitConfig))
    suite.addTests(loader.loadTestsFromTestCase(TestRateLimitIntegration))

    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # 汇总报告
    print()
    print("=" * 60)
    print("测试汇总")
    print("=" * 60)
    print(f"总测试数：{result.testsRun}")
    print(f"成功：{result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败：{len(result.failures)}")
    print(f"错误：{len(result.errors)}")

    success_rate = (result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100 if result.testsRun > 0 else 0
    print(f"成功率：{success_rate:.1f}%")
    print("=" * 60)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
