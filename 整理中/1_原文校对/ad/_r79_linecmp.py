# -*- coding: utf-8 -*-
"""行级比对：r77 原版有而用户新版没有的正文行（用户删除/改写的内容）。"""
import io, re, collections

def load_lines(fn):
    raw = io.open(fn, encoding="utf-8", newline="").read()
    out = []
    for ln in raw.split("\n"):
        s = re.sub(r"\s+", "", ln.rstrip("\r"))
        if not s or s.startswith("%"):
            continue
        if re.match(r"^\\(part|chapter|section|subsection|subsubsection)\*?\{", ln.rstrip("\r")):
            continue  # 标题行单独统计
        out.append(s)
    return out

A = load_lines("position_r77.tex")
B = load_lines("3_position.tex")
ca, cb = collections.Counter(A), collections.Counter(B)
miss = ca - cb          # r77 有、新版没有（被删或改写）
gain = cb - ca          # 新版新增
print("r77 正文行 %d；新版正文行 %d" % (sum(ca.values()), sum(cb.values())))
print("新版缺少的 r77 行: %d 种 / %d 行" % (len(miss), sum(miss.values())))
print("新版新增行: %d 种 / %d 行" % (len(gain), sum(gain.values())))
print()
print("=== 新版缺少的行（按长度降序，前 40 条）===")
for s in sorted(miss, key=len, reverse=True)[:40]:
    print("  -(%d) %s" % (len(s), s[:150]))
print()
print("=== 新版新增的行（按长度降序，前 30 条）===")
for s in sorted(gain, key=len, reverse=True)[:30]:
    print("  +(%d) %s" % (len(s), s[:150]))
