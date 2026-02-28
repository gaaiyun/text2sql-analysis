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
    scenario: Optional[str] = "data_insight"
    database: Optional[str] = "scenario_1_3"


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


# 全局配置
_config = None
_vanna_initialized = False
_current_database = None


def load_config():
    """加载配置"""
    global _config
    if not CONFIG_PATH.exists():
        logger.warning(f"配置文件不存在：{CONFIG_PATH}")
        return None
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        _config = json.load(f)
    return _config


def init_vanna(database_key="scenario_1_3"):
    """初始化 Vanna AI"""
    global _vanna_initialized, _current_database
    
    if not _config:
        load_config()
    
    if not _config:
        return False
    
    try:
        vanna_config = _config.get('vanna', {})
        db_config = _config.get('database', {}).get(database_key, {})
        
        # 初始化 Vanna
        vn.api_key = vanna_config.get('api_key', '')
        vn.org = vanna_config.get('org', 'gaaiyun')
        
        # 连接数据库
        vn.connect_to_mysql(
            host=db_config.get('host', 'localhost'),
            database=db_config.get('database', ''),
            user=db_config.get('user', ''),
            password=db_config.get('password', ''),
            port=db_config.get('port', 3306)
        )
        
        _vanna_initialized = True
        _current_database = database_key
        logger.info(f"Vanna AI 初始化成功，数据库：{database_key}")
        return True
        
    except Exception as e:
        logger.error(f"Vanna 初始化失败：{e}")
        return False


def switch_database(database_key):
    """切换数据库"""
    return init_vanna(database_key)


@app.on_event("startup")
async def startup_event():
    """应用启动时初始化"""
    init_vanna()


@app.get("/")
async def root():
    """根路径"""
    return {
        "service": "Vanna AI Text2SQL Service",
        "version": "1.0.0",
        "endpoints": ["/health", "/api/v0/generate_sql", "/api/v0/train"]
    }


@app.get("/health")
async def health():
    """健康检查"""
    return {
        "status": "ok" if _vanna_initialized else "initializing",
        "service": "Vanna AI Service",
        "version": "1.0.0",
        "vanna_initialized": _vanna_initialized,
        "current_database": _current_database
    }


@app.post("/api/v0/generate_sql", response_model=SQLResponse)
async def generate_sql(request: SQLRequest):
    """
    生成 SQL 查询（n8n工作流调用）
    
    Args:
        request: SQL 生成请求
        
    Returns:
        SQLResponse: 生成的 SQL 语句
    """
    # 根据场景切换数据库
    if request.database and request.database != _current_database:
        logger.info(f"切换数据库：{_current_database} -> {request.database}")
        switch_database(request.database)
    
    if not _vanna_initialized:
        logger.error("Vanna AI 未初始化")
        raise HTTPException(
            status_code=503,
            detail="Vanna AI 服务未就绪，请检查配置"
        )
    
    try:
        logger.info(f"收到 SQL 生成请求：{request.question} (场景: {request.scenario})")
        
        # 使用 Vanna 生成 SQL
        sql = vn.generate_sql(request.question)
        
        logger.info(f"SQL 生成成功：{sql[:100]}...")
        
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
