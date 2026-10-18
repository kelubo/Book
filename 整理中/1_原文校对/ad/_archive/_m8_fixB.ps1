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
 @(831,31980,32019),
 @(994,32195,32232),
 @(1175,32437,32478),
 @(1230,32509,32540),
 @(1509,32891,32931),
 @(1561,32960,32996),
 @(3375,33218,33264),
 @(3467,33330,33369),
 @(3691,33603,33650),
 @(3766,33693,33728),
 @(4268,34294,34330),
 @(4663,34740,34772),
 @(11454,41512,41545),
 @(11485,41551,41580),
 @(11506,41586,41625),
 @(11569,41667,41688),
 @(11605,41706,41725),
 @(11627,41731,41756),
 @(11682,41792,41822),
 @(11709,41828,41858),
 @(11734,41864,41907),
 @(11891,42037,42061),
 @(11918,42067,42094),
 @(11947,42100,42135),
 @(12039,42196,42211),
 @(18307,58183,58208),
 @(18418,58297,58338)
)

$lst = New-Object 'System.Collections.Generic.List[string]'
$lst.AddRange([string[]]$femArr)

$log = New-Object Text.StringBuilder
$done = 0; $skip = 0
# process bottom-up
for($m = $map.Count-1; $m -ge 0; $m--){
  $femStart = $map[$m][0]; $bs = $map[$m][1]; $be = $map[$m][2]
  $W = $femStart - 1
  $We = FindEnd $femArr $W
  if($We -lt 0){ [void]$log.AppendLine("SKIP F$femStart : no matching end"); $skip++; continue }

  # collect cleaned non-empty fem block lines
  $fblk = New-Object System.Collections.ArrayList
  for($k=$W;$k -le $We;$k++){ $c=Clean $femArr[$k]; if($c -ne ''){ [void]$fblk.Add($c) } }
  # collect cleaned non-empty book block lines
  $bblk = New-Object System.Collections.ArrayList
  for($k=$bs-1;$k -le $be-1;$k++){ $c=Clean $bkArr[$k]; if($c -ne ''){ [void]$bblk.Add($c) } }

  # verify fblk is ordered subsequence of bblk
  $bp=0; $ok=$true
  for($i=0;$i -lt $fblk.Count;$i++){
    $found=$false
    while($bp -lt $bblk.Count){ if($bblk[$bp] -eq $fblk[$i]){ $bp++; $found=$true; break } else { $bp++ } }
    if(-not $found){ $ok=$false; break }
  }
  if(-not $ok){ [void]$log.AppendLine("SKIP F$femStart : fem not ordered-subsequence of book"); $skip++; continue }

  $cnt = $We - $W + 1
  $lst.RemoveRange($W, $cnt)
  $ins = [string[]]$bkArr[($bs-1)..($be-1)]
  $lst.InsertRange($W, $ins)
  [void]$log.AppendLine("OK   F$femStart..$($We+1) ($cnt) <- B$bs..$be ($($be-$bs+1))  gain=$((($be-$bs+1)-$cnt))")
  $done++
}

$outTxt = ($lst.ToArray() -join "`r`n")
$enc = New-Object Text.UTF8Encoding($false)
[IO.File]::WriteAllBytes($femPath, $enc.GetBytes($outTxt))
[IO.File]::WriteAllText((Join-Path $root '_m8_fixB_log.txt'), $log.ToString(), (New-Object Text.UTF8Encoding($false)))
Write-Output "DONE=$done SKIP=$skip"
