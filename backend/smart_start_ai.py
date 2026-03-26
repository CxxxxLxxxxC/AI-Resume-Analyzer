#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
智能启动AI简历分析系统（自动选择本地或在线模型）
"""

import os
import sys
import uvicorn
from pathlib import Path
import torch

def check_local_model():
    """检查本地模型是否存在"""
    cache_path = Path.home() / ".cache" / "huggingface" / "hub"
    model_cache_dir = cache_path / "models--bert-base-chinese"

    if model_cache_dir.exists():
        # 检查关键文件
        required_files = ["config.json", "tokenizer_config.json", "vocab.txt"]
        has_files = all((model_cache_dir / "snapshots" / "8f23c25b06e129b6c986331a13d8d025a92cf0ea" / f).exists()
                       for f in required_files)

        if has_files:
            print("✓ 找到完整的本地BERT模型")
            return True

    return False

def setup_model_environment():
    """设置模型加载环境"""
    cache_dir = str(Path.home() / ".cache" / "huggingface")
    os.environ["HF_DATASETS_OFFLINE"] = "0"  # 允许回退到在线
    os.environ["TRANSFORMERS_OFFLINE"] = "0"
    os.environ["HF_HOME"] = cache_dir
    os.environ["HF_DATASETS_CACHE"] = cache_dir
    os.environ["TRANSFORMERS_CACHE"] = cache_dir

def test_model_loading():
    """测试模型加载"""
    try:
        print("测试BERT模型加载...")

        # 临时修改导入以使用本地版本
        sys.path.insert(0, 'utils')

        if check_local_model():
            print("使用本地模型加载器")
            from bert_optimizer_local import BertOptimizerLocal
            optimizer = BertOptimizerLocal()
        else:
            print("使用标准模型加载器")
            from bert_optimizer import BertOptimizer
            optimizer = BertOptimizer()

        print("✓ 模型测试通过")
        return True

    except Exception as e:
        print(f"✗ 模型测试失败: {e}")
        return False

def main():
    print("=" * 60)
    print("AI简历分析系统 - 智能启动")
    print("=" * 60)

    # 检查本地模型
    if check_local_model():
        print("✓ 检测到本地BERT模型")
        print("  路径: ~/.cache/huggingface/hub/models--bert-base-chinese")
        print("  大小: ~400MB")
    else:
        print("⚠ 未检测到本地BERT模型")
        print("  将需要从网络下载（约500MB）")
        print("  建议先运行离线模式: start_offline.bat")

    # 设置环境
    setup_model_environment()

    print("\n正在启动服务...")

    # 启动应用
    try:
        uvicorn.run(
            "app:app",
            host="0.0.0.0",
            port=8000,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n服务已停止")
    except Exception as e:
        print(f"\n启动失败: {e}")
        print("请尝试: start_offline.bat")

if __name__ == "__main__":
    main()