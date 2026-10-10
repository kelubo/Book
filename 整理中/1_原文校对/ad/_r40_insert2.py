# -*- coding: utf-8 -*-
"""r40-fix: 从备份恢复 book.tex，行级插入三个新节（不受注释行子串干扰）"""
import io, shutil

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
FN = BASE + r"\book.tex"
BK = BASE + r"\_backup_r40\book.tex"
CR = "\r\n"

# 1) 恢复
shutil.copy2(BK, FN)
text = io.open(FN, "r", encoding="utf-8", newline="").read()
lines = text.split(CR)
print("restored from backup: %d lines" % len(lines))

JOBS = [
    ("_r40_blk_a.tex", r"\section{性与多元关系}"),          # A1
    ("_r40_blk_b.tex", r"\section{性创伤与心理康复}"),      # A2
    ("_r40_blk_c.tex", r"\section{特殊职业人群的性健康}"),  # A3
]

# 2) 先展示每个锚的全部子串出现位置（含注释），确认风险
for _, anchor in JOBS:
    subs = [i for i, ln in enumerate(lines, 1) if anchor in ln]
    real = [i for i, ln in enumerate(lines, 1) if ln.strip().startswith(anchor)]
    print("anchor %-24s substring@%s  real@%s" % (anchor, subs, real))

# 3) 行级插入：在"非注释行首锚"行前插入 core 行 + 2 空行
for blk, anchor in JOBS:
    raw = io.open(BASE + "\\" + blk, "r", encoding="utf-8", newline="").read()
    raw = raw.replace("\r\n", "\n").replace("\r", "\n")  # LF 归一
    core_lines = [ln.rstrip() for ln in raw.rstrip("\n").split("\n")]  # 每行去尾空白，重建 CRLF
    if not core_lines or not core_lines[0].startswith("\\"):
        raise RuntimeError("bad block: %s" % blk)
    # 幂等：正文行首锚 + core 已存在则跳过
    already = any(anchor in ln for ln in core_lines)
    hits = [i - 1 for i, ln in enumerate(lines, 1) if ln.strip().startswith(anchor)]
    assert len(hits) == 1, "real anchor not unique: %s -> %s" % (anchor, hits)
    idx = hits[0]
    # 检查是否已插入（锚前一行是否已是本块结尾）
    if idx >= 2 and core_lines[-1] in lines[idx - 2]:
        print("skip (already): %s" % blk)
        continue
    lines[idx:idx] = core_lines + ["", ""]
    print("line-inserted %-18s before real anchor @L%d (+%d lines)" % (blk, idx + 1, len(core_lines) + 2))

with io.open(FN, "w", encoding="utf-8", newline="") as f:
    f.write(CR.join(lines))
print("book.tex now %d lines" % (len(lines)))

# 4) 验证：三个新节标题在正文中的行号 + 注释树未被污染
out = CR.join(lines).split(CR)
for probe in (r"\section{年龄差伴侣", r"\subsection{皮肤可见疾病与性自信", r"\section{职场恋情与权力不对等}", r"\section{性与多元关系}", r"\section{性创伤与心理康复}", r"\section{特殊职业人群的性健康}"):
    hit = [i for i, ln in enumerate(out, 1) if ln.strip().startswith(probe)]
    print("probe %-30s -> %s" % (probe, hit))
bad = sum(1 for ln in out[:400] if not ln.strip().startswith("%") and ("有一类皮肤病" in ln or "忘年恋的亲密" in ln))
print("preamble contamination (should be 0):", bad)
