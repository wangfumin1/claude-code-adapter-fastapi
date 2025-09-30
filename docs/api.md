# API文档

本文档详细说明Claude Code Adapter FastAPI的API接口。

## 🌐 基础信息

- **Base URL**: `http://localhost:8000`
- **API版本**: v1
- **内容类型**: `application/json`

## 📋 端点列表

### 健康检查

#### GET /health

检查服务健康状态。

**响应示例**:
```json
{
  "ok": true,
  "target_base": "http://127.0.0.1:1234"
}
```

**状态码**:
- `200 OK`: 服务正常

### 消息代理

#### POST /v1/messages

代理消息请求到目标服务，支持工具调用。

**请求体**:
```json
{
  "model": "string",
  "messages": [
    {
      "role": "user|assistant|system",
      "content": "string|object|array"
    }
  ],
  "max_tokens": 4096,
  "temperature": 0.1,
  "stream": false,
  "system": "string",
  "tools": [
    {
      "name": "string",
      "description": "string",
      "input_schema": {
        "type": "object",
        "properties": {},
        "required": []
      }
    }
  ]
}
```

**响应示例**:

**非流式响应**:
```json
{
  "id": "msg_1234567890",
  "type": "message",
  "role": "assistant",
  "model": "target-model",
  "stop_reason": "end_turn|tool_use",
  "stop_sequence": null,
  "usage": {
    "input_tokens": 100,
    "output_tokens": 50
  },
  "content": [
    {
      "type": "text",
      "text": "Hello! How can I help you?"
    }
  ]
}
```

**工具调用响应**:
```json
{
  "id": "msg_1234567890",
  "type": "message",
  "role": "assistant",
  "model": "target-model",
  "stop_reason": "tool_use",
  "stop_sequence": null,
  "usage": {
    "input_tokens": 100,
    "output_tokens": 50
  },
  "content": [
    {
      "type": "text",
      "text": "I'll help you with that."
    },
    {
      "type": "tool_use",
      "id": "call_123",
      "name": "get_weather",
      "input": {
        "location": "Beijing"
      }
    }
  ]
}
```

**流式响应**:
```
data: {"id": "msg_123", "object": "chat.completion.chunk", "choices": [{"delta": {"content": "Hello"}}]}

data: {"id": "msg_123", "object": "chat.completion.chunk", "choices": [{"delta": {"content": "!"}}]}

data: [DONE]
```

**状态码**:
- `200 OK`: 请求成功
- `400 Bad Request`: 请求格式错误
- `500 Internal Server Error`: 服务器内部错误
- `502 Bad Gateway`: 目标服务错误

## 🔧 工具调用

### 工具定义处理策略

系统根据配置自动选择工具定义的处理方式，以优化性能和功能完整性：

#### 📍 工具定义位置

| 配置状态 | 工具定义位置 | 优势 | 适用场景 |
|---------|-------------|------|---------|
| `enable_tool_selection: true` | 作为用户消息追加 | 避免系统提示词缓存失效，提高性能 | 动态工具选择、高性能场景 |
| `enable_tool_selection: false` | 拼接到系统提示词 | 确保模型始终了解所有可用工具，保证功能完整性 | 稳定所有工具支持、传统场景 |

#### 🔄 处理流程

1. **检查配置**: 读取 `enable_tool_selection` 设置
2. **选择策略**: 
   - `true`: 工具定义 → 用户消息
   - `false`: 工具定义 → 系统提示词
3. **格式转换**: 将工具定义转换为相应的提示词格式
4. **消息构建**: 按选定策略构建最终消息列表

### 工具定义格式

```json
{
  "name": "tool_name",
  "description": "Tool description",
  "input_schema": {
    "type": "object",
    "properties": {
      "param1": {
        "type": "string",
        "description": "Parameter description"
      },
      "param2": {
        "type": "number",
        "description": "Another parameter"
      }
    },
    "required": ["param1"]
  }
}
```

### 工具调用格式

模型响应中的工具调用格式：

```json
{
  "type": "tool_use",
  "id": "call_123",
  "name": "tool_name",
  "input": {
    "param1": "value1",
    "param2": 42
  }
}
```

## 📝 请求示例

### 基本对话

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
        "content": "What is the weather like in Beijing?"
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

### 流式请求

```bash
curl -X POST "http://localhost:8000/v1/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "test-model",
    "messages": [
      {
        "role": "user",
        "content": "Tell me a story"
      }
    ],
    "stream": true
  }'
```

## 🔄 消息格式转换

### Anthropic → OpenAI

**输入 (Anthropic格式)**:
```json
{
  "model": "claude-3-sonnet",
  "messages": [
    {
      "role": "user",
      "content": "Hello"
    }
  ],
  "system": "You are a helpful assistant",
  "tools": [
    {
      "name": "get_weather",
      "description": "Get weather"
    }
  ]
}
```

**转换后 (OpenAI格式)**:

*未启用工具选择时 (enable_tool_selection: false)*:
```json
{
  "model": "claude-3-sonnet",
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful assistant\n\nYou have access to the following tools..."
    },
    {
      "role": "user",
      "content": "Hello"
    }
  ]
}
```

*启用工具选择时 (enable_tool_selection: true)*:
```json
{
  "model": "claude-3-sonnet",
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful assistant"
    },
    {
      "role": "user",
      "content": "Hello"
    },
    {
      "role": "user",
      "content": "You have access to the following tools..."
    }
  ]
}
```

### OpenAI → Anthropic

**输入 (OpenAI响应)**:
```json
{
  "choices": [
    {
      "message": {
        "content": "I'll help you with that.\n\n```json\n{\"type\": \"tool_use\", \"id\": \"call_123\", \"name\": \"get_weather\", \"input\": {\"location\": \"Beijing\"}}\n```"
      }
    }
  ]
}
```

**转换后 (Anthropic格式)**:
```json
{
  "content": [
    {
      "type": "text",
      "text": "I'll help you with that."
    },
    {
      "type": "tool_use",
      "id": "call_123",
      "name": "get_weather",
      "input": {
        "location": "Beijing"
      }
    }
  ],
  "stop_reason": "tool_use"
}
```

## 🚨 错误处理

### 错误响应格式

```json
{
  "detail": "Error message description"
}
```

### 常见错误

| 状态码 | 错误类型 | 说明 |
|--------|----------|------|
| 400 | Bad Request | 请求格式错误 |
| 500 | Internal Server Error | 服务器内部错误 |
| 502 | Bad Gateway | 目标服务不可用 |

### 错误示例

```json
{
  "detail": "invalid json body"
}
```

```json
{
  "detail": "request failed: Connection refused"
}
```

## 📊 性能指标

### 响应时间

- **健康检查**: < 10ms
- **简单对话**: < 100ms
- **工具调用**: < 200ms

### 并发支持

- **最大并发连接**: 1000
- **推荐并发连接**: 100

## 🔐 安全考虑

### API密钥

- 通过环境变量或配置文件设置
- 不要在请求中明文传输
- 定期轮换密钥

### 请求限制

- 建议实施速率限制
- 监控异常请求
- 记录访问日志

## 📚 更多资源

- [FastAPI文档](https://fastapi.tiangolo.com/)
- [OpenAI API文档](https://platform.openai.com/docs/api-reference)
- [Anthropic API文档](https://docs.anthropic.com/)

## 🔗 相关文档

- [🚀 快速开始指南](getting-started.md) - 安装和基本使用
- [⚙️ 配置说明](configuration.md) - 详细配置选项
- [🛠️ 开发指南](development.md) - 开发和调试指南