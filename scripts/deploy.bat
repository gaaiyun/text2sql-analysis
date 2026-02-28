@echo off
REM Text2SQL 部署脚本 (Windows)
REM 启动Vanna服务器和API服务器

echo ============================================================
echo Text2SQL 服务部署
echo ============================================================
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo [1/4] 检查依赖...
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo [警告] 缺少依赖，正在安装...
    pip install -r requirements.txt
)

echo [2/4] 启动Vanna服务器 (端口5000)...
start "Vanna Server" cmd /k "python api\vanna_server.py"
timeout /t 3 >nul

echo [3/4] 启动API服务器 (端口8000)...
start "API Server" cmd /k "python api_server.py"
timeout /t 3 >nul

echo [4/4] 健康检查...
timeout /t 5 >nul

curl -s http://localhost:5000/health >nul 2>&1
if errorlevel 1 (
    echo [警告] Vanna服务器未响应
) else (
    echo [成功] Vanna服务器运行正常 (5000)
)

curl -s http://localhost:8000/health >nul 2>&1
if errorlevel 1 (
    echo [警告] API服务器未响应
) else (
    echo [成功] API服务器运行正常 (8000)
)

echo.
echo ============================================================
echo 部署完成！
echo ============================================================
echo Vanna服务: http://localhost:5000
echo API服务: http://localhost:8000
echo.
echo 按任意键退出...
pause >nul
