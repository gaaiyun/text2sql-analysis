#!/bin/bash
# Text2SQL 部署脚本 (Linux/macOS)
# 启动Vanna服务器和API服务器

echo "============================================================"
echo "Text2SQL 服务部署"
echo "============================================================"
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未找到Python3，请先安装Python 3.8+"
    exit 1
fi

echo "[1/4] 检查依赖..."
if ! python3 -c "import fastapi" &> /dev/null; then
    echo "[警告] 缺少依赖，正在安装..."
    pip3 install -r requirements.txt
fi

echo "[2/4] 启动Vanna服务器 (端口5000)..."
nohup python3 api/vanna_server.py > logs/vanna_server.log 2>&1 &
VANNA_PID=$!
echo "Vanna PID: $VANNA_PID"
sleep 3

echo "[3/4] 启动API服务器 (端口8000)..."
nohup python3 api_server.py > logs/api_server.log 2>&1 &
API_PID=$!
echo "API PID: $API_PID"
sleep 3

echo "[4/4] 健康检查..."
sleep 5

if curl -s http://localhost:5000/health > /dev/null; then
    echo "[成功] Vanna服务器运行正常 (5000)"
else
    echo "[警告] Vanna服务器未响应"
fi

if curl -s http://localhost:8000/health > /dev/null; then
    echo "[成功] API服务器运行正常 (8000)"
else
    echo "[警告] API服务器未响应"
fi

echo ""
echo "============================================================"
echo "部署完成！"
echo "============================================================"
echo "Vanna服务: http://localhost:5000 (PID: $VANNA_PID)"
echo "API服务: http://localhost:8000 (PID: $API_PID)"
echo ""
echo "停止服务: kill $VANNA_PID $API_PID"
echo "查看日志: tail -f logs/*.log"
