$ErrorActionPreference='Stop'
$root = $PSScriptRoot
$femPath = Join-Path $root '2_female.tex'
$t = [Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes($femPath))
$arr = [regex]::Split($t, "\r?\n")
$sb = New-Object Text.StringBuilder
for($i=4844;$i -lt 7090;$i++){
  $l = $arr[$i]
  if($l -match '^\\(sub)?(sub)?section\{' -or $l -match '^\\chapter\{'){
    [void]$sb.AppendLine(("{0}: {1}" -f ($i+1), $l))
  }
}
[IO.File]::WriteAllText((Join-Path $root '_m8_breastmap.txt'), $sb.ToString(), (New-Object Text.UTF8Encoding($false)))
Write-Output "DONE"
