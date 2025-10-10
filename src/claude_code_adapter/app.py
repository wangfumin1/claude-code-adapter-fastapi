"""
FastAPI应用主文件
"""

import json
import logging
from typing import Any, Dict, List

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse

from .config import config_manager, settings
from .models import HealthResponse
from .services import (
    MessageConverter,
    OpenAIClient,
    ResponseProcessor,
    ToolSelectionClient,
)
from .utils import flatten_content

# 配置日志
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="Claude Code Tool Prompt Adapter",
    description="将Claude Code的工具定义添加到系统提示词中，让非原生工具模型也能理解和使用工具",
    version="1.0.0",
)


# 初始化服务
message_converter = MessageConverter()
openai_client = OpenAIClient()
tool_selection_client = ToolSelectionClient()
response_processor = ResponseProcessor()


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """健康检查端点"""
    return HealthResponse(ok=True, target_base=settings.target_base_url)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """全局异常处理器，记录所有未捕获的异常"""
    logger.exception(f"未被捕获的异常: {exc}")
    return JSONResponse(
        status_code=500, content={"detail": f"内部服务器错误: {str(exc)}"}
    )


@app.post("/v1/messages")
async def proxy_messages(request: Request) -> Any:
    """代理消息请求到目标服务"""
    try:
        body = await request.json()
        logger.debug(f"收到请求体: {body}")
    except Exception:
        logger.exception("解析请求体失败")
        raise HTTPException(status_code=400, detail="无效的JSON")

    messages = body.get("messages", [])
    if not messages:
        raise HTTPException(status_code=400, detail="messages 不能为空")
    if not isinstance(messages, list):
        raise HTTPException(status_code=400, detail="messages 必须是一个列表")

    try:
        # 重新初始化以应用新的配置
        config_manager.reload()
        openai_client = OpenAIClient()
        settings = config_manager.settings

        tools = body.get("tools") or []
        tool_choice = body.get("tool_choice")

        # 工具选择逻辑
        if settings.enable_tool_selection and tools:
            if tool_choice:
                # 已经指定了工具，直接过滤
                selected_tools = [t for t in tools if tool_choice]
                logger.info(f"已指定工具调用: {tool_choice}")
            else:
                # 未指定时，再根据上下文做工具选择
                recent_count = settings.recent_messages_count
                recent_msgs = (body.get("messages") or [])[-recent_count:]
                selected_tools = await select_tools(
                    body.get("model"), recent_msgs, tools
                )
                logger.info(f"动态选择工具: {[t['name'] for t in selected_tools]}")

            body["tools"] = selected_tools
        else:
            if tools:
                logger.info("工具选择未启用，使用所有工具")
            else:
                logger.info("无工具可用")

        # 转换消息格式
        openai_messages = message_converter.convert_anthropic_to_openai_messages(body)

        payload = settings.target_model_config
        payload["model"] = payload["model"] if payload["model"] else body.get("model")
        payload["messages"] = openai_messages

        stream_mode = bool(body.get("stream"))
        payload["stream"] = stream_mode

        # 记录实际调用目标
        logger.info(
            f"请求地址：{openai_client.client.base_url}，"
            f"模型：{settings.target_model_config['model']}，流式：{stream_mode}"
        )

        if stream_mode:

            async def event_stream() -> Any:
                try:
                    stream = await openai_client.create_completion(payload)
                    async for chunk in stream:
                        yield f"data: {json.dumps(chunk.model_dump())}\n\n".encode()
                except Exception as e:
                    logger.exception("流式请求失败")
                    error_data = {
                        "type": "error",
                        "error": {
                            "type": "api_error",
                            "message": f"request failed: {str(e)}",
                        },
                    }
                    yield f"data: {json.dumps(error_data)}\n\n".encode()

            return StreamingResponse(event_stream(), media_type="text/event-stream")
        else:
            try:
                completion = await openai_client.create_completion(payload)
                lm_resp = completion.model_dump()
                logger.debug(f"非流式模型响应: {lm_resp}")
            except Exception as e:
                logger.exception("非流式请求失败")
                raise HTTPException(status_code=502, detail=f"request failed: {str(e)}")

            # 处理响应
            anthropic_resp = response_processor.process_response(
                lm_resp, settings.target_model_config["model"]
            )
            logger.debug(f"返回给客户端的响应: {anthropic_resp}")
            return JSONResponse(content=anthropic_resp, status_code=200)

    except Exception as e:
        logger.exception("处理请求失败")
        raise HTTPException(status_code=500, detail=f"internal error: {str(e)}")


async def select_tools(
    target_model: str,
    recent_msgs: List[Dict[str, Any]],
    all_tools: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    if not all_tools:
        return []

    # 构建待选择工具列表
    tools_list = "\n".join(
        f"{{{t['name']}: '{t['description'][0:100]}...'}}," for t in all_tools
    )

    # 构建最近消息列表
    recent_str = "\n\n".join(
        f"{{{m['role']}: '{flatten_content(m['content'])}'}}," for m in recent_msgs
    )

    # 格式化提示词
    user_content = settings.tool_selection_prompt.format(
        max_tools=settings.max_tools_to_select,
        recent_messages=recent_str,
        tools_list=tools_list,
    )
    logger.debug(f"工具选择提示词: {user_content}")
    payload = settings.tool_selection_model_config
    payload["model"] = payload.get("model") if payload.get("model") else target_model
    payload["messages"] = [{"role": "user", "content": user_content}]
    payload["stream"] = False
    if not payload["model"]:
        raise ValueError("工具选择模型未配置")

    try:
        completion = await tool_selection_client.create_completion(payload)
        response_content = completion.choices[0].message.content.strip()
        logger.info(f"工具选择模型响应: {response_content}")

        # 解析选择结果
        selected_names = json.loads(response_content)
        if not isinstance(selected_names, list):
            raise ValueError("选择结果不是列表")

        # 过滤出选择的工具
        logger.debug(f"所有可用工具: {all_tools}")
        selected_tools = [t for t in all_tools if t["name"] in selected_names]

        # 确保Read工具被包含
        read_tool = next((t for t in all_tools if t["name"] == "Read"), None)
        if read_tool and read_tool not in selected_tools:
            selected_tools.append(read_tool)
            logger.info("补充Read工具到选择列表")

        logger.info(f"从 {len(all_tools)} 个工具中选择了 {len(selected_tools)} 个工具")
        return selected_tools
    except Exception as e:
        logger.warning(f"选择工具失败: {e}。 使用默认工具列表。")
        # 优先从配置中的默认工具名称过滤可用工具
        try:
            default_tool_names = getattr(settings, "default_tools", []) or []
            if default_tool_names:
                filtered = [t for t in all_tools if t.get("name") in default_tool_names]
                if filtered:
                    return filtered[: settings.max_tools_to_select]
        except Exception as e:
            # 安全回退，不阻断主流程
            logger.exception(f"获取默认工具名称失败: {e}")
        # 若未配置或未匹配到，则截取前N个
        return all_tools[0 : settings.max_tools_to_select]


def create_app() -> FastAPI:
    """创建应用实例"""
    return app


def main() -> None:
    """命令行入口：启动 uvicorn 服务（仅服务端部署）"""
    uvicorn.run(
        "claude_code_adapter.app:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )


if __name__ == "__main__":
    main()
