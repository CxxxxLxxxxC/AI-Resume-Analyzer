import json
import os
import hashlib
from pathlib import Path
from typing import Any, Dict, Optional
import time

def _safe_filename(key: str) -> str:
    """
    将缓存键转换为安全的文件名
    使用hash避免特殊字符问题
    """
    return hashlib.md5(key.encode('utf-8')).hexdigest()

class CacheManager:
    """简化的缓存管理器（使用文件系统）"""

    def __init__(self, cache_dir: str = "./cache"):
        """
        初始化缓存管理器
        :param cache_dir: 缓存目录
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
    """简化的缓存管理器（使用文件系统）"""

    def __init__(self, cache_dir: str = "./cache"):
        """
        初始化缓存管理器
        :param cache_dir: 缓存目录
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def get_cache(self, key: str) -> Optional[Dict[str, Any]]:
        """
        获取缓存
        :param key: 缓存键
        :return: 缓存内容
        """
        safe_key = _safe_filename(key)
        cache_file = self.cache_dir / f"{safe_key}.json"

        if not cache_file.exists():
            return None

        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 检查是否过期
            if 'expire_time' in data and time.time() > data['expire_time']:
                cache_file.unlink()  # 删除过期文件
                return None

            return data['content']
        except:
            return None

    def set_cache(self, key: str, content: Any, expire: int = 3600):
        """
        设置缓存
        :param key: 缓存键
        :param content: 缓存内容
        :param expire: 过期时间（秒）
        """
        safe_key = _safe_filename(key)
        cache_file = self.cache_dir / f"{safe_key}.json"

        data = {
            'content': content,
            'expire_time': time.time() + expire
        }

        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def clear_cache(self):
        """
        清空缓存
        """
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()

# 创建全局缓存管理器实例
cache_manager = CacheManager()