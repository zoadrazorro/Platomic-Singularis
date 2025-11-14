# Zoadra Docs Setup Script
# Run this script to set up and start the development server

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Zoadra.com Documentation Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Node.js is installed
Write-Host "Checking Node.js installation..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "✓ Node.js installed: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Node.js not found! Please install Node.js 18+ from https://nodejs.org/" -ForegroundColor Red
    exit 1
}

# Check if npm is available
Write-Host "Checking npm installation..." -ForegroundColor Yellow
try {
    $npmVersion = npm --version
    Write-Host "✓ npm installed: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ npm not found!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..." -ForegroundColor Gray
Write-Host ""

npm install

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✓ Dependencies installed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  Setup Complete!" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Available commands:" -ForegroundColor Yellow
    Write-Host "  npm run dev      - Start development server" -ForegroundColor White
    Write-Host "  npm run build    - Build for production" -ForegroundColor White
    Write-Host "  npm run preview  - Preview production build" -ForegroundColor White
    Write-Host ""
    Write-Host "Starting development server..." -ForegroundColor Yellow
    Write-Host ""
    
    npm run dev
} else {
    Write-Host ""
    Write-Host "✗ Installation failed!" -ForegroundColor Red
    Write-Host "Please check the error messages above." -ForegroundColor Red
    exit 1
}
