#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
清理BERT模型缓存
"""

import os
import shutil
import sys
from pathlib import Path

def clear_bert_cache():
    """清理BERT模型缓存"""
    cache_paths = [
        Path.home() / ".cache" / "huggingface",
        Path.cwd() / "models",
        Path.cwd() / ".cache"
    ]

    cleared = False

    for cache_path in cache_paths:
        if cache_path.exists():
            print(f"找到缓存目录: {cache_path}")

            # 删除bert-base-chinese相关的缓存
            bert_dir = cache_path / "hub" / "models--bert-base-chinese"
            if bert_dir.exists():
                print(f"删除BERT缓存: {bert_dir}")
                try:
                    shutil.rmtree(bert_dir)
                    print("✓ 清理成功")
                    cleared = True
                except Exception as e:
                    print(f"✗ 清理失败: {e}")
                    try:
                        # Windows可能需要文件句柄关闭
                        import time
                        time.sleep(2)
                        shutil.rmtree(bert_dir, ignore_errors=True)
                        print("✓ 重试清理成功")
                        cleared = True
                    except Exception as e2:
                        print(f"✗ 重试也失败: {e2}")

    if not cleared:
        print("未找到BERT缓存文件")

    print("\n请重新启动应用以重新下载模型")

if __name__ == "__main__":
    print("=== 清理BERT模型缓存 ===")
    clear_bert_cache()