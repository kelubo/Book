$ErrorActionPreference='Stop'
$dir='D:\Git\Book\整理中\1_原文校对\ad'
function StripC([string]$s){ $r='';$i=0;$n=$s.Length; while($i -lt $n){ $c=$s[$i]; if($c -eq '%'){ if($i -gt 0 -and $s[$i-1] -eq '\'){ $r+=$c;$i++;continue } else { break } } else { $r+=$c }; $i++ }; return $r }
function Check($file){
  $L=[IO.File]::ReadAllLines($file)
  $text=(($L | ForEach-Object { StripC([string]$_) }) -join "`n")
  $ob=([regex]::Matches($text,'\{')).Count
  $cb=([regex]::Matches($text,'\}')).Count
  Write-Host ("=== " + $file)
  Write-Host ("lines=" + $L.Count + "  braces {" + $ob + " }" + $cb + "  diff=" + ($ob-$cb))
  $envs=@{}
  foreach($m in [regex]::Matches($text,'\\begin\{([a-zA-Z\*]+)\}')){ $k=$m.Groups[1].Value; if(-not $envs.ContainsKey($k)){$envs[$k]=@(0,0)}; $envs[$k][0]++ }
  foreach($m in [regex]::Matches($text,'\\end\{([a-zA-Z\*]+)\}')){ $k=$m.Groups[1].Value; if(-not $envs.ContainsKey($k)){$envs[$k]=@(0,0)}; $envs[$k][1]++ }
  foreach($k in ($envs.Keys | Sort-Object)){ $v=$envs[$k]; $flag=''; if($v[0] -ne $v[1]){$flag='  <<< MISMATCH'}; Write-Host ("  env " + $k + " begin=" + $v[0] + " end=" + $v[1] + $flag) }
  $labels=@{}
  foreach($m in [regex]::Matches($text,'\\label\{([^}]*)\}')){ $k=$m.Groups[1].Value; if($labels.ContainsKey($k)){ $labels[$k]++ } else { $labels[$k]=1 } }
  $dup=$labels.Keys | Where-Object { $labels[$_] -gt 1 }
  if($dup){ foreach($d in $dup){ Write-Host ("  DUP label: " + $d + " x" + $labels[$d]) } } else { Write-Host "  labels unique OK (" + $labels.Count + ")" }
}
Check "$dir\2_female.tex"
Check "$dir\3_position.tex"
