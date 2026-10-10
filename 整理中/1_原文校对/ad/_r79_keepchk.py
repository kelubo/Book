# -*- coding: utf-8 -*-
"""对比 position_r77.tex（r77 原版）与 3_position.tex（用户新版）：
   逐章核对 r77 正文是否保留；列出用户新增/删除的内容。"""
import io, re, os, collections

def load(fn):
    raw = io.open(fn, encoding="utf-8", newline="").read()
    return raw.split("\n")

def chapters(lines):
    """返回 [(章名, 正文文本)]；\part 之前算「前言」。"""
    out = []
    cur = ["(卷首)"]
    buf = []
    for ln in lines:
        s = ln.rstrip("\r")
        if re.match(r"^\\part\*?\{", s) or re.match(r"^\\chapter\*?\{", s):
            out.append((cur[0], "\n".join(buf)))
            m = re.match(r"^\\(part|chapter)\*?\{([^}]*)\}", s)
            cur = [m.group(2).strip()]
            buf = [s]
        else:
            buf.append(s)
    out.append((cur[0], "\n".join(buf)))
    return out

def fingerprint(text):
    """规范化正文指纹：剥注释/空白后按字符 bigram 统计。"""
    body = []
    for ln in text.split("\n"):
        s = ln.rstrip("\r")
        if s.lstrip().startswith("%"):
            continue
        if re.match(r"^\\(part|chapter)\*?\{", s):
            continue
        body.append(re.sub(r"\s+", "", s))
    return "".join(body)

A = load("position_r77.tex")
B = load("3_position.tex")
CA, CB = chapters(A), chapters(B)

def normname(t):
    return re.sub(r"\s+", "", t)

mapB = {}
for name, txt in CB:
    mapB.setdefault(normname(name), []).append(fingerprint(txt))
totalB = {k: sum(len(x) for x in v) for k, v in mapB.items()}

print("r77 版章数 %d（含卷首/参考文献）；新版章数 %d" % (len(CA), len(CB)))
print()
missing_total = 0
for name, txt in CA:
    fn = normname(name)
    fa = fingerprint(txt)
    if not fa:
        print("  [空章] %s" % name)
        continue
    if fn in mapB:
        # r77 正文在新版同名章中的保留率（粗略：最长公共子串比例太贵，用字符覆盖近似）
        fb_all = "".join(mapB[fn])
        kept = sum(1 for i in range(0, len(fa) - 40, 40) if fa[i:i+40] in fb_all)
        tot = max(1, (len(fa) - 41) // 40 + 1)
        pct = kept / tot * 100
        flag = "OK" if pct > 97 else ("部分丢失" if pct > 60 else "大量丢失!")
        if pct <= 97:
            print("  [%s] %s : r77 %d 字符块, 新版保留 %.0f%% (新版该章 %d 字符)" % (flag, name, tot, pct, totalB[fn]))
            missing_total += tot - kept
        else:
            print("  [OK]   %s (%d 块)" % (name, tot))
    else:
        print("  [章消失] %s : r77 %d 字符, 新版无同名章!" % (name, tot if False else len(fa)))
        # 在新版全文中找
        fb_all = "".join("".join(v) for v in mapB.values())
        kept = sum(1 for i in range(0, len(fa) - 40, 40) if fa[i:i+40] in fb_all)
        tot = max(1, (len(fa) - 41) // 40 + 1)
        print("          其正文在新版全文中可找到 %.0f%%" % (kept / tot * 100))
        missing_total += tot - kept
print()
print("估计丢失字符块: %d" % missing_total)
