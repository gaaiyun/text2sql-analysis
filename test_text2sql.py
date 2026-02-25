#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Text2SQL 测试脚本
测试 LangChain + 百炼 API 的 Text2SQL 功能
"""
import os
from sqlalchemy import create_engine, text

# 连接数据库
engine = create_engine("sqlite:///./test.db")

print("=" * 50)
print("Text2SQL 测试 - 数据库连接验证")
print("=" * 50)

# 测试数据库连接
with engine.connect() as conn:
    # 查询用户表
    result = conn.execute(text("SELECT * FROM users"))
    users = result.fetchall()
    print("\n[USERS 表]")
    for user in users:
        print(f"  ID={user[0]}, Name={user[1]}, Email={user[2]}, Age={user[3]}")
    
    # 查询订单表
    result = conn.execute(text("SELECT * FROM orders"))
    orders = result.fetchall()
    print("\n[ORDERS 表]")
    for order in orders:
        print(f"  ID={order[0]}, User_ID={order[1]}, Product={order[2]}, Amount={order[3]}, Date={order[4]}")
    
    # 测试 JOIN 查询
    result = conn.execute(text("""
        SELECT u.name, o.product, o.amount 
        FROM users u 
        JOIN orders o ON u.id = o.user_id
    """))
    joins = result.fetchall()
    print("\n[JOIN 查询 - 用户订单]")
    for join in joins:
        print(f"  {join[0]}: {join[1]} (¥{join[2]})")

print("\n" + "=" * 50)
print("数据库连接测试完成！")
print("=" * 50)
