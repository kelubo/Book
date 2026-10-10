$ErrorActionPreference='Stop'
$root = $PSScriptRoot
$femPath = Join-Path $root '2_female.tex'
$bkPath  = Join-Path $root '0_book.tex.r81bak_20260924_102404'
$femArr = [regex]::Split([Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes($femPath)), "\r?\n")
$bkArr  = [regex]::Split([Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes($bkPath)), "\r?\n")
function Clean([string]$s){ return ($s -replace '(?<!\\)%.*$','').Trim() }

function GetSubs([string[]]$arr,[int]$from,[int]$to){
  $res = New-Object System.Collections.ArrayList
  $cur = $null
  for($i=$from-1;$i -lt $to -and $i -lt $arr.Count;$i++){
    $c = Clean $arr[$i]
    if($c -match '^\\(sub)?subsection\{' ){
      if($cur){ $cur[2] = $i+1; [void]$res.Add($cur) }
      $cur = @($c, ($i+1), $arr.Count)
    }
  }
  if($cur){ $cur[2] = [Math]::Min($to,$arr.Count); [void]$res.Add($cur) }
  return $res
}

$femSubs = GetSubs $femArr 5400 6700
$bkSubs  = GetSubs $bkArr 30800 32000

# normalize subsubsection name
function Name([string]$s){
  if($s -match '^\\subsubsection\{(.*)\}'){ return $Matches[1] }
  return $null
}

$sb = New-Object Text.StringBuilder
[void]$sb.AppendLine("=== FEM subsubsections 5400..6700 ===")
foreach($s in $femSubs){ [void]$sb.AppendLine(("{0}: {1}  [body {2}..{3}]" -f $s[1], $s[0], ($s[1]+1), $s[2])) }
[void]$sb.AppendLine("=== BOOK subsubsections 30800..32000 ===")
foreach($s in $bkSubs){ [void]$sb.AppendLine(("{0}: {1}  [body {2}..{3}]" -f $s[1], $s[0], ($s[1]+1), $s[2])) }

# For each FEM subsubsection with a name matching a BOOK subsubsection, run subsequence test
[void]$sb.AppendLine("=== SUBSEQUENCE TEST (fem body vs book body) ===")
foreach($fs in $femSubs){
  $fn = Name $fs[0]; if(-not $fn){ continue }
  $bs = $null
  foreach($b in $bkSubs){ if((Name $b[0]) -eq $fn){ $bs = $b; break } }
  if(-not $bs){ [void]$sb.AppendLine("NO-BOOK-MATCH : $fn"); continue }
  $fa = New-Object System.Collections.ArrayList
  for($i=$fs[1];$i -le $fs[2]-2;$i++){ $c=Clean $femArr[$i]; if($c -ne ''){ [void]$fa.Add($c) } }
  $ba = New-Object System.Collections.ArrayList
  for($i=$bs[1];$i -le $bs[2]-2;$i++){ $c=Clean $bkArr[$i]; if($c -ne ''){ [void]$ba.Add($c) } }
  # subsequence
  $bp=0;$ok=$true;$missing=""
  for($i=0;$i -lt $fa.Count;$i++){
    $found=$false
    while($bp -lt $ba.Count){ if($ba[$bp] -eq $fa[$i]){ $bp++; $found=$true; break } else { $bp++ } }
    if(-not $found){ $ok=$false; if($missing -eq ""){ $missing=" first missing: "+$fa[$i] }; break }
  }
  [void]$sb.AppendLine(("FEM[{0}..{1}] len={2}  BOOK[{3}..{4}] len={5}  SUBSEQ={6}{7}" -f $fs[1],$fs[2],$fa.Count,$bs[1],$bs[2],$ba.Count,$ok,$missing))
}
[IO.File]::WriteAllText((Join-Path $root '_m8_subdiag.txt'), $sb.ToString(), (New-Object Text.UTF8Encoding($false)))
Write-Output "WROTE"
