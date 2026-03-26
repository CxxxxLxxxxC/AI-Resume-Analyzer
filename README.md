# AI 赋能的智能简历分析系统

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)
![Vue.js](https://img.shields.io/badge/Vue.js-3.x-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)

</div>

基于人工智能的简历解析与岗位匹配度分析系统，支持 PDF 简历自动解析、关键信息提取、技能识别以及简历与岗位描述的智能匹配度分析。

## ✨ 项目简介

本系统是一个全栈 Web 应用，能够：

- 📄 **自动解析 PDF 格式的简历文件**
- 🔍 **提取候选人基本信息**（姓名、电话、邮箱、地址）
- 💼 **识别求职信息**（求职意向、期望薪资）
- 🏷️ **智能提取技能关键词**
- 📊 **分析简历与岗位描述的匹配度**
- 📈 **提供多维度评分**（技能、经验、学历）

## 🏗️ 项目架构

```
AI 赋能的智能简历分析系统/
├── backend/                      # 后端服务 (FastAPI)
│   ├── app.py                  # API 主入口
│   ├── start_with_ai.py         # AI模式启动脚本
│   ├── start_without_model.py    # 无模型启动脚本
│   ├── models/                 # 数据模型
│   │   └── resume.py           # 简历数据结构
│   ├── utils/                  # 工具模块
│   │   ├── pdf_parser.py       # PDF 文本提取
│   │   ├── nlp_service.py      # NLP 信息提取与匹配分析
│   │   ├── bert_optimizer.py    # BERT 模型优化
│   │   └── cache_simple.py     # 缓存管理
│   ├── requirements.txt         # Python 依赖
│   ├── Dockerfile             # Docker 配置
│   └── cache/                # 缓存目录
├── frontend/                     # 前端页面
│   ├── index.html             # 单页应用入口
│   └── src/                 # Vue 组件
│       ├── App.vue
│       ├── main.js
│       ├── router/
│       └── store/
├── DEPLOYMENT.md               # 详细部署文档
├── Start-Backend.ps1          # Windows 后端启动脚本
├── Start-Frontend.ps1         # Windows 前端启动脚本
└── README.md                # 项目说明
```

## 🛠️ 技术选型

### 后端技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.8+ | 开发语言 |
| FastAPI | Latest | Web 框架 |
| Uvicorn | Latest | ASGI 服务器 |
| PyPDF2 | Latest | PDF 解析 |
| Transformers | 4.35.2+ | BERT 模型 |
| PyTorch | 2.1.0+ | 深度学习框架 |
| Pydantic | Latest | 数据验证 |
| Axios | Latest | HTTP 客户端 |

### 前端技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Vue.js | 3.x | 前端框架 |
| Bootstrap | 5.3.0 | UI 框架 |
| Bootstrap Icons | 1.10.0 | 图标库 |
| Axios | Latest | HTTP 客户端 |

### 核心算法

- **PDF 解析**: PyPDF2 提取文本内容
- **信息提取**: 正则表达式 + 关键词匹配
- **技能识别**: 预定义技能词库 + 文本匹配
- **匹配度计算**: 关键词重叠度 + 文本相似度
- **缓存优化**: MD5 哈希避免特殊字符问题

## 📦 部署方式

### 方式一：本地快速启动

#### 环境要求
- Python 3.8+
- pip

#### 后端启动

**Windows（使用脚本）：**
```powershell
.\Start-Backend.ps1
```

**手动启动：**
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate      # Windows
# source venv/bin/activate    # Linux/Mac
pip install -r requirements.txt
python app.py
```

#### 前端启动

**Windows（使用脚本）：**
```powershell
.\Start-Frontend.ps1
```

**手动启动：**
```bash
cd frontend
python -m http.server 3000
```

### 方式二：Docker 部署

```bash
# 构建并启动
docker-compose up --build

# 后台运行
docker-compose up -d --build
```

### 方式三：云服务部署

#### 后端部署（推荐平台）
- [Railway](https://railway.app) - 免费部署 Python 应用
- [Render](https://render.com) - 免费全栈部署
- [Vercel](https://vercel.com) - 免费部署

#### 前端部署
- [GitHub Pages](https://pages.github.com) - 免费托管静态网站
- [Netlify](https://netlify.com) - 拖拽部署
- [Vercel](https://vercel.com) - 一键部署

详细部署说明请查看 [DEPLOYMENT.md](DEPLOYMENT.md)

## 📖 使用说明

### 1. 访问系统

- **本地地址**: http://localhost:3000
- **API 文档**: http://localhost:8000/docs

### 2. 上传简历

点击页面中间的上传区域，选择 PDF 格式的简历文件（最大 10MB）

### 3. 查看解析结果

系统自动提取并展示：
- 📝 **基本信息**: 姓名、电话、邮箱、地址
- 💼 **求职信息**: 求职意向、期望薪资
- 📚 **背景信息**: 工作经历、学历、项目经历
- 🏷️ **技能关键词**: 自动识别的技术栈

### 4. 分析岗位匹配度

1. 在"岗位匹配度分析"区域输入岗位描述（JD）
2. 点击"分析匹配度"按钮
3. 查看匹配度结果：
   - 📊 **总体匹配度**（0-100%）
   - 🛠️ **技能匹配度**
   - 📈 **经验匹配度**
   - 🎓 **学历匹配度**

### 5. API 接口

| 接口 | 方法 | 功能 |
|------|------|------|
| `/api/upload` | POST | 上传并解析简历 |
| `/api/analyze` | POST | 分析简历与岗位匹配度 |
| `/api/resume/{id}` | GET | 获取简历信息 |
| `/api/clear-cache` | POST | 清空缓存 |

访问 http://localhost:8000/docs 查看 Swagger API 文档

## 📊 功能特性

### 简历解析
- ✅ 多模式姓名提取（支持"姓名：xxx"、"xxx 男"、"xxx | 年龄"等格式）
- ✅ 电话号码识别（中国大陆手机号）
- ✅ 邮箱地址提取
- ✅ 求职意向和期望薪资识别
- ✅ 教育背景、工作经历、项目经验提取
- ✅ 技能关键词智能识别（Java、Spring、Vue、MySQL 等）

### 匹度分析
- ✅ 技能匹配度：简历技能与岗位要求技能的重叠度
- ✅ 经验匹配度：工作经验描述的匹配程度
- ✅ 学历匹配度：学历要求的匹配程度
- ✅ 综合评分：多维度加权计算
- ✅ 可视化展示：进度条 + 颜色区分
  - 🟢 绿色：80-100（高匹配）
  - 🟠 橙色：60-79（中匹配）
  - 🔴 红色：0-59（低匹配）

### 性能优化
- ✅ 缓存机制：MD5 哈希避免文件名冲突
- ✅ 整数显示：匹配度分数四舍五入为整数
- ✅ 错误处理：完善的异常捕获和提示

## 🔧 配置说明

### 修改后端端口

编辑 `backend/app.py`:
```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # 修改端口号
```

### 修改前端 API 地址

编辑 `frontend/index.html`:
```javascript
const response = await axios.post('http://localhost:8000/api/upload', formData)
```

将 `http://localhost:8000` 改为你的后端部署地址。

## 🐛 常见问题

### Q1: BERT 模型加载失败？
**A**: 首次运行会自动下载模型（约 500MB），需要网络连接。如遇网络问题，可使用本地模型。

### Q2: PDF 解析失败？
**A**: 确保上传的是标准 PDF 文件，非扫描版 PDF。扫描版需要 OCR 功能支持。

### Q3: 姓名提取不准确？
**A**: 系统使用多种模式匹配，但如果简历格式非常规，可能需要手动调整 `backend/utils/nlp_service.py` 中的正则表达式。

### Q4: 匹配度分数不准确？
**A**: 当前算法基于关键词和文本相似度，可进一步优化为基于 BERT 的语义相似度计算。

### Q5: 前端无法连接后端？
**A**:
1. 确保后端服务已启动
2. 检查 CORS 配置（当前已允许所有来源）
3. 检查防火墙设置

## 🚀 未来优化方向

- [ ] 集成更先进的 NLP 模型（如 BERT 预训练模型微调）
- [ ] 支持多种简历格式（Word、图片 OCR）
- [ ] 增加简历质量评分功能
- [ ] 支持批量简历分析
- [ ] 添加用户认证和历史记录管理
- [ ] 优化匹配度算法，引入语义理解
- [ ] 添加招聘方管理后台
- [ ] 支持简历导出功能

## 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议

## 👤 作者信息

| 项目 | 信息 |
|------|------|
| 作者 | 三十 |
| GitHub | [CxxxxLxxxxC/AI-Resume-Analyzer](https://github.com/CxxxxLxxxxC/AI-Resume-Analyzer) |
| 项目地址 | [在线演示](https://cxxxxlxxxxc.github.io/ai-resume-analyzer/) |

## 🙏 致谢

感谢以下开源项目的支持：
- [FastAPI](https://fastapi.tiangolo.com/)
- [Vue.js](https://vuejs.org/)
- [Bootstrap](https://getbootstrap.com/)
- [Transformers](https://huggingface.co/docs/transformers)
- [PyPDF2](https://pypdf2.readthedocs.io/)

## 📮 联系方式

欢迎提交 Issue 和 Pull Request！

---

<div align="center">

如果觉得这个项目对你有帮助，请给个 ⭐ Star

</div>
