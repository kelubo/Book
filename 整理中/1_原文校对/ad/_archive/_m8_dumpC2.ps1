$ErrorActionPreference='Stop'
$root = $PSScriptRoot
$femPath = Join-Path $root '2_female.tex'
$femTxt = [Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes($femPath))
$femArr = [regex]::Split($femTxt, "\r?\n")
Write-Output "######## FEM 12605-12665 ########"
for($k=12604; $k -le 12664; $k++){ Write-Output ("[" + ($k+1) + "] " + $femArr[$k]) }
Write-Output "######## FEM 12845-12900 ########"
for($k=12844; $k -le 12899; $k++){ Write-Output ("[" + ($k+1) + "] " + $femArr[$k]) }
