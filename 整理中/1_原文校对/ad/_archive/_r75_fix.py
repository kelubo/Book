# -*- coding: utf-8 -*-
r"""r75 修缺字：① 源文本真错修正；② 三卷 preamble 插入符号字体回退块。

用法: python _r75_fix.py [dry-run|apply]

不变量：
  · book.tex 为纯 LF；female/male 为纯 CRLF（写回后不得出现裸 \n）
  · \part{old} / \part*{原始内容} 起逐字一致
  · 花括号 delta 不变
  · references.bib 只替换 U+30FB，不做其他改动
"""
import io
import sys

MODE = sys.argv[1] if len(sys.argv) > 1 else "dry-run"
assert MODE in ("dry-run", "apply"), MODE

FALLBACK = io.open("_r75_fallback.txt", encoding="utf-8", newline="").read().rstrip("\n")
assert FALLBACK.count("{") - FALLBACK.count("}") == 0
FB = FALLBACK.split("\n")

# ---------------- ① 源文本真错 ----------------
EDITS = [
    # (文件, 旧串, 新串, 说明)
    ("book.tex",
     "又常被用来\ufffd\ufffd疑陈述的可信度",
     "又常被用来质疑陈述的可信度",
     "U+FFFD 乱码 -> 质疑"),
    ("book.tex",
     "用 CO\u2082激光烧灼疣体",
     "用 CO$_2$ 激光烧灼疣体",
     "CO₂ 下标缺字 -> 数学模式（化学式规范）"),
    ("female.tex",
     "（<15\u00d710\u2076/ml）",
     "（$<15\\times10^{6}$/ml）",
     "10⁶ 上标缺字 -> 科学计数规范"),
    ("female.tex",
     "而是由黏膜包覆\u2e3a你一定看过黏膜",
     "而是由黏膜包覆——你一定看过黏膜",
     "⸺ 缺字 -> 中文破折号"),
    ("female.tex",
     "妮娜\u2027布罗克 艾伦\u2027斯托肯\u2027达尔",
     "妮娜\u00b7布罗克 艾伦\u00b7斯托肯\u00b7达尔",
     "‧ 缺字 -> 中西文间隔号 ·"),
]
print("=" * 74)
print("【① 源文本真错修正】")
cache = {}
for f, old, new, why in EDITS:
    if f not in cache:
        cache[f] = io.open(f, encoding="utf-8", newline="").read()
    s = cache[f]
    n = s.count(old)
    print("  %-12s %-42s 命中 %d 处" % (f, why, n))
    assert n == 1, "%s 的「%s」命中 %d 处（应恰好 1）" % (f, why, n)
    cache[f] = s.replace(old, new)

# references.bib：日文书名的 ・ 属正确用法，但 SimSun 缺字且 newunicodechar 被 xeCJK 拦截
bib = io.open("references.bib", encoding="utf-8", newline="").read()
nb = bib.count("\u30fb")
print("  %-12s %-42s 命中 %d 处" % ("references.bib", "日文中点 ・ -> ·（SimSun 无此字形）", nb))
assert nb == 3, "references.bib 中 ・ 命中 %d（应 3）" % nb
cache["references.bib"] = bib.replace("\u30fb", "\u00b7")
print("  -> 合计待写盘文件 %d 个" % len(cache))

# ---------------- ② 三卷插入回退块 ----------------
ANCHOR = "\\setCJKmonofont{SimSun}"
PLANS = []


def plan_lf(fname):
    s = cache.get(fname) or io.open(fname, encoding="utf-8", newline="").read()
    assert "\r" not in s, fname + " 预期纯 LF"
    lines = s.split("\n")
    ai = next(i for i, l in enumerate(lines) if l.startswith(ANCHOR))
    out = lines[:ai + 1] + [""] + FB + lines[ai + 1:]
    added = 1 + len(FB)
    new = "\n".join(out)
    ol = next(i for i, l in enumerate(lines) if l.strip() == "\\part{old}")
    nl = next(i for i, l in enumerate(out) if l.strip() == "\\part{old}")
    assert lines[ol:] == out[nl:], fname + " 旧区被改动"
    assert s.count("{") - s.count("}") == new.count("{") - new.count("}"), fname + " 花括号 delta 变"
    return fname, new, len(lines), len(out), "LF"


def plan_crlf(fname):
    s = cache.get(fname) or io.open(fname, encoding="utf-8", newline="").read()
    lines = s.split("\n")
    skel = next(i for i, l in enumerate(lines) if l.rstrip("\r").strip().startswith("\\part*{原始内容}"))
    ai = next(i for i in range(skel) if lines[i].rstrip("\r").startswith(ANCHOR))
    ins = [""] + FB
    out = lines[:ai + 1] + [x + "\r" for x in ins] + lines[ai + 1:]
    new = "\n".join(out)
    nl = next(i for i, l in enumerate(out) if l.rstrip("\r").strip().startswith("\\part*{原始内容}"))
    assert lines[skel:] == out[nl:], fname + " 原始内容区被改动"
    assert s.count("{") - s.count("}") == new.count("{") - new.count("}"), fname + " 花括号 delta 变"
    assert new.count("\r\n") == s.count("\r\n") + len(ins), fname + " CRLF 数异常"
    assert "\n" not in new.replace("\r\n", ""), fname + " 出现裸 \\n"
    return fname, new, len(lines), len(out), "CRLF"


print("=" * 74)
print("【② 三卷 preamble 插入符号字体回退块】")
PLANS.append(plan_lf("book.tex"))
PLANS.append(plan_crlf("female.tex"))
PLANS.append(plan_crlf("male.tex"))
PLANS.append(("references.bib", cache["references.bib"], 0, 0, "BIB"))
for fname, new, a, b, kind in PLANS:
    print("  %-16s %-6s 行 %s -> %s" % (fname, kind, a if a else "-", b if b else "-"))

# ---------------- 写盘 ----------------
if MODE == "dry-run":
    print("=" * 74)
    print("DRY-RUN 完成，未写盘。")
else:
    # 保险：先备份
    import os
    import shutil
    import time
    stamp = time.strftime("%Y%m%d_%H%M%S")
    for fname in [f for f, *_ in PLANS]:
        shutil.copy2(fname, fname + ".r75bak_" + stamp)
    print("已备份:", ", ".join(f + ".r75bak_" + stamp for f, *_ in PLANS))
    for fname, new, *_ in PLANS:
        io.open(fname, "w", encoding="utf-8", newline="").write(new)
        print("已写盘: %-16s %d 行 %d 字节" % (fname, new.count("\n") + 1, len(new.encode("utf-8"))))
    # 复验
    for fname, *_ in PLANS:
        s = io.open(fname, encoding="utf-8", newline="").read()
        if fname.endswith(".tex"):
            assert "\\newunicodechar" in s, fname + " 回退块缺失"
        print("复验 %-16s 回退块=True 行数=%d CRLF=%d" % (fname, s.count("\n") + 1, s.count("\r\n")))
    print("APPLY 完成。")
