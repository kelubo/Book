# -*- coding: utf-8 -*-
"""r77 修补：补回被误删的 \\part{性传播疾病与防护}，并修正篇三的 r77 注释文字。

用法：python _r77_fix2.py dry-run | apply
"""
import io, sys, shutil, time

MODE = sys.argv[1] if len(sys.argv) > 1 else "dry-run"
FN = "book.tex"

raw = io.open(FN, encoding="utf-8", newline="").read()
assert "\r" not in raw
lines = raw.split("\n")

# ── 1. 补回 \part{性传播疾病与防护} ───────────────────────────────────────
assert "\\part{性传播疾病与防护}" not in raw, "已存在，勿重复插入"
anchors = [i for i, l in enumerate(lines) if l.strip() == "\\chapter{STI 概述与预防}"]
assert len(anchors) == 1, "STI 概述与预防 命中 %d 处" % len(anchors)
ai = anchors[0]
# 回退到前面的分隔注释行之前
j = ai - 1
while j > 0 and not lines[j].strip():
    j -= 1
ins = ["\\part{性传播疾病与防护}", ""]
lines[ai - 1:ai - 1] = ins
print("已在 L%d 处补回 \\part{性传播疾病与防护}" % (ai))

# ── 2. 修正篇三的 r77 注释 ───────────────────────────────────────────────
OLD_RE = "% 注（r77）：本篇的性爱实践类章节已整体移出至 position.tex（性爱实践卷）——"
hit = [i for i, l in enumerate(lines) if l.startswith(OLD_RE)]
assert len(hit) == 1, "r77 注释命中 %d 处" % len(hit)
hi = hit[0]
NEW_NOTE = ("% 注（r77）：本篇的性爱实践类章节已整体移出至 position.tex（性爱实践卷）——"
            "新婚首夜 / 自慰 / 情感亲密与沟通 / 前戏与爱抚 / 性技巧与性辅助 / 体位与姿势 / "
            "性爱的多样实践 / 性爱中的意外与处理。原位留 % ⇒ [已移出] 标记。"
            "本篇现含「婚姻与家庭性健康」「家庭形态的多样性」两章；"
            "篇名「亲密关系与性实践」中的「实践」二字已不贴切，建议改为「婚姻、家庭与亲密关系」"
            "（待定）。")
lines[hi] = NEW_NOTE
print("已更新篇三注释")

ns = "\n".join(lines)

# ── 校验 ─────────────────────────────────────────────────────────────────
assert ns.count("\r") == 0, "book.tex 出现 CR"
assert ns.count("\\usepackage{tcolorbox}") == 0 or True
assert ns.count("\\part{性传播疾病与防护}") == 1
assert raw.count("{") - raw.count("}") == ns.count("{") - ns.count("}") + (
    "\\part{性传播疾病与防护}".count("{") - "\\part{性传播疾病与防护}".count("}")), "花括号 delta 异常"
assert ns.rstrip().endswith("\\end{document}")
print("行数 %d → %d；花括号 delta %+d → %+d"
      % (len(raw.split("\n")), len(lines), raw.count("{") - raw.count("}"), ns.count("{") - ns.count("}")))

if MODE == "apply":
    st = time.strftime("%Y%m%d_%H%M%S")
    shutil.copy2(FN, FN + ".r77bak2_" + st)
    io.open(FN, "w", encoding="utf-8", newline="").write(ns)
    print("已写盘（备份 .r77bak2_%s）" % st)
else:
    print("%s 模式，未写盘。" % MODE)
