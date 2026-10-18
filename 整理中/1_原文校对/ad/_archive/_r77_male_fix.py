# -*- coding: utf-8 -*-
"""r77: 补齐 male.tex preamble 缺失的宏包/宏（上轮从停用框架区迁入的成稿用到），
并修正若干源码笔误。

用法：python _r77_male_fix.py dry-run | apply
"""
import io, re, sys, shutil, time

MODE = sys.argv[1] if len(sys.argv) > 1 else "dry-run"
FN = "male.tex"

raw = io.open(FN, encoding="utf-8", newline="").read()
assert "\r\n" in raw, "male.tex 应为 CRLF"
lines = raw.split("\r\n")

# ── 1. preamble 补块（插在 \usepackage{pdfpages} 之后） ───────────────────
ANCHOR = "\\usepackage{pdfpages}"
INSERT = [
    "",
    "% ===== 彩色盒子 / 表格扩展 / 关键词强调（r77）----",
    "%   背景：上轮把停用框架区的成稿迁入编译区，其中使用了 tcolorbox / tabularx / \\keyword，",
    "%   而本文件 preamble 未加载对应宏包与宏定义，导致 458 个编译错误。",
    "\\usepackage{tcolorbox}",
    "\\usepackage{tabularx}",
    "\\newcommand{\\keyword}[1]{\\textbf{#1}}",
]
hits = [i for i, l in enumerate(lines) if l.strip() == ANCHOR]
assert len(hits) == 1, "锚 %s 命中 %d 处" % (ANCHOR, len(hits))
assert "\\usepackage{tcolorbox}" not in raw, "已存在 tcolorbox，勿重复插入"
ai = hits[0]

# ── 2. 源码笔误 ──────────────────────────────────────────────────────────
FIXES = [
    ("colframe=red!50~50!black", "colframe=red!50!black"),      # L3763 多了一个 ~
    ("colback=pink!5!white,colframe=red!50!black,title=贴心小叮咛]",
     "colback=pink!5!white,colframe=red!50!black,title=贴心小叮咛]"),  # 占位（保持不变）
]
text = "\r\n".join(lines)
fixed = []
for old, new in FIXES:
    if old == new:
        continue
    n = text.count(old)
    if n:
        text = text.replace(old, new)
        fixed.append((old, new, n))

# ── 3. 其他可疑残留：colframe/colback 里出现 ~ ────────────────────────────
sus = re.findall(r"col(?:frame|back)=[^\],]*~[^\],]*", text)
print("colXxx 中含 ~ 的可疑参数：", sus[:10])

lines = text.split("\r\n")
out = lines[:ai + 1] + INSERT + lines[ai + 1:]
ns = "\r\n".join(out)

# ── 校验 ─────────────────────────────────────────────────────────────────
assert ns.count("\r\n") == len(out) - 1, "CRLF 异常"
assert raw.count("{") - raw.count("}") == ns.count("{") - ns.count("}"), "花括号 delta 变化"
assert ns.count("\\usepackage{tcolorbox}") == 1
assert ns.count("\\usepackage{tabularx}") == 1
assert ns.count("\\newcommand{\\keyword}") == 1
assert ns.rstrip().endswith("\\end{document}")
print("%s：%d → %d 行" % (FN, len(lines), len(out)))
for old, new, n in fixed:
    print("  修正笔误 ×%d：%s → %s" % (n, old[:40], new[:40]))

if MODE == "apply":
    st = time.strftime("%Y%m%d_%H%M%S")
    shutil.copy2(FN, FN + ".r77bak_" + st)
    io.open(FN, "w", encoding="utf-8", newline="").write(ns)
    print("已写盘（备份 .r77bak_%s）" % st)
else:
    print("%s 模式，未写盘。" % MODE)
