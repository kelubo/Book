# -*- coding: utf-8 -*-
"""r73 修复：删除被重复插入的 4 个 \\subsection 标题行。
锚点：L2030/2031、L2047/2048、L2064/2065、L2083/2084 的重复标题对，删掉第二行（我的块首标题）。
用法: python _r73_fixdup.py dry-run | apply
"""
import io, sys
sys.stdout.reconfigure(encoding="utf-8")

MODE = sys.argv[1] if len(sys.argv) > 1 else "dry-run"
assert MODE in ("dry-run", "apply")

F = "book.tex"
raw = io.open(F, encoding="utf-8", newline="").read()
assert raw.count("\r\n") == 0
lines = raw.split("\n")

TARGETS = ["\\subsection{医疗机构}", "\\subsection{心理咨询机构}",
           "\\subsection{公益热线与社群}", "\\subsection{网络求助的注意事项}"]

# 找出所有"连续两行同为某 subsection 标题"的位置，删除第二次出现
to_del = []
i = 0
while i < len(lines) - 1:
    if lines[i] in TARGETS and lines[i + 1] == lines[i]:
        to_del.append(i + 1)   # 0-based，删第二行
        i += 2
    else:
        i += 1

print("=== 待删重复标题行 ===")
for ln in to_del:
    print("  L%d |%s|" % (ln + 1, lines[ln]))
print("  共 %d 处" % len(to_del))

# 校验：每处上下文必须是「标题 + 空行 + 正文」，即删除后紧跟空行
for ln in to_del:
    nxt = lines[ln + 1] if ln + 1 < len(lines) else ""
    assert nxt.strip() == "", "L%d 后不是空行：|%s|" % (ln + 2, nxt)

assert len(to_del) == 4, "重复标题数应为 4，实际 %d" % len(to_del)

out = [l for idx, l in enumerate(lines) if idx not in set(to_del)]
new_text = "\n".join(out)

print()
print("行数: %d -> %d (净 %d)" % (len(lines), len(out), len(out) - len(lines)))
print("花括号 delta: %d -> %d" % (raw.count("{") - raw.count("}"),
                                  new_text.count("{") - new_text.count("}")))
assert (raw.count("{") - raw.count("}")) == (new_text.count("{") - new_text.count("}"))

# 旧区一致
oi = lines.index("\\part{old}")
ni = out.index("\\part{old}")
print("旧区逐字一致:", lines[oi:] == out[ni:])
assert lines[oi:] == out[ni:]

if MODE == "dry-run":
    print()
    print("DRY-RUN 完成，未写盘。目标区预览：")
    for i in range(2027, 2050):
        print("  %d |%s|" % (i + 1, out[i]))
else:
    io.open(F, "w", encoding="utf-8", newline="").write(new_text)
    print()
    print("已写盘。")
