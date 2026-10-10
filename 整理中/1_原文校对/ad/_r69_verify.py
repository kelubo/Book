# -*- coding: utf-8 -*-
"""r69_verify：逐行对比备份与当前，证明只动了标题行与注释行"""
import io, os, re, collections

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
a = io.open(os.path.join(BASE, "_backup_r68", "book.tex"), encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")
b = io.open(os.path.join(BASE, "book.tex"), encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")
print("行数 %d -> %d（%+d）" % (len(a), len(b), len(b) - len(a)))

raw = io.open(os.path.join(BASE, "book.tex"), "rb").read()
print("换行：CRLF %d ｜ 裸 LF %d" % (raw.count(b"\r\n"), raw.count(b"\n") - raw.count(b"\r\n")))

H = re.compile(r"^\s*\\(part|chapter|section|subsection|subsubsection)\*?\{")


def kind(l):
    s = l.strip()
    if not s:
        return "blank"
    if s.startswith("%"):
        return "comment"
    if H.match(s):
        return "heading"
    return "body"


ka = [kind(x) for x in a]
kb = [kind(x) for x in b]

# 正文行（body）多重集必须完全一致
ma = collections.Counter(x for x, k in zip(a, ka) if k == "body")
mb = collections.Counter(x for x, k in zip(b, kb) if k == "body")
print("正文行数 %d -> %d" % (sum(ma.values()), sum(mb.values())))
d = ma - mb
d2 = mb - ma
print("正文行差异：消失 %d 行，新增 %d 行" % (sum(d.values()), sum(d2.values())))
for k, v in list(d.items())[:10]:
    print("   -", v, repr(k[:70]))
for k, v in list(d2.items())[:10]:
    print("   +", v, repr(k[:70]))
assert sum(d.values()) == 0 and sum(d2.values()) == 0, "正文被改动！"

# 标题行差异
ha = [x for x, k in zip(a, ka) if k == "heading"]
hb = [x for x, k in zip(b, kb) if k == "heading"]
ca, cb = collections.Counter(x.strip() for x in ha), collections.Counter(x.strip() for x in hb)
print("标题行 %d -> %d（%+d）" % (len(ha), len(hb), len(hb) - len(ha)))
gone = ca - cb
new = cb - ca
print("移除的标题 %d 类：" % len(gone))
for k, v in gone.items():
    print("   -", v, k[:70])
print("新增的标题 %d 类：" % len(new))
for k, v in list(new.items())[:12]:
    print("   +", v, k[:70])
print("   ...（共 %d 类）" % len(new))

# 旧区逐字
ia = a.index("\\part{old}")
ib = b.index("\\part{old}")
print("旧区起点 L%d -> L%d；逐字一致：%s" % (ia + 1, ib + 1, a[ia:] == b[ib:]))
assert a[ia:] == b[ib:]

# 花括号
def br(ls):
    n = 0
    for l in ls:
        s = l.strip()
        if s.startswith("%"):
            continue
        n += s.count("{") - s.count("}")
    return n
print("花括号净值 %d -> %d" % (br(a), br(b)))
print()
print("全部断言通过。")
