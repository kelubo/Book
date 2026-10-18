# -*- coding: utf-8 -*-
"""r68b：内容覆盖缺口分析
1) 骨架区（\part{old} 之前）的 part/chapter/section/subsection 结构 + \iffalse 区间
2) 旧区所有 chapter/section/subsection 标题及其块行数
3) 旧区标题在新骨架中的覆盖情况（未覆盖 -> 候选新增）
4) 骨架注释锚 `% 移入："..."` 是否能在旧区解析
"""
import io, os, re, collections

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
P = os.path.join(BASE, "book.tex")
lines = io.open(P, encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")
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


# ---- \iffalse 区间 ----
ifblk = []
depth = 0
start = None
for i, l in enumerate(lines):
    s = l.strip()
    if s == "\\iffalse":
        if depth == 0:
            start = i + 1
        depth += 1
    elif s == "\\fi" and depth > 0:
        depth -= 1
        if depth == 0:
            ifblk.append((start, i + 1))
print("\\iffalse 区间:", ifblk)

OFF = set()
for a, b in ifblk:
    for k in range(a, b + 1):
        OFF.add(k)

T = []
for i, l in enumerate(lines):
    s = l.strip()
    if not s or s.startswith("%"):
        continue
    m = H.match(s)
    if m:
        T.append((i + 1, m.group(1), gt(s)))

OLD = next(ln for ln, lv, t in T if lv == "part" and t == "old")
print("旧区起点 L%d" % OLD)

# 块行数
blk = {}
for k, (ln, lv, t) in enumerate(T):
    lvl = LV[lv]
    end = N + 1
    for ln2, lv2, _ in T[k + 1:]:
        if LV[lv2] <= lvl:
            end = ln2
            break
    body = sum(1 for x in lines[ln:end - 1] if x.strip() and not x.strip().startswith("%"))
    blk[ln] = body

# 骨架区结构
skel_secs = set()
skel_all = set()


def norm(t):
    t = re.sub(r"\\[a-zA-Z@]+\*?(\[[^\]]*\])?(\{[^{}]*\})?", lambda m: m.group(2) or "", t)
    t = t.replace("\\", "")
    t = re.sub(r"[（(][^（）()]*[）)]", "", t)
    return re.sub(r"[\s\u3000·、，,：:；;（）()「」【】\-—–_/]", "", t)


for ln, lv, t in T:
    if ln >= OLD:
        break
    if ln in OFF:
        continue
    skel_all.add(norm(t))
    if lv in ("section", "subsection"):
        skel_secs.add(norm(t))

print("骨架区标题（去重后）:", len(skel_all), " 其中节/小节:", len(skel_secs))

# 旧区标题覆盖
old_items = [(ln, lv, t) for ln, lv, t in T if ln >= OLD]
print("旧区标题总数:", len(old_items))
print("  其中 chapter %d / section %d / subsection %d" % (
    sum(1 for a, b, c in old_items if b == "chapter"),
    sum(1 for a, b, c in old_items if b == "section"),
    sum(1 for a, b, c in old_items if b == "subsection")))

# 旧区 part 归属
cur_old = "?"
old_part_of = {}
for ln, lv, t in old_items:
    if lv == "part":
        cur_old = t
    old_part_of[ln] = cur_old

miss = collections.defaultdict(list)
for ln, lv, t in old_items:
    if lv not in ("chapter", "section"):
        continue
    n = norm(t)
    if not n:
        continue
    hit = n in skel_all
    if not hit:
        # 子串式宽松匹配
        for s in skel_all:
            if len(n) >= 4 and (n in s or s in n):
                hit = True
                break
    if not hit:
        miss[old_part_of[ln]].append((ln, lv, t, blk[ln]))

print()
print("=" * 78)
print("旧区未被骨架覆盖的 chapter / section（按旧 part 分组）")
print("=" * 78)
tot = 0
for k, v in miss.items():
    v.sort(key=lambda x: -x[3])
    print()
    print("### %s  （未覆盖 %d 项）" % (k, len(v)))
    for ln, lv, t, b in v[:60]:
        print("   L%-6d %-9s %-46s %5d 行" % (ln, lv, t[:46], b))
    tot += len(v)
print()
print("未覆盖合计 %d 项" % tot)

# 骨架注释锚解析
print()
print("=" * 78)
print("骨架注释锚 `% 移入：\"...\"` 解析情况")
print("=" * 78)
anchors = []
for i in range(0, OLD - 1):
    s = lines[i].strip()
    if not s.startswith("%"):
        continue
    for m in re.finditer(r'"([^"]{2,60})"', s):
        anchors.append((i + 1, m.group(1)))
print("锚总数:", len(anchors))
bad = []
for ln, a in anchors:
    n = norm(a)
    if not n:
        continue
    found = any(n in norm(t) or norm(t) in n for _, _, t in old_items if len(norm(t)) >= 2)
    if not found:
        bad.append((ln, a))
print("旧区搜不到的锚:", len(bad))
for ln, a in bad:
    print("   L%-5d %s" % (ln, a))
