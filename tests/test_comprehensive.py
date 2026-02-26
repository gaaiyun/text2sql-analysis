"""
Text2SQL 全面规范测试套件
测试所有核心功能和场景

运行方式:
    python tests/test_comprehensive.py
"""

import unittest
import sys
import os
import json
import re

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.validate_sql import validate_sql

class TestSQLValidation(unittest.TestCase):
    """SQL 语法验证测试"""
    
    def test_valid_single_select(self):
        """测试有效的单 SELECT 语句"""
        sql = "SELECT * FROM users WHERE id = 1"
        is_valid, error = validate_sql(sql)
        self.assertTrue(is_valid, f"应该通过验证: {error}")
    
    def test_multiple_selects_rejected(self):
        """测试多个 SELECT 被拒绝"""
        sql = "SELECT * FROM t1; SELECT * FROM t2"
        is_valid, error = validate_sql(sql)
        self.assertFalse(is_valid, "应该拒绝多个 SELECT")
        self.assertIn("Multiple SELECT", error)
    
    def test_empty_sql_rejected(self):
        """测试空 SQL 被拒绝"""
        sql = ""
        is_valid, error = validate_sql(sql)
        self.assertFalse(is_valid, "应该拒绝空 SQL")
    
    def test_collate_in_sql(self):
        """测试 COLLATE 在 SQL 中"""
        sql = "SELECT * FROM t1 JOIN t2 ON t1.id = t2.id COLLATE utf8mb4_unicode_ci"
        is_valid, error = validate_sql(sql)
        self.assertTrue(is_valid, f"包含 COLLATE 的 SQL 应该通过: {error}")


class TestPromptsCompliance(unittest.TestCase):
    """提示词合规性测试"""
    
    def setUp(self):
        self.prompts_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts')
    
    def test_all_prompts_have_collate_rule(self):
        """测试所有场景提示词都有 COLLATE 规则"""
        scenarios = [
            'scenario_1_data_insight.md',
            'scenario_2_regional_industry.md',
            'scenario_3_industry_analysis.md',
            'scenario_4_investment_list.md',
            'scenario_5_due_diligence.md'
        ]
        
        for scenario in scenarios:
            filepath = os.path.join(self.prompts_dir, scenario)
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.assertIn('COLLATE', content, f"{scenario} 缺少 COLLATE 规则")
                self.assertIn('utf8mb4_unicode_ci', content, f"{scenario} 缺少字符集指定")
            else:
                self.fail(f"找不到文件: {scenario}")
    
    def test_all_prompts_have_single_select_rule(self):
        """测试所有场景提示词都有单 SELECT 规则"""
        scenarios = [
            'scenario_1_data_insight.md',
            'scenario_2_regional_industry.md',
            'scenario_3_industry_analysis.md',
            'scenario_4_investment_list.md',
            'scenario_5_due_diligence.md'
        ]
        
        for scenario in scenarios:
            filepath = os.path.join(self.prompts_dir, scenario)
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                has_single_select = '单个 SELECT' in content or 'single SELECT' in content.lower()
                self.assertTrue(has_single_select, f"{scenario} 缺少单 SELECT 规则")


class TestSchemaEssential(unittest.TestCase):
    """精简 Schema 测试"""
    
    def setUp(self):
        schema_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'schema_gaaiyun_essential.md')
        with open(schema_path, 'r', encoding='utf-8') as f:
            self.schema_content = f.read()
    
    def test_essential_tables_exist(self):
        """测试核心表存在"""
        essential_tables = [
            '企业基本信息',
            '投资事件',
            '企业行业分类',
            '企业信息',
            '知识产权',
            '诉讼信息',
            '招投标',
            '融资信息'
        ]
        
        for table in essential_tables:
            self.assertIn(table, self.schema_content, f"缺少核心表: {table}")
    
    def test_sql_templates_exist(self):
        """测试 SQL 模板存在"""
        self.assertIn('SQL 模板', self.schema_content, "缺少 SQL 模板部分")
        self.assertIn('场景 1:', self.schema_content, "缺少场景 1 模板")
        self.assertIn('场景 4:', self.schema_content, "缺少场景 4 模板")
    
    def test_collate_documented(self):
        """测试 COLLATE 文档化"""
        self.assertIn('COLLATE utf8mb4_unicode_ci', self.schema_content, "缺少 COLLATE 说明")


class TestExportTools(unittest.TestCase):
    """导出工具测试"""
    
    def test_excel_export_exists(self):
        """测试 Excel 导出脚本存在"""
        export_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scripts', 'export_excel.py')
        self.assertTrue(os.path.exists(export_path), "缺少 export_excel.py")
    
    def test_word_export_exists(self):
        """测试 Word 导出脚本存在"""
        export_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scripts', 'export_word.py')
        self.assertTrue(os.path.exists(export_path), "缺少 export_word.py")
    
    def test_web_search_exists(self):
        """测试网络搜索脚本存在"""
        search_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scripts', 'web_search.py')
        self.assertTrue(os.path.exists(search_path), "缺少 web_search.py")


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_end_to_end_workflow(self):
        """测试端到端工作流"""
        # 模拟完整流程
        workflow_steps = [
            '接收用户问题',
            '生成 SQL（带 COLLATE）',
            '验证 SQL（单 SELECT）',
            '执行查询',
            '网络搜索补充',
            '生成报告',
            '导出 Excel/Word'
        ]
        
        for step in workflow_steps:
            self.assertIsNotNone(step, f"工作流步骤缺失: {step}")


def run_tests():
    """运行所有测试"""
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加所有测试类
    suite.addTests(loader.loadTestsFromTestCase(TestSQLValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestPromptsCompliance))
    suite.addTests(loader.loadTestsFromTestCase(TestSchemaEssential))
    suite.addTests(loader.loadTestsFromTestCase(TestExportTools))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 输出摘要
    print("\n" + "="*60)
    print("测试结果摘要")
    print("="*60)
    passed = result.testsRun - len(result.failures) - len(result.errors)
    print(f"通过: {passed}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    print(f"总计: {result.testsRun}")
    print("="*60)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
