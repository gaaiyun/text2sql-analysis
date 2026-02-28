#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Text2SQL Web应用 - 基于Gradio
提供专业的Web界面用于Text2SQL查询和报告生成
"""

import gradio as gr
import sys
import os
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from demo.text2sql_utils import Text2SQLPipeline
from src.utils.config import Config

# 创建场景1-3的pipeline（Gaaiyun数据库）
pipeline_1_3 = Text2SQLPipeline(scenario="scenario_1_3")

# 创建场景4-5的pipeline（gaaiyun_2数据库）
pipeline_4_5 = Text2SQLPipeline(scenario="scenario_4_5")


def process_query(question: str, scenario: str):
    """处理查询请求"""
    try:
        # 选择对应的pipeline
        if scenario in ["场景1-数据洞察", "场景2-地区产业", "场景3-行业分析"]:
            pipeline = pipeline_1_3
            output_prefix = f"scenario_{scenario[3]}"
        else:
            pipeline = pipeline_4_5
            output_prefix = f"scenario_{scenario[3]}"
        
        # 1. 生成SQL
        sql = pipeline.generate_sql(question)
        
        # 2. 执行查询
        try:
            columns, rows = pipeline.execute_sql(sql)
            data_preview = format_data_table(columns, rows[:10])
            record_count = len(rows)
        except Exception as e:
            return sql, f"查询执行失败：{str(e)}", "", "", None, None, None
        
        # 3. 生成图表
        chart_path = f"output/web_{output_prefix}_chart.png"
        try:
            chart_file = pipeline.generate_chart(columns, rows, question, chart_path)
        except Exception as e:
            chart_file = None
        
        # 4. 网络搜索
        try:
            search_results = pipeline.web_search(f"{question} 2024 2025", num_results=3)
            search_text = format_search_results(search_results)
        except Exception as e:
            search_text = f"网络搜索失败：{str(e)}"
        
        # 5. 数据分析
        try:
            analysis = pipeline.analyze_data(question, sql, columns, rows)
        except Exception as e:
            analysis = f"数据分析失败：{str(e)}"
        
        # 6. 生成报告
        try:
            results = pipeline.run(question, output_prefix=f"web_{output_prefix}")
            md_file = results.get('markdown')
            pdf_file = results.get('pdf')
            word_file = results.get('word')
        except Exception as e:
            md_file = pdf_file = word_file = None
        
        return (
            sql,
            f"查询成功！共{record_count}条记录",
            data_preview,
            analysis,
            search_text,
            chart_file,
            [md_file, pdf_file, word_file] if md_file else None
        )
        
    except Exception as e:
        return f"错误：{str(e)}", "", "", "", "", None, None


def format_data_table(columns, rows):
    """格式化数据表格为Markdown"""
    if not rows:
        return "无数据"
    
    # 表头
    header = "| " + " | ".join(str(col) for col in columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    
    # 数据行
    data_rows = []
    for row in rows[:10]:  # 只显示前10行
        row_str = "| " + " | ".join(str(val) if val is not None else "" for val in row) + " |"
        data_rows.append(row_str)
    
    result = "\n".join([header, separator] + data_rows)
    if len(rows) > 10:
        result += f"\n\n（共{len(rows)}条记录，仅显示前10条）"
    
    return result


def format_search_results(results):
    """格式化搜索结果"""
    if not results:
        return "未找到相关信息"
    
    formatted = []
    for i, result in enumerate(results[:3], 1):
        formatted.append(f"{i}. **{result.get('title', '无标题')}**")
        formatted.append(f"   {result.get('snippet', '无摘要')}")
        formatted.append(f"   来源：{result.get('url', '无链接')}\n")
    
    return "\n".join(formatted)


# 创建Gradio界面
with gr.Blocks(title="Text2SQL 智能查询系统") as app:
    
    gr.Markdown("""
    # Text2SQL 智能查询系统
    
    **基于大语言模型的自然语言数据库查询与报告生成系统**
    
    支持5个业务场景：数据洞察、地区产业分析、行业分析、招商清单、企业尽调
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            scenario = gr.Dropdown(
                choices=[
                    "场景1-数据洞察",
                    "场景2-地区产业",
                    "场景3-行业分析",
                    "场景4-招商清单",
                    "场景5-企业尽调"
                ],
                value="场景1-数据洞察",
                label="选择场景"
            )
            
            question = gr.Textbox(
                label="输入您的问题（自然语言）",
                placeholder="例如：分析2023-2024年融资趋势，按行业统计融资金额和融资数量",
                lines=3
            )
            
            submit_btn = gr.Button("查询", variant="primary", size="lg")
            
            gr.Markdown("""
            ### 示例问题
            
            **场景1-数据洞察**：
            - 分析2023-2024年融资趋势，按行业统计融资金额和融资数量
            - 查询近三年融资金额最高的10个行业
            
            **场景2-地区产业**：
            - 分析广东省深圳市的产业分布，统计各行业企业数量和主要领域
            
            **场景3-行业分析**：
            - 分析科技行业近5年的发展趋势，包括企业数量增长和地域分布
            
            **场景4-招商清单**：
            - 查询注册资本超过1000万的企业，统计其基本信息、知识产权和诉讼情况
            
            **场景5-企业尽调**：
            - 查询某一家企业的详细信息，生成全面尽职调查报告
            """)
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 查询结果")
            
            with gr.Tab("生成的SQL"):
                sql_output = gr.Code(label="SQL查询语句", language="sql")
            
            with gr.Tab("数据预览"):
                status_output = gr.Textbox(label="查询状态")
                data_output = gr.Markdown(label="数据表格（前10条）")
            
            with gr.Tab("图表分析"):
                chart_output = gr.Image(label="数据图表")
            
            with gr.Tab("数据解读"):
                analysis_output = gr.Markdown(label="AI数据分析")
            
            with gr.Tab("网络信息"):
                search_output = gr.Markdown(label="网络搜索补充")
            
            with gr.Tab("报告下载"):
                report_files = gr.Files(label="生成的报告文件（Markdown/PDF/Word）")
    
    # 绑定事件
    submit_btn.click(
        fn=process_query,
        inputs=[question, scenario],
        outputs=[
            sql_output,
            status_output,
            data_output,
            analysis_output,
            search_output,
            chart_output,
            report_files
        ]
    )
    
    gr.Markdown("""
    ---
    
    ### 使用说明
    
    1. **选择场景**：根据您的需求选择对应的业务场景
    2. **输入问题**：用自然语言描述您想查询的内容
    3. **点击查询**：系统将自动生成SQL、执行查询、分析数据并生成报告
    4. **查看结果**：在不同Tab页查看SQL、数据、图表、分析和报告
    5. **下载报告**：在"报告下载"Tab页下载完整的分析报告
    
    ### 技术架构
    
    - **SQL生成**：阿里云百炼 Coding Plan (qwen3.5-plus)
    - **数据库**：MySQL (场景1-3: Gaaiyun, 场景4-5: gaaiyun_2)
    - **图表生成**：Matplotlib + 自动推断
    - **网络搜索**：DuckDuckGo
    - **报告生成**：Markdown/PDF/Word多格式输出
    
    ### 注意事项
    
    - 查询时间可能需要1-2分钟，请耐心等待
    - 复杂查询可能需要更长时间
    - 报告文件保存在 output 目录
    
    ---
    *Powered by Text2SQL v2.0 | © 2026*
    """)


if __name__ == "__main__":
    # 启动Web应用
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )
