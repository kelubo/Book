$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath (Split-Path -Parent $MyInvocation.MyCommand.Path)
$book = '.\0_book.tex'
$bak  = '.\_r98c_backup_0_book.tex'
$enc  = New-Object System.Text.UTF8Encoding($false)

$lines = New-Object System.Collections.Generic.List[string]
foreach ($x in [IO.File]::ReadAllLines($book)) { [void]$lines.Add($x) }

$A = New-Object System.Collections.Generic.List[string]
foreach ($x in [IO.File]::ReadAllLines('.\_r98c_anchors.txt')) { if ($x.Trim() -ne '') { [void]$A.Add($x) } }
if ($A.Count -ne 8) { throw "anchors count = $($A.Count), expect 8" }

function FindOne([System.Collections.Generic.List[string]]$lst, [string]$a) {
  $res = -1
  for ($i = 0; $i -lt $lst.Count; $i++) {
    if ($lst[$i].Trim() -eq $a) { if ($res -ge 0) { throw "anchor not unique: $a" }; $res = $i }
  }
  if ($res -lt 0) { throw "anchor not found: $a" }
  return $res
}

$idxMultiSec   = FindOne $lines $A[0]
$idxTcLine     = FindOne $lines $A[1]
$idxNos        = FindOne $lines $A[2]
$idxOldMulti   = FindOne $lines $A[3]
$idxFriend     = FindOne $lines $A[4]
$idxBlockStart = FindOne $lines $A[5]
$idxPart       = FindOne $lines $A[6]
$repairTitle   = $A[7]

if (-not ($idxMultiSec -lt $idxTcLine)) { throw "multiSec should be before tcLine" }
if (-not $lines[$idxTcLine - 1].Trim().StartsWith('\begin{tcolorbox}')) { throw "tc predecessor is not tcolorbox header" }
$idxTc = $idxTcLine - 1

if ($idxPart -le $idxBlockStart) { throw "part before block start" }
$block = New-Object System.Collections.Generic.List[string]
for ($i = $idxBlockStart; $i -lt $idxPart; $i++) { [void]$block.Add($lines[$i]) }
if ($block.Count -lt 10) { throw "block too small: $($block.Count)" }

if (-not ($idxTc -gt $idxPart -and $idxPart -gt $idxOldMulti -and $idxOldMulti -gt $idxNos)) {
  throw "unexpected order: tc=$idxTc part=$idxPart oldMulti=$idxOldMulti nos=$idxNos"
}
if ($idxFriend -le $idxOldMulti) { throw "friend before oldMulti" }

Copy-Item -LiteralPath $book -Destination $bak -Force

$log = New-Object System.Collections.Generic.List[string]

$ins1 = New-Object System.Collections.Generic.List[string]
foreach ($x in [IO.File]::ReadAllLines('.\_r98c_multisup.tex')) { [void]$ins1.Add($x) }
[void]$ins1.Add('')
$lines.InsertRange($idxTc, $ins1)
$log.Add("insert multisup at $idxTc ($($ins1.Count) lines)")

$lines.RemoveRange($idxBlockStart, ($idxPart - $idxBlockStart))
$log.Add("delete repair block [$idxBlockStart,$idxPart) = $($idxPart - $idxBlockStart) lines")

$lines.RemoveRange($idxOldMulti, ($idxFriend - $idxOldMulti))
$log.Add("delete old multi section [$idxOldMulti,$idxFriend) = $($idxFriend - $idxOldMulti) lines")

$ins2 = New-Object System.Collections.Generic.List[string]
[void]$ins2.Add($repairTitle)
[void]$ins2.Add('')
foreach ($x in $block) { [void]$ins2.Add($x) }
[void]$ins2.Add('')
$lines.InsertRange($idxNos, $ins2)
$log.Add("insert repair at $idxNos ($($ins2.Count) lines)")

[IO.File]::WriteAllLines($book, $lines, $enc)

$out = New-Object System.Collections.Generic.List[string]
$out.Add("OK newLines=$($lines.Count) blockLines=$($block.Count)")
foreach ($l in $log) { $out.Add($l) }
[IO.File]::WriteAllLines('.\_r98c_apply_out.txt', $out, $enc)
