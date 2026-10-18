# -*- coding: utf-8 -*-
"""r72 探针：导出三卷「新目录骨架区」的完整标题 + 注释结构。
- book.tex：L0 .. \part{old}
- female.tex / male.tex：新骨架区（从 \mainmatter / \listoftables 锚之后到 \part*{原始内容}）
"""
import io
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
TITLE_RE = re.compile(r"\\(part|chapter|section|subsection|subsubsection|subparagraph)\*?\{([^{}]*)\}")


def read(fn):
    raw = io.open(os.path.join(BASE, fn), encoding="utf-8", newline="").read()
    n_crlf = raw.count("\r\n")
    lines = raw.replace("\r\n", "\n").split("\n")
    return lines, n_crlf


def dump(fn, start_pred, end_pred, out):
    lines, n_crlf = read(fn)
    si = next((i for i, l in enumerate(lines) if start_pred(l)), None)
    ei = next((i for i, l in enumerate(lines) if end_pred(l)), None)
    out.append("=" * 90)
    out.append("%s  lines=%d CRLF=%d  骨架区 L%d .. L%d" % (fn, len(lines), n_crlf,
                                                        (si or 0) + 1, (ei or len(lines))))
    out.append("=" * 90)
    if si is None:
        return
    end = ei if ei is not None else len(lines)
    for i in range(si, end):
        l = lines[i]
        st = l.strip()
        m = TITLE_RE.match(st)
        if m:
            lv, name = m.group(1), m.group(2).strip()
            ind = {"part": "", "chapter": "  ", "section": "    ",
                   "subsection": "      ", "subsubsection": "        ",
                   "subparagraph": "          "}[lv]
            out.append("%s[%s] %s" % (ind, lv[:4], name))
        elif st.startswith("%"):
            out.append("        %s" % st)
    out.append("")


res = []
# book.tex：preamble 之后到 \part{old}
dump("book.tex",
     lambda l: l.strip() == "\\begin{document}",
     lambda l: l.strip() in ("\\part{old}", "\\part{old}"),
     res)
# female.tex：\mainmatter 之后到 \part*{原始内容}
dump("female.tex",
     lambda l: l.strip() == "\\mainmatter",
     lambda l: "原始内容" in l and l.strip().startswith("\\part"),
     res)
dump("male.tex",
     lambda l: l.strip() == "\\listoftables",
     lambda l: "原始内容" in l and l.strip().startswith("\\part"),
     res)

io.open(os.path.join(BASE, "_r72a_dump.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(res))
print("写 _r72a_dump.txt 行数", len(res))
