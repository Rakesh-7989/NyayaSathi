# NyayaSathi Dev Script (PowerShell)
# Run this to start both frontend and backend

Write-Host "🚀 Starting NyayaSathi..." -ForegroundColor Green

# Start backend
$backendJob = Start-Job -ScriptBlock {
    Set-Location "C:\Users\boyap\NyayaSathi\backend"
    .\venv\Scripts\Activate.ps1
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
}

# Start frontend
$frontendJob = Start-Job -ScriptBlock {
    Set-Location "C:\Users\boyap\NyayaSathi\frontend"
    npm run dev
}

Write-Host "✅ Backend: http://localhost:8000" -ForegroundColor Cyan
Write-Host "✅ Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "📖 API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "`nPress Ctrl+C to stop both services" -ForegroundColor Yellow

# Wait for both
$backendJob, $frontendJob | Wait-Job
