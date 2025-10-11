@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM 解析命令行参数
set "ENV_TYPE=venv"
set "FORCE=false"
set "ENV_NAME=claude-adapter"

:parse_args
if "%~1"=="" goto :start_setup
if "%~1"=="--env" (
    set "ENV_TYPE=%~2"
    shift
    shift
    goto :parse_args
)
if "%~1"=="--force" (
    set "FORCE=true"
    shift
    goto :parse_args
)
shift
goto :parse_args

:start_setup
echo 🚀 Claude Code Adapter FastAPI 快速设置
echo ================================================
echo 环境类型: %ENV_TYPE%

REM 检查环境管理工具
if "%ENV_TYPE%"=="conda" (
    call conda --version >nul 2>&1
    if errorlevel 1 (
        echo ❌ conda未安装，请先安装Anaconda或Miniconda
        echo 或使用venv: scripts\setup.bat --env venv
        pause
        exit /b 1
    )
    echo ✅ conda已安装
) else (
    echo ✅ 使用venv创建虚拟环境
)

REM 创建环境
echo.
echo 🔧 开始创建环境...
echo 当前环境类型: %ENV_TYPE%

if "%ENV_TYPE%"=="conda" (
    echo 🔧 创建conda环境 '%ENV_NAME%'...

    REM 检查环境是否已存在
    echo 检查conda环境是否已存在...
    call conda env list | findstr "%ENV_NAME%" >nul 2>&1
    if not errorlevel 1 (
        if "%FORCE%"=="false" (
            echo ℹ️ conda环境 '%ENV_NAME%' 已存在，跳过创建
            goto :activate_env
        ) else (
            echo 🔄 强制重新创建conda环境...
            call conda env remove -n %ENV_NAME% -y >nul 2>&1
        )
    )

    echo 正在创建conda环境...
    call conda create -n %ENV_NAME% python=3.11 -y
    if errorlevel 1 (
        echo ❌ conda环境创建失败
        pause
        exit /b 1
    )
    echo ✅ conda环境 '%ENV_NAME%' 创建成功
) else (
    echo 🔧 创建虚拟环境...

    REM 检查Python是否可用
    python --version >nul 2>&1
    if errorlevel 1 (
        echo ❌ 未检测到Python，请安装Python 3.11+并将其加入PATH
        echo 可从 https://www.python.org/downloads/ 下载
        pause
        exit /b 1
    )

    REM 检查虚拟环境是否已存在
    if exist venv (
        if "%FORCE%"=="false" (
            echo ℹ️ 虚拟环境已存在，跳过创建
            goto :activate_env
        ) else (
            echo 🔄 强制重新创建虚拟环境...
            rmdir /s /q venv >nul 2>&1
        )
    )

    echo 正在创建虚拟环境...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ 虚拟环境创建失败
        pause
        exit /b 1
    )
    echo ✅ 虚拟环境创建成功
)

:activate_env
REM 激活环境
echo.
echo 🔄 激活环境...
if "%ENV_TYPE%"=="conda" (
    echo 正在激活conda环境 '%ENV_NAME%'...
    call conda activate "%ENV_NAME%"
    if errorlevel 1 (
        echo ❌ conda环境激活失败
        pause
        exit /b 1
    )
    echo ✅ conda环境激活成功
) else (
    echo 正在激活虚拟环境...
    if not exist venv\Scripts\activate.bat (
        echo ❌ 虚拟环境激活脚本不存在
        pause
        exit /b 1
    )
    call venv\Scripts\activate.bat
    if errorlevel 1 (
        echo ❌ 虚拟环境激活失败
        pause
        exit /b 1
    )
    echo ✅ 虚拟环境激活成功
)

REM 升级pip
echo.
echo ⬆️ 升级pip...
call python -m pip install --upgrade pip
if errorlevel 1 (
    echo ⚠️ pip升级失败，继续安装依赖...
)

REM 安装依赖
echo.
echo 📥 安装项目依赖...
if not exist requirements.txt (
    echo ❌ 未找到 requirements.txt 文件
    pause
    exit /b 1
)
echo 正在安装依赖包，请稍候...
call pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ 依赖安装失败
    echo 请检查网络连接和requirements.txt文件内容
    pause
    exit /b 1
)
echo ✅ 依赖安装成功

:end
echo.
echo ================================================
echo 🎉 设置完成！
echo.
echo 📋 下一步操作：
if "%ENV_TYPE%"=="conda" (
    echo 1. 激活conda环境: conda activate %ENV_NAME%
) else (
    echo 1. 激活虚拟环境: venv\Scripts\activate
)
echo 2. 编辑配置文件: config.yaml
echo 3. 启动服务: make run
echo 4. 或直接运行: python -m uvicorn src.claude_code_adapter.app:app --host 0.0.0.0 --port 8000
echo.
echo 📚 更多信息请查看: docs/getting-started.md
echo.
