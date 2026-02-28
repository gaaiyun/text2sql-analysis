# 🤖 Text2SQL Agent化升级方案

> 基于2024-2025年最新研究，将Text2SQL系统升级为具有自主决策、反思、规划能力的智能Agent

---

## 📋 目录

1. [当前架构分析](#当前架构分析)
2. [Agent化核心能力](#agent化核心能力)
3. [技术选型与架构](#技术选型与架构)
4. [实施路线图](#实施路线图)
5. [关键技术实现](#关键技术实现)
6. [参考资源](#参考资源)

---

## 当前架构分析

### 现有能力
- ✅ 基础Text2SQL转换（LLM + Vanna双引擎）
- ✅ SQL执行和结果获取
- ✅ 数据分析和洞察生成
- ✅ 图表生成（固定逻辑）
- ✅ 网络搜索集成
- ✅ 文档报告生成

### 局限性
- ❌ **无自主决策**：图表类型、是否搜索等由硬编码逻辑决定
- ❌ **无错误恢复**：SQL报错后无法自动修复和重试
- ❌ **无反思能力**：无法评估生成质量并自我改进
- ❌ **无规划能力**：复杂问题无法分解为子任务
- ❌ **无记忆系统**：每次对话独立，无上下文积累
- ❌ **无Python执行**：复杂计算指标无法通过代码实现
- ❌ **报告单一**：格式和内容缺乏多样性

---

## Agent化核心能力

### 1. ReAct循环（Reasoning + Acting）

**能力描述**：Agent通过"思考-行动-观察"循环自主完成任务

```
用户问题：分析广州近三年企业增长趋势

Agent思考：
1. 需要查询企业注册数据（按年份、地区）
2. 可能需要网络搜索了解政策背景
3. 需要生成趋势图和增长率计算
4. 报告需要包含数据+洞察+外部信息

Agent行动序列：
→ 工具1: generate_sql("广州企业注册数量按年统计")
→ 观察: SQL执行成功，获得2021-2023数据
→ 工具2: execute_python("计算同比增长率")
→ 观察: 增长率计算完成
→ 工具3: web_search("广州企业发展政策 2024")
→ 观察: 获取政策信息
→ 工具4: decide_chart_type(data, question)
→ 观察: 推荐折线图+柱状图组合
→ 工具5: generate_report(data, insights, charts)
→ 完成
```

### 2. 错误处理与重试

**SQL错误自动修复**
```python
状态机设计：
生成SQL → 验证语法 → 执行
    ↓ 错误        ↓ 错误     ↓ 错误
  重新生成 ← 注入错误信息 ← 分析错误原因
    ↓
  重试计数 < 3 ? 继续 : 降级处理
```

**重试策略**
- 语法错误：立即重试（最多3次）
- 执行错误：分析错误类型（字段不存在/权限/超时）
- 超时错误：简化查询或采样
- 降级方案：使用Vanna兜底或返回部分结果

### 3. 自主决策系统

**决策点1：是否需要网络搜索**
```python
def should_search(question: str, data_result: dict) -> bool:
    """LLM判断是否需要外部信息"""
    prompt = f"""
    问题：{question}
    数据结果：{data_result}
    
    判断是否需要网络搜索补充信息：
    - 问题涉及外部因素（政策、事件、趋势）？
    - 数据异常需要解释？
    - 需要行业对比？
    
    返回：{{"need_search": true/false, "reason": "..."}}
    """
    return llm_decide(prompt)
```

**决策点2：图表类型选择**
```python
def decide_chart_types(data: pd.DataFrame, question: str) -> List[str]:
    """智能推断最佳图表类型"""
    prompt = f"""
    数据特征：
    - 行数：{len(data)}
    - 列：{data.columns.tolist()}
    - 数据类型：{data.dtypes.to_dict()}
    
    问题：{question}
    
    推荐图表类型（可多选）：
    - 趋势分析 → 折线图
    - 对比分析 → 柱状图
    - 占比分析 → 饼图
    - 分布分析 → 直方图/箱线图
    - 关系分析 → 散点图
    - 地理分析 → 地图
    
    返回：{{"charts": ["line", "bar"], "reason": "..."}}
    """
    return llm_decide(prompt)
```

**决策点3：是否需要二次计算**
```python
def need_secondary_computation(question: str, sql_result: dict) -> dict:
    """判断是否需要Python计算复杂指标"""
    prompt = f"""
    问题：{question}
    SQL结果：{sql_result}
    
    是否需要额外计算：
    - 同比/环比增长率
    - 移动平均
    - 复合指标（如CAGR）
    - 统计检验
    
    返回：{{"need_compute": true/false, "metrics": [...], "code": "..."}}
    """
    return llm_decide(prompt)
```

### 4. 反思与自我改进

**质量评估**
```python
def reflect_on_result(question: str, sql: str, result: dict, analysis: str) -> dict:
    """评估结果质量并提出改进"""
    prompt = f"""
    评估以下结果质量：
    
    问题：{question}
    SQL：{sql}
    结果：{result}
    分析：{analysis}
    
    评分标准：
    1. SQL是否准确回答问题？(0-10)
    2. 数据是否完整？(0-10)
    3. 分析是否深入？(0-10)
    4. 是否需要补充信息？
    
    返回：{{"score": 8.5, "issues": [...], "improvements": [...]}}
    """
    reflection = llm_reflect(prompt)
    
    if reflection["score"] < 7.0:
        # 触发改进流程
        return improve_result(reflection["improvements"])
    
    return reflection
```

### 5. 规划与任务分解

**复杂问题分解**
```python
def plan_task(question: str) -> List[dict]:
    """将复杂问题分解为子任务"""
    prompt = f"""
    问题：{question}
    
    分解为可执行的子任务序列：
    
    示例：
    问题："对比广州和深圳近三年企业增长，分析差异原因"
    
    计划：
    1. 查询广州企业数据（2021-2023）
    2. 查询深圳企业数据（2021-2023）
    3. 计算各自增长率
    4. 网络搜索两地政策差异
    5. 生成对比图表
    6. 综合分析差异原因
    
    返回：[
        {{"task": "query_data", "params": {{"city": "广州"}}}},
        {{"task": "query_data", "params": {{"city": "深圳"}}}},
        ...
    ]
    """
    return llm_plan(prompt)
```

### 6. 记忆系统

**短期记忆（会话内）**
```python
class ConversationMemory:
    def __init__(self):
        self.history = []  # 对话历史
        self.context = {}  # 上下文变量
        
    def add_interaction(self, question, sql, result, analysis):
        self.history.append({
            "question": question,
            "sql": sql,
            "result": result,
            "analysis": analysis,
            "timestamp": datetime.now()
        })
        
    def get_relevant_context(self, current_question):
        """检索相关历史"""
        # 使用embedding相似度检索
        return semantic_search(current_question, self.history)
```

**长期记忆（跨会话）**
```python
class LongTermMemory:
    """持久化用户偏好和领域知识"""
    
    def store_user_preference(self, user_id, preference):
        """存储用户偏好（图表类型、分析深度等）"""
        
    def store_domain_knowledge(self, entity, description):
        """存储领域术语和实体"""
        # 例如："注册资本" → "企业注册时申报的资本总额"
        
    def store_successful_sql(self, question, sql, feedback):
        """存储成功的SQL模式"""
        # 用于Few-shot学习
```

### 7. Python代码执行

**安全沙箱执行**
```python
from agentrun import CodeRunner

class SafePythonExecutor:
    def __init__(self):
        self.runner = CodeRunner(
            timeout=30,
            memory_limit="512MB",
            allowed_imports=["pandas", "numpy", "scipy", "statsmodels"]
        )
    
    def execute(self, code: str, data: dict) -> dict:
        """在隔离环境中执行Python代码"""
        try:
            result = self.runner.run(
                code=code,
                context={"data": data}
            )
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
```

**代码生成示例**
```python
# Agent生成的计算代码
code = """
import pandas as pd
import numpy as np

df = pd.DataFrame(data)

# 计算同比增长率
df['growth_rate'] = df['count'].pct_change() * 100

# 计算CAGR（复合年增长率）
years = len(df)
cagr = (df['count'].iloc[-1] / df['count'].iloc[0]) ** (1/years) - 1

result = {
    'growth_rates': df['growth_rate'].tolist(),
    'cagr': round(cagr * 100, 2)
}
"""

result = executor.execute(code, sql_result)
```

### 8. 多样化报告生成

**报告模板库**
```python
REPORT_TEMPLATES = {
    "executive": "高管摘要（简洁、关键指标、建议）",
    "detailed": "详细分析（完整数据、多维度、深度洞察）",
    "visual": "可视化为主（大图表、少文字）",
    "comparative": "对比分析（多维度对比、差异分析）",
    "trend": "趋势报告（时间序列、预测）"
}

def select_report_template(question: str, data: dict) -> str:
    """根据问题类型选择报告模板"""
    prompt = f"""
    问题：{question}
    数据特征：{data}
    
    选择最合适的报告模板：{list(REPORT_TEMPLATES.keys())}
    """
    return llm_decide(prompt)
```

**动态图标和图片**
```python
def enrich_report_visuals(report_type: str, content: str) -> str:
    """添加多样化的图标和装饰元素"""
    
    icon_library = {
        "trend_up": "📈", "trend_down": "📉",
        "warning": "⚠️", "success": "✅",
        "insight": "💡", "data": "📊",
        "location": "📍", "time": "⏰"
    }
    
    # 根据内容语义插入图标
    # 使用Unsplash API获取相关图片
    # 生成数据驱动的信息图
    
    return enriched_report
```

---

## 技术选型与架构

### 核心框架：LangGraph

**为什么选择LangGraph？**
- ✅ 原生支持ReAct模式
- ✅ 状态机设计，易于错误处理和重试
- ✅ 工具调用和条件路由
- ✅ 检查点机制（支持暂停/恢复）
- ✅ 生产级错误处理

**架构设计**
```python
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor

# 定义Agent状态
class AgentState(TypedDict):
    question: str
    plan: List[dict]
    current_step: int
    sql: str
    sql_result: dict
    python_code: str
    python_result: dict
    search_results: List[dict]
    charts: List[str]
    analysis: str
    report: str
    errors: List[str]
    retry_count: int
    memory: dict

# 构建状态图
workflow = StateGraph(AgentState)

# 添加节点
workflow.add_node("planner", plan_task)
workflow.add_node("sql_generator", generate_sql)
workflow.add_node("sql_executor", execute_sql)
workflow.add_node("error_handler", handle_sql_error)
workflow.add_node("python_executor", execute_python)
workflow.add_node("search_decision", decide_search)
workflow.add_node("web_searcher", search_web)
workflow.add_node("chart_decision", decide_charts)
workflow.add_node("chart_generator", generate_charts)
workflow.add_node("analyzer", analyze_data)
workflow.add_node("reflector", reflect_quality)
workflow.add_node("report_generator", generate_report)

# 添加条件边
workflow.add_conditional_edges(
    "sql_executor",
    lambda state: "error_handler" if state["errors"] else "python_executor"
)

workflow.add_conditional_edges(
    "error_handler",
    lambda state: "sql_generator" if state["retry_count"] < 3 else END
)

workflow.add_conditional_edges(
    "search_decision",
    lambda state: "web_searcher" if state["need_search"] else "chart_decision"
)

# 设置入口和出口
workflow.set_entry_point("planner")
workflow.set_finish_point("report_generator")

# 编译
agent = workflow.compile()
```

### Python沙箱：AgentRun

**安装和配置**
```bash
pip install agentrun
docker pull agentrun/sandbox
```

**集成示例**
```python
from agentrun import CodeRunner

runner = CodeRunner(
    image="agentrun/sandbox:latest",
    timeout=30,
    memory_limit="512MB",
    cpu_limit=1.0
)

# 执行代码
result = runner.run(
    code=generated_code,
    context={"data": sql_result}
)
```

### 记忆系统：Mem0 + ChromaDB

**向量数据库存储**
```python
from chromadb import Client
from chromadb.config import Settings

# 初始化
client = Client(Settings(persist_directory="./memory"))
collection = client.create_collection("text2sql_memory")

# 存储成功案例
collection.add(
    documents=[question],
    metadatas=[{"sql": sql, "success": True}],
    ids=[f"case_{timestamp}"]
)

# 检索相似案例
results = collection.query(
    query_texts=[current_question],
    n_results=3
)
```

### 图表决策：LLM + 规则混合

```python
def intelligent_chart_selection(data, question):
    # 规则层：快速过滤
    rules = ChartRules()
    candidates = rules.filter(data)
    
    # LLM层：语义理解
    if len(candidates) > 1:
        prompt = f"数据：{data}\n问题：{question}\n候选：{candidates}\n选择最佳图表"
        final = llm_select(prompt)
    else:
        final = candidates[0]
    
    return final
```

---

## 实施路线图

### Phase 1: 基础Agent能力（2周）

**目标**：实现ReAct循环和基础工具调用

- [ ] 搭建LangGraph框架
- [ ] 实现工具系统（SQL生成、执行、搜索、图表）
- [ ] 实现简单的决策逻辑（是否搜索、图表类型）
- [ ] 添加基础日志和追踪

**交付物**：
- `src/agent/base_agent.py` - 基础Agent类
- `src/agent/tools.py` - 工具定义
- `demo/agent_demo_basic.py` - 基础演示

### Phase 2: 错误处理与重试（1周）

**目标**：实现健壮的错误恢复机制

- [ ] SQL错误分类和处理
- [ ] 重试策略实现
- [ ] 降级方案（Vanna兜底）
- [ ] 错误日志和监控

**交付物**：
- `src/agent/error_handler.py`
- 测试用例覆盖各类错误场景

### Phase 3: Python代码执行（1周）

**目标**：安全执行LLM生成的Python代码

- [ ] 集成AgentRun沙箱
- [ ] 代码生成提示词优化
- [ ] 安全检查和限制
- [ ] 结果验证

**交付物**：
- `src/agent/python_executor.py`
- 代码执行示例和测试

### Phase 4: 记忆系统（1周）

**目标**：实现短期和长期记忆

- [ ] 会话内上下文管理
- [ ] 向量数据库集成
- [ ] 用户偏好存储
- [ ] 成功案例学习

**交付物**：
- `src/agent/memory.py`
- 记忆检索和更新API

### Phase 5: 反思与规划（1周）

**目标**：实现自我评估和任务分解

- [ ] 质量评估机制
- [ ] 复杂任务分解
- [ ] 多步骤执行
- [ ] 结果改进循环

**交付物**：
- `src/agent/planner.py`
- `src/agent/reflector.py`

### Phase 6: 报告多样化（1周）

**目标**：生成多样化、高质量报告

- [ ] 多种报告模板
- [ ] 动态图标和图片
- [ ] 布局优化
- [ ] 样式定制

**交付物**：
- `src/agent/report_templates/`
- 报告生成示例

### Phase 7: 集成测试与优化（1周）

**目标**：端到端测试和性能优化

- [ ] 完整流程测试
- [ ] 性能基准测试
- [ ] 成本优化（减少LLM调用）
- [ ] 文档完善

**交付物**：
- 完整的Agent系统
- 性能报告
- 使用文档

---

## 关键技术实现

### 1. ReAct提示词模板

```python
REACT_PROMPT = """
你是一个数据分析Agent，通过"思考-行动-观察"循环完成任务。

可用工具：
1. generate_sql(question) - 生成SQL查询
2. execute_sql(sql) - 执行SQL
3. execute_python(code) - 执行Python代码
4. web_search(query) - 网络搜索
5. generate_chart(data, type) - 生成图表
6. finish(report) - 完成任务

格式：
思考：[分析当前情况，决定下一步]
行动：[选择工具和参数]
观察：[工具返回结果]
... (重复直到完成)

问题：{question}

开始！
"""
```

### 2. SQL错误修复提示词

```python
SQL_FIX_PROMPT = """
SQL执行失败，请修复：

原始问题：{question}
生成的SQL：{sql}
错误信息：{error}
数据库Schema：{schema}

常见错误类型：
1. 字段不存在 → 检查Schema
2. 语法错误 → 检查SQL语法
3. 类型不匹配 → 检查数据类型
4. 权限不足 → 简化查询

请生成修复后的SQL：
"""
```

### 3. 图表决策提示词

```python
CHART_DECISION_PROMPT = """
根据数据和问题，决定生成哪些图表：

数据预览：
{data_preview}

数据特征：
- 行数：{row_count}
- 时间列：{time_columns}
- 数值列：{numeric_columns}
- 分类列：{categorical_columns}

问题：{question}

图表类型选择指南：
- 趋势/时间序列 → 折线图
- 对比/排名 → 柱状图
- 占比/构成 → 饼图/堆叠图
- 分布 → 直方图/箱线图
- 关系 → 散点图
- 地理 → 地图

返回JSON：
{{
    "charts": [
        {{"type": "line", "x": "year", "y": "count", "reason": "展示时间趋势"}},
        {{"type": "bar", "x": "city", "y": "count", "reason": "对比不同城市"}}
    ]
}}
"""
```

### 4. Python代码生成提示词

```python
PYTHON_CODE_PROMPT = """
生成Python代码计算以下指标：

数据：{data_description}
需要计算：{metrics}

要求：
1. 使用pandas处理数据
2. 代码简洁高效
3. 包含错误处理
4. 返回dict格式结果

可用库：pandas, numpy, scipy, statsmodels

示例：
```python
import pandas as pd
import numpy as np

df = pd.DataFrame(data)

# 计算同比增长率
df['growth_rate'] = df['value'].pct_change() * 100

result = {{
    'growth_rates': df['growth_rate'].tolist(),
    'avg_growth': df['growth_rate'].mean()
}}
```

请生成代码：
"""
```

### 5. 质量反思提示词

```python
REFLECTION_PROMPT = """
评估以下分析结果的质量：

问题：{question}
SQL：{sql}
数据：{data_summary}
分析：{analysis}
图表：{charts}

评分维度（0-10分）：
1. 准确性：SQL是否正确回答问题？
2. 完整性：数据是否充分？
3. 洞察力：分析是否深入？
4. 可视化：图表是否合适？

返回JSON：
{{
    "scores": {{
        "accuracy": 9,
        "completeness": 8,
        "insight": 7,
        "visualization": 9
    }},
    "overall": 8.25,
    "issues": ["分析可以更深入", "缺少行业对比"],
    "improvements": [
        "添加网络搜索获取行业数据",
        "增加趋势预测"
    ]
}}
"""
```

---

## 参考资源

### 学术论文
1. **AgentSM** (2025) - Semantic Memory for Agentic Text-to-SQL
   - https://arxiv.org/abs/2601.15709
   
2. **MARS-SQL** (2024) - Multi-Agent Reinforcement Learning for Text-to-SQL
   - https://arxiv.org/abs/2511.01008
   
3. **A2P-Vis** (2024) - Analyzer-to-Presenter Pipeline for Visual Insights
   - https://arxiv.org/abs/2512.22101

### 开源项目
1. **LangGraph** - Agent框架
   - https://github.com/langchain-ai/langgraph
   - 文档：https://langchain-ai.github.io/langgraph/
   
2. **AgentRun** - Python沙箱执行
   - https://github.com/tjmlabs/agentrun
   - PyPI：https://pypi.org/project/agentrun/
   
3. **Mem0** - AI记忆层
   - https://github.com/mem0ai/mem0
   
4. **ChartAgent** - 图表理解框架
   - https://arxiv.org/abs/2512.14040

### 技术博客
1. LangGraph错误处理最佳实践
   - https://rangesh.medium.com/error-handling-fundas-langgraph-langchain-fd48e959a8ca
   
2. 生产级SQL Agent构建
   - https://mlnotes.substack.com/p/building-a-production-ready-sql-agent
   
3. Text2SQL长期记忆系统
   - https://text2sql-hub.dev/approaches/text2sql-long-term-memory

### 工具和服务
1. **HopX** - 云端代码沙箱
   - https://hopx.dev/
   
2. **ChromaDB** - 向量数据库
   - https://www.trychroma.com/
   
3. **Unsplash API** - 图片资源
   - https://unsplash.com/developers

---

## 下一步行动

1. **技术验证**（本周）
   - 搭建LangGraph最小可行原型
   - 测试AgentRun沙箱
   - 验证LLM决策能力

2. **架构设计**（下周）
   - 详细设计状态机
   - 定义工具接口
   - 设计数据流

3. **迭代开发**（8周）
   - 按Phase 1-7逐步实现
   - 每周演示和反馈
   - 持续优化

4. **生产部署**
   - 性能测试
   - 安全审计
   - 文档完善

---

Made with ❤️ by gaaiyun
