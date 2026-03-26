from .bert_optimizer import bert_optimizer
import numpy as np
from typing import Dict, Any, List, Optional
import re

class NLPService:
    def __init__(self, model_path: str = "bert-base-chinese"):
        """
        初始化NLP服务,使用BERT模型
        :param model_path: BERT模型路径或名称
        """
        # 使用全局BERT优化器
        self.optimizer = bert_optimizer
        self.model_path = model_path

    def extract_key_info(self, text: str) -> Dict[str, Any]:
        """
        从文本中提取关键信息
        :param text: 简历文本
        :return: 提取的关键信息字典
        """
        try:
            # 预处理文本
            processed_text = self._preprocess_text(text)

            # 提取基本信息
            basic_info = self._extract_basic_info(processed_text)

            # 提取求职信息
            job_info = self._extract_job_info(processed_text)

            # 提取背景信息
            background_info = self._extract_background_info(processed_text)

            # 提取技能关键词
            skills = self._extract_skills(processed_text)

            return {
                "name": basic_info.get("name", ""),
                "phone": basic_info.get("phone", ""),
                "email": basic_info.get("email", ""),
                "address": basic_info.get("address", ""),
                "job_intention": job_info.get("job_intention", ""),
                "expected_salary": job_info.get("expected_salary", ""),
                "work_experience": background_info.get("work_experience", ""),
                "education": background_info.get("education", ""),
                "projects": background_info.get("projects", ""),
                "skills": skills
            }
        except Exception as e:
            raise Exception(f"关键信息提取失败: {str(e)}")

    def extract_keywords(self, text: str) -> List[str]:
        """
        从文本中提取关键词
        :param text: 文本内容
        :return: 关键词列表
        """
        try:
            # 使用BERT进行关键词提取
            keywords = self._extract_keywords_with_bert(text)
            return keywords
        except Exception as e:
            raise Exception(f"关键词提取失败: {str(e)}")

    def analyze_match(self, resume_text: str, job_description: str) -> Dict[str, float]:
        """
        分析简历与岗位的匹配度
        :param resume_text: 简历文本
        :param job_description: 岗位描述
        :return: 匹配度评分
        """
        try:
            # 提取简历关键词
            resume_keywords = self.extract_keywords(resume_text)

            # 提取岗位关键词
            job_keywords = self.extract_keywords(job_description)

            # 计算匹配度
            match_score = self._calculate_match_score(resume_keywords, job_keywords, resume_text, job_description)

            return {
                "overall_score": round(match_score),
                "details": {
                    "skill_match": round(self._calculate_skill_match(resume_keywords, job_keywords)),
                    "experience_match": round(self._calculate_experience_match(resume_text, job_description)),
                    "education_match": round(self._calculate_education_match(resume_text, job_description))
                }
            }
        except Exception as e:
            raise Exception(f"匹配度分析失败: {str(e)}")

    def _preprocess_text(self, text: str) -> str:
        """
        预处理文本
        :param text: 原始文本
        :return: 处理后的文本
        """
        # 去除多余空格和换行符
        text = ' '.join(text.split())
        # 去除特殊字符
        text = ''.join(c for c in text if c.isprintable())
        return text

    def _extract_basic_info(self, text: str) -> Dict[str, str]:
        """
        提取基本信息
        :param text: 处理后的文本
        :return: 基本信息字典
        """
        basic_info = {
            "name": "",
            "phone": "",
            "email": "",
            "address": ""
        }

        # 提取姓名（多种模式匹配）
        name = ""

        # 模式1: "姓名：xxx" 或 "姓名: xxx"
        name_match = re.search(r'姓[名氏][:：]\s*([\u4e00-\u9fa5]{2,4}(?:·[\u4e00-\u9fa5]{2,4})*)', text)
        if name_match:
            name = name_match.group(1)

        # 模式2: "xxx 男" 或 "xxx 女" （姓名后接性别）
        if not name:
            name_match = re.search(r'([\u4e00-\u9fa5]{2,4})\s+[男女]', text)
            if name_match:
                name = name_match.group(1)

        # 模式3: "xxx | 年龄：xx岁" （姓名后接竖线分隔符）
        if not name:
            name_match = re.search(r'([\u4e00-\u9fa5]{2,4})\s*\|\s*年龄[：:]', text)
            if name_match:
                name = name_match.group(1)

        # 模式4: 查找独立的2-4字中文名字，排除常见学校、公司等关键词
        if not name:
            # 常见排除词
            exclude_keywords = ['大学', '学院', '公司', '技术', '系统', '管理', '开发', '设计', '实现',
                              '简历', '应聘', '申请', '求职', '个人', '专业', '项目', '教育', '工作']

            # 在前500字符中查找
            short_text = text[:500] if len(text) > 500 else text
            name_matches = re.finditer(r'([\u4e00-\u9fa5]{2,4})', short_text)

            for match in name_matches:
                candidate = match.group(1)
                # 检查是否包含排除词
                if not any(exclude in candidate for exclude in exclude_keywords):
                    # 检查上下文是否像名字（后面紧跟性别、年龄或竖线）
                    context = short_text[match.start():match.end()+20]
                    if re.search(r'[男女]|年龄|\|', context):
                        name = candidate
                        break

        basic_info["name"] = name

        # 提取电话
        phone_match = re.search(r'1[3-9]\d{9}', text)
        if phone_match:
            basic_info["phone"] = phone_match.group(0)

        # 提取邮箱
        email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
        if email_match:
            basic_info["email"] = email_match.group(0)

        # 提取地址
        address_keywords = ['地址', '住址', '省', '市', '区', '县']
        for keyword in address_keywords:
            if keyword in text:
                address_match = re.search(rf'{keyword}[:：]?[\s\S]*?(?:\n|\d)', text)
                if address_match:
                    basic_info["address"] = address_match.group(0).replace(keyword + ':', '').strip()
                    break

        return basic_info

    def _extract_job_info(self, text: str) -> Dict[str, str]:
        """
        提取求职信息
        :param text: 处理后的文本
        :return: 求职信息字典
        """
        job_info = {
            "job_intention": "",
            "expected_salary": ""
        }

        # 提取求职意向
        job_intention_keywords = ['求职意向', '期望职位', '应聘职位']
        for keyword in job_intention_keywords:
            if keyword in text:
                intention_match = re.search(rf'{keyword}[:：]?[\s\S]*?(?:\n|\d)', text)
                if intention_match:
                    job_info["job_intention"] = intention_match.group(0).replace(keyword + ':', '').strip()
                    break

        # 提取期望薪资
        salary_keywords = ['期望薪资', '薪资要求', '月薪']
        for keyword in salary_keywords:
            if keyword in text:
                salary_match = re.search(rf'{keyword}[:：]?[\s\S]*?(?:\n|\d)', text)
                if salary_match:
                    job_info["expected_salary"] = salary_match.group(0).replace(keyword + ':', '').strip()
                    break

        return job_info

    def _extract_background_info(self, text: str) -> Dict[str, str]:
        """
        提取背景信息
        :param text: 处理后的文本
        :return: 背景信息字典
        """
        background_info = {
            "work_experience": "",
            "education": "",
            "projects": ""
        }

        # 提取工作经历
        experience_keywords = ['工作经历', '工作经历', '实习经历', '项目经验']
        for keyword in experience_keywords:
            if keyword in text:
                experience_match = re.search(rf'{keyword}[:：]?[\s\S]*?(?=(?:教育背景|项目经历|技能特长|$))', text)
                if experience_match:
                    background_info["work_experience"] = experience_match.group(0).replace(keyword + ':', '').strip()
                    break

        # 提取教育背景
        education_keywords = ['教育背景', '学历', '教育经历']
        for keyword in education_keywords:
            if keyword in text:
                education_match = re.search(rf'{keyword}[:：]?[\s\S]*?(?=(?:工作经历|项目经历|技能特长|$))', text)
                if education_match:
                    background_info["education"] = education_match.group(0).replace(keyword + ':', '').strip()
                    break

        # 提取项目经历
        project_keywords = ['项目经历', '项目经验', '项目描述']
        for keyword in project_keywords:
            if keyword in text:
                project_match = re.search(rf'{keyword}[:：]?[\s\S]*?(?=(?:工作经历|教育背景|技能特长|$))', text)
                if project_match:
                    background_info["projects"] = project_match.group(0).replace(keyword + ':', '').strip()
                    break

        return background_info

    def _extract_skills(self, text: str) -> List[str]:
        """
        提取技能关键词
        :param text: 文本内容
        :return: 技能关键词列表
        """
        try:
            # 使用BERT模型提取技能
            skills = self._extract_skills_with_bert(text)
            return skills
        except Exception as e:
            print(f"BERT技能提取失败，使用规则提取: {str(e)}")
            # 回退到规则提取
            return self._extract_skills_with_bert(text)

    def _extract_skills_with_bert(self, text: str) -> List[str]:
        """
        使用BERT提取技能关键词
        :param text: 文本内容
        :return: 技能关键词列表
        """
        # 这里简化处理，实际应用中需要更复杂的BERT模型
        # 可以使用命名实体识别或关键词提取模型
        skills = []

        # 常见技能关键词
        skill_keywords = [
            'Python', 'Java', 'JavaScript', 'C++', 'SQL', 'HTML', 'CSS', 'React', 'Vue', 'Angular',
            'Node.js', 'Spring', 'Django', 'Flask', 'TensorFlow', 'PyTorch', '机器学习', '深度学习',
            '数据分析', '算法', '数据库', '前端', '后端', '全栈', 'DevOps', 'Docker', 'Kubernetes'
        ]

        for keyword in skill_keywords:
            if keyword in text:
                skills.append(keyword)

        return list(set(skills))  # 去重

    def _extract_keywords_with_bert(self, text: str) -> List[str]:
        """
        使用BERT提取关键词
        :param text: 文本内容
        :return: 关键词列表
        """
        # 简化处理，实际应用中需要更复杂的BERT模型
        # 可以使用文本摘要、关键词提取等技术
        return self._extract_skills_with_bert(text)

    def _calculate_match_score(self, resume_keywords: List[str], job_keywords: List[str],
                           resume_text: str, job_description: str) -> float:
        """
        计算匹配度评分
        :param resume_keywords: 简历关键词
        :param job_keywords: 岗位关键词
        :param resume_text: 简历文本
        :param job_description: 岗位描述
        :return: 匹配度评分（0-100）
        """
        # 基于关键词重叠度计算
        overlap = set(resume_keywords) & set(job_keywords)
        overlap_score = len(overlap) / len(set(job_keywords)) * 100 if job_keywords else 0

        # 基于文本相似度（简化版）
        text_similarity = self._calculate_text_similarity(resume_text, job_description)

        # 综合评分
        final_score = (overlap_score * 0.7) + (text_similarity * 30)
        return min(100, max(0, final_score))

    def _calculate_skill_match(self, resume_keywords: List[str], job_keywords: List[str]) -> float:
        """
        计算技能匹配度
        :param resume_keywords: 简历关键词
        :param job_keywords: 岗位关键词
        :return: 技能匹配度（0-100）
        """
        if not job_keywords:
            return 0

        overlap = set(resume_keywords) & set(job_keywords)
        return len(overlap) / len(set(job_keywords)) * 100

    def _calculate_experience_match(self, resume_text: str, job_description: str) -> float:
        """
        计算经验匹配度
        :param resume_text: 简历文本
        :param job_description: 岗位描述
        :return: 经验匹配度（0-100）
        """
        # 简化处理，实际应用中需要更复杂的分析
        experience_keywords = ['工作经验', '工作年限', '项目经验', '实习经历']
        resume_experience = any(keyword in resume_text for keyword in experience_keywords)
        job_experience = any(keyword in job_description for keyword in experience_keywords)

        return 80 if resume_experience and job_experience else 40

    def _calculate_education_match(self, resume_text: str, job_description: str) -> float:
        """
        计算学历匹配度
        :param resume_text: 简历文本
        :param job_description: 岗位描述
        :return: 学历匹配度（0-100）
        """
        # 简化处理，实际应用中需要更复杂的分析
        education_keywords = ['学历', '本科', '硕士', '博士', '教育背景']
        resume_education = any(keyword in resume_text for keyword in education_keywords)
        job_education = any(keyword in job_description for keyword in education_keywords)

        return 80 if resume_education and job_education else 40

    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """
        计算文本相似度（简化版）
        :param text1: 文本1
        :param text2: 文本2
        :return: 相似度（0-100）
        """
        # 简化处理，实际应用中可以使用BERT的文本嵌入和余弦相似度
        common_words = set(text1.split()) & set(text2.split())
        return len(common_words) / max(len(set(text1.split())), len(set(text2.split()))) * 100 if text1 and text2 else 0