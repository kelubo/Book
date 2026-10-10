import io, sys
sys.stdout.reconfigure(encoding="utf-8")
raw = io.open("book.tex", encoding="utf-8", newline="").read()
lines = raw.replace("\r\n", "\n").split("\n")
for i in range(57118, 57315):
    s = lines[i].rstrip()
    if s.startswith("\section") or s.startswith("\subsection") or s.startswith("\subsubsection"):
        print(i+1, "|", s[:85])
