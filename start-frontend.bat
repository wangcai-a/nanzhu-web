@echo off
chcp 65001 >nul
echo ========================================
echo   南竹竹制品管理系统 - 前端服务启动
echo ========================================
echo.

cd /d "%~dp0"

echo 正在启动前端开发服务器...
echo.
echo 前端地址: http://localhost:8080
echo 后端地址: http://localhost:8000
echo.
echo 按 Ctrl+C 停止服务
echo.

python -m http.server 8080

pause