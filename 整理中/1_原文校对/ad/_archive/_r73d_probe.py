import io, sys
sys.stdout.reconfigure(encoding="utf-8")
raw = io.open("book.tex", encoding="utf-8", newline="").read()
lines = raw.replace("\r\n", "\n").split("\n")
# 列出 57589-58096 之间的所有标题
for i in range(57588, 58097):
    s = lines[i].rstrip()
    if s.startswith("\chapter") or s.startswith("\section") or s.startswith("\subsection"):
        print(i+1, "|", s[:85])
