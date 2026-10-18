$ErrorActionPreference='Stop'
$root = $PSScriptRoot
$femPath = Join-Path $root '2_female.tex'
$bkPath  = Join-Path $root '0_book.tex.r81bak_20260924_102404'

$femTxt = [Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes($femPath))
$bkTxt  = [Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes($bkPath))
$femArr = [regex]::Split($femTxt, "\r?\n")
$bkArr  = [regex]::Split($bkTxt, "\r?\n")
function Clean([string]$s){ return ($s -replace '(?<!\\)%.*$','').Trim() }

# (femBodyStart, femBodyEnd, bookBodyStart, bookBodyEnd) 1-based inclusive
$map = @(
 @(5653,5793,31024,31167),
 @(5904,6032,31280,31412),
 @(6119,6459,31505,31853),
 @(6461,6483,31855,31882)
)

$lst = New-Object 'System.Collections.Generic.List[string]'
$lst.AddRange([string[]]$femArr)

$log = New-Object Text.StringBuilder
$done=0; $skip=0
for($m=$map.Count-1;$m -ge 0;$m--){
  $fs=$map[$m][0]; $fe=$map[$m][1]; $bs=$map[$m][2]; $be=$map[$m][3]
  # boundaries: header must be at fs-1 and fe+1
  if(-not ($femArr[$fs-2] -match '^\\(sub)?subsection\{')){ [void]$log.AppendLine("SKIP F$fs : fem head not subsubsection"); $skip++; continue }
  if(-not ($femArr[$fe]   -match '^\\(sub)?subsection\{')){ [void]$log.AppendLine("SKIP F$fs : fem tail next not subsubsection"); $skip++; continue }
  if(-not ($bkArr[$bs-2] -match '^\\(sub)?subsection\{')){ [void]$log.AppendLine("SKIP B$bs : book head not subsubsection"); $skip++; continue }
  if(-not ($bkArr[$be]   -match '^\\(sub)?subsection\{')){ [void]$log.AppendLine("SKIP B$bs : book tail next not subsubsection"); $skip++; continue }

  # subsequence check
  $fa=New-Object System.Collections.ArrayList
  for($k=$fs-1;$k -le $fe-1;$k++){ $c=Clean $femArr[$k]; if($c -ne ''){ [void]$fa.Add($c) } }
  $ba=New-Object System.Collections.ArrayList
  for($k=$bs-1;$k -le $be-1;$k++){ $c=Clean $bkArr[$k]; if($c -ne ''){ [void]$ba.Add($c) } }
  $bp=0;$ok=$true
  for($i=0;$i -lt $fa.Count;$i++){
    $found=$false
    while($bp -lt $ba.Count){ if($ba[$bp] -eq $fa[$i]){ $bp++; $found=$true; break } else { $bp++ } }
    if(-not $found){ $ok=$false; break }
  }
  if(-not $ok){ [void]$log.AppendLine("SKIP F$fs : not ordered-subsequence"); $skip++; continue }

  $cnt=$fe-$fs+1
  [void]$log.AppendLine("FEMHEAD : " + $femArr[$fs-2])
  [void]$log.AppendLine("BOOKHEAD: " + $bkArr[$bs-2])
  $lst.RemoveRange($fs-1,$cnt)
  $ins=[string[]]$bkArr[($bs-1)..($be-1)]
  $lst.InsertRange($fs-1,$ins)
  [void]$log.AppendLine("OK F$fs..$fe ($cnt) <- B$bs..$be ($($be-$bs+1)) gain=$((($be-$bs+1)-$cnt))")
  $done++
}

$outTxt = ($lst.ToArray() -join "`r`n")
$enc = New-Object Text.UTF8Encoding($false)
[IO.File]::Copy($femPath, (Join-Path $root '2_female.tex.bak_fixE'), $true)
[IO.File]::WriteAllBytes($femPath, $enc.GetBytes($outTxt))
[IO.File]::WriteAllText((Join-Path $root '_m8_fixE_log.txt'), $log.ToString(), (New-Object Text.UTF8Encoding($false)))
Write-Output "DONE=$done SKIP=$skip"
