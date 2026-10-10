# -*- coding: utf-8 -*-
"""r49 female.tex 结构修复：
1) 把 L221-237 裸内容块（documentclass 之前无法编译）移入 \\begin{document} 之后，加迁移注释
2) 修复 'fi %% \\ifskipfemaleframework 结束' 缺失的反斜杠
不删除任何内容。
"""
import io, os, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
FN = "female.tex"

os.makedirs(os.path.join(BASE, "_backup_r49"), exist_ok=True)
shutil.copy2(os.path.join(BASE, FN), os.path.join(BASE, "_backup_r49", FN))

raw = io.open(os.path.join(BASE, FN), encoding="utf-8", newline="").read().replace("\r\n", "\n")
L = raw.split("\n")

# --- 1. 定位并剪切裸块 ---
i_start = None
for i, ln in enumerate(L, 1):
    if ln.strip() == "\\subsection{阴唇形态多样性与外阴美容手术的风险}":
        i_start = i; break
assert i_start, "未找到裸块起始行"
i_end = None
for j in range(i_start, len(L)):
    if L[j].strip() == "\\section{饮食与营养}":
        i_end = j + 1; break  # 含该行
    if L[j].strip() == "\\newif\\ifskipfemaleframework":
        raise SystemExit("未找到块尾 \\section{饮食与营养}")
assert i_end and i_end - i_start < 30, "块范围异常: %d-%d" % (i_start, i_end)
block = L[i_start-1:i_end]
# 校验块内没有章节/文档结构命令（防止误搬）
forbidden = [s for s in block if s.strip().startswith(("\\chapter", "\\documentclass", "\\begin{document}", "\\part"))]
assert not forbidden, "块内含结构命令: %s" % forbidden

del L[i_start-1:i_end]

# --- 2. 修复 fi 笔误 ---
n_fi = 0
for k, ln in enumerate(L):
    if ln.strip().startswith("fi %%") and "ifskipfemaleframework" in ln:
        L[k] = ln.replace("fi %%", "\\fi %%", 1)
        n_fi += 1
assert n_fi == 1, "fi 笔误行数=%d" % n_fi

# --- 3. 在 \begin{document} 后插入块 ---
i_bd = None
for k, ln in enumerate(L):
    if ln.strip() == "\\begin{document}":
        i_bd = k; break
assert i_bd is not None, "未找到 begin{document}"
note = [
    "",
    "% ════ r49 迁移说明 ══════════════════════════════════════════════════════",
    "% 以下内容原位于文件头部注释区之后、\\documentclass 之前（无法编译的位置），",
    "% 于第四十九轮整体移入文档内。内容未作任何删改，待按“章节重组方案”归位。",
    "% ════════════════════════════════════════════════════════════════════════",
]
L[i_bd+1:i_bd+1] = note + block

new_raw = "\r\n".join(L)
with io.open(os.path.join(BASE, FN), "w", encoding="utf-8", newline="") as f:
    f.write(new_raw)

print("裸块 %d-%d（%d 行）已移至 begin{document} 后" % (i_start, i_end, i_end - i_start + 1))
print("fi 笔误修复 %d 处" % n_fi)
print("female.tex 现行数:", new_raw.count("\n") + 1, " bare-LF =", new_raw.count("\n") - new_raw.count("\r\n"))
