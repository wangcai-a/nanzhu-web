@echo off
chcp 65001 >nul
echo ========================================
echo   Python环境变量设置
echo ========================================
echo.

echo [1/3] 检查Python路径...
if exist "D:\miniconda3\python.exe" (
    echo   ✓ 找到Python: D:\miniconda3\python.exe
) else (
    echo   ✗ 未找到Python！
    pause
    exit /b 1
)

echo.
echo [2/3] 设置当前会话的环境变量...
set PATH=D:\miniconda3;D:\miniconda3\Scripts;D:\miniconda3\Library\bin;%PATH%

echo.
echo [3/3] 验证Python是否可用...
python --version
if errorlevel 1 (
    echo   ✗ Python命令仍然无法识别！
    pause
    exit /b 1
) else (
    echo   ✓ Python可用！
)

echo.
echo ========================================
echo   环境变量设置完成！
echo ========================================
echo.
echo 提示：此设置仅对当前会话有效。
echo.
echo 如需永久设置，请：
echo 1. 右键"此电脑" -^> 属性 -^> 高级系统设置
echo 2. 环境变量 -^> 系统变量 -^> 编辑Path
echo 3. 添加：D:\miniconda3
echo      添加：D:\miniconda3\Scripts
echo      添加：D:\miniconda3\Library\bin
echo.
echo 现在可以在当前窗口使用Python和pip命令了！
echo.
echo 可用的命令：
echo   python --version
echo   pip --version
echo.

cmd /k