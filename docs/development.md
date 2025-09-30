# 开发指南

本文档为开发者提供详细的开发环境设置、代码结构和贡献指南。

## 🛠️ 开发环境设置

### 1. 克隆项目

```bash
git clone https://github.com/wangfumin1/claude-code-adapter-fastapi.git
cd claude-code-adapter-fastapi
```

### 2. 创建开发环境

```bash
# 使用自动设置脚本
# Windows:
scripts\setup.bat
# Linux/macOS:
./scripts/setup.sh

# 或手动设置
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3. 安装开发依赖

```bash
pip install -r requirements-dev.txt
```

### 4. 安装pre-commit钩子

```bash
pre-commit install
```

## 📁 项目结构

```
claude-code-adapter-fastapi/
├── src/
│   └── claude_code_adapter/
│       ├── __init__.py          # 包初始化
│       ├── app.py              # FastAPI应用主文件
│       ├── config.py           # 配置管理
│       ├── models.py           # 数据模型
│       ├── services.py         # 业务逻辑服务
│       └── utils.py            # 工具函数
├── tests/                      # 测试文件
│   ├── __init__.py
│   ├── test_app.py            # 应用测试
│   └── test_utils.py          # 工具函数测试
├── scripts/                    # 脚本文件
│   ├── setup.bat               # Windows设置脚本
│   ├── setup.sh               # Linux/macOS设置脚本
│   ├── check_env.py           # 环境检查
│   └── start.py               # 启动脚本
├── docs/                       # 文档
├── docker/                     # Docker相关文件
├── .github/workflows/          # CI/CD配置
├── config.yaml                # 配置文件
├── requirements.txt           # 生产依赖
├── requirements-dev.txt       # 开发依赖
├── pyproject.toml            # 项目配置
├── Makefile                  # 构建脚本
└── README.md                 # 项目说明
```

## 🧪 测试

### 运行测试

```bash
# 运行所有测试
make test

# 或使用pytest
pytest tests/ -v

# 运行特定测试
pytest tests/test_utils.py -v

# 生成覆盖率报告
make test-cov
```

### 测试结构

- **单元测试**: 测试单个函数和类
- **集成测试**: 测试API端点
- **端到端测试**: 测试完整流程

### 编写测试

```python
# tests/test_example.py
import pytest
from src.claude_code_adapter.utils import example_function

def test_example_function():
    """测试示例函数"""
    result = example_function("input")
    assert result == "expected_output"
```

## 🔧 代码质量

### 代码格式化

```bash
# 格式化代码
make format

# 检查格式
make format-check
```

### 代码检查

```bash
# 运行所有检查
make lint

# 单独运行
flake8 src/ tests/
mypy src/
```

### 代码规范

- 使用Black进行代码格式化
- 使用isort进行导入排序
- 使用flake8进行代码检查
- 使用mypy进行类型检查

## 🚀 开发服务器

### 启动开发服务器

```bash
# 使用Makefile
make run

# 或直接运行
python -m uvicorn src.claude_code_adapter.app:app --host 0.0.0.0 --port 8000 --reload
```

### 热重载

开发服务器支持热重载，修改代码后自动重启。

## 📝 代码贡献

> 💡 **快速贡献指南**: 查看 [CONTRIBUTING.md](../../CONTRIBUTING.md) 获取简洁的贡献流程和规范。

### 详细贡献流程

#### 1. Fork项目
在GitHub上Fork项目到你的账户。

#### 2. 创建分支
```bash
git checkout -b feature/your-feature-name
```

#### 3. 开发过程
```bash
# 编写代码
# 添加测试
# 更新文档

# 运行测试和检查
make test
make lint
make format
```

#### 4. 提交更改
```bash
git add .
git commit -m "feat: add new feature"
git push origin feature/your-feature-name
```

#### 5. 创建Pull Request
在GitHub上创建Pull Request。

### 提交信息规范

使用[Conventional Commits](https://www.conventionalcommits.org/)规范：

- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式
- `refactor`: 重构
- `test`: 测试
- `chore`: 构建过程或辅助工具的变动

示例：
```
feat: add support for conda environment
fix: resolve encoding issue in setup scripts
docs: update installation guide
```

## 🐳 Docker开发

### 构建开发镜像

```bash
docker build -t claude-code-adapter:dev .
```

### 运行开发容器

```bash
docker run -p 8000:8000 -v $(pwd):/app claude-code-adapter:dev
```

### 使用docker-compose

```bash
docker-compose up -d
```

## 📊 性能优化

### 性能分析

```bash
# 安装性能分析工具
pip install py-spy

# 分析性能
py-spy top --pid <process_id>
```

### 内存分析

```bash
# 安装内存分析工具
pip install memory-profiler

# 分析内存使用
python -m memory_profiler script.py
```

## 🔍 调试

### 日志调试

```python
import logging

# 设置日志级别
logging.basicConfig(level=logging.DEBUG)

# 使用日志
logger = logging.getLogger(__name__)
logger.debug("Debug message")
```

### 断点调试

```python
# 使用pdb
import pdb; pdb.set_trace()

# 或使用ipdb
import ipdb; ipdb.set_trace()
```

## 📚 文档

### 生成文档

```bash
# 启动文档服务器
make docs

# 构建文档
make docs-build
```

### 编写文档

- 使用Markdown格式
- 包含代码示例
- 保持文档更新

## 🚨 故障排除

### 常见问题

1. **导入错误**
   ```bash
   # 检查Python路径
   export PYTHONPATH=$PWD:$PYTHONPATH
   ```

2. **依赖冲突**
   ```bash
   # 重新创建虚拟环境
   rm -rf venv
   python -m venv venv
   pip install -r requirements-dev.txt
   ```

3. **测试失败**
   ```bash
   # 检查测试环境
   python scripts/check_env.py
   ```

### 获取帮助

- 查看[Issues](https://github.com/wangfumin1/claude-code-adapter-fastapi/issues)
- 创建新的Issue
- 联系维护者

## 🔗 相关文档

- [🚀 快速开始指南](getting-started.md) - 安装和基本使用
- [⚙️ 配置说明](configuration.md) - 详细配置选项  
- [📚 API文档](api.md) - API接口参考
- [🤝 贡献指南](../../CONTRIBUTING.md) - 简洁的贡献流程和规范

## 🔄 版本管理

### 版本号规范

使用[语义化版本](https://semver.org/)：

- `MAJOR`: 不兼容的API修改
- `MINOR`: 向下兼容的功能性新增
- `PATCH`: 向下兼容的问题修正

### 发布流程

1. 更新版本号
2. 更新CHANGELOG
3. 创建Release
4. 构建和发布包

## 📋 开发检查清单

- [ ] 代码通过所有测试
- [ ] 代码格式化正确
- [ ] 类型检查通过
- [ ] 文档已更新
- [ ] 提交信息规范
- [ ] 无安全漏洞
- [ ] 性能测试通过
