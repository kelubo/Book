$ErrorActionPreference='Stop'
$root = $PSScriptRoot
$p = Join-Path $root '2_female.tex'
$bytes = [IO.File]::ReadAllBytes($p)
$text  = [Text.Encoding]::UTF8.GetString($bytes)
$lines = $text -split "`r`n"
$cnt = 0
for($i=0; $i -lt $lines.Count; $i++){
  if($lines[$i] -match '^ubparagraph\{'){
    $lines[$i] = $lines[$i] -replace '^ubparagraph\{','\subparagraph{'
    $cnt++
  } elseif($lines[$i] -match '^aragraph\{'){
    $lines[$i] = $lines[$i] -replace '^aragraph\{','\paragraph{'
    $cnt++
  }
}
$out = ($lines -join "`r`n")
$enc = New-Object Text.UTF8Encoding($false)
[IO.File]::WriteAllBytes($p, $enc.GetBytes($out))
Write-Output "FIXED=$cnt"
