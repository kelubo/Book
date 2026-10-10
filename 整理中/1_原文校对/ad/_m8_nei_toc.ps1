$ErrorActionPreference='Stop'
$root = $PSScriptRoot
$out = New-Object Text.StringBuilder
function DumpToc($path,$tag,$from,$to){
  $txt = [Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes($path))
  $arr = [regex]::Split($txt, "\r?\n")
  [void]$out.AppendLine("######## $tag structure (lines $from..$to) ########")
  for($i=$from-1; $i -le $to-1 -and $i -lt $arr.Count; $i++){
    $c = ($arr[$i] -replace '(?<!\\)%.*$','').Trim()
    if($c -match '^\\(section|subsection|subsubsection|subsubsubsection)\{'){ [void]$out.AppendLine("[" + ($i+1) + "] " + $arr[$i].Trim()) }
  }
}
$femPath = Join-Path $root '2_female.tex'
$bkPath  = Join-Path $root '0_book.tex.r81bak_20260924_102404'
DumpToc $femPath 'FEM' 5400 6700
DumpToc $bkPath 'BOOK' 30500 31500
[IO.File]::WriteAllText((Join-Path $root '_m8_nei_toc.txt'), $out.ToString(), (New-Object Text.UTF8Encoding($false)))
Write-Output "WROTE"
