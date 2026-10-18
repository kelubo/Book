# -*- coding: utf-8 -*-
r"""r76：枚举某卷「停用框架区」的完整标题树 + 每块正文行数/字符数，
并同时枚举「编译区 r72 骨架」的标题树，输出两份清单供建迁移映射。

用法: python _r76_tree.py male   |   python _r76_tree.py female
"""
import io
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

F = sys.argv[1] if len(sys.argv) > 1 else "male"
lines = io.open(F + ".tex", encoding="utf-8", newline="").read().split("\n")

H = re.compile(r"^\\(part|chapter|section|subsection|subsubsection)\*?\{(.*)\}\s*$")
ifm = next(i for i, l in enumerate(lines) if re.match(r"^\\ifskip\w*framework", l.rstrip("\r")))
els = next(i for i in range(ifm, len(lines)) if lines[i].rstrip("\r").strip() == "\\else")
end = next(i for i in range(els, len(lines)) if lines[i].rstrip("\r").strip().startswith("\\fi"))
dc = next(i for i, l in enumerate(lines) if l.rstrip("\r").strip().startswith("\\documentclass"))
oi = next(i for i, l in enumerate(lines) if l.rstrip("\r").strip().startswith("\\part*{原始内容}"))

print("#" * 90)
print("# %s  停用框架区（有正文，不编译） L%d~L%d" % (F, els + 2, end))
print("#" * 90)
fw = [(i, H.match(lines[i].rstrip("\r")).group(1), H.match(lines[i].rstrip("\r")).group(2).strip())
      for i in range(els + 1, end) if H.match(lines[i].rstrip("\r"))]
for k, (i, lvl, t) in enumerate(fw):
    j = fw[k + 1][0] if k + 1 < len(fw) else end
    body = [x for x in lines[i + 1:j] if x.strip() and not x.rstrip("\r").strip().startswith("%")]
    ind = {"part": "", "chapter": "  ", "section": "    ", "subsection": "      ", "subsubsection": "        "}[lvl]
    print("%sL%-6d %-13s %-52s 正文 %4d 行" % (ind, i + 1, lvl, t[:52], len(body)))

print()
print("#" * 90)
print("# %s  编译区 r72 骨架（无正文，待迁入） L%d~L%d" % (F, dc + 1, oi))
print("#" * 90)
sk = [(i, H.match(lines[i].rstrip("\r")).group(1), H.match(lines[i].rstrip("\r")).group(2).strip())
      for i in range(dc, oi) if H.match(lines[i].rstrip("\r"))]
for k, (i, lvl, t) in enumerate(sk):
    j = sk[k + 1][0] if k + 1 < len(sk) else oi
    cmt = [x.rstrip("\r").strip() for x in lines[i + 1:j] if x.rstrip("\r").strip().startswith("%")]
    ind = {"part": "", "chapter": "  ", "section": "    ", "subsection": "      ", "subsubsection": "        "}[lvl]
    print("%sL%-6d %-13s %s" % (ind, i + 1, lvl, t[:52]))
    for c in cmt:
        print("%s        · %s" % (ind, c[:100]))

print()
print("#" * 90)
print("# %s  原始内容区（旧材料） L%d~%d" % (F, oi + 1, len(lines)))
print("#" * 90)
od = [(i, H.match(lines[i].rstrip("\r")).group(1), H.match(lines[i].rstrip("\r")).group(2).strip())
      for i in range(oi, len(lines)) if H.match(lines[i].rstrip("\r"))]
for k, (i, lvl, t) in enumerate(od):
    j = od[k + 1][0] if k + 1 < len(od) else len(lines)
    ind = {"part": "", "chapter": "  ", "section": "    ", "subsection": "      ", "subsubsection": "        "}[lvl]
    print("%sL%-6d %-13s %-52s %5d 行" % (ind, i + 1, lvl, t[:52], j - i))
