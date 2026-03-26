#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
启动AI简历分析系统（使用BERT模型）
"""

import os
import sys
import subprocess
import uvicorn
from app import app

def test_dependencies():
    """测试依赖是否安装"""
    try:
        import torch
        import transformers
        print("✓ 依赖包检查通过")
        return True
    except ImportError as e:
        print(f"✗ 缺少依赖包: {e}")
        return False

def test_bert_model():
    """测试BERT模型"""
    try:
        from transformers import BertTokenizer, BertForTokenClassification
        print("✓ 正在测试BERT模型加载...")

        model_name = "bert-base-chinese"
        tokenizer = BertTokenizer.from_pretrained(model_name)
        model = BertForTokenClassification.from_pretrained(model_name)

        print("✓ BERT模型加载成功")
        return True
    except Exception as e:
        print(f"✗ BERT模型加载失败: {e}")
        return False

def main():
    print("=" * 60)
    print("AI简历分析系统 - AI模式启动")
    print("=" * 60)

    # 测试依赖
    if not test_dependencies():
        print("请先运行依赖安装脚本")
        return

    # 测试模型
    if not test_bert_model():
        print("模型未准备好，将使用离线模式")
        print("运行 'python start_offline.bat' 使用离线模式")
        return

    print("\n🚀 启动AI增强版服务...")
    print("API地址: http://localhost:8000")
    print("API文档: http://localhost:8000/docs")
    print("\n注意: 首次使用AI功能可能需要几秒钟")
    print("按 Ctrl+C 停止服务")
    print("=" * 60)

    try:
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n服务已停止")

if __name__ == "__main__":
    main()