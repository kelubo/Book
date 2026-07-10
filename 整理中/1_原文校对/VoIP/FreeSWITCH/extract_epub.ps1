$epubPath = "D:\Git\Book\整理中\1_原文校对\VoIP\FreeSWITCH\FreeSWITCH权威指南 (杜金房 张令考著) (Z-Library).epub"
$destPath = "D:\Git\Book\整理中\1_原文校对\VoIP\FreeSWITCH\epub_content"

if(!(Test-Path $destPath)) {
    New-Item -ItemType Directory -Path $destPath | Out-Null
}

Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::ExtractToDirectory($epubPath, $destPath)