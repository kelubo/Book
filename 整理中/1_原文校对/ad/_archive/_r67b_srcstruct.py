# -*- coding: utf-8 -*-
"""r67：为骨架每章解析出旧区来源，并列出旧区对应块的内部 section 结构。
用途：为「补二级结构」提供事实依据（不猜，全部来自旧区实际标题）。
"""
import io, os, re, collections

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
P = os.path.join(BASE, "book.tex")
lines = io.open(P, encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")
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


def body(ln, e):
    return sum(1 for x in lines[ln:e - 1] if x.strip() and not x.strip().startswith("%"))


# ---- 骨架区：章 -> 锚 ----
STR = re.compile(r'"([^"]{2,60})"')
frames = []  # (part, chapter_ln, chapter, raw_comment)
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

# ---- 旧区索引 ----
def n2(t):
    return re.sub(r"[\s\u3000]", "", re.sub(r"[（(][^（）()]*[）)]", "", t))


idx = collections.defaultdict(list)
for ln, lv, t in T:
    if ln >= OLD:
        idx[n2(t)].append((ln, lv, t))

out = []
out.append("旧区起点 L%d；骨架 %d 章\n" % (OLD, len(frames)))

for part, cl, ch, cm in frames:
    out.append("\n" + "=" * 78)
    out.append("【%s】L%d  %s   body=%d" % (part, cl, ch, body(cl, ENDMAP[cl])))
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
    seen = set()
    for a in anchors:
        if a in seen:
            continue
        seen.add(a)
        c = idx.get(n2(a), [])
        if not c:
            out.append("   [未命中] %s" % a)
            continue
        for ln, lv, t in c[:3]:
            out.append("   %-6s L%-6d %-10s %-34s %d行" % ("HIT", ln, lv, t[:34], body(ln, ENDMAP[ln])))
            if lv in ("chapter", "section"):
                for ln2, lv2, t2 in T:
                    if ln2 > ln and ln2 < ENDMAP[ln] and lv2 in ("section", "subsection"):
                        out.append("            %s   %s  L%d" % ("  " if lv2 == "section" else "      ", t2[:50], ln2))

io.open(os.path.join(BASE, "_r67b_out.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(out))
print("written _r67b_out.txt lines=", len(out))
