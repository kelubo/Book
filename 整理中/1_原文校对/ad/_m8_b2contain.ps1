$ErrorActionPreference='Stop'
$root = $PSScriptRoot
$femPath = Join-Path $root '2_female.tex'
$t = [Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes($femPath))
$arr = [regex]::Split($t, "\r?\n")
function Clean([string]$s){ return ($s -replace '(?<!\\)%.*$','').Trim() }

# batch1 = 5509..6512 (headers+body of batch1 subsubsections), batch2 = 6513..6741
$b1 = @{}
for($i=5508;$i -le 6511;$i++){ $c=Clean $arr[$i]; if($c -ne ''){ $b1[$c]=1 } }

# whole file set
$all = @{}
for($i=0;$i -lt $arr.Count;$i++){ $c=Clean $arr[$i]; if($c -ne ''){ if(-not $all.ContainsKey($c)){ $all[$c]=$i+1 } } }

$sb = New-Object Text.StringBuilder
[void]$sb.AppendLine("=== batch2 lines NOT in batch1 (new knowledge?) ===")
$newc=0; $tot=0
for($i=6512;$i -le 6740;$i++){
  $c = Clean $arr[$i]
  if($c -eq ''){ continue }
  $tot++
  if(-not $b1.ContainsKey($c)){
    $newc++
    $where = if($all.ContainsKey($c)){ "firstAt:" + $all[$c] } else { "NOWHERE" }
    [void]$sb.AppendLine(("{0}: [{1}] {2}" -f ($i+1), $where, $c))
  }
}
[void]$sb.AppendLine("")
[void]$sb.AppendLine("TOTAL_nonempty=$tot  NEW_notInBatch1=$newc")
[IO.File]::WriteAllText((Join-Path $root '_m8_b2c.txt'), $sb.ToString(), (New-Object Text.UTF8Encoding($false)))
Write-Output "DONE"
