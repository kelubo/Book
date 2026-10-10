# -*- coding: utf-8 -*-
"""r41 备选 5 节 + 术语表词条 行级插入执行器（before 型 + gloss after 型）"""
import io, os, importlib.util

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
FN = "book.tex"

def norm(s):
    return s.replace("\r\n", "\n").replace("\r", "\n")

spec = importlib.util.spec_from_file_location("_r41_new5", os.path.join(BASE, "_r41_new5.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

# (行号, 锚行全文(strip后), 内容key, mode)  mode: before=插锚行前 / gloss=插锚行后(词表内)
PLAN = [
    (53805, "\\begin{description}", "GLOSSARY", "gloss"),
    (26319, "\\section{数字时代的性教育}", "legacy", "before"),
    (27529, "\\section{残疾人的性需求与解决方案}", "burn", "before"),
    (25211, "\\section{性与多元关系}", "ldrs", "before"),
    (3864,  "\\section{新婚首夜}", "dink", "before"),
    (951,   "\\section{性交时长、频率与\"正常\"的标准}", "aid", "before"),
]

with io.open(os.path.join(BASE, FN), "r", encoding="utf-8", newline="") as f:
    raw = f.read()
lines = norm(raw).split("\n")
n0 = len(lines)

for lineno, anchor, key, mode in sorted(PLAN, key=lambda x: -x[0]):
    line = lines[lineno - 1].strip()
    if line != anchor:
        raise SystemExit("锚校验失败 L%d: 期望 %r 实际 %r" % (lineno, anchor, line))
    content = getattr(mod, key) if key == "GLOSSARY" else mod.NEW[key]
    clines = [x.rstrip() for x in norm(content).rstrip("\n").split("\n")]
    if mode == "before":
        lines[lineno - 1:lineno - 1] = [""] + clines + [""]
    else:
        lines[lineno:lineno] = clines
    print("L%-6d %s %-8s +%d 行" % (lineno, mode, key, len(clines) + (2 if mode == "before" else 0)))

out = "\r\n".join(lines)
with io.open(os.path.join(BASE, FN), "w", encoding="utf-8", newline="") as f:
    f.write(out)

print("book.tex: %d -> %d 行 (+%d)" % (n0, len(lines), len(lines) - n0))
