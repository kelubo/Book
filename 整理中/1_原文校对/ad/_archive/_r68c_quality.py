# -*- coding: utf-8 -*-
"""r68c：骨架质量体检
1) 每章节数（0 节的"光杆章"）
2) 每节小节数
3) 章名/节名 跨章重名
4) 标题规范（中文主体宽度 >=30；疑问句；顿号堆叠；英文括号）
5) 每篇章/节规模
"""
import io, os, re, collections, unicodedata

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
SK = [(ln, lv, t) for ln, lv, t in T if ln < OLD]


def W(s):
    """中文主体宽度：剥英文对照括号"""
    def cjk(x):
        return sum(1 for c in x if "\u4e00" <= c <= "\u9fff")
    def rep(m):
        return "" if cjk(m.group(1)) == 0 else m.group(0)
    s2 = re.sub(r"[（(]([^（）()]*)[）)]", rep, s)
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in s2.strip())


print("=" * 78)
print("1) 每章节数（骨架区）")
print("=" * 78)
flat = []
cur = None
cnt = {}
order = []
for ln, lv, t in SK:
    if lv == "part":
        cur = t
    elif lv == "chapter":
        order.append((ln, t, cur))
        cnt[ln] = 0
        last_ch = ln
    elif lv == "section":
        if order:
            cnt[order[-1][0]] += 1
for ln, t, p in order:
    c = cnt[ln]
    if c == 0:
        flat.append((ln, t, p))
print("章总数:", len(order), " 0 节的章:", len(flat))
for ln, t, p in flat:
    print("   L%-5d [%s] %s" % (ln, (p or "（无篇）")[:8], t))

print()
print("=" * 78)
print("2) 每节小节数（骨架区）")
print("=" * 78)
secs = [(ln, t) for ln, lv, t in SK if lv == "section"]
cnt2 = {}
idx = 0
for i, (ln, lv, t) in enumerate(SK):
    if lv == "section":
        n = 0
        for ln2, lv2, _ in SK[i + 1:]:
            if LV[lv2] <= 2:
                break
            if lv2 == "subsection":
                n += 1
        cnt2[ln] = n
deep = [(ln, t, cnt2[ln]) for ln, t in secs if cnt2[ln] > 0]
print("节总数:", len(secs), " 带小节的节:", len(deep))
for ln, t, n in deep:
    print("   L%-5d %-44s %d 小节" % (ln, t[:44], n))

print()
print("=" * 78)
print("3) 跨章重名（章名 / 节名）")
print("=" * 78)
ch = collections.defaultdict(list)
for ln, t, p in order:
    ch[t].append(ln)
d = {k: v for k, v in ch.items() if len(v) > 1}
print("重名章:", len(d))
for k, v in d.items():
    print("   %s  @ %s" % (k, v))
secn = collections.defaultdict(list)
for ln, lv, t in SK:
    if lv in ("section", "subsection"):
        secn[t].append((ln, lv))
d2 = {k: v for k, v in secn.items() if len(v) > 1}
print("重名节/小节:", len(d2))
for k, v in sorted(d2.items(), key=lambda x: -len(x[1])):
    print("   %-40s x%d  @ %s" % (k[:40], len(v), [a for a, b in v]))

print()
print("=" * 78)
print("4) 标题规范（骨架区）")
print("=" * 78)
long_t = []
for ln, lv, t in SK:
    w = W(t)
    if w >= 30:
        long_t.append((ln, lv, t, w))
print("中文主体宽 >=30：", len(long_t))
for ln, lv, t, w in long_t:
    print("   L%-5d %-9s w=%-3d %s" % (ln, lv, w, t[:60]))
q = [(ln, lv, t) for ln, lv, t in SK if re.search(r"[？?]$", t) or "还是" in t or "是否" in t]
print("疑问句/选择式：", len(q))
for ln, lv, t in q:
    print("   L%-5d %-9s %s" % (ln, lv, t[:60]))
dun = [(ln, lv, t) for ln, lv, t in SK if re.search(r"[、，]", t) and lv in ("chapter", "section")]
print("章/节名含顿号逗号：", len(dun))
for ln, lv, t in dun[:20]:
    print("   L%-5d %-9s %s" % (ln, lv, t[:60]))
en = [(ln, lv, t) for ln, lv, t in SK if re.search(r"[（(][^（）()]*[A-Za-z][^（）()]*[）)]", t)]
print("含英文对照括号：", len(en))
for ln, lv, t in en:
    print("   L%-5d %-9s %s" % (ln, lv, t[:60]))

print()
print("=" * 78)
print("5) 每篇规模")
print("=" * 78)
cur = None
st = {}
for ln, lv, t in SK:
    if lv == "part":
        cur = t
        st.setdefault(t, {"line": ln, "ch": 0, "sec": 0, "sub": 0})
    elif cur:
        if lv == "chapter":
            st[cur]["ch"] += 1
        elif lv == "section":
            st[cur]["sec"] += 1
        elif lv == "subsection":
            st[cur]["sub"] += 1
for k, v in st.items():
    print("   %-24s 章 %2d  节 %3d  小节 %3d" % (k[:24], v["ch"], v["sec"], v["sub"]))
