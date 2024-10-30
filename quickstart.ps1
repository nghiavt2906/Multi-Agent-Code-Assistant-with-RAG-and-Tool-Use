# Quick Start Script for Windows PowerShell
# Run this to set up and start the project

Write-Host "🚀 Multi-Agent Code Assistant - Quick Start" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "✗ Python not found. Please install Python 3.9+" -ForegroundColor Red
    exit 1
}

# Check Node
Write-Host "Checking Node.js installation..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✓ Found Node.js: $nodeVersion" -ForegroundColor Green
}
catch {
    Write-Host "✗ Node.js not found. Please install Node.js 16+" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Would you like to:" -ForegroundColor Cyan
Write-Host "1. Set up backend only" -ForegroundColor White
Write-Host "2. Set up frontend only" -ForegroundColor White
Write-Host "3. Set up both (recommended)" -ForegroundColor White
$choice = Read-Host "Enter your choice (1-3)"

if ($choice -in @("1", "3")) {
    Write-Host ""
    Write-Host "Setting up backend..." -ForegroundColor Yellow
    
    Set-Location backend
    
    # Install dependencies
    Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
    
    # Create .env if not exists
    if (!(Test-Path .env)) {
        Write-Host "Creating .env file..." -ForegroundColor Yellow
        Copy-Item .env.example .env
        Write-Host "⚠ IMPORTANT: Edit backend\.env and add your API keys!" -ForegroundColor Red
        Write-Host "   - OPENAI_API_KEY" -ForegroundColor Yellow
        Write-Host "   - ANTHROPIC_API_KEY" -ForegroundColor Yellow
    }
    
    # Initialize vector DB
    Write-Host "Initializing vector database..." -ForegroundColor Yellow
    python scripts/init_vectordb.py
    
    Write-Host "✓ Backend setup complete!" -ForegroundColor Green
    
    Set-Location ..
}

if ($choice -in @("2", "3")) {
    Write-Host ""
    Write-Host "Setting up frontend..." -ForegroundColor Yellow
    
    Set-Location frontend
    
    # Install dependencies
    Write-Host "Installing Node dependencies (this may take a while)..." -ForegroundColor Yellow
    npm install
    
    Write-Host "✓ Frontend setup complete!" -ForegroundColor Green
    
    Set-Location ..
}

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "✨ Setup Complete!" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To start the application:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Start backend (in one terminal):" -ForegroundColor White
Write-Host "   cd backend" -ForegroundColor Gray
Write-Host "   python main.py" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Start frontend (in another terminal):" -ForegroundColor White
Write-Host "   cd frontend" -ForegroundColor Gray
Write-Host "   npm run dev" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Open browser:" -ForegroundColor White
Write-Host "   http://localhost:3000" -ForegroundColor Gray
Write-Host ""
Write-Host "API Documentation: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
