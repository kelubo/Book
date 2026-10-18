$ErrorActionPreference='Stop'
$root = $PSScriptRoot
$fem = Join-Path $root '2_female.tex'
$bk  = Join-Path $root '0_book.tex.r81bak_20260924_102404'

$fl = [regex]::Split([Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes($fem)), "\r?\n")
$bl = [regex]::Split([Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes($bk)),  "\r?\n")
$fn = $fl.Count; $bn = $bl.Count

function Clean([string]$s){ return ($s -replace '(?<!\\)%.*$','').Trim() }
$fc = New-Object string[] $fn
for($i=0;$i -lt $fn;$i++){ $fc[$i] = Clean $fl[$i] }
$bc = New-Object string[] $bn
for($i=0;$i -lt $bn;$i++){ $bc[$i] = Clean $bl[$i] }

$bmap = @{}
for($i=0;$i -lt $bn;$i++){ $c=$bc[$i]; if($c -eq ''){continue}; if(-not $bmap.ContainsKey($c)){ $bmap[$c]=New-Object System.Collections.ArrayList }; [void]$bmap[$c].Add($i) }

# find wrappers in female
$wrapStarts = New-Object System.Collections.ArrayList
for($i=0;$i -lt $fn;$i++){
  if($fc[$i] -eq '\begin{itemize}'){
    $j=$i+1; while($j -lt $fn -and $fc[$j] -eq ''){$j++}
    if($j -lt $fn -and $fc[$j] -eq '\begin{itemize}'){ [void]$wrapStarts.Add($i) }
  }
}
function FemBlockEnd([int]$W){
  $d=0
  for($k=$W;$k -lt $fn;$k++){
    if($fc[$k] -eq '\begin{itemize}'){$d++}
    elseif($fc[$k] -eq '\end{itemize}'){$d--; if($d -eq 0){return $k}}
  }
  return -1
}
function BookBlockRange([int]$introFrom){
  # find first \begin{itemize} at/after introFrom
  $s=-1
  for($k=$introFrom;$k -lt $bn;$k++){ if($bc[$k] -eq '\begin{itemize}'){$s=$k;break}; if($bc[$k] -match '^\\(chapter|section|subsection|subsubsection|paragraph|subparagraph|part)\b'){return @(-1,-1)} }
  if($s -lt 0){return @(-1,-1)}
  $d=0
  for($k=$s;$k -lt $bn;$k++){
    if($bc[$k] -eq '\begin{itemize}'){$d++}
    elseif($bc[$k] -eq '\end{itemize}'){$d--; if($d -eq 0){return @($s,$k)}}
  }
  return @($s,-1)
}

$sb = New-Object Text.StringBuilder
foreach($W in $wrapStarts){
  $We = FemBlockEnd $W
  [void]$sb.AppendLine("=================== FEM WRAP L$($W+1) .. L$($We+1) ===================")
  # intro: previous non-blank female line before W
  $p=$W-1; while($p -ge 0 -and $fc[$p] -eq ''){$p--}
  $intro = if($p -ge 0){$fc[$p]} else {''}
  [void]$sb.AppendLine("INTRO: $intro")
  # locate in book
  $bs=-1;$be=-1
  if($intro -ne '' -and $bmap.ContainsKey($intro)){
    foreach($bi in $bmap[$intro]){
      $r = BookBlockRange $bi
      if($r[0] -ge 0 -and $r[1] -ge 0 -and ($r[1]-$r[0]) -ge ($We-$W-5)){ $bs=$r[0]; $be=$r[1]; break }
    }
  }
  if($bs -lt 0){ [void]$sb.AppendLine("  [BOOK REGION NOT FOUND]"); continue }
  [void]$sb.AppendLine("  BOOK RANGE L$($bs+1) .. L$($be+1)  (fem len=$($We-$W+1), book len=$($be-$bs+1))")
  # multiset of book block normalized (non-empty)
  $bset = @{}
  for($k=$bs;$k -le $be;$k++){ $c=$bc[$k]; if($c -eq ''){continue}; if(-not $bset.ContainsKey($c)){$bset[$c]=0}; $bset[$c]++ }
  $fset = @{}
  for($k=$W;$k -le $We;$k++){ $c=$fc[$k]; if($c -eq ''){continue}; if(-not $fset.ContainsKey($c)){$fset[$c]=0}; $fset[$c]++ }
  # book-only lines (candidates to restore)
  [void]$sb.AppendLine("  -- BOOK-ONLY lines (absent in fem):")
  for($k=$bs;$k -le $be;$k++){
    $c=$bc[$k]; if($c -eq ''){continue}
    $has = $fset.ContainsKey($c)
    if(-not $has){ [void]$sb.AppendLine("     B$($k+1): $c") }
    elseif($fset[$c] -lt $bset[$c]){ if(-not $script:_seen){$script:_seen=@{}}; [void]$sb.AppendLine("     B$($k+1) (dup x$($bset[$c]) vs x$($fset[$c])): $c") }
  }
  # fem-only lines (extra in fem, would be lost on replace)
  [void]$sb.AppendLine("  -- FEM-ONLY lines (absent in book):")
  for($k=$W;$k -le $We;$k++){
    $c=$fc[$k]; if($c -eq ''){continue}
    if(-not $bset.ContainsKey($c)){ [void]$sb.AppendLine("     F$($k+1): $c") }
    elseif($fset[$c] -gt $bset[$c]){ [void]$sb.AppendLine("     F$($k+1) (dup x$($fset[$c]) vs x$($bset[$c])): $c") }
  }
  $script:_seen=$null
}
$outp = Join-Path $root '_m8_blockdiff.txt'
[IO.File]::WriteAllText($outp, $sb.ToString(), (New-Object Text.UTF8Encoding($false)))
Write-Output "DONE -> $outp"
