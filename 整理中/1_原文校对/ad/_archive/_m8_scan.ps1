$ErrorActionPreference='Stop'
$p = Join-Path $PSScriptRoot '2_female.tex'
$raw = [Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes($p))
$lines = $raw -split "`r`n"
$n = $lines.Count

$owner = New-Object 'int[]' $n
$nodes = New-Object System.Collections.ArrayList
$stack = New-Object System.Collections.ArrayList

for ($i=0; $i -lt $n; $i++){
  $lc = $lines[$i] -replace '(?<!\\)%.*$',''
  $nb = ([regex]::Matches($lc,'\\begin\{itemize\}')).Count
  $ne = ([regex]::Matches($lc,'\\end\{itemize\}')).Count
  if ($nb -eq 1 -and $ne -eq 0){
     $parent = if($stack.Count -gt 0){ $stack[$stack.Count-1] } else { -1 }
     $id = $nodes.Add([pscustomobject]@{B=$i; E=-1; Parent=$parent; OwnItem=0; Stray=New-Object System.Collections.ArrayList})
     $owner[$i] = $id
     [void]$stack.Add($id)
  } elseif ($ne -eq 1 -and $nb -eq 0){
     $id = $stack[$stack.Count-1]
     [void]$stack.RemoveAt($stack.Count-1)
     $nodes[$id].E = $i
     $owner[$i] = $id
  } else {
     $owner[$i] = if($stack.Count -gt 0){ $stack[$stack.Count-1] } else { -1 }
  }
}

# classify direct content
for ($i=0; $i -lt $n; $i++){
  $o = $owner[$i]
  if ($o -lt 0){ continue }
  $node = $nodes[$o]
  if ($i -eq $node.B -or $i -eq $node.E){ continue }
  $lc = $lines[$i] -replace '(?<!\\)%.*$',''
  if ([string]::IsNullOrWhiteSpace($lc)){ continue }
  if ($lc -match '\\item'){ $nodes[$o].OwnItem++ }
  elseif ($lc -match '\\begin\{itemize\}' -or $lc -match '\\end\{itemize\}'){ }
  else { [void]$nodes[$o].Stray.Add(("{0}: {1}" -f ($i+1), $lines[$i])) }
}

$childCount = @{}
foreach($n2 in $nodes){ $childCount[$n2.B] = 0 }
foreach($n2 in $nodes){ if($n2.Parent -ge 0){ $childCount[$nodes[$n2.Parent].B]++ } }

$wrappers = @()
for ($k=0; $k -lt $nodes.Count; $k++){
  $nd = $nodes[$k]
  $cc = $childCount[$nd.B]
  if ($cc -ge 1 -and $nd.OwnItem -eq 0){
     $wrappers += [pscustomobject]@{K=$k; B=$nd.B+1; E=$nd.E+1; Children=$cc; Strays=$nd.Stray.Count; StrayList=$nd.Stray}
  }
}

Write-Output ("lines={0} nodes={1} wrappers={2}" -f $n, $nodes.Count, $wrappers.Count)
$withStray = $wrappers | Where-Object { $_.Strays -gt 0 }
Write-Output ("wrappers_with_stray={0}" -f $withStray.Count)
Write-Output "--- wrappers (line, children, strays) ---"
foreach($w in $wrappers){ Write-Output ("L{0}-{1} children={2} strays={3}" -f $w.B,$w.E,$w.Children,$w.Strays) }
Write-Output "--- stray samples (first 40) ---"
$c=0
foreach($w in $withStray){ foreach($s in $w.StrayList){ Write-Output ("  [wrap L{0}] {1}" -f $w.B,$s); $c++; if($c -ge 40){break} }; if($c -ge 40){break} }
