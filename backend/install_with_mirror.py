#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
使用国内镜像安装依赖的脚本
"""

import subprocess
import sys
import os

def install_with_mirror():
    """使用清华镜像安装依赖"""
    print("使用国内镜像安装依赖...")

    # 设置国内镜像
    os.environ["PIP_INDEX_URL"] = "https://pypi.tuna.tsinghua.edu.cn/simple"

    # 安装基础包
    packages = [
        "fastapi",
        "uvicorn[standard]",
        "PyPDF2",
        "redis",
        "pydantic",
        "orjson",
        "python-dateutil",
        "aiofiles",
        "loguru",
        "requests",
        "typing-extensions"
    ]

    print("\n安装基础包...")
    for package in packages:
        print(f"  正在安装 {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"  ✓ {package} 安装成功")
        except Exception as e:
            print(f"  ✗ {package} 安装失败: {e}")

    # 安装机器学习包（可能需要较长时间）
    ml_packages = [
        "transformers==4.35.2",
        "accelerate==0.25.0",
        "sentence-transformers==2.2.2"
    ]

    print("\n安装机器学习包...")
    for package in ml_packages:
        print(f"  正在安装 {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"  ✓ {package} 安装成功")
        except Exception as e:
            print(f"  ✗ {package} 安装失败: {e}")

    # 安装PyTorch（CPU版本）
    print("\n安装PyTorch（CPU版本）...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            "torch==2.1.0",
            "torchvision==0.16.0",
            "torchaudio==2.1.0",
            "--index-url", "https://download.pytorch.org/whl/cpu"
        ])
        print("  ✓ PyTorch 安装成功")
    except Exception as e:
        print(f"  ✗ PyTorch 安装失败: {e}")

    # 安装其他工具
    dev_packages = [
        "pytest",
        "pytest-asyncio",
        "httpx",
        "black",
        "isort",
        "flake8",
        "gunicorn"
    ]

    print("\n安装开发工具...")
    for package in dev_packages:
        print(f"  正在安装 {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"  ✓ {package} 安装成功")
        except Exception as e:
            print(f"  ✗ {package} 安装失败: {e}")

    print("\n" + "="*50)
    print("所有依赖安装完成！")
    print("="*50)

if __name__ == "__main__":
    install_with_mirror()