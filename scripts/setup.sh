#!/bin/bash

# 设置UTF-8编码
if ! locale -a | grep -q "zh_CN.utf8"; then
    export LANG=en_US.UTF-8
    export LC_ALL=en_US.UTF-8
else
    export LANG=zh_CN.UTF-8
    export LC_ALL=zh_CN.UTF-8
fi

# 解析命令行参数
ENV_TYPE="venv"
FORCE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --env)
            ENV_TYPE="$2"
            shift 2
            ;;
        --force)
            FORCE=true
            shift
            ;;
        *)
            shift
            ;;
    esac
done

echo "🚀 Claude Code Adapter FastAPI 快速设置"
echo "================================================"
echo "环境类型: $ENV_TYPE"

# 检查环境管理工具
if [ "$ENV_TYPE" = "conda" ]; then
    if ! command -v conda &> /dev/null; then
        echo "❌ conda未安装，请先安装Anaconda或Miniconda"
        echo "或使用venv: ./scripts/setup.sh --env venv"
        exit 1
    fi
    echo "✅ conda已安装"
    conda --version
else
    echo "✅ 使用venv创建虚拟环境"
fi

if [ "$ENV_TYPE" = "venv" ]; then
# 检查Python是否安装
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python3未安装"
        echo "请先安装Python 3.9或更高版本"
        exit 1
    fi
    echo "✅ Python已安装"
    python3 --version
fi

if [ "$ENV_TYPE" = "venv" ]; then
# 检查Python版本
    python_version=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    required_version="3.9"

    if [ "$(printf '%s\n' "$python_version" "$required_version" | sort -V | head -n1)" != "$required_version" ]; then
        echo "❌ Python版本过低: $python_version"
        echo "需要Python $required_version或更高版本"
        exit 1
    fi

fi
# 创建环境
echo ""
if [ "$ENV_TYPE" = "conda" ]; then
    ENV_NAME="claude-adapter"
    echo "🔧 创建conda环境 '$ENV_NAME'..."

    # 检查环境是否已存在
    if conda env list | grep -q "$ENV_NAME" && [ "$FORCE" = false ]; then
        echo "ℹ️ conda环境 '$ENV_NAME' 已存在，跳过创建"
    else
        conda create -n $ENV_NAME python=3.11 -y
        if [ $? -ne 0 ]; then
            echo "❌ conda环境创建失败"
            exit 1
        fi
        echo "✅ conda环境 '$ENV_NAME' 创建成功"
    fi
else
    echo "🔧 创建虚拟环境..."

    # 检查虚拟环境是否已存在
    if [ -d "venv" ] && [ "$FORCE" = false ]; then
        echo "ℹ️ 虚拟环境已存在，跳过创建"
    else
        python3 -m venv venv
        if [ $? -ne 0 ]; then
            echo "❌ 虚拟环境创建失败"
            exit 1
        fi
        echo "✅ 虚拟环境创建成功"
    fi
fi

# 激活环境
echo ""
if [ "$ENV_TYPE" = "conda" ]; then
    echo "🔄 激活conda环境..."
    eval "$(conda shell.bash hook)"
    conda activate $ENV_NAME
else
    echo "🔄 激活虚拟环境..."
    source venv/bin/activate
fi

# 升级pip
echo "⬆️ 升级pip..."
python -m pip install --upgrade pip

# 安装依赖
echo "📥 安装项目依赖..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ 依赖安装失败"
    exit 1
fi
echo "✅ 依赖安装成功"

echo ""
echo "================================================"
echo "🎉 设置完成！"
echo ""
echo "📋 下一步操作："
if [ "$ENV_TYPE" = "conda" ]; then
    echo "1. 激活conda环境: conda activate $ENV_NAME"
else
    echo "1. 激活虚拟环境: source venv/bin/activate"
fi
echo "2. 编辑配置文件: config.yaml"
echo "3. 启动服务: make run"
echo "4. 或直接运行: python -m uvicorn src.claude_code_adapter.app:app --host 0.0.0.0 --port 8000"
echo ""
echo "📚 更多信息请查看: docs/getting-started.md"
echo ""
