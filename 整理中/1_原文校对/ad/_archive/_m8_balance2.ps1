$ErrorActionPreference='Stop'
$root = $PSScriptRoot
function Balance([string]$path,[string]$tag){
  $txt = [Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes($path))
  $arr = [regex]::Split($txt, "\r?\n")
  $stack = New-Object System.Collections.Generic.List[int]
  $unmatchedEnd = New-Object System.Collections.Generic.List[int]
  $bi=0; $ei=0
  for($i=0;$i -lt $arr.Count;$i++){
    $c = ($arr[$i] -replace '(?<!\\)%.*$','').Trim()
    if($c -match '^\\begin\{itemize\}'){ $bi++; [void]$stack.Add(($i+1)) }
    elseif($c -eq '\end{itemize}'){ $ei++; if($stack.Count -gt 0){ $stack.RemoveAt($stack.Count-1) } else { [void]$unmatchedEnd.Add(($i+1)) } }
  }
  $ub = @(); foreach($s in $stack){ $ub += $s }
  Write-Output "[$tag] begins=$bi ends=$ei"
  Write-Output ("[$tag] unmatched BEGIN lines: " + ($ub -join ', '))
  Write-Output ("[$tag] unmatched END   lines: " + ($unmatchedEnd -join ', '))
}
Balance (Join-Path $root '2_female.tex') 'FEM'
Balance (Join-Path $root '0_book.tex.r81bak_20260924_102404') 'BOOK'
