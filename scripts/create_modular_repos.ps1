# PowerShell script to create modular repositories
# Run from Singularis root directory

Write-Host "🧩 Creating Modular Singularis Repositories..." -ForegroundColor Cyan
Write-Host ""

$rootDir = Get-Location
$parentDir = Split-Path $rootDir -Parent

# Module definitions
$modules = @{
    "singularis-core" = @(
        "singularis/consciousness",
        "singularis/llm",
        "singularis/core",
        "singularis/learning"
    )
    "singularis-lifeops" = @(
        "singularis/life_ops",
        "integrations/life_timeline.py",
        "integrations/pattern_engine.py",
        "integrations/intervention_policy.py",
        "integrations/emergency_validator.py"
    )
    "singularis-perception" = @(
        "singularis/perception"
    )
    "singularis-integrations" = @(
        "integrations/messenger_bot_adapter.py",
        "integrations/fitbit_health_adapter.py",
        "integrations/meta_glasses_adapter.py",
        "integrations/roku_screencap_gateway.py",
        "integrations/main_orchestrator.py"
    )
    "singularis-skyrim" = @(
        "singularis/skyrim",
        "run_skyrim_agi.py"
    )
    "singularis-deployment" = @(
        "SEPHIROT_CLUSTER_ARCHITECTURE.md",
        "DEPLOYMENT_CHECKLIST.md",
        "MODULAR_ARCHITECTURE.md",
        "docs"
    )
}

# Create each module repo
foreach ($moduleName in $modules.Keys) {
    Write-Host "📦 Creating $moduleName..." -ForegroundColor Yellow
    
    $moduleDir = Join-Path $parentDir $moduleName
    
    # Create module directory
    if (Test-Path $moduleDir) {
        Write-Host "   ⚠️  Directory exists, skipping..." -ForegroundColor Yellow
        continue
    }
    
    New-Item -ItemType Directory -Path $moduleDir -Force | Out-Null
    
    # Copy files
    foreach ($item in $modules[$moduleName]) {
        $sourcePath = Join-Path $rootDir $item
        
        if (Test-Path $sourcePath) {
            # Determine destination
            if (Test-Path $sourcePath -PathType Container) {
                # Directory
                $destPath = Join-Path $moduleDir $item
                $destParent = Split-Path $destPath -Parent
                
                if (-not (Test-Path $destParent)) {
                    New-Item -ItemType Directory -Path $destParent -Force | Out-Null
                }
                
                Copy-Item -Path $sourcePath -Destination $destPath -Recurse -Force
                Write-Host "   ✅ Copied directory: $item" -ForegroundColor Green
            }
            else {
                # File
                $fileName = Split-Path $item -Leaf
                $destPath = Join-Path $moduleDir $fileName
                
                Copy-Item -Path $sourcePath -Destination $destPath -Force
                Write-Host "   ✅ Copied file: $item" -ForegroundColor Green
            }
        }
        else {
            Write-Host "   ⚠️  Not found: $item" -ForegroundColor Yellow
        }
    }
    
    # Create basic structure
    $readmePath = Join-Path $moduleDir "README.md"
    $setupPath = Join-Path $moduleDir "setup.py"
    $requirementsPath = Join-Path $moduleDir "requirements.txt"
    $testsDir = Join-Path $moduleDir "tests"
    
    # Create tests directory
    if (-not (Test-Path $testsDir)) {
        New-Item -ItemType Directory -Path $testsDir -Force | Out-Null
    }
    
    # Create README.md
    if (-not (Test-Path $readmePath)) {
        $readmeContent = @"
# $moduleName

Part of the Singularis AGI system.

## Installation

``````bash
pip install $moduleName
``````

## Usage

See [documentation](docs/) for details.

## License

MIT
"@
        Set-Content -Path $readmePath -Value $readmeContent
        Write-Host "   ✅ Created README.md" -ForegroundColor Green
    }
    
    # Create requirements.txt (basic)
    if (-not (Test-Path $requirementsPath)) {
        $reqContent = "# Dependencies for $moduleName`n"
        Set-Content -Path $requirementsPath -Value $reqContent
        Write-Host "   ✅ Created requirements.txt" -ForegroundColor Green
    }
    
    # Initialize git
    Push-Location $moduleDir
    git init | Out-Null
    Write-Host "   ✅ Initialized git repository" -ForegroundColor Green
    Pop-Location
    
    Write-Host ""
}

Write-Host "✅ All modular repositories created!" -ForegroundColor Green
Write-Host ""
Write-Host "📁 Repositories created in: $parentDir" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Review each module's files"
Write-Host "2. Update setup.py with proper dependencies"
Write-Host "3. Update requirements.txt"
Write-Host "4. Test each module independently"
Write-Host "5. Push to GitHub/GitLab"
Write-Host ""
