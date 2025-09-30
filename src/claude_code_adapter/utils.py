"""
工具函数模块
"""
import json
import re
import time
from typing import Any, Dict, List, Tuple
import logging
logger = logging.getLogger(__name__)

def flatten_content(content: Any) -> str:
    """将复杂内容结构扁平化为字符串"""
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, dict):
        if content.get("type") == "text":
            return content.get("text", "")
        elif content.get("type") == "tool_result":
            # 处理工具调用结果
            tool_id = content.get("tool_use_id", "unknown")
            result_content = content.get("content", "")
            if isinstance(result_content, list):
                result_text = ""
                for item in result_content:
                    if isinstance(item, dict) and item.get("type") == "text":
                        result_text += item.get("text", "")
                    else:
                        result_text += str(item)
            else:
                result_text = str(result_content)
            return f"Tool {tool_id} result: {result_text}"
        return json.dumps(content, ensure_ascii=False)
    if isinstance(content, list):
        parts = []
        for p in content:
            parts.append(flatten_content(p))
        return "\n".join([p for p in parts if p])
    return str(content)


def convert_tools_to_prompt(tools: List[Dict[str, Any]], template: str) -> str:
    """将工具定义转换为提示词"""
    if not tools:
        return ""
    
    tools_json = json.dumps(tools, indent=2, ensure_ascii=False)
    # 使用 replace 方法避免 format() 的花括号冲突问题
    return template.replace("{tools_json}", tools_json)

def extract_json_objects(text: str, mode: str = "object") -> List[Tuple[str, int, int]]:
    """
    从文本中提取所有 JSON 对象或数组（支持嵌套）。
    mode: "object" 只提取 {...}，"array" 只提取 [...]
    返回: [(json_str, start_idx, end_idx), ...]
    """
    results = []

    # 先处理 ```json ... ``` 包裹的情况
    fenced_matches = list(re.finditer(r"```json\s*([\s\S]*?)```", text, re.MULTILINE))
    for m in fenced_matches:
        json_str = m.group(1).strip()
        results.append((json_str, m.start(), m.end()))

    # 如果 fenced code block 里已经有了 JSON，就不再从裸文本里重复找
    if results:
        return results

    # 裸 JSON 扫描器
    stack = []
    start_idx = None
    opening_char = "{" if mode == "object" else "["
    closing_char = "}" if mode == "object" else "]"

    for i, ch in enumerate(text):
        if ch == opening_char:
            if not stack:
                start_idx = i
            stack.append(ch)
        elif ch == closing_char:
            if not stack:
                continue
            stack.pop()
            if not stack and start_idx is not None:
                results.append((text[start_idx:i+1], start_idx, i+1))
                start_idx = None
    return results


def fix_invalid_json(json_str: str) -> str:
    """修复非法 JSON（如单引号 -> 双引号）"""
    return re.sub(
        r"'([^']*)'",
        lambda m: '"' + m.group(1).replace('"', '\\"') + '"',
        json_str
    )


def remove_json_objects(text: str, objects: List[Tuple[str, int, int]]) -> str:
    """
    从文本中移除指定的 JSON 片段（包括 ```json``` 包裹的）。
    objects: [(json_str, start, end), ...]
    """
    if not objects:
        return text.strip()

    clean_parts = []
    last_idx = 0
    for _, start, end in objects:
        clean_parts.append(text[last_idx:start])
        last_idx = end
    clean_parts.append(text[last_idx:])  # 最后一段
    return "".join(clean_parts).strip()



def parse_tool_calls_from_response(content: str) -> Tuple[List[Dict[str, Any]], str]:
    """解析工具调用，并返回 (tool_calls, clean_content)"""
    tool_calls = []
    clean_content = content

    try:
        # 先尝试匹配对象
        json_candidates = extract_json_objects(content, mode="object")
        if not json_candidates:
            json_candidates = extract_json_objects(content, mode="array")

        # 保存需要移除的 JSON 片段
        tool_json_segments = []

        for idx, (json_str, start, end) in enumerate(json_candidates):
            try:
                fixed_str = fix_invalid_json(json_str)
                parsed = json.loads(fixed_str)

                if (isinstance(parsed, dict) and 
                    parsed.get("type") == "tool_use" and 
                    "name" in parsed and 
                    "input" in parsed):
                    tool_call = {
                        "id": parsed.get("id", f"call_{int(time.time())}_{idx}"),
                        "type": "function",
                        "function": {
                            "name": parsed["name"],
                            "arguments": json.dumps(parsed["input"])
                        }
                    }
                    tool_calls.append(tool_call)
                    tool_json_segments.append((json_str, start, end))  # 仅记录工具调用 JSON

            except json.JSONDecodeError:
                continue

        # 移除工具调用 JSON 内容，返回干净文本
        clean_content = remove_json_objects(content, tool_json_segments)

    except Exception as e:
        logger.warning(f"解析工具调用时出错: {e}")

    return tool_calls, clean_content

def build_chat_completion_args(params: dict) -> dict:
    """
    将原始参数字典转换为符合 OpenAI create() 方法要求的关键字参数。

    - 丢弃非法字段（只保留 OpenAI API 支持的字段）
    - 将显式为 None 的字段替换为 NOT_GIVEN
    - 检查是否包含必要的参数：model 与 messages

    参数:
        params (dict): 外部传入的参数字典。

    返回:
        dict: 可传入 openai.chat.completions.create() 的关键字参数。
    """
    # 必须包含的字段
    required_fields = ['model', 'messages']
    for field in required_fields:
        if field not in params:
            raise ValueError(f"缺少必须参数: '{field}'")

    # OpenAI Chat Completion 支持的字段白名单
    legal_keys = {
        "messages",              # 对话消息数组，包含 role（system/user/assistant 等）和 content（文本/多模态内容）
        "model",                 # 指定使用的模型名称，如 gpt-4o、gpt-4o-mini、gpt-3.5-turbo 等
        "audio",                 # 音频相关参数（如输入音频、生成语音等功能）
        "frequency_penalty",     # 控制生成时的重复频率，范围 -2.0~2.0，值大减少重复
        "function_call",         # 指定函数调用方式，如 "auto"、"none"、或指定函数名
        "functions",             # 定义可调用的函数列表，包含函数名和 JSON Schema 格式的参数
        "logit_bias",            # 调整指定 token 的生成概率，值范围 -100~100
        "logprobs",              # 是否返回每个位置的 token 生成概率（log 概率）
        "max_completion_tokens", # 限制补全部分的最大 token 数（新版字段）
        "max_tokens",            # 限制生成的最大 token 数（旧版通用字段）
        "metadata",              # 携带请求的元数据（与 store 配合使用）
        "modalities",            # 指定生成的输出模态类型，如 ["text"]、["text", "image"]
        "n",                     # 生成并返回的结果数量
        "parallel_tool_calls",   # 是否允许并行调用多个工具
        "prediction",            # 用于推理或预测任务的参数（实验性）
        "presence_penalty",      # 控制生成新主题的倾向，范围 -2.0~2.0，值大更鼓励引入新主题
        "reasoning_effort",      # 指定推理复杂度（如 "low"、"medium"、"high"）
        "response_format",       # 指定输出格式，如 {"type": "json_object"} 用于 JSON 输出
        "seed",                  # 固定随机种子，便于结果复现
        "service_tier",          # 服务套餐级别（仅部分账户/接口支持）
        "stop",                  # 指定最多 4 个停止序列，遇到时生成立即结束
        "store",                 # 是否将请求和响应存储在服务器端（与 metadata 配合）
        "stream",                # 是否启用流式输出
        "stream_options",        # 流式输出的附加设置
        "temperature",           # 控制生成的随机性，0~2，值大输出更随机
        "tool_choice",           # 指定工具调用策略，如 "auto" 或具体工具名
        "tools",                 # 定义可用工具列表
        "top_logprobs",          # 返回每个位置最可能的前 N 个 token 及 log 概率
        "top_p",                 # nucleus sampling 采样范围，常与 temperature 二选一
        "user",                  # 表示请求用户的唯一标识字符串（非敏感），用于监控与分析
        "web_search_options",    # 网页搜索相关参数（仅部分模型支持）
        "extra_headers",         # 额外 HTTP 请求头
        "extra_query",           # 额外查询参数
        "extra_body",            # 额外请求体字段
        "timeout",               # 请求超时时间（秒）
    }
    # 构造最终参数：非法字段丢弃
    args = {}
    for key in legal_keys:
        val = params.get(key)
        if val is not None:
            args[key] = val

    return args