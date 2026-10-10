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
Dump 5509 5651 'b1_zhonglei'
Dump 5652 5796 'b1_xuanze'
Dump 5797 5905 'b1_guanxi'
Dump 5906 6039 'b1_baoyang'
Dump 6475 6503 'b1_tshiqi'
Write-Output "DONE"
