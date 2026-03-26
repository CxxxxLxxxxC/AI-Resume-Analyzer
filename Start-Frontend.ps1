Write-Host "=== 启动前端服务 ===" -ForegroundColor Green
Write-Host "当前路径: $(Get-Location)"
Write-Host "切换到前端目录..." -ForegroundColor Yellow

# 切换到前端目录
Set-Location "C:\Users\Administrator\Desktop\AI 赋能的智能简历分析系统\frontend"

Write-Host "启动HTTP服务器在端口3000..." -ForegroundColor Yellow
Write-Host "前端访问地址: http://localhost:3000" -ForegroundColor Cyan

# 启动HTTP服务器
python -m http.server 3000

Write-Host "服务器已停止" -ForegroundColor Red
Read-Host "按Enter键退出"