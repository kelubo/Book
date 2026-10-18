$ErrorActionPreference='Stop'
$dir='D:\Git\Book\整理中\1_原文校对\ad'
$F=[IO.File]::ReadAllLines("$dir\2_female.tex")
$stack=New-Object System.Collections.Generic.List[int]
for($i=0;$i -lt $F.Count;$i++){
  $s=[string]$F[$i]
  if($s -match '\\begin\{itemize\}'){ [void]$stack.Add($i) }
  elseif($s -match '\\end\{itemize\}'){ if($stack.Count -gt 0){ $stack.RemoveAt($stack.Count-1) } else { Write-Host ("STRAY END at line " + ($i+1)) } }
}
Write-Host ("UNCLOSED begins remaining=" + $stack.Count)
foreach($k in $stack){ Write-Host ("  unclosed begin at line " + ($k+1) + "  |" + ([string]$F[$k]).Trim() + "|") }
