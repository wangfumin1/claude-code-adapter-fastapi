# API Documentation

[中文](/docs/api.md) | English

This document provides detailed information about the Claude Code Adapter FastAPI API endpoints.

## 🌐 Basic Information

- **Base URL**: `http://localhost:8000`
- **API Version**: v1
- **Content Type**: `application/json`

## 📋 Endpoint List

### Health Check

#### GET /health

Checks the health status of the service.

**Response Example**:
```json
{
  "ok": true,
  "target_base": "http://127.0.0.1:1234"
}
```

**Status Codes**:
- `200 OK`: Service is operational

### Message Proxy

#### POST /v1/messages

Proxies message requests to the target service, supporting tool calls.

**Request Body**:
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

**Response Examples**:

**Non-Streaming Response**:
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

**Tool Call Response**:
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

**Streaming Response**:
```
data: {"id": "msg_123", "object": "chat.completion.chunk", "choices": [{"delta": {"content": "Hello"}}]}

data: {"id": "msg_123", "object": "chat.completion.chunk", "choices": [{"delta": {"content": "!"}}]}

data: [DONE]
```

**Status Codes**:
- `200 OK`: Request successful
- `400 Bad Request`: Invalid request format
- `500 Internal Server Error`: Server error
- `502 Bad Gateway`: Target service error

## 🔧 Tool Calls

### Tool Definition Handling Strategy

The system automatically selects the tool definition handling method based on configuration to optimize performance and functionality:

#### 📍 Tool Definition Placement

| Configuration | Tool Definition Location | Advantages | Use Cases |
|---------------|-------------------------|------------|-----------|
| `enable_tool_selection: true` | Appended as user message | Avoids system prompt cache invalidation, improves performance | Dynamic tool selection, high-performance scenarios |
| `enable_tool_selection: false` | Included in system prompt | Ensures model awareness of all available tools, maintains functionality | Stable tool support, traditional scenarios |

#### 🔄 Processing Workflow

1. **Check Configuration**: Reads `enable_tool_selection` setting
2. **Select Strategy**:
   - `true`: Tool definitions → User messages
   - `false`: Tool definitions → System prompt
3. **Format Conversion**: Converts tool definitions to the appropriate prompt format
4. **Message Construction**: Builds the final message list based on the selected strategy

### Tool Definition Format

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

### Tool Call Format

Tool call format in the model response:

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

## 📝 Request Examples

### Basic Conversation

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

### Streaming Request

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

## 🔄 Message Format Conversion

### Anthropic → OpenAI

**Input (Anthropic Format)**:
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

**Converted (OpenAI Format)**:

*When tool selection is disabled (enable_tool_selection: false)*:
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

*When tool selection is enabled (enable_tool_selection: true)*:
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

**Input (OpenAI Response)**:
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

**Converted (Anthropic Format)**:
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

## 🚨 Error Handling

### Error Response Format

```json
{
  "detail": "Error message description"
}
```

### Common Errors

| Status Code | Error Type | Description |
|-------------|------------|-------------|
| 400 | Bad Request | Invalid request format |
| 500 | Internal Server Error | Server internal error |
| 502 | Bad Gateway | Target service unavailable |

### Error Examples

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

## 📊 Performance Metrics

### Response Times

- **Health Check**: < 10ms
- **Simple Conversation**: < 100ms
- **Tool Calls**: < 200ms

### Concurrency Support

- **Maximum Concurrent Connections**: 1000
- **Recommended Concurrent Connections**: 100

## 🔐 Security Considerations

### API Key

- Set via environment variables or configuration file
- Do not transmit in plaintext in requests
- Rotate keys regularly

### Request Limits

- Implement rate limiting
- Monitor abnormal requests
- Log access activities

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)
- [Anthropic API Documentation](https://docs.anthropic.com/)

## 🔗 Related Documentation

- [🚀 Quick Start Guide](getting-started.md) - Installation and basic usage
- [⚙️ Configuration Guide](configuration.md) - Detailed configuration options
- [🛠️ Development Guide](development.md) - Development and debugging guide
