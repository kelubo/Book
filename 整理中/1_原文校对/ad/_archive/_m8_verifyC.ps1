$ErrorActionPreference='Stop'
$root = $PSScriptRoot
$femPath = Join-Path $root '2_female.tex'
$b = [IO.File]::ReadAllBytes($femPath)
Write-Output ("SIZE=" + $b.Length)
Write-Output ("BOM=" + $b[0] + "," + $b[1] + "," + $b[2])
$txt = [Text.Encoding]::UTF8.GetString($b)
Write-Output ("CRLF=" + ([regex]::Matches($txt,"\r\n")).Count)
Write-Output ("LF=" + ([regex]::Matches($txt,"`n")).Count)
Write-Output ("CR=" + ([regex]::Matches($txt,"`r")).Count)
$arr = [regex]::Split($txt, "\r?\n")
Write-Output ("LINES=" + $arr.Count)
$bi=0;$ei=0;$ben=0;$een=0
foreach($l in $arr){
  $c = ($l -replace '(?<!\\)%.*$','').Trim()
  if($c -eq '\begin{itemize}'){$bi++}
  elseif($c -eq '\end{itemize}'){$ei++}
  elseif($c -eq '\begin{enumerate}'){$ben++}
  elseif($c -eq '\end{enumerate}'){$een++}
}
Write-Output ("itemize=" + $bi + "/" + $ei)
Write-Output ("enumerate=" + $ben + "/" + $een)
