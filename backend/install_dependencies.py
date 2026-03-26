"""
智能简历分析系统 - 依赖安装脚本
自动检测环境并安装合适的PyTorch版本
"""

import subprocess
import sys
import os

def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    print(f"Python版本: {version.major}.{version.minor}.{version.micro}")
    return version

def install_basic_packages():
    """安装基础包"""
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

    print("\n正在安装基础包...")
    for package in packages:
        print(f"安装 {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

    print("基础包安装完成!")

def install_ml_packages():
    """安装机器学习包"""
    packages = [
        "transformers",
        "accelerate",
        "sentence-transformers"
    ]

    print("\n正在安装机器学习包...")
    for package in packages:
        print(f"安装 {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

    print("机器学习包安装完成!")

def install_pytorch():
    """安装PyTorch - 自动选择CPU或CUDA版本"""
    import platform

    print("\n检测系统环境...")
    system = platform.system()
    print(f"操作系统: {system}")

    if system == "Linux":
        # 尝试检测NVIDIA GPU
        try:
            result = subprocess.run(['nvidia-smi'],
                                   capture_output=True,
                                   text=True,
                                   timeout=10)
            if result.returncode == 0:
                print("检测到NVIDIA GPU，安装CUDA支持的PyTorch")
                subprocess.check_call([sys.executable, "-m", "pip", "install", "torch", "torchvision", "torchaudio", "--index-url", "https://download.pytorch.org/whl/cu121"])
            else:
                print("未检测到NVIDIA GPU，安装CPU版本的PyTorch")
                subprocess.check_call([sys.executable, "-m", "pip", "install", "torch", "torchvision", "torchaudio", "--index-url", "https://download.pytorch.org/whl/cpu"])
        except:
            print("无法检测GPU，安装CPU版本的PyTorch")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "torch", "torchvision", "torchaudio", "--index-url", "https://download.pytorch.org/whl/cpu"])
    else:
        # Windows或其他系统安装CPU版本
        print("安装CPU版本的PyTorch")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "torch", "torchvision", "torchaudio"])

def install_testing_packages():
    """安装测试相关包"""
    packages = [
        "pytest",
        "pytest-asyncio",
        "httpx"
    ]

    print("\n正在安装测试包...")
    for package in packages:
        print(f"安装 {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

    print("测试包安装完成!")

def install_dev_tools():
    """安装开发工具"""
    packages = [
        "black",
        "isort",
        "flake8"
    ]

    print("\n正在安装开发工具...")
    for package in packages:
        print(f"安装 {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

    print("开发工具安装完成!")

def main():
    """主安装流程"""
    print("=" * 50)
    print("智能简历分析系统 - 依赖安装程序")
    print("=" * 50)

    # 检查Python版本
    version = check_python_version()

    # 安装基础包
    install_basic_packages()

    # 安装机器学习包
    install_ml_packages()

    # 安装PyTorch
    install_pytorch()

    # 安装测试包
    install_testing_packages()

    # 安装开发工具
    install_dev_tools()

    print("\n" + "=" * 50)
    print("所有依赖安装完成!")
    print("现在可以运行项目了")
    print("=" * 50)

if __name__ == "__main__":
    main()