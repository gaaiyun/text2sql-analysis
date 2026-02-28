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
from src.utils.chart_generator import generate_chart_auto
from src.utils.web_search import search
from src.utils.document_generator import pdf_from_markdown_sections, word_from_sections
import pymysql
from openai import OpenAI
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
        self.api_key = self.config.get_api_key('dashscope')
        self.base_url = os.environ.get('DASHSCOPE_BASE_URL', 'https://coding.dashscope.aliyuncs.com/v1')
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        
    def load_schema(self) -> str:
        """加载Schema"""
        if 'scenario_1_3' in self.scenario:
            schema_file = "gaaiyun_schema.md"
        else:
            schema_file = "gaaiyun_2_schema.md"
        
        schema_path = Path(__file__).parent.parent / "schema" / schema_file
        with open(schema_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def load_examples(self) -> str:
        """加载Few-shot示例"""
        examples_path = Path(__file__).parent.parent / "schema" / "question_sql_examples.md"
        with open(examples_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def generate_sql(self, question: str) -> str:
        """使用LLM生成SQL"""
        schema = self.load_schema()
        examples = self.load_examples()
        
        prompt = f"""你是SQL专家。根据Schema和示例生成MySQL查询。

## Schema
{schema[:2000]}

## Few-shot示例
{examples[:1000]}

## 重要规则
1. SELECT子句中，每个字段后面必须有逗号（最后一个字段除外）
2. JOIN必须使用COLLATE: ON a.eid = b.eid COLLATE utf8mb4_unicode_ci
3. 时间范围默认近3年
4. LIMIT 1000
5. **GROUP BY和ORDER BY必须使用原始字段名或表达式，不能使用SELECT中的别名**

## 正确的SQL格式示例
SELECT 
    ic.name AS 行业名,
    COUNT(*) AS 数量,
    SUM(amount) AS 总金额
FROM 融资数据 rf
LEFT JOIN 企业行业代码 ic ON rf.eid = ic.eid COLLATE utf8mb4_unicode_ci
WHERE rf.round_date >= '2023-01-01'
GROUP BY ic.name
ORDER BY SUM(amount) DESC
LIMIT 1000

注意：
- 每个字段后面都有逗号
- GROUP BY使用ic.name（原始字段），不是"行业名"（别名）
- ORDER BY使用SUM(amount)（原始表达式），不是"总金额"（别名）

## 问题
{question}

## SQL（必须包含逗号）
"""
        
        response = self.client.chat.completions.create(
            model="qwen3.5-plus",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600,
            temperature=0.1
        )
        
        sql = response.choices[0].message.content.strip()
        sql = sql.replace('```sql', '').replace('```', '').strip()
        
        # 验证并修复SQL
        sql = self._validate_and_fix_sql(sql)
        return sql
    
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
        conn = pymysql.connect(**self.db_config)
        cur = conn.cursor()
        cur.execute(sql)
        columns = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return columns, rows
    
    def analyze_data(self, question: str, sql: str, columns: list, rows: list, search_results: list = None) -> str:
        """使用LLM分析数据，融合网络搜索结果"""
        data_summary = f"查询返回{len(rows)}条记录，字段：{', '.join(columns)}\n"
        if rows:
            data_summary += f"前3条数据：\n"
            for i, row in enumerate(rows[:3], 1):
                data_summary += f"{i}. {dict(zip(columns, row))}\n"
        
        # 整合网络搜索信息
        web_context = ""
        if search_results:
            web_context = "\n\n外部信息参考：\n"
            for i, r in enumerate(search_results[:3], 1):
                web_context += f"{i}. {r['title']}\n   {r['snippet'][:200]}...\n"
        
        prompt = f"""你是数据分析专家。根据查询结果和外部信息进行综合分析。

问题：{question}

SQL查询：
{sql}

数据摘要：
{data_summary}
{web_context}

请提供：
1. 数据概览（3-5句话，说明查询结果的基本情况）
2. 关键发现（3-5个要点，基于实际数据）
3. 趋势分析（结合数据和外部信息）
4. 业务建议（可操作的建议）

要求：
- 基于实际数据进行分析，不要编造数字
- 如果有外部信息，自然地融合到分析中
- 用中文回答，简洁专业
- 使用markdown格式，用###标记小标题"""
        
        response = self.client.chat.completions.create(
            model="qwen3.5-plus",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.3
        )
        
        return response.choices[0].message.content.strip()
    
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
        # 使用LLM提取关键词
        prompt = f"""从以下问题中提取2-3个核心关键词，用于网络搜索。

问题：{query}

要求：
1. 提取地区、行业、主题等核心词
2. 去掉"分析"、"查询"、"统计"等动词
3. 只返回关键词，用空格分隔

示例：
问题：分析广州这几年的企业增长的特征
关键词：广州 企业增长 发展趋势

现在提取关键词："""
        
        try:
            response = self.client.chat.completions.create(
                model="qwen3.5-plus",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=50,
                temperature=0.1
            )
            keywords = response.choices[0].message.content.strip()
            print(f"搜索关键词：{keywords}")
        except Exception as e:
            print(f"关键词提取失败：{e}")
            keywords = query
        
        # 添加时间范围和地域信息
        search_query = f"{keywords} 2024 2025 最新发展"
        
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
