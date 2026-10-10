$ErrorActionPreference='Stop'
$root = $PSScriptRoot
$p = Join-Path $root '1_male.tex'
$b = [IO.File]::ReadAllBytes($p)
$bl = 0
if($b[0] -eq 0xEF -and $b[1] -eq 0xBB -and $b[2] -eq 0xBF){ $bl = 3 }
$t = [Text.Encoding]::UTF8.GetString($b, $bl, $b.Length - $bl)
$a = [regex]::Split($t, "\r?\n")
$o = New-Object System.Collections.Generic.List[string]
$o.Add('COUNT=' + $a.Count)
for($i=0; $i -lt 3; $i++){ $o.Add('L' + ($i+1) + '=[' + $a[$i] + ']') }
for($i=554; $i -lt 570; $i++){ $o.Add('L' + ($i+1) + '=[' + $a[$i] + ']') }
$o.Add('--- tcolorbox+subsection pattern matches ---')
for($i=0; $i -lt ($a.Count-2); $i++){
  if($a[$i] -eq '\end{tcolorbox}' -and $a[$i+1] -eq '' -and $a[$i+2].StartsWith('\subsection{')){
    $o.Add('IDX=' + ($i+1) + ' next=' + $a[$i+2])
  }
}
[IO.File]::WriteAllBytes((Join-Path $root '_m8_male_probe.txt'), (New-Object Text.UTF8Encoding($false)).GetBytes(($o -join "`r`n")))
Write-Output 'OK'
