# Detailed Installation Guide

[中文](../getting-started.md) | English

This guide provides detailed instructions for installing and configuring Claude Code Adapter FastAPI.

## 📋 Requirements

- **Python**: 3.9 or higher
- **Package Manager**: pip or conda
- **Operating System**: Windows, macOS, Linux

## 🚀 Installation Methods

### Method 1: Automated Setup (Recommended)

We provide intelligent setup scripts that support multiple environment management methods:

#### Windows Batch Script
```bash
# Clone the repository
git clone https://github.com/wangfumin1/claude-code-adapter-fastapi.git
cd claude-code-adapter-fastapi

# Using venv (default)
scripts\setup.bat

# Using conda
scripts\setup.bat --env conda

# Force reinstall
scripts\setup.bat --force
```

#### Linux/macOS Shell Script
```bash
# Clone the repository
git clone https://github.com/wangfumin1/claude-code-adapter-fastapi.git
cd claude-code-adapter-fastapi

# Using venv (default)
./scripts/setup.sh

# Using conda
./scripts/setup.sh --env conda

# Force reinstall
./scripts/setup.sh --force
```

### Method 2: Manual Setup

If the automated scripts are not suitable, you can set up manually:

#### 1. Create Virtual Environment

**Using venv (Recommended)**:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

**Using conda**:
```bash
# Create conda environment
conda create -n claude-adapter python=3.11

# Activate environment
conda activate claude-adapter
```

**Using virtualenv**:
```bash
# Install virtualenv
pip install virtualenv

# Create virtual environment
virtualenv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

**Using poetry**:
```bash
# Install poetry
curl -sSL https://install.python-poetry.org | python3 -

# Create project environment
poetry install

# Activate environment
poetry shell
```

#### 2. Install Dependencies

```bash
# Production dependencies
pip install -r requirements.txt

# Development dependencies (includes testing and development tools)
pip install -r requirements-dev.txt
```

## Configuration

### 1. Configuration File

The project supports multiple configuration methods, prioritized as follows:

1. Configuration file (`config.yaml`)
2. Environment variables
3. Default values

### 2. Create Configuration File

Edit the `config.yaml` file:

```yaml
# Target service configuration
target_base_url: "http://127.0.0.1:1234"
target_api_key: "your-api-key"
target_api_key_header: "Authorization"

# Service configuration
host: "127.0.0.1"
port: 8000
debug: false
log_level: "INFO"
```

### 3. Environment Variable Configuration

You can also configure via environment variables:

```bash
export TARGET_BASE_URL="http://your-target-service:1234"
export TARGET_API_KEY="your-api-key"
export HOST="0.0.0.0"
export PORT="8000"

# Important: Client configuration
# In the client, set ANTHROPIC_BASE_URL to point to this service
export ANTHROPIC_BASE_URL="http://localhost:8000"
```

## Running

### Development Mode

```bash
python -m uvicorn src.claude_code_adapter.app:app --host 0.0.0.0 --port 8000 --reload
```

### Production Mode

```bash
python -m uvicorn src.claude_code_adapter.app:app --host 0.0.0.0 --port 8000
```

### Using Startup Script

```bash
python scripts/start.py
```

## Verify Installation

### 1. Health Check

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{
  "ok": true,
  "target_base": "http://127.0.0.1:1234"
}
```

### 2. API Documentation

Access the API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Docker Deployment

### 1. Build Image

```bash
docker build -t claude-code-adapter .
```

### 2. Run Container

```bash
docker run -p 8000:8000 -v $(pwd)/config.yaml:/app/config.yaml claude-code-adapter
```

### 3. Using docker-compose

```bash
docker-compose up -d
```

## Test Requests

### Basic Request

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

### Request with Tools

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

## Troubleshooting

### Common Issues

1. **Port Occupied**
   ```bash
   # Check port usage
   netstat -tulpn | grep :8000
   # Or use a different port
   python -m uvicorn src.claude_code_adapter.app:app --port 8001
   ```

2. **Configuration File Not Found**
   - Ensure `config.yaml` is in the project root directory
   - Check file permissions

3. **Target Service Connection Failure**
   - Verify `target_base_url` configuration
   - Ensure the target service is running
   - Check network connectivity

### Logging for Debugging

Set a more detailed log level:

```yaml
log_level: "DEBUG"
```

Or via environment variable:

```bash
export LOG_LEVEL=DEBUG
```

## Next Steps

- [⚙️ Configuration Guide](configuration.md) - Learn about all configuration options
- [📚 API Documentation](api.md) - View detailed API reference
- [🛠️ Development Guide](development.md) - Learn how to contribute code

> 📝 **Related Documentation**: If you encounter issues, refer to the [Troubleshooting](#troubleshooting) section or the debugging section in the [Development Guide](development.md).
