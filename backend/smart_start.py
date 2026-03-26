#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
智能简历分析系统 - 智能启动脚本
自动处理模型下载和依赖问题
"""

import os
import sys
import time
import subprocess
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    print(f"Python版本: {version.major}.{version.minor}.{version.micro}")
    return version.major >= 3 and version.minor >= 8

def install_requirements():
    """安装依赖"""
    print("正在安装依赖...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ 依赖安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ 依赖安装失败: {e}")
        return False

def check_model_download():
    """检查模型是否已下载"""
    model_dir = Path("./models")
    if model_dir.exists():
        model_files = list(model_dir.glob("*.bin")) + list(model_dir.glob("*.pt"))
        if model_files:
            print(f"✓ 找到已下载的模型文件: {len(model_files)} 个")
            return True
    print("⚠ 未找到本地模型文件")
    return False

def create_offline_mode():
    """创建离线模式响应"""
    offline_responses = {
        "/api/upload": {
            "error": "AI模型未下载",
            "message": "正在首次使用，需要下载AI模型（约500MB）...",
            "solution": [
                "1. 请保持网络连接",
                "2. 如果网络较慢，可能需要几分钟时间",
                "3. 下载完成后即可使用"
            ],
            "offline_mode": True
        }
    }
    return offline_responses

def start_app():
    """启动应用"""
    print("\n" + "="*50)
    print("启动AI简历分析系统")
    print("="*50)

    # 检查Python版本
    if not check_python_version():
        print("❌ 需要Python 3.8或更高版本")
        return False

    # 安装依赖
    if not install_requirements():
        print("❌ 依赖安装失败")
        return False

    # 检查模型
    if not check_model_download():
        print("\n⚠ 注意：首次运行需要下载AI模型（约500MB）")
        print("这可能需要几分钟时间，请保持网络连接")
        print("\n如果下载失败，系统将在离线模式下运行")
        print("您可以稍后重新启动应用以完成模型下载")
        time.sleep(3)

    # 设置环境变量
    os.environ["TRANSFORMERS_OFFLINE"] = "0"
    os.environ["HF_DATASETS_OFFLINE"] = "0"

    # 启动应用
    print("\n🚀 启动服务...")
    print("API地址: http://localhost:8000")
    print("API文档: http://localhost:8000/docs")
    print("\n按 Ctrl+C 停止服务")
    print("="*50)

    try:
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n服务已停止")

    return True

if __name__ == "__main__":
    start_app()