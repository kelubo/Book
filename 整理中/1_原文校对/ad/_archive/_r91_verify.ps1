$ErrorActionPreference='Stop'
function StripC([string]$s){ $r='';$i=0;$n=$s.Length; while($i -lt $n){ $c=$s[$i]; if($c -eq '%'){ if($i -gt 0 -and $s[$i-1] -eq '\'){ $r+=$c;$i++;continue } else { break } } else { $r+=$c }; $i++ }; return $r }
$files=@('.\0_book.tex','.\1_male.tex','.\2_female.tex','.\3_position.tex')
foreach($f in $files){
  if(-not (Test-Path $f)){ Write-Host ("=== " + $f + "  MISSING"); continue }
  $L=[IO.File]::ReadAllLines($f)
  $text=(($L | ForEach-Object { StripC([string]$_) }) -join "`n")
  $ob=([regex]::Matches($text,'\{')).Count
  $cb=([regex]::Matches($text,'\}')).Count
  Write-Host ("=== " + $f + "  lines=" + $L.Count + "  braces {" + $ob + " }" + $cb + "  diff=" + ($ob-$cb))
  $envs=@{}
  foreach($m in [regex]::Matches($text,'\\begin\{([a-zA-Z\*]+)\}')){ $k=$m.Groups[1].Value; if(-not $envs.ContainsKey($k)){$envs[$k]=@(0,0)}; $envs[$k][0]++ }
  foreach($m in [regex]::Matches($text,'\\end\{([a-zA-Z\*]+)\}')){ $k=$m.Groups[1].Value; if(-not $envs.ContainsKey($k)){$envs[$k]=@(0,0)}; $envs[$k][1]++ }
  $bad=@()
  foreach($k in ($envs.Keys | Sort-Object)){ $v=$envs[$k]; if($v[0] -ne $v[1]){ $bad += ($k + "(" + $v[0] + "/" + $v[1] + ")") } }
  if($bad.Count -gt 0){ Write-Host ("  ENV MISMATCH: " + ($bad -join ", ")) } else { Write-Host "  envs paired OK" }
  $labels=@{}
  foreach($m in [regex]::Matches($text,'\\label\{([^}]*)\}')){ $k=$m.Groups[1].Value; if($labels.ContainsKey($k)){ $labels[$k]++ } else { $labels[$k]=1 } }
  $dup=@($labels.Keys | Where-Object { $labels[$_] -gt 1 })
  if($dup.Count -gt 0){ Write-Host ("  DUP labels: " + (($dup | ForEach-Object { $_ + "x" + $labels[$_] }) -join ", ")) } else { Write-Host ("  labels unique OK (" + $labels.Count + ")") }
  $np=([regex]::Matches($text,'\\part(?:\[[^\]]*\])?\{')).Count
  $nc=([regex]::Matches($text,'\\chapter(?:\[[^\]]*\])?\{')).Count
  $ns=([regex]::Matches($text,'\\section(?:\[[^\]]*\])?\{')).Count
  $nss=([regex]::Matches($text,'\\subsection(?:\[[^\]]*\])?\{')).Count
  Write-Host ("  parts=" + $np + " chapters=" + $nc + " sections=" + $ns + " subsections=" + $nss)
}
Write-Host "DONE"
