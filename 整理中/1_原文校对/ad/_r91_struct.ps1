$ErrorActionPreference='Stop'
$out=New-Object System.Collections.Generic.List[string]
$files=@{ '0_book.tex'='_r91_struct_0book.txt'; '1_male.tex'='_r91_struct_1male.txt'; '2_female.tex'='_r91_struct_2female.txt'; '3_position.tex'='_r91_struct_3position.txt' }
$secRe=[regex]'(?<!\\)\\(part|chapter|section|subsection|subsubsection)\*?(?:\[[^\]]*\])?\{([^}]*)\}'
foreach($f in $files.Keys){
  $L=[IO.File]::ReadAllLines(".\" + $f)
  $list=New-Object System.Collections.Generic.List[string]
  $byTitle=@{}
  for($i=0;$i -lt $L.Count;$i++){
    $m=$secRe.Match([string]$L[$i])
    if($m.Success){
      $kind=$m.Groups[1].Value; $title=$m.Groups[2].Value
      [void]$list.Add(($i+1).ToString().PadLeft(7) + "  " + $kind.PadRight(13) + "  " + $title)
      if($kind -eq 'section' -or $kind -eq 'subsection' -or $kind -eq 'chapter'){
        $key=$kind + "||" + $title
        if(-not $byTitle.ContainsKey($key)){ $byTitle[$key]=New-Object System.Collections.Generic.List[int] }
        [void]$byTitle[$key].Add($i+1)
      }
    }
  }
  [void]$out.Add("######## " + $f + "  (" + $L.Count + " lines) ########")
  [void]$out.Add("---- DUPLICATES ----")
  foreach($k in ($byTitle.Keys | Sort-Object)){
    if($byTitle[$k].Count -gt 1){
      [void]$out.Add("DUP  " + $k.Replace('||','  ') + "   @lines: " + ($byTitle[$k] -join ","))
    }
  }
  [void]$out.Add("")
  [void]$out.Add("---- FULL STRUCTURE ----")
  foreach($s in $list){ [void]$out.Add($s) }
  [void]$out.Add("")
  [IO.File]::WriteAllLines((".\" + $files[$f]), $out, (New-Object Text.UTF8Encoding($false)))
  Write-Host ("wrote " + $files[$f] + "  (" + $list.Count + " headings, " + $out.Count + " lines)")
  $out.Clear()
}
Write-Host "DONE"
