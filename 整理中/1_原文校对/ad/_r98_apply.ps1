$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath (Split-Path -Parent $MyInvocation.MyCommand.Path)
$book = '.\0_book.tex'
$ops  = '.\_r98_ops.txt'
$bak  = '.\_r98_backup_0_book.tex'
$enc  = New-Object System.Text.UTF8Encoding($false)
$lines = New-Object System.Collections.Generic.List[string]
foreach ($x in [IO.File]::ReadAllLines($book)) { [void]$lines.Add($x) }

function FindSig([System.Collections.Generic.List[string]]$lst, [string]$a, [string]$b, [int]$occ) {
  $single = ($b -eq 'NONE')
  $n = 0
  for ($i = 0; $i -lt $lst.Count; $i++) {
    $hit = $false
    if ($lst[$i].Trim() -eq $a) {
      if ($single) { $hit = $true }
      elseif ($i -lt ($lst.Count - 1) -and $lst[$i + 1].Trim() -eq $b) { $hit = $true }
    }
    if ($hit) { $n++; if ($n -eq $occ) { return $i } }
  }
  return -1
}

$actions = New-Object System.Collections.Generic.List[object]
foreach ($ol in [IO.File]::ReadAllLines($ops)) {
  if ($ol.Trim() -eq '') { continue }
  $f = $ol -split '@@@'
  $op = $f[0].Trim(); $frag = $f[1].Trim()
  $sa = $f[2]; $sb = $f[3]; $ea = $f[4]; $eb = $f[5]
  $os = [int]$f[6]; $oe = [int]$f[7]
  $si = FindSig $lines $sa $sb $os
  $ei = FindSig $lines $ea $eb $oe
  if ($si -lt 0) { throw "start sig not found: [$sa] / [$sb] occ=$os" }
  if ($ei -lt 0) { throw "end sig not found: [$ea] / [$eb] occ=$oe" }
  if ($ei -lt $si) { throw "end before start: $si $ei" }
  if ($op -eq 'DELETE' -and $ei -eq $si) { throw "delete empty: $si" }
  $actions.Add([pscustomobject]@{ op = $op; frag = $frag; si = $si; ei = $ei })
}

Copy-Item -LiteralPath $book -Destination $bak -Force

$log = New-Object System.Collections.Generic.List[string]
foreach ($a in ($actions | Sort-Object -Property si -Descending)) {
  $log.Add("$($a.op) si=$($a.si) ei=$($a.ei)")
  $lines.RemoveRange($a.si, ($a.ei - $a.si))
  if ($a.op -ne 'DELETE') {
    $ins = New-Object System.Collections.Generic.List[string]
    foreach ($x in [IO.File]::ReadAllLines($a.frag)) { [void]$ins.Add($x) }
    [void]$ins.Add('')
    $lines.InsertRange($a.si, $ins)
  }
}

[IO.File]::WriteAllLines($book, $lines, $enc)

$out = New-Object System.Collections.Generic.List[string]
$out.Add("OK ops=$($actions.Count) newLines=$($lines.Count)")
foreach ($l in $log) { $out.Add($l) }
[IO.File]::WriteAllLines('.\_r98_apply_out.txt', $out, $enc)
