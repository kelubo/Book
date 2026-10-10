# -*- coding: utf-8 -*-
"""r72 验证：与 _backup_r72/ 逐段比对。

断言：
  book.tex   —— \\part{old} 及其后逐行一致；替换区之前的行也逐行一致。
  female/male—— \\part*{原始内容} 及其后逐行一致；\\mainmatter / \\listoftables 之前逐行一致。
另报告正文行多重集变化（只允许注释/标题行变化，正文行不得增减）。
"""
import io
import os
import re
from collections import Counter

BASE = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(BASE, "_backup_r72")
TITLE = re.compile(r"^\\(part|chapter|section|subsection)\*?\{")


def load(p):
    raw = io.open(p, encoding="utf-8", newline="").read()
    return raw, raw.count("\r\n"), raw.replace("\r\n", "\n").split("\n")


def body_counter(lines, zone=None):
    """正文行（非空、非注释、非标题）的多重集"""
    return Counter(l for l in lines if l.strip() and not l.strip().startswith("%") and not TITLE.match(l.strip()))


ok = True

# ── book.tex ──
raw_a, crlf_a, a = load(os.path.join(B, "book.tex"))
raw_b, crlf_b, b = load(os.path.join(BASE, "book.tex"))
ia = next(i for i, l in enumerate(a) if l.strip() == "\\part{old}")
ib = next(i for i, l in enumerate(b) if l.strip() == "\\part{old}")
print("book.tex  CRLF %d→%d ; 行 %d→%d ; \\part{old} L%d→L%d" % (crlf_a, crlf_b, len(a), len(b), ia + 1, ib + 1))
print("  旧区逐字一致 :", a[ia:] == b[ib:])
print("  骨架区前段（\\mainmatter 之前）逐字一致 :", a[:140] == b[:140])
ca, cb = body_counter(a), body_counter(b)
d = ca - cb
e = cb - ca
print("  正文行多重集：旧 %d → 新 %d ; 消失 %d ; 新增 %d" % (sum(ca.values()), sum(cb.values()), sum(d.values()), sum(e.values())))
if d:
    print("    消失样例：", list(d.items())[:5])
if e:
    print("    新增样例：", list(e.items())[:5])
ok &= (a[ia:] == b[ib:]) and (a[:140] == b[:140]) and sum(d.values()) == 0 and sum(e.values()) == 0

# ── female / male ──
for fn, anchor in (("female.tex", "\\mainmatter"), ("male.tex", "\\listoftables")):
    ra, ca_, la = load(os.path.join(B, fn))
    rb, cb_, lb = load(os.path.join(BASE, fn))
    ia = next(i for i, l in enumerate(la) if l.strip() == anchor)
    ib = next(i for i, l in enumerate(lb) if l.strip() == anchor)
    oa = next(i for i, l in enumerate(la) if ("原始内容" in l and l.strip().startswith("\\part")))
    ob = next(i for i, l in enumerate(lb) if ("原始内容" in l and l.strip().startswith("\\part")))
    print("%s  CRLF %d→%d ; 行 %d→%d" % (fn, ca_, cb_, len(la), len(lb)))
    print("  锚点前逐字一致 :", la[:ia + 1] == lb[:ib + 1])
    print("  原始内容区逐字一致 :", la[oa:] == lb[ob:])
    ok &= (la[:ia + 1] == lb[:ib + 1]) and (la[oa:] == lb[ob:])

print("\n总体：", "全部通过 ✓" if ok else "存在失败 ✗")
