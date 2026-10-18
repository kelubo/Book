import io, sys
sys.stdout.reconfigure(encoding="utf-8")
raw = io.open("book.tex", encoding="utf-8", newline="").read()
lines = raw.replace("\r\n", "\n").split("\n")
# 列出所有 chapter 标题，取 52000-58364 之间
for i, l in enumerate(lines):
    s = l.rstrip()
    if s.startswith("\chapter") or s.startswith("\part"):
        if 49000 < i+1:
            print(i+1, "|", s[:80])
