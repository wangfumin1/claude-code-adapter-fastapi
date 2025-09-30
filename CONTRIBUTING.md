# 贡献指南

感谢您有兴趣为 Claude Code Adapter FastAPI 项目做出贡献！

## 🚀 快速开始

### 1. Fork 并克隆仓库
```bash
git clone https://github.com/wangfumin1/claude-code-adapter-fastapi.git
cd claude-code-adapter-fastapi
```

### 2. 设置开发环境
```bash
# 使用自动设置脚本
# Windows:
scripts\setup.bat
# Linux/macOS:
./scripts/setup.sh

# 或手动设置
python -m venv venv
source venv/bin/activate  # Linux/macOS
pip install -r requirements-dev.txt
```

### 3. 运行测试
```bash
make test
```

## 📝 开发流程

1. **创建特性分支**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **进行开发并测试**
   ```bash
   # 开发过程中
   make test
   make lint
   make format
   ```

3. **提交更改**
   ```bash
   git add .
   git commit -m "feat: 添加新功能描述"
   git push origin feature/your-feature-name
   ```

4. **创建 Pull Request**

## 📋 贡献要求

### 代码质量
- 新功能必须包含单元测试
- 确保所有现有测试通过
- 使用 `make format` 格式化代码
- 使用 `make lint` 检查代码质量

### 提交信息规范
使用约定式提交格式：
- `feat`: 新功能
- `fix`: 修复问题
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 重构代码
- `test`: 测试相关
- `chore`: 构建过程或辅助工具变动

### 文档要求
- 新功能需要更新 README.md
- API 变更需要更新 docs/api.md
- 配置变更需要更新 docs/configuration.md

> 📖 **详细开发指南**: 查看 [docs/development.md](docs/development.md) 获取完整的开发环境设置和调试指南。

## 🐛 问题报告

提交 Issue 时请包含：
- 问题描述
- 复现步骤
- 期望行为
- 实际行为
- 环境信息

## 🤝 行为准则

请遵守以下行为准则：
- 尊重所有贡献者
- 建设性讨论
- 包容性语言
- 专业态度

## 📄 许可证

通过提交贡献，您同意您的贡献将根据项目的 MIT 许可证进行许可。

## 🔗 相关资源

- [📖 详细开发指南](docs/development.md) - 完整的开发环境设置和调试指南
- [🐛 问题反馈](https://github.com/wangfumin1/claude-code-adapter-fastapi/issues) - 报告问题或建议
- [🔒 安全策略](SECURITY.md) - 安全漏洞报告指南
