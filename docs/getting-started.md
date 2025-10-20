# 详细安装指南

中文 | [English](/docs/en/getting-started.md)

本指南提供Claude Code Adapter FastAPI的详细安装和配置说明。

## 📋 环境要求

- **Python**: 3.9 或更高版本
- **包管理器**: pip 或 conda
- **操作系统**: Windows, macOS, Linux

## 🚀 安装方式

### 方式一：自动设置（推荐）

我们提供了智能设置脚本，支持多种环境管理方式：

#### Windows批处理脚本
```bash
# 克隆项目
git clone https://github.com/wangfumin1/claude-code-adapter-fastapi.git
cd claude-code-adapter-fastapi

# 使用venv（默认）
scripts\setup.bat

# 使用conda
scripts\setup.bat --env conda

# 强制重新安装
scripts\setup.bat --force
```

#### Linux/macOS Shell脚本
```bash
# 克隆项目
git clone https://github.com/wangfumin1/claude-code-adapter-fastapi.git
cd claude-code-adapter-fastapi

# 使用venv（默认）
./scripts/setup.sh

# 使用conda
./scripts/setup.sh --env conda

# 强制重新安装
./scripts/setup.sh --force
```


### 方式二：手动设置

如果自动脚本不适用，可以手动设置：

#### 1. 创建虚拟环境

**使用venv（推荐）**：
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

**使用conda**：
```bash
# 创建conda环境
conda create -n claude-adapter python=3.11

# 激活环境
conda activate claude-adapter
```

**使用virtualenv**：
```bash
# 安装virtualenv
pip install virtualenv

# 创建虚拟环境
virtualenv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

**使用poetry**：
```bash
# 安装poetry
curl -sSL https://install.python-poetry.org | python3 -

# 创建项目环境
poetry install

# 激活环境
poetry shell
```

#### 2. 安装依赖

```bash
# 生产依赖
pip install -r requirements.txt

# 开发依赖（包含测试和开发工具）
pip install -r requirements-dev.txt
```

## 配置

### 1. 配置文件

项目支持多种配置方式，按优先级排序：

1. 配置文件 (`config.yaml`)
2. 环境变量
3. 默认值

### 2. 创建配置文件

编辑 `config.yaml` 文件：

```yaml
# 目标服务配置
target_base_url: "http://127.0.0.1:1234"
target_api_key: "your-api-key"
target_api_key_header: "Authorization"

# 服务配置
host: "127.0.0.1"
port: 8000
debug: false
log_level: "INFO"
```

### 3. 环境变量配置

您也可以通过环境变量配置：

```bash
export TARGET_BASE_URL="http://your-target-service:1234"
export TARGET_API_KEY="your-api-key"
export HOST="0.0.0.0"
export PORT="8000"

# 重要：客户端配置
# 在客户端需要将ANTHROPIC_BASE_URL指向本服务地址
export ANTHROPIC_BASE_URL="http://localhost:8000"
```

## 运行

### 开发模式

```bash
python -m uvicorn src.claude_code_adapter.app:app --host 0.0.0.0 --port 8000 --reload
```

### 生产模式

```bash
python -m uvicorn src.claude_code_adapter.app:app --host 0.0.0.0 --port 8000
```

### 使用启动脚本

```bash
python scripts/start.py
```

## 验证安装

### 1. 健康检查

```bash
curl http://localhost:8000/health
```

预期响应：

```json
{
  "ok": true,
  "target_base": "http://127.0.0.1:1234"
}
```

### 2. API文档

访问以下地址查看API文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Docker部署

### 1. 构建镜像

```bash
docker build -t claude-code-adapter .
```

### 2. 运行容器

```bash
docker run -p 8000:8000 -v $(pwd)/config.yaml:/app/config.yaml claude-code-adapter
```

### 3. 使用docker-compose

```bash
docker-compose up -d
```

## 测试请求

### 基本请求

```bash
curl -X POST "http://localhost:8000/v1/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "test-model",
    "messages": [
      {
        "role": "user",
        "content": "Hello, how are you?"
      }
    ]
  }'
```

### 带工具的请求

```bash
curl -X POST "http://localhost:8000/v1/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "test-model",
    "messages": [
      {
        "role": "user",
        "content": "What is the weather like?"
      }
    ],
    "tools": [
      {
        "name": "get_weather",
        "description": "Get current weather information",
        "input_schema": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "The city name"
            }
          },
          "required": ["location"]
        }
      }
    ]
  }'
```

## 故障排除

### 常见问题

1. **端口被占用**
   ```bash
   # 检查端口使用情况
   netstat -tulpn | grep :8000
   # 或使用其他端口
   python -m uvicorn src.claude_code_adapter.app:app --port 8001
   ```

2. **配置文件未找到**
   - 确保 `config.yaml` 文件在项目根目录
   - 检查文件权限

3. **目标服务连接失败**
   - 检查 `target_base_url` 配置
   - 确保目标服务正在运行
   - 检查网络连接

### 日志调试

设置更详细的日志级别：

```yaml
log_level: "DEBUG"
```

或在环境变量中：

```bash
export LOG_LEVEL=DEBUG
```

## 下一步

- [⚙️ 配置说明](configuration.md) - 了解所有配置选项
- [📚 API文档](api.md) - 查看详细的API参考
- [🛠️ 开发指南](development.md) - 学习如何贡献代码

> 📝 **相关文档**: 如果遇到问题，请查看 [故障排除](#故障排除) 部分或参考 [开发指南](development.md) 中的调试部分。
