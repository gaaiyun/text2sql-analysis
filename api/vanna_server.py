"""
Vanna AI API Server
Text2SQL Analysis System - Vanna API 服务

提供 RESTful API 接口，供 n8n 工作流调用生成 SQL
"""

import json
import logging
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import vanna as vn

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Text2SQL API",
    description="Vanna AI Text2SQL 生成服务",
    version="0.1.0"
)

# 配置路径
CONFIG_PATH = Path(__file__).parent.parent / "config.json"


class SQLRequest(BaseModel):
    """SQL 生成请求"""
    question: str
    scenario: Optional[str] = "数据洞察"
    session_id: Optional[str] = None


class SQLResponse(BaseModel):
    """SQL 生成响应"""
    sql: str
    question: str
    scenario: str
    confidence: float = 1.0
    error: Optional[str] = None


class TrainRequest(BaseModel):
    """训练请求"""
    ddl: Optional[str] = None
    sql: Optional[str] = None
    document: Optional[str] = None


# 全局 Vanna 实例
_vanna_initialized = False


def init_vanna():
    """初始化 Vanna AI"""
    global _vanna_initialized
    
    if not CONFIG_PATH.exists():
        logger.warning(f"配置文件不存在：{CONFIG_PATH}")
        return False
    
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        vanna_config = config.get('vanna', {})
        db_config = config.get('database', {}).get('scenario_1_3', {})
        
        # 初始化 Vanna
        vn.api_key = vanna_config.get('api_key', '')
        vn.org = vanna_config.get('org', 'default')
        
        # 连接数据库
        vn.connect_to_mysql(
            host=db_config.get('host', 'localhost'),
            database=db_config.get('database', ''),
            user=db_config.get('user', ''),
            password=db_config.get('password', '')
        )
        
        _vanna_initialized = True
        logger.info("Vanna AI 初始化成功")
        return True
        
    except Exception as e:
        logger.error(f"Vanna 初始化失败：{e}")
        return False


@app.on_event("startup")
async def startup_event():
    """应用启动时初始化"""
    init_vanna()


@app.get("/")
async def root():
    """健康检查"""
    return {
        "status": "ok",
        "service": "Text2SQL API",
        "version": "0.1.0",
        "vanna_initialized": _vanna_initialized
    }


@app.post("/api/v0/generate_sql", response_model=SQLResponse)
async def generate_sql(request: SQLRequest):
    """
    生成 SQL 查询
    
    Args:
        request: SQL 生成请求
        
    Returns:
        SQLResponse: 生成的 SQL 语句
    """
    if not _vanna_initialized:
        logger.error("Vanna AI 未初始化")
        raise HTTPException(
            status_code=503,
            detail="Vanna AI 服务未就绪，请检查配置"
        )
    
    try:
        logger.info(f"收到 SQL 生成请求：{request.question}")
        
        # 使用 Vanna 生成 SQL
        sql = vn.generate_sql(request.question)
        
        logger.info(f"SQL 生成成功：{sql}")
        
        return SQLResponse(
            sql=sql,
            question=request.question,
            scenario=request.scenario,
            confidence=1.0
        )
        
    except Exception as e:
        logger.error(f"SQL 生成失败：{e}")
        return SQLResponse(
            sql="",
            question=request.question,
            scenario=request.scenario,
            confidence=0.0,
            error=str(e)
        )


@app.post("/api/v0/train")
async def train_model(request: TrainRequest):
    """
    训练 Vanna 模型
    
    Args:
        request: 训练请求（DDL/SQL/文档）
        
    Returns:
        dict: 训练结果
    """
    if not _vanna_initialized:
        raise HTTPException(status_code=503, detail="Vanna AI 服务未就绪")
    
    try:
        if request.ddl:
            status = vn.train(ddl=request.ddl)
            logger.info(f"DDL 训练成功：{status}")
            return {"status": "success", "type": "ddl", "training_id": status}
        
        elif request.sql:
            status = vn.train(sql=request.sql)
            logger.info(f"SQL 训练成功：{status}")
            return {"status": "success", "type": "sql", "training_id": status}
        
        elif request.document:
            status = vn.train(document=request.document)
            logger.info(f"文档训练成功：{status}")
            return {"status": "success", "type": "document", "training_id": status}
        
        else:
            raise HTTPException(status_code=400, detail="至少需要提供 DDL、SQL 或文档之一")
            
    except Exception as e:
        logger.error(f"训练失败：{e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v0/schema")
async def get_schema():
    """获取数据库 Schema"""
    if not _vanna_initialized:
        raise HTTPException(status_code=503, detail="Vanna AI 服务未就绪")
    
    try:
        # 获取 DDL
        ddl = vn.get_training_data()
        return {"status": "success", "schema": ddl}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
