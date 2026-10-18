$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
$file = Join-Path $root '2_female.tex'
$dataFile = Join-Path $root '_m8_clean_data.txt'
$log = Join-Path $root '_m8_clean_log.txt'
$bak = Join-Path $root '2_female.tex.bak_clean'

$data = [Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes($dataFile))
$dl = [regex]::Split($data, "\r?\n")
$marker  = $dl[0]
$anchor  = $dl[1]
$stale   = $dl[2]
$emptsec = $dl[3]

$bytes = [IO.File]::ReadAllBytes($file)
$bom = 'NOBOM'
if ($bytes.Length -ge 3 -and $bytes[0] -eq 239 -and $bytes[1] -eq 187 -and $bytes[2] -eq 191) { $bom = 'BOM' }
$txt = [Text.Encoding]::UTF8.GetString($bytes)
$lines = @([regex]::Split($txt, "\r?\n"))

$out = @()
$out += "BOM=$bom origElts=$($lines.Count)"

# locate marker
$s = -1
for ($i = 0; $i -lt $lines.Count; $i++) { if ($lines[$i] -eq $marker) { $s = $i; break } }
$out += "markerIdx0=$s  markerLine1=$($s + 1)"
$bad = 0
if ($s -ne 492) { $out += "ASSERT-FAIL marker not at 0-based 492"; $bad = 1 }

# extract block = 15 elements
$block = @()
for ($k = $s; $k -le $s + 14; $k++) { $block += $lines[$k] }
$out += "blockLen=$($block.Count) blockEnd=[$($block[14])]"
if ($block[14] -ne '\end{tcolorbox}') { $out += "ASSERT-FAIL block end"; $bad = 1 }

# check comment header just before
$out += "pre4=[$($lines[$s-4])]"
$out += "pre1=[$($lines[$s-1])]"
$out += "post15=[$($lines[$s+15])]"
$out += "post16=[$($lines[$s+16])]"
$out += "post17=[$($lines[$s+17])]"

# remove top range 0-based s-4 .. s+17
$rf = $s - 4
$rt = $s + 17
$new = @()
for ($i = 0; $i -lt $lines.Count; $i++) {
  if ($i -ge $rf -and $i -le $rt) { continue }
  $new += $lines[$i]
}
$out += "afterTopRemove=$($new.Count) expected=$($lines.Count - 22)"

# insert block before anchor
$a = -1
for ($i = 0; $i -lt $new.Count; $i++) { if ($new[$i] -eq $anchor) { $a = $i; break } }
$out += "anchorIdx0=$a anchorLine1=$($a + 1)"
if ($a -lt 0) { $out += "ASSERT-FAIL anchor missing"; $bad = 1 }
elseif ($new[$a-1] -ne '') { $out += "ASSERT-FAIL pre-anchor not blank: [$($new[$a-1])]"; $bad = 1 }

$build = New-Object System.Collections.ArrayList
for ($i = 0; $i -lt $a; $i++) { [void]$build.Add($new[$i]) }
foreach ($b in $block) { [void]$build.Add($b) }
[void]$build.Add('')
for ($i = $a; $i -lt $new.Count; $i++) { [void]$build.Add($new[$i]) }
$out += "afterInsert=$($build.Count) expected=$($new.Count + 16)"

# remove stale comments
$cntStale = 0
$finalA = New-Object System.Collections.ArrayList
foreach ($l in $build) { if ($l -eq $stale) { $cntStale++; continue }; [void]$finalA.Add($l) }
$out += "staleRemoved=$cntStale"
if ($cntStale -ne 49) { $out += "ASSERT-FAIL stale count != 49"; $bad = 1 }
$out += "final=$($finalA.Count)"

# asserts on final
$cSec = 0; $cMark = 0; $cAnch = 0
foreach ($l in $finalA) {
  if ($l -eq $emptsec) { $cSec++ }
  if ($l -eq $marker) { $cMark++ }
  if ($l -eq $anchor) { $cAnch++ }
}
$out += "cntEmptySection=$cSec cntMarker=$cMark cntAnchor=$cAnch"
if ($cSec -ne 1) { $out += "ASSERT-FAIL empty section count"; $bad = 1 }
if ($cMark -ne 1) { $out += "ASSERT-FAIL marker count"; $bad = 1 }
if ($cAnch -ne 1) { $out += "ASSERT-FAIL anchor count"; $bad = 1 }

# placement check
$ai = -1
for ($i = 0; $i -lt $finalA.Count; $i++) { if ($finalA[$i] -eq $anchor) { $ai = $i; break } }
$out += "placedBeforeAnchor-1=[$($finalA[$ai-1])] -2=[$($finalA[$ai-2])] -16=[$($finalA[$ai-16])]"
if ($finalA[$ai-2] -ne '\end{tcolorbox}') { $out += "ASSERT-FAIL placement end"; $bad = 1 }
if ($finalA[$ai-16] -ne $marker) { $out += "ASSERT-FAIL placement start"; $bad = 1 }

# top region check
for ($i = 0; $i -lt 12; $i++) { $out += "top[$i]=[$($finalA[$i])]" }

if ($bad -eq 0) {
  Copy-Item -LiteralPath $file -Destination $bak -Force
  $enc = New-Object Text.UTF8Encoding($false)
  $joined = ($finalA.ToArray() -join "`r`n")
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
