# Claude Code Adapter FastAPI

[![CI/CD Pipeline](https://github.com/wangfumin1/claude-code-adapter-fastapi/actions/workflows/ci.yml/badge.svg)](https://github.com/wangfumin1/claude-code-adapter-fastapi/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

[中文](/README.md) | English

A lightweight proxy/adapter layer based on FastAPI: Converts Anthropic/Claude messages and tool call requests to OpenAI Chat Completions compatible format; intelligently selects tool definition handling strategy (system prompt vs. user message) to optimize performance and functionality; supports optional automatic tool selection, SSE streaming forwarding, and response conversion back to Anthropic format. Provides server-side proxying without modifying client SDKs.

## Features

- 🔧 **Smart Tool Definition Handling**: Automatically selects tool definition placement (system prompt vs. user message) based on configuration to optimize performance and functionality.
- 🔄 **Format Adaptation**: Bidirectional conversion between Anthropic and OpenAI message and tool call formats.
- 🧠 **Automatic Tool Selection (Optional)**: Intelligently selects tools from the tool list based on recent conversation context.
- 📡 **Proxy Forwarding**: Supports both non-streaming and SSE streaming forwarding to target services.
- ⚙️ **Flexible Configuration**: YAML configuration with environment variable overrides and hot-reload support.
- 🐳 **Docker Deployment**: Start with a single command.

## 🚀 Quick Start

### Requirements

- Python 3.9+
- pip or conda

### One-Click Installation

```bash
# Clone the repository
git clone https://github.com/wangfumin1/claude-code-adapter-fastapi.git
cd claude-code-adapter-fastapi

# Windows users
scripts\setup.bat

# Linux/macOS users
./scripts/setup.sh
```

### Start the Service

```bash
# Using Makefile
make run

# Or run directly
python -m uvicorn src.claude_code_adapter.app:app --host 0.0.0.0 --port 8000
```

### Verify Installation

Visit http://localhost:8000/docs to view the API documentation.

### Client Configuration

**Important**: In the client (e.g., Claude Code), configure the environment variable ANTHROPIC_BASE_URL to point to this service:
```bash
export ANTHROPIC_BASE_URL="http://localhost:8000"
```

> 📖 **Detailed Installation Guide**: See [getting-started.md](getting-started.md) for complete installation and configuration instructions.

### Docker Deployment

```bash
# Using docker-compose (recommended)
docker-compose up -d

# Or build manually
docker build -t claude-code-adapter .
docker run -p 8000:8000 -v $(pwd)/config.yaml:/app/config.yaml claude-code-adapter
```

> 🐳 **Docker Details**: See [getting-started.md#docker-deployment](getting-started.md#docker-deployment) for a complete Docker deployment guide.

## Configuration

### Basic Configuration

```yaml
# Target service configuration
target_base_url: "http://127.0.0.1:1234/v1"

# Service configuration
host: "127.0.0.1"
port: 8000
```

### Configure API Key via Environment Variables (Recommended)

```bash
export TARGET_API_KEY="your-secret-key"
```

> ⚙️ **Complete Configuration Guide**: See [configuration.md](configuration.md) for a detailed explanation of all configuration options.

## API Documentation

After starting the service, access the API documentation at:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Main Endpoints

- `GET /health` - Health check
- `POST /v1/messages` - Proxy message requests

> 📚 **Complete API Documentation**: See [api.md](api.md) for detailed API reference documentation.

## Development Guide

### Quick Development

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/ -v

# Code formatting
black src/ tests/
isort src/ tests/
```

> 🛠️ **Detailed Development Guide**: See [development.md](development.md) for complete development environment setup and contribution guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework
- [OpenAI Python](https://github.com/openai/openai-python) - OpenAI API client
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation library

## 📚 Documentation

- [🚀 Quick Start Guide](getting-started.md) - Detailed installation and configuration guide
- [⚙️ Configuration Guide](configuration.md) - Complete configuration options
- [📚 API Documentation](api.md) - Detailed API reference
- [🛠️ Development Guide](development.md) - Development and contribution guide

## 🔗 Related Links

- [📖 Online Documentation](https://wangfumin1.github.io/claude-code-adapter-fastapi)
- [🐙 GitHub Repository](https://github.com/wangfumin1/claude-code-adapter-fastapi)
- [🐛 Issue Tracker](https://github.com/wangfumin1/claude-code-adapter-fastapi/issues)
- [🤝 Contribution Guidelines](CONTRIBUTING.md)
- [🔒 Security Policy](SECURITY.md)

## Support

If you find this project useful, please give it a ⭐️!

For issues or suggestions, submit an [Issue](https://github.com/wangfumin1/claude-code-adapter-fastapi/issues).
