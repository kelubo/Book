# -*- coding: utf-8 -*-
r"""r75 两卷结构体检：对比「停用框架区（新框架成稿）」与「原始内容区（旧材料）」的
标题树与体量，找出若启用新框架会丢失的知识点（旧区有、框架无的标题）。

用法: python _r75_volaudit.py
"""
import io
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

H = re.compile(r"^\\(part|chapter|section|subsection|subsubsection)\*?\{(.*?)\}")


def norm(t):
    t = re.sub(r"（[^）]*）", "", t)
    t = re.sub(r"\([^)]*\)", "", t)
    t = re.sub(r"[\s、，,。·・\-—–：:；;／/]+", "", t)
    return t.strip()


def tree(lines, a, b, label):
    """a,b 为 0-based 半开区间"""
    out = []
    for i in range(a, b):
        s = lines[i].rstrip("\r")
        m = H.match(s)
        if m:
            out.append((m.group(1), m.group(2).strip(), i + 1))
    return out


for f, fr_a, fr_b, old_a in (("female.tex", 284, 6481, 7092),
                             ("male.tex", 179, 5766, 6251)):
    lines = io.open(f, encoding="utf-8", newline="").read().split("\n")
    # 原始内容区：从 \part*{原始内容} 起（0-based 找）
    oi = next(i for i, l in enumerate(lines)
              if l.rstrip("\r").strip().startswith("\\part*{原始内容}"))
    # 框架区外、documentclass 之后的「编译骨架」区（迁移跟踪表）
    dc = next(i for i, l in enumerate(lines) if l.rstrip("\r").strip().startswith("\\documentclass"))
    skel = tree(lines, dc, oi, "skel")
    fw = tree(lines, fr_a, fr_b, "fw")
    od = tree(lines, oi, len(lines), "old")

    print("=" * 80)
    print("%s  总 %d 行" % (f, len(lines)))
    print("  · 停用框架区 L%d~L%d : %d 行，标题 %d（%s）"
          % (fr_a + 1, fr_b, fr_b - fr_a,
             len(fw), dict((k, sum(1 for x in fw if x[0] == k)) for k in ("part", "chapter", "section", "subsection"))))
    print("  · 编译骨架区 L%d~L%d : %d 行，标题 %d"
          % (dc + 1, oi, oi - dc, len(skel)))
    print("  · 原始内容区 L%d~%d : %d 行，标题 %d（%s）"
          % (oi + 1, len(lines), len(lines) - oi,
             len(od), dict((k, sum(1 for x in od if x[0] == k)) for k in ("part", "chapter", "section", "subsection"))))

    fw_norm = {}
    for lvl, t, ln in fw:
        fw_norm.setdefault(norm(t), []).append((lvl, t))
    # 逐级覆盖：旧区的 chapter / section 在框架中是否存在
    for lvl in ("chapter", "section"):
        old_at = [x for x in od if x[0] == lvl]
        miss = [x for x in old_at if norm(x[1]) not in fw_norm]
        # 退一步：包含关系兜底
        miss2 = []
        for lvl2, t, ln in miss:
            n = norm(t)
            if n and (any(n in k or k in n for k in fw_norm if k)):
                continue
            miss2.append((lvl2, t, ln))
        print("  · 旧区 %s %d 个 → 框架中精确缺失 %d，宽松后缺失 %d"
              % (lvl, len(old_at), len(miss), len(miss2)))
        for lvl2, t, ln in miss2[:40]:
            print("        [缺] L%-6d %s" % (ln, t[:80]))
