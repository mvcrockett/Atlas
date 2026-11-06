# Operation No Pants / Windows RTX 4060 ComfyUI launcher — Sprint 3
# Invoke from a local clone on the Windows NVIDIA PC:
# powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\quality_tournament\launch_wan_windows.ps1
# No unapproved model downloads. Never exposes ComfyUI to the network.
param([switch]$CheckOnly, [switch]$SkipInstall)
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
function Require($condition,$message) { if (-not $condition) { throw $message } }
Write-Host "Operation No Pants — Wan2.2 5B local preflight" -ForegroundColor Magenta
Require ($env:OS -eq "Windows_NT") "Windows + NVIDIA only. This launcher does not support macOS/Linux."
foreach ($command in @("git","py","nvidia-smi")) {
 Require ([bool](Get-Command $command -ErrorAction SilentlyContinue)) "Missing $command. Install Git, Python 3.11 Python Launcher, and NVIDIA drivers."
}
$gpuText = (& nvidia-smi --query-gpu=name,memory.total --format=csv,noheader,nounits 2>&1 | Out-String).Trim()
Require ($LASTEXITCODE -eq 0 -and $gpuText.Length -gt 0) "NVIDIA driver/GPU not detected."
Write-Host "GPU: $gpuText"
$memMatch = [regex]::Match($gpuText, ',\s*(\d+)')
Require ($memMatch.Success) "Unable to read NVIDIA VRAM capacity."
$vram = [int]$memMatch.Groups[1].Value
Require ($vram -ge 7500) "Less than 7.5 GiB GPU memory; Wan2.2 5B offload plan not validated."
$base = Join-Path $env:USERPROFILE "OperationNoPants"
$root = [IO.Path]::GetPathRoot($base)
$disk = [IO.DriveInfo]::new($root)
Require ($disk.AvailableFreeSpace -ge 45000000000) "At least 45 GB free disk recommended before installation/models."
Write-Host ("Free disk: {0:N1} GB" -f ($disk.AvailableFreeSpace/1GB))
$repo = Join-Path $base "ComfyUI"
$requirements = @(
 @{dir="diffusion_models"; file="wan2.2_ti2v_5B_fp16.safetensors"; minBytes=9000000000},
 @{dir="text_encoders"; file="umt5_xxl_fp8_e4m3fn_scaled.safetensors"; minBytes=5500000000},
 @{dir="vae"; file="wan2.2_vae.safetensors"; minBytes=900000000}
)
$allModels = $true
foreach ($item in $requirements) {
 $path = Join-Path $repo ("models\"+$item.dir+"\"+$item.file)
 $exists = Test-Path -LiteralPath $path -PathType Leaf
 $bytes = if ($exists) { (Get-Item -LiteralPath $path).Length } else { 0 }
 $valid = $exists -and $bytes -ge $item.minBytes
 Write-Host ("Model {0}: {1} ({2:N2} GB)" -f $item.file, $(if($valid){"size-check passed"}else{"MISSING / too small"}), ($bytes/1GB))
 if (-not $valid) { $allModels=$false }
}
Write-Host "Model checks are file-size checks only, NOT cryptographic authenticity verification."
if ($CheckOnly) { Write-Host "Preflight only; no installation, server, or generation."; exit 0 }
if (-not (Test-Path -LiteralPath $repo)) {
 Require (-not $SkipInstall) "ComfyUI not installed; remove -SkipInstall to install."
 New-Item -ItemType Directory -Force -Path $base | Out-Null
 & git clone --depth 1 https://github.com/comfyanonymous/ComfyUI.git $repo
 Require ($LASTEXITCODE -eq 0) "ComfyUI clone failed."
}
Set-Location $repo
$py = Join-Path $repo ".venv\Scripts\python.exe"
if (-not (Test-Path $py)) {
 Require (-not $SkipInstall) "Python environment missing; remove -SkipInstall."
 & py -3.11 -m venv .venv
 Require ($LASTEXITCODE -eq 0) "Python 3.11 environment creation failed."
}
if (-not $SkipInstall) {
 & $py -m pip install --upgrade pip
 Require ($LASTEXITCODE -eq 0) "pip upgrade failed."
 & $py -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
 Require ($LASTEXITCODE -eq 0) "CUDA PyTorch install failed."
 & $py -m pip install -r requirements.txt
 Require ($LASTEXITCODE -eq 0) "ComfyUI requirements install failed."
}
& $py -c "import torch; print('CUDA available:',torch.cuda.is_available()); assert torch.cuda.is_available()"
Require ($LASTEXITCODE -eq 0) "PyTorch CUDA check failed."
if (-not $allModels) {
 Write-Host "Missing/undersized model files. Download official model files via ComfyUI template, then relaunch." -ForegroundColor Yellow
 Write-Host "Official guide: https://docs.comfy.org/tutorials/video/wan/wan2_2"
 Write-Host "No model downloads or generation attempted. Local UI will open for template setup."
}
Write-Host "Starting local-only ComfyUI at http://127.0.0.1:8188"
Start-Process "http://127.0.0.1:8188"
& $py main.py --listen 127.0.0.1 --port 8188 --lowvram
exit $LASTEXITCODE
