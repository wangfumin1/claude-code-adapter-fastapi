"""
工具函数测试
"""
from src.claude_code_adapter.utils import (
    flatten_content,
    convert_tools_to_prompt,
    parse_tool_calls_from_response
)


class TestFlattenContent:
    """测试内容扁平化"""
    
    def test_flatten_string(self):
        """测试字符串扁平化"""
        assert flatten_content("hello") == "hello"
        assert flatten_content("") == ""
    
    def test_flatten_none(self):
        """测试None扁平化"""
        assert flatten_content(None) == ""
    
    def test_flatten_text_dict(self):
        """测试文本字典扁平化"""
        content = {"type": "text", "text": "hello world"}
        assert flatten_content(content) == "hello world"
    
    def test_flatten_tool_result(self):
        """测试工具结果扁平化"""
        content = {
            "type": "tool_result",
            "tool_use_id": "call_123",
            "content": "result"
        }
        assert flatten_content(content) == "Tool call_123 result: result"
    
    def test_flatten_list(self):
        """测试列表扁平化"""
        content = ["hello", "world"]
        assert flatten_content(content) == "hello\nworld"


class TestConvertToolsToPrompt:
    """测试工具转提示词"""
    
    def test_convert_tools_empty(self):
        """测试空工具列表"""
        template = "Tools: {tools_json}"
        result = convert_tools_to_prompt([], template)
        assert result == ""
    
    def test_convert_tools_single(self):
        """测试单个工具"""
        tools = [{"name": "test_tool", "description": "A test tool"}]
        template = "Tools: {tools_json}"
        result = convert_tools_to_prompt(tools, template)
        assert "test_tool" in result
        assert "A test tool" in result


class TestParseToolCalls:
    """测试工具调用解析"""
    
    def test_parse_tool_calls_valid(self):
        """测试解析有效的工具调用"""
        content = '''
        ```json
        {
          "type": "tool_use",
          "id": "call_123",
          "name": "test_tool",
          "input": {"param": "value"}
        }
        ```
        '''
        tools, content = parse_tool_calls_from_response(content)
        assert len(tools) == 1
        assert tools[0]["id"] == "call_123"
        assert tools[0]["function"]["name"] == "test_tool"
        assert content == ''
    
    def test_parse_tool_calls_invalid(self):
        """测试解析无效的工具调用"""
        content = "This is just text without tool calls"
        tools, content = parse_tool_calls_from_response(content)
        assert len(tools) == 0
        assert content == "This is just text without tool calls"

    def test_parse_tool_calls_multiple(self):
        """测试解析多个工具调用"""
        content = '''
        Having multiple tool calls:
        ```json
        {
          "type": "tool_use",
          "id": "call_1",
          "name": "tool1",
          "input": {}
        }
        ```
        
        ```json
        {
          "type": "tool_use",
          "id": "call_2",
          "name": "tool2",
          "input": {}
        }
        ```
        '''
        tools, content = parse_tool_calls_from_response(content)
        assert len(tools) == 2
        assert tools[0]["function"]["name"] == "tool1"
        assert tools[1]["function"]["name"] == "tool2"
        assert content == "Having multiple tool calls:"