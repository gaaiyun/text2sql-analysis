#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Text2SQL API Server
提供 Text2SQL 查询、报告生成、可视化等接口

功能：
- Text2SQL 查询（Vanna AI + LLM 双模式）
- 网络搜索
- Excel/Word 导出
- 可视化图表生成

使用方法:
    python api_server.py

API 端点:
    GET  /health                 - 健康检查
    POST /api/query              - Text2SQL 查询
    POST /api/query/llm          - LLM 模式生成 SQL
    POST /api/search             - 网络搜索
    POST /api/export/excel       - Excel 导出
    POST /api/export/word        - Word 导出
    POST /api/report             - 报告生成
"""
import json
import logging
from pathlib import Path
from typing import Optional, List, Any
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn
import os
from dotenv import load_dotenv

# 导入 Vanna
import vanna as vn

# 导入配置模块
import sys
sys.path.insert(0, str(Path(__file__).parent))
from src.utils.config import get_kiro_config, get_database_config
from openai import OpenAI
import pymysql

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 初始化 FastAPI
app = FastAPI(
    title="Text2SQL API",
    description="Text2SQL 查询接口 - 支持 Vanna AI 和 LLM 双模式",
    version="1.1.0"
)

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 配置路径
CONFIG_PATH = Path(__file__).parent / "config.json"

# ============================================================================
# 请求/响应模型
# ============================================================================

class QueryRequest(BaseModel):
    """查询请求"""
    question: str = Field(..., description="自然语言问题")
    mode: str = Field(default="auto", description="模式：auto/vanna/llm")
    scenario: str = Field(default="data_insight", description="场景：data_insight/regional/industry/investment/due_diligence")
    generate_chart: bool = Field(default=False, description="是否生成图表")

class QueryResponse(BaseModel):
    """查询响应"""
    question: str
    sql: str
    data: List[Any] = Field(default_factory=list)
    columns: List[str] = Field(default_factory=list)
    row_count: int = 0
    chart: Optional[str] = None
    mode: str = "auto"
    error: Optional[str] = None

class SearchRequest(BaseModel):
    """搜索请求"""
    query: str = Field(..., description="搜索关键词")
    num_results: int = Field(default=5, description="返回结果数量")

class SearchResponse(BaseModel):
    """搜索响应"""
    query: str
    results: List[dict] = Field(default_factory=list)
    count: int = 0

class ExportRequest(BaseModel):
    """导出请求"""
    question: str
    format: str = Field(default="excel", description="格式：excel/word")
    filename: Optional[str] = None

class ExportResponse(BaseModel):
    """导出响应"""
    status: str
    filename: str
    filepath: str
    message: str

class ReportRequest(BaseModel):
    """报告生成请求"""
    question: str
    template: str = Field(default="default", description="模板：default/investment/due_diligence")
    include_chart: bool = Field(default=True, description="是否包含图表")

class ReportResponse(BaseModel):
    """报告响应"""
    status: str
    title: str
    content: str
    filepath: Optional[str] = None

class TrainRequest(BaseModel):
    """训练请求"""
    ddl: Optional[str] = None
    sql: Optional[str] = None
    document: Optional[str] = None

class TrainResponse(BaseModel):
    """训练响应"""
    status: str
    type: str
    training_id: Optional[str] = None
    message: str

# ============================================================================
# 全局状态
# ============================================================================

_vanna_initialized = False
_llm_client = None

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
        db_config = get_database_config('scenario_1_3')

        # 初始化 Vanna
        vn.api_key = vanna_config.get('api_key', '')
        vn.org = vanna_config.get('org', 'gaaiyun')

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


def init_llm():
    """初始化 LLM 客户端"""
    global _llm_client

    try:
        kiro_config = get_kiro_config()
        _llm_client = OpenAI(
            base_url=kiro_config["base_url"],
            api_key=kiro_config["api_key"]
        )
        logger.info("LLM 客户端初始化成功")
        return True
    except Exception as e:
        logger.error(f"LLM 客户端初始化失败：{e}")
        return False


def get_schema(db_config: dict, limit: int = 10) -> str:
    """获取数据库 Schema"""
    try:
        conn = pymysql.connect(**db_config)
        cur = conn.cursor()

        cur.execute("""
            SELECT table_name, table_comment
            FROM information_schema.tables
            WHERE table_schema = %s
        """, (db_config["database"],))

        tables = cur.fetchall()
        schema = []

        for table_name, comment in tables[:limit]:
            cur.execute(f"SHOW CREATE TABLE `{table_name}`")
            create_sql = cur.fetchone()[1]
            schema.append(f"-- {comment or table_name}\n{create_sql}")

        conn.close()
        return "\n\n".join(schema)
    except Exception as e:
        return f"ERROR: {e}"


def generate_sql_llm(question: str, schema: str) -> str:
    """使用 LLM 生成 SQL"""
    prompt = f"""你是 SQL 专家。基于以下数据库表结构，为问题生成 MySQL 查询语句。

表结构：
{schema[:5000]}

问题：{question}

要求：
1. 只返回 SQL 语句，不要解释
2. SQL 必须是有效的 MySQL 语法
3. 使用合适的 JOIN 和聚合函数
4. 添加必要的 WHERE 条件

SQL:"""

    response = _llm_client.chat.completions.create(
        model="qwen-plus",
        messages=[
            {"role": "system", "content": "你是 SQL 专家，擅长生成准确的 MySQL 查询语句。"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.3
    )

    sql = response.choices[0].message.content.strip()

    # 清理 Markdown 代码块
    for prefix in ["```sql", "```"]:
        if sql.startswith(prefix):
            sql = sql[len(prefix):]
    if sql.endswith("```"):
        sql = sql[:-3]

    return sql.strip()


def execute_sql(sql: str, db_config: dict) -> dict:
    """执行 SQL 并返回结果"""
    try:
        conn = pymysql.connect(**db_config)
        cur = conn.cursor()
        cur.execute(sql)
        results = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        conn.close()
        return {
            "success": True,
            "row_count": len(results),
            "columns": columns,
            "data": [dict(zip(columns, row)) for row in results[:100]]
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# ============================================================================
# API 端点
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """应用启动时初始化"""
    init_vanna()
    init_llm()


@app.get("/")
async def root():
    """健康检查"""
    return {
        "status": "ok",
        "service": "Text2SQL API",
        "version": "1.1.0",
        "vanna_initialized": _vanna_initialized,
        "llm_initialized": _llm_client is not None
    }


@app.get("/health")
async def health():
    """健康检查"""
    return {
        "status": "ok",
        "vanna": _vanna_initialized,
        "llm": _llm_client is not None
    }


@app.post("/api/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """
    Text2SQL 查询接口

    支持三种模式：
    - auto: 自动选择 Vanna 或 LLM
    - vanna: 强制使用 Vanna
    - llm: 强制使用 LLM

    Args:
        request: QueryRequest (question, mode, scenario, generate_chart)

    Returns:
        QueryResponse (question, sql, data, columns, row_count, chart, mode, error)
    """
    logger.info(f"收到查询请求：{request.question} (mode={request.mode})")

    try:
        # 确定数据库配置
        if request.scenario in ["investment", "due_diligence"]:
            db_config = get_database_config('scenario_4_5')
        else:
            db_config = get_database_config('scenario_1_3')

        sql = ""
        mode = request.mode

        # 模式选择
        if request.mode == "auto":
            # 自动选择：优先 Vanna，失败则使用 LLM
            if _vanna_initialized:
                mode = "vanna"
            else:
                mode = "llm"

        if mode == "vanna":
            if not _vanna_initialized:
                raise HTTPException(status_code=503, detail="Vanna 服务未就绪")

            # 使用 Vanna 生成 SQL
            sql = vn.generate_sql(request.question)
            logger.info(f"Vanna 生成 SQL: {sql}")

        elif mode == "llm":
            if not _llm_client:
                raise HTTPException(status_code=503, detail="LLM 服务未就绪")

            # 获取 Schema
            schema = get_schema(db_config)

            # 使用 LLM 生成 SQL
            sql = generate_sql_llm(request.question, schema)
            logger.info(f"LLM 生成 SQL: {sql}")

        # 执行 SQL
        result = execute_sql(sql, db_config)

        if not result["success"]:
            raise HTTPException(status_code=400, detail=f"SQL 执行失败：{result['error']}")

        # 生成图表（可选）
        chart = None
        if request.generate_chart and result["data"]:
            try:
                # 简单的 ASCII 图表
                chart = generate_ascii_chart(result["data"], result["columns"])
            except Exception as e:
                logger.warning(f"图表生成失败：{e}")

        return QueryResponse(
            question=request.question,
            sql=sql,
            data=result["data"],
            columns=result["columns"],
            row_count=result["row_count"],
            chart=chart,
            mode=mode
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"查询失败：{e}")
        return QueryResponse(
            question=request.question,
            sql="",
            data=[],
            columns=[],
            row_count=0,
            mode=request.mode,
            error=str(e)
        )


@app.post("/api/query/llm", response_model=QueryResponse)
async def query_llm(request: QueryRequest):
    """
    使用 LLM 生成 SQL 并查询

    Args:
        request: QueryRequest

    Returns:
        QueryResponse
    """
    request.mode = "llm"
    return await query(request)


@app.post("/api/query/vanna", response_model=QueryResponse)
async def query_vanna(request: QueryRequest):
    """
    使用 Vanna 生成 SQL 并查询

    Args:
        request: QueryRequest

    Returns:
        QueryResponse
    """
    request.mode = "vanna"
    return await query(request)


@app.post("/api/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    """
    网络搜索接口

    Args:
        request: SearchRequest (query, num_results)

    Returns:
        SearchResponse (query, results, count)
    """
    try:
        from scripts.web_search import duckduckgo_search

        results = duckduckgo_search(request.query, max_results=request.num_results)

        return SearchResponse(
            query=request.query,
            results=results,
            count=len(results)
        )
    except ImportError:
        raise HTTPException(status_code=501, detail="网络搜索模块未安装")
    except Exception as e:
        logger.error(f"搜索失败：{e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/export/excel", response_model=ExportResponse)
async def export_excel(request: ExportRequest):
    """
    Excel 导出接口

    Args:
        request: ExportRequest (question, format, filename)

    Returns:
        ExportResponse (status, filename, filepath, message)
    """
    try:
        from scripts.export_excel import export_to_excel

        # 生成查询
        query_request = QueryRequest(question=request.question)
        response = await query(query_request)

        if response.error:
            raise HTTPException(status_code=400, detail=response.error)

        # 导出 Excel
        filename = request.filename or f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        filepath = export_to_excel(response.data, filename)

        return ExportResponse(
            status="success",
            filename=filename,
            filepath=filepath,
            message=f"Excel 导出成功：{filepath}"
        )
    except ImportError:
        raise HTTPException(status_code=501, detail="Excel 导出模块未安装")
    except Exception as e:
        logger.error(f"Excel 导出失败：{e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/export/word", response_model=ExportResponse)
async def export_word(request: ExportRequest):
    """
    Word 导出接口

    Args:
        request: ExportRequest (question, format, filename)

    Returns:
        ExportResponse (status, filename, filepath, message)
    """
    try:
        from scripts.export_word import export_to_word

        # 生成查询
        query_request = QueryRequest(question=request.question)
        response = await query(query_request)

        if response.error:
            raise HTTPException(status_code=400, detail=response.error)

        # 导出 Word
        filename = request.filename or f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
        filepath = export_to_word(response.data, request.question, filename)

        return ExportResponse(
            status="success",
            filename=filename,
            filepath=filepath,
            message=f"Word 导出成功：{filepath}"
        )
    except ImportError:
        raise HTTPException(status_code=501, detail="Word 导出模块未安装")
    except Exception as e:
        logger.error(f"Word 导出失败：{e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/report", response_model=ReportResponse)
async def generate_report(request: ReportRequest):
    """
    行业分析报告生成接口

    Args:
        request: ReportRequest (question, template, include_chart)

    Returns:
        ReportResponse (status, title, content, filepath)
    """
    try:
        # 生成查询
        query_request = QueryRequest(
            question=request.question,
            generate_chart=request.include_chart
        )
        query_response = await query(query_request)

        if query_response.error:
            raise HTTPException(status_code=400, detail=query_response.error)

        # 生成报告内容
        title = request.question
        content = f"""# {title}

## 查询结果

共查询到 {query_response.row_count} 条记录。

### SQL 语句
```sql
{query_response.sql}
```

### 数据摘要
"""

        # 添加数据摘要
        for row in query_response.data[:5]:
            content += f"- {row}\n"

        if query_response.chart:
            content += f"\n### 图表\n\n{query_response.chart}\n"

        # 保存报告
        filepath = f"reports/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        Path("reports").mkdir(exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        return ReportResponse(
            status="success",
            title=title,
            content=content,
            filepath=filepath
        )
    except Exception as e:
        logger.error(f"报告生成失败：{e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/train", response_model=TrainResponse)
async def train_model(request: TrainRequest):
    """
    训练 Vanna 模型

    Args:
        request: TrainRequest (ddl, sql, document)

    Returns:
        TrainResponse (status, type, training_id, message)
    """
    if not _vanna_initialized:
        raise HTTPException(status_code=503, detail="Vanna 服务未就绪")

    try:
        if request.ddl:
            status = vn.train(ddl=request.ddl)
            logger.info(f"DDL 训练成功：{status}")
            return TrainResponse(
                status="success",
                type="ddl",
                training_id=status,
                message="DDL 训练成功"
            )

        elif request.sql:
            status = vn.train(sql=request.sql)
            logger.info(f"SQL 训练成功：{status}")
            return TrainResponse(
                status="success",
                type="sql",
                training_id=status,
                message="SQL 训练成功"
            )

        elif request.document:
            status = vn.train(document=request.document)
            logger.info(f"文档训练成功：{status}")
            return TrainResponse(
                status="success",
                type="document",
                training_id=status,
                message="文档训练成功"
            )

        else:
            raise HTTPException(
                status_code=400,
                detail="至少需要提供 DDL、SQL 或文档之一"
            )

    except Exception as e:
        logger.error(f"训练失败：{e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/schema")
async def get_schema_endpoint():
    """获取数据库 Schema"""
    if not _vanna_initialized:
        raise HTTPException(status_code=503, detail="Vanna 服务未就绪")

    try:
        ddl = vn.get_training_data()
        return {"status": "success", "schema": ddl}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# 工具函数
# ============================================================================

def generate_ascii_chart(data: List[dict], columns: List[str]) -> str:
    """生成简单的 ASCII 图表"""
    if not data:
        return "无数据"

    # 尝试找到数值列
    numeric_col = None
    label_col = None

    for col in columns:
        for row in data:
            val = row.get(col)
            if isinstance(val, (int, float)):
                numeric_col = col
                break
        if numeric_col:
            label_col = columns[0] if columns[0] != col else (columns[1] if len(columns) > 1 else col)
            break

    if not numeric_col:
        return "无合适数据生成图表"

    # 生成条形图
    max_val = max(row.get(numeric_col, 0) for row in data[:10])
    chart_width = 40

    lines = [f"图表：{label_col} vs {numeric_col}", "=" * (chart_width + 20)]

    for row in data[:10]:
        label = row.get(label_col, "Unknown")
        val = row.get(numeric_col, 0)
        bar_len = int((val / max_val) * chart_width) if max_val > 0 else 0
        bar = "█" * bar_len
        lines.append(f"{str(label)[:15]:15} | {bar} {val}")

    return "\n".join(lines)


# ============================================================================
# 主程序
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Text2SQL API Server v1.1.0")
    print("=" * 60)
    print("启动服务...")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
