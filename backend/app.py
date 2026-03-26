from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import uuid
import tempfile
import os

# 导入自定义模块
from utils.pdf_parser import extract_text_from_pdf, clean_text
from utils.nlp_service import NLPService
from utils.cache_simple import cache_manager
from models.resume import Resume, ResumeAnalysisResult

app = FastAPI(
    title="AI简历分析系统",
    description="基于AI的智能简历分析服务",
    version="1.0.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境应该指定具体域名
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有请求头
)

# 配置NLP服务（使用BERT模型）
nlp_service = NLPService()  # 使用默认的bert-base-chinese模型

@app.post("/api/upload", summary="上传简历文件")
async def upload_resume(file: UploadFile = File(...)):
    """
    上传PDF简历文件
    """
    try:
        # 生成唯一的简历ID
        resume_id = str(uuid.uuid4())

        # 保存上传的文件到临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        # 提取PDF文本
        print(f"开始提取PDF文本: {temp_file_path}")
        raw_text = extract_text_from_pdf(temp_file_path)
        print(f"提取到原始文本长度: {len(raw_text)}")

        cleaned_text = clean_text(raw_text)
        print(f"清理后文本长度: {len(cleaned_text)}")

        if not cleaned_text.strip():
            raise Exception("无法从PDF中提取文本内容")

        # 创建简历对象
        resume = Resume(resume_id, cleaned_text)

        # 检查缓存
        cache_key = f"resume:{resume_id}"
        cached_result = cache_manager.get_cache(cache_key)

        if cached_result:
            print("从缓存加载结果")
            resume = Resume.from_dict(cached_result)
        else:
            print("开始分析简历")
            # 分析简历
            analysis_result = analyze_resume(resume)
            print("简历分析完成")

        # 确保有返回数据
        result = resume.to_dict()
        print(f"返回数据: {result}")
        return JSONResponse(content=result, status_code=200)

    except Exception as e:
        import traceback
        error_detail = f"简历上传失败: {str(e)}\n traceback: {traceback.format_exc()}"
        print(f"ERROR: {error_detail}")
        raise HTTPException(status_code=500, detail=error_detail)
    finally:
        # 清理临时文件
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

@app.post("/api/analyze", summary="分析简历与岗位匹配度")
async def analyze_match(
    resume_id: str = Form(...),
    job_description: str = Form(...)
):
    """
    分析简历与岗位的匹配度
    """
    try:
        # 检查缓存
        cache_key = f"match:{resume_id}:{job_description}"
        cached_result = cache_manager.get_cache(cache_key)

        if cached_result:
            return JSONResponse(content=cached_result, status_code=200)
        else:
            # 获取简历信息
            resume_cache_key = f"resume:{resume_id}"
            resume_data = cache_manager.get_cache(resume_cache_key)

            if not resume_data:
                raise HTTPException(status_code=404, detail="简历不存在")

            resume = Resume.from_dict(resume_data)

            # 分析匹配度
            match_result = nlp_service.analyze_match(resume.raw_text, job_description)

            # 更新简历匹配度
            resume.match_score = match_result.get("overall_score", 0.0)
            resume.match_details = match_result.get("details", {})

            # 保存到缓存
            cache_manager.set_cache(cache_key, match_result, expire=3600)

            return JSONResponse(content=match_result, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"匹配度分析失败: {str(e)}")

@app.get("/api/resume/{resume_id}", summary="获取简历信息")
async def get_resume(resume_id: str):
    """
    获取指定简历的信息
    """
    try:
        # 检查缓存
        cache_key = f"resume:{resume_id}"
        resume_data = cache_manager.get_cache(cache_key)

        if not resume_data:
            raise HTTPException(status_code=404, detail="简历不存在")

        return JSONResponse(content=resume_data, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取简历信息失败: {str(e)}")

@app.post("/api/clear-cache", summary="清空缓存")
async def clear_cache():
    """
    清空所有缓存
    """
    try:
        cache_manager.clear_cache()
        return JSONResponse(content={"message": "缓存已清空"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"清空缓存失败: {str(e)}")

def analyze_resume(resume: Resume) -> ResumeAnalysisResult:
    """
    分析简历内容
    """
    try:
        print("开始提取关键信息")
        # 提取关键信息
        analysis_result = nlp_service.extract_key_info(resume.raw_text)
        print(f"分析结果: {analysis_result}")

        # 填充简历信息
        resume.basic_info = {
            "name": analysis_result.get("name", ""),
            "phone": analysis_result.get("phone", ""),
            "email": analysis_result.get("email", ""),
            "address": analysis_result.get("address", "")
        }

        resume.job_info = {
            "job_intention": analysis_result.get("job_intention", ""),
            "expected_salary": analysis_result.get("expected_salary", "")
        }

        resume.background_info = {
            "work_experience": analysis_result.get("work_experience", ""),
            "education": analysis_result.get("education", ""),
            "projects": analysis_result.get("projects", "")
        }

        resume.skills = analysis_result.get("skills", [])
        print(f"提取到技能: {resume.skills}")

        # 计算一个默认的匹配度评分（基于技能数量）
        skill_count = len(resume.skills)
        resume.match_score = min(100, skill_count * 10)  # 每个技能10分，最高100分
        print(f"默认匹配度评分: {resume.match_score}%")

        # 保存到缓存
        cache_key = f"resume:{resume.resume_id}"
        cache_manager.set_cache(cache_key, resume.to_dict(), expire=86400)

        print("简历分析完成")
        return ResumeAnalysisResult(resume)

    except Exception as e:
        import traceback
        print(f"简历分析失败: {str(e)}")
        print(traceback.format_exc())
        raise Exception(f"简历分析失败: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)