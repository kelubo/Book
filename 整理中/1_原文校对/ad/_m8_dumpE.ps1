$ErrorActionPreference='Stop'
$root = $PSScriptRoot
$femPath = Join-Path $root '2_female.tex'
$bkPath  = Join-Path $root '0_book.tex.r81bak_20260924_102404'
$femArr = [regex]::Split([Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes($femPath)), "\r?\n")
$bkArr  = [regex]::Split([Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes($bkPath)), "\r?\n")
$sb = New-Object Text.StringBuilder
function Dump([string]$name,[string[]]$arr,[int]$a,[int]$b){
  [void]$sb.AppendLine("===== $name $a..$b =====")
  for($i=$a-1;$i -le $b-1 -and $i -lt $arr.Count;$i++){ [void]$sb.AppendLine(("{0}: {1}" -f ($i+1), $arr[$i])) }
}
Dump "FEM-A-xuanze" $femArr 5715 5765
Dump "FEM-B-baoyang" $femArr 5898 5998
Dump "FEM-C-siwang" $femArr 6120 6210
Dump "FEM-D-teshu" $femArr 6452 6495
Dump "BOOK-A-xuanze" $bkArr 31023 31070
Dump "BOOK-B-baoyang" $bkArr 31279 31330
Dump "BOOK-D-teshu" $bkArr 31854 31882
[IO.File]::WriteAllText((Join-Path $root '_m8_dumpE.txt'), $sb.ToString(), (New-Object Text.UTF8Encoding($false)))
Write-Output "WROTE"
