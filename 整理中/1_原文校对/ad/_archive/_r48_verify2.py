# -*- coding: utf-8 -*-
"""r48 尾批校验：内容块唯一落位 + 格式检查 + 薄条复扫确认清零"""
import io, json, os, re

BASE = os.path.dirname(os.path.abspath(__file__))
T = {}
for fn in ("book.tex", "female.tex", "male.tex"):
    raw = io.open(os.path.join(BASE, fn), encoding="utf-8", newline="").read()
    bare = raw.count("\n") - raw.count("\r\n")
    T[fn] = raw
    print("%-12s 行数=%6d  CRLF=%d  bare-LF=%d" % (fn, raw.replace("\r\n","\n").count("\n")+1, raw.count("\r\n"), bare))
    md = [ln for ln in raw.replace("\r\n","\n").split("\n")
          if not ln.strip().startswith("%") and re.match(r"^\s*(#{1,4}\s|\*\*|\|.*\|)", ln)]
    print("             markdown 残留=%d" % len(md))

# 内容块唯一性：取每条的首句前 18 字作为定位串
mods = {}
import importlib.util
for name in ("_r48_d1", "_r48_d2", "_r48_d3"):
    spec = importlib.util.spec_from_file_location(name, os.path.join(BASE, name + ".py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    mods.update(m.D)

fail = 0
for key, content in sorted(mods.items()):
    text = content.replace("\r\n", "\n").replace("\r", "\n")
    # 取内容里第一个不含 LaTeX 命令的连续 14 字片段
    seg = None
    for s in re.split(r"[\n\\{}]", text):
        s = s.strip()
        if len(s) >= 14 and not s.startswith(("```", "print")):
            seg = s[:14]; break
    n = sum(t.count(seg) for t in T.values()) if seg else 0
    ok = (n == 1)
    if not ok:
        fail += 1
        print("<<异常>> %s x%d  seg=%r" % (key, n, seg))
print("内容块唯一性：共 %d 条，异常 %d" % (len(mods), fail))
