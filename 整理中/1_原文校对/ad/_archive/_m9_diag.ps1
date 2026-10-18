$ErrorActionPreference='Stop'
$dir='D:\Git\Book\整理中\1_原文校对\ad'
$F=[IO.File]::ReadAllLines("$dir\2_female.tex")
function Idx($arr,$pat,$start){ for($i=$start;$i -lt $arr.Count;$i++){ if(([string]$arr[$i]) -match $pat){ return $i } }; throw ("NOT FOUND: "+$pat) }
function Cnt($arr,$a0,$b0){ $b=0;$e=0; for($i=$a0;$i -le $b0;$i++){ $s=[string]$arr[$i]; if($s -match '\\begin\{itemize\}'){$b++}; if($s -match '\\end\{itemize\}'){$e++} }; return ($b.ToString()+"/"+$e.ToString()) }
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
Write-Host ("WHOLE FILE 1..end        " + (Cnt $F 0 ($F.Count-1)))
Write-Host ("prefix 1..1861           " + (Cnt $F 0 ($iSecNei-1)))
Write-Host ("A_vag 1868..1920         " + (Cnt $F ($iYin+1) ($iSpill-1)))
Write-Host ("B_vag 3083..3097         " + (Cnt $F ($iH110+1) ($iG-1)))
Write-Host ("C_vag 4410..4655         " + (Cnt $F ($iVagC+1) ($iBrast-1)))
Write-Host ("B_G 3099..3141           " + (Cnt $F ($iG+1) ($iGongB-1)))
Write-Host ("A_G 2700..2708           " + (Cnt $F $iGA ($iUterA-1)))
Write-Host ("A_cervix 2679..2699      " + (Cnt $F $iCervixA ($iGA-1)))
Write-Host ("B_uter 3143..3153        " + (Cnt $F ($iGongB+1) ($iOvaB-1)))
Write-Host ("A_uter 2709..2818        " + (Cnt $F $iUterA ($iTubA-1)))
Write-Host ("C_uter 3825..4408        " + (Cnt $F ($iUterC+1) ($iVagC-1)))
Write-Host ("B_tub 3167..3178         " + (Cnt $F ($iTubB+1) ($iOvaC-1)))
Write-Host ("A_tub 2819..2889         " + (Cnt $F $iTubA ($iOvaA-1)))
Write-Host ("C_tub 3509..3823         " + (Cnt $F ($iTubC+1) ($iUterC-1)))
Write-Host ("B_ova 3155..3165         " + (Cnt $F ($iOvaB+1) ($iTubB-1)))
Write-Host ("A_ova 2890..3048         " + (Cnt $F $iOvaA ($iHorA-1)))
Write-Host ("C_ova 3180..3507         " + (Cnt $F ($iOvaC+1) ($iTubC-1)))
Write-Host ("A_hor 3049..3080         " + (Cnt $F $iHorA ($iNote-1)))
Write-Host ("brast..end 4656..end     " + (Cnt $F $iBrast ($F.Count-1)))
Write-Host ("SPILL 1921..2678         " + (Cnt $F $iSpill ($iMoved)))
Write-Host ("ruj 2357..2676           " + (Cnt $F $iRujSpill ($iMoved-1)))
Write-Host ("kou body 1924..2356      " + (Cnt $F ($iSpill+3) ($iRujSpill-1)))
