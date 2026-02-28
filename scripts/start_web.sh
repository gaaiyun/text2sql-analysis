#!/bin/bash
# Text2SQL Web应用启动脚本 (Linux/macOS)

echo "================================================================================"
echo "Text2SQL Web应用启动"
echo "================================================================================"
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未找到Python，请先安装Python 3.8+"
    exit 1
fi

# 检查依赖
echo "[1/3] 检查依赖..."
if ! python3 -c "import gradio" &> /dev/null; then
    echo "[提示] 正在安装Web依赖..."
    pip3 install -r requirements_web.txt
fi

# 检查配置
echo "[2/3] 检查配置..."
if [ ! -f ".env" ]; then
    echo "[错误] 未找到.env文件，请先配置环境变量"
    echo "请复制.env.example为.env并填入真实配置"
    exit 1
fi

# 启动Web应用
echo "[3/3] 启动Web应用..."
echo ""
echo "================================================================================"
echo "Web应用已启动！"
echo "================================================================================"
echo ""
echo "访问地址：http://localhost:7860"
echo ""
echo "按 Ctrl+C 停止服务"
echo "================================================================================"
echo ""

python3 web_app.py
