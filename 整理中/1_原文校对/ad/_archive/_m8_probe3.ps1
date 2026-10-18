$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
$file = Join-Path $root '2_female.tex'
$bytes = [IO.File]::ReadAllBytes($file)
$txt = [Text.Encoding]::UTF8.GetString($bytes)
$lines = @([regex]::Split($txt, "\r?\n"))
$out = @()
$out += "totalElts=$($lines.Count)"
$ranges = @(@(785, 795), @(1725, 1740), @(2015, 2050))
foreach ($r in $ranges) {
  $s = $r[0]; $e = $r[1]
  $out += "--- range $s..$e ---"
  for ($i = $s - 1; $i -le $e - 1; $i++) {
    $c = $lines[$i]
    if ($c.Length -gt 70) { $c = $c.Substring(0, 70) + '...' }
    $out += ("{0}: {1}" -f ($i + 1), $c)
  }
}
[IO.File]::WriteAllText((Join-Path $root '_m8_probe3_log.txt'), ($out -join "`r`n"), (New-Object Text.UTF8Encoding($false)))
Write-Output ($out -join "`r`n")
