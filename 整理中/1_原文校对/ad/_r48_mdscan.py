# -*- coding: utf-8 -*-
"""统计三卷行内 ** 残留、奇偶检查、其他 markdown 痕迹"""
import io, re, os

BASE = os.path.dirname(os.path.abspath(__file__))
for fn in ("book.tex", "female.tex", "male.tex"):
    raw = io.open(os.path.join(BASE, fn), encoding="utf-8", newline="").read().replace("\r\n", "\n")
    lines = raw.split("\n")
    hits = [(i, ln) for i, ln in enumerate(lines, 1) if "**" in ln and not ln.strip().startswith("%")]
    # 每行 ** 出现次数应为偶数
    odd = [(i, ln[:80]) for i, ln in hits if ln.count("**") % 2 != 0]
    print("%-12s **行数=%d  奇数行=%d" % (fn, len(hits), len(odd)))
    for i, s in odd:
        print("  奇数 L%d: %s" % (i, s))
    # 其他 markdown 痕迹（非注释行）：行首 '- '、反引号、行内单个 *
    bt = [i for i, ln in enumerate(lines, 1) if "`" in ln and not ln.strip().startswith("%")]
    dash = [i for i, ln in enumerate(lines, 1) if re.match(r"^\s*- ", ln) and not ln.strip().startswith("%")]
    print("             反引号行=%d  行首'- '行=%d" % (len(bt), len(dash)))
    for i in bt[:5]:
        print("  反引号 L%d: %s" % (i, lines[i-1].strip()[:90]))
    for i in dash[:5]:
        print("  短横   L%d: %s" % (i, lines[i-1].strip()[:90]))
