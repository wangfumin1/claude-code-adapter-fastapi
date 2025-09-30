"""
数据模型定义
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class Message(BaseModel):
    """消息模型"""

    role: str
    content: Any


class ToolCall(BaseModel):
    """工具调用模型"""

    id: str
    type: str = "function"
    function: Dict[str, Any]


class ContentBlock(BaseModel):
    """内容块模型"""

    type: str
    text: Optional[str] = None
    id: Optional[str] = None
    name: Optional[str] = None
    input: Optional[Dict[str, Any]] = None


class ChatRequest(BaseModel):
    """聊天请求模型"""

    model: str
    messages: List[Message]
    max_tokens: Optional[int] = 4096
    temperature: Optional[float] = 0.1
    stream: Optional[bool] = False
    system: Optional[str] = None
    tools: Optional[List[Dict[str, Any]]] = None


class ChatResponse(BaseModel):
    """聊天响应模型"""

    id: str
    type: str = "message"
    role: str = "assistant"
    model: str
    stop_reason: str
    stop_sequence: Optional[str] = None
    usage: Dict[str, int]
    content: List[ContentBlock]


class HealthResponse(BaseModel):
    """健康检查响应模型"""

    ok: bool
    target_base: str
