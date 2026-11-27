# -*- coding: utf-8 -*-
$ErrorActionPreference = 'Stop'

Add-Type -AssemblyName System.Runtime.Serialization
Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem

$homerDir = 'C:\Program Files\HOMER Energy\HOMER Pro x64'
$srcPath  = 'D:\Du an\code\chinhan\HO_SO_BAO_CAO_CHIEU_NAY\05_File_Mo_Phong_HOMER_Pro.homer'
$dstPath  = 'D:\Du an\code\chinhan\ST_Giai_doan_3_toi_uu.homer'
$wfPath   = Join-Path $homerDir 'Library\Component\Wind Turbine\Windflow 45 [500kW].xml'
$genPath  = Join-Path $homerDir 'Library\Component\Generator\Autosize Genset.xml'

Add-Type -TypeDefinition @"
using System;
using System.IO;
using System.Reflection;
public static class HomerResolver {
    public static void Init(string dir) {
        AppDomain.CurrentDomain.AssemblyResolve += (s, e) => {
            var name = new AssemblyName(e.Name).Name + ".dll";
            var p = Path.Combine(dir, name);
            return File.Exists(p) ? Assembly.LoadFrom(p) : null;
        };
    }
}
"@
[HomerResolver]::Init($homerDir)
[System.Reflection.Assembly]::LoadFrom((Join-Path $homerDir 'HomerModel.dll')) | Out-Null

# 1. Load original .homer via official Homer.ReadHomer
$h = New-Object HomerModel.Model.Homer
if (-not $h.ReadHomer($srcPath)) {
    throw "Failed to ReadHomer source: $srcPath"
}
$prob = $h.Problem

# 2. Enforce 0% capacity shortage
$shortageCol = $prob.SimulationParameters.Constraints.MaximumAnnualCapacityShortageSensitivity
$shortageCol.Clear()
$shortageCol.Add([decimal]0.00)

# 3. Converter search space (0, 800, 1000, 1200 kW)
$prob.Converter.Optimizer.UseOptimizer = $false
$convCap = $prob.Converter.CapacityOptimization
$convCap.Clear()
foreach ($v in @(0, 800, 1000, 1200)) { $convCap.Add([decimal]$v) }

# 4. PV search space (0, 600, 800, 1000, 1200 kWp)
$pvOpt = $prob.Pvs[0].OptimizationVariable
$pvOpt.UseOptimizer = $false
$pvVals = $pvOpt.SearchSpace.Values
$pvVals.Clear()
foreach ($v in @(0, 600, 800, 1000, 1200)) { $pvVals.Add([decimal]$v) }

# 5. Wind Turbine: Windflow 45 [500kW] via official Problem.Add()
$dcsWt = New-Object System.Runtime.Serialization.DataContractSerializer([HomerModel.Model.Components.WindTurbine])
$fsWt = [System.IO.File]::OpenRead($wfPath)
try { $wf = $dcsWt.ReadObject($fsWt) } finally { $fsWt.Close() }

$wf.HubHeightSensitivity.Clear()
$wf.HubHeightSensitivity.Add([decimal]47.00)

$wfOpt = $wf.OptimizationVariable
$wfOpt.UseOptimizer = $false
$wfCost = $wfOpt.CostTable.Costs[0]
$wfCost.Initial     = [decimal]961500
$wfCost.Replacement = [decimal]961500
$wfCost.Operating   = [decimal]19230
$wfVals = $wfOpt.SearchSpace.Values
$wfVals.Clear()
foreach ($q in @(0, 1, 2)) { $wfVals.Add([int]$q) }

$prob.WindTurbines.Clear()
$prob.Add($wf)

# 6. Storage search space (20, 40, 60, 80, 117 strings)
$stOpt = $prob.Storage[0].OptimizationVariables[0]
$stOpt.UseOptimizer = $false
$stVals = $stOpt.SearchSpace.Values
$stVals.Clear()
foreach ($q in @(20, 40, 60, 80, 117)) { $stVals.Add([int]$q) }

# 7. Generator: Autosize Genset via official Problem.Add()
$dcsGen = New-Object System.Runtime.Serialization.DataContractSerializer([HomerModel.Model.Components.Generator])
$fsGen = [System.IO.File]::OpenRead($genPath)
try { $ag = $dcsGen.ReadObject($fsGen) } finally { $fsGen.Close() }

$ag.Autosize = $true
$prob.Generators.Clear()
$prob.Add($ag)

Write-Host "In-memory Check -> HasErrors:" $prob.HasErrors "| CantBeCalculated:" $prob.CantBeCalculated
if ($prob.HasErrors -or $prob.CantBeCalculated) {
    throw "Model reported HasErrors=$($prob.HasErrors) CantBeCalculated=$($prob.CantBeCalculated)"
}

# 8. Clear stale results and save via official Homer.WriteHomer
$h.CalculatedProblem = $null
$h.Results = $null
if (Test-Path $dstPath) { Remove-Item $dstPath -Force }
if (-not $h.WriteHomer($dstPath)) {
    throw "WriteHomer returned False!"
}

# 9. Copy 'state' entry from source if WriteHomer omitted it
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
        if ($null -eq $zipUpd.GetEntry('state')) {
            $e = $zipUpd.CreateEntry('state', [System.IO.Compression.CompressionLevel]::Optimal)
            $es = $e.Open(); $es.Write($stateBytes, 0, $stateBytes.Length); $es.Close()
        }
        $entries = @($zipUpd.Entries | Select-Object -ExpandProperty FullName)
    } finally {
        $zipUpd.Dispose()
    }
}

# 10. Strict verification via official Homer.ReadHomer (both overloads)
$hCheck = New-Object HomerModel.Model.Homer
$p2 = $null; $cp2 = $null; $res2 = $null; $msg = $null
$ok1 = $hCheck.ReadHomer($dstPath, [ref]$p2, [ref]$cp2, [ref]$res2, [ref]$msg, [System.Threading.CancellationToken]::None, $null, $null)
$hCheck2 = New-Object HomerModel.Model.Homer
$ok2 = $hCheck2.ReadHomer($dstPath)

$zipRead = [System.IO.Compression.ZipFile]::OpenRead($dstPath)
try {
    $sr = New-Object System.IO.StreamReader($zipRead.GetEntry('problem').Open(), [System.Text.Encoding]::UTF8)
    $xmlText = $sr.ReadToEnd(); $sr.Close()
    $srV = New-Object System.IO.StreamReader($zipRead.GetEntry('version').Open(), [System.Text.Encoding]::UTF8)
    $verText = $srV.ReadToEnd().Trim(); $srV.Close()
} finally {
    $zipRead.Dispose()
}

$hasXmlnsA = $xmlText.Contains('xmlns:a=')
$hasZSize  = $xmlText.Contains('z:Size=')
$fuelRefOk = [object]::ReferenceEquals($p2.Generators[0].FuelResource, $p2.FuelResources[0])

Write-Host "=== OFFICIAL READHOMER VERIFICATION ==="
Write-Host "File        :" $dstPath ("({0:N1} KB)" -f ((Get-Item $dstPath).Length / 1KB))
Write-Host "Version     :" $verText "| Entries:" ($entries -join ', ')
Write-Host "XML Format  : xmlns:a=" $hasXmlnsA "| z:Size=" $hasZSize
Write-Host "ReadHomer 1 :" $ok1 "| FailMsg:" ([string]$msg)
Write-Host "ReadHomer 2 :" $ok2 "| ModelError:" $hCheck2.ModelError
Write-Host "HasErrors   :" $p2.HasErrors "| CantBeCalculated:" $p2.CantBeCalculated
Write-Host "MaxShortage :" ($p2.SimulationParameters.Constraints.MaximumAnnualCapacityShortageSensitivity -join ',')
Write-Host "PV          :" $p2.Pvs[0].Name "->" ($p2.Pvs[0].OptimizationVariable.SearchSpace.Values -join ',')
Write-Host "Wind        :" $p2.WindTurbines[0].Name "-> Qty:" ($p2.WindTurbines[0].OptimizationVariable.SearchSpace.Values -join ',') "| Hub:" ($p2.WindTurbines[0].HubHeightSensitivity -join ',') "| Cost:" $p2.WindTurbines[0].OptimizationVariable.CostTable.Costs[0].Initial "/" $p2.WindTurbines[0].OptimizationVariable.CostTable.Costs[0].Replacement "/" $p2.WindTurbines[0].OptimizationVariable.CostTable.Costs[0].Operating
Write-Host "Storage     :" $p2.Storage[0].Name "-> Strings:" ($p2.Storage[0].OptimizationVariables[0].SearchSpace.Values -join ',')
Write-Host "Converter   :" $p2.Converter.Name "-> Cap:" ($p2.Converter.CapacityOptimization -join ',')
Write-Host "Generator   :" $p2.Generators[0].Name "| Autosize:" $p2.Generators[0].Autosize "| FuelRefEquals:" $fuelRefOk

if (-not $ok1 -or -not $ok2 -or $msg -or $p2.HasErrors -or $p2.CantBeCalculated -or -not $fuelRefOk -or -not $hasXmlnsA -or $hasZSize) {
    throw "Verification failed!"
}
