# LangChain Text2SQL 配置指南

## 环境准备

```bash
pip install langchain langchain-community langchain-core
pip install sqlalchemy
```

## 百炼 API 配置

```python
import os
from langchain_community.llms import Tongyi
from langchain_community.utilities import SQLDatabase
from langchain.chains import SQLDatabaseChain

# 配置百炼 API（从环境变量读取）
llm = Tongyi(
    model_name="qwen-plus",
    dashscope_api_key=os.environ.get("DASHSCOPE_API_KEY", "")
)

# 配置数据库
db = SQLDatabase.from_uri("sqlite:///./test.db")

# 创建 SQLDatabaseChain
chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)
```

## 使用示例

```python
# 执行查询
result = chain.run("查询所有用户的姓名和邮箱")
print(result)
```
