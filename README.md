# Claude Code Adapter FastAPI

[![CI/CD Pipeline](https://github.com/wangfumin1/claude-code-adapter-fastapi/actions/workflows/ci.yml/badge.svg)](https://github.com/wangfumin1/claude-code-adapter-fastapi/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

中文 | [English](docs/en/README.md)

一个基于 FastAPI 的轻量代理/适配层：将 Anthropic/Claude 的消息与工具调用请求转换为 OpenAI Chat Completions 兼容格式；智能选择工具定义处理策略（系统提示词 vs 用户消息），根据配置自动优化性能和功能完整性；支持可选的自动工具选择、SSE 流式转发，以及将目标模型响应回转为 Anthropic 格式。仅提供服务端代理，不侵入客户端 SDK。

## 功能特性

- 🔧 **智能工具定义处理**: 根据配置自动选择工具定义位置（系统提示词 vs 用户消息），优化性能和功能完整性
- 🔄 **格式适配**: Anthropic ⇄ OpenAI 消息与工具调用格式双向转换
- 🧠 **自动工具选择（可选）**: 基于近期对话上下文从工具列表中智能挑选
- 📡 **代理转发**: 支持非流式与 SSE 流式转发到目标服务
- ⚙️ **灵活配置**: YAML 配置与环境变量覆盖，热重载生效
- 🐳 **Docker 部署**: 一条命令即可启动

## 🚀 快速开始

### 环境要求

- Python 3.9+
- pip 或 conda

### 一键安装

```bash
# 克隆项目
git clone https://github.com/wangfumin1/claude-code-adapter-fastapi.git
cd claude-code-adapter-fastapi

# Windows用户
scripts\setup.bat

# Linux/macOS用户
./scripts/setup.sh
```

### 启动服务

```bash
# 使用Makefile
make run

# 或直接运行
python -m uvicorn src.claude_code_adapter.app:app --host 0.0.0.0 --port 8000
```

### 验证安装

访问 http://localhost:8000/docs 查看API文档

### 客户端配置

**重要**：在客户端（如Claude Code）中需要配置环境变量ANTHROPIC_BASE_URL指向本服务地址：

```bash
export ANTHROPIC_BASE_URL="http://localhost:8000"
```

> 📖 **详细安装指南**: 查看 [docs/getting-started.md](docs/getting-started.md) 获取完整的安装和配置说明。

### Docker部署

```bash
# 使用docker-compose（推荐）
docker-compose up -d

# 或手动构建
docker build -t claude-code-adapter .
docker run -p 8000:8000 -v $(pwd)/config.yaml:/app/config.yaml claude-code-adapter
```

> 🐳 **Docker详细说明**: 查看 [docs/getting-started.md#docker部署](docs/getting-started.md#docker部署) 获取完整的Docker部署指南。

## 配置说明

### 基本配置

```yaml
# 目标服务配置
target_base_url: "http://127.0.0.1:1234/v1"

# 服务配置
host: "127.0.0.1"
port: 8000
```

### 使用环境变量配置KEY（推荐）

```bash
export TARGET_API_KEY="your-secret-key"
```

> ⚙️ **完整配置说明**: 查看 [docs/configuration.md](docs/configuration.md) 获取所有配置选项的详细说明。

## API文档

启动服务后，访问以下地址查看API文档：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 主要端点

- `GET /health` - 健康检查
- `POST /v1/messages` - 代理消息请求

> 📚 **完整API文档**: 查看 [docs/api.md](docs/api.md) 获取详细的API参考文档。

## 开发指南

### 快速开发

```bash
# 安装开发依赖
pip install -r requirements-dev.txt

# 运行测试
pytest tests/ -v

# 代码格式化
black src/ tests/
isort src/ tests/
```

> 🛠️ **详细开发指南**: 查看 [docs/development.md](docs/development.md) 获取完整的开发环境设置和贡献指南。

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 致谢

- [FastAPI](https://fastapi.tiangolo.com/) - 现代、快速的Web框架
- [OpenAI Python](https://github.com/openai/openai-python) - OpenAI API客户端
- [Pydantic](https://pydantic-docs.helpmanual.io/) - 数据验证库

## 📚 文档

- [🚀 快速开始指南](docs/getting-started.md) - 详细的安装和配置指南
- [⚙️ 配置说明](docs/configuration.md) - 完整的配置选项说明
- [📚 API文档](docs/api.md) - 详细的API参考文档
- [🛠️ 开发指南](docs/development.md) - 开发和贡献指南

## 🔗 相关链接

- [📖 在线文档](https://wangfumin1.github.io/claude-code-adapter-fastapi)
- [🐙 GitHub仓库](https://github.com/wangfumin1/claude-code-adapter-fastapi)
- [🐛 问题反馈](https://github.com/wangfumin1/claude-code-adapter-fastapi/issues)
- [🤝 贡献指南](CONTRIBUTING.md)
- [🔒 安全策略](SECURITY.md)

## 支持

如果你觉得这个项目有用，请给它一个 ⭐️！

如有问题或建议，请提交 [Issue](https://github.com/wangfumin1/claude-code-adapter-fastapi/issues)。
