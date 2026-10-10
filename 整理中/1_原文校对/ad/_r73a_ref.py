import io, sys
sys.stdout.reconfigure(encoding="utf-8")
raw = io.open("book.tex", encoding="utf-8", newline="").read()
lines = raw.replace("\r\n", "\n").split("\n")
print("total lines:", len(lines))
print("CRLF:", raw.count("\r\n"), "LF:", raw.count("\n"))
targets = ["求助渠道", "网络求助", "网络信息", "线上问诊", "信息鉴别", "甄别"]
for i, l in enumerate(lines):
    for t in targets:
        if t in l:
            print(i+1, "|", l.strip()[:100])
