#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Vanna AI API 服务
提供 Text2SQL 查询接口
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 初始化 FastAPI
app = FastAPI(
    title="Text2SQL API",
    description="Vanna AI Text2SQL 查询接口",
    version="1.0.0"
)

# 请求模型
class QueryRequest(BaseModel):
    question: str
    generate_chart: bool = False

class ReportRequest(BaseModel):
    question: str
    template: str = "default"

# 响应模型
class QueryResponse(BaseModel):
    question: str
    sql: str
    data: list
    chart: str = None

# 健康检查
@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "1.0.0"}

# Text2SQL 查询接口
@app.post("/api/vanna/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """
    Text2SQL 查询接口
    
    Args:
        request: QueryRequest (question, generate_chart)
    
    Returns:
        QueryResponse (question, sql, data, chart)
    """
    try:
        # TODO: 集成 Vanna AI
        # import vanna as vn
        # sql = vn.generate_sql(request.question)
        # result = vn.run_sql(sql)
        # chart = vn.generate_plotly_code(result) if request.generate_chart else None
        
        # 模拟响应
        return {
            "question": request.question,
            "sql": "SELECT * FROM enterprises LIMIT 10",
            "data": [
                {"name": "企业 A", "regist_capi": "5000 万", "status": "存续"},
                {"name": "企业 B", "regist_capi": "3000 万", "status": "存续"}
            ],
            "chart": None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 行业报告接口
@app.post("/api/vanna/report")
async def generate_report(request: ReportRequest):
    """
    行业分析报告生成接口
    
    Args:
        request: ReportRequest (question, template)
    
    Returns:
        HTML 报告
    """
    try:
        # TODO: 集成报告生成逻辑
        return {"html": "<h1>行业分析报告</h1>"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
