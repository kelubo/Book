$ErrorActionPreference='Stop'
function StripC([string]$s){ $r='';$i=0;$n=$s.Length; while($i -lt $n){ $c=$s[$i]; if($c -eq '%'){ if($i -gt 0 -and $s[$i-1] -eq '\'){ $r+=$c;$i++;continue } else { break } } else { $r+=$c }; $i++ }; return $r }

$f='.\0_book.tex'
$L=[IO.File]::ReadAllLines($f)
$N=$L.Count
$hre=[regex]'(?<!\\)\\(part|chapter|section|subsection|subsubsection|subparagraph)\*?(?:\[[^\]]*\])?\{([^}]*)\}'
$rank=@{'part'=1;'chapter'=2;'section'=3;'subsection'=4;'subsubsection'=5;'subparagraph'=6}
$SEP=[string[]]@('||')

$hs=New-Object System.Collections.ArrayList
for($i=0;$i -lt $N;$i++){
  $m=$hre.Match($L[$i])
  if($m.Success){
    $o=New-Object psobject
    $o|Add-Member NoteProperty Line $i
    $o|Add-Member NoteProperty Kind ([string]$m.Groups[1].Value)
    $o|Add-Member NoteProperty Title ([string]$m.Groups[2].Value)
    $o|Add-Member NoteProperty End $N
    [void]$hs.Add($o)
  }
}
for($k=0;$k -lt $hs.Count;$k++){
  $r=$rank[$hs[$k].Kind]
  for($j=$k+1;$j -lt $hs.Count;$j++){
    if($rank[$hs[$j].Kind] -le $r){ $hs[$k].End=$hs[$j].Line; break }
  }
}

function BodySet($h){
  $set=New-Object 'System.Collections.Generic.HashSet[string]'
  for($x=[int]$h.Line+1;$x -lt [int]$h.End;$x++){
    $t=StripC([string]$L[$x]).Trim()
    if($t.Length -lt 4){continue}
    [void]$set.Add($t)
  }
  return ,$set
}

$groups=@{}
foreach($h in $hs){
  $key=$h.Kind + "||" + $h.Title
  if(-not $groups.ContainsKey($key)){ $groups[$key]=New-Object System.Collections.ArrayList }
  [void]$groups[$key].Add($h)
}

$out=New-Object System.Collections.ArrayList
foreach($key in ($groups.Keys | Sort-Object)){
  $arr=@($groups[$key])
  $cnt=[int]$arr.Count
  if($cnt -lt 2){continue}
  $parts=$key.Split($SEP, [System.StringSplitOptions]::None)
  [void]$out.Add("==== DUP " + $parts[0] + " | " + $parts[1] + "   x" + $cnt)
  $sets=@()
  foreach($h in $arr){ $sets+=,(BodySet $h) }
  for($ia=0;$ia -lt $cnt;$ia++){
    for($ib=$ia+1;$ib -lt $cnt;$ib++){
      $setA=$sets[$ia]; $setB=$sets[$ib]
      $inter=0
      foreach($v in $setA){ if($setB.Contains($v)){$inter++} }
      $union=[int]$setA.Count + [int]$setB.Count - $inter
      $jc=0.0
      if($union -gt 0){ $jc=[math]::Round($inter/$union,3) }
      $la=$arr[$ia].Line; $lb=$arr[$ib].Line
      [void]$out.Add(("  J={0,-5}  L{1}(sz{2}) <-> L{3}(sz{4})  inter={5}" -f $jc,$la,$setA.Count,$lb,$setB.Count,$inter))
    }
  }
}

$of='.\_r92_sim_0book.txt'
$enc=New-Object System.Text.UTF8Encoding($false)
[IO.File]::WriteAllLines((Join-Path (Get-Location) $of), $out, $enc)
Write-Output "DONE groups=$($groups.Count) lines=$N out=$($out.Count)"
