$ErrorActionPreference='Stop'
$dir='D:\Git\Book\整理中\1_原文校对\ad'

# ---------- load ----------
$F=[IO.File]::ReadAllLines("$dir\2_female.tex")   # CRLF file, logical line numbers
$P=[IO.File]::ReadAllLines("$dir\3_position.tex") # LF file

# ---------- helpers ----------
function Idx($arr,$pat,$start){
  for($i=$start;$i -lt $arr.Count;$i++){ if(([string]$arr[$i]) -match $pat){ return $i } }
  throw ("NOT FOUND: " + $pat + " from " + $start)
}
function AddR($t,$arr,$a0,$b0){ for($i=$a0;$i -le $b0;$i++){ [void]$t.Add([string]$arr[$i]) } }
function AddL($t,[string]$s){ [void]$t.Add($s) }
function AddT($t,$arr,$a0,$b0){
  $s=$a0;$e=$b0
  while($s -le $e -and ([string]$arr[$s]).Trim() -eq ''){$s++}
  while($e -ge $s -and ([string]$arr[$e]).Trim() -eq ''){$e--}
  for($i=$s;$i -le $e;$i++){ [void]$t.Add([string]$arr[$i]) }
}
function A($idx,$line,$tag){ if(($idx+1) -ne $line){ throw ("ANCHOR FAIL " + $tag + ": got line " + ($idx+1) + " expected " + $line) } }
function StripC([string]$s){
  $r=''; $i=0; $n=$s.Length
  while($i -lt $n){
    $c=$s[$i]
    if($c -eq '%'){ if($i -gt 0 -and $s[$i-1] -eq '\'){ $r+=$c; $i++; continue } else { break } }
    else { $r+=$c }
    $i++
  }
  return $r
}
function ItemBal($lines,$tag){
  $b=0;$e=0
  foreach($l in $lines){ $s=StripC([string]$l); if($s -match '\\begin\{itemize\}'){$b++}; if($s -match '\\end\{itemize\}'){$e++} }
  if($b -ne $e){ throw ($tag + " itemize unbalanced: begin=" + $b + " end=" + $e) }
  Write-Host ($tag + " itemize OK (" + $b + "/" + $e + ")")
}

# ---------- locate anchors in 2_female.tex ----------
$iSecNei  = Idx $F '^\s*\\section\{内生殖器\}' 0
$iYin     = Idx $F '^\s*\\subsection\{阴道\}\s*$' $iSecNei
$iSpill   = Idx $F '口交相关卫生与技巧' $iYin
$iCervixA = Idx $F '子宫的颈部就是子宫颈' 0
$iGA      = Idx $F '格雷芬伯格' $iCervixA
$iUterA   = Idx $F '^\s*\\subparagraph\{解剖结构\}' $iGA
$iTubA    = Idx $F '^\s*\\subparagraph\{解剖结构\}' ($iUterA+1)
$iOvaA    = Idx $F '^\s*\\subparagraph\{解剖结构\}' ($iTubA+1)
$iHorA    = Idx $F '性激素是一种化学物质' 0
$iNote    = Idx $F '^\s*%\s*注（r80）' 0
$iH110    = Idx $F '^\s*\\subsection\{阴道的结构与功能\}' 0
$iG       = Idx $F '^\s*\\subsection\{G点与前壁敏感区\}' 0
$iGongB   = Idx $F '^\s*\\subsection\{子宫的结构与周期\}' 0
$iOvaB    = Idx $F '^\s*\\subsection\{卵巢的排卵与激素\}' 0
$iTubB    = Idx $F '^\s*\\subsection\{输卵管\}' 0
$iOvaC    = Idx $F '^\s*\\subsubsection\{卵巢\}' 0
$iTubC    = Idx $F '^\s*\\subsubsection\{输卵管\}' 0
$iUterC   = Idx $F '^\s*\\subsubsection\{子宫\}' 0
$iVagC    = Idx $F '^\s*\\subsubsection\{阴道\}' 0
$iBrast   = Idx $F '^\s*\\section\{乳房\}' 0
$iRujSpill= Idx $F '^\s*\\textbf\{二十、乳交技巧与体验\}' 0
$iMoved   = Idx $F '已移出.*阴交技巧与体验' 0

A $iSecNei  1862 'secNei'
A $iYin     1866 'yin'
A $iSpill   1921 'spill'
A $iCervixA 2679 'cervixA'
A $iGA      2700 'GA'
A $iUterA   2709 'uterA'
A $iTubA    2819 'tubA'
A $iOvaA    2890 'ovaA'
A $iHorA    3049 'horA'
A $iNote    3081 'note'
A $iH110    3082 'h110'
A $iG       3098 'G'
A $iGongB   3142 'gongB'
A $iOvaB    3154 'ovaB'
A $iTubB    3166 'tubB'
A $iOvaC    3179 'ovaC'
A $iTubC    3508 'tubC'
A $iUterC   3824 'uterC'
A $iVagC    4409 'vagC'
A $iBrast   4656 'brast'
A $iRujSpill 2357 'rujSpill'
A $iMoved   2677 'moved'
Write-Host 'FEMALE ANCHORS OK'

# ---------- locate anchors in 3_position.tex ----------
$iPRuj  = Idx $P '^\s*\\section\{乳交\}' 0
$iPSugu = Idx $P '^\s*\\section\{素股' 0
A $iPRuj  2700 'pRuj'
A $iPSugu 2730 'pSugu'
Write-Host 'POSITION ANCHORS OK'

# ---------- build new female ----------
$new=New-Object System.Collections.Generic.List[string]
AddR $new $F 0 ($iSecNei-1)                 # 1..1861 prefix
AddL $new '\section{内生殖器}'
AddL $new '% 移入："内生殖器"整节（原始内容区，按标题搜索）'
AddL $new ''
AddL $new ''
AddL $new '\subsection{阴道}'
AddL $new ''
AddT $new $F ($iYin+1) ($iSpill-1)          # A 阴道解剖
AddL $new '\end{itemize}'
AddL $new ''
AddT $new $F ($iH110+1) ($iG-1)             # B 阴道
AddL $new ''
AddT $new $F ($iVagC+1) ($iBrast-1)         # C 阴道
AddL $new ''
AddL $new '\subsection{G点与前壁敏感区}'
AddL $new ''
AddT $new $F ($iG+1) ($iGongB-1)            # B G点
AddL $new ''
AddT $new $F $iGA ($iUterA-1)               # A G点
AddL $new ''
AddL $new '\subsection{子宫颈}'
AddL $new ''
AddT $new $F $iCervixA ($iGA-1)             # A 子宫颈
AddL $new ''
AddL $new '\subsection{子宫}'
AddL $new ''
AddT $new $F ($iGongB+1) ($iOvaB-1)         # B 子宫
AddL $new ''
AddT $new $F $iUterA ($iTubA-1)             # A 子宫
AddL $new ''
AddT $new $F ($iUterC+1) ($iVagC-1)         # C 子宫
AddL $new ''
AddL $new '\subsection{输卵管}'
AddL $new ''
AddT $new $F ($iTubB+1) ($iOvaC-1)          # B 输卵管
AddL $new ''
AddT $new $F $iTubA ($iOvaA-1)              # A 输卵管
AddL $new ''
AddT $new $F ($iTubC+1) ($iUterC-1)         # C 输卵管
AddL $new ''
AddL $new '\subsection{卵巢}'
AddL $new ''
AddT $new $F ($iOvaB+1) ($iTubB-1)          # B 卵巢
AddL $new ''
AddT $new $F $iOvaA ($iHorA-1)              # A 卵巢
AddL $new ''
AddT $new $F ($iOvaC+1) ($iTubC-1)          # C 卵巢
AddL $new ''
AddL $new '\section{女性性激素}'
AddL $new ''
AddT $new $F $iHorA ($iNote-1)              # A 性激素
AddL $new ''
AddR $new $F $iBrast ($F.Count-1)           # 乳房及之后

ItemBal $new 'FEMALE'

# ---------- build new position ----------
$pos=New-Object System.Collections.Generic.List[string]
AddR $pos $P 0 ($iPRuj-1)                   # 1..2699
AddL $pos ''
AddL $pos '% --- 由 2_female.tex《内生殖器》误置区迁入：口交详解（详细版） ---'
AddL $pos '\section{口交技巧详解（详细版）}'
AddL $pos ''
$intro=[string]$F[$iSpill]
$intro=$intro -replace '^\s*\\item\s*',''
AddL $pos $intro
AddL $pos ''
AddT $pos $F ($iSpill+3) ($iRujSpill-1)     # 口交详解正文
AddL $pos ''
AddR $pos $P $iPRuj ($iPSugu-1)             # 2700..2729
AddL $pos '% --- 由 2_female.tex《内生殖器》误置区迁入：乳交详解（详细版） ---'
AddL $pos '\section{乳交技巧详解（详细版）}'
AddL $pos ''
AddT $pos $F $iRujSpill ($iMoved-1)         # 乳交详解正文
AddL $pos ''
AddR $pos $P $iPSugu ($P.Count-1)           # 2730..end

ItemBal $pos 'POSITION'

# ---------- write ----------
$enc=New-Object Text.UTF8Encoding($false)
[IO.File]::WriteAllText("$dir\2_female.tex", ($new -join "`r`n"), $enc)
Write-Host ("FEMALE written lines=" + $new.Count)
[IO.File]::WriteAllText("$dir\3_position.tex", ($pos -join "`n"), $enc)
Write-Host ("POSITION written lines=" + $pos.Count)
Write-Host 'DONE'
