import torch
from transformers import BertTokenizer, BertForTokenClassification
from typing import Optional
import os
from pathlib import Path

class BertOptimizer:
    def __init__(self, model_name: str = "bert-base-chinese"):
        """
        初始化BERT优化器
        :param model_name: BERT模型名称
        """
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self.device = None
        self._load_model()

    def _load_model(self):
        """
        加载BERT模型（支持多个路径）
        """
        try:
            # 设置设备
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

            # 定义可能的模型路径
            possible_paths = []

            # 1. 缓存目录路径
            cache_dir = Path.home() / ".cache" / "huggingface" / "hub"
            model_cache_dir = cache_dir / "models--bert-base-chinese"
            snapshot_dir = model_cache_dir / "snapshots" / "8f23c25b06e129b6c986331a13d8d025a92cf0ea"

            if snapshot_dir.exists():
                possible_paths.append(snapshot_dir)

            # 2. 项目目录路径
            project_model_dir = Path.cwd() / "models" / "bert-base-chinese"
            if project_model_dir.exists():
                possible_paths.append(project_model_dir)

            print(f"尝试从以下路径加载BERT模型 '{self.model_name}':")
            for i, path in enumerate(possible_paths, 1):
                print(f"  {i}. {path}")

            # 尝试每个路径
            loaded = False
            for path in possible_paths:
                try:
                    print(f"\n尝试从路径加载: {path}")
                    self.tokenizer = BertTokenizer.from_pretrained(str(path))
                    self.model = BertForTokenClassification.from_pretrained(str(path))
                    print(f"✓ 从 {path} 加载成功！")
                    loaded = True
                    break
                except Exception as e:
                    print(f"✗ 从 {path} 加载失败: {e}")
                    continue

            if not loaded:
                # 如果所有路径都失败，尝试在线加载
                print("\n所有本地路径都失败，尝试在线加载...")
                self._load_online()

            # 移动到设备
            self.model.to(self.device)

            # 设置为评估模式
            self.model.eval()

            print(f"\n✓ BERT模型 {self.model_name} 加载成功，使用设备: {self.device}")

        except Exception as e:
            print(f"✗ 模型加载失败: {str(e)}")
            raise Exception(f"BERT模型初始化失败: {str(e)}")

    def _load_online(self):
        """
        在线加载BERT模型
        """
        print("尝试从HuggingFace在线加载...")
        print("⚠ 注意：需要网络连接")
        self.tokenizer = BertTokenizer.from_pretrained(self.model_name)
        self.model = BertForTokenClassification.from_pretrained(self.model_name)

    def optimize_inference(self, text: str, max_length: int = 512) -> torch.Tensor:
        """
        优化BERT推理过程
        :param text: 输入文本
        :param max_length: 最大长度
        :return: 模型输出
        """
        try:
            # 分词
            inputs = self.tokenizer(
                text,
                padding=True,
                truncation=True,
                max_length=max_length,
                return_tensors="pt"
            )

            # 移动到设备
            inputs = {k: v.to(self.device) for k, v in inputs.items()}

            # 禁用梯度计算
            with torch.no_grad():
                outputs = self.model(**inputs)

            return outputs

        except Exception as e:
            print(f"BERT推理失败: {str(e)}")
            raise Exception(f"BERT推理过程出错: {str(e)}")

    def get_model_info(self) -> dict:
        """
        获取模型信息
        :return: 模型信息字典
        """
        return {
            "model_name": self.model_name,
            "device": str(self.device),
            "is_cuda_available": torch.cuda.is_available(),
            "cuda_device_count": torch.cuda.device_count()
        }

    def clear_cache(self):
        """
        清理GPU缓存
        """
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            print("GPU缓存已清理")

# 全局BERT优化器实例
bert_optimizer = BertOptimizer()