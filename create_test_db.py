#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
创建测试数据库
"""
import sqlite3

# 连接数据库
conn = sqlite3.connect('test.db')
c = conn.cursor()

# 创建用户表
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    age INTEGER
)
''')

# 创建订单表
c.execute('''
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    product TEXT,
    amount REAL,
    order_date TEXT
)
''')

# 插入测试数据
users = [
    (1, '张三', 'zhangsan@example.com', 25),
    (2, '李四', 'lisi@example.com', 30),
    (3, '王五', 'wangwu@example.com', 28),
]

orders = [
    (1, 1, '笔记本电脑', 5999.00, '2026-02-25'),
    (2, 2, '手机', 3999.00, '2026-02-25'),
    (3, 1, '鼠标', 99.00, '2026-02-26'),
]

c.executemany('INSERT OR REPLACE INTO users VALUES (?, ?, ?, ?)', users)
c.executemany('INSERT OR REPLACE INTO orders VALUES (?, ?, ?, ?, ?)', orders)

conn.commit()
conn.close()

print('[OK] 测试数据库已创建：test.db')
print('[DB] 表结构:')
print('  - users: id, name, email, age')
print('  - orders: id, user_id, product, amount, order_date')
print('[DATA] 测试数据:')
print('  - 3 个用户')
print('  - 3 个订单')
