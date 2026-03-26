Write-Host "=== 启动后端服务 ===" -ForegroundColor Green
Write-Host "当前路径: $(Get-Location)"
Write-Host "切换到后端目录..." -ForegroundColor Yellow

# 切换到后端目录
Set-Location "C:\Users\Administrator\Desktop\AI 赋能的智能简历分析系统\backend"

Write-Host "检查依赖..." -ForegroundColor Yellow

# 检查是否需要安装依赖
if (-not (Test-Path "venv")) {
    Write-Host "创建虚拟环境..." -ForegroundColor Yellow
    python -m venv venv
}

# 激活虚拟环境
.\venv\Scripts\activate

Write-Host "安装依赖（如果需要）..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host "启动FastAPI服务器..." -ForegroundColor Yellow
Write-Host "后端API地址: http://localhost:8000" -ForegroundColor Cyan
Write-Host "API文档地址: http://localhost:8000/docs" -ForegroundColor Cyan

# 启动API服务器
python app.py

Write-Host "服务器已停止" -ForegroundColor Red
Read-Host "按Enter键退出"