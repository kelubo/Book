$ErrorActionPreference = 'Stop'
$dir = 'D:\Git\Book\整理中\1_原文校对\ad'
$utf8 = [System.Text.UTF8Encoding]::new($false)

# 1) 2_female: replace everything before \documentclass with a compact header
$f = Join-Path $dir '2_female.tex'
$t = [System.IO.File]::ReadAllText($f, [System.Text.Encoding]::UTF8)
$header = @'
% ════════════════════════════════════════════════════════════════════════
%                              女 性 卷
% ════════════════════════════════════════════════════════════════════════
% 本文件定位：女性专属内容（解剖、妇科疾病、生育、保健、中医妇科）
% 两性共通内容见 0_book.tex，男性专属内容见 1_male.tex
% 使用 xelatex 编译

'@
$t = [regex]::Replace($t, '\A[\s\S]+?(?=\\documentclass)', $header)

# 2) 2_female: delete the 使用说明 banner block (migration completed)
$t = [regex]::Replace($t, "(?m)^% ═+\r?\n% +女性卷目录结构[\s\S]+?再删除本说明。\r?\n% ═+\r?\n\r?\n?", '')
[System.IO.File]::WriteAllText($f, $t, $utf8)

# 3) remove migration-log comment lines in all three volumes (keep 分工 notes)
$pat = '^\s*%.*(移入|⇒|⇐|来源[：:])'
foreach ($name in @('1_male.tex','2_female.tex','3_position.tex')) {
  $fp = Join-Path $dir $name
  $lines = [System.IO.File]::ReadAllLines($fp, [System.Text.Encoding]::UTF8)
  $kept = $lines | Where-Object { ($_ -notmatch $pat) -or ($_ -match '分工') }
  $removed = $lines.Count - $kept.Count
  [System.IO.File]::WriteAllLines($fp, $kept, $utf8)
  Write-Output "$name removed=$removed"
}
