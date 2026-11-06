# Windows RTX 4060 8GB — ComfyUI/Wan2.2 5B installer and launcher
# Run in PowerShell: powershell -ExecutionPolicy Bypass -File .\quality_tournament\launch_wan_windows.ps1
# This script has NOT been executed on the user's hardware. It does NOT run a model generation.
$ErrorActionPreference = "Stop"
Write-Host "Operation No Pants / ComfyUI local setup (NO paid APIs)" -ForegroundColor Magenta
if (-not $IsWindows -and $PSVersionTable.PSEdition -eq "Core") { throw "Windows NVIDIA launcher only" }
foreach ($cmd in @("git","python","nvidia-smi")) {
 if (-not (Get-Command $cmd -ErrorAction SilentlyContinue)) { throw "Missing prerequisite: $cmd. Install Git, Python 3.11 and NVIDIA driver." }
}
& nvidia-smi
if ($LASTEXITCODE -ne 0) { throw "NVIDIA GPU driver unavailable" }
$base = Join-Path $env:USERPROFILE "OperationNoPants"
New-Item -ItemType Directory -Force -Path $base | Out-Null
$drive = (Get-Item $base).PSDrive
if ($drive.Free -lt 35000000000) { throw "Need at least 35 GB free disk before installing ComfyUI and ~18 GB model files" }
$repo = Join-Path $base "ComfyUI"
if (-not (Test-Path $repo)) {
 git clone https://github.com/comfyanonymous/ComfyUI.git $repo
 if ($LASTEXITCODE -ne 0) { throw "Git clone failed" }
}
Set-Location $repo
if (-not (Test-Path ".venv\Scripts\python.exe")) {
 python -m venv .venv
 if ($LASTEXITCODE -ne 0) { throw "venv creation failed" }
}
$py = ".\.venv\Scripts\python.exe"
& $py -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) { throw "pip upgrade failed" }
& $py -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
if ($LASTEXITCODE -ne 0) { throw "CUDA PyTorch installation failed" }
& $py -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw "ComfyUI dependencies failed" }
Write-Host "Model downloads NOT performed. Open Workflow > Browse Templates > Video > Wan2.2 5B, download official files." -ForegroundColor Yellow
Write-Host "Diffusion: wan2.2_ti2v_5B_fp16.safetensors (~10GB)"
Write-Host "Text: umt5_xxl_fp8_e4m3fn_scaled.safetensors (~6.7GB)"
Write-Host "VAE: wan2.2_vae.safetensors (~1.4GB)"
Start-Process "http://127.0.0.1:8188"
& $py main.py --listen 127.0.0.1 --port 8188 --lowvram
