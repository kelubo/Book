# -*- coding: utf-8 -*-
"""r77: 定位提取块中的环境不配平。"""
import io, re
import _r77_plan as P

H = re.compile(r"^\\(part|chapter|section|subsection|subsubsection)\*?\{(.*)\}\s*$")
lines = io.open("book.tex", encoding="utf-8", newline="").read().split("\n")

BA, BB = 59372, 66080
toks = []
for i in range(BA - 1, BB):
    m = H.match(lines[i])
    if m:
        toks.append((i, m.group(1), m.group(2).strip()))
toks.append((BB, None, None))
BIGPOS = {}
for k in range(len(toks) - 1):
    i, lvl, t = toks[k]
    if lvl == "subsection":
        BIGPOS[t] = (i + 1, toks[k + 1][0])

def bal(blk):
    b = len(re.findall(r"\\begin\{itemize\}", "\n".join(blk)))
    e = len(re.findall(r"\\end\{itemize\}", "\n".join(blk)))
    return b, e

def check(region, a, b, lab):
    lo, hi = P.REGION[region]
    blk = lines[a - 1:b - 1]
    b1, e1 = bal(blk)
    if b1 != e1:
        print("!! %-8s %s  L%d~L%d  itemize %d/%d 差 %+d" % (region, lab, a, b, b1, e1, b1 - e1))
        # 列出块内最后 6 行
        for x in blk[-6:]:
            print("        |", x[:100])
        # 若右端点刚好是下一个标题，检查它是否属于本块
        return True
    return False

print("=== 逐块检查 ===")
bad = 0
for part, chaps in P.STRUCT:
    for ctitle, blocks in chaps:
        for spec in blocks:
            if spec[0] == "BIGPOS":
                for t in sorted(P.BIG_POS[spec[1]], key=lambda t: BIGPOS[t][0]):
                    a, b = BIGPOS[t]
                    if check("BIG", a, b, t):
                        bad += 1
            else:
                if check(spec[0], spec[1], spec[2], ctitle):
                    bad += 1
print("不配平块数 =", bad)

# 顺带：整段 S/P4/BIG 的 itemize 平衡情况（判断是源就坏了，还是被切坏）
for r, (lo, hi) in P.REGION.items():
    blk = lines[lo - 1:hi]
    b1, e1 = bal(blk)
    print("区 %-4s 全段 itemize %d/%d 差 %+d" % (r, b1, e1, b1 - e1))
