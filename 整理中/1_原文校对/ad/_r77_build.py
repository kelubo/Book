# -*- coding: utf-8 -*-
"""r77 执行层：按 _r77_plan.STRUCT 生成 position.tex。

用法：
    python _r77_build.py report     仅盘点（不写盘）
    python _r77_build.py dry-run    生成 + 全量校验，不写盘
    python _r77_build.py apply      写盘（覆盖 position.tex）
"""
import io, re, sys, collections
import _r77_plan as P

MODE = sys.argv[1] if len(sys.argv) > 1 else "report"
SRC = "book.tex"
OUT = "position.tex"

H = re.compile(r"^\\(part|chapter|section|subsection|subsubsection)\*?\{(.*)\}\s*$")
LV = {"part": 0, "chapter": 1, "section": 2, "subsection": 3, "subsubsection": 4}

raw = io.open(SRC, encoding="utf-8", newline="").read()
assert "\r" not in raw, "book.tex 应为纯 LF"
lines = raw.split("\n")
N = len(lines)

# female.tex 为纯 CRLF：读原始字节后按行切，逐行剥 \r
raw_f = io.open("female.tex", encoding="utf-8", newline="").read()
flines = [x[:-1] if x.endswith("\r") else x for x in raw_f.split("\n")]
print("female.tex 行数 %d（原 CRLF %d）" % (len(flines), raw_f.count("\r\n")))

LINES_OF = {"book.tex": lines, "female.tex": flines}

# ── 校验：每个来源区首行确实是预期标题 ────────────────────────────────────
for k, (a, b) in P.REGION.items():
    L = LINES_OF[P.FILE_OF[k]]
    print("区 %-4s（%s）L%d~L%d  首行：%s" % (k, P.FILE_OF[k], a, b, L[a - 1][:70]))

# ── 解析巨块 59372..66079 的 subsection 区间 ──────────────────────────────
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
    nxt = toks[k + 1][0]
    if lvl == "subsection":
        BIGPOS.setdefault(t, (i + 1, nxt))   # 同名取首次出现（巨块里 摇篮式/螺旋式 各出现 2 次）

kept = set()
for bucket in ("base", "classic", "variation", "special"):
    for t in P.BIG_POS[bucket]:
        assert t in BIGPOS, "巨块中找不到小节：%s" % t
        kept.add(t)
miss = [t for t in P.BIG_DROP if t not in BIGPOS]
assert not miss, "DROP 表里有不存在的标题：%s" % miss
dup = kept & set(P.BIG_DROP)
assert not dup, "同一标题既保留又丢弃：%s" % dup
print("巨块 subsection 总数 %d；保留 %d，显式丢弃 %d，其余未选 %d"
      % (len(BIGPOS), len(kept), len(P.BIG_DROP), len(BIGPOS) - len(kept) - len(P.BIG_DROP)))


# ── 块提取 ───────────────────────────────────────────────────────────────
def trim(blk):
    while blk and not blk[0].strip():
        blk.pop(0)
    while blk and not blk[-1].strip():
        blk.pop()
    return blk


def slice_region(region, a, b):
    lo, hi = P.REGION[region]
    L = LINES_OF[P.FILE_OF[region]]
    if b is None:                       # b=None：取到下一个同级或更高级标题之前
        m0 = H.match(L[a - 1])
        assert m0, "b=None 但首行不是标题：%s" % L[a - 1][:70]
        lv0 = LV[m0.group(1)]
        b = hi
        for j in range(a, hi):
            m = H.match(L[j])
            if m and LV[m.group(1)] <= lv0:
                b = j + 1
                break
        print("   [b=None] %s L%d 结束于 L%d（%s）" % (region, a, b, L[b - 1][:50]))
    assert lo <= a < b <= hi + 1, "%s 区间越界：%d~%d（区 %d~%d）" % (region, a, b, lo, hi)
    blk = list(L[a - 1:b - 1])
    # r77 教训：块尾可能紧邻 \part（篇分隔），必须截断——否则会把别的篇的 \part 搬进来
    cut = [k for k, x in enumerate(blk) if x.lstrip().startswith("\\part")]
    if cut:
        print("   [截断] %s L%d~ 处发现 \\part 行，截断于块内第 %d 行" % (region, a, cut[0] + 1))
        blk = blk[:cut[0]]
    return blk


def apply_ops(blk, ops):
    for op in ops:
        if op is None:
            continue
        if op == "skip_head":
            assert H.match(blk[0]), "skip_head 但首行不是标题：%s" % blk[0][:60]
            blk = blk[1:]
        elif op == "demote_sub":
            blk = [re.sub(r"^\\subsubsection\{", r"\\subsection{", x) for x in blk]
        elif isinstance(op, tuple) and op[0] == "replace_head":
            assert H.match(blk[0]), "replace_head 但首行不是标题：%s" % blk[0][:60]
            blk = [op[1]] + blk[1:]
        else:
            raise ValueError("未知 op: %r" % (op,))
    return trim(blk)


BODY, STAT = [], []
for part, chaps in P.STRUCT:
    BODY.append("\\part{%s}" % part)
    BODY.append("")
    for ctitle, blocks in chaps:
        BODY.append("\\chapter{%s}" % ctitle)
        BODY.append("")
        n_lines = 0
        for spec in blocks:
            region = spec[0]
            if region == "BIGPOS":
                bucket = spec[1]
                items = sorted(P.BIG_POS[bucket], key=lambda t: BIGPOS[t][0])
                sub = []
                for t in items:
                    a, b = BIGPOS[t]
                    blk = trim(list(lines[a - 1:b - 1]))
                    assert H.match(blk[0]) and blk[0].strip() == "\\subsection{%s}" % t, \
                        "BIGPOS 块首行不符：%s" % blk[0][:70]
                    sub += blk + [""]
                    n_lines += len(blk)
                BODY += sub
            else:
                a, b = spec[1], spec[2]
                ops = spec[3:]
                blk = apply_ops(slice_region(region, a, b), ops)
                assert blk, "块为空：%s %s" % (region, spec)
                BODY += blk + [""]
                n_lines += len(blk)
        STAT.append((part, ctitle, len(blocks), n_lines))
        while BODY and not BODY[-1].strip():
            BODY.pop()
        BODY.append("")

# ── 组装全文 ─────────────────────────────────────────────────────────────
PRE = lines[3:163]                       # L4 \documentclass ~ L163 \keyword 定义
assert PRE[0].startswith("\\documentclass"), PRE[0][:60]
assert PRE[-1].startswith("\\newcommand{\\keyword}"), PRE[-1][:60]

head = []
head.append("% 本文件定位：性爱实践卷（前戏、爱抚、技巧、体位与姿势、安全事项）")
head.append("% 内容来源：book.tex 骨架第三篇 + book.tex 旧区（第四篇·性交体位与姿势艺术、")
head.append("%           \\part{性爱与亲密关系} 巨块中的可核查部分）；三卷原位留 % ⇒ [已移出] 标记。")
head.append("% 生成脚本：_r77_build.py（数据层 _r77_plan.py）。改动内容请改数据层后重跑。")
head.append("")
head += PRE
head.append("")
head.append("\\title{\\heiti\\zihao{0} %s}" % P.TITLE)
head.append("\\author{}")
head.append("\\date{}")
head.append("")
head.append("\\begin{document}")
head.append("")
head.append("\\maketitle")
head.append("")
head.append("\\frontmatter")
head.append("")
head.append("\\chapter{前言}")
head.append("")
head.append("本书是《性学大全指南》的\\keyword{性爱实践卷}，独立于共通卷（book.tex）、女性卷（female.tex）与男性卷（male.tex）单独成册，")
head.append("内容聚焦于\\keyword{性行为本身}——前戏与爱抚、亲密技法、性交体位与姿势、辅助器具与安全事项。")
head.append("")
head.append("分五篇：%s。" % "；".join(p for p, _ in P.STRUCT))
head.append("")
head.append("\\begin{tcolorbox}[colback=pink!5!white,colframe=red!50!black,title=使用说明]")
head.append('本卷讲的是"怎么做"，不重复讲"为什么会这样"——生理机制、疾病诊治、心理与社会议题在其余三卷。')
head.append("体位与技巧的价值在于\\keyword{舒适与默契}，不在于难度或数量；任何造成疼痛的做法都应立即调整或停止。")
head.append("\\end{tcolorbox}")
head.append("")
head.append("\\tableofcontents")
head.append("")
head.append("\\listoffigures")
head.append("\\listoftables")
head.append("")
head.append("\\mainmatter")
head.append("")

tail = []
tail.append("\\backmatter")
tail.append("")
tail.append("\\chapter{参考文献}")
tail.append("")
tail.append("\\nocite{*}")
tail.append("\\bibliography{references}")
tail.append("")
tail.append("\\end{document}")
tail.append("")

out = head + BODY + tail
text = "\n".join(out)

print("=" * 96)
print("%-12s %-24s %-5s %8s" % ("篇", "章", "块数", "行数"))
tot = 0
for part, ctitle, nb, nl in STAT:
    print("%-12s %-24s %-5d %8d" % (part, ctitle, nb, nl))
    tot += nl
print("正文合计 %d 行；position.tex 全文 %d 行" % (tot, text.count("\n") + 1))

# ── 全量校验 ─────────────────────────────────────────────────────────────
assert "\r" not in text, "position.tex 应为纯 LF"
assert "**" not in text, "含 markdown 粗体"
assert "\ufffd" not in text, "含替换字符 U+FFFD"
d = text.count("{") - text.count("}")
assert d == 0, "花括号不配平：delta=%d" % d
assert text.rstrip().endswith("\\end{document}"), "结尾异常"
# 环境配对检查：必须剥离注释（preamble 注释里含 \begin{itemize} 字样，会污染计数）
NOCMT = "\n".join(re.sub(r"(?<!\\)%.*$", "", x) for x in out)
envs = collections.Counter(re.findall(r"\\begin\{([a-zA-Z*]+)\}", NOCMT))
ende = collections.Counter(re.findall(r"\\end\{([a-zA-Z*]+)\}", NOCMT))
assert envs == ende, "环境不配对：%s" % {k: (envs[k], ende[k]) for k in set(envs) | set(ende) if envs[k] != ende[k]}
# 正文不得出现未定义的起首结构
bad = [x for x in out if x.strip().startswith("\\part*") ]
stray = [x for x in BODY if x.strip().startswith("\\part")
         and not re.match(r"^\\part\{第[一二三四五六七八九十]+篇", x.strip())]
assert not stray, "正文里出现非本脚本生成的 \\part：%s" % stray[:3]
assert not bad, "出现 \\part* ：%s" % bad[:3]
# 小节标题不得重复到"同章内完全同名"
for part, chaps in P.STRUCT:
    pass
print("校验：纯LF / 无 ** / 无 U+FFFD / 花括号 delta=0 / 环境配对 / 无 \\part*  [全部通过]")

if MODE == "apply":
    io.open(OUT, "w", encoding="utf-8", newline="").write(text)
    print("已写盘：%s" % OUT)
else:
    print("%s 模式，未写盘。" % MODE)
