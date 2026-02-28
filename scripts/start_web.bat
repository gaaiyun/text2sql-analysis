@echo off
REM Text2SQL Web应用启动脚本 (Windows)

echo ================================================================================
echo Text2SQL Web应用启动
echo ================================================================================
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

REM 检查依赖
echo [1/3] 检查依赖...
pip show gradio >nul 2>&1
if errorlevel 1 (
    echo [提示] 正在安装Web依赖...
    pip install -r requirements_web.txt
)

REM 检查配置
echo [2/3] 检查配置...
if not exist ".env" (
    echo [错误] 未找到.env文件，请先配置环境变量
    echo 请复制.env.example为.env并填入真实配置
    pause
    exit /b 1
)

REM 启动Web应用
echo [3/3] 启动Web应用...
echo.
echo ================================================================================
echo Web应用已启动！
echo ================================================================================
echo.
echo 访问地址：http://localhost:7860
echo.
echo 按 Ctrl+C 停止服务
echo ================================================================================
echo.

python web_app.py

pause
