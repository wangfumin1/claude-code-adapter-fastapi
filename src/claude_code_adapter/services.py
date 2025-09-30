"""
服务层模块
"""

import json
import logging
import re
from typing import Any, Dict, List

from openai import AsyncOpenAI

from .config import settings
from .utils import (
    convert_tools_to_prompt,
    flatten_content,
    parse_tool_calls_from_response,
)

logger = logging.getLogger(__name__)


class MessageConverter:
    """消息转换服务"""

    def __init__(self) -> None:
        self.tool_use_prompt = settings.tool_use_prompt

    def convert_anthropic_to_openai_messages(
        self, body: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """将Anthropic格式消息转换为OpenAI格式"""
        out: List[Dict[str, Any]] = []

        # 构建系统提示词
        system_parts = []

        # 原始系统提示词
        sys_field = body.get("system")
        if settings.enable_raw_system_prompt and sys_field:
            system_parts.append(flatten_content(sys_field))

        if settings.enable_custom_system_prompt:
            system_parts.append(settings.custom_system_prompt)

        # 处理工具定义
        tools = body.get("tools", [])
        if tools:
            tool_prompt = convert_tools_to_prompt(tools, self.tool_use_prompt)

            if settings.enable_tool_selection:
                # 启用工具选择时，追加到用户消息中
                logger.info(f"工具选择已启用，将 {len(tools)} 个工具追加到messages，role=user")
            else:
                # 未启用工具选择时，拼接到系统提示词中
                system_parts.append(tool_prompt)
                logger.info(f"工具选择未启用，将 {len(tools)} 个工具拼接到系统提示词中")

        # 如果有系统提示词，先加入
        if system_parts:
            out.append({"role": "system", "content": "\n".join(system_parts)})

        # 处理对话消息
        msgs = body.get("messages") or []
        for m in msgs:
            role = m.get("role", "user")
            content = m.get("content")
            text = flatten_content(content)
            if text:
                out.append({"role": role, "content": text})

        # 如果启用了工具选择，将工具定义作为用户消息追加
        if settings.enable_tool_selection:
            tools = body.get("tools", [])
            if tools:
                tool_prompt = convert_tools_to_prompt(tools, self.tool_use_prompt)
                out.append({"role": "user", "content": tool_prompt})

        return out


class OpenAIClient:
    """OpenAI客户端服务"""

    def __init__(self) -> None:
        self.client = AsyncOpenAI(
            api_key=settings.target_api_key, base_url=settings.target_base_url
        )

    async def create_completion(self, payload: Dict[str, Any]) -> Any:
        """创建完成请求"""
        return await self.client.chat.completions.create(**payload)


class ToolSelectionClient:
    """工具选择专用客户端服务"""

    def __init__(self) -> None:
        self.client = AsyncOpenAI(
            api_key=settings.tool_selection_api_key,
            base_url=settings.tool_selection_base_url,
        )

    async def create_completion(self, payload: Dict[str, Any]) -> Any:
        """创建工具选择完成请求"""
        return await self.client.chat.completions.create(**payload)


class ResponseProcessor:
    """响应处理服务"""

    def process_response(
        self, lm_resp: Dict[str, Any], target_model: str
    ) -> Dict[str, Any]:
        """处理模型响应，转换为Anthropic格式"""
        content_blocks = []

        logger.debug(f"原始响应内容: {lm_resp}")
        for choice in lm_resp.get("choices", []):
            msg = choice.get("message", {})
            content = msg.get("content", "")

            # 检查是否包含工具调用
            tool_calls, content = parse_tool_calls_from_response(content)

            if tool_calls:
                # 有工具调用，转换为Anthropic格式
                logger.info(f"在响应中找到 {len(tool_calls)} 个工具调用")

                # 先添加可能存在的文本内容
                text_content = re.sub(
                    r"```json.*?```", "", content, flags=re.DOTALL
                ).strip()
                if text_content:
                    content_blocks.append({"type": "text", "text": text_content})

                # 添加工具调用
                for tc in tool_calls:
                    func = tc["function"]
                    try:
                        args = (
                            json.loads(func["arguments"])
                            if isinstance(func["arguments"], str)
                            else func["arguments"]
                        )
                    except Exception:
                        args = {}
                        logger.warning(f"解析工具调用参数失败: {func.get('arguments')}, 使用空参数")

                    content_blocks.append(
                        {
                            "type": "tool_use",
                            "id": tc["id"],
                            "name": func["name"],
                            "input": args,
                        }
                    )
            else:
                logger.info("响应中没有找到工具调用")
                # 没有工具调用，直接添加文本
                if content:
                    content_blocks.append({"type": "text", "text": content})

        # 构建Anthropic格式响应
        import time

        anthropic_resp = {
            "id": lm_resp.get("id") or f"msg_{int(time.time())}",
            "type": "message",
            "role": "assistant",
            "model": lm_resp.get("model", target_model),
            "stop_reason": (
                "tool_use"
                if any(block.get("type") == "tool_use" for block in content_blocks)
                else "end_turn"
            ),
            "stop_sequence": None,
            "usage": {
                "input_tokens": lm_resp.get("usage", {}).get("prompt_tokens", 0),
                "output_tokens": lm_resp.get("usage", {}).get("completion_tokens", 0),
            },
            "content": content_blocks or [{"type": "text", "text": ""}],
        }

        logger.info(f"返回响应: {len(content_blocks)} 个块")
        logger.debug(
            f"响应内容: {json.dumps(anthropic_resp, ensure_ascii=False, indent=2)}"
        )
        return anthropic_resp
