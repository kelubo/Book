$ErrorActionPreference='Stop'
$root = $PSScriptRoot
$femPath = Join-Path $root '2_female.tex'
$bkPath  = Join-Path $root '0_book.tex.r81bak_20260924_102404'
$femTxt = [Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes($femPath))
$bkTxt  = [Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes($bkPath))
$femArr = [regex]::Split($femTxt, "\r?\n")
$bkArr  = [regex]::Split($bkTxt, "\r?\n")

$sb = New-Object Text.StringBuilder
[void]$sb.AppendLine("=== FEM lines=$($femArr.Count) ===")
[void]$sb.AppendLine("=== BOOK lines=$($bkArr.Count) ===")
[void]$sb.AppendLine("=== FEM 5500..5600 (file line = idx+1) ===")
for($i=5499;$i -le 5599 -and $i -lt $femArr.Count;$i++){ [void]$sb.AppendLine(("{0}: {1}" -f ($i+1), $femArr[$i])) }
[void]$sb.AppendLine("=== BOOK 30875..31025 ===")
for($i=30874;$i -le 31024 -and $i -lt $bkArr.Count;$i++){ [void]$sb.AppendLine(("{0}: {1}" -f ($i+1), $bkArr[$i])) }
[IO.File]::WriteAllText((Join-Path $root '_m8_dumpD.txt'), $sb.ToString(), (New-Object Text.UTF8Encoding($false)))
Write-Output "WROTE _m8_dumpD.txt"
