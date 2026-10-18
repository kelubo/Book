# -*- coding: utf-8 -*-
"""r80 四卷全面静态体检"""
import io, re, sys, collections

FILES = ["0_book.tex", "1_male.tex", "2_female.tex", "3_position.tex"]
AD = "D:/Git/Book/整理中/1_原文校对/ad/"

def read(fn):
    raw = io.open(AD + fn, encoding="utf-8", newline="").read()
    lines = [x.rstrip("\r") for x in raw.split("\n")]
    return raw, lines

def nocomment(lines):
    return [re.sub(r"(?<!\\)%.*$", "", x) for x in lines]

def block_end(lines, i, level):
    """i 指向标题行(0-based)，返回块尾(不含)。level: chapter/section"""
    order = {"part": 0, "chapter": 1, "section": 2, "subsection": 3, "subsubsection": 4}
    for j in range(i + 1, len(lines)):
        m = re.match(r"^\\(part|chapter|section|subsection)\*?\{", lines[j])
        if m and order[m.group(1)] <= order[level]:
            return j
    return len(lines)

def body_lines(lines, a, b):
    """统计 (a,b) 区间内的非空、非注释、非标题行"""
    n = 0
    for x in lines[a:b]:
        s = x.strip()
        if not s or s.startswith("%"):
            continue
        if re.match(r"^\\(part|chapter|section|subsection|subsubsection)\*?\{", s):
            continue
        n += 1
    return n

print("=" * 70)
for fn in FILES:
    raw, lines = read(fn)
    NC = nocomment(lines)
    text = "\n".join(NC)
    print("### %s (%d 行)" % (fn, len(lines)))
    issues = []

    # 1. 花括号
    d = text.count("{") - text.count("}")
    if d != 0:
        issues.append("花括号 delta=%d" % d)

    # 2. 环境配对
    envs = collections.Counter()
    for m in re.finditer(r"\\(begin|end)\{([^}]*)\}", text):
        envs[m.group(2)] += 1 if m.group(1) == "begin" else -1
    bad = {k: v for k, v in envs.items() if v != 0}
    if bad:
        issues.append("环境不配对: %s" % bad)

    # 3. old 残留
    olds = [(i + 1, x.strip()) for i, x in enumerate(lines)
            if re.match(r"^\\(?:sub)*section\{old\}\s*$", x)
            or re.match(r"^\\(?:sub)*section\{Old\}\s*$", x)]
    if olds:
        issues.append("old 残留 %d 处: %s" % (len(olds), [o[0] for o in olds]))

    # 4. U+FFFD / **
    if "\ufffd" in raw:
        issues.append("含 U+FFFD 乱码")
    n_star = len(re.findall(r"\*\*", raw))
    if n_star:
        issues.append("** 出现 %d 次" % n_star)

    # 5. 标题未转义 &
    amp = []
    for i, x in enumerate(lines):
        s = x.strip()
        if s.startswith("%"):
            continue
        m = re.match(r"^\\(?:part|chapter|section|subsection|subsubsection)\*?\{", s)
        if m and re.search(r"(?<!\\)&", s):
            amp.append(i + 1)
    if amp:
        issues.append("标题未转义&: %s" % amp)

    # 6. 结构统计 + 空壳章/节
    parts, chaps = [], []
    empty_ch, empty_sec = [], []
    cur_part = None
    sec_of_ch = 0
    i = 0
    n_ch = n_sec = n_sub = 0
    while i < len(lines):
        m = re.match(r"^\\part\*?\{([^}]*)\}", lines[i])
        if m and not lines[i].lstrip().startswith("%"):
            cur_part = m.group(1)
            parts.append(cur_part)
        m2 = re.match(r"^\\chapter\*?\{([^}]*)\}", lines[i])
        if m2 and not lines[i].lstrip().startswith("%"):
            chaps.append((i + 1, m2.group(1), cur_part))
            n_ch += 1
        if re.match(r"^\\section\*?\{", lines[i]) and not lines[i].lstrip().startswith("%"):
            n_sec += 1
        if re.match(r"^\\subsection\*?\{", lines[i]) and not lines[i].lstrip().startswith("%"):
            n_sub += 1
        i += 1
    # 章体量
    chinfo = []
    for k, (ln, title, pt) in enumerate(chaps):
        a = ln - 1
        b = chaps[k + 1][0] - 1 if k + 1 < len(chaps) else len(lines)
        # 章边界被 part 打断的情况：忽略，粗略即可
        nb = body_lines(lines, a, b)
        chinfo.append((ln, title, pt, nb))
        if nb < 3:
            empty_ch.append((ln, title, nb))
    if empty_ch:
        issues.append("空壳章(<3行正文): %s" % [(l, t) for l, t, _ in empty_ch])

    # 7. 章级重名（本文件内）
    cnt = collections.Counter(t for _, t, _, _ in chinfo)
    dup = {t: c for t, c in cnt.items() if c > 1}
    if dup:
        issues.append("章级重名: %s" % dup)

    # 8. \part 清单
    print("  part(%d): %s" % (len(parts), " | ".join(parts)))
    print("  chapter=%d section=%d subsection=%d" % (n_ch, n_sec, n_sub))
    if issues:
        for x in issues:
            print("  [问题] " + x)
    else:
        print("  [OK] 无静态问题")
    print("-" * 70)
