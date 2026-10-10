import io, sys
sys.stdout.reconfigure(encoding="utf-8")
raw = io.open("book.tex", encoding="utf-8", newline="").read()
lines = raw.replace("\r\n", "\n").split("\n")
rng = [(57000, 57600), (56000, 56610)]
for a,b in rng:
    for i in range(a, min(b, len(lines))):
        s = lines[i].rstrip()
        if s.startswith("\chapter") or s.startswith("\section"):
            print(i+1, "|", s[:85])
    print("---")
