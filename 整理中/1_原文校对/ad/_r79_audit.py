# -*- coding: utf-8 -*-
"""r79: 四卷静态体检（换行/花括号/环境配对/层级统计/卷内章级重名/标题转义）。"""
import io, re, os, collections

DIR = os.path.dirname(os.path.abspath(__file__))
FILES = ["0_book.tex", "1_male.tex", "2_female.tex", "3_position.tex"]
ENVS = ["itemize", "enumerate", "description", "center", "table", "tabular",
        "tabularx", "longtable", "tcolorbox", "quote", "verbatim", "figure",
        "multicols", "paracol", "glossary", "thebibliography", "abstract", "minipage"]

def strip_cmt(s):
    return re.sub(r"(?<!\\)%.*$", "", s)

for fn in FILES:
    p = os.path.join(DIR, fn)
    raw = io.open(p, encoding="utf-8", newline="").read()
    crlf = raw.count("\r\n")
    lf = raw.count("\n")
    nl = "纯CRLF" if crlf == lf and crlf > 0 else ("纯LF" if crlf == 0 else "混合!(crlf=%d/lf=%d)" % (crlf, lf))
    lines = raw.split("\n")
    nocmt = [strip_cmt(x.rstrip("\r")) for x in lines]
    nocmt_t = "\n".join(nocmt)
    bal = nocmt_t.count("{") - nocmt_t.count("}")
    print("=" * 60)
    print("%s: %d 行 / %s / 花括号净值 %d" % (fn, len(lines), nl, bal))
    # 层级统计
    cnt = {}
    for lv in ("part", "chapter", "section", "subsection", "subsubsection"):
        cnt[lv] = len(re.findall(r"^\\%s\*?\{" % lv, nocmt_t, re.M))
    print("  层级: " + " / ".join("%s=%d" % (k, v) for k, v in cnt.items()))
    # 环境配对
    bad = []
    for e in ENVS:
        b = len(re.findall(r"\\begin\{%s\}" % e, nocmt_t))
        f = len(re.findall(r"\\end\{%s\}" % e, nocmt_t))
        if b != f:
            bad.append("%s begin=%d end=%d" % (e, b, f))
    print("  环境配对: " + ("OK" if not bad else "; ".join(bad)))
    # 卷内章级重名（排除注释、排除 \iffalse 区间不计——粗略：跳过 \iffalse..\fi）
    # 简化：统计注释外 \chapter 标题
    chs = re.findall(r"^\\chapter\*?\{([^}]*)\}", nocmt_t, re.M)
    dup = [(t, c) for t, c in collections.Counter(chs).items() if c > 1]
    print("  章级重名: " + ("无" if not dup else str(dup)))
    # 标题未转义 &
    HEAD = re.compile(r"^\s*\\(part|chapter|section|subsection|subsubsection|paragraph)\*?\{")
    amp = sum(1 for x in nocmt if HEAD.match(x) and re.search(r"(?<!\\)&", x))
    print("  标题未转义 &: %d" % amp)
    # U+FFFD / **
    print("  U+FFFD: %d  |  '**': %d" % (raw.count("\ufffd"), nocmt_t.count("**")))
print("=" * 60)
