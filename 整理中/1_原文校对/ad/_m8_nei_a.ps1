$ErrorActionPreference='Stop'
$root = $PSScriptRoot
$out = New-Object Text.StringBuilder
function Dump($path,$tag,$from,$to){
  $txt = [Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes($path))
  $arr = [regex]::Split($txt, "\r?\n")
  [void]$out.AppendLine("######## $tag $from..$to ########")
  for($i=$from-1; $i -le $to-1 -and $i -lt $arr.Count; $i++){ [void]$out.AppendLine("[" + ($i+1) + "] " + $arr[$i]) }
}
$femPath = Join-Path $root '2_female.tex'
$bkPath  = Join-Path $root '0_book.tex.r81bak_20260924_102404'
Dump $femPath 'FEM' 5500 5600
Dump $bkPath 'BOOK' 30868 31030
[IO.File]::WriteAllText((Join-Path $root '_m8_nei_a.txt'), $out.ToString(), (New-Object Text.UTF8Encoding($false)))
Write-Output "WROTE A"
