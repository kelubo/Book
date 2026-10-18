$ErrorActionPreference='Stop'
$root = $PSScriptRoot
$femPath = Join-Path $root '2_female.tex'
$t = [Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes($femPath))
$arr = [regex]::Split($t, "\r?\n")

function Dump($from,$to,$tag){
  $sb = New-Object Text.StringBuilder
  for($i=$from-1;$i -le $to-1 -and $i -lt $arr.Count;$i++){
    [void]$sb.AppendLine(("{0}: {1}" -f ($i+1), $arr[$i]))
  }
  [IO.File]::WriteAllText((Join-Path $root ("_m8_b2_" + $tag + ".txt")), $sb.ToString(), (New-Object Text.UTF8Encoding($false)))
}

Dump 6504 6745 'batch2'
Dump 6743 6800 'breast'
Write-Output "DUMP_DONE"
