# -*- coding: utf-8 -*-
"""r81b：检查 male/female 停用框架区内容 vs 当前编译区的重合度（判断是否独有知识点）"""
import io, re, sys

AD = "D:/Git/Book/整理中/1_原文校对/ad/"

def read(fn):
    raw = io.open(AD + fn, encoding="utf-8", newline="").read()
    return [x.rstrip("\r") for x in raw.split("\n")]

def pnorm(s):
    return re.sub(r"[\s\u3000\u00a0]+", "", s.strip())

TITLE = re.compile(r"^\\(part|chapter|section|subsection|subsubsection)\*?\{")

def content_lines(lines, a, b):
    out = []
    for i in range(a, b):
        s = lines[i].strip()
        if not s or s.startswith("%"):
            continue
        if TITLE.match(s):
            continue
        t = pnorm(s)
        if len(t) < 12:
            continue
        out.append((i, s))
    return out

def analyze(fn, flag, dcfind):
    lines = read(fn)
    # 找 flag 块
    i_if = i_else = i_fi = None
    for i, x in enumerate(lines):
        if re.match(r"^\s*\\if" + flag, x):
            i_if = i
        elif i_if is not None and i_else is None and x.strip().startswith("\\else"):
            i_else = i
        elif i_if is not None and re.match(r"^\s*\\fi\b", x):
            i_fi = i
            break
    # 找编译区（最后一个 \documentclass）
    dc = None
    for i, x in enumerate(lines):
        if "\\documentclass" in x:
            dc = i
    print("=" * 74)
    print("### %s  总行 %d" % (fn, len(lines)))
    print("    if=%s else=%s fi=%s  documentclass=%s" % (
        i_if + 1 if i_if is not None else None,
        i_else + 1 if i_else is not None else None,
        i_fi + 1 if i_fi is not None else None,
        dc + 1 if dc is not None else None))
    if i_if is None or i_else is None or i_fi is None:
        print("    [无停用框架区]")
        return
    fw = content_lines(lines, i_else + 1, i_fi)
    comp = content_lines(lines, dc, len(lines))
    fw_set = {}
    for i, s in fw:
        fw_set.setdefault(pnorm(s), i + 1)
    comp_set = set(pnorm(s) for _, s in comp)
    hit = [t for t in fw_set if t in comp_set]
    miss = [t for t in fw_set if t not in comp_set]
    print("    框架区正文行(去空白>=12字) %d 条 / 唯一 %d 条  编译区 %d 条 / 唯一 %d 条"
          % (len(fw), len(fw_set), len(comp), len(comp_set)))
    print("    框架区唯一行在编译区命中 %d 条 → 覆盖率 %.1f%%"
          % (len(hit), 100.0 * len(hit) / max(1, len(fw_set))))
    print("    框架区独有 %d 条" % len(miss))
    return lines, i_else, i_fi, miss, fw_set

for fn, flag in (("1_male.tex", "skipmaleframework"), ("2_female.tex", "skipfemaleframework")):
    r = analyze(fn, flag, None)
    if not r:
        continue
    lines, i_else, i_fi, miss, fw_set = r
    # 按所在 section 归组统计独有行
    if miss:
        # 建立行号→所属 section
        cur_part = cur_ch = cur_sec = ""
        owner = {}
        for i in range(i_else + 1, i_fi):
            s = lines[i].strip()
            m = re.match(r"^\\part\*?\{([^}]*)\}", s)
            if m: cur_part = m.group(1)
            m = re.match(r"^\\chapter\*?\{([^}]*)\}", s)
            if m: cur_ch = m.group(1)
            m = re.match(r"^\\section\*?\{([^}]*)\}", s)
            if m: cur_sec = m.group(1)
            if pnorm(s) in fw_set:
                owner[fw_set[pnorm(s)]] = (cur_part, cur_ch, cur_sec)
        import collections
        g = collections.Counter()
        for t in miss:
            ln = fw_set[t]
            g[" / ".join(owner.get(ln, ("?", "?", "?")))] += 1
        print("    ── 独有行分布（按 篇/章/节）──")
        for k, v in g.most_common(40):
            print("       %4d  %s" % (v, k))
