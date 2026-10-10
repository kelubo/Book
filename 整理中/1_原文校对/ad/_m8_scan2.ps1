$ErrorActionPreference='Stop'
$p = Join-Path $PSScriptRoot '2_female.tex'
$lines = [Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes($p)) -split "`r`n"
$n = $lines.Count
$cl = New-Object string[] $n
for($i=0;$i -lt $n;$i++){ $cl[$i] = ($lines[$i] -replace '(?<!\\)%.*$','').Trim() }
function IsBegin([string]$s){ return ($s -match '^\\begin\{itemize\}') }
function IsEnd([string]$s){ return ($s -match '^\\end\{itemize\}') }
$wrapStarts = New-Object System.Collections.ArrayList
for($i=0;$i -lt $n;$i++){
  if(IsBegin $cl[$i]){
    $j=$i+1
    while($j -lt $n -and [string]::IsNullOrWhiteSpace($cl[$j])){ $j++ }
    if($j -lt $n -and (IsBegin $cl[$j])){ [void]$wrapStarts.Add($i) }
  }
}
Write-Output ("adjacent_begin_wrappers={0}" -f $wrapStarts.Count)
$out = @()
foreach($i in $wrapStarts){ $out += ("L"+($i+1)) }
Write-Output ($out -join ' ')
