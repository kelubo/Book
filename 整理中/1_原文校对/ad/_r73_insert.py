# -*- coding: utf-8 -*-
"""r73 执行器：把《求助渠道》四小节正文插入 book.tex，并更正两处注释。
用法: python _r73_insert.py dry-run | apply
"""
import io, sys, difflib
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, ".")
from _r73_new import NEW

MODE = sys.argv[1] if len(sys.argv) > 1 else "dry-run"
assert MODE in ("dry-run", "apply"), MODE

F = "book.tex"
raw = io.open(F, encoding="utf-8", newline="").read()
assert raw.count("\r\n") == 0, "book.tex 应为纯 LF"
lines = raw.split("\n")

# 锚点：行号(1-based) -> 该行原文（必须逐字相符）
ANCH = {
    2019: "% [重写] 原三条锚（求助渠道 / 心理咨询 / 医疗机构导航）在旧区无同名来源；",
    2020: "%        改挂旧区实际存在的 \"性健康资源与支持\"（6 小节）与\"紧急情况的应对指南\"。",
    2023: "% [待写] 旧区暂无可对位来源",
    2024: "\\subsection{医疗机构}",
    2025: "\\subsection{心理咨询机构}",
    2026: "\\subsection{公益热线与社群}",
    2027: "\\subsection{网络求助的注意事项}",
    156: "%   5. 个别章标注 [待写]，表示旧区暂无可对位的来源，需另行撰写。",
}

# ── 校验 1：锚行逐字相符 ──
print("=== 校验 1：锚行逐字比对 ===")
bad = 0
for ln, txt in sorted(ANCH.items()):
    actual = lines[ln - 1]
    ok = (actual == txt)
    if not ok:
        bad += 1
        print("  [X] L%d 不符" % ln)
        print("      期望: |%s|" % txt)
        print("      实际: |%s|" % actual)
print("  锚行 %d 条，不符 %d 条" % (len(ANCH), bad))
assert bad == 0, "锚行不匹配，终止。"

# ── 构造插入计划（倒序执行） ──
# mode=after : 在该行之后插入
# mode=repl  : 用新串替换该行
PLAN = [
    # 四小节正文（在各 \subsection 行之后插入）
    (2024, "after", NEW["医疗机构"]),
    (2025, "after", NEW["心理咨询机构"]),
    (2026, "after", NEW["公益热线与社群"]),
    (2027, "after", NEW["网络求助的注意事项"]),
    # 章级注释重写（两行 → 新注释）
    (2019, "repl2", NEW["__chapter_note__"].rstrip("\n")),
    # 节级注释：撤销错误 [待写]
    (2023, "repl", NEW["__section_note__"].rstrip("\n")),
]
# 说明注释第 5 条：撤销（[待写] 归零）
PLAN.append((156, "del", None))

# repl2 需要把 L2019+L2020 两行合并替换，单独处理
plan = [p for p in PLAN if p[1] != "repl2"]

# ── 校验 2：内容自身洁净（无 **、无裸 %） ──
print()
print("=== 校验 2：内容洁净度 ===")
for k, v in NEW.items():
    if k.startswith("__"):
        continue
    assert "**" not in v, k + " 含 **"
    for i, l in enumerate(v.split("\n")):
        # 行内 % 必须是转义 \% 或整行注释开头
        s = l
        idx = 0
        while True:
            p = s.find("%", idx)
            if p < 0:
                break
            if p > 0 and s[p - 1] == "\\":
                idx = p + 1
                continue
            if s.lstrip().startswith("%"):
                break
            raise AssertionError("%s 第%d行有未转义 %%: %s" % (k, i + 1, l))
    print("  [OK] %s (%d 行)" % (k, len(v.split("\n"))))
for k in ("__chapter_note__", "__section_note__"):
    v = NEW[k]
    assert "**" not in v, k
    print("  [OK] %s (%d 行, 纯注释)" % (k, len(v.split("\n"))))

# ── 校验 3：花括号净值 ──
def brace_delta(text):
    return text.count("{") - text.count("}")

print()
print("=== 校验 3：花括号净值 ===")
tot = 0
for k, v in NEW.items():
    d = brace_delta(v)
    tot += d
    print("  [%s] %s delta=%d" % ("OK" if d == 0 else "!!", k, d))
assert tot == 0, "花括号不配平: %d" % tot

# ── 预演结果 ──
out = list(lines)
for ln, mode, txt in sorted(plan, key=lambda x: -x[0]):
    if mode == "after":
        out.insert(ln, txt)
    elif mode == "repl":
        assert out[ln - 1] == ANCH[ln], "repl 锚失效 L%d" % ln
        out[ln - 1] = txt
    elif mode == "del":
        assert out[ln - 1] == ANCH[ln], "del 锚失效 L%d" % ln
        del out[ln - 1]

# 章级注释：L2019 起两行替换、L2021 空行删除
out2 = []
i = 0
done_chapter = False
while i < len(out):
    if (not done_chapter) and i < len(out) and out[i] == ANCH[2019]:
        assert out[i + 1] == ANCH[2020], "章级注释第二行不符"
        out2.append(NEW["__chapter_note__"].rstrip("\n"))
        i += 2
        # 吃掉紧随的空行
        if i < len(out) and out[i] == "":
            i += 1
        done_chapter = True
        continue
    out2.append(out[i])
    i += 1
assert done_chapter, "章级注释未替换"
out = out2

new_text = "\n".join(out)

print()
print("=== 预演统计 ===")
print("  原行数: %d  新行数: %d  净增: %d" % (len(lines), len(out), len(out) - len(lines)))
# 注：book.tex 全文存在 1 处基线花括号失衡（L53514 遗留注释内的孤立 '{'，位于注释中不参与编译）。
#     故仅断言"基线 delta 不变"，而非 delta == 0。
base_delta = brace_delta(raw)
post_delta = brace_delta(new_text)
print("  花括号 delta: 基线 %d -> 修改后 %d" % (base_delta, post_delta))
assert base_delta == post_delta, "花括号净值被改变（基线 %d -> %d）" % (base_delta, post_delta)

# 正文行多重集守恒（新增行之外的旧行必须原样保留）
old_counter = {}
for l in lines:
    old_counter[l] = old_counter.get(l, 0) + 1
new_counter = {}
for l in out:
    new_counter[l] = new_counter.get(l, 0) + 1
added = {}
for k, v in new_counter.items():
    d = v - old_counter.get(k, 0)
    if d > 0:
        added[k] = d
removed = {}
for k, v in old_counter.items():
    d = v - new_counter.get(k, 0)
    if d > 0:
        removed[k] = d
print("  新增行种类: %d  删除行种类: %d" % (len(added), len(removed)))
for k, v in list(removed.items())[:20]:
    print("    - [x%d] %s" % (v, k[:80]))

# 旧区完整性：\part{old} 之后逐字一致
old_idx = None
for i, l in enumerate(lines):
    if l == r"\part{old}":
        old_idx = i
        break
new_old_idx = None
for i, l in enumerate(out):
    if l == r"\part{old}":
        new_old_idx = i
        break
assert old_idx is not None and new_old_idx is not None
seg_old = lines[old_idx:]
seg_new = out[new_old_idx:]
print("  旧区逐字一致: %s (L%d -> L%d)" % (seg_old == seg_new, old_idx + 1, new_old_idx + 1))
assert seg_old == seg_new, "旧区被改动！"

# 说明注释区块之外的头部一致
assert lines[:155] == out[:155], "头部 L1-155 被改动"

print()
print("=== 目标区预演 (新 L2015-L2065) ===")
for i in range(2014, min(2066, len(out))):
    print("  %d |%s|" % (i + 1, out[i]))

if MODE == "dry-run":
    print()
    print("DRY-RUN 完成，未写盘。")
else:
    io.open(F, "w", encoding="utf-8", newline="").write(new_text)
    print()
    print("已写盘:", F, len(new_text), "字符")
