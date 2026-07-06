#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Text2SQL 通用工具模块
提供所有场景共用的功能：SQL生成、执行、分析、图表、搜索、报告
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.config import Config
from src.utils.web_search import search
from src.utils.document_generator import pdf_from_markdown_sections, word_from_sections
from src.agent.factory import build_agent_runtime
from src.utils.safe_sql import enforce_safe_sql
from datetime import datetime
import os

class Text2SQLPipeline:
    """Text2SQL完整流水线"""
    
    def __init__(self, scenario: str):
        """
        初始化流水线
        Args:
            scenario: 场景标识，如 'scenario_1_3' 或 'scenario_4_5'
        """
        self.scenario = scenario
        self.config = Config.load()
        self.db_config = self.config.get_database_config(scenario)
        self._runtime = None
        self._last_result = None

    def _get_runtime(self):
        """懒加载统一 Agent Runtime。"""
        if self._runtime is None:
            self._runtime = build_agent_runtime(profile_name="znjz", scenario_key="scenario_1_3")
        return self._runtime

    def _agent_scenario(self) -> str:
        if "4_5" in self.scenario:
            return "due_diligence"
        return "data_insight"
        
    def load_schema(self) -> str:
        """加载Schema"""
        schema_file = "znjz_text2sql_schema.md" if "scenario_1_3" in self.scenario else "gaaiyun_2_schema.md"
        
        schema_path = Path(__file__).parent.parent / "schema" / schema_file
        with open(schema_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def load_examples(self) -> str:
        """加载Few-shot示例"""
        examples_path = Path(__file__).parent.parent / "schema" / "question_sql_examples.md"
        with open(examples_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def generate_sql(self, question: str) -> str:
        """使用统一 Agent Runtime 生成并校验 SQL。"""
        result = self._get_runtime().query(question, scenario=self._agent_scenario())
        self._last_result = result
        if not result.success:
            raise RuntimeError(result.error or "Agent Runtime 查询失败")
        return result.safe_sql or result.sql or ""
    
    def _validate_and_fix_sql(self, sql: str) -> str:
        """验证并修复SQL语法"""
        lines = sql.split('\n')
        fixed_lines = []
        in_select = False
        select_aliases = {}  # 存储别名到原始表达式的映射
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # 检测SELECT子句
            if 'SELECT' in stripped.upper():
                in_select = True
                fixed_lines.append(line)
                continue
            
            # 检测SELECT子句结束
            if in_select and any(keyword in stripped.upper() for keyword in ['FROM', 'WHERE', 'GROUP', 'ORDER', 'LIMIT']):
                in_select = False
            
            # 在SELECT子句中，提取别名映射并修复逗号
            if in_select and stripped and 'AS' in stripped.upper():
                # 移除多余的逗号
                stripped = stripped.replace('，,', '').replace(',,', ',')
                
                # 提取 "expression AS alias" 模式
                parts = stripped.split(' AS ', 1)
                if len(parts) == 2:
                    expr = parts[0].strip().rstrip(',').rstrip('，')
                    alias = parts[1].strip().rstrip(',').rstrip('，')
                    select_aliases[alias] = expr
                
                # 确保只有一个逗号
                if not stripped.endswith(','):
                    if i + 1 < len(lines):
                        next_stripped = lines[i + 1].strip()
                        if next_stripped and not any(keyword in next_stripped.upper() for keyword in ['FROM', 'WHERE', 'GROUP', 'ORDER', 'LIMIT']):
                            stripped = stripped.rstrip() + ','
                
                line = ' ' * (len(line) - len(line.lstrip())) + stripped
                fixed_lines.append(line)
                continue
            
            # 修复GROUP BY中的别名
            if 'GROUP BY' in stripped.upper():
                for alias, expr in select_aliases.items():
                    if alias in stripped and alias != expr:
                        stripped = stripped.replace(alias, expr)
                line = ' ' * (len(line) - len(line.lstrip())) + stripped
            
            # 修复ORDER BY中的别名
            if 'ORDER BY' in stripped.upper():
                for alias, expr in select_aliases.items():
                    if alias in stripped and alias != expr:
                        # 处理 "ORDER BY alias DESC/ASC" 的情况
                        pattern = alias
                        if pattern in stripped:
                            stripped = stripped.replace(pattern, expr)
                line = ' ' * (len(line) - len(line.lstrip())) + stripped
            
            fixed_lines.append(line)
        
        # 移除所有类型的双逗号和中文逗号
        result = '\n'.join(fixed_lines)
        result = result.replace('，,', ',').replace(',,', ',').replace('，', '')
        return result
    
    def execute_sql(self, sql: str) -> tuple:
        """执行SQL查询"""
        if self._last_result and sql in {self._last_result.sql, self._last_result.safe_sql}:
            columns = self._last_result.columns
            rows = [tuple(row.get(col) for col in columns) for row in self._last_result.rows]
            return columns, rows

        runtime = self._get_runtime()
        safety = enforce_safe_sql(sql, allowed_tables=runtime.profile.allowed_tables, max_limit=1000)
        if not safety.is_safe:
            raise RuntimeError("; ".join(safety.errors) or "SQL安全校验未通过")
        query_result = runtime.sql_executor(safety.safe_sql or sql)
        columns = query_result.get("columns", [])
        rows = [tuple(row.get(col) for col in columns) for row in query_result.get("rows", [])]
        return columns, rows
    
    def analyze_data(self, question: str, sql: str, columns: list, rows: list, search_results: list = None) -> str:
        """使用LLM分析数据，融合网络搜索结果"""
        if self._last_result and sql in {self._last_result.sql, self._last_result.safe_sql}:
            return self._last_result.analysis

        if not rows:
            return "### 数据概览\n\n查询结果为空，当前数据库没有返回对应数据。"
        preview = [dict(zip(columns, row)) for row in rows[:3]]
        return f"""### 数据概览

查询返回 {len(rows)} 条记录，字段包括：{', '.join(columns)}。

### 数据预览

{preview}

### 分析局限性

该分析基于当前 SQL 返回结果生成，未引入额外外部数据。"""
    
    def generate_chart(self, columns: list, rows: list, question: str, output_path: str) -> str:
        """生成图表（优先matplotlib，稳定可靠）"""
        try:
            # 确保输出路径是PNG格式
            if not output_path.endswith('.png'):
                output_path = output_path.replace('.png', '') + '.png'
            
            # 使用matplotlib生成图表（稳定可靠）
            from src.utils.chart_generator import generate_chart_auto
            
            # 转换rows为字典格式
            rows_dict = [dict(zip(columns, row)) for row in rows]
            result = generate_chart_auto(columns, rows_dict, output_path, title=question)
            
            if result and os.path.exists(result):
                print(f"图表已生成：{result}")
                return result
            else:
                # 如果自动推断失败，使用默认柱状图
                from src.utils.chart_generator import bar_chart
                if len(columns) >= 2 and len(rows) > 0:
                    labels = [str(row[0]) for row in rows[:10]]
                    values = [float(row[1]) if len(row) > 1 and row[1] else 0 for row in rows[:10]]
                    result = bar_chart(labels, values, output_path, title=question)
                    if result and os.path.exists(result):
                        return result
            
            # 如果所有方法都失败，返回None
            return None
        except Exception as e:
            print(f"图表生成失败：{e}")
            import traceback
            traceback.print_exc()
            return None
    
    def web_search(self, query: str, num_results: int = 3) -> list:
        """网络搜索 - 提取关键词并搜索相关内容"""
        search_query = f"{query} 2024 2025 最新发展"
        
        try:
            results = search(search_query, max_results=num_results)
            return results if results else []
        except Exception as e:
            print(f"网络搜索失败：{e}")
            return []
    
    def generate_report(self, question: str, sql: str, columns: list, rows: list, 
                       analysis: str, chart_path: str, search_results: list,
                       output_prefix: str) -> dict:
        """生成完整报告（Markdown, PDF, Word）"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 数据表格
        table_text = "| " + " | ".join(columns) + " |\n"
        table_text += "| " + " | ".join(["---"] * len(columns)) + " |\n"
        for row in rows[:10]:
            table_text += "| " + " | ".join([str(v) for v in row]) + " |\n"
        if len(rows) > 10:
            table_text += f"\n（共{len(rows)}条记录，仅显示前10条）\n"
        
        # 网络搜索结果格式化
        if search_results:
            search_text = "### 相关行业动态\n\n"
            for i, r in enumerate(search_results, 1):
                search_text += f"**{i}. {r['title']}**\n\n{r['snippet']}\n\n来源：{r.get('source', 'N/A')}\n\n"
        else:
            search_text = "暂无相关网络信息"
        
        # Markdown报告
        report = f"""# {question} - 分析报告

**生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 1. 问题描述

{question}

## 2. 生成的SQL

```sql
{sql}
```

## 3. 数据概览

{table_text}

## 4. 图表分析

![数据图表]({chart_path})

## 5. 数据分析与解读

{analysis}

## 6. 网络信息补充

{search_text}

## 7. 结论与建议

基于以上数据分析和网络信息，建议：
- 持续关注行业动态和政策变化
- 重点关注高增长领域的投资机会
- 加强风险管理和尽职调查

---
*本报告由Text2SQL系统自动生成*
"""
        
        # 保存Markdown
        md_path = f"output/{output_prefix}_{timestamp}.md"
        Path(md_path).parent.mkdir(parents=True, exist_ok=True)
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        # 生成PDF和Word
        sections = [
            {"heading": "问题描述", "content": question},
            {"heading": "生成的SQL", "content": f"```sql\n{sql}\n```"},
            {"heading": "数据概览", "content": f"查询返回{len(rows)}条记录\n\n{table_text}"},
            {"heading": "图表分析", "content": "数据可视化图表"},
            {"heading": "数据分析与解读", "content": analysis},
            {"heading": "网络信息补充", "content": search_text},
        ]
        
        # 只在图表存在时传递图片路径
        image_paths = []
        if chart_path and os.path.exists(chart_path):
            image_paths = [chart_path]
            print(f"图表将插入报告：{chart_path}")
        else:
            print("警告：图表文件不存在，将跳过图片插入")
        
        pdf_path = f"output/{output_prefix}_{timestamp}.pdf"
        pdf_from_markdown_sections(sections, pdf_path, title=question, image_paths=image_paths)
        
        word_path = f"output/{output_prefix}_{timestamp}.docx"
        word_from_sections(sections, word_path, title=question, image_paths=image_paths)
        
        return {
            'markdown': md_path,
            'pdf': pdf_path,
            'word': word_path,
            'chart': chart_path
        }
    
    def run(self, question: str, output_prefix: str) -> dict:
        """运行完整流水线"""
        print("=" * 80)
        print(f"Text2SQL 完整流水线")
        print("=" * 80)
        print(f"\n问题：{question}\n")
        
        # 1. 生成SQL
        print("[1/7] 生成SQL...")
        sql = self.generate_sql(question)
        print(f"生成的SQL:\n{sql}\n")
        
        # 2. 执行查询
        print("[2/7] 执行查询...")
        columns, rows = self.execute_sql(sql)
        print(f"查询结果：{len(rows)}条记录\n")
        
        # 3. 生成图表
        print("[3/7] 生成图表...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        chart_path = f"output/{output_prefix}_{timestamp}_chart.png"
        chart_path = self.generate_chart(columns, rows, question, chart_path)
        print(f"图表已保存：{chart_path}\n")
        
        # 4. 网络搜索
        print("[4/7] 网络搜索补充...")
        search_results = self.web_search(f"{question} 2024 2025", num_results=3)
        print(f"搜索到{len(search_results)}条相关信息\n")
        
        # 5. LLM分析（融合网络搜索结果）
        print("[5/7] 数据分析...")
        analysis = self.analyze_data(question, sql, columns, rows, search_results)
        print(f"分析完成\n")
        
        # 6. 生成报告
        print("[6/7] 生成报告...")
        results = self.generate_report(question, sql, columns, rows, analysis, 
                                      chart_path, search_results, output_prefix)
        
        print(f"Markdown报告：{results['markdown']}")
        print(f"PDF报告：{results['pdf']}")
        print(f"Word报告：{results['word']}")
        
        print("\n" + "=" * 80)
        print("流水线完成！")
        print("=" * 80)
        
        return results
