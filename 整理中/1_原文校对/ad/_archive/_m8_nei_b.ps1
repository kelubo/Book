$ErrorActionPreference='Stop'
$root = $PSScriptRoot
$out = New-Object Text.StringBuilder
$bkPath  = Join-Path $root '0_book.tex.r81bak_20260924_102404'
$bkTxt = [Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes($bkPath))
$bkArr = [regex]::Split($bkTxt, "\r?\n")
[void]$out.AppendLine("######## BOOK structure (lines 31400..32200) ########")
for($i=31399; $i -le 32199 -and $i -lt $bkArr.Count; $i++){
  $c = ($bkArr[$i] -replace '(?<!\\)%.*$','').Trim()
  if($c -match '^\\(section|subsection|subsubsection|subsubsubsection)\{'){ [void]$out.AppendLine("[" + ($i+1) + "] " + $bkArr[$i].Trim()) }
}
$femPath = Join-Path $root '2_female.tex'
$femTxt = [Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes($femPath))
$femArr = [regex]::Split($femTxt, "\r?\n")
[void]$out.AppendLine("######## FEM 6430..6675 ########")
for($i=6429; $i -le 6674 -and $i -lt $femArr.Count; $i++){ [void]$out.AppendLine("[" + ($i+1) + "] " + $femArr[$i]) }
[IO.File]::WriteAllText((Join-Path $root '_m8_nei_b.txt'), $out.ToString(), (New-Object Text.UTF8Encoding($false)))
Write-Output "WROTE B"
