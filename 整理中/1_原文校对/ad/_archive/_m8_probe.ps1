$ErrorActionPreference='Stop'
$root = $PSScriptRoot
$log = Join-Path $root '_m8_probe_male.txt'
$out = New-Object System.Collections.Generic.List[string]
foreach($f in @('1_male.tex','2_female.tex','0_book.tex')){
  $p = Join-Path $root $f
  if(-not (Test-Path $p)){ $out.Add($f + ' MISSING'); continue }
  $b = [IO.File]::ReadAllBytes($p)
  $bom = ($b[0].ToString()+','+$b[1].ToString()+','+$b[2].ToString())
  $t = [Text.Encoding]::UTF8.GetString($b)
  $crlf = ([regex]::Matches($t,"\r\n")).Count
  $lf = ([regex]::Matches($t,"\n")).Count
  $cr = ([regex]::Matches($t,"\r")).Count
  $lines = ([regex]::Split($t,"\r?\n")).Count
  $out.Add($f + ' size=' + $b.Length + ' bom=' + $bom + ' crlf=' + $crlf + ' lf=' + $lf + ' cr=' + $cr + ' lines=' + $lines)
}
[IO.File]::WriteAllBytes($log, (New-Object Text.UTF8Encoding($false)).GetBytes(($out -join "`r`n")))
Write-Output 'OK'
