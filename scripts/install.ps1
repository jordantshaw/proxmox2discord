param(
  [string]$AppDir = "$HOME\proxmox2discord"
)

$ErrorActionPreference = 'Stop'

Write-Host "📥 Cloning proxmox2discord into $AppDir…" -ForegroundColor Cyan
git clone https://github.com/jordantshaw/proxmox2discord.git $AppDir

Set-Location $AppDir

Write-Host "🐍 Installing Python dependencies…" -ForegroundColor Cyan
python -m pip install -r requirements.txt

Write-Host "`n✅ Installation complete!" -ForegroundColor Green
Write-Host "To start the server:" -ForegroundColor Yellow
Write-Host "  proxmox2discord" -ForegroundColor White
Write-Host "`nConfigure your Proxmox notification‐script to POST to:"
Write-Host "  http://<YOUR_SERVER>:6068/notify" -ForegroundColor White