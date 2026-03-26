# AI 赋能的智能简历分析系统

基于人工智能的简历解析与岗位匹配度分析系统，支持 PDF 简历自动解析、关键信息提取、技能识别以及简历与岗位描述的智能匹配度分析。

## 📋 项目简介

本系统是一个全栈 Web 应用，能够：
- 自动解析 PDF 格式的简历文件
- 提取候选人基本信息（姓名、电话、邮箱等）
- 识别求职信息和技能关键词
- 分析简历与岗位描述的匹配度评分
- 提供详细的技能、经验、学历三个维度的匹配分析

## 🏗️ 项目架构

```
AI 赋能的智能简历分析系统/
├── backend/                 # 后端服务 (FastAPI)
│   ├── app.py             # API 主入口
│   ├── models/            # 数据模型
│   │   └── resume.py     # 简历数据结构
│   ├── utils/             # 工具模块
│   │   ├── pdf_parser.py      # PDF 文本提取
│   │   ├── nlp_service.py     # NLP 信息提取与匹配分析
│   │   ├── bert_optimizer.py   # BERT 模型优化
│   │   └── cache_simple.py    # 缓存管理
│   ├── requirements.txt    # Python 依赖
│   └── cache/            # 缓存目录
└── frontend/               # 前端页面
    ├── index.html         # 单页应用入口
    └── src/             # Vue 组件
        ├── App.vue
        ├── router/
        ├── store/
        └── views/
            └── HomeView.vue
```

## 🛠️ 技术选型

### 后端

| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.8+ | 开发语言 |
| FastAPI | Latest | Web 框架 |
| Uvicorn | Latest | ASGI 服务器 |
| PyPDF2 | Latest | PDF 解析 |
| Transformers | 4.35.2+ | BERT 模型 |
| PyTorch | 2.1.0+ | 深度学习框架 |
| Redis | Latest | 缓存服务（可选）|

### 前端

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

## 📦 部署方式

### 方式一：本地部署

#### 1. 环境要求

- Python 3.8+
- pip

#### 2. 后端部署

```bash
# 进入后端目录
cd backend

# 创建虚拟环境（推荐）
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动后端服务
python app.py
```

后端服务地址: http://localhost:8000
API 文档地址: http://localhost:8000/docs

#### 3. 前端部署

```bash
# 使用 Python HTTP 服务器
cd frontend
python -m http.server 3000
```

前端地址: http://localhost:3000

### 方式二：Docker 部署

```bash
# 构建并启动
docker-compose up --build

# 后台运行
docker-compose up -d --build
```

### 方式三：云服务部署

#### 后端部署（推荐平台）
- [Railway](https://railway.app)
- [Render](https://render.com)
- [Vercel](https://vercel.com)

#### 前端部署
- [GitHub Pages](https://pages.github.com) - 免费托管静态网站
- [Netlify](https://netlify.com) - 免费静态网站托管
- [Vercel](https://vercel.com) - 免费部署

## 📖 使用说明

### 1. 上传简历

访问前端页面，点击上传区域选择 PDF 简历文件。

### 2. 查看解析结果

系统自动提取并展示：
- 基本信息（姓名、电话、邮箱、地址）
- 求职信息（求职意向、期望薪资）
- 背景信息（工作经历、学历、项目经历）
- 技能关键词

### 3. 分析匹配度

1. 在"岗位匹配度分析"区域输入岗位描述（JD）
2. 点击"分析匹配度"按钮
3. 查看匹配度结果：
   - 总体匹配度（0-100%）
   - 技能匹配度
   - 经验匹配度
   - 学历匹配度

### 4. API 接口

| 接口 | 方法 | 功能 |
|------|------|------|
| `/api/upload` | POST | 上传并解析简历 |
| `/api/analyze` | POST | 分析简历与岗位匹配度 |
| `/api/resume/{id}` | GET | 获取简历信息 |
| `/api/clear-cache` | POST | 清空缓存 |

详细 API 文档: 访问后端地址 `/docs`

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

## 📊 功能演示

### 简历解析
- 自动提取姓名、电话、邮箱、地址
- 识别求职意向和期望薪资
- 提取工作经历、教育背景、项目经验
- 识别技术栈和技能关键词

### 匹度分析
- 技能匹配度：基于简历技能与岗位要求技能的重叠度
- 经验匹配度：基于工作经验描述的匹配程度
- 学历匹配度：基于学历要求的匹配程度
- 综合评分：多维度加权计算

## 🐛 常见问题

### Q1: BERT 模型加载失败？
**A**: 首次运行会自动下载模型（约 500MB），需要网络连接。如遇网络问题，可使用本地模型。

### Q2: PDF 解析失败？
**A**: 确保上传的是标准 PDF 文件，非扫描版 PDF。扫描版需要 OCR 功能支持。

### Q3: 姓名提取不准确？
**A**: 系统使用多种模式匹配，但如果简历格式非常规，可能需要手动调整正则表达式。

### Q4: 匹配度分数不准确？
**A**: 当前算法基于关键词和文本相似度，可进一步优化为基于 BERT 的语义相似度计算。

## 🚀 未来优化方向

- [ ] 集成更先进的 NLP 模型（如 BERT 预训练模型微调）
- [ ] 支持多种简历格式（Word、图片 OCR）
- [ ] 增加简历质量评分功能
- [ ] 支持批量简历分析
- [ ] 添加用户认证和历史记录管理
- [ ] 优化匹配度算法，引入语义理解

## 📄 开源协议

MIT License

## 👤 作者信息

- **姓名**: 陈磊
- **邮箱**: [待填写]
- **GitHub**: [仓库地址]

## 🙏 致谢

感谢以下开源项目的支持：
- [FastAPI](https://fastapi.tiangolo.com/)
- [Vue.js](https://vuejs.org/)
- [Bootstrap](https://getbootstrap.com/)
- [Transformers](https://huggingface.co/docs/transformers)
