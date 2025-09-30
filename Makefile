.PHONY: help install install-dev test lint format clean run docker-build docker-run

help: ## 显示帮助信息
	@echo "可用的命令:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## 创建虚拟环境并安装依赖
	python -m venv venv
	@echo "虚拟环境已创建，请运行以下命令激活："
	@echo "Windows: venv\\Scripts\\activate"
	@echo "macOS/Linux: source venv/bin/activate"
	@echo "然后运行: make install"

setup-windows-bat: ## Windows快速设置（批处理）
	scripts/setup.bat

setup-conda: ## 使用conda创建环境
	conda create -n claude-adapter python=3.11 -y
	@echo "conda环境已创建，请运行: conda activate claude-adapter"
	@echo "然后运行: make install"

setup-poetry: ## 使用poetry创建环境
	poetry install
	@echo "poetry环境已创建，请运行: poetry shell"

poetry-install: ## 使用poetry安装依赖
	poetry install

poetry-run: ## 使用poetry运行应用
	poetry run python -m uvicorn src.claude_code_adapter.app:app --host 0.0.0.0 --port 8000

poetry-test: ## 使用poetry运行测试
	poetry run pytest tests/ -v

check-env: ## 检查环境配置
	python scripts/check_env.py

install: ## 安装生产依赖
	pip install -r requirements.txt

install-dev: ## 安装开发依赖
	pip install -r requirements-dev.txt

test: ## 运行测试
	pytest tests/ -v

test-cov: ## 运行测试并生成覆盖率报告
	pytest tests/ -v --cov=src/ --cov-report=html --cov-report=term

lint: ## 运行代码检查
	flake8 src/ tests/
	mypy src/

format: ## 格式化代码
	black src/ tests/
	isort src/ tests/

format-check: ## 检查代码格式
	black --check src/ tests/
	isort --check-only src/ tests/

clean: ## 清理临时文件
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/

run: ## 运行应用
	python -m uvicorn src.claude_code_adapter.app:app --host 0.0.0.0 --port 8000 --reload

run-prod: ## 运行生产环境
	python -m uvicorn src.claude_code_adapter.app:app --host 0.0.0.0 --port 8000

docker-build: ## 构建Docker镜像
	docker build -t claude-code-adapter .

docker-run: ## 运行Docker容器
	docker run -p 8000:8000 -v $(PWD)/config.yaml:/app/config.yaml claude-code-adapter

docker-compose-up: ## 使用docker-compose启动
	docker-compose up -d

docker-compose-down: ## 停止docker-compose服务
	docker-compose down

docs: ## 启动文档服务器
	mkdocs serve

docs-build: ## 构建文档
	mkdocs build

docs-deploy: ## 部署文档到GitHub Pages
	mkdocs gh-deploy

pre-commit: ## 安装pre-commit钩子
	pre-commit install

pre-commit-run: ## 运行pre-commit检查
	pre-commit run --all-files
