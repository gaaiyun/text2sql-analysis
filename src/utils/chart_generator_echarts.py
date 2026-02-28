#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
基于ECharts的图表生成模块
使用pyecharts生成专业的交互式图表
"""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional

from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Pie, Scatter
from pyecharts.globals import ThemeType


def _ensure_output_dir(output_path: str) -> str:
    """确保输出目录存在"""
    p = Path(output_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    return str(p.resolve())


def bar_chart_echarts(
    categories: List[str],
    values: List[float],
    output_path: str,
    title: str = "柱状图",
    x_label: str = "",
    y_label: str = "",
) -> str:
    """ECharts柱状图"""
    path = _ensure_output_dir(output_path)
    
    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width="1000px", height="600px"))
        .add_xaxis([str(x) for x in categories[:20]])
        .add_yaxis(y_label or "数值", values[:20], label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            title_opts=opts.TitleOpts(title=title, subtitle=""),
            xaxis_opts=opts.AxisOpts(name=x_label, axislabel_opts=opts.LabelOpts(rotate=45)),
            yaxis_opts=opts.AxisOpts(name=y_label),
            toolbox_opts=opts.ToolboxOpts(),
        )
    )
    c.render(path)
    
    # 转换为PNG
    png_path = path.replace('.html', '.png')
    try:
        from snapshot_selenium import snapshot
        snapshot.make_snapshot(snapshot.driver(), c.render(), png_path)
        return png_path
    except:
        # 如果截图失败，返回HTML路径
        return path


def line_chart_echarts(
    x_data: List[str],
    y_series: Dict[str, List[float]],
    output_path: str,
    title: str = "折线图",
    x_label: str = "",
    y_label: str = "",
) -> str:
    """ECharts折线图"""
    path = _ensure_output_dir(output_path)
    
    c = Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width="1000px", height="600px"))
    c.add_xaxis([str(x) for x in x_data])
    
    for name, values in y_series.items():
        c.add_yaxis(
            name,
            values,
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False),
        )
    
    c.set_global_opts(
        title_opts=opts.TitleOpts(title=title),
        xaxis_opts=opts.AxisOpts(name=x_label, axislabel_opts=opts.LabelOpts(rotate=45)),
        yaxis_opts=opts.AxisOpts(name=y_label),
        toolbox_opts=opts.ToolboxOpts(),
        legend_opts=opts.LegendOpts(pos_top="5%"),
    )
    c.render(path)
    
    # 转换为PNG
    png_path = path.replace('.html', '.png')
    try:
        from snapshot_selenium import snapshot
        snapshot.make_snapshot(snapshot.driver(), c.render(), png_path)
        return png_path
    except:
        return path


def pie_chart_echarts(
    labels: List[str],
    sizes: List[float],
    output_path: str,
    title: str = "饼图",
) -> str:
    """ECharts饼图"""
    path = _ensure_output_dir(output_path)
    
    data = [[labels[i], sizes[i]] for i in range(min(len(labels), len(sizes), 10))]
    
    c = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width="1000px", height="600px"))
        .add(
            "",
            data,
            radius=["30%", "75%"],
            label_opts=opts.LabelOpts(formatter="{b}: {c} ({d}%)"),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title=title),
            legend_opts=opts.LegendOpts(orient="vertical", pos_left="left"),
        )
    )
    c.render(path)
    
    # 转换为PNG
    png_path = path.replace('.html', '.png')
    try:
        from snapshot_selenium import snapshot
        snapshot.make_snapshot(snapshot.driver(), c.render(), png_path)
        return png_path
    except:
        return path


def infer_chart_type(columns: List[str], rows: List[tuple]) -> Dict[str, Any]:
    """推断图表类型"""
    if not columns or not rows:
        return {"chart_type": "table", "x_column": None, "y_columns": [], "title": "数据表格"}
    
    # 识别列类型
    time_keywords = ["年份", "年", "时间", "日期", "月份", "季度", "year", "date", "time", "month"]
    category_keywords = ["名称", "行业", "地区", "省份", "城市", "类型", "name", "industry", "region", "type"]
    
    time_cols = [i for i, col in enumerate(columns) if any(kw in str(col).lower() for kw in time_keywords)]
    category_cols = [i for i, col in enumerate(columns) if any(kw in str(col).lower() for kw in category_keywords)]
    
    # 识别数值列
    numeric_cols = []
    for i, col in enumerate(columns):
        if i not in time_cols and i not in category_cols:
            try:
                val = rows[0][i]
                if isinstance(val, (int, float)) or (isinstance(val, str) and val.replace('.', '').replace('-', '').isdigit()):
                    numeric_cols.append(i)
            except:
                pass
    
    # 推断图表类型
    if time_cols and numeric_cols:
        return {
            "chart_type": "line",
            "x_column": time_cols[0],
            "y_columns": numeric_cols[:3],
            "title": f"{columns[time_cols[0]]}趋势图"
        }
    elif len(category_cols) == 1 and len(numeric_cols) == 1:
        if len(rows) <= 10:
            return {
                "chart_type": "pie",
                "x_column": category_cols[0],
                "y_columns": [numeric_cols[0]],
                "title": f"{columns[category_cols[0]]}分布"
            }
        else:
            return {
                "chart_type": "bar",
                "x_column": category_cols[0],
                "y_columns": [numeric_cols[0]],
                "title": f"{columns[category_cols[0]]}统计"
            }
    elif len(columns) >= 2 and numeric_cols:
        x_col = 0 if 0 not in numeric_cols else 1
        return {
            "chart_type": "bar",
            "x_column": x_col,
            "y_columns": numeric_cols[:1],
            "title": "数据统计"
        }
    else:
        return {"chart_type": "table", "x_column": None, "y_columns": [], "title": "数据表格"}


def generate_chart_auto_echarts(
    columns: List[str],
    rows: List[tuple],
    output_path: str,
    title: Optional[str] = None
) -> Optional[str]:
    """自动生成ECharts图表"""
    if not rows:
        return None
    
    chart_info = infer_chart_type(columns, rows)
    
    if chart_info["chart_type"] == "table":
        return None
    
    chart_title = title or chart_info["title"]
    x_col = chart_info["x_column"]
    y_cols = chart_info["y_columns"]
    
    try:
        if chart_info["chart_type"] == "line":
            x_data = [str(row[x_col]) for row in rows]
            y_series = {columns[col]: [float(row[col]) if row[col] else 0 for row in rows] for col in y_cols}
            return line_chart_echarts(x_data, y_series, output_path, title=chart_title, x_label=columns[x_col])
        
        elif chart_info["chart_type"] == "bar":
            categories = [str(row[x_col]) for row in rows[:20]]
            values = [float(row[y_cols[0]]) if row[y_cols[0]] else 0 for row in rows[:20]]
            return bar_chart_echarts(categories, values, output_path, title=chart_title, 
                                    x_label=columns[x_col], y_label=columns[y_cols[0]])
        
        elif chart_info["chart_type"] == "pie":
            labels = [str(row[x_col]) for row in rows[:10]]
            sizes = [float(row[y_cols[0]]) if row[y_cols[0]] else 0 for row in rows[:10]]
            return pie_chart_echarts(labels, sizes, output_path, title=chart_title)
        
    except Exception as e:
        print(f"ECharts图表生成失败: {e}")
        return None
    
    return None
