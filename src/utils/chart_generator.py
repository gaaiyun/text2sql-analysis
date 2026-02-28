#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
图表生成模块

封装 matplotlib，提供标准图表类型：折线图、柱状图、饼图、热力图。
返回图片文件路径，供场景 1-3 多模态报告使用。
"""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional, Union

import matplotlib
matplotlib.use('Agg')  # 无头模式，适合服务器
import matplotlib.pyplot as plt
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

import numpy as np


def _ensure_output_dir(output_path: str) -> str:
    """确保输出目录存在，返回绝对路径"""
    p = Path(output_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    return str(p.resolve())


def line_chart(
    x_data: List[Union[str, int, float]],
    y_series: Dict[str, List[float]],
    output_path: str,
    title: str = "",
    x_label: str = "",
    y_label: str = "",
    figsize: tuple = (10, 6),
    dpi: int = 150,
) -> str:
    """
    折线图：融资趋势、企业增长等。现代化专业样式。

    Args:
        x_data: 横轴标签（如年份、月份）
        y_series: 多条线，key 为图例名，value 为数值列表
        output_path: 输出图片路径
        title, x_label, y_label: 标题与轴标签
        figsize, dpi: 图像尺寸与分辨率

    Returns:
        生成的图片文件绝对路径
    """
    path = _ensure_output_dir(output_path)
    
    # 设置现代化样式
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi, facecolor='white')
    
    x_pos = np.arange(len(x_data))
    colors = ['#4A90E2', '#E74C3C', '#2ECC71', '#F39C12', '#9B59B6']
    
    for idx, (name, values) in enumerate(y_series.items()):
        color = colors[idx % len(colors)]
        ax.plot(x_pos, values, marker='o', label=name, linewidth=2.5, 
               markersize=8, color=color, alpha=0.9)
    
    ax.set_xticks(x_pos)
    ax.set_xticklabels([str(x) for x in x_data], rotation=45, ha='right', fontsize=10)
    
    if title:
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20, color='#2C3E50')
    if x_label:
        ax.set_xlabel(x_label, fontsize=11, fontweight='bold')
    if y_label:
        ax.set_ylabel(y_label, fontsize=11, fontweight='bold')
    
    ax.legend(loc='best', fontsize=10, frameon=True, shadow=True, fancybox=True)
    ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    fig.tight_layout()
    fig.savefig(path, bbox_inches='tight', dpi=dpi, facecolor='white')
    plt.close(fig)
    return path


def bar_chart(
    categories: List[str],
    values: List[float],
    output_path: str,
    title: str = "",
    x_label: str = "",
    y_label: str = "",
    color: str = "#4A90E2",
    figsize: tuple = (10, 6),
    dpi: int = 150,
    horizontal: bool = False,
) -> str:
    """
    柱状图：产业分布、排名等。现代化专业样式。

    Args:
        categories: 类别名称
        values: 对应数值
        output_path: 输出路径
        horizontal: 是否横向柱状图

    Returns:
        图片文件路径
    """
    path = _ensure_output_dir(output_path)
    
    # 设置现代化样式
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi, facecolor='white')
    
    x_pos = np.arange(len(categories))
    if horizontal:
        bars = ax.barh(x_pos, values, color=color, alpha=0.85, edgecolor='white', linewidth=1.5)
        ax.set_yticks(x_pos)
        ax.set_yticklabels(categories, fontsize=10)
        if y_label:
            ax.set_xlabel(y_label, fontsize=11, fontweight='bold')
        if x_label:
            ax.set_ylabel(x_label, fontsize=11, fontweight='bold')
        # 添加数值标签
        for i, (bar, val) in enumerate(zip(bars, values)):
            ax.text(val, i, f' {val:.1f}', va='center', fontsize=9, color='#333')
    else:
        bars = ax.bar(x_pos, values, color=color, alpha=0.85, edgecolor='white', linewidth=1.5)
        ax.set_xticks(x_pos)
        ax.set_xticklabels(categories, rotation=45, ha='right', fontsize=10)
        if x_label:
            ax.set_xlabel(x_label, fontsize=11, fontweight='bold')
        if y_label:
            ax.set_ylabel(y_label, fontsize=11, fontweight='bold')
        # 添加数值标签
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}', ha='center', va='bottom', fontsize=9, color='#333')
    
    if title:
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20, color='#2C3E50')
    
    ax.grid(True, axis='y', alpha=0.3, linestyle='--', linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    fig.tight_layout()
    fig.savefig(path, bbox_inches='tight', dpi=dpi, facecolor='white')
    plt.close(fig)
    return path


def pie_chart(
    labels: List[str],
    sizes: List[float],
    output_path: str,
    title: str = "",
    figsize: tuple = (10, 7),
    dpi: int = 150,
    autopct: str = "%1.1f%%",
) -> str:
    """
    饼图：行业分布、占比等。现代化专业样式。

    Args:
        labels: 类别标签
        sizes: 数值（将自动计算占比）
        output_path: 输出路径

    Returns:
        图片文件路径
    """
    path = _ensure_output_dir(output_path)
    
    # 设置现代化样式
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi, facecolor='white')
    
    total = sum(sizes)
    if total <= 0:
        sizes = [1.0] * len(labels)
    
    # 现代化配色方案
    colors = ['#4A90E2', '#E74C3C', '#2ECC71', '#F39C12', '#9B59B6', 
              '#1ABC9C', '#E67E22', '#3498DB', '#95A5A6', '#34495E']
    
    # 突出显示最大的扇区
    explode = [0.05 if i == sizes.index(max(sizes)) else 0 for i in range(len(sizes))]
    
    wedges, texts, autotexts = ax.pie(
        sizes, 
        labels=labels, 
        autopct=autopct, 
        startangle=90, 
        pctdistance=0.85,
        colors=colors[:len(labels)],
        explode=explode,
        shadow=True,
        textprops={'fontsize': 10, 'weight': 'bold'}
    )
    
    # 美化百分比文字
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(10)
        autotext.set_weight('bold')
    
    if title:
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20, color='#2C3E50')
    
    ax.axis('equal')
    fig.tight_layout()
    fig.savefig(path, bbox_inches='tight', dpi=dpi, facecolor='white')
    plt.close(fig)
    return path


def heatmap(
    data: List[List[float]],
    row_labels: List[str],
    col_labels: List[str],
    output_path: str,
    title: str = "",
    figsize: tuple = (8, 6),
    dpi: int = 150,
    cmap: str = "YlOrRd",
) -> str:
    """
    热力图：地域×指标、相关性等。

    Args:
        data: 二维数值矩阵
        row_labels, col_labels: 行、列标签
        output_path: 输出路径
        cmap: matplotlib 色图名称

    Returns:
        图片文件路径
    """
    path = _ensure_output_dir(output_path)
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    arr = np.array(data)
    im = ax.imshow(arr, cmap=cmap, aspect='auto')
    ax.set_xticks(np.arange(len(col_labels)))
    ax.set_yticks(np.arange(len(row_labels)))
    ax.set_xticklabels(col_labels)
    ax.set_yticklabels(row_labels)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    for i in range(len(row_labels)):
        for j in range(len(col_labels)):
            ax.text(j, i, f"{arr[i, j]:.1f}", ha="center", va="center", color="black", fontsize=8)
    if title:
        ax.set_title(title, fontsize=14)
    fig.colorbar(im, ax=ax)
    fig.tight_layout()
    fig.savefig(path, bbox_inches='tight', dpi=dpi)
    plt.close(fig)
    return path


def multi_bar_chart(
    categories: List[str],
    series: Dict[str, List[float]],
    output_path: str,
    title: str = "",
    x_label: str = "",
    y_label: str = "",
    figsize: tuple = (10, 6),
    dpi: int = 150,
) -> str:
    """
    分组柱状图：多系列对比（如不同年份/类型的柱状对比）。

    Returns:
        图片文件路径
    """
    path = _ensure_output_dir(output_path)
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    n_cat = len(categories)
    n_series = len(series)
    width = 0.8 / n_series
    x = np.arange(n_cat)
    for i, (name, values) in enumerate(series.items()):
        offset = (i - n_series / 2 + 0.5) * width
        ax.bar(x + offset, values, width, label=name, alpha=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=45, ha='right')
    if title:
        ax.set_title(title, fontsize=14)
    if x_label:
        ax.set_xlabel(x_label)
    if y_label:
        ax.set_ylabel(y_label)
    ax.legend(loc='best', fontsize=9)
    ax.grid(True, axis='y', alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, bbox_inches='tight', dpi=dpi)
    plt.close(fig)
    return path


def infer_chart_type(columns: List[str], rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    根据查询结果自动推断图表类型
    
    规则：
    - 含"年份"/"时间"/"日期" + 数值列 → 折线图
    - 1列分类 + 1列数值 → 饼图/柱状图
    - 多分类 + 多数值 → 分组柱状图
    - 其他 → 表格
    
    Args:
        columns: 列名列表
        rows: 数据行列表（字典格式）
    
    Returns:
        {
            "chart_type": "line/bar/pie/multi_bar/table",
            "x_column": "x轴列名",
            "y_columns": ["y轴列名列表"],
            "title": "建议标题"
        }
    """
    if not columns or not rows:
        return {"chart_type": "table", "x_column": None, "y_columns": [], "title": "数据表格"}
    
    # 识别列类型
    time_keywords = ["年份", "年", "时间", "日期", "月份", "季度", "year", "date", "time", "month"]
    category_keywords = ["名称", "行业", "地区", "省份", "城市", "类型", "name", "industry", "region", "type"]
    
    time_cols = [col for col in columns if any(kw in col.lower() for kw in time_keywords)]
    category_cols = [col for col in columns if any(kw in col.lower() for kw in category_keywords)]
    
    # 识别数值列
    numeric_cols = []
    for col in columns:
        if col not in time_cols and col not in category_cols:
            # 检查第一行数据是否为数值
            if rows and col in rows[0]:
                val = rows[0][col]
                if isinstance(val, (int, float)) or (isinstance(val, str) and val.replace('.', '').replace('-', '').isdigit()):
                    numeric_cols.append(col)
    
    # 推断图表类型
    if time_cols and numeric_cols:
        # 时间序列 → 折线图
        return {
            "chart_type": "line",
            "x_column": time_cols[0],
            "y_columns": numeric_cols[:3],  # 最多3条线
            "title": f"{time_cols[0]}趋势图"
        }
    
    elif len(category_cols) == 1 and len(numeric_cols) == 1:
        # 单分类 + 单数值
        if len(rows) <= 10:
            # 数据少 → 饼图
            return {
                "chart_type": "pie",
                "x_column": category_cols[0],
                "y_columns": [numeric_cols[0]],
                "title": f"{category_cols[0]}分布"
            }
        else:
            # 数据多 → 柱状图
            return {
                "chart_type": "bar",
                "x_column": category_cols[0],
                "y_columns": [numeric_cols[0]],
                "title": f"{category_cols[0]}统计"
            }
    
    elif category_cols and len(numeric_cols) > 1:
        # 多分类 + 多数值 → 分组柱状图
        return {
            "chart_type": "multi_bar",
            "x_column": category_cols[0],
            "y_columns": numeric_cols[:3],  # 最多3个系列
            "title": f"{category_cols[0]}对比"
        }
    
    elif len(columns) == 2 and numeric_cols:
        # 2列数据，其中一列是数值 → 柱状图
        x_col = [c for c in columns if c not in numeric_cols][0] if len(numeric_cols) == 1 else columns[0]
        return {
            "chart_type": "bar",
            "x_column": x_col,
            "y_columns": numeric_cols[:1],
            "title": "数据统计"
        }
    
    else:
        # 默认表格
        return {
            "chart_type": "table",
            "x_column": None,
            "y_columns": [],
            "title": "数据表格"
        }


def generate_chart_auto(
    columns: List[str],
    rows: List[Dict[str, Any]],
    output_path: str,
    title: Optional[str] = None
) -> Optional[str]:
    """
    根据数据自动生成图表
    
    Args:
        columns: 列名列表
        rows: 数据行列表
        output_path: 输出路径
        title: 自定义标题（可选）
    
    Returns:
        生成的图片路径，如果无法生成则返回None
    """
    if not rows:
        return None
    
    # 推断图表类型
    chart_info = infer_chart_type(columns, rows)
    
    if chart_info["chart_type"] == "table":
        return None
    
    chart_title = title or chart_info["title"]
    x_col = chart_info["x_column"]
    y_cols = chart_info["y_columns"]
    
    try:
        if chart_info["chart_type"] == "line":
            # 折线图
            x_data = [row[x_col] for row in rows]
            y_series = {col: [float(row.get(col, 0)) for row in rows] for col in y_cols}
            return line_chart(x_data, y_series, output_path, title=chart_title, x_label=x_col)
        
        elif chart_info["chart_type"] == "bar":
            # 柱状图
            categories = [str(row[x_col]) for row in rows[:20]]  # 最多20个
            values = [float(row.get(y_cols[0], 0)) for row in rows[:20]]
            return bar_chart(categories, values, output_path, title=chart_title, x_label=x_col, y_label=y_cols[0])
        
        elif chart_info["chart_type"] == "pie":
            # 饼图
            labels = [str(row[x_col]) for row in rows[:10]]  # 最多10个
            sizes = [float(row.get(y_cols[0], 0)) for row in rows[:10]]
            return pie_chart(labels, sizes, output_path, title=chart_title)
        
        elif chart_info["chart_type"] == "multi_bar":
            # 分组柱状图
            categories = [str(row[x_col]) for row in rows[:15]]  # 最多15个
            series = {col: [float(row.get(col, 0)) for row in rows[:15]] for col in y_cols}
            return multi_bar_chart(categories, series, output_path, title=chart_title, x_label=x_col)
        
    except Exception as e:
        print(f"图表生成失败: {e}")
        return None
    
    return None
