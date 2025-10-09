#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环境检查脚本
检查Python环境和依赖是否正确安装
"""
import importlib
import io
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")


def check_python_version() -> bool:
    """检查Python版本"""
    version = sys.version_info
    print(f"Python版本: {version.major}.{version.minor}.{version.micro}")

    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ Python版本过低，需要3.9或更高版本")
        return False
    else:
        print("✅ Python版本符合要求")
        return True


def check_virtual_env() -> bool:
    """检查是否在虚拟环境中"""
    in_venv = hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    )
    if in_venv:
        print("✅ 当前在虚拟环境中")
        return True
    else:
        print("⚠️ 当前不在虚拟环境中，建议使用虚拟环境")
        return False


def check_dependencies() -> bool:
    """检查依赖包"""
    required_packages = [
        "fastapi",
        "uvicorn",
        "pydantic",
        "pydantic_settings",
        "openai",
        "yaml",
    ]

    missing_packages = []

    for package in required_packages:
        try:
            if package == "yaml":
                importlib.import_module("yaml")
            else:
                importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)

    if missing_packages:
        print(f"\n缺少以下依赖包: {', '.join(missing_packages)}")
        print("请运行: pip install -r requirements.txt")
        return False
    else:
        print("✅ 必要依赖包已安装")
        return True


def check_config_files() -> bool:
    """检查配置文件"""
    config_files = ["config.yaml"]
    missing_files = []

    for file in config_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"⚠️ {file} 不存在")
            missing_files.append(file)

    if missing_files:
        print(f"\n缺少配置文件: {', '.join(missing_files)}")
        if "config.yaml" in missing_files:
            print("请复制 config.yaml 并修改配置")
        return False
    else:
        print("✅ 配置文件存在")
        return True


def check_project_structure() -> bool:
    """检查项目结构"""
    required_dirs = ["src", "tests", "docs"]
    required_files = ["src/claude_code_adapter/app.py", "requirements.txt"]

    all_good = True

    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"✅ {dir_path}/")
        else:
            print(f"❌ {dir_path}/ 不存在")
            all_good = False

    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} 不存在")
            all_good = False

    return all_good


def main() -> None:
    """主函数"""
    print("🔍 环境检查")
    print("=" * 50)

    checks = [
        ("Python版本", check_python_version),
        ("虚拟环境", check_virtual_env),
        ("依赖包", check_dependencies),
        ("配置文件", check_config_files),
        ("项目结构", check_project_structure),
    ]

    results = []
    for name, check_func in checks:
        print(f"\n📋 检查 {name}:")
        result = check_func()
        results.append(result)

    print("\n" + "=" * 50)
    if all(results):
        print("🎉 环境检查通过！可以开始使用项目了。")
        print("\n启动服务:")
        print("make run")
        print("或")
        print("python -m uvicorn src.claude_code_adapter.app:app --host 0.0.0.0")
    else:
        print("❌ 环境检查未通过，请根据上述提示修复问题。")
        print("\n快速修复:")
        print("1. 运行设置脚本: ./scripts/setup.sh（Linux/macOS）")
        print("              或 scripts\\setup.bat（Windows）")
        print("2. 或手动安装: pip install -r requirements.txt")
        print("3. 修改配置文件: config.yaml")


if __name__ == "__main__":
    main()
