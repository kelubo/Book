# -*- coding: utf-8 -*-
"""r79b: 把「体位基础」章移到第四篇（性交体位与姿势）篇首。dry-run / apply"""
import io, os, re, sys, shutil, time

DIR = os.path.dirname(os.path.abspath(__file__))
MODE = sys.argv[1] if len(sys.argv) > 1 else "dry-run"
P = os.path.join(DIR, "3_position.tex")
TITLE = re.compile(r"^\\(part|chapter|section|subsection|subsubsection)\*?\{")
LVL = {"part": 0, "chapter": 1, "section": 2, "subsection": 3, "subsubsection": 4}

raw = io.open(P, encoding="utf-8", newline="").read()
assert "\r" not in raw
lines = raw.split("\n")

i = [k for k, ln in enumerate(lines) if ln == "\\chapter{体位基础}"]
assert len(i) == 1, i
i = i[0]
e = len(lines)
for j in range(i + 1, len(lines)):
    m = TITLE.match(lines[j])
    if m and LVL[m.group(1)] <= 1:
        e = j
        break
blk = lines[i:e]
lines2 = lines[:i] + lines[e:]
k = [k for k, ln in enumerate(lines2) if ln == "\\part{性交体位与姿势}"]
assert len(k) == 1
k = k[0]
out = lines2[:k + 1] + blk + lines2[k + 1:]

# 校验：正文行 multiset 不变
def body(ls):
    import collections
    c = collections.Counter()
    for ln in ls:
        s = ln.strip()
        if s and not s.startswith("%") and not TITLE.match(ln):
            c[ln] += 1
    return c
assert body(out) == body(lines), "正文行变化!"

if MODE == "apply":
    st = time.strftime("%Y%m%d_%H%M%S")
    shutil.copy2(P, P + ".r79bbak_" + st)
    io.open(P, "w", encoding="utf-8", newline="\n").write("\n".join(out))
    print("已写盘（备份 .r79bbak_%s）" % st)
else:
    print("[dry-run] 体位基础块 %d 行将从 L%d 移至第四篇篇首" % (len(blk), i + 1))
