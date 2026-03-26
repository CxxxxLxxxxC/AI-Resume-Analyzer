#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import shutil
import os

def copy_model_file():
    """将项目中的pytorch_model.bin复制到缓存目录"""
    print("=== 复制模型文件 ===\n")

    # 源文件（项目目录）
    src_file = Path.cwd() / "models" / "bert-base-chinese" / "pytorch_model.bin"

    # 目标位置（缓存目录）
    cache_dir = Path.home() / ".cache" / "huggingface" / "hub"
    model_cache_dir = cache_dir / "models--bert-base-chinese"
    blobs_dir = model_cache_dir / "blobs"

    # 目标文件名（需要计算正确的hash）
    # 我们先复制，然后链接到正确的位置
    target_file = blobs_dir / "pytorch_model.bin"

    print(f"源文件: {src_file}")
    print(f"目标目录: {blobs_dir}")
    print()

    if not src_file.exists():
        print("❌ 源文件不存在！")
        return

    try:
        # 确保目标目录存在
        blobs_dir.mkdir(parents=True, exist_ok=True)

        # 复制文件
        print("正在复制文件...")
        shutil.copy2(src_file, target_file)
        print(f"✓ 文件已复制到: {target_file}")

        # 计算文件大小
        size = target_file.stat().st_size
        print(f"文件大小: {size:,} bytes ({size/1024/1024:.1f} MB)")

        # 创建链接到快照目录
        snapshot_dir = model_cache_dir / "snapshots" / "8f23c25b06e129b6c986331a13d8d025a92cf0ea"
        snapshot_file = snapshot_dir / "pytorch_model.bin"

        if not snapshot_file.exists():
            print(f"创建链接到: {snapshot_file}")
            if os.name == 'nt':
                # Windows: 创建硬链接
                import ctypes
                ctypes.CreateHardLink(str(snapshot_file), str(target_file), None)
            else:
                # Unix-like: 创建符号链接
                snapshot_file.symlink_to(target_file)

        print("\n✅ 模型文件复制完成！")
        print("\n现在可以启动服务了:")
        print("python final_start.bat")

    except Exception as e:
        print(f"❌ 复制失败: {e}")

if __name__ == "__main__":
    copy_model_file()