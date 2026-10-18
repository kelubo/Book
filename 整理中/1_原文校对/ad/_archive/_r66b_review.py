# -*- coding: utf-8 -*-
"""r66b：book.tex 新骨架（\part{old} 之前）目录合理性审查。

输出：
  A 各篇规模（章数 / 来源预算 / 细化程度）
  B 章粒度失衡
  C 命名规范（中文主体宽度 / 顿号堆叠 / 英文括号）
  D 节标题宽度（section/subsection）
  E 骨架内重名与近似名
  F 注释与结构卫生（失效引用、无注释无正文章、陈旧说明）
  G 骨架区 vs r65 备份的结构差异
"""
import io, re, os, collections, unicodedata

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
SRC = os.path.join(BASE, "book.tex")
raw = io.open(SRC, encoding="utf-8", newline="").read().replace("\r\n", "\n")
lines = raw.split("\n")
N = len(lines)
H = re.compile(r"^\s*\\(part|chapter|section|subsection|subsubsection)\*?\{")


def get_title(s):
    rest = s[s.index("{"):]
    d = 0
    for j, ch in enumerate(rest):
        if ch == "{":
            d += 1
        elif ch == "}":
            d -= 1
            if d == 0:
                return rest[1:j]
    return rest[1:]


titles = []
for i, l in enumerate(lines):
    s = l.strip()
    if s.startswith("%"):
        continue
    m = H.match(s)
    if m:
        titles.append((i + 1, m.group(1), get_title(s)))

OLD_PART = next(ln for ln, lv, t in titles if lv == "part" and t.strip() == "old")
# 骨架起点：第一个 \part 之前的说明注释块首
SK_START = next(ln for ln, lv, t in titles if lv == "part" and ln < OLD_PART) 
print("骨架首个 \\part 在 L%d，旧区 \\part{old} 在 L%d，总行数 %d" % (SK_START, OLD_PART, N))

LEVEL_ORDER = {"part": 0, "chapter": 1, "section": 2, "subsection": 3, "subsubsection": 4}
blocks = {}
for k, (ln, lv, t) in enumerate(titles):
    lvl = LEVEL_ORDER[lv]
    end = N
    for ln2, lv2, t2 in titles[k + 1:]:
        if LEVEL_ORDER[lv2] <= lvl:
            end = ln2
            break
    body = sum(1 for x in lines[ln:end - 1] if x.strip() and not x.strip().startswith("%"))
    blocks[ln] = (lv, t, end, body)


def norm(t):
    return re.sub(r"[\s\u3000]", "", t)


def norm2(t):
    return re.sub(r"[\s\u3000]", "", re.sub(r"[（(][^（）()]*[）)]", "", t))


old_idx = collections.defaultdict(list)
old_idx2 = collections.defaultdict(list)
for ln, lv, t in titles:
    if ln >= OLD_PART:
        old_idx[norm(t)].append((ln, lv, t))
        old_idx2[norm2(t)].append((ln, lv, t))


def resolve(title):
    c = old_idx.get(norm(title)) or old_idx2.get(norm2(title)) or []
    if c:
        return c[0][0], c[0][1], blocks[c[0][0]][3], c
    return None, None, None, []


Q = re.compile(r"[“\"]([^”\"]+)[”\"]")

# ---- 归集骨架结构 ----
chapters = []
sections = []          # (part, chapter, line, level, title)
cur_part = None
cur_ch = None
i = SK_START - 1
while i < OLD_PART - 1:
    s = lines[i].strip()
    if not s:
        i += 1; continue
    if s.startswith("%"):
        # 收集该章下所有注释里的锚
        if chapters and (cur_ch is not None):
            kind = None
            for k in ("移入", "去重", "合并", "可选", "回收", "拆分"):
                if k in s:
                    kind = k; break
            if kind:
                qs = Q.findall(s)
                if not qs and ("合并" in s or "拆" in s):
                    tail = s.split("：", 1)[1] if "：" in s else ""
                    tail = re.sub(r"[（(][^）)]*[）)]", "", tail)
                    qs = [x.strip() for x in re.split(r"[/、]", tail) if x.strip()]
                for t in qs:
                    chapters[-1][3].append((kind, t))
        i += 1; continue
    m = H.match(s)
    if not m:
        i += 1; continue
    lv, t = m.group(1), get_title(s)
    if lv == "part":
        cur_part = t; cur_ch = None
    elif lv == "chapter":
        chapters.append([cur_part, t, i + 1, []])
        cur_ch = t
    elif lv in ("section", "subsection", "subsubsection"):
        sections.append((cur_part, cur_ch, i + 1, lv, t))
    i += 1

# ---- 逐章预算 ----
rows = []
for part, ch, cl, items in chapters:
    srcs = [x for x in items if x[0] in ("移入", "去重", "合并", "回收")]
    subs = [x for x in items if x[0] == "细目"]
    budget, missing, resolved = 0, [], []
    for kind, t in srcs:
        ln, lv, body, cands = resolve(t)
        if ln:
            budget += body
            resolved.append((kind, t, ln, lv, body, len(cands)))
        else:
            missing.append((kind, t))
    rows.append(dict(part=part, ch=ch, cl=cl, budget=budget, nsrc=len(srcs),
                     nsub=0, details=resolved, missing=missing))
# 细目计数
subcnt = collections.Counter((c[0], c[1]) for c in ((s[0], s[1]) for s in sections))
for r in rows:
    r["nsub"] = subcnt.get((r["part"], r["ch"]), 0)

out = []
w = out.append
w("=" * 100)
w("A. 各篇规模")
w("=" * 100)
bypart = collections.OrderedDict()
for r in rows:
    bypart.setdefault(r["part"], []).append(r)
for p, rs in bypart.items():
    tb = sum(x["budget"] for x in rs)
    nsub = sum(x["nsub"] for x in rs)
    nempty = sum(1 for x in rs if x["nsrc"] == 0 and x["nsub"] == 0)
    ndetail = sum(1 for x in rs if x["nsub"] > 0)
    w("")
    w("【%s】章 %d ｜ 来源预算 %d 行 ｜ 均 %d 行/章 ｜ 已细化 %d 章 ｜ 纯占位 %d 章 ｜ 细目 %d"
      % (p, len(rs), tb, tb // max(len(rs), 1), ndetail, nempty, nsub))
    for x in rs:
        flag = " [细目%d]" % x["nsub"] if x["nsub"] else (" [占位]" if x["nsrc"] == 0 else "")
        w("   L%-6d %-40s 预算 %6d 行  锚 %d%s" % (x["cl"], x["ch"][:40], x["budget"], x["nsrc"], flag))

w("")
w("=" * 100)
w("B. 章粒度失衡")
w("=" * 100)
srt = sorted(rows, key=lambda x: -x["budget"])
w("-- 预算最大 15 章 --")
for x in srt[:15]:
    w("   %6d 行  %-18s %s" % (x["budget"], x["part"][:16], x["ch"][:46]))
w("-- 预算最小 18 章（未细化者）--")
tiny = [x for x in sorted(rows, key=lambda x: x["budget"]) if x["nsub"] == 0]
for x in tiny[:18]:
    w("   %6d 行  %-18s %s" % (x["budget"], x["part"][:16], x["ch"][:46]))

PAREN = re.compile(r"[（(]([^（）()]*)[）)]")


def cjk(s):
    return sum(1 for c in s if "\u4e00" <= c <= "\u9fff")


def W(s):
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in s)


def body(s):
    def rep(m):
        return "" if cjk(m.group(1)) == 0 else m.group(0)
    return W(PAREN.sub(rep, s).strip())


w("")
w("=" * 100)
w("C. 章标题命名规范（中文主体宽度）")
w("=" * 100)
w("-- 宽 >= 18 --")
for x in rows:
    b = body(x["ch"])
    if b >= 18:
        w("   %3d  %s" % (b, x["ch"]))
w("-- 含 2 个以上顿号 --")
for x in rows:
    if x["ch"].count("\u3001") >= 2:
        w("   顿号%d  %s" % (x["ch"].count("\u3001"), x["ch"]))
w("-- 带英文对照括号 --")
for x in rows:
    if re.search(r"[（(][A-Za-z]", x["ch"]):
        w("   %s" % x["ch"])

w("")
w("=" * 100)
w("D. 骨架内节/小节标题宽度（中文主体 >= 20）")
w("=" * 100)
for part, ch, ln, lv, t in sections:
    b = body(t)
    if b >= 20:
        w("   %3d  %-10s  L%-6d %s" % (b, lv, ln, t))

w("")
w("=" * 100)
w("E. 骨架内重名 / 近似名")
w("=" * 100)
namec = collections.Counter(norm(x["ch"]) for x in rows)
for k, v in namec.items():
    if v > 1:
        hit = [x for x in rows if norm(x["ch"]) == k]
        w("   重名×%d  %s   ->  %s" % (v, k, " / ".join("L%d(%s)" % (x["cl"], x["part"]) for x in hit)))
# 近似：共享 >= 3 连续汉字
w("-- 共享 >=3 连续字的章名对 --")
for a in range(len(rows)):
    for b2 in range(a + 1, len(rows)):
        ta, tb = norm(rows[a]["ch"]), norm(rows[b2]["ch"])
        best = 0
        for L in range(3, min(len(ta), len(tb)) + 1):
            for st in range(len(ta) - L + 1):
                if ta[st:st + L] in tb:
                    best = max(best, L)
        if best >= 3:
            w("   共享%d字： %s(%s) ｜ %s(%s)" % (best, rows[a]["ch"], rows[a]["part"][:6],
                                                rows[b2]["ch"], rows[b2]["part"][:6]))

w("")
w("=" * 100)
w("F. 注释与结构卫生")
w("=" * 100)
w("-- 锚未命中（注释里的标题在旧区找不到）--")
miss = 0
for x in rows:
    for kind, t in x["missing"]:
        miss += 1
        w("   [%s] %s「%s」" % (x["ch"], kind, t))
if not miss:
    w("   （无）")
w("-- 既无来源注释也无细目的章 --")
for x in rows:
    if x["nsrc"] == 0 and x["nsub"] == 0:
        w("   L%-6d %s" % (x["cl"], x["ch"]))
w("-- 一行正文（非注释）出现在骨架区的行 --")
cnt = 0
for i in range(SK_START - 1, OLD_PART - 1):
    s = lines[i].strip()
    if s and not s.startswith("%") and not H.match(s):
        cnt += 1
        if cnt <= 20:
            w("   L%-6d %s" % (i + 1, s[:80]))
w("   骨架区正文行合计 %d" % cnt)

w("")
w("=" * 100)
w("G. 骨架区 vs r65 备份结构差异")
w("=" * 100)
BAK = os.path.join(BASE, "_backup_r65", "book.tex")
if os.path.exists(BAK):
    bl = io.open(BAK, encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")
    def scoop(ls):
        res, cp, cc = [], None, None
        for l in ls:
            s = l.strip()
            if s.startswith("%"): continue
            m = H.match(s)
            if not m: continue
            lv, t = m.group(1), get_title(s)
            if lv == "part": cp = t; cc = None
            elif lv == "chapter": res.append((cp, t)); cc = t
        return res
    # r65 备份里骨架区 = \part{old} 之前
    bp = next(i for i, l in enumerate(bl) if l.strip() == "\\part{old}")
    old_sk = scoop(bl[:bp])
    new_sk = scoop(lines[:OLD_PART - 1])
    so, sn = collections.OrderedDict(), collections.OrderedDict()
    for p, c in old_sk: so.setdefault(p, []).append(c)
    for p, c in new_sk: sn.setdefault(p, []).append(c)
    w("r65：%d 篇 / %d 章       现在：%d 篇 / %d 章" %
      (len(so), len(old_sk), len(sn), len(new_sk)))
    w("")
    w("-- 篇（r65 -> 现在）--")
    for p in so: 
        w("   r65  %s" % p)
    for p in sn:
        w("   现   %s" % p)
    w("")
    w("-- 仅 r65 有的章 --")
    oc = set(norm(c) for _, c in old_sk)
    nc = set(norm(c) for _, c in new_sk)
    for p, c in old_sk:
        if norm(c) not in nc:
            w("   [%s] %s" % (p, c))
    w("-- 仅现在有的章 --")
    for p, c in new_sk:
        if norm(c) not in oc:
            w("   [%s] %s" % (p, c))

io.open(os.path.join(BASE, "_r66b_out.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(out))
print("written _r66b_out.txt  %d lines" % len(out))
