# -*- coding: utf-8 -*-
r"""r74z 骨架完整性审查：检查插错章的正文块。

原理：
  1) 扫描 book.tex 骨架区（到 \part{old} 为止），记录每个 \subsection 的行号与所属章。
  2) 逐条内容块检查「首个非空行是否紧跟锚行」——若有空行再出现内容，说明锚行后无正文但
     下面有孤块（错位）。
  3) 更强判定：把每段正文的「章归属」与其锚点位置比对——凡是某小节下方的内容块，
     如果其首行紧接的锚行不是它自己的标题，即报错。
简化实现：找出所有「\subsection 行之后没有紧接着非空内容行，但紧随几个空行后出现正文」
的情况，以及「\subsection 行后直接是正文，但该正文实际属于别处」——
真正可靠的检测方式：统计连续两个 \subsection 之间内容块的归属是否合理。
本脚本采用：列出所有「\subsection 之后第 1~3 行内即出现正文」的槽位，
  以及所有「\subsection 之后只有空行、随后出现正文但该段正文的锚点是更早的小节」。
"""
import io, re, sys

PATH = "book.tex"
raw = io.open(PATH, encoding="utf-8", newline="").read()
lines = raw.split("\n")

old_idx = next(i for i, l in enumerate(lines) if l.strip() == "\\part{old}")
skel = lines[:old_idx]

hdr = re.compile(r"^(\\part|\\chapter|\\section|\\subsection)\*?\{")
marks = []  # (idx, level, title)
for i, l in enumerate(skel):
    m = hdr.match(l)
    if m:
        lvl = m.group(1)
        t = l[len(lvl):].strip()
        if t.startswith("*"):
            t = t[1:]
        t = t.strip("{}")
        marks.append((i, lvl, t))

# 建立每个 mark 的所属章
cur_chap = None
own = {}
for idx, lvl, t in marks:
    if lvl == "\\chapter":
        cur_chap = t
    own[idx] = (lvl, t, cur_chap)

# 找出每个 \subsection 的内容区间
subs = [(idx, t, own[idx][2]) for idx, lvl, t in marks if lvl == "\\subsection"]
anchor_set = set(idx for idx, _, _ in marks)

problems = []
for k, (idx, title, chap) in enumerate(subs):
    # 找下一个任何层级的锚行（同为标题的行）
    nxt = None
    for j in range(idx + 1, len(skel)):
        if j in anchor_set:
            nxt = j
            break
    end = nxt if nxt is not None else len(skel)
    body = [j for j in range(idx + 1, end) if skel[j].strip() and not skel[j].lstrip().startswith("%")]
    if not body:
        continue
    # 内容块：连续的正文行段（中间可含空行）
    # 找出所有「正文块」的起点
    starts = []
    prev_blank = True
    for j in range(idx + 1, end):
        s = skel[j].strip()
        if not s or s.startswith("%"):
            prev_blank = True
            continue
        if prev_blank:
            starts.append(j)
        prev_blank = False
    if not starts:
        continue
    first = starts[0]
    # 判定：若首块起点紧跟锚行（idx+1），正常
    gap = first - idx - 1
    blanks_between = gap
    if gap > 1:
        problems.append(("LEAD_GAP", chap, title, idx + 1, first + 1, blanks_between))

# ========== 检测 2：内容块归属错位（核心）==========
# 原理：每个内容块（连续正文，中间可有空行但不超过 1 行间隔）只能属于其上方最近的
# 骨架标题。若发现某个 \subsection 与下一个骨架标题之间，存在【两个以上】由「>1 行间隔」
# 分隔的正文块，说明有多块内容堆在同一槽位下 —— 极度可疑。
susp = []
for k, (idx, title, chap) in enumerate(subs):
    nxt = None
    for j in range(idx + 1, len(skel)):
        if j in anchor_set:
            nxt = j
            break
    end = nxt if nxt is not None else len(skel)
    blocks = 0
    prev_blank = False
    for j in range(idx + 1, end):
        s = skel[j].strip()
        if not s or s.startswith("%"):
            prev_blank = True
            continue
        if prev_blank and blocks > 0:
            blocks += 1   # 新块
            prev_blank = False
            continue
        if blocks == 0:
            blocks = 1
        prev_blank = False
    if blocks >= 2:
        susp.append((chap, title, idx + 1, end, blocks))

print()
print("== 槽位内出现多个正文块（>=2）的可疑槽位 ==")
print("数量 =", len(susp))
for chap, title, anch, end, n in susp:
    print("  章=%s | 小节=%s | L%d~L%d | 块数=%d" % (chap, title, anch, end, n))

# ========== 检测 3：内容中出现的检验点 ==========
print()
print("== 检测 3：特定内容归属 ==")
targets = ["滴虫感染与性传播感染风险的关联", "监狱环境中的性行为", "帕金森", "伴侣告知"]
for t in targets:
    hits = [i + 1 for i, l in enumerate(lines) if l.startswith(t)]
    print("  '%s' 首行出现于 L%s" % (t, hits[:5]))

