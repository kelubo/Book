$ErrorActionPreference='Stop'
$root = $PSScriptRoot
$femPath = Join-Path $root '2_female.tex'
$bkPath  = Join-Path $root '0_book.tex.r81bak_20260924_102404'

$femTxt = [Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes($femPath))
$bkTxt  = [Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes($bkPath))
$femArr = [regex]::Split($femTxt, "\r?\n")
$bkArr  = [regex]::Split($bkTxt, "\r?\n")

function Clean([string]$s){ return ($s -replace '(?<!\\)%.*$','').Trim() }
function FindEnd([string[]]$arr,[int]$W){
  $d=0
  for($k=$W;$k -lt $arr.Count;$k++){
    $c = Clean $arr[$k]
    if($c -eq '\begin{itemize}'){$d++}
    elseif($c -eq '\end{itemize}'){$d--; if($d -eq 0){return $k}}
  }
  return -1
}

# (femStart, bookStart, bookEnd) 1-based
$map = @(
 ,@(5510,30880,31021)
)

$lst = New-Object 'System.Collections.Generic.List[string]'
$lst.AddRange([string[]]$femArr)

$log = New-Object Text.StringBuilder
$done = 0; $skip = 0
for($m = $map.Count-1; $m -ge 0; $m--){
  $femStart = $map[$m][0]; $bs = $map[$m][1]; $be = $map[$m][2]
  $W = $femStart - 1
  $We = FindEnd $femArr $W
  if($We -lt 0){ [void]$log.AppendLine("SKIP F$femStart : no matching end"); $skip++; continue }

  $fblk = New-Object System.Collections.ArrayList
  for($k=$W;$k -le $We;$k++){ $c=Clean $femArr[$k]; if($c -ne ''){ [void]$fblk.Add($c) } }
  $bblk = New-Object System.Collections.ArrayList
  for($k=$bs-1;$k -le $be-1;$k++){ $c=Clean $bkArr[$k]; if($c -ne ''){ [void]$bblk.Add($c) } }

  $bp=0; $ok=$true
  for($i=0;$i -lt $fblk.Count;$i++){
    $found=$false
    while($bp -lt $bblk.Count){ if($bblk[$bp] -eq $fblk[$i]){ $bp++; $found=$true; break } else { $bp++ } }
    if(-not $found){ $ok=$false; break }
  }
  if(-not $ok){ [void]$log.AppendLine("SKIP F$femStart : fem not ordered-subsequence of book"); $skip++; continue }

  $cnt = $We - $W + 1
  [void]$log.AppendLine("FEM HEAD  : " + $femArr[$W])
  [void]$log.AppendLine("FEM TAIL  : " + $femArr[$We])
  [void]$log.AppendLine("BOOK HEAD : " + $bkArr[$bs-1])
  [void]$log.AppendLine("BOOK TAIL : " + $bkArr[$be-1])
  $lst.RemoveRange($W, $cnt)
  $ins = [string[]]$bkArr[($bs-1)..($be-1)]
  $lst.InsertRange($W, $ins)
  [void]$log.AppendLine("OK   F$femStart..$($We+1) ($cnt) <- B$bs..$be ($($be-$bs+1))  gain=$((($be-$bs+1)-$cnt))")
  $done++
}

$outTxt = ($lst.ToArray() -join "`r`n")
$enc = New-Object Text.UTF8Encoding($false)
[IO.File]::Copy($femPath, (Join-Path $root '2_female.tex.bak_fixD'), $true)
[IO.File]::WriteAllBytes($femPath, $enc.GetBytes($outTxt))
[IO.File]::WriteAllText((Join-Path $root '_m8_fixD_log.txt'), $log.ToString(), (New-Object Text.UTF8Encoding($false)))
Write-Output "DONE=$done SKIP=$skip"
