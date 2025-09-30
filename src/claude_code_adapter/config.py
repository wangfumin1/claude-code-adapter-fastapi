"""
配置管理模块
支持从配置文件和环境变量读取配置
"""
import yaml
import json
from typing import Any, Dict, Optional, List
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    """应用配置类"""

    # 目标服务配置
    target_base_url: str = Field(default="http://127.0.0.1:1234", alias="TARGET_BASE_URL")
    target_api_key: str = Field(default="key", alias="TARGET_API_KEY")
    target_api_key_header: str = Field(default="Authorization", alias="TARGET_API_KEY_HEADER")
    target_model_config: dict = Field(default={}, alias="TARGET_MODEL_CONFIG")

    # 服务配置
    host: str = Field(default="127.0.0.1", alias="HOST")
    port: int = Field(default=8000, alias="PORT")
    debug: bool = Field(default=False, alias="DEBUG")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    

    # 系统提示词相关配置
    enable_raw_system_prompt: bool = Field(default=False, alias="ENABLE_RAW_SYSTEM_PROMPT")
    enable_custom_system_prompt: bool = Field(default=True, alias="ENABLE_CUSTOM_SYSTEM_PROMPT")
    custom_system_prompt: str = Field(
        default="你是Claude Code Adapter",
        alias="CUSTOM_SYSTEM_PROMPT"
    )
    
    # 工具配置
    enable_tool_selection: bool = Field(default=False, alias="ENABLE_TOOL_SELECTION")
    tool_selection_base_url: str = Field(default="http://127.0.0.1:1234", alias="TOOL_SELECTION_BASE_URL")
    tool_selection_api_key: str = Field(default="key", alias="TOOL_SELECTION_API_KEY")
    tool_selection_model_config: dict = Field(default={}, alias="TOOL_SELECTION_MODEL_CONFIG")
    # 当工具选择失败或未启用时的默认工具名称列表
    default_tools: List[str] = Field(default=["Read", "Edit", "Grep"], alias="DEFAULT_TOOLS")
    tool_selection_prompt: str = Field(
        default="""
  Select up to {max_tools} tools from 'Available tools' that best match the user's needs based on recent messages. Only use tool names from 'Available tools', not from messages. Choose tools proactively if they seem relevant. Return a JSON array of tool names, or [] if no tools apply.

  Recent messages: [
  {recent_messages}
  ]

  Available tools: [
  {tools_list}
  ]""",
        alias="TOOL_SELECTION_PROMPT"
    )
    recent_messages_count: int = Field(default=5, alias="RECENT_MESSAGES_COUNT")
    max_tools_to_select: int = Field(default=3, alias="MAX_TOOLS_TO_SELECT")
    tool_use_prompt: str = Field(
        default="""You have access to the following tools. The available tools are defined in JSON format below:

```json
{tools_json}
```

When you need to use a tool, respond with JSON in this exact format:
```json
{{
  "type": "tool_use",
  "id": "call_123",
  "name": "ToolName",
  "input": {{"param": "value"}}
}}
```

Use the tools to help complete the user's request.""",
        alias="TOOL_USE_PROMPT"
    )
    logger.info(f'环境配置加载完成')

class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file or self._find_config_file()
        self.settings = self._load_settings()
    
    def _find_config_file(self) -> Optional[str]:
        """查找配置文件"""
        possible_files = [
            "config.yaml",
            "config.yml", 
            "config.json",
            "config/config.yaml",
            "config/config.yml",
            "config/config.json"
        ]
        
        for file_path in possible_files:
            if Path(file_path).exists():
                return file_path
        logger.warning("没有找到配置文件，使用默认配置")
        return None
    
    def _load_settings(self) -> Settings:
        """加载配置"""
        settings = Settings()
        
        if self.config_file:
            config_data = self._load_config_file()
            if config_data:
                # 更新设置
                for key, value in config_data.items():
                    if hasattr(settings, key):
                        setattr(settings, key, value)
        logger.info(f"配置加载完成: {self.config_file or '默认配置'}")
        return settings
    
    def _load_config_file(self) -> Dict[str, Any]:
        """从配置文件加载数据"""
        if not self.config_file or not Path(self.config_file).exists():
            logger.warning("没有找到配置文件，使用默认配置")
            return {}
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                if self.config_file.endswith(('.yaml', '.yml')):
                    return yaml.safe_load(f) or {}
                elif self.config_file.endswith('.json'):
                    return json.load(f) or {}
        except Exception as e:
            logger.exception(f"加载配置文件失败 {self.config_file}: {e}")
            return {}
        return {}
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        return getattr(self.settings, key, default)
    
    def reload(self):
        """重新加载配置"""
        self.settings = self._load_settings()


# 全局配置实例
config_manager = ConfigManager()
settings = config_manager.settings
