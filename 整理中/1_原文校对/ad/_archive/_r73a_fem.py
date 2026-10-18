import io, sys
sys.stdout.reconfigure(encoding="utf-8")
f = "female.tex"
raw = io.open(f, encoding="utf-8", newline="").read()
lines = raw.replace("\r\n", "\n").split("\n")
print("total", len(lines))
keys = ["生理","解剖","阴蒂","子宫","卵巢","阴道","盆底","功能","反应","感觉","解剖学"]
for i, l in enumerate(lines):
    s = l.strip()
    if not (s.startswith("\\section") or s.startswith("\\subsection") or s.startswith("\\subsubsection")):
        continue
    # print all headings from 6960 onward
    if i + 1 > 6960:
        print(i + 1, s[:70])
