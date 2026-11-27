# Go cai dat HOMER Pro x64 {589CE2E1-27FE-4247-AE9F-1E2CDF6B1201}
param([switch]$Elevated)
$ErrorActionPreference = 'Stop'

$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin -and -not $Elevated) {
    Start-Process powershell.exe -ArgumentList @('-NoProfile','-ExecutionPolicy','Bypass','-File',$PSCommandPath,'-Elevated') -Verb RunAs
    exit 0
}

Get-Process -Name HomerPro -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2
$p = Start-Process -FilePath 'msiexec.exe' -ArgumentList @('/X{589CE2E1-27FE-4247-AE9F-1E2CDF6B1201}','/passive','/norestart') -Wait -PassThru
Write-Host "msiexec ExitCode:" $p.ExitCode
if ($p.ExitCode -eq 0) {
    $hDir = 'C:\Program Files\HOMER Energy'
    if (Test-Path $hDir) {
        $rem = Get-ChildItem $hDir -Recurse -Force -ErrorAction SilentlyContinue | Measure-Object
        if ($rem.Count -eq 0) {
            Remove-Item $hDir -Force -ErrorAction SilentlyContinue
        }
    }
    Write-Host "Da go sach HOMER Pro x64!"
} else {
    Write-Host "Kiem tra ma thoat msiexec:" $p.ExitCode
}
Read-Host 'Nhan Enter de dong'
