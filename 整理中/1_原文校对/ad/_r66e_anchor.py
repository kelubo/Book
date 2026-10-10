# -*- coding: utf-8 -*-
import io, re, collections
BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
lines = io.open(BASE + r"\book.tex", encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")
N = len(lines)
H = re.compile(r"^\s*\\(part|chapter|section|subsection|subsubsection)\*?\{")


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
LV = {"part": 0, "chapter": 1, "section": 2, "subsection": 3, "subsubsection": 4}
blk = {}
for k, (ln, lv, t) in enumerate(T):
    lvl = LV[lv]
    end = N + 1
    for ln2, lv2, _ in T[k + 1:]:
        if LV[lv2] <= lvl:
            end = ln2
            break
    blk[ln] = (lv, t, end, sum(1 for x in lines[ln:end - 1] if x.strip() and not x.strip().startswith("%")))


def n2(t):
    return re.sub(r"[\s\u3000]", "", re.sub(r"[（(][^（）()]*[）)]", "", t))


idx = collections.defaultdict(list)
for ln, lv, t in T:
    if ln >= OLD:
        idx[n2(t)].append((ln, lv, t))

for a in ["梅毒", "淋病", "衣原体感染", "软下疳", "滴虫病", "阴虱病", "尖锐湿疣",
          "生殖器疱疹", "乙型肝炎", "丙型肝炎", "猴痘", "COVID-19", "艾滋病"]:
    c = idx.get(n2(a), [])
    print("%-12s -> %s" % (a, " ; ".join("L%d %s %d行" % (ln, lv, blk[ln][3]) for ln, lv, t in c) or "无匹配"))
