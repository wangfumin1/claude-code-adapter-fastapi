# 更新日志

本文档记录了项目的所有重要变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
项目遵循 [语义化版本](https://semver.org/spec/v2.0.0.html)。

## [1.0.0] - 2025-09-30

### 新增
- 初始版本发布
- FastAPI应用框架
- 工具提示词适配功能
- 消息格式转换（Anthropic ↔ OpenAI）
- 配置管理系统
- 支持conda环境管理
- 智能环境检测和跳过重复操作
- 强制重新安装选项
- 完整的文档系统
- 多种设置脚本（批处理、Shell）
- 智能工具定义处理策略
- Docker支持
- 测试框架
- CI/CD流水线
- 基础文档

### 功能特性
- 🔧 工具提示词适配
- 🚀 FastAPI框架
- ⚙️ 灵活配置
- 🐳 Docker支持
- 🧪 完整测试
- 📚 详细文档

### 技术栈
- FastAPI 0.104.1+
- Pydantic 2.5.0+
- OpenAI Python 1.3.0+
- Uvicorn 0.24.0+
- PyYAML 6.0.1+

### 支持的Python版本
- Python 3.9
- Python 3.10
- Python 3.11

---

## 版本说明

### 版本号格式
- **MAJOR**: 不兼容的API修改
- **MINOR**: 向下兼容的功能性新增
- **PATCH**: 向下兼容的问题修正

### 变更类型
- **新增**: 新功能
- **改进**: 现有功能的改进
- **修复**: 问题修复
- **移除**: 移除的功能
- **安全**: 安全相关的修复

### 链接格式
- [版本号]: https://github.com/wangfumin1/claude-code-adapter-fastapi/compare/v1.0.0...v1.1.0
- [未发布]: https://github.com/wangfumin1/claude-code-adapter-fastapi/compare/v1.0.0...HEAD
