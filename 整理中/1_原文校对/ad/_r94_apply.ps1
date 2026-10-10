$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath (Split-Path -Parent $MyInvocation.MyCommand.Path)
$book = '.\0_book.tex'
$ops  = '.\_r94_ops.txt'
$bak  = '.\_r94_backup_0_book.tex'
$enc  = New-Object System.Text.UTF8Encoding($false)

$lines = New-Object System.Collections.Generic.List[string]
foreach ($x in [IO.File]::ReadAllLines($book)) { [void]$lines.Add($x) }

function FindSig([System.Collections.Generic.List[string]]$lst, [string]$a, [string]$b) {
  for ($i = 0; $i -lt ($lst.Count - 1); $i++) {
    if ($lst[$i].Trim() -eq $a -and $lst[$i + 1].Trim() -eq $b) { return $i }
  }
  return -1
}

$actions = New-Object System.Collections.Generic.List[object]
foreach ($ol in [IO.File]::ReadAllLines($ops)) {
  if ($ol.Trim() -eq '') { continue }
  $f = $ol -split '@@@'
  if ($f.Count -lt 6) { throw "bad ops line: $ol" }
  $op = $f[0].Trim(); $frag = $f[1].Trim()
  $sa = $f[2]; $sb = $f[3]; $ea = $f[4]; $eb = $f[5]
  $si = FindSig $lines $sa $sb
  $ei = FindSig $lines $ea $eb
  if ($si -lt 0) { throw "start sig not found: [$sa] / [$sb]" }
  if ($ei -lt 0) { throw "end sig not found: [$ea] / [$eb]" }
  if ($ei -le $si) { throw "end not after start: $si $ei" }
  $actions.Add([pscustomobject]@{ op = $op; frag = $frag; si = $si; ei = $ei })
}

Copy-Item -LiteralPath $book -Destination $bak -Force

$sorted = $actions | Sort-Object -Property si -Descending
foreach ($a in $sorted) {
  $lines.RemoveRange($a.si, ($a.ei - $a.si))
  if ($a.op -ne 'DELETE') {
    $ins = New-Object System.Collections.Generic.List[string]
    foreach ($x in [IO.File]::ReadAllLines($a.frag)) { [void]$ins.Add($x) }
    [void]$ins.Add('')
    $lines.InsertRange($a.si, $ins)
  }
}

[IO.File]::WriteAllLines($book, $lines, $enc)
$report = foreach ($a in $sorted) { "  $($a.op) si=$($a.si) ei=$($a.ei) frag=$($a.frag)" }
$out = "OK ops=$($actions.Count) newLines=$($lines.Count)`n" + ($report -join "`n")
[IO.File]::WriteAllText('.\_r94_apply_out.txt', $out, $enc)
Write-Output $out
