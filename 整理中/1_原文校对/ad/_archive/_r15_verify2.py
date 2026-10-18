# -*- coding: utf-8 -*-
"""剔除注释后重新检查花括号与环境配对"""
import os, re
from collections import Counter
BASE = r"D:/Git/Book/整理中/1_原文校对/ad"

def strip_comment(ln):
    # 去掉未转义的 % 之后的内容
    out = []
    i = 0
    while i < len(ln):
        c = ln[i]
        if c == "\\" and i + 1 < len(ln):
            out.append(ln[i:i+2]); i += 2; continue
        if c == "%":
            break
        out.append(c); i += 1
    return "".join(out)

def check(fname):
    with open(os.path.join(BASE, fname), encoding="utf-8", newline="") as fp:
        raw = fp.read()
    lines = raw.split("\n")
    body = []
    in_verb = False
    for i, ln in enumerate(lines, 1):
        if re.search(r"\\begin\{(verbatim|lstlisting|minted|Verbatim)\}", ln):
            in_verb = True; continue
        if in_verb:
            if re.search(r"\\end\{(verbatim|lstlisting|minted|Verbatim)\}", ln):
                in_verb = False
            continue
        s = strip_comment(ln)
        body.append((i, s))
    text = "\n".join(s for _, s in body)
    ob, cb = text.count("{"), text.count("}")
    esc_ob = len(re.findall(r"\\\{", text)); esc_cb = len(re.findall(r"\\\}", text))
    b = Counter(re.findall(r"\\begin\{([^}]+)\}", text))
    e = Counter(re.findall(r"\\end\{([^}]+)\}", text))
    bad = {k: (b[k], e.get(k, 0)) for k in set(list(b)+list(e)) if b[k] != e.get(k, 0)}
    # 栈检查
    stack = []
    errs = []
    for i, s in body:
        for m in re.finditer(r"\\(begin|end)\{([^}]+)\}", s):
            kind, env = m.group(1), m.group(2)
            if kind == "begin":
                stack.append((env, i))
            else:
                if stack and stack[-1][0] == env:
                    stack.pop()
                else:
                    errs.append((i, env, stack[-1] if stack else None))
    print(f"=== {fname}（已剔注释）===")
    print(f"  {{ }}: {ob}/{cb} delta={ob-cb}  转义后 delta={ob-esc_ob-(cb-esc_cb)}")
    print(f"  环境不平衡: {bad if bad else '无'}")
    if errs:
        for i, env, top in errs[:10]:
            print(f"  栈错配 L{i}: \\end{{{env}}}  栈顶={top}")
    else:
        print(f"  环境栈无错配")
    if stack:
        print(f"  残留未闭合(前10): {stack[:10]}")

for f in ["book.tex", "female.tex", "male.tex"]:
    check(f)
