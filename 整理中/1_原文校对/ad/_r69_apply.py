# -*- coding: utf-8 -*-
"""r69：按用户选定的"全量"方案重构 book.tex 前置目录骨架。

改动（只动标题行与注释，绝不触碰正文与旧区）：
  1) 删除重复的旧"使用说明"注释块（L157-167，仍写"九篇 53 章"）
  2) 更新说明注释：八篇 51 章 -> 八篇 58 章（另设附录）
  3) 消 4 处重名节（性取向 / 常见性偏好 / 男性性欲低下 / 女性性欲低下）
  4) 唯一零节章「性健康误区与真相」补 3 节
  5) 新增 7 章（补缺口模块）
  6) 为 213 个零小节的节补学习要点小节
  7) 「结语」独立成篇

用法：python _r69_apply.py [preview|apply]
"""
import io, os, re, sys, importlib.util

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
P = os.path.join(BASE, "book.tex")


def load_mod(name, fn):
    sp = importlib.util.spec_from_file_location(name, os.path.join(BASE, fn))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


d1 = load_mod("d1", "_r69_data1.py")
d2 = load_mod("d2", "_r69_data2.py")
d3 = load_mod("d3", "_r69_data3.py")
d4 = load_mod("d4", "_r69_data4.py")
d5 = load_mod("d5", "_r69_data5.py")

SUBS = {}
for d in (d1.D1, d2.D2, d3.D3, d4.D4, d5.D5):
    for ch, secs in d.items():
        assert ch not in SUBS, "章重复: " + ch
        SUBS[ch] = dict(secs)

FIX_SECTIONS = d5.FIX_SECTIONS
RENAMES = d5.RENAMES
NEW_CHAPTERS = d5.NEW_CHAPTERS

raw = io.open(P, "rb").read()
nl = "\r\n" if raw.count(b"\r\n") > 0 else "\n"
lines = raw.decode("utf-8").replace("\r\n", "\n").split("\n")
N = len(lines)
print("载入 %d 行，换行=%s" % (N, "CRLF" if nl == "\r\n" else "LF"))

H = re.compile(r"^\s*\\(part|chapter|section|subsection|subsubsection)\*?\{")
LV = {"part": 0, "chapter": 1, "section": 2, "subsection": 3, "subsubsection": 4}


def gt(s):
    r = s[s.index("{"):]
    dep = 0
    for j, c in enumerate(r):
        if c == "{":
            dep += 1
        elif c == "}":
            dep -= 1
            if dep == 0:
                return r[1:j]
    return r[1:]


def qn(s):
    """引号归一化"""
    return s.replace("\u201c", '"').replace("\u201d", '"').replace("\u2018", "'").replace("\u2019", "'")


heads = []  # (idx0, level, title, rawline)
for i, l in enumerate(lines):
    s = l.strip()
    if not s or s.startswith("%"):
        continue
    m = H.match(s)
    if m:
        heads.append((i, m.group(1), gt(s)))

OLD = next(i for i, lv, t in heads if lv == "part" and t == "old")
SK = [(i, lv, t) for i, lv, t in heads if i < OLD]
print("骨架区标题 %d 个；旧区起点 L%d" % (len(SK), OLD + 1))

# 章的上下文
chap_of = {}
cur = None
for i, lv, t in SK:
    if lv == "chapter":
        cur = t
    chap_of[i] = cur

ops = []  # (start, end_exclusive, newlines, desc)


def add(a, b, nl_, desc):
    ops.append((a, b, nl_, desc))


# ── 1) 删重复说明块 ─────────────────────────────────────────
us = [i for i, l in enumerate(lines[:OLD]) if l.strip() == "% 使用说明："]
assert len(us) == 2, "使用说明块数 = %d（预期 2）" % len(us)
start = us[1]
end = None
for i in range(start, OLD):
    if re.match(r"^%\s*═{10,}\s*$", lines[i]):
        end = i
        break
assert end, "未找到旧说明块结尾"
add(start, end + 1, [], "删除重复说明块 L%d-L%d" % (start + 1, end + 1))

# ── 2) 更新说明正文 ─────────────────────────────────────────
tgt = [i for i, l in enumerate(lines[:OLD]) if "共八篇 51 章" in l]
assert len(tgt) == 1, "未找到「共八篇 51 章」"
add(tgt[0], tgt[0] + 1,
    ["%   1. 本结构为全书按主题去重后的目标目录，共八篇 58 章，另有独立的「结语」与「附录」两篇。",
     "%      篇 / 章 / 节 / 小节四层，小节即该节的学习要点，可直接作为写作或迁移的提纲。"],
    "更新说明第 1 条")

# ── 3) 消重名节 ────────────────────────────────────────────
for ch, oldt, newt in RENAMES:
    hit = [i for i, lv, t in SK if lv == "section" and qn(t) == qn(oldt) and chap_of.get(i) == ch]
    assert len(hit) == 1, "重命名锚不唯一: %s / %s -> %d" % (ch, oldt, len(hit))
    i = hit[0]
    add(i, i + 1, ["\\section{%s}" % newt], "重命名 %s：%s -> %s" % (ch, oldt, newt))

# ── 4) 零节章补节 ──────────────────────────────────────────
for ch, secs in FIX_SECTIONS.items():
    ci = [i for i, lv, t in SK if lv == "chapter" and t == ch]
    assert len(ci) == 1, "章锚不唯一: " + ch
    i = ci[0] + 1
    while i < N and lines[i].strip().startswith("%"):
        i += 1
    blk = [""]
    for sn, subs in secs:
        blk.append("\\section{%s}" % sn)
        for u in subs:
            blk.append("\\subsection{%s}" % u)
    add(i, i, blk, "补节 「%s」 %d 节" % (ch, len(secs)))

# ── 5) 新增章 ──────────────────────────────────────────────
for part, before, name, secs in NEW_CHAPTERS:
    if before is None:
        parts = [i for i, lv, t in SK if lv == "part"]
        nxt = [i for i in parts if i > [j for j, lv, t in SK if lv == "part" and t == part][0]]
        assert nxt, "篇后无下一个 part: " + part
        at = nxt[0]
    else:
        hit = [i for i, lv, t in SK if lv == "chapter" and t == before]
        assert len(hit) == 1, "插章锚不唯一: " + before
        at = hit[0]
    blk = ["\\chapter{%s}" % name, "% [框架] 2026-09-21 新增：补齐知识框架缺口模块。"]
    for sn, subs in secs:
        blk.append("\\section{%s}" % sn)
        for u in subs:
            blk.append("\\subsection{%s}" % u)
    blk.append("")
    add(at, at, blk, "新增章 「%s」 %d 节（插在「%s」前）" % (name, len(secs), before or "篇末"))

# ── 6) 补小节 ──────────────────────────────────────────────
done = set()
nsub = 0
for i, lv, t in SK:
    if lv != "section":
        continue
    ch = chap_of.get(i)
    if ch not in SUBS:
        continue
    key = None
    for k in SUBS[ch]:
        if qn(k) == qn(t):
            key = k
            break
    if key is None:
        continue
    # 已有小节则跳过
    j = i + 1
    has = False
    while j < N:
        s = lines[j].strip()
        if not s or s.startswith("%"):
            j += 1
            continue
        if H.match(s) and LV[H.match(s).group(1)] > 2:
            has = True
        break
    if has:
        continue
    j = i + 1
    while j < N and lines[j].strip().startswith("%"):
        j += 1
    subs = SUBS[ch][key]
    add(j, j, ["\\subsection{%s}" % u for u in subs], "补小节 %s / %s (%d)" % (ch, t, len(subs)))
    done.add((ch, key))
    nsub += len(subs)

# 覆盖率检查
missing = []
for ch, secs in SUBS.items():
    for s in secs:
        if (ch, s) not in done:
            missing.append(ch + " / " + s)
print("补小节：%d 个节，%d 条小节" % (len(done), nsub))
if missing:
    print("!! 未命中（可能已有小节或不在骨架）：")
    for m in missing:
        print("   ", m)

# ── 7) 结语独立成篇 ────────────────────────────────────────
jie = [i for i, lv, t in SK if lv == "chapter" and t == "结语"]
assert len(jie) == 1
add(jie[0], jie[0], ["\\part{结语}", ""], "结语独立成篇")

# ── 应用（自下而上）────────────────────────────────────────
ops.sort(key=lambda x: -x[0])
out = list(lines)
for a, b, blk, desc in ops:
    out[a:b] = blk
print("\n共 %d 项编辑；行数 %d -> %d（%+d）" % (len(ops), N, len(out), len(out) - N))

# ── 校验 ───────────────────────────────────────────────────
old_tail_a = lines[OLD:]
old_tail_b = out[len(out) - len(old_tail_a):]
assert old_tail_a == old_tail_b, "旧区被改动！"


def braces(ls):
    n = 0
    for l in ls:
        s = l.strip()
        if s.startswith("%"):
            continue
        n += s.count("{") - s.count("}")
    return n


ba, bb = braces(lines), braces(out)
print("花括号净值 %d -> %d（差 %d）" % (ba, bb, bb - ba))
assert bb >= ba, "花括号净值下降"
# 旧区逐字一致（自 old 起）
print("旧区逐字一致：是")

mode = sys.argv[1] if len(sys.argv) > 1 else "dry"
if mode == "preview":
    io.open(os.path.join(BASE, "_r69_preview.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
    print("已写预览 _r69_preview.txt")
elif mode == "apply":
    io.open(P, "wb").write(nl.join(out).encode("utf-8"))
    print("已落盘。")
else:
    print("[dry-run] 未写盘。")
