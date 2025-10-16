# Contributing Guide

[中文](/CONTRIBUTING.md) | English

Thank you for your interest in contributing to the Claude Code Adapter FastAPI project!

## 🚀 Getting Started

### 1. Fork and Clone the Repository
```bash
git clone https://github.com/wangfumin1/claude-code-adapter-fastapi.git
cd claude-code-adapter-fastapi
```

### 2. Set Up the Development Environment
```bash
# Use the automated setup script
# Windows:
scripts\setup.bat
# Linux/macOS:
./scripts/setup.sh

# Or set up manually
python -m venv venv
source venv/bin/activate  # Linux/macOS
pip install -r requirements-dev.txt
```

### 3. Run Tests
```bash
make test
```

## 📝 Development Workflow

1. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Develop and Test**
   ```bash
   # During development
   make test
   make lint
   make format
   ```

3. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   git push origin feature/your-feature-name
   ```

4. **Create a Pull Request**

## 📋 Contribution Requirements

### Code Quality
- New features must include unit tests
- Ensure all existing tests pass
- Use `make format` to format code
- Use `make lint` to check code quality

### Commit Message Guidelines
Use conventional commit format:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation updates
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test-related changes
- `chore`: Build process or auxiliary tool changes

### Documentation Requirements
- New features require updates to README.md
- API changes require updates to docs/api.md
- Configuration changes require updates to docs/configuration.md

> 📖 **Detailed Development Guide**: See [docs/development.md](docs/development.md) for complete setup and debugging instructions.

## 🐛 Issue Reporting

When submitting an issue, please include:
- Issue description
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment information

## 🤝 Code of Conduct

Please adhere to the following code of conduct:
- Respect all contributors
- Engage in constructive discussions
- Use inclusive language
- Maintain a professional attitude

## 📄 License

By contributing, you agree that your contributions will be licensed under the project's MIT License.

## 🔗 Related Resources

- [📖 Detailed Development Guide](docs/development.md) - Complete setup and debugging instructions
- [🐛 Issue Tracker](https://github.com/wangfumin1/claude-code-adapter-fastapi/issues) - Report issues or suggestions
- [🔒 Security Policy](SECURITY.md) - Guidelines for reporting security vulnerabilities
