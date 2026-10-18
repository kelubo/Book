$ErrorActionPreference='Stop'
$root = $PSScriptRoot
$femPath = Join-Path $root '2_female.tex'
$femTxt = [Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes($femPath))
$femArr = [regex]::Split($femTxt, "\r?\n")
Write-Output "######## TOC of structure (fem 5400-6700) ########"
for($i=5399; $i -le 6699; $i++){
  $c = ($femArr[$i] -replace '(?<!\\)%.*$','').Trim()
  if($c -match '^\\(section|subsection|subsubsection|subsubsubsection)\{'){ Write-Output ("[" + ($i+1) + "] " + $femArr[$i]) }
}
Write-Output "######## WRAPPERS (context) ########"
function Clean([string]$s){ return ($s -replace '(?<!\\)%.*$','').Trim() }
function FindEnd([string[]]$arr,[int]$W){ $d=0; for($k=$W;$k -lt $arr.Count;$k++){ $c=Clean $arr[$k]; if($c -eq '\begin{itemize}'){$d++} elseif($c -eq '\end{itemize}'){$d--; if($d -eq 0){return $k}} }; return -1 }
foreach($w in @(5510,5511,5525,5661,5845,6074,6127,6402)){
  $W=$w-1; $We=FindEnd $femArr $W
  Write-Output ("=== wrapper F$w  end=" + ($We+1) + " ===")
  $s = [Math]::Max(0,$W-4); $e = [Math]::Min($femArr.Count-1, $We+2)
  for($k=$s;$k -le $e;$k++){ Write-Output ("[" + ($k+1) + "] " + $femArr[$k]) }
}
