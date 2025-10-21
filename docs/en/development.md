# Development Guide

[中文](../development.md) | English

This document provides detailed instructions for setting up the development environment, project structure, and contribution guidelines for developers.

## 🛠️ Development Environment Setup

### 1. Clone the Repository

```bash
git clone https://github.com/wangfumin1/claude-code-adapter-fastapi.git
cd claude-code-adapter-fastapi
```

### 2. Create Development Environment

```bash
# Using automated setup scripts
# Windows:
scripts\setup.bat
# Linux/macOS:
./scripts/setup.sh

# Or manual setup
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3. Install Development Dependencies

```bash
pip install -r requirements-dev.txt
```

### 4. Install Pre-Commit Hooks

```bash
pre-commit install
```

## 📁 Project Structure

```
claude-code-adapter-fastapi/
├── src/
│   └── claude_code_adapter/
│       ├── __init__.py          # Package initialization
│       ├── app.py              # FastAPI application main file
│       ├── config.py           # Configuration management
│       ├── models.py           # Data models
│       ├── services.py         # Business logic services
│       └── utils.py            # Utility functions
├── tests/                      # Test files
│   ├── __init__.py
│   ├── test_app.py            # Application tests
│   └── test_utils.py          # Utility function tests
├── scripts/                    # Script files
│   ├── setup.bat               # Windows setup script
│   ├── setup.sh               # Linux/macOS setup script
│   ├── check_env.py           # Environment check
│   └── start.py               # Startup script
├── docs/                       # Documentation
├── docker/                     # Docker-related files
├── .github/workflows/          # CI/CD configuration
├── config.yaml                # Configuration file
├── requirements.txt           # Production dependencies
├── requirements-dev.txt       # Development dependencies
├── pyproject.toml            # Project configuration
├── Makefile                  # Build scripts
└── README.md                 # Project description
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
make test

# Or use pytest
pytest tests/ -v

# Run specific tests
pytest tests/test_utils.py -v

# Generate coverage report
make test-cov
```

### Test Structure

- **Unit Tests**: Test individual functions and classes
- **Integration Tests**: Test API endpoints
- **End-to-End Tests**: Test complete workflows

### Writing Tests

```python
# tests/test_example.py
import pytest
from src.claude_code_adapter.utils import example_function

def test_example_function():
    """Test example function"""
    result = example_function("input")
    assert result == "expected_output"
```

## 🔧 Code Quality

### Code Formatting

```bash
# Format code
make format

# Check formatting
make format-check
```

### Code Checks

```bash
# Run all checks
make lint

# Run individually
flake8 src/ tests/
mypy src/
```

### Code Standards

- Use Black for code formatting
- Use isort for import sorting
- Use flake8 for code linting
- Use mypy for type checking

## 🚀 Development Server

### Starting the Development Server

```bash
# Using Makefile
make run

# Or run directly
python -m uvicorn src.claude_code_adapter.app:app --host 0.0.0.0 --port 8000 --reload
```

### Hot Reload

The development server supports hot reloading, automatically restarting on code changes.

## 📝 Code Contribution

> 💡 **Quick Contribution Guide**: See [CONTRIBUTING.md](/docs/en/CONTRIBUTING.md) for a concise contribution process and guidelines.

### Detailed Contribution Process

#### 1. Fork the Repository
Fork the project on GitHub to your account.

#### 2. Create a Branch
```bash
git checkout -b feature/your-feature-name
```

#### 3. Development Process
```bash
# Write code
# Add tests
# Update documentation

# Run tests and checks
make test
make lint
make format
```

#### 4. Commit Changes
```bash
git add .
git commit -m "feat: add new feature"
git push origin feature/your-feature-name
```

#### 5. Create Pull Request
Create a Pull Request on GitHub.

### Commit Message Guidelines

Follow [Conventional Commits](https://www.conventionalcommits.org/) standards:

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation update
- `style`: Code formatting
- `refactor`: Code refactoring
- `test`: Test additions
- `chore`: Build process or auxiliary tool changes

Examples:
```
feat: add support for conda environment
fix: resolve encoding issue in setup scripts
docs: update installation guide
```

## 🐳 Docker Development

### Building Development Image

```bash
docker build -t claude-code-adapter:dev .
```

### Running Development Container

```bash
docker run -p 8000:8000 -v $(pwd):/app claude-code-adapter:dev
```

### Using docker-compose

```bash
docker-compose up -d
```

## 📊 Performance Optimization

### Performance Profiling

```bash
# Install performance profiling tool
pip install py-spy

# Profile performance
py-spy top --pid <process_id>
```

### Memory Profiling

```bash
# Install memory profiling tool
pip install memory-profiler

# Profile memory usage
python -m memory_profiler script.py
```

## 🔍 Debugging

### Logging

```python
import logging

# Set logging level
logging.basicConfig(level=logging.DEBUG)

# Use logger
logger = logging.getLogger(__name__)
logger.debug("Debug message")
```

### Breakpoint Debugging

```python
# Using pdb
import pdb; pdb.set_trace()

# Or using ipdb
import ipdb; ipdb.set_trace()
```

## 📚 Documentation

### Generating Documentation

```bash
# Start documentation server
make docs

# Build documentation
make docs-build
```

### Writing Documentation

- Use Markdown format
- Include code examples
- Keep documentation updated

## 🚨 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Check Python path
   export PYTHONPATH=$PWD:$PYTHONPATH
   ```

2. **Dependency Conflicts**
   ```bash
   # Recreate virtual environment
   rm -rf venv
   python -m venv venv
   pip install -r requirements-dev.txt
   ```

3. **Test Failures**
   ```bash
   # Check test environment
   python scripts/check_env.py
   ```

### Getting Help

- Check [Issues](https://github.com/wangfumin1/claude-code-adapter-fastapi/issues)
- Create a new Issue
- Contact maintainers

## 🔗 Related Documentation

- [🚀 Quick Start Guide](getting-started.md) - Installation and basic usage
- [⚙️ Configuration Guide](configuration.md) - Detailed configuration options
- [📚 API Documentation](api.md) - API reference
- [🤝 Contribution Guidelines](/CONTRIBUTING.md) - Concise contribution process and guidelines

## 🔄 Version Management

### Versioning Scheme

Follow [Semantic Versioning](https://semver.org/):

- `MAJOR`: Breaking API changes
- `MINOR`: Backward-compatible feature additions
- `PATCH`: Backward-compatible bug fixes

### Release Process

1. Update version number
2. Update CHANGELOG
3. Create Release
4. Build and publish package

## 📋 Development Checklist

- [ ] Code passes all tests
- [ ] Code is properly formatted
- [ ] Type checks pass
- [ ] Documentation is updated
- [ ] Commit messages follow guidelines
- [ ] No security vulnerabilities
- [ ] Performance tests pass
