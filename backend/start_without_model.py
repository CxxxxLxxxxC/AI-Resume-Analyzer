#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
启动简历分析系统（不等待模型下载）
"""

import os
import sys
import uvicorn
from app import app

if __name__ == "__main__":
    print("="*50)
    print("AI简历分析系统")
    print("="*50)
    print("注意：当前为离线模式")
    print("AI模型未下载，部分功能可能不可用")
    print("API文档: http://localhost:8000/docs")
    print("="*50)

    # 强制离线模式
    os.environ["TRANSFORMERS_OFFLINE"] = "1"

    # 启动服务器
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )