# 配置说明

中文 | [English](/docs/en/configuration.md)

本文档详细说明Claude Code Adapter FastAPI的所有配置选项。

## 📁 配置文件

项目支持多种配置方式，按优先级排序：

1. **配置文件** (`config.yaml`)
2. **环境变量**
3. **默认值**

> 💡 **提示**: 建议使用环境变量管理敏感信息如API密钥，避免在配置文件中明文存储。详见 [安全配置](#安全配置) 部分。

## ⚙️ 配置选项

### 目标服务配置

| 配置项 | 环境变量 | 默认值 | 说明 |
|--------|----------|--------|------|
| `target_base_url` | `TARGET_BASE_URL` | `http://127.0.0.1:1234` | 目标模型服务的URL |
| `target_api_key` | `TARGET_API_KEY` | `key` | 目标模型服务的API密钥（建议配置为环境变量） |
| `target_api_key_header` | `TARGET_API_KEY_HEADER` | `Authorization` | API密钥的请求头名称 |
| `target_model_config` | `TARGET_MODEL_CONFIG` | 空 | 模型的配置参数（可包含温度、最大token等），支持嵌套JSON结构 |

### 客户端配置

| 环境变量 | 说明 | 示例值 |
|----------|------|--------|
| `ANTHROPIC_BASE_URL` | **重要**：在客户端（如Claude Code）中需要配置此环境变量，指向本服务地址 | `http://localhost:8000` |

### 服务配置

| 配置项 | 环境变量 | 默认值 | 说明 |
|--------|----------|--------|------|
| `host` | `HOST` | `127.0.0.1` | 服务绑定的主机地址 |
| `port` | `PORT` | `8000` | 服务端口 |
| `debug` | `DEBUG` | `false` | 调试模式 |
| `log_level` | `LOG_LEVEL` | `INFO` | 日志级别 |

### 系统提示词配置

| 配置项 | 环境变量 | 默认值 | 说明 |
|--------|----------|--------|------|
| `enable_raw_system_prompt` | `ENABLE_RAW_SYSTEM_PROMPT` | `false` | 是否启用Claude Code原始系统提示词（建议禁用，原始提示词较长，但启用可提高上下文理解能力） |
| `enable_custom_system_prompt` | `ENABLE_CUSTOM_SYSTEM_PROMPT` | `true` | 是否启用自定义系统提示词（建议启用，以便更好地满足特定需求） |
| `custom_system_prompt` | `CUSTOM_SYSTEM_PROMPT` | `你是Claude Code。` | 自定义系统提示词 |

### 工具配置

| 配置项                  | 环境变量                | 默认值                                                       | 说明                           |
| ----------------------- | ----------------------- | ------------------------------------------------------------ | ------------------------------ |
| `enable_tool_selection` | `ENABLE_TOOL_SELECTION` | `false`                                                      | 是否启用工具选择功能           |
| `tool_selection_base_url` | `TOOL_SELECTION_BASE_URL` | `http://127.0.0.1:1234`                                  | 工具选择模型服务的基础URL           |
| `tool_selection_api_key` | `TOOL_SELECTION_API_KEY` | `key`                                                      | 工具选择模型服务的API密钥（建议配置为环境变量） |
| `tool_selection_model_config` | `TOOL_SELECTION_MODEL_CONFIG` | 空                                           | 工具选择模型的配置参数（可包含温度、最大token等，建议model配置为与target_model_config中model不同的模型，以避免缓存失效），支持嵌套JSON结构 |
| `recent_messages_count` | `RECENT_MESSAGES_COUNT` | `5`                                                          | 用于工具选择的最近消息数量     |
| `max_tools_to_select`   | `MAX_TOOLS_TO_SELECT`   | `3`                                                          | 每次工具选择最多返回的工具数量 |
| `default_tools`         | `DEFAULT_TOOLS`         | `["Read", "Edit", "Grep"]`                                   | 工具选择失败时使用的默认工具名称列表 |
| `tool_selection_prompt` | `TOOL_SELECTION_PROMPT` | 见下方                                                       | 工具选择提示词模板             |
| `tool_use_prompt`       | `TOOL_USE_PROMPT`       | 见下方                                                       | 工具使用提示词模板             |
| `tool_selection_model_config`     | `TOOL_SELECTION_MODEL_CONFIG`     | 见下方                                                       | 模型级别的配置参数（可包含温度、最大token等），支持嵌套JSON结构 |

### 工具定义处理策略

系统根据 `enable_tool_selection` 配置自动选择工具定义的处理方式：

#### 🔧 启用工具选择时 (`enable_tool_selection: true`)
- **处理方式**: 工具定义作为用户消息追加到消息列表
- **优势**: 避免系统提示词缓存失效，提高性能
- **适用场景**: 需要动态工具选择的高性能场景

#### 📝 未启用工具选择时 (`enable_tool_selection: false`)
- **处理方式**: 工具定义拼接到系统提示词中
- **优势**: 确保模型始终了解可用工具，保证功能完整性
- **适用场景**: 需要稳定工具支持的场景


## 📝 配置文件示例

### config.yaml

```yaml

# 服务配置
host: "127.0.0.1"
port: 8000
debug: false
log_level: "INFO"

# 目标服务配置（建议用环境变量覆盖）
target_base_url: "http://127.0.0.1:1234/v1"
target_api_key_header: "Authorization"
# 模型配置
target_model_config:
  model: 'qwen3-4b-instruct'
  max_tokens: 4096
  temperature: 0.1

# 系统提示词相关配置
enable_raw_system_prompt: true
enable_custom_system_prompt: false
custom_system_prompt: |
  你是Claude Code。

# 工具配置
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

  ```json
  {tools_json}
  ```

  When you need to use a tool, respond with JSON in this exact format:
  ```json
  {
    "type": "tool_use",
    "id": "call_123",
    "name": "ToolName",
    "input": {"param": "value"}
  }
  ```

  Use the tools to help complete the user's request.
```

## 🔧 配置管理

### 验证配置

```bash
# 检查环境配置
python scripts/check_env.py

# 或使用Makefile
make check-env
```

### 配置热重载

配置文件支持热重载，修改后无需重启服务：

```python
from src.claude_code_adapter.config import config_manager

# 重新加载配置
config_manager.reload()
```

## 🌍 环境特定配置

### 开发环境

```yaml
debug: true
log_level: "DEBUG"
target_base_url: "http://localhost:1234"
```

### 生产环境

```yaml
debug: false
log_level: "WARNING"
host: "0.0.0.0"
port: 8000
```

### Docker环境

```yaml
host: "0.0.0.0"
target_base_url: "http://host.docker.internal:1234"
```

## 安全配置

### API密钥管理

```bash
# 使用环境变量（推荐）
export TARGET_API_KEY="your-secret-key"

# 或使用配置文件
# 注意：不要将包含密钥的配置文件提交到版本控制
```

### 网络安全

```yaml
# 限制访问来源
host: "127.0.0.1"  # 仅本地访问
# 或
host: "0.0.0.0"    # 允许外部访问
```

## 📊 性能配置

### 日志级别

```yaml
# 生产环境
log_level: "WARNING"

# 开发环境
log_level: "DEBUG"
```

## 🐛 故障排除

### 配置不生效

1. 检查配置文件路径
2. 验证YAML语法
3. 确认环境变量优先级

### 连接失败

1. 检查目标服务URL
2. 验证API密钥
3. 确认网络连接

### 权限问题

1. 检查文件权限
2. 确认用户权限
3. 验证防火墙设置
