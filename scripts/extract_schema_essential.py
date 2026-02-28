#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
精简 Schema 提取工具
基于实践经验优化：只提取核心信息，避免 token 过载

使用方法:
    python scripts/extract_schema_essential.py
"""

import pymysql
import json
from pathlib import Path


def load_db_config_from_file(scenario):
    """直接从 config.json 加载数据库配置"""
    config_path = Path(__file__).parent.parent / "config.json"
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    return config['database'][scenario]


def extract_essential_schema(db_config, output_file):
    """
    提取精简 Schema
    
    只保留：
    1. 表名 + 表注释
    2. 核心字段名（前10个）
    3. 特殊类型字段（非text/varchar）
    4. 主键信息
    """
    try:
        conn = pymysql.connect(**db_config)
        cur = conn.cursor()
        
        # 获取所有表
        cur.execute(f"""
            SELECT table_name, table_comment
            FROM information_schema.tables
            WHERE table_schema = '{db_config['database']}'
            ORDER BY table_name
        """)
        tables = cur.fetchall()
        
        schema_lines = []
        schema_lines.append(f"# {db_config['database']} 数据库精简 Schema")
        schema_lines.append(f"\n共 {len(tables)} 张表\n")
        schema_lines.append("---\n")
        
        for table_name, table_comment in tables:
            # 获取字段信息
            cur.execute(f"""
                SELECT 
                    column_name,
                    data_type,
                    column_key,
                    column_comment
                FROM information_schema.columns
                WHERE table_schema = '{db_config['database']}'
                AND table_name = '{table_name}'
                ORDER BY ordinal_position
            """)
            columns = cur.fetchall()
            
            # 表信息
            schema_lines.append(f"## {table_name}")
            if table_comment:
                schema_lines.append(f"**说明**: {table_comment}\n")
            
            # 主键
            primary_keys = [col[0] for col in columns if col[2] == 'PRI']
            if primary_keys:
                schema_lines.append(f"**主键**: {', '.join(primary_keys)}")
            
            # 核心字段（前10个）
            schema_lines.append(f"**字段** ({len(columns)} 个):")
            for i, (col_name, data_type, col_key, col_comment) in enumerate(columns[:10]):
                key_mark = " [PK]" if col_key == 'PRI' else ""
                comment_mark = f" - {col_comment}" if col_comment else ""
                schema_lines.append(f"  - {col_name}{key_mark}{comment_mark}")
            
            if len(columns) > 10:
                schema_lines.append(f"  - ... (还有 {len(columns) - 10} 个字段)")
            
            # 特殊类型字段
            special_fields = [
                (col[0], col[1]) for col in columns 
                if col[1] not in ['varchar', 'text', 'char', 'longtext', 'mediumtext']
            ]
            if special_fields:
                schema_lines.append(f"\n**特殊类型字段**:")
                for col_name, data_type in special_fields[:5]:
                    schema_lines.append(f"  - {col_name}: {data_type}")
            
            schema_lines.append("\n---\n")
        
        # 写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(schema_lines))
        
        conn.close()
        
        print(f"[OK] 精简 Schema 已保存到: {output_file}")
        print(f"[INFO] 表数量: {len(tables)}")
        print(f"[INFO] 文件大小: {Path(output_file).stat().st_size / 1024:.1f} KB")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] 提取失败: {e}")
        return False


def extract_sql_templates(db_config, output_file):
    """
    生成常用 SQL 模板
    """
    templates = []
    
    templates.append("# SQL 查询模板\n")
    templates.append("## 场景 1-3: 数据洞察/地区产业/行业分析\n")
    
    templates.append("### 模板 1: 企业融资趋势")
    templates.append("```sql")
    templates.append("SELECT ")
    templates.append("    YEAR(投资时间) as 年份,")
    templates.append("    COUNT(*) as 融资次数,")
    templates.append("    SUM(投资金额) as 总金额")
    templates.append("FROM 投资事件")
    templates.append("WHERE 投资时间 >= DATE_SUB(NOW(), INTERVAL 3 YEAR)")
    templates.append("GROUP BY YEAR(投资时间)")
    templates.append("ORDER BY 年份")
    templates.append("```\n")
    
    templates.append("### 模板 2: 行业分布")
    templates.append("```sql")
    templates.append("SELECT ")
    templates.append("    ic.行业名称,")
    templates.append("    COUNT(DISTINCT b.eid) as 企业数量")
    templates.append("FROM 企业基本信息 b")
    templates.append("LEFT JOIN 企业行业分类 ic ON b.eid = ic.eid COLLATE utf8mb4_unicode_ci")
    templates.append("GROUP BY ic.行业名称")
    templates.append("ORDER BY 企业数量 DESC")
    templates.append("LIMIT 20")
    templates.append("```\n")
    
    templates.append("### 模板 3: 地区企业分析")
    templates.append("```sql")
    templates.append("SELECT ")
    templates.append("    b.注册地址,")
    templates.append("    COUNT(*) as 企业数量,")
    templates.append("    AVG(b.注册资本) as 平均注册资本")
    templates.append("FROM 企业基本信息 b")
    templates.append("WHERE b.注册地址 LIKE '%{地区}%'")
    templates.append("GROUP BY b.注册地址")
    templates.append("```\n")
    
    templates.append("## 场景 4-5: 招商清单/企业尽调\n")
    
    templates.append("### 模板 4: 企业综合信息")
    templates.append("```sql")
    templates.append("SELECT ")
    templates.append("    e.企业名称,")
    templates.append("    e.注册资本,")
    templates.append("    e.成立日期,")
    templates.append("    COUNT(DISTINCT p.专利ID) as 专利数量,")
    templates.append("    COUNT(DISTINCT l.诉讼ID) as 诉讼次数,")
    templates.append("    COUNT(DISTINCT b.投标ID) as 投标次数")
    templates.append("FROM 企业信息 e")
    templates.append("LEFT JOIN 知识产权 p ON e.eid = p.eid COLLATE utf8mb4_unicode_ci")
    templates.append("LEFT JOIN 诉讼信息 l ON e.eid = l.eid COLLATE utf8mb4_unicode_ci")
    templates.append("LEFT JOIN 招投标 b ON e.eid = b.eid COLLATE utf8mb4_unicode_ci")
    templates.append("WHERE e.企业名称 IN ({企业清单})")
    templates.append("GROUP BY e.eid")
    templates.append("```\n")
    
    templates.append("## 重要规则\n")
    templates.append("1. **JOIN 必须使用 COLLATE**: `ON a.eid = b.eid COLLATE utf8mb4_unicode_ci`")
    templates.append("2. **禁止 SELECT ***: 明确指定字段")
    templates.append("3. **时间范围**: 默认近 3 年")
    templates.append("4. **结果限制**: LIMIT 1000")
    templates.append("5. **单个 SELECT**: 不允许多语句")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(templates))
    
    print(f"[OK] SQL 模板已保存到: {output_file}")


def main():
    """主函数"""
    print("=" * 60)
    print("精简 Schema 提取工具")
    print("=" * 60)
    
    # 场景 1-3
    print("\n[1/4] 提取场景 1-3 Schema...")
    db1_config = load_db_config_from_file('scenario_1_3')
    output1 = Path(__file__).parent.parent / "schema_gaaiyun_essential.md"
    extract_essential_schema(db1_config, output1)
    
    # 场景 4-5
    print("\n[2/4] 提取场景 4-5 Schema...")
    db2_config = load_db_config_from_file('scenario_4_5')
    output2 = Path(__file__).parent.parent / "schema_gaaiyun_2_essential.md"
    extract_essential_schema(db2_config, output2)
    
    # SQL 模板
    print("\n[3/4] 生成 SQL 模板...")
    template_output = Path(__file__).parent.parent / "sql_templates.md"
    extract_sql_templates(db1_config, template_output)
    
    # 统计信息
    print("\n[4/4] 统计信息")
    print("-" * 60)
    
    total_size = 0
    for file in [output1, output2, template_output]:
        if file.exists():
            size = file.stat().st_size / 1024
            total_size += size
            print(f"  {file.name}: {size:.1f} KB")
    
    print(f"\n总大小: {total_size:.1f} KB")
    print("=" * 60)
    print("[OK] 完成！")


if __name__ == "__main__":
    main()
