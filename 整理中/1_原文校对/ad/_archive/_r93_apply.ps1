$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath (Split-Path -Parent $MyInvocation.MyCommand.Path)
$book = '.\0_book.tex'
$frag = '.\_r93_blk_female.tex'
$ancF = '.\_r93_anchors.txt'
$bak  = '.\_r93_backup_0_book.tex'

$A = [IO.File]::ReadAllLines($ancF)
$startA = $A[0].Trim()
$endA   = $A[1].Trim()

$L = [IO.File]::ReadAllLines($book)
$F = [IO.File]::ReadAllLines($frag)

$si = -1; $ei = -1
for ($i = 0; $i -lt $L.Length; $i++) {
  $t = $L[$i].Trim()
  if ($si -lt 0 -and $t -eq $startA) { $si = $i }
  elseif ($si -ge 0 -and $t -eq $endA) { $ei = $i; break }
}
if ($si -lt 0) { throw 'start anchor not found' }
if ($ei -lt 0) { throw 'end anchor not found' }

Copy-Item -LiteralPath $book -Destination $bak -Force

$new = New-Object System.Collections.Generic.List[string]
for ($i = 0; $i -lt $si; $i++) { [void]$new.Add($L[$i]) }
foreach ($x in $F) { [void]$new.Add($x) }
[void]$new.Add('')
for ($i = $ei; $i -lt $L.Length; $i++) { [void]$new.Add($L[$i]) }

[IO.File]::WriteAllLines($book, $new, (New-Object System.Text.UTF8Encoding($false)))

$out = "OK start=$si end=$ei oldLines=$($L.Length) fragLines=$($F.Length) newLines=$($new.Count)"
[IO.File]::WriteAllText('.\_r93_apply_out.txt', $out, (New-Object System.Text.UTF8Encoding($false)))
Write-Output $out
