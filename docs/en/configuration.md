# Configuration Guide

[中文](/docs/configuration.md) | English

This document details all configuration options for Claude Code Adapter FastAPI.

## 📁 Configuration File

The project supports multiple configuration methods, prioritized as follows:

1. **Configuration File** (`config.yaml`)
2. **Environment Variables**
3. **Default Values**

> 💡 **Tip**: It is recommended to use environment variables for sensitive information like API keys to avoid storing them in plaintext in the configuration file. See the [Security Configuration](#security-configuration) section for details.

## ⚙️ Configuration Options

### Target Service Configuration

| Configuration Item | Environment Variable | Default Value | Description |
|--------------------|---------------------|---------------|-------------|
| `target_base_url` | `TARGET_BASE_URL` | `http://127.0.0.1:1234` | URL of the target model service |
| `target_api_key` | `TARGET_API_KEY` | `key` | API key for the target model service (recommended to set via environment variable) |
| `target_api_key_header` | `TARGET_API_KEY_HEADER` | `Authorization` | Name of the request header for the API key |
| `target_model_config` | `TARGET_MODEL_CONFIG` | Empty | Model configuration parameters (e.g., temperature, max tokens), supports nested JSON structure |

### Client Configuration

| Environment Variable | Description | Example Value |
|---------------------|-------------|---------------|
| `ANTHROPIC_BASE_URL` | **Important**: In the client, configure this environment variable to point to this service's address | `http://localhost:8000` |

### Service Configuration

| Configuration Item | Environment Variable | Default Value | Description |
|--------------------|---------------------|---------------|-------------|
| `host` | `HOST` | `127.0.0.1` | Host address for the service |
| `port` | `PORT` | `8000` | Service port |
| `debug` | `DEBUG` | `false` | Debug mode |
| `log_level` | `LOG_LEVEL` | `INFO` | Logging level |

### System Prompt Configuration

| Configuration Item | Environment Variable | Default Value | Description |
|--------------------|---------------------|---------------|-------------|
| `enable_raw_system_prompt` | `ENABLE_RAW_SYSTEM_PROMPT` | `false` | Whether to enable Claude Code's raw system prompt (recommended to disable, as the raw prompt is lengthy, but enabling may improve context understanding) |
| `enable_custom_system_prompt` | `ENABLE_CUSTOM_SYSTEM_PROMPT` | `true` | Whether to enable a custom system prompt (recommended to enable for better customization) |
| `custom_system_prompt` | `CUSTOM_SYSTEM_PROMPT` | `You are Claude Code.` | Custom system prompt |

### Tool Configuration

| Configuration Item | Environment Variable | Default Value | Description |
|--------------------|---------------------|---------------|-------------|
| `enable_tool_selection` | `ENABLE_TOOL_SELECTION` | `false` | Whether to enable tool selection functionality |
| `tool_selection_base_url` | `TOOL_SELECTION_BASE_URL` | `http://127.0.0.1:1234` | Base URL for the tool selection model service |
| `tool_selection_api_key` | `TOOL_SELECTION_API_KEY` | `key` | API key for the tool selection model service (recommended to set via environment variable) |
| `tool_selection_model_config` | `TOOL_SELECTION_MODEL_CONFIG` | Empty | Model configuration parameters for tool selection (e.g., temperature, max tokens; recommended to use a different model than in `target_model_config` to avoid cache invalidation), supports nested JSON structure |
| `recent_messages_count` | `RECENT_MESSAGES_COUNT` | `5` | Number of recent messages used for tool selection |
| `max_tools_to_select` | `MAX_TOOLS_TO_SELECT` | `3` | Maximum number of tools to select each time |
| `default_tools` | `DEFAULT_TOOLS` | `["Read", "Edit", "Grep"]` | List of default tool names to use if tool selection fails |
| `tool_selection_prompt` | `TOOL_SELECTION_PROMPT` | See below | Tool selection prompt template |
| `tool_use_prompt` | `TOOL_USE_PROMPT` | See below | Tool usage prompt template |
| `tool_selection_model_config` | `TOOL_SELECTION_MODEL_CONFIG` | See below | Model-level configuration parameters (e.g., temperature, max tokens), supports nested JSON structure |

### Tool Definition Handling Strategy

The system automatically selects the tool definition handling method based on the `enable_tool_selection` configuration:

#### 🔧 When Tool Selection is Enabled (`enable_tool_selection: true`)
- **Handling**: Tool definitions are appended as user messages to the message list
- **Advantages**: Avoids system prompt cache invalidation, improves performance
- **Use Cases**: High-performance scenarios requiring dynamic tool selection

#### 📝 When Tool Selection is Disabled (`enable_tool_selection: false`)
- **Handling**: Tool definitions are included in the system prompt
- **Advantages**: Ensures the model is always aware of available tools, maintaining functionality
- **Use Cases**: Scenarios requiring stable tool support

## 📝 Configuration File Example

### config.yaml

```yaml
# Service configuration
host: "127.0.0.1"
port: 8000
debug: false
log_level: "INFO"

# Target service configuration (recommended to override with environment variables)
target_base_url: "http://127.0.0.1:1234/v1"
target_api_key_header: "Authorization"
# Model configuration
target_model_config:
  model: 'qwen3-4b-instruct'
  max_tokens: 4096
  temperature: 0.1

# System prompt configuration
enable_raw_system_prompt: true
enable_custom_system_prompt: false
custom_system_prompt: |
  You are Claude Code.

# Tool configuration
enable_tool_selection: true
tool_selection_base_url: "http://127.0.0.1:1234/v1"
tool_selection_model_config:
  model: "qwen3-4b-instruct_1"
  max_tokens: 1024
  temperature: 0.1
recent_messages_count: 5
max_tools_to_select: 3
default_tools:
  - Read
  - Edit
  - Grep
tool_selection_prompt: |
  Select up to {max_tools} tools from 'Available tools' that best match the user's needs based on recent messages. Only use tool names from 'Available tools', not from messages. Choose tools proactively if they seem relevant. Return a JSON array of tool names, or [] if no tools apply.

  Recent messages: [
  {recent_messages}
  ]

  Available tools: [
  {tools_list}
  ]

tool_use_prompt: |
  You have access to the following tools. The available tools are defined in JSON format below:

  {tools_json}

  When you need to use a tool, respond with JSON in this exact format:

  {
    "type": "tool_use",
    "id": "call_123",
    "name": "ToolName",
    "input": {"param": "value"}
  }


  Use the tools to help complete the user's request.
```

## 🔧 Configuration Management

### Verify Configuration

```bash
# Check environment configuration
python scripts/check_env.py

# Or use Makefile
make check-env
```

### Configuration Hot Reload

The configuration file supports hot reloading, allowing changes to take effect without restarting the service:

```python
from src.claude_code_adapter.config import config_manager

# Reload configuration
config_manager.reload()
```

## 🌍 Environment-Specific Configuration

### Development Environment

```yaml
debug: true
log_level: "DEBUG"
target_base_url: "http://localhost:1234"
```

### Production Environment

```yaml
debug: false
log_level: "WARNING"
host: "0.0.0.0"
port: 8000
```

### Docker Environment

```yaml
host: "0.0.0.0"
target_base_url: "http://host.docker.internal:1234"
```

## Security Configuration

### API Key Management

```bash
# Using environment variables (recommended)
export TARGET_API_KEY="your-secret-key"

# Or using configuration file
# Note: Do not commit configuration files containing keys to version control
```

### Network Security

```yaml
# Restrict access source
host: "127.0.0.1"  # Local access only
# Or
host: "0.0.0.0"    # Allow external access
```

## 📊 Performance Configuration

### Logging Level

```yaml
# Production environment
log_level: "WARNING"

# Development environment
log_level: "DEBUG"
```

## 🐛 Troubleshooting

### Configuration Not Taking Effect

1. Check the configuration file path
2. Validate YAML syntax
3. Confirm environment variable precedence

### Connection Failures

1. Verify target service URL
2. Validate API key
3. Confirm network connectivity

### Permission Issues

1. Check file permissions
2. Verify user permissions
3. Validate firewall settings
