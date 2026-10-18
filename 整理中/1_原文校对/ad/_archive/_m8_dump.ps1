$ErrorActionPreference='Stop'
$root = $PSScriptRoot
$p = Join-Path $root '2_female.tex'
$lines = [Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes($p)) -split "`r`n"
$n = $lines.Count
$out = New-Object System.Collections.Generic.List[string]
$out.Add("TOTAL_LINES=$n")

$starts = @(831,994,1175,1230,1509,1561,3375,3467,3691,3766,4268,4663,5434,5435,5449,5585,5769,5998,6051,6326,11352,11393,11443,11454,11485,11506,11553,11569,11605,11627,11666,11682,11709,11734,11876,11891,11918,11947,12039,12071,18307,18418)

foreach($s in $starts){
  # find the begin line index (1-based s)
  $idx = $s - 1
  $depth = 0
  $j = $idx
  while($j -lt $n){
    $t = ($lines[$j] -replace '(?<!\\)%.*$','').Trim()
    if($t -match '^\\begin\{itemize\}$'){ $depth++ }
    elseif($t -match '^\\end\{itemize\}$'){ $depth-- ; if($depth -eq 0){ break } }
    $j++
  }
  $a = [Math]::Max(0, $idx-3)
  $b = [Math]::Min($n-1, $j+2)
  $out.Add("")
  $out.Add("========== WRAPPER at L$s  (block L$($a+1)-L$($b+1)) ==========")
  for($k=$a; $k -le $b; $k++){
    $out.Add(("{0,6}: {1}" -f ($k+1), $lines[$k]))
  }
}
$outFile = Join-Path $root '_m8_wrappers_dump.txt'
[IO.File]::WriteAllLines($outFile, $out, (New-Object Text.UTF8Encoding($true)))
Write-Output "DUMPED=$($out.Count) lines to _m8_wrappers_dump.txt"
