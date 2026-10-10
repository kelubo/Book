$ErrorActionPreference='Stop'
$root = $PSScriptRoot
$femPath = Join-Path $root '2_female.tex'
$mergePath = Join-Path $root '_m8_merge_tshiqi.txt'
$logPath = Join-Path $root '_m8_fixF_log.txt'

$femTxt = [Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes($femPath))
$femArr = [regex]::Split($femTxt, "\r?\n")
$mergeTxt = [Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes($mergePath))
$mergeArr = [regex]::Split($mergeTxt, "\r?\n")
if($mergeArr.Count -gt 0 -and $mergeArr[-1] -eq ''){ $mergeArr = $mergeArr[0..($mergeArr.Count-2)] }

function L([int]$n){ return $femArr[$n-1] }

$bad = @()
function Chk([string]$name,[bool]$cond){ if(-not $cond){ $script:bad += $name } }

Chk 'L6475sss'  (L 6475).StartsWith('\subsubsection{')
Chk 'L6476blank' ((L 6476) -eq '')
Chk 'L6477beg'  ((L 6477) -eq '\begin{itemize}')
Chk 'L6502end'  ((L 6502) -eq '\end{itemize}')
Chk 'L6504sss'  (L 6504).StartsWith('\subsubsection{')
Chk 'L6513sss'  (L 6513).StartsWith('\subsubsection{')
Chk 'L6741end'  ((L 6741) -eq '\end{itemize}')
Chk 'L6742blank' ((L 6742) -eq '')
Chk 'L6743ss'   (L 6743).StartsWith('\subsection{')
Chk 'mergeFirst' ($mergeArr[0] -eq '\begin{itemize}')
Chk 'mergeLast'  ($mergeArr[-1] -eq '\end{itemize}')

$out = New-Object System.Collections.Generic.List[string]
$out.Add('BAD=' + ($bad -join ','))
$out.Add('totalLines=' + $femArr.Count)
$out.Add('mergeCount=' + $mergeArr.Count)
$out.Add('L6475=' + (L 6475))
$out.Add('L6476=[' + (L 6476) + ']')
$out.Add('L6477=' + (L 6477))
$out.Add('L6502=' + (L 6502))
$out.Add('L6504=' + (L 6504))
$out.Add('L6513=' + (L 6513))
$out.Add('L6741=' + (L 6741))
$out.Add('L6742=[' + (L 6742) + ']')
$out.Add('L6743=' + (L 6743))
if($bad.Count -gt 0){
  $out.Add('ABORT')
  [IO.File]::WriteAllBytes($logPath, (New-Object Text.UTF8Encoding($false)).GetBytes(($out -join "`r`n")))
  throw ('assert failed: ' + ($bad -join ','))
}

$lst = New-Object 'System.Collections.Generic.List[string]'
$lst.AddRange([string[]]$femArr)
# delete 1-based 6513..6741 (229 lines)
$lst.RemoveRange(6512, 6741-6513+1)
# replace 1-based 6477..6502 (26 lines) with merged block
$lst.RemoveRange(6476, 6502-6477+1)
$lst.InsertRange(6476, [string[]]$mergeArr)
$newArr = $lst.ToArray()
$outTxt = ($newArr -join "`r`n")
[IO.File]::Copy($femPath, (Join-Path $root '2_female.tex.bak_fixF'), $true)
$enc = New-Object Text.UTF8Encoding($false)
[IO.File]::WriteAllBytes($femPath, $enc.GetBytes($outTxt))
$out.Add('DONE removed=229 inserted=' + $mergeArr.Count + ' newLines=' + $newArr.Count)
[IO.File]::WriteAllBytes($logPath, $enc.GetBytes(($out -join "`r`n")))
Write-Output ('DONE bad=' + $bad.Count + ' newLines=' + $newArr.Count)
