$ErrorActionPreference='Stop'
$root = $PSScriptRoot
$femPath = Join-Path $root '2_female.tex'
$femTxt = [Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes($femPath))
$femArr = [regex]::Split($femTxt, "\r?\n")
$W = @(11428,11469,11519,11664,11787,12025,12232)
foreach($w in $W){
  Write-Output ("=== F$w  (idx " + ($w-1) + ") ===")
  for($k=$w-1; $k -le $w+1; $k++){ Write-Output ("  [" + ($k+1) + "] " + $femArr[$k]) }
}
$bkPath  = Join-Path $root '0_book.tex.r81bak_20260924_102404'
$bkTxt  = [Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes($bkPath))
$bkArr  = [regex]::Split($bkTxt, "\r?\n")
$BW = @(41393,41440,41495,41649,41774,42020,42229)
foreach($w in $BW){
  Write-Output ("=== B$w ===")
  Write-Output ("  [" + $w + "] " + $bkArr[$w-1])
}
