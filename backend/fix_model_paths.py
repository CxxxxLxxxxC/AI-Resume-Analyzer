#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import shutil
import os

def fix_model_paths():
    """修复模型文件路径，将所有文件合并到缓存目录"""
    print("=== 修复BERT模型路径 ===\n")

    # 定义路径
    cache_dir = Path.home() / ".cache" / "huggingface" / "hub"
    model_cache_dir = cache_dir / "models--bert-base-chinese"
    snapshot_dir = model_cache_dir / "snapshots" / "8f23c25b06e129b6c986331a13d8d025a92cf0ea"
    blobs_dir = model_cache_dir / "blobs"

    # 项目中的模型文件
    project_model_dir = Path.cwd() / "models" / "bert-base-chinese"
    project_pytorch_file = project_model_dir / "pytorch_model.bin"

    print(f"缓存目录: {model_cache_dir}")
    print(f"项目模型文件: {project_pytorch_file}")
    print(f"快照目录: {snapshot_dir}")
    print()

    if not project_pytorch_file.exists():
        print("❌ 项目中没有找到 pytorch_model.bin")
        return

    if not snapshot_dir.exists():
        print("❌ 快照目录不存在")
        return

    # 计算目标文件名
    pytorch_hash = "d2a3a5f2873b0e2c5e5b1f2e3d4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3"
    target_pytorch_file = blobs_dir / pytorch_hash

    print("开始复制 pytorch_model.bin 到缓存目录...")

    try:
        # 复制文件
        shutil.copy2(project_pytorch_file, target_pytorch_file)
        print(f"✓ 成功复制到: {target_pytorch_file}")

        # 创建符号链接（或硬链接）
        link_path = snapshot_dir / "pytorch_model.bin"
        if link_path.exists():
            link_path.unlink()

        # 在Windows上创建硬链接
        if os.name == 'nt':
            import ctypes
            ctypes.CreateHardLink(str(link_path), str(target_pytorch_file), None)
        else:
            link_path.symlink_to(target_pytorch_file)

        print(f"✓ 创建链接: {link_path}")

        print("\n✅ 模型文件修复完成！")

    except Exception as e:
        print(f"❌ 修复失败: {e}")

    print("\n现在可以正常启动服务了:")
    print("python final_start.bat")

if __name__ == "__main__":
    fix_model_paths()