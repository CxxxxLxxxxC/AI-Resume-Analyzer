# 智能简历分析系统 - 部署指南

## 系统要求

### 硬件要求
- CPU: 推荐4核以上
- 内存: 推荐8GB以上
- 存储: 建议20GB可用空间

### 软件要求
- Python 3.8+
- Node.js 16+
- npm 8+

## 快速开始

### 1. 环境准备

#### Windows系统
```bash
# 安装Python 3.9或3.10（如果没有）
# 从 https://www.python.org/downloads/ 下载安装

# 验证安装
python --version
pip --version
```

#### Linux系统
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv

# CentOS/RHEL
sudo yum install python3 python3-pip
```

### 2. 后端服务安装

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

# 运行自动安装脚本
python install_dependencies.py
```

或者手动安装：
```bash
# 安装所有依赖
pip install -r requirements.txt

# 验证PyTorch安装
python -c "import torch; print(f'PyTorch版本: {torch.__version__}'); print(f'CUDA可用: {torch.cuda.is_available()}')"
```

### 3. 前端服务安装

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 开发模式启动
npm run dev
```

### 4. 启动服务

#### 使用Docker（推荐）
```bash
# 使用Docker Compose
docker-compose up --build

# 后台运行
docker-compose up -d --build
```

#### 手动启动
```bash
# 后端
cd backend
python app.py

# 前端
cd frontend
npm run dev
```

## 故障排除

### 问题1: PyTorch安装失败
**错误信息**: `ERROR: No matching distribution found for torch==2.1.0`

**解决方案**:
1. 使用CPU版本
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

2. 或安装稳定版本
```bash
pip install torch==2.0.1 torchvision==0.15.1 torchaudio==2.0.1
```

### 问题2: GPU不可用
**解决方案**:
```python
# 在代码中强制使用CPU
import torch
device = torch.device('cpu')
```

### 问题3: Redis连接失败
**解决方案**:
1. 安装Redis服务
```bash
# Windows
choco install redis
# Linux
sudo apt install redis-server

# 启动Redis
redis-server
```

2. 或使用Docker运行Redis
```bash
docker run -d -p 6379:6379 redis
```

### 问题4: 端口被占用
**解决方案**:
- 修改后端端口：编辑 `backend/app.py` 中的 `uvicorn.run` 部分
- 修改前端端口：编辑 `frontend/vue.config.js` 中的 `devServer.port`

## 性能优化

### 1. 使用GPU（可选）
如果您的系统有NVIDIA GPU，可以：
```bash
# 安装CUDA支持的PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### 2. 使用Redis缓存
确保Redis服务正在运行以提升AI分析速度。

### 3. 优化模型
- 第一次运行时模型会自动下载（约500MB）
- 模型会缓存在本地，后续运行会更快

## 常用命令

### 后端
```bash
# 启动API服务
python app.py

# 运行测试
pytest tests/

# 重新安装依赖
pip install -r requirements.txt --force-reinstall
```

### 前端
```bash
# 开发模式
npm run dev

# 构建生产版本
npm run build

# 预览生产版本
npm run preview

# 安装依赖
npm install

# 清理依赖
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### Docker
```bash
# 构建并启动所有服务
docker-compose up --build

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

# 重建容器
docker-compose down -v
docker-compose up --build
```

## 访问地址

- 前端界面: http://localhost:3000
- API服务: http://localhost:8000
- API文档: http://localhost:8000/docs