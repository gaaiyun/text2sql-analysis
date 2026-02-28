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

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn
import os
from dotenv import load_dotenv

# 导入限流中间件
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

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

# 初始化限流器
# 限制规则：默认 100 次/分钟，可自定义
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

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
# Schema 和 Few-shot 示例路径
# ============================================================================
SCHEMA_DIR = Path(__file__).parent / "schema"
SCHEMA_FILES = {
    "scenario_1_3": SCHEMA_DIR / "gaaiyun_schema.md",
    "scenario_4_5": SCHEMA_DIR / "gaaiyun_2_schema.md",
}
EXAMPLES_FILE = SCHEMA_DIR / "question_sql_examples.md"

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
        db_config = get_db_config_with_fallback('scenario_1_3') if CONFIG_PATH.exists() else get_database_config('scenario_1_3')
        if not db_config.get('host') or not db_config.get('database'):
            logger.warning("数据库配置不完整，跳过 Vanna 连接")
            return False

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


def get_db_config_with_fallback(scenario: str) -> dict:
    """获取数据库配置，若 Config 未提供则从 config.json 读取对应 scenario"""
    cfg = get_database_config(scenario)
    if cfg.get("database") and cfg.get("host") and cfg.get("host") != "localhost":
        return {**cfg, "charset": "utf8mb4"}
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            db = (data.get("database") or {}).get(scenario, {})
            if db.get("host"):
                return {
                    "host": db.get("host", "localhost"),
                    "port": int(db.get("port", 3306)),
                    "user": db.get("user", ""),
                    "password": db.get("password", ""),
                    "database": db.get("database", ""),
                    "charset": "utf8mb4",
                }
        except Exception as e:
            logger.warning(f"从 config.json 读取数据库配置失败: {e}")
    return {**cfg, "charset": "utf8mb4"}


def load_schema_for_scenario(scenario: str) -> str:
    """加载场景对应的Schema文档"""
    try:
        if scenario in ["investment", "due_diligence"]:
            schema_file = SCHEMA_FILES["scenario_4_5"]
        else:
            schema_file = SCHEMA_FILES["scenario_1_3"]
        
        if schema_file.exists():
            with open(schema_file, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            logger.warning(f"Schema文件不存在: {schema_file}")
            return ""
    except Exception as e:
        logger.error(f"加载Schema失败: {e}")
        return ""


def load_sql_examples(scenario: str, limit: int = 5) -> str:
    """加载场景对应的Few-shot SQL示例"""
    try:
        if not EXAMPLES_FILE.exists():
            logger.warning(f"示例文件不存在: {EXAMPLES_FILE}")
            return ""
        
        with open(EXAMPLES_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 根据场景提取对应的示例
        scenario_map = {
            "data_insight": "场景1：数据洞察",
            "regional": "场景2：地区产业分析",
            "industry": "场景3：行业分析",
            "investment": "场景4：招商清单",
            "due_diligence": "场景5：企业尽调"
        }
        
        scenario_title = scenario_map.get(scenario, "场景1：数据洞察")
        
        # 简单提取：找到场景标题后的内容
        if scenario_title in content:
            start = content.find(scenario_title)
            # 找到下一个场景标题或文件结尾
            next_scenario = content.find("## 场景", start + len(scenario_title))
            if next_scenario == -1:
                next_scenario = content.find("## 通用规则", start)
            if next_scenario == -1:
                next_scenario = len(content)
            
            examples = content[start:next_scenario]
            # 限制示例数量（每个示例约100-200行）
            return examples[:3000]  # 限制长度
        
        return ""
    except Exception as e:
        logger.error(f"加载SQL示例失败: {e}")
        return ""


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


def generate_sql_llm(question: str, schema: str, scenario: str = "data_insight") -> str:
    """使用 LLM 生成 SQL（基于详细Schema + Few-shot示例）"""
    
    # 加载场景对应的Schema和Few-shot示例
    detailed_schema = load_schema_for_scenario(scenario)
    examples = load_sql_examples(scenario)
    
    # 如果加载失败，使用传入的schema
    if not detailed_schema:
        detailed_schema = schema[:3000]
    
    prompt = f"""你是SQL专家。根据Schema和示例生成准确的MySQL查询语句。

## Schema
{detailed_schema[:2000]}

## Few-shot示例
{examples[:2000]}

## 问题
{question}

## 规则（必须遵守）
1. 只返回一条SELECT语句，不要解释、不要Markdown代码块
2. JOIN必须使用COLLATE: ON a.eid = b.eid COLLATE utf8mb4_unicode_ci
3. 禁止SELECT *，明确指定字段
4. 时间范围默认近3年: WHERE date >= DATE_SUB(CURDATE(), INTERVAL 3 YEAR)
5. 结果限制: LIMIT 1000
6. 单个SELECT语句，不允许多语句
7. NULL处理: 使用COALESCE(field, default)
8. 去重统计: 使用COUNT(DISTINCT eid)

## 固化SOP（根据场景）
场景1-数据洞察：
1. 识别意图（融资趋势/行业分布/地区分析）
2. 从对应表获取字段（融资数据.round_date, amount / 企业行业代码.name）
3. 使用LEFT JOIN关联，必须COLLATE
4. 按维度分组，计算COUNT/SUM/AVG
5. ORDER BY + LIMIT

场景4-招商清单：
1. 从企业信息表获取基本信息（企业名称、注册资本、成立日期）
2. LEFT JOIN专利信息、诉讼信息、招投标等表
3. 计算各维度指标（专利数量、诉讼次数、投标次数）
4. 使用CASE WHEN实现评分逻辑
5. WHERE企业名称 IN (用户清单)

SQL:"""

    response = _llm_client.chat.completions.create(
        model="qwen-plus",
        messages=[
            {"role": "system", "content": "你是SQL专家，擅长根据Schema和示例生成准确的MySQL查询语句。严格遵守规则，不要添加解释。"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,
        temperature=0.2
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
    """执行 SQL 并返回结果（含 charset 与错误详情）"""
    try:
        # 确保连接参数完整（charset 避免中文乱码）
        conn_params = {k: v for k, v in db_config.items() if k in ("host", "port", "user", "password", "database", "charset")}
        if "charset" not in conn_params:
            conn_params["charset"] = "utf8mb4"
        conn = pymysql.connect(**conn_params)
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
async def root(request: Request):
    """健康检查"""
    return {
        "status": "ok",
        "service": "Text2SQL API",
        "version": "1.1.0",
        "vanna_initialized": _vanna_initialized,
        "llm_initialized": _llm_client is not None
    }


@app.get("/health")
async def health(request: Request):
    """健康检查"""
    return {
        "status": "ok",
        "vanna": _vanna_initialized,
        "llm": _llm_client is not None
    }


@app.post("/api/query", response_model=QueryResponse)
@limiter.limit("100/minute")
async def query(request: Request, query_request: QueryRequest):
    """
    Text2SQL 查询接口

    支持三种模式：
    - auto: 自动选择 Vanna 或 LLM
    - vanna: 强制使用 Vanna
    - llm: 强制使用 LLM

    Args:
        query_request: QueryRequest (question, mode, scenario, generate_chart)

    Returns:
        QueryResponse (question, sql, data, columns, row_count, chart, mode, error)
    """
    logger.info(f"收到查询请求：{query_request.question} (mode={query_request.mode})")

    try:
        # 确定数据库配置（支持从 config.json 回退）
        if query_request.scenario in ["investment", "due_diligence"]:
            db_config = get_db_config_with_fallback("scenario_4_5")
        else:
            db_config = get_db_config_with_fallback("scenario_1_3")

        sql = ""
        mode = query_request.mode

        # 模式选择：LLM为主，Vanna兜底
        if query_request.mode == "auto":
            if _llm_client:
                mode = "llm"
            elif _vanna_initialized:
                mode = "vanna"
            else:
                raise HTTPException(status_code=503, detail="LLM和Vanna服务均未就绪")

        # 1) 优先使用 LLM 生成 SQL
        if mode == "llm":
            if not _llm_client:
                # LLM不可用，尝试Vanna兜底
                if _vanna_initialized:
                    mode = "vanna"
                    logger.warning("LLM服务未就绪，切换到Vanna兜底")
                else:
                    raise HTTPException(status_code=503, detail="LLM服务未就绪")
            else:
                try:
                    # 获取 Schema
                    schema = get_schema(db_config)
                    
                    # 使用 LLM 生成 SQL（带Schema和Few-shot示例）
                    sql = generate_sql_llm(query_request.question, schema, query_request.scenario)
                    logger.info(f"LLM 生成 SQL: {sql[:100]}...")
                except Exception as e:
                    logger.error(f"LLM生成SQL失败: {e}")
                    # LLM失败，尝试Vanna兜底
                    if _vanna_initialized:
                        mode = "vanna"
                        logger.warning("LLM生成失败，切换到Vanna兜底")
                    else:
                        raise

        # 2) Vanna 兜底
        if not sql and mode == "vanna":
            if not _vanna_initialized:
                raise HTTPException(status_code=503, detail="Vanna 服务未就绪")

            try:
                # 使用 Vanna 生成 SQL
                sql = vn.generate_sql(query_request.question)
                logger.info(f"Vanna 生成 SQL: {sql[:100]}...")
            except Exception as e:
                logger.error(f"Vanna生成SQL失败: {e}")
                raise HTTPException(status_code=500, detail=f"SQL生成失败: {str(e)}")

        if not sql:
            raise HTTPException(status_code=400, detail="未能生成 SQL，请重试或更换问题描述")

        # 执行 SQL
        result = execute_sql(sql, db_config)

        if not result["success"]:
            raise HTTPException(status_code=400, detail=f"SQL 执行失败：{result['error']}")

        # 生成图表（可选）
        chart = None
        if query_request.generate_chart and result["data"]:
            try:
                # 简单的 ASCII 图表
                chart = generate_ascii_chart(result["data"], result["columns"])
            except Exception as e:
                logger.warning(f"图表生成失败：{e}")

        return QueryResponse(
            question=query_request.question,
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
        logger.error(f"查询失败：{e}", exc_info=True)
        return QueryResponse(
            question=query_request.question,
            sql="",
            data=[],
            columns=[],
            row_count=0,
            mode=query_request.mode,
            error=str(e),
        )


@app.post("/api/query/llm", response_model=QueryResponse)
@limiter.limit("100/minute")
async def query_llm(request: Request, query_request: QueryRequest):
    """
    使用 LLM 生成 SQL 并查询

    Args:
        query_request: QueryRequest

    Returns:
        QueryResponse
    """
    query_request.mode = "llm"
    return await query(request, query_request)


@app.post("/api/query/vanna", response_model=QueryResponse)
@limiter.limit("100/minute")
async def query_vanna(request: Request, query_request: QueryRequest):
    """
    使用 Vanna 生成 SQL 并查询

    Args:
        query_request: QueryRequest

    Returns:
        QueryResponse
    """
    query_request.mode = "vanna"
    return await query(request, query_request)


@app.post("/api/search", response_model=SearchResponse)
@limiter.limit("60/minute")
async def search(request: Request, search_request: SearchRequest):
    """
    网络搜索接口

    Args:
        request: SearchRequest (query, num_results)

    Returns:
        SearchResponse (query, results, count)
    """
    try:
        from src.utils.web_search import search as web_search

        results = web_search(
            query=search_request.query,
            max_results=search_request.num_results,
        )
        return SearchResponse(
            query=search_request.query,
            results=results,
            count=len(results),
        )
    except ImportError:
        raise HTTPException(status_code=501, detail="网络搜索模块未安装")
    except Exception as e:
        logger.error(f"搜索失败：{e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/export/excel", response_model=ExportResponse)
@limiter.limit("30/minute")
async def export_excel(request: Request, export_request: ExportRequest):
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
@limiter.limit("30/minute")
async def export_word(request: Request, export_request: ExportRequest):
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
@limiter.limit("30/minute")
async def generate_report(request: Request, report_request: ReportRequest):
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
@limiter.limit("20/minute")
async def train_model(request: Request, train_request: TrainRequest):
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
@limiter.limit("60/minute")
async def get_schema_endpoint(request: Request):
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
