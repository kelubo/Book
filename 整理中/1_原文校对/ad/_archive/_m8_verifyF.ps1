param([string]$file)
$ErrorActionPreference='Stop'
$root = $PSScriptRoot
$p = Join-Path $root $file
$b = [IO.File]::ReadAllBytes($p)
$hasBom = ($b.Length -ge 3 -and $b[0] -eq 0xEF -and $b[1] -eq 0xBB -and $b[2] -eq 0xBF)
$bl = 0; if($hasBom){ $bl = 3 }
Write-Output ("FILE=" + $file)
Write-Output ("SIZE=" + $b.Length)
Write-Output ("BOM=" + $b[0] + "," + $b[1] + "," + $b[2] + " hasBom=" + $hasBom)
$txt = [Text.Encoding]::UTF8.GetString($b, $bl, $b.Length - $bl)
Write-Output ("CRLF=" + ([regex]::Matches($txt,"\r\n")).Count)
Write-Output ("LF=" + ([regex]::Matches($txt,"`n")).Count)
Write-Output ("CR=" + ([regex]::Matches($txt,"`r")).Count)
$arr = [regex]::Split($txt, "\r?\n")
$n = $arr.Count
Write-Output ("LINES=" + $n)
$cl = New-Object string[] $n
for($i=0;$i -lt $n;$i++){ $cl[$i] = ($arr[$i] -replace '(?<!\\)%.*$','').Trim() }
$bi=0;$ei=0;$ben=0;$een=0
foreach($c in $cl){
  if($c -match '^\\begin\{itemize\}'){$bi++}
  elseif($c -match '^\\end\{itemize\}'){$ei++}
  elseif($c -eq '\begin{enumerate}'){$ben++}
  elseif($c -eq '\end{enumerate}'){$een++}
}
Write-Output ("itemize=" + $bi + "/" + $ei)
Write-Output ("enumerate=" + $ben + "/" + $een)
$stk = New-Object System.Collections.ArrayList
$bad=0
for($i=0;$i -lt $n;$i++){
  $c=$cl[$i]
  if($c -match '^\\begin\{itemize\}'){ [void]$stk.Add($i+1) }
  elseif($c -match '^\\end\{itemize\}'){ if($stk.Count -gt 0){ $stk.RemoveAt($stk.Count-1) } else { Write-Output ("UNMATCHED_END L"+($i+1)); $bad++ } }
}
foreach($s in $stk){ Write-Output ("UNMATCHED_BEGIN L$s"); $bad++ }
Write-Output ("balance_bad=" + $bad)
$wrapStarts = New-Object System.Collections.ArrayList
for($i=0;$i -lt $n;$i++){
  if($cl[$i] -match '^\\begin\{itemize\}'){
    $j=$i+1
    while($j -lt $n -and [string]::IsNullOrWhiteSpace($cl[$j])){ $j++ }
    if($j -lt $n -and ($cl[$j] -match '^\\begin\{itemize\}')){ [void]$wrapStarts.Add($i) }
  }
}
Write-Output ("adjacent_begin_wrappers=" + $wrapStarts.Count)
$out = @()
foreach($i in $wrapStarts){ $out += ("L"+($i+1)) }
Write-Output ($out -join ' ')
