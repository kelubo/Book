# -*- coding: utf-8 -*-
"""r48 修复：历轮新增内容中的 **bold** 行内 markdown → \\textbf{bold}
仅处理非注释行；替换前后花括号 delta 必须保持配平。
"""
import io, os, re

BASE = os.path.dirname(os.path.abspath(__file__))
PAT = re.compile(r"\*\*(.+?)\*\*")

for fn in ("book.tex", "female.tex", "male.tex"):
    p = os.path.join(BASE, fn)
    raw = io.open(p, encoding="utf-8", newline="").read()
    lines = raw.replace("\r\n", "\n").split("\n")
    n_rep = 0
    out = []
    for ln in lines:
        if "**" in ln and not ln.strip().startswith("%"):
            before_b = ln.count("{") - ln.count("}")
            new = PAT.sub(lambda m: "\\textbf{" + m.group(1) + "}", ln)
            after_b = new.count("{") - ln.count("{")
            assert new.count("**") == 0, "残留在 L: %s" % new[:80]
            assert before_b == ln.count("{") - ln.count("}")
            n_rep += len(PAT.findall(ln))
            out.append(new)
        else:
            out.append(ln)
    new_raw = "\r\n".join(out)
    with io.open(p, "w", encoding="utf-8", newline="") as f:
        f.write(new_raw)
    print("%-12s 替换 %d 处  bare-LF=%d" % (fn, n_rep, new_raw.count("\n") - new_raw.count("\r\n")))

# 终检
print("--- 终检 ---")
for fn in ("book.tex", "female.tex", "male.tex"):
    raw = io.open(os.path.join(BASE, fn), encoding="utf-8", newline="").read().replace("\r\n", "\n")
    resid = [i for i, ln in enumerate(raw.split("\n"), 1) if "**" in ln and not ln.strip().startswith("%")]
    print("%-12s **残留=%d" % (fn, len(resid)))
print("完成")
