# -*- coding: utf-8 -*-
"""r81: 旧区各段 -> 骨架章 归属与覆盖度分析"""
import io, re, collections

BASE = "D:/Git/Book/整理中/1_原文校对/ad/"
HEAD = re.compile(r"^\\(part|chapter|section|subsection|subsubsection)\*?\{([^}]*)\}")
ENV = re.compile(r"^\\(begin|end)\{")


def load(fn):
    return [x.rstrip("\r") for x in io.open(BASE + fn, encoding="utf-8").read().split("\n")]


def pnorm(s):
    return re.sub(r"\s+", "", s.strip())


book = load("0_book.tex"); male = load("1_male.tex")
fem = load("2_female.tex"); pos = load("3_position.tex")

O = next(i for i, x in enumerate(book) if re.match(r"^\\part\{old\}", x))
mm = next(i for i, x in enumerate(book) if re.match(r"^\\mainmatter", x))
mdc = [i for i, x in enumerate(male) if x.startswith("\\documentclass")][-1]
mO = next(i for i, x in enumerate(male) if re.match(r"^\\part\*\{原始内容\}", x))
fdc = [i for i, x in enumerate(fem) if x.startswith("\\documentclass")][-1]


def paras(lines, lo, hi, minlen=12):
    out = []
    for i in range(lo, min(hi, len(lines))):
        s = lines[i].strip()
        if not s or s.startswith("%") or HEAD.match(s) or ENV.match(s):
            continue
        if s in ("\\par", "\\\\", "\\noindent"):
            continue
        p = pnorm(s)
        if len(p) >= minlen:
            out.append(p)
    return out


def paraset(lines, lo, hi):
    return set(paras(lines, lo, hi))


NEWSET = set()
NEWSET |= paraset(book, mm, O)
NEWSET |= paraset(male, mdc, mO)
NEWSET |= paraset(fem, fdc, len(fem))
NEWSET |= paraset(pos, 0, len(pos))
POSSET = paraset(pos, 0, len(pos))
FEMSET = paraset(fem, fdc, len(fem))

# 旧区分段：按 part/chapter 行切
segs = []
cur = None
for i in range(O, len(book)):
    x = book[i]
    if x.lstrip().startswith("%"):
        continue
    m = HEAD.match(x)
    if m and m.group(1) in ("part", "chapter"):
        if cur:
            segs.append(cur + (i,))
        cur = (i, m.group(1), m.group(2).strip())
if cur:
    segs.append(cur + (len(book),))

# 骨架章清单
skch = [(i, HEAD.match(x).group(2).strip()) for i, x in enumerate(book)
        if mm <= i < O and HEAD.match(x) and HEAD.match(x).group(1) == "chapter"]

print("%-42s %6s %6s %6s %7s %7s" % ("旧区段", "行", "段落", "未覆盖", "在pos", "在fem"))
print("-" * 90)
rows = []
for (a, lv, t, b) in segs:
    ps = paras(book, a, b)
    un = [p for p in ps if p not in NEWSET]
    inp = sum(1 for p in un if p in POSSET)
    inf = sum(1 for p in un if p in FEMSET)
    rows.append((a, lv, t, b, len(ps), len(un), inp, inf))
    print("%-42s %6d %6d %6d %7d %7d" % (t[:42], b - a, len(ps), len(un), inp, inf))

with io.open(BASE + "_r81_segs.txt", "w", encoding="utf-8") as f:
    for a, lv, t, b, n, un, inp, inf in rows:
        f.write("L%d\t%s\t%d\t%d\t%d\n" % (a + 1, t, b - a, n, un))

# 每段最匹配骨架章（用 section 名交集 + 段落重叠）
print("\n" + "=" * 90)
print("【每段最匹配的骨架章】")
sksec = {}
for k, (i, t) in enumerate(skch):
    e = skch[k + 1][0] if k + 1 < len(skch) else O
    sksec[t] = set(norm for norm in [
        re.sub(r"\s+", "", HEAD.match(book[j]).group(2).strip())
        for j in range(i, e) if HEAD.match(book[j]) and HEAD.match(book[j]).group(1) == "section"])
    sksec[t + "#a"] = set(paras(book, i, e))

for a, lv, t, b in segs:
    my = set(re.sub(r"\s+", "", HEAD.match(book[j]).group(2).strip())
             for j in range(a, b) if HEAD.match(book[j]) and HEAD.match(book[j]).group(1) == "section")
    myp = set(paras(book, a, b))
    best = []
    for k, (i, ct) in enumerate(skch):
        e = skch[k + 1][0] if k + 1 < len(skch) else O
        cp = sksec.get(ct + "#a", set())
        ov = len(myp & cp)
        best.append((ov, ct))
    best.sort(reverse=True)
    print("  %-40s -> %s" % (t[:40], " | ".join("%s(%d)" % (c, o) for o, c in best[:3])))
