# -*- coding: utf-8 -*-
$ErrorActionPreference = 'Stop'

Add-Type -AssemblyName System.Runtime.Serialization
Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem

$homerDir = 'C:\Program Files\HOMER Energy\HOMER Pro x64'
$srcPath  = 'D:\Du an\code\chinhan\homer\ST_Giai_doan_3_toi_uu.homer'
$dstPath  = 'D:\Du an\code\chinhan\homer\ST_Giai_doan_3_toi_uu_783kW.homer'

Add-Type -TypeDefinition @"
using System;
using System.IO;
using System.Reflection;
public static class HomerResolver783 {
    public static void Init(string dir) {
        AppDomain.CurrentDomain.AssemblyResolve += (s, e) => {
            var name = new AssemblyName(e.Name).Name + ".dll";
            var p = Path.Combine(dir, name);
            return File.Exists(p) ? Assembly.LoadFrom(p) : null;
        };
    }
}
"@
[HomerResolver783]::Init($homerDir)
[System.Reflection.Assembly]::LoadFrom((Join-Path $homerDir 'HomerModel.dll')) | Out-Null

# 1. Doc file .homer goc bang API chinh thuc Homer.ReadHomer
$h = New-Object HomerModel.Model.Homer
if (-not $h.ReadHomer($srcPath)) {
    throw "Failed to ReadHomer source: $srcPath"
}
$prob = $h.Problem

# 2. Cap nhat duong cong phu tai 24h thuc te dao ST (tong ngay = 10.337 kWh/ngay, Peak <= 783.1 kW)
$wd24 = [float[]]@(245, 235, 230, 230, 250, 310, 370, 420, 450, 470, 485, 495, 480, 465, 470, 485, 515, 560, 620, 640, 615, 540, 405, 352)
$we24 = [float[]]@(250, 240, 235, 235, 250, 300, 360, 410, 440, 465, 485, 495, 485, 475, 480, 495, 525, 565, 620, 640, 620, 545, 410, 312)

$wd288 = New-Object 'System.Single[]' 288
$we288 = New-Object 'System.Single[]' 288
for ($m = 0; $m -lt 12; $m++) {
    for ($hr = 0; $hr -lt 24; $hr++) {
        $wd288[$m * 24 + $hr] = $wd24[$hr]
        $we288[$m * 24 + $hr] = $we24[$hr]
    }
}

$ld = $prob.LoadFancy[0]
$ld.Data.Weekdays = $wd288
$ld.Data.Weekends = $we288
$ld.Data.DailyNoise = [double]3.0
$ld.Data.TimestepNoise = [double]5.0

# Dam bao ScaledAnnualAverageSensitivity giu 10337
$ld.ScaledAnnualAverageSensitivity.Clear()
$ld.ScaledAnnualAverageSensitivity.Add([decimal]10337)

Write-Host "Peak after initial noise (3%, 5%):" $ld.Data.Peak
if ([double]$ld.Data.Peak -gt 783.1) {
    Write-Host "Peak > 783.1 kW, dieu chinh nhe gio cao diem va giam nhieu ve (2%, 4%)..."
    $wd24b = [float[]]@(260, 250, 245, 245, 265, 320, 380, 425, 455, 475, 490, 500, 485, 470, 475, 490, 520, 560, 600, 615, 595, 535, 415, 362)
    $we24b = [float[]]@(265, 255, 250, 250, 265, 310, 370, 415, 445, 470, 490, 500, 490, 480, 485, 500, 530, 565, 600, 615, 600, 540, 420, 322)
    for ($m = 0; $m -lt 12; $m++) {
        for ($hr = 0; $hr -lt 24; $hr++) {
            $wd288[$m * 24 + $hr] = $wd24b[$hr]
            $we288[$m * 24 + $hr] = $we24b[$hr]
        }
    }
    $ld.Data.Weekdays = $wd288
    $ld.Data.Weekends = $we288
    $ld.Data.DailyNoise = [double]2.0
    $ld.Data.TimestepNoise = [double]4.0
    Write-Host "Peak after tuning:" $ld.Data.Peak
}

# 3. Mo rong PV SearchSpace len 0..1600 kWp
$pvVals = $prob.Pvs[0].OptimizationVariable.SearchSpace.Values
$pvVals.Clear()
foreach ($v in @(0, 600, 800, 1000, 1200, 1400, 1600)) {
    $pvVals.Add([decimal]$v)
}

Write-Host "In-memory Check -> HasErrors:" $prob.HasErrors "| CantBeCalculated:" $prob.CantBeCalculated "| Peak:" $ld.Data.Peak
if ($prob.HasErrors -or $prob.CantBeCalculated) {
    throw "Model reported HasErrors=$($prob.HasErrors) CantBeCalculated=$($prob.CantBeCalculated)"
}

# 4. Xoa ket qua cu va luu qua API chinh thuc WriteHomer
$h.CalculatedProblem = $null
$h.Results = $null
if (Test-Path $dstPath) { Remove-Item $dstPath -Force }
if (-not $h.WriteHomer($dstPath)) {
    throw "WriteHomer returned False!"
}

# 5. Copy 'state' entry tu file nguon
$stateBytes = $null
$zipIn = [System.IO.Compression.ZipFile]::OpenRead($srcPath)
try {
    $stEntry = $zipIn.GetEntry('state')
    if ($null -ne $stEntry) {
        $ms = New-Object System.IO.MemoryStream
        $es = $stEntry.Open(); $es.CopyTo($ms); $es.Close()
        $stateBytes = $ms.ToArray(); $ms.Dispose()
    }
} finally {
    $zipIn.Dispose()
}
if ($null -ne $stateBytes) {
    $zipUpd = [System.IO.Compression.ZipFile]::Open($dstPath, [System.IO.Compression.ZipArchiveMode]::Update)
    try {
        $oldSt = $zipUpd.GetEntry('state')
        if ($null -ne $oldSt) { $oldSt.Delete() }
        $newSt = $zipUpd.CreateEntry('state')
        $ns = $newSt.Open()
        $ns.Write($stateBytes, 0, $stateBytes.Length)
        $ns.Close()
    } finally {
        $zipUpd.Dispose()
    }
}

# 6. Kiem chung doc lai bang Homer.ReadHomer
$hCheck = New-Object HomerModel.Model.Homer
$okCheck = $hCheck.ReadHomer($dstPath)
if (-not $okCheck) {
    throw "Verification ReadHomer FAILED on $dstPath!"
}
$ldC = $hCheck.Problem.LoadFancy[0]
Write-Host "VERIFY OK -> ReadHomer=$okCheck | HasErrors=$($hCheck.Problem.HasErrors) | CantBeCalculated=$($hCheck.Problem.CantBeCalculated)"
Write-Host "VERIFY LOAD -> Peak=$([math]::Round([double]$ldC.Data.Peak, 2)) kW | DailyNoise=$($ldC.Data.DailyNoise)% | TimestepNoise=$($ldC.Data.TimestepNoise)% | Weekdays[0..3]=$($ldC.Data.Weekdays[0]),$($ldC.Data.Weekdays[1]),$($ldC.Data.Weekdays[2]),$($ldC.Data.Weekdays[3]) | Weekdays[19]=$($ldC.Data.Weekdays[19])"
Write-Host "VERIFY PV SEARCH -> $($hCheck.Problem.Pvs[0].OptimizationVariable.SearchSpace.Values -join ', ')"
