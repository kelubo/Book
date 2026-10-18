# -*- coding: utf-8 -*-
"""r72 执行器：按 _r72_data.py 的三卷分工方案改写三个文件。

用法：
    _r72_apply.py             dry-run，只报告不落盘
    _r72_apply.py preview     生成 _r72_preview_book/female/male.txt 供人工审阅
    _r72_apply.py apply       落盘

安全断言：
    1. book.tex 的 \\part{old} 及其后内容逐字不变；
    2. female.tex / male.tex 的 \\part*{原始内容} 及其后内容逐字不变；
    3. 换行类型（LF / CRLF）保持原样；
    4. 花括号净值不减少。
"""
import io
import os
import re
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _r72_data as D  # noqa: E402

BASE = os.path.dirname(os.path.abspath(__file__))
MODE = (sys.argv[1] if len(sys.argv) > 1 else "dry").lower()

PURE_SEP = re.compile(r"^\s*%\s*=+\s*(第[一二三四五六七八九十]+篇)?\s*=*\s*$")
ANY_TITLE = re.compile(r"^\\(part|chapter|section|subsection)\*?\{")


# ═══════════════════════════════ 基础 ═══════════════════════════════
def load(fn):
    raw = io.open(os.path.join(BASE, fn), encoding="utf-8", newline="").read()
    crlf = raw.count("\r\n")
    lines = raw.replace("\r\n", "\n").split("\n")
    return lines, crlf


def save(fn, lines, crlf):
    sep = "\r\n" if crlf else "\n"
    io.open(os.path.join(BASE, fn), "w", encoding="utf-8", newline="").write(sep.join(lines))


def nbrace(lines):
    t = "".join(lines)
    return t.count("{") - t.count("}")


def strip_braces(lines):
    """把 \\chapter{X} / \\section{X} 的标题名抽出来（仅统计用）"""
    out = []
    for l in lines:
        s = l.strip()
        m = re.match(r"\\(part|chapter|section|subsection)\*?\{([^{}]*)\}", s)
        if m:
            out.append((m.group(1), m.group(2).strip()))
    return out


# ═══════════════════════════ book.tex ops ═══════════════════════════
def find_title(lines, lo, hi, kind, name):
    pat = "\\%s{%s}" % (kind, name)
    for i in range(lo, hi):
        if lines[i].rstrip() == pat:
            return i
    return None


def block_end(lines, i, hi, kinds):
    """从 i 之后找下一个 col-0 的 kinds 标题行"""
    j = i + 1
    while j < hi:
        s = lines[j]
        for k in kinds:
            if s.startswith("\\%s{" % k) or s.startswith("\\%s*{" % k):
                return j
        j += 1
    return hi


def trim_tail(lines, i, j):
    k = j - 1
    while k > i and (lines[k].strip() == "" or PURE_SEP.match(lines[k])):
        k -= 1
    return k + 1


def apply_book():
    lines, crlf = load("book.tex")
    n0 = len(lines)
    br0 = nbrace(lines)
    si = next(i for i, l in enumerate(lines) if l.strip() == "\\begin{document}")
    ei = next(i for i, l in enumerate(lines) if l.strip() == "\\part{old}")
    old_tail = list(lines[ei:])
    log = []

    for op in D.BOOK_OPS:
        kind = op["op"]

        if kind == "sub":
            whole = "\n".join(lines)
            assert whole.count(op["old"]) == 1, "sub 未命中或命中多次：%r" % op["old"][:40]
            whole = whole.replace(op["old"], op["new"])
            lines = whole.split("\n")
            log.append("sub          %s" % op["old"][:36])

        elif kind == "replace_chapter":
            i = find_title(lines, si, ei, "chapter", op["ch"])
            assert i is not None, "未找到章：" + op["ch"]
            j = trim_tail(lines, i, block_end(lines, i, ei, ("chapter", "part")))
            lines[i:j] = op["block"]
            log.append("replace_ch   %s（%d 行 → %d 行）" % (op["ch"], j - i, len(op["block"])))
        elif kind == "delete_chapter":
            i = find_title(lines, si, ei, "chapter", op["ch"])
            assert i is not None, "未找到章：" + op["ch"]
            j = trim_tail(lines, i, block_end(lines, i, ei, ("chapter", "part")))
            lines[i:j] = op["marker"]
            log.append("del_chapter  %s（删 %d 行 → 留 %d 行标记）" % (op["ch"], j - i, len(op["marker"])))

        elif kind in ("delete_section", "delete_subsection"):
            lv = "section" if kind == "delete_section" else "subsection"
            key = "sec" if lv == "section" else "sub"
            ci = find_title(lines, si, ei, "chapter", op["ch"])
            assert ci is not None, "未找到章：" + op["ch"]
            cj = block_end(lines, ci, ei, ("chapter", "part"))
            i = find_title(lines, ci, cj, lv, op[key])
            assert i is not None, "未找到%s：%s / %s" % (lv, op["ch"], op[key])
            j = trim_tail(lines, i, block_end(lines, i, cj, ("section", "chapter", "part") if lv == "section"
                                              else ("subsection", "section", "chapter", "part")))
            lines[i:j] = op["marker"]
            log.append("del_%-8s %s / %s（%d 行 → %d 行标记）" % (lv, op["ch"], op[key], j - i, len(op["marker"])))

        elif kind == "rename_section":
            ci = find_title(lines, si, ei, "chapter", op["ch"])
            cj = block_end(lines, ci, ei, ("chapter", "part"))
            i = find_title(lines, ci, cj, "section", op["sec"])
            assert i is not None, "未找到节：%s / %s" % (op["ch"], op["sec"])
            lines[i] = "\\section{%s}" % op["new"]
            log.append("rename_sec   %s / %s → %s" % (op["ch"], op["sec"], op["new"]))

        elif kind in ("note_chapter", "note_section"):
            lv = "chapter" if kind == "note_chapter" else "section"
            key = "ch" if lv == "chapter" else "sec"
            if lv == "chapter":
                i = find_title(lines, si, ei, "chapter", op[key])
            else:
                ci = find_title(lines, si, ei, "chapter", op["ch"])
                cj = block_end(lines, ci, ei, ("chapter", "part"))
                i = find_title(lines, ci, cj, "section", op[key])
            assert i is not None, "未找到锚：%s" % op.get(key)
            lines[i + 1:i + 1] = op["lines"]
            log.append("note_%-7s %s（+%d 行）" % (lv, op[key], len(op["lines"])))

        else:
            raise ValueError("未知 op：" + kind)

    # ---- 断言 ----
    ei2 = next(i for i, l in enumerate(lines) if l.strip() == "\\part{old}")
    assert list(lines[ei2:]) == old_tail, "book.tex 旧区被改动！"
    assert nbrace(lines) == br0, "花括号净值变化：%d → %d" % (br0, nbrace(lines))

    if MODE == "preview":
        io.open(os.path.join(BASE, "_r72_preview_book.txt"), "w", encoding="utf-8", newline="\n") \
            .write("\n".join(lines[:ei2]))
    if MODE == "apply":
        save("book.tex", lines, crlf)

    print("── book.tex ──")
    print("  行数 %d → %d（%+d）；\\part{old} L%d → L%d；旧区逐字一致 ✓；花括号 %d → %d"
          % (n0, len(lines), len(lines) - n0, ei + 1, ei2 + 1, br0, nbrace(lines)))
    for l in log:
        print("   ", l)
    return lines[:ei2]


# ═══════════════ female.tex / male.tex 全量骨架替换 ═══════════════
def apply_block(fn, block, start_anchor, tag):
    lines, crlf = load(fn)
    n0 = len(lines)
    br0 = nbrace(lines)
    sa = next(i for i, l in enumerate(lines) if l.strip() == start_anchor)
    oi = next(i for i, l in enumerate(lines) if l.strip().startswith("\\part*{原始内容}")
              or ("原始内容" in l and l.strip().startswith("\\part")))
    old_tail = list(lines[oi:])
    old_block = list(lines[sa + 1:oi])

    new_lines = block.split("\n")
    out = lines[:sa + 1] + new_lines + lines[oi:]

    # ---- 断言 ----
    oi2 = next(i for i, l in enumerate(out) if l.strip().startswith("\\part*{原始内容}")
               or ("原始内容" in l and l.strip().startswith("\\part")))
    assert list(out[oi2:]) == old_tail, "%s 旧区被改动！" % fn
    assert nbrace(out) == br0, "%s 花括号净值变化：%d → %d" % (fn, br0, nbrace(out))

    if MODE == "preview":
        io.open(os.path.join(BASE, "_r72_preview_%s.txt" % tag), "w", encoding="utf-8", newline="\n") \
            .write("\n".join(out[sa + 1:oi2]))
    if MODE == "apply":
        save(fn, out, crlf)

    print("── %s ──" % fn)
    print("  行数 %d → %d（%+d）；骨架块 L%d..L%d（%d 行）→ %d 行；旧区逐字一致 ✓；花括号 %d → %d"
          % (n0, len(out), len(out) - n0, sa + 2, oi, len(old_block), len(new_lines),
             br0, nbrace(out)))
    return out[sa + 1:oi2]


bk = apply_book()
fm = apply_block("female.tex", D.FEMALE_BLOCK, "\\mainmatter", "female")
ml = apply_block("male.tex", D.MALE_BLOCK, "\\listoftables", "male")


def stat(name, lines):
    c = Counter(k for k, _ in strip_braces(lines))
    print("%-12s part %d / chapter %d / section %d / subsection %d"
          % (name, c["part"], c["chapter"], c["section"], c["subsection"]))


print()
stat("book 骨架", bk)
stat("female 骨架", fm)
stat("male 骨架", ml)
print("\nMODE =", MODE)
