# -*- coding: utf-8 -*-
"""r81 零丢失审计：旧区每一条内容行是否都已落入新结果"""
import io, re, collections

BASE = "D:/Git/Book/整理中/1_原文校对/ad/"
HEAD = re.compile(r"^\\(part|chapter|section|subsection|subsubsection)\*?\{")
ENV = re.compile(r"^\\(begin|end)\{")
SKIP = ("\\par", "\\\\", "\\noindent", "\\bigskip", "\\medskip", "\\smallskip")


def load(fn):
    return [x.rstrip("\r") for x in io.open(BASE + fn, encoding="utf-8").read().split("\n")]


def pnorm(s):
    return re.sub(r"[\s\u3000\u00a0]+", "", s.strip())


def content(lines, lo, hi):
    out = []
    for i in range(lo, min(hi, len(lines))):
        s = lines[i].strip()
        if not s or s.startswith("%") or HEAD.match(s) or ENV.match(s) or s in SKIP:
            continue
        if len(pnorm(s)) >= 12:
            out.append((i, s))
    return out


book = load("0_book.tex"); male = load("1_male.tex")
O = next(i for i, x in enumerate(book) if re.match(r"^\\part\{old\}", x))
mO = next(i for i, x in enumerate(male) if re.match(r"^\\part\*\{原始内容\}", x))

pv = {n: load("_r81pv_" + n + ".tex") for n in ("book", "male", "female", "position")}
SETS = {}
for n, L in pv.items():
    s = set()
    for x in L:
        t = x.strip()
        if t and not t.startswith("%") and not HEAD.match(t) and not ENV.match(t) and t not in SKIP:
            s.add(pnorm(t))
    SETS[n] = s
    print("预览 %-9s %6d 行, 唯一内容行 %d" % (n, len(L), len(s)))

# 旧区全部内容行（book + male），去重要按"是否任一卷已收录"
targets = {n: set() for n in pv}
for i, x in enumerate(pv["book"]):
    pass


def owner_file(norm_title):
    return None


miss = []
for i, s in content(book, O, len(book)):
    p = pnorm(s)
    if not any(p in SETS[n] for n in SETS):
        miss.append(("book", i + 1, s))
for i, s in content(male, mO, len(male)):
    p = pnorm(s)
    if not any(p in SETS[n] for n in SETS):
        miss.append(("male", i + 1, s))

print("=" * 80)
print("旧区内容行未落入新结果的条数：%d" % len(miss))
grp = collections.Counter()
for f, i, s in miss:
    grp[f] += 1
print(dict(grp))
print("=" * 80)
print("旧区内容行未落入新结果的条数：%d" % len(miss))
grp = collections.Counter()
for f, i, s in miss:
    grp[f] += 1
print(dict(grp))


def own(src, O2, i):
    cur = None
    for j in range(O2, i):
        m = re.match(r"^\\(part|chapter)\{([^}]*)\}", src[j])
        if m:
            cur = (m.group(1), m.group(2))
    return cur


grp2 = collections.Counter()
for f, i, s in miss:
    src = book if f == "book" else male
    grp2[own(src, O if f == "book" else mO, i - 1)] += 1
print("\n按旧区归属统计：")
for k, v in grp2.most_common(40):
    print("  %-6s %-40s %5d" % (k[0] if k else "?", (k[1] if k else "?")[:40], v))
for f, i, s in miss[:40]:
    print("  [%s] L%-6d %s" % (f, i, s[:100]))
