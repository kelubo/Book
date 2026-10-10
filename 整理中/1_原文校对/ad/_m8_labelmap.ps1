$ErrorActionPreference='Stop'
$root = $PSScriptRoot
$fem = Join-Path $root '2_female.tex'
$bk  = Join-Path $root '0_book.tex.r81bak_20260924_102404'

$fl = [regex]::Split([Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes($fem)), "\r?\n")
$bl = [regex]::Split([Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes($bk)),  "\r?\n")
$fn = $fl.Count

function Clean([string]$s){ return ($s -replace '(?<!\\)%.*$','').Trim() }

# per-line cleaned content of female
$fc = New-Object string[] $fn
for($i=0;$i -lt $fn;$i++){ $fc[$i] = Clean $fl[$i] }

# index book: content(normalized) -> list of 1-based line numbers
$bmap = @{}
for($i=0;$i -lt $bl.Count;$i++){
  $c = Clean $bl[$i]
  if($c -eq ''){ continue }
  if(-not $bmap.ContainsKey($c)){ $bmap[$c] = New-Object System.Collections.ArrayList }
  [void]$bmap[$c].Add($i)   # 0-based index into $bl
}

# find wrappers
$wrapStarts = New-Object System.Collections.ArrayList
for($i=0;$i -lt $fn;$i++){
  if($fc[$i] -match '^\\begin\{itemize\}$'){
    $j=$i+1
    while($j -lt $fn -and $fc[$j] -eq ''){ $j++ }
    if($j -lt $fn -and $fc[$j] -match '^\\begin\{itemize\}$'){ [void]$wrapStarts.Add($i) }
  }
}

$sb = New-Object Text.StringBuilder
[void]$sb.AppendLine("WRAPPERS=$($wrapStarts.Count)")
foreach($W in $wrapStarts){
  # scan forward from W, depth tracking; record direct-child inner itemize starts
  $depth = 0
  $inners = New-Object System.Collections.ArrayList
  for($k=$W; $k -lt $fn; $k++){
    $c = $fc[$k]
    if($c -match '^\\begin\{itemize\}$'){
      if($depth -eq 1){ [void]$inners.Add($k) }
      $depth++
    } elseif($c -match '^\\end\{itemize\}$'){
      $depth--
      if($depth -eq 0){ break }
    }
  }
  [void]$sb.AppendLine("--WRAP L$($W+1)  inner=$($inners.Count)")
  foreach($I in $inners){
    # first \item after inner begin
    $t = $I+1; $anchor=$null
    while($t -lt $fn){ if($fc[$t] -match '^\\item\b'){ $anchor=$fc[$t]; break }; if($fc[$t] -match '^\\end\{itemize\}$'){break}; $t++ }
    if($null -eq $anchor){ [void]$sb.AppendLine("    inner L$($I+1): NO_ITEM"); continue }
    $labels = @()
    if($bmap.ContainsKey($anchor)){
      foreach($bi in $bmap[$anchor]){
        # walk up: skip blanks, expect \begin{itemize}, then label
        $u = $bi-1
        while($u -ge 0 -and (Clean $bl[$u]) -eq ''){ $u-- }
        if($u -ge 0 -and (Clean $bl[$u]) -match '^\\begin\{itemize\}$'){
          $v = $u-1
          while($v -ge 0 -and (Clean $bl[$v]) -eq ''){ $v-- }
          if($v -ge 0){ $labels += ("$($v+1):" + (Clean $bl[$v])) }
        }
      }
    }
    $lab = if($labels.Count -eq 0){ 'NOLABEL' } else { ($labels -join ' | ') }
    [void]$sb.AppendLine("    inner L$($I+1): [$lab]  <= " + $anchor.Substring(0,[Math]::Min(40,$anchor.Length)))
  }
}
$outp = Join-Path $root '_m8_labelmap.txt'
[IO.File]::WriteAllText($outp, $sb.ToString(), (New-Object Text.UTF8Encoding($false)))
Write-Output "DONE -> $outp"
