#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
连接 MySQL 数据库，提取 Schema 信息
"""
import pymysql
from sqlalchemy import create_engine, text
import json

# 数据库配置
DB_CONFIG_1 = {
    'host': '8.134.9.77',
    'port': 3306,
    'user': 'Gaaiyun',
    'password': 'Why513338',
    'database': 'Gaaiyun'
}

DB_CONFIG_2 = {
    'host': '8.134.9.77',
    'port': 3306,
    'user': 'gaaiyun_2',
    'password': 'Why513338',
    'database': 'gaaiyun_2'
}

def get_tables_schema(config):
    """获取数据库表结构信息"""
    print(f"\n{'='*60}")
    print(f"连接数据库：{config['database']} @ {config['host']}")
    print(f"{'='*60}\n")
    
    try:
        # 连接数据库
        connection = pymysql.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database=config['database']
        )
        
        cursor = connection.cursor()
        
        # 获取所有表名
        cursor.execute("""
            SELECT TABLE_NAME, TABLE_COMMENT 
            FROM information_schema.TABLES 
            WHERE TABLE_SCHEMA = %s
            ORDER BY TABLE_NAME
        """, (config['database'],))
        
        tables = cursor.fetchall()
        print(f"找到 {len(tables)} 个表\n")
        
        schema_info = {}
        
        # 获取每个表的字段信息
        for table_name, table_comment in tables:
            print(f"[TABLE] {table_name} - {table_comment or '无注释'}")
            
            cursor.execute("""
                SELECT 
                    COLUMN_NAME,
                    COLUMN_TYPE,
                    IS_NULLABLE,
                    COLUMN_KEY,
                    COLUMN_DEFAULT,
                    COLUMN_COMMENT
                FROM information_schema.COLUMNS
                WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
                ORDER BY ORDINAL_POSITION
            """, (config['database'], table_name))
            
            columns = cursor.fetchall()
            
            schema_info[table_name] = {
                'comment': table_comment,
                'columns': []
            }
            
            for col in columns:
                col_info = {
                    'name': col[0],
                    'type': col[1],
                    'nullable': col[2],
                    'key': col[3],
                    'default': col[4],
                    'comment': col[5]
                }
                schema_info[table_name]['columns'].append(col_info)
                print(f"  - {col[0]}: {col[1]} {'NULL' if col[2]=='YES' else 'NOT NULL'} {col[3] or ''} {col[5] or ''}")
            
            print()
        
        cursor.close()
        connection.close()
        
        return schema_info
        
    except Exception as e:
        print(f"[ERROR] 连接失败：{e}")
        return None

def save_schema(schema_info, filename):
    """保存 Schema 到 Markdown 文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# 数据库 Schema 文档\n\n")
        f.write(f"**数据库**: {filename.split('_')[1]}\n")
        f.write(f"**生成时间**: 2026-02-26\n\n")
        f.write(f"---\n\n")
        
        for table_name, info in schema_info.items():
            f.write(f"## 📊 表：{table_name}\n\n")
            f.write(f"**注释**: {info['comment'] or '无'}\n\n")
            f.write("| 字段名 | 类型 | 可空 | 键 | 默认值 | 注释 |\n")
            f.write("|--------|------|------|-----|--------|------|\n")
            
            for col in info['columns']:
                key_str = col['key'] if col['key'] else ''
                default_str = str(col['default']) if col['default'] is not None else 'NULL'
                f.write(f"| {col['name']} | {col['type']} | {col['nullable']} | {key_str} | {default_str} | {col['comment'] or ''} |\n")
            
            f.write(f"\n")
    
    print(f"[OK] Schema 已保存到：{filename}")

if __name__ == '__main__':
    print("[START] 开始提取数据库 Schema...\n")
    
    # 提取场景 1-3 数据库
    print("\n" + "="*60)
    print("场景 1-3: 数据洞察/地区分析/行业分析")
    print("="*60)
    schema1 = get_tables_schema(DB_CONFIG_1)
    if schema1:
        save_schema(schema1, 'schema_gaaiyun.md')
    
    # 提取场景 4-5 数据库
    print("\n" + "="*60)
    print("场景 4-5: 招商清单/企业尽调")
    print("="*60)
    schema2 = get_tables_schema(DB_CONFIG_2)
    if schema2:
        save_schema(schema2, 'schema_gaaiyun_2.md')
    
    print("\n" + "="*60)
    print("[OK] Schema 提取完成！")
    print("="*60)
