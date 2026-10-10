# -*- coding: utf-8 -*-
"""定位环境栈错配与花括号负平衡点"""
import os, re
BASE = r"D:/Git/Book/整理中/1_原文校对/ad"

def scan_env(fname):
    p = os.path.join(BASE, fname)
    with open(p, encoding="utf-8", newline="") as fp:
        lines = fp.read().split("\n")
    stack = []
    print(f"=== {fname} 环境栈检查 ===")
    for i, ln in enumerate(lines, 1):
        for m in re.finditer(r"\\(begin|end)\{([^}]+)\}", ln):
            kind, env = m.group(1), m.group(2)
            if kind == "begin":
                stack.append((env, i))
            else:
                if not stack:
                    print(f"  L{i}: \\end{{{env}}} 但栈为空（多余结束）")
                elif stack[-1][0] != env:
                    # 找栈里最近的同名
                    found = None
                    for j in range(len(stack)-1, -1, -1):
                        if stack[j][0] == env:
                            found = j
                            break
                    if found is not None:
                        dangling = stack[found+1:]
                        print(f"  L{i}: \\end{{{env}}} 期望 \\end{{{stack[-1][0]}}}"
                              f"（由 L{stack[-1][1]} 开启）；被跨越未闭合：{[(e,l) for e,l in dangling]}")
                        del stack[found:]
                    else:
                        print(f"  L{i}: \\end{{{env}}} 无匹配 begin")
    if stack:
        print(f"  未闭合栈残留: {stack}")

def scan_braces(fname):
    p = os.path.join(BASE, fname)
    with open(p, encoding="utf-8", newline="") as fp:
        lines = fp.read().split("\n")
    bal = 0
    print(f"=== {fname} 花括号负平衡检查 ===")
    in_verb = False
    for i, ln in enumerate(lines, 1):
        # 跳过 verbatim / lstlisting
        if re.search(r"\\begin\{(verbatim|lstlisting|minted|Verbatim)\}", ln):
            in_verb = True
        if in_verb:
            if re.search(r"\\end\{(verbatim|lstlisting|minted|Verbatim)\}", ln):
                in_verb = False
            continue
        s = re.sub(r"\\\{", "", ln)
        s = re.sub(r"\\\}", "", s)
        prev = bal
        bal += s.count("{") - s.count("}")
        if bal < 0 <= prev:
            print(f"  L{i}: 累计平衡首次转负 -> {bal}  | {ln.strip()[:110]}")
    print(f"  最终累计平衡: {bal}")

scan_env("female.tex")
scan_braces("book.tex")
