@echo off
chcp 65001 >nul
echo ========================================
echo   Git推送到远程仓库
echo ========================================
echo.

echo [1/4] 检查远程配置...
"D:\Git\bin\git.exe" remote -v

echo.
echo [2/4] 检查当前状态...
"D:\Git\bin\git.exe" status

echo.
echo [3/4] 尝试推送到远程仓库...
"D:\Git\bin\git.exe" push -u origin main

if errorlevel 1 (
    echo.
    echo ========================================
    echo   推送需要身份验证！
    echo ========================================
    echo.
    echo 请在GitHub上配置以下方式之一：
    echo.
    echo 1. 使用Personal Access Token (推荐)
    echo    - 创建token: https://github.com/settings/tokens/new
    echo    - 权限: repo, workflow
    echo    - 第一次推送时，用户名留空，密码填token
    echo.
    echo 2. 使用SSH密钥
    echo    - 配置SSH密钥后，修改远程地址为：
    echo      git remote set-url origin git@github.com:wangcai-a/nanzhu-web.git
    echo.
    echo ========================================
    pause
    exit /b 1
)

echo.
echo [4/4] 完成！
echo.
echo ========================================
echo   推送成功！
echo ========================================
echo.
echo 访问仓库地址：
echo https://github.com/wangcai-a/nanzhu-web
echo.
pause