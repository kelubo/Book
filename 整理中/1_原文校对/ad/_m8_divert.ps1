$ErrorActionPreference='Stop'
$root = $PSScriptRoot
$logPath = Join-Path $root '_m8_divert_log.txt'

function Get-BomLen([string]$p){
  $b = [IO.File]::ReadAllBytes($p)
  if($b.Length -ge 3 -and $b[0] -eq 0xEF -and $b[1] -eq 0xBB -and $b[2] -eq 0xBF){ return 3 }
  return 0
}
function Read-Lines([string]$p){
  $b = [IO.File]::ReadAllBytes($p)
  $bl = Get-BomLen $p
  $txt = [Text.Encoding]::UTF8.GetString($b, $bl, $b.Length - $bl)
  return ,([regex]::Split($txt, "\r?\n"))
}
function Write-Lines([string]$p,[string[]]$arr,[bool]$withBom){
  $txt = ($arr -join "`r`n")
  if($withBom){
    $enc = New-Object Text.UTF8Encoding($true)
    $pre = $enc.GetPreamble()
    $body = $enc.GetBytes($txt)
    $all = New-Object byte[] ($pre.Length + $body.Length)
    [Array]::Copy($pre,0,$all,0,$pre.Length)
    [Array]::Copy($body,0,$all,$pre.Length,$body.Length)
    [IO.File]::WriteAllBytes($p,$all)
  } else {
    $enc = New-Object Text.UTF8Encoding($false)
    [IO.File]::WriteAllBytes($p, $enc.GetBytes($txt))
  }
}

$femPath = Join-Path $root '2_female.tex'
$malePath = Join-Path $root '1_male.tex'
$blockPath = Join-Path $root '_m8_male_block.txt'

$fem = Read-Lines $femPath
$mal = Read-Lines $malePath
$blk = Read-Lines $blockPath
if($blk.Count -gt 0 -and $blk[-1] -eq ''){ $blk = $blk[0..($blk.Count-2)] }

function Lf([int]$n){ return $fem[$n-1] }
function Lm([int]$n){ return $mal[$n-1] }

$bad = @()
function Chk([string]$n,[bool]$c){ if(-not $c){ $script:bad += $n } }

# --- female assertions ---
Chk 'f5873'  ((Lf 5873) -eq '  \end{itemize}')
Chk 'f5874'  ((Lf 5874).StartsWith('\item \textbf{'))
Chk 'f5875'  ((Lf 5875) -eq '  \begin{itemize}')
Chk 'f5898'  ((Lf 5898) -eq '  \end{itemize}')
Chk 'f5899'  ((Lf 5899).StartsWith('\item \textbf{'))
Chk 'f5905'  ((Lf 5905) -eq '\end{itemize}')
Chk 'f6507'  ((Lf 6507) -eq '')
Chk 'f6508'  ((Lf 6508).StartsWith('\subsubsection{'))
Chk 'f6510'  ((Lf 6510) -eq '\begin{itemize}')
Chk 'f6511'  ((Lf 6511).StartsWith('\item \textbf{'))
Chk 'f6515'  ((Lf 6515) -eq '\end{itemize}')
Chk 'f6516'  (-not (Lf 6516).StartsWith('\'))
# --- male assertions ---
Chk 'm558'   ((Lm 558) -eq '\end{itemize}')
Chk 'm560'   ((Lm 560).StartsWith('\begin{tcolorbox}'))
Chk 'm562'   ((Lm 562) -eq '\end{tcolorbox}')
Chk 'm563'   ((Lm 563) -eq '')
Chk 'm564'   ((Lm 564).StartsWith('\subsection{'))
$dynIdx = -1
for($i=0; $i -lt ($mal.Count-2); $i++){
  if($mal[$i] -eq '\end{tcolorbox}' -and $mal[$i+1] -eq '' -and $mal[$i+2].StartsWith('\subsection{')){ $dynIdx = $i+1; break }
}
Chk 'mDyn'   ($dynIdx -eq 562)
# --- block assertions ---
Chk 'blk0'   ($blk[0].StartsWith('\subsubsection{'))
Chk 'blkLast' ($blk[-1] -eq '\end{itemize}')

$out = New-Object System.Collections.Generic.List[string]
$out.Add('BAD=' + ($bad -join ','))
$out.Add('femTotal=' + $fem.Count + ' maleTotal=' + $mal.Count + ' blk=' + $blk.Count)
$out.Add('f5873=[' + (Lf 5873) + ']')
$out.Add('f5874=' + (Lf 5874))
$out.Add('f5898=[' + (Lf 5898) + ']')
$out.Add('f5899=' + (Lf 5899))
$out.Add('f6507=[' + (Lf 6507) + ']')
$out.Add('f6508=' + (Lf 6508))
$out.Add('f6515=[' + (Lf 6515) + ']')
$out.Add('f6516=' + (Lf 6516))
$out.Add('m561=' + (Lm 561) + ' m563=' + (Lm 563))
if($bad.Count -gt 0){
  $out.Add('ABORT')
  [IO.File]::WriteAllBytes($logPath, (New-Object Text.UTF8Encoding($false)).GetBytes(($out -join "`r`n")))
  throw ('assert failed: ' + ($bad -join ','))
}

# --- female edits: remove 6508..6515 (8), then 5874..5898 (25) ---
$lstF = New-Object 'System.Collections.Generic.List[string]'
$lstF.AddRange([string[]]$fem)
$lstF.RemoveRange(6507, 8)
$lstF.RemoveRange(5873, 25)
$femNew = $lstF.ToArray()

# --- male insert before 1-based 563 ---
$lstM = New-Object 'System.Collections.Generic.List[string]'
$lstM.AddRange([string[]]$mal)
$ins = New-Object 'System.Collections.Generic.List[string]'
$ins.AddRange([string[]]$blk)
$ins.Add('')
$lstM.InsertRange(563, [string[]]$ins.ToArray())
$malNew = $lstM.ToArray()

[IO.File]::Copy($femPath,  (Join-Path $root '2_female.tex.bak_divert'), $true)
[IO.File]::Copy($malePath, (Join-Path $root '1_male.tex.bak_divert'), $true)
Write-Lines $femPath  $femNew  $false
Write-Lines $malePath $malNew  $true

$out.Add('DONE femRemoved=' + (8+25) + ' femNew=' + $femNew.Count + ' maleInserted=' + $ins.Count + ' maleNew=' + $malNew.Count)
[IO.File]::WriteAllBytes($logPath, (New-Object Text.UTF8Encoding($false)).GetBytes(($out -join "`r`n")))
Write-Output ('DONE bad=' + $bad.Count + ' femNew=' + $femNew.Count + ' maleNew=' + $malNew.Count)
