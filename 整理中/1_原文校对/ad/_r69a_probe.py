# -*- coding: utf-8 -*-
"""r69a：为每个"零小节"的骨架节，在旧区里找出同名的块及其现成子标题。
输出：_r69a_out.txt
"""
import io, os, re, collections

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
lines = io.open(os.path.join(BASE, "book.tex"), encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")
N = len(lines)
H = re.compile(r"^\s*\\(part|chapter|section|subsection|subsubsection)\*?\{")
LV = {"part": 0, "chapter": 1, "section": 2, "subsection": 3, "subsubsection": 4}


def gt(s):
    r = s[s.index("{"):]
    d = 0
    for j, c in enumerate(r):
        if c == "{":
            d += 1
        elif c == "}":
            d -= 1
            if d == 0:
                return r[1:j]
    return r[1:]


T = []
for i, l in enumerate(lines):
    s = l.strip()
    if not s or s.startswith("%"):
        continue
    m = H.match(s)
    if m:
        T.append((i + 1, m.group(1), gt(s)))
OLD = next(ln for ln, lv, t in T if lv == "part" and t == "old")

# 每个标题的块区间与子标题
kids = collections.defaultdict(list)
endof = {}
for k, (ln, lv, t) in enumerate(T):
    lvl = LV[lv]
    end = N + 1
    for ln2, lv2, _ in T[k + 1:]:
        if LV[lv2] <= lvl:
            end = ln2
            break
    endof[ln] = end
    for ln2, lv2, t2 in T[k + 1:]:
        if ln2 >= end:
            break
        kids[ln].append((ln2, lv2, t2))


def norm(t):
    t = re.sub(r"\\[a-zA-Z@]+\*?(\[[^\]]*\])?(\{[^{}]*\})?", lambda m: m.group(2) or "", t)
    t = t.replace("\\", "")
    t = re.sub(r"[（(][^（）()]*[）)]", "", t)
    return re.sub(r"[\s\u3000·、，,：:；;（）()「」【】\-—–_/’'\"“”]", "", t)


def body(ln):
    e = endof[ln]
    return sum(1 for x in lines[ln:e - 1] if x.strip() and not x.strip().startswith("%"))


# 旧区索引（任意层级）
old_idx = collections.defaultdict(list)
for ln, lv, t in T:
    if ln >= OLD:
        old_idx[norm(t)].append((ln, lv, t))

# 骨架章 -> 锚
anchors = collections.defaultdict(list)
for i, l in enumerate(lines[:OLD - 1]):
    s = l.strip()
    if not s.startswith("%"):
        continue
    for m in re.finditer(r'"([^"]{2,60})"', s):
        anchors[i + 1].append(m.group(1))

# 骨架：章 / 节
sk = [(ln, lv, t) for ln, lv, t in T if ln < OLD]

# \iffalse
off = set()
d = 0
st = None
for i, l in enumerate(lines):
    s = l.strip()
    if re.match(r"^\\iffalse\b", s):
        if d == 0:
            st = i + 1
        d += 1
    elif s == "\\fi" and d > 0:
        d -= 1
        if d == 0:
            for k in range(st, i + 2):
                off.add(k)

out = []
A = out.append
cp = cc = None
n_done = n_no = 0
for i, (ln, lv, t) in enumerate(sk):
    if ln in off:
        continue
    if lv == "part":
        cp = t
        A("")
        A("#" * 2 + " 篇 " + t)
        continue
    if lv == "chapter":
        cc = t
        A("")
        A("### 章 " + t)
        # 章的锚
        for j in range(ln, endof[ln]):
            pass
        an = []
        for k in range(ln, min(endof[ln], OLD)):
            an += anchors.get(k + 1, [])
        A("  锚: " + (" ; ".join(an) if an else "（无）"))
        continue
    if lv != "section":
        continue
    # 已有小节？
    has = [x for x in kids.get(ln, []) if x[1] == "subsection"]
    n = len(has)
    if n:
        continue
    n_no += 1
    # 找旧区同名块
    cand = old_idx.get(norm(t), [])
    A("")
    A("- 节 %s" % t)
    if not cand:
        A("    [无同名旧区块]")
        continue
    best = None
    for cln, clv, ct in cand:
        ks = [x for x in kids.get(cln, []) if x[1] in ("subsection", "subsubsection")]
        if best is None or len(ks) > len(best[2]):
            best = (cln, clv, ks)
    cln, clv, ks = best
    n_done += 1
    A("    旧区 L%d (%s) %d 行, 子标题 %d 个:" % (cln, clv, body(cln), len(ks)))
    for kln, klv, kt in ks:
        A("       - %s" % kt[:56])

print("零小节骨架节 %d 个；其中旧区有同名块 %d 个（%.0f%%）" % (n_no, n_done, 100.0 * n_done / max(n_no, 1)))
io.open(os.path.join(BASE, "_r69a_out.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
print("written _r69a_out.txt")
