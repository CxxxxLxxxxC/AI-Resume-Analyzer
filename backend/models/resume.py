from typing import Dict, Any, List, Optional

class Resume:
    def __init__(self, resume_id: str, raw_text: str):
        """
        初始化简历对象
        :param resume_id: 简历ID
        :param raw_text: 原始文本
        """
        self.resume_id = resume_id
        self.raw_text = raw_text
        self.basic_info = {}  # 基本信息：姓名、电话、邮箱、地址
        self.job_info = {}    # 求职信息：求职意向、期望薪资
        self.background_info = {}  # 背景信息：工作年限、学历、项目经历
        self.skills = []     # 技能关键词
        self.match_score = 0.0  # 匹配度评分
        self.analysis_time = None  # 分析时间

    def to_dict(self) -> Dict[str, Any]:
        """
        将简历对象转换为字典
        :return: 字典格式的简历数据
        """
        return {
            "resume_id": self.resume_id,
            "raw_text": self.raw_text,
            "basic_info": self.basic_info,
            "job_info": self.job_info,
            "background_info": self.background_info,
            "skills": self.skills,
            "match_score": self.match_score,
            "analysis_time": self.analysis_time
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Resume':
        """
        从字典创建简历对象
        :param data: 字典数据
        :return: 简历对象
        """
        resume = cls(data["resume_id"], data["raw_text"])
        resume.basic_info = data.get("basic_info", {})
        resume.job_info = data.get("job_info", {})
        resume.background_info = data.get("background_info", {})
        resume.skills = data.get("skills", [])
        resume.match_score = data.get("match_score", 0.0)
        resume.analysis_time = data.get("analysis_time")
        return resume

class ResumeAnalysisResult:
    def __init__(self, resume: Resume, job_description: str = None):
        """
        初始化简历分析结果
        :param resume: 简历对象
        :param job_description: 岗位描述（可选）
        """
        # 复制简历的所有属性
        self.resume_id = resume.resume_id
        self.raw_text = resume.raw_text
        self.basic_info = resume.basic_info
        self.job_info = resume.job_info
        self.background_info = resume.background_info
        self.skills = resume.skills
        self.match_score = resume.match_score
        self.analysis_time = resume.analysis_time

        self.job_description = job_description
        self.match_details = {}  # 匹配详情
        self.analysis_status = "completed"  # 分析状态

    def to_dict(self) -> Dict[str, Any]:
        """
        将分析结果转换为字典
        :return: 字典格式的分析结果
        """
        return {
            "resume_id": self.resume.resume_id,
            "analysis_status": self.analysis_status,
            "basic_info": self.resume.basic_info,
            "job_info": self.resume.job_info,
            "background_info": self.resume.background_info,
            "skills": self.resume.skills,
            "match_score": self.resume.match_score,
            "match_details": self.match_details,
            "analysis_time": self.resume.analysis_time
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ResumeAnalysisResult':
        """
        从字典创建分析结果对象
        :param data: 字典数据
        :return: 分析结果对象
        """
        resume = Resume.from_dict(data)
        result = cls(resume, data.get("job_description"))
        result.match_details = data.get("match_details", {})
        result.analysis_status = data.get("analysis_status", "completed")
        return result