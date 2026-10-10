$ErrorActionPreference='Stop'
$root = $PSScriptRoot
$femPath = Join-Path $root '2_female.tex'
$femTxt = [Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes($femPath))
$femArr = [regex]::Split($femTxt, "\r?\n")
$bkPath  = Join-Path $root '0_book.tex.r81bak_20260924_102404'
$bkTxt  = [Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes($bkPath))
$bkArr  = [regex]::Split($bkTxt, "\r?\n")

Write-Output "######## FEMALE 11418-11460 ########"
for($k=11417; $k -le 11459; $k++){ Write-Output ("[" + ($k+1) + "] " + $femArr[$k]) }
Write-Output "######## BOOK 41388-41490 ########"
for($k=41387; $k -le 41489; $k++){ Write-Output ("[" + ($k+1) + "] " + $bkArr[$k]) }
