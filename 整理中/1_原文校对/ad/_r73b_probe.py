import io, sys
sys.stdout.reconfigure(encoding="utf-8")
raw = io.open("book.tex", encoding="utf-8", newline="").read()
lines = raw.replace("\r\n", "\n").split("\n")
targets = ["男性生殖健康检查指南", "生殖健康检查", "定期自检"]
for i, l in enumerate(lines):
    for t in targets:
        if t in l and (l.startswith("\chapter") or l.startswith("\section") or l.startswith("\subsection")):
            print(i+1, "|", l.strip()[:90])
