#!/usr/bin/env python3
"""
启动脚本
"""
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import uvicorn
from src.claude_code_adapter.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "src.claude_code_adapter.app:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
