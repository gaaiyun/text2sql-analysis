#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
API调用示例 - 完整报告生成

演示完整的流水线：问题→SQL→执行→分析→图表→网络搜索→报告
"""
import requests
import sys
from pathlib import Path
from datetime import datetime

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from src.utils.chart_generator import generate_chart_auto
from src.utils.web_search import search
from src.utils.document_generator import pdf_from_markdown_sections

API_BASE = "http://localhost:8000"
OUTPUT_DIR = Path(__file__).parent.parent.parent / "output"

def generate_full_report(question: str, scenario: str = "data_insight"):
    """生成完整报告"""
    print("=" * 60)
    print(f"生成完整报告: {question}")
    print("=" * 60)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. 调用API生成SQL并执行
    print("\n[1/5] 调用Text2SQL API...")
    response = requests.post(
        f"{API_BASE}/api/query",
        json={
            "question": question,
            "scenario": scenario,
            "mode": "llm"
        }
    )
    
    if response.status_code != 200:
        print(f"✗ API调用失败: {response.status_code}")
        return None
    
    result = response.json()
    sql = result['sql']
    data = result['data']
    columns = result['columns']
    
    print(f"✓ SQL生成成功")
    print(f"  模式: {result['mode']}")
    print(f"  返回行数: {result['row_count']}")
    
    # 2. 生成图表
    print("\n[2/5] 生成图表...")
    chart_path = OUTPUT_DIR / f"report_{timestamp}_chart.png"
    chart_file = generate_chart_auto(
        columns=columns,
        rows=data,
        output_path=str(chart_path)
    )
    
    if chart_file:
        print(f"✓ 图表已生成: {Path(chart_file).name}")
    else:
        print("⚠ 未生成图表（数据不适合可视化）")
        chart_file = None
    
    # 3. 网络搜索补充
    print("\n[3/5] 网络搜索补充信息...")
    try:
        search_results = search(f"{question} 2026", max_results=3)
        print(f"✓ 找到 {len(search_results)} 条相关信息")
    except Exception as e:
        print(f"⚠ 网络搜索失败: {e}")
        search_results = []
    
    # 4. 组装Markdown报告
    print("\n[4/5] 组装报告...")
    report_md = f"""# {question} - 数据分析报告

**生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**场景**: {scenario}
**模式**: {result['mode']}

---

## 一、用户问题

{question}

---

## 二、生成的SQL

```sql
{sql}
```

---

## 三、数据概览

查询返回 **{result['row_count']}** 行数据，列名：{', '.join(columns)}

### 前10行数据

| {' | '.join(columns)} |
| {' | '.join(['---'] * len(columns))} |
"""
    
    for row in data[:10]:
        values = [str(row.get(col, '')) for col in columns]
        report_md += f"| {' | '.join(values)} |\n"
    
    # 添加图表
    if chart_file:
        report_md += f"\n---\n\n## 四、数据可视化\n\n![图表]({Path(chart_file).name})\n"
    
    # 添加网络搜索结果
    if search_results:
        report_md += "\n---\n\n## 五、网络信息补充\n\n"
        for i, item in enumerate(search_results, 1):
            report_md += f"### {i}. {item['title']}\n\n"
            report_md += f"{item['snippet']}\n\n"
            report_md += f"来源: [{item['source']}]({item['url']})\n\n"
    
    # 添加建议
    report_md += "\n---\n\n## 六、分析建议\n\n"
    report_md += "基于以上数据分析，建议：\n\n"
    report_md += "1. 关注数据趋势变化，识别关键指标\n"
    report_md += "2. 结合网络信息，了解行业动态\n"
    report_md += "3. 定期更新数据，持续跟踪分析\n"
    
    # 5. 保存报告
    print("\n[5/5] 保存报告...")
    md_path = OUTPUT_DIR / f"report_{timestamp}.md"
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(report_md)
    print(f"✓ Markdown报告: {md_path.name}")
    
    # 生成PDF（可选）
    try:
        pdf_path = OUTPUT_DIR / f"report_{timestamp}.pdf"
        sections = [
            {"heading": "用户问题", "content": question},
            {"heading": "生成的SQL", "content": sql},
            {"heading": "数据概览", "content": f"返回{result['row_count']}行数据"},
        ]
        if chart_file:
            sections.append({"heading": "数据可视化", "images": [chart_file]})
        
        pdf_from_markdown_sections(sections, str(pdf_path), title=question)
        print(f"✓ PDF报告: {pdf_path.name}")
    except Exception as e:
        print(f"⚠ PDF生成失败: {e}")
    
    print("\n" + "=" * 60)
    print("报告生成完成！")
    print("=" * 60)
    print(f"输出目录: {OUTPUT_DIR}")
    
    return md_path

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Text2SQL 完整报告生成示例")
    print("=" * 60)
    
    try:
        health = requests.get(f"{API_BASE}/health", timeout=5)
        if health.status_code != 200:
            print("✗ API服务异常")
            exit(1)
        print("✓ API服务正常")
    except Exception as e:
        print(f"✗ 无法连接到API: {e}")
        exit(1)
    
    # 示例1：融资趋势分析
    generate_full_report(
        question="分析近五年融资趋势",
        scenario="data_insight"
    )
    
    print("\n\n")
    
    # 示例2：行业分布分析
    generate_full_report(
        question="统计各行业的企业数量分布",
        scenario="industry"
    )
