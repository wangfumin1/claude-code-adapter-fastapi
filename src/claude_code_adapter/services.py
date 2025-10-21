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
    get_structured_config,
    is_multimodal_model,
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
        logger.setLevel(settings.log_level)
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
                logger.info(
                    f"工具选择已启用，将 {len(tools)} 个工具追加到messages，role=user"
                )
            else:
                # 未启用工具选择时，拼接到系统提示词中
                system_parts.append(tool_prompt)
                logger.info(f"工具选择未启用，将 {len(tools)} 个工具拼接到系统提示词中")

        # 如果有系统提示词，先加入
        if system_parts:
            out.append({"role": "system", "content": "\n".join(system_parts)})

        # 处理对话消息
        msgs = body.get("messages") or []
        out = self.convert_messages(msgs, body.get("model", ""))

        # 如果启用了工具选择，将工具定义作为用户消息追加
        if settings.enable_tool_selection:
            tools = body.get("tools", [])
            if tools:
                tool_prompt = convert_tools_to_prompt(tools, self.tool_use_prompt)
                out.append({"role": "user", "content": tool_prompt})
        logger.debug(f"转换后的OpenAI消息: {out}")
        return out

    def convert_claude_structured(self, content: Any, cfg: Dict) -> Any:
        """通用转换器：Claude结构 → 目标模型结构（含 image/audio/video）"""
        if content is None:
            return ""

        if not cfg:
            # 未匹配模型 → 降级为纯文本
            if isinstance(content, dict):
                logger.debug("未找到模型配置，降级为JSON字符串")
                return content.get("text", json.dumps(content, ensure_ascii=False))
            if isinstance(content, list):
                logger.debug("未找到模型配置，按列表处理")
                return [self.convert_claude_structured(c, cfg) for c in content]
            logger.debug("未找到模型配置，降级为字符串")
            return str(content)

        ctype_map = cfg.get("content_types", {})

        # === 文本 ===
        if isinstance(content, dict) and content.get("type") == "text":
            text_cfg = ctype_map.get("text", {"type": "text"})
            return {"type": text_cfg["type"], "text": content.get("text", "")}

        # === 通用媒体类型转换函数 ===
        def convert_media(media_type: str) -> Dict[str, Any]:
            logger.debug(
                f"{media_type.capitalize()}内容转换，使用配置: {ctype_map.get(media_type)}"
            )
            src = content.get("source", {})
            base64_data = src.get("data")
            mime = src.get("media_type", f"{media_type}/*")
            media_cfg = ctype_map.get(media_type)
            if not media_cfg:
                return {
                    "type": "text",
                    "text": f"[{media_type.capitalize()} not supported by model]",
                }

            # URL 形式（最常见）
            if "url_key" in media_cfg:
                key = media_cfg["url_key"]
                return {
                    "type": media_cfg["type"],
                    media_cfg["type"]: {key: f"data:{mime};base64,{base64_data}"},
                }

            # 源结构（如 Claude 自身格式）
            if "source" in media_cfg:
                src_cfg = media_cfg["source"]
                return {
                    "type": media_cfg["type"],
                    "source": {
                        "type": src_cfg.get("type", "base64"),
                        "media_type": mime,
                        src_cfg.get("data_key", "data"): base64_data,
                    },
                }

            return {
                "type": "text",
                "text": f"[{media_type.capitalize()} conversion failed]",
            }

        # === 图片 ===
        if isinstance(content, dict) and content.get("type") == "image":
            return convert_media("image")

        # === 音频 ===
        if isinstance(content, dict) and content.get("type") == "audio":
            return convert_media("audio")

        # === 视频 ===
        if isinstance(content, dict) and content.get("type") == "video":
            return convert_media("video")

        # === 列表递归 ===
        if isinstance(content, list):
            return [self.convert_claude_structured(c, cfg) for c in content]

        logger.warning(f"未知内容类型，降级为字符串: {content}")
        # 其他 → 转字符串
        return str(content)

    def convert_messages(
        self, msgs: List[Dict[str, Any]], model: str
    ) -> List[Dict[str, Any]]:
        """转换对话消息，处理多模态结构化内容"""
        out = []
        if not is_multimodal_model(model):
            logger.info("目标模型不支持多模态结构化内容，降级为纯文本处理")
            for m in msgs:
                role = m.get("role", "user")
                content = m.get("content")
                text = flatten_content(content)
                if text:
                    out.append({"role": role, "content": text})
        else:
            logger.info("目标模型支持多模态结构化内容，进行结构化内容转换")
            for m in msgs:
                role = m.get("role", "user")
                content = m.get("content")
                converted_content = self.convert_claude_structured(
                    content, get_structured_config(model)
                )
                out.append({"role": role, "content": converted_content})
        return out


class OpenAIClient:
    """OpenAI客户端服务"""

    async def create_completion(
        self, url: str, key: str, payload: Dict[str, Any]
    ) -> Any:
        """创建完成请求"""
        client = AsyncOpenAI(base_url=url, api_key=key)
        return await client.chat.completions.create(**payload)


class ResponseProcessor:
    """响应处理服务"""

    def process_response(
        self, lm_resp: Dict[str, Any], target_model: str
    ) -> Dict[str, Any]:
        """处理模型响应，转换为Anthropic格式"""
        logger.setLevel(settings.log_level)
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
                        logger.warning(
                            f"解析工具调用参数失败: {func.get('arguments')}, 使用空参数"
                        )

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
