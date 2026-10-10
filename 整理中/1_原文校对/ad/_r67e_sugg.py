# -*- coding: utf-8 -*-
"""r67：为骨架每章生成"建议补的节"清单。
规则：来源块若为 chapter -> 取其 section；若为 section -> 取其 subsection。
     标题全部来自旧区实际，归一化去重，附行数；不做任何创作。
"""
import io, os, re, collections

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
lines = io.open(os.path.join(BASE, "book.tex"), encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")
N = len(lines)
H = re.compile(r"^[ \t]*\\(part|chapter|section|subsection|subsubsection)\*?\{")
LVN = {"part": 0, "chapter": 1, "section": 2, "subsection": 3, "subsubsection": 4}


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
ENDMAP = {}
for k, (ln, lv, t) in enumerate(T):
    lvl = LVN[lv]
    e = N + 1
    for ln2, lv2, _ in T[k + 1:]:
        if LVN[lv2] <= lvl:
            e = ln2
            break
    ENDMAP[ln] = e


def nb(ln, e):
    return sum(1 for x in lines[ln:e - 1] if x.strip() and not x.strip().startswith("%"))


def n2(t):
    return re.sub(r"[\s\u3000]", "", re.sub(r"[（(][^（）()]*[）)]", "", t))


idx = collections.defaultdict(list)
for ln, lv, t in T:
    if ln >= OLD:
        idx[n2(t)].append((ln, lv, t))

STR = re.compile(r'"([^"]{2,60})"')
frames = []
cur_part = None
cur_ch = None
for i, l in enumerate(lines[:OLD - 1]):
    s = l.strip()
    if s.startswith("\\part"):
        cur_part = gt(s)
    elif H.match(s) and s.lstrip("\\").startswith("chapter"):
        if cur_ch:
            frames.append(cur_ch)
        cur_ch = [cur_part, i + 1, gt(s), []]
    if cur_ch is not None and s.startswith("%"):
        cur_ch[3].append(s)
if cur_ch:
    frames.append(cur_ch)

out = []
for part, cl, ch, cm in frames:
    own_secs = [t2 for ln2, lv2, t2 in T if ln2 > cl and ln2 < ENDMAP[cl] and lv2 == "section"]
    anchors = []
    for c in cm:
        anchors += STR.findall(c)
        m = re.match(r"%\s*(?:移入|合并|去重|拆分)\s*[:：]\s*(.+)$", c)
        if m and '"' not in c:
            seg = re.split(r"[（(]", m.group(1))[0]
            for x in re.split(r"[、/]", seg):
                x = x.strip().strip('"')
                if 2 <= len(x) <= 40:
                    anchors.append(x)
    out.append("\n" + "=" * 76)
    out.append("【%s】L%d %s  (现有 %d 节: %s)" % (part, cl, ch, len(own_secs), "、".join(x[:14] for x in own_secs)))
    seen_anchor = set()
    touched = set()
    for a in anchors:
        if a in seen_anchor:
            continue
        seen_anchor.add(a)
        cand = idx.get(n2(a), [])
        if not cand:
            continue
        for ln, lv, t in cand[:2]:
            e = ENDMAP[ln]
            sub = [(l2, v2, t2) for l2, v2, t2 in T if ln < l2 < e and LVN[v2] == LVN[lv] + 1]
            out.append("   [%s] %s L%d %d行 -> 直接子级 %d 个" % (lv, t[:32], ln, nb(ln, e), len(sub)))
            for l2, v2, t2 in sub[:16]:
                if n2(t2) in touched:
                    out.append("        · %-40s L%-6d %d行  已见" % (t2[:40], l2, nb(l2, ENDMAP[l2])))
                else:
                    touched.add(n2(t2))
                    out.append("        · %-40s L%-6d %d行" % (t2[:40], l2, nb(l2, ENDMAP[l2])))

io.open(os.path.join(BASE, "_r67e_out.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(out))
print("written", len(out))
