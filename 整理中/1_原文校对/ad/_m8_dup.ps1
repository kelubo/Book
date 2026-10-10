$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
$file = Join-Path $root '2_female.tex'
$dataFile = Join-Path $root '_m8_dup_data.txt'
$log = Join-Path $root '_m8_dup_log.txt'
$bak = Join-Path $root '2_female.tex.bak_dup'

$data = [Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes($dataFile))
$dl = [regex]::Split($data, "\r?\n")
$titleH = $dl[0]
$physH  = $dl[1]
$editAnch = $dl[2]
$defAnch  = $dl[3]

$bytes = [IO.File]::ReadAllBytes($file)
$bom = 'NOBOM'
if ($bytes.Length -ge 3 -and $bytes[0] -eq 239 -and $bytes[1] -eq 187 -and $bytes[2] -eq 191) { $bom = 'BOM' }
$txt = [Text.Encoding]::UTF8.GetString($bytes)
$lines = @([regex]::Split($txt, "\r?\n"))

$out = @()
$out += "BOM=$bom n0=$($lines.Count)"
$bad = 0

# locate unique title line (Block A header)
$idxA = -1; $cT = 0
for ($i = 0; $i -lt $lines.Count; $i++) { if ($lines[$i] -eq $titleH) { $cT++; if ($idxA -lt 0) { $idxA = $i } } }
$out += "cntTitle=$cT idxA0=$idxA idxA1=$($idxA + 1)"
if ($cT -ne 1) { $out += "ASSERT-FAIL cntTitle"; $bad = 1 }

# locate unique physics subsection line (boundary after Block A)
$idxP = -1; $cP = 0
for ($i = 0; $i -lt $lines.Count; $i++) { if ($lines[$i] -eq $physH) { $cP++; if ($idxP -lt 0) { $idxP = $i } } }
$out += "cntPhys=$cP idxP0=$idxP idxP1=$($idxP + 1)"
if ($cP -ne 1) { $out += "ASSERT-FAIL cntPhys"; $bad = 1 }

if ($bad -eq 0) {
  $out += "gap=$($idxP - $idxA) (expect 55)"
  if (($idxP - $idxA) -ne 55) { $out += "ASSERT-FAIL gap"; $bad = 1 }
  $out += "preDelBeforeA=[$($lines[$idxA - 1])]"
  $out += "preDelAtP=[$($lines[$idxP])]"
  $out += "blockFirst=[$($lines[$idxA])]"
  $out += "blockLast=[$($lines[$idxP - 1])]"
}

$del = New-Object System.Collections.ArrayList
if ($bad -eq 0) {
  for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($i -ge $idxA -and $i -le $idxP - 1) { continue }
    [void]$del.Add($lines[$i])
  }
  $out += "afterDel=$($del.Count) expected=$($lines.Count - 55)"
  if ($del.Count -ne ($lines.Count - 55)) { $out += "ASSERT-FAIL delcount"; $bad = 1 }
}

$idxE = -1
if ($bad -eq 0) {
  $cE = 0
  for ($i = 0; $i -lt $del.Count; $i++) { if ($del[$i].Contains($editAnch)) { $cE++; if ($idxE -lt 0) { $idxE = $i } } }
  $out += "cntEdit=$cE idxE0=$idxE idxE1=$($idxE + 1)"
  if ($cE -ne 1) { $out += "ASSERT-FAIL cntEdit"; $bad = 1 }
}

$idxD = -1
if ($bad -eq 0) {
  for ($i = $idxE + 1; $i -lt $del.Count; $i++) { if ($del[$i].Contains($defAnch)) { $idxD = $i; break } }
  $out += "idxD0=$idxD idxD1=$($idxD + 1) gap2=$($idxD - $idxE) (expect 4)"
  if (($idxD - $idxE) -ne 4) { $out += "ASSERT-FAIL gap2"; $bad = 1 }
  if ($del[$idxE + 1] -ne '' -or $del[$idxE + 2] -ne '' -or $del[$idxE + 3] -ne '') { $out += "ASSERT-FAIL mid not blank"; $bad = 1 }
  $out += "editLine=[$($del[$idxE])]"
  $out += "defLine=[$($del[$idxD])]"
}

$build = New-Object System.Collections.ArrayList
if ($bad -eq 0) {
  for ($i = 0; $i -le $idxE; $i++) { [void]$build.Add($del[$i]) }
  [void]$build.Add($titleH)
  [void]$build.Add('')
  for ($i = $idxD; $i -lt $del.Count; $i++) { [void]$build.Add($del[$i]) }
  $out += "afterIns=$($build.Count) expected=$($del.Count - 1)"
  if ($build.Count -ne ($del.Count - 1)) { $out += "ASSERT-FAIL inscount"; $bad = 1 }
}

if ($bad -eq 0) {
  $cT2 = 0; $cD2 = 0
  foreach ($l in $build) { if ($l -eq $titleH) { $cT2++ }; if ($l.Contains($defAnch)) { $cD2++ } }
  $out += "finalTitle=$cT2 finalDef=$cD2"
  if ($cT2 -ne 1) { $out += "ASSERT-FAIL finalTitle"; $bad = 1 }
  if ($cD2 -ne 1) { $out += "ASSERT-FAIL finalDef"; $bad = 1 }

  $ti = -1
  for ($i = 0; $i -lt $build.Count; $i++) { if ($build[$i] -eq $titleH) { $ti = $i; break } }
  $out += "placedBefore3=[$($build[$ti - 3])]"
  $out += "placedBefore1=[$($build[$ti - 1])]"
  $out += "placedAfter1=[$($build[$ti + 1])]"
  $out += "placedAfter2=[$($build[$ti + 2])]"
}

if ($bad -eq 0) {
  Copy-Item -LiteralPath $file -Destination $bak -Force
  $enc = New-Object Text.UTF8Encoding($false)
  $joined = ($build.ToArray() -join "`r`n")
  [IO.File]::WriteAllText($file, $joined, $enc)
  $sz = (Get-Item -LiteralPath $file).Length
  $out += "writtenSize=$sz"
  if ($sz -lt 100000) { $out += "ASSERT-FAIL written too small"; $bad = 2 }
  $out += "DONE bad=$bad written"
} else {
  $out += "DONE bad=$bad NOT written"
}

[IO.File]::WriteAllText($log, ($out -join "`r`n"), (New-Object Text.UTF8Encoding($false)))
Write-Output ($out -join "`r`n")
