param()
$ErrorActionPreference = 'Stop'
$path = 'd:\Git\Book\整理中\1_原文校对\ad\2_female.tex'
$bytes = [IO.File]::ReadAllBytes($path)
$t = [Text.Encoding]::UTF8.GetString($bytes)
$lines = $t -split "`r`n"
Write-Output ("BEFORE_LINES=" + $lines.Count)

# 1-based inclusive ranges to delete
$ranges = @(
  @(1808,1920),
  @(1938,2072),
  @(2110,2117)
)

function Assert-True($c,$m){ if(-not $c){ throw ('ASSERT-FAIL: ' + $m) } }
# boundary assertions (0-based indices)
Assert-True ($lines[1807] -match '^\\subsection\{') ('r1 start: ' + $lines[1807])
Assert-True ($lines[1919] -match '^\\end\{itemize\}$') ('r1 end: ' + $lines[1919])
Assert-True ($lines[1921] -match '^\\subsection\{') ('keep1: ' + $lines[1921])
Assert-True ($lines[1935] -match '^\\end\{tcolorbox\}$') ('r2 prev: ' + $lines[1935])
Assert-True ($lines[1936] -eq '') ('r2 gap blank: [' + $lines[1936] + ']')
Assert-True ($lines[1937] -match '^\\subsection\{') ('r2 start: ' + $lines[1937])
Assert-True ($lines[2071] -eq '') ('r2 end blank: [' + $lines[2071] + ']')
Assert-True ($lines[2072] -match '^\\subsection\{') ('keep2: ' + $lines[2072])
Assert-True ($lines[2107] -match '^\\noindent') ('editor note: ' + $lines[2107])
Assert-True ($lines[2108] -eq '') ('gap3 blank: [' + $lines[2108] + ']')
Assert-True ($lines[2116] -eq '') ('r3 end blank: [' + $lines[2116] + ']')
Assert-True ($lines[2117] -match '^\\section\{') ('keep3: ' + $lines[2117])

$del = New-Object System.Collections.Generic.HashSet[int]
$total = 0
foreach($r in $ranges){
  for($i=$r[0]; $i -le $r[1]; $i++){ [void]$del.Add($i-1); $total++ }
}
Write-Output ("DELETE_COUNT=" + $total)

$kept = New-Object System.Collections.Generic.List[string]
for($i=0; $i -lt $lines.Count; $i++){
  if(-not $del.Contains($i)){ [void]$kept.Add($lines[$i]) }
}
$out = ($kept.ToArray() -join "`r`n")
$enc = New-Object System.Text.UTF8Encoding($false)
[IO.File]::WriteAllText($path, $out, $enc)
Write-Output ("AFTER_LINES=" + $kept.Count)
Write-Output ('EXPECTED=' + ($lines.Count - $total))
