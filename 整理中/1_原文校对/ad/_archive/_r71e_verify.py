# -*- coding: utf-8 -*-
"""r71e：验证插入结果 —— 与 _backup_r71 中的原版逐段比对。只读。"""
import io

for fn, after in (("female.tex", "\\mainmatter"), ("male.tex", "\\listoftables")):
    old = io.open("_backup_r71/" + fn, encoding="utf-8", newline="").read()
    new = io.open(fn, encoding="utf-8", newline="").read()
    ol, nl = old.split("\r\n"), new.split("\r\n")
    a = next(i for i, l in enumerate(ol) if l.strip() == after)
    # 新文件里同名锚的位置应相同，且其前行与旧文件逐字一致
    b = next(i for i, l in enumerate(nl) if l.strip() == after)
    assert nl[: b + 1] == ol[: a + 1], "插入点之前不一致！"
    tail = ol[a + 1:]
    assert nl[len(nl) - len(tail):] == tail, "插入点之后不一致！"
    print("%s: 前 %d 行逐字一致；尾 %d 行逐字一致；中间插入 %d 行（原 %d -> 新 %d 行）"
          % (fn, b + 1, len(tail), len(nl) - len(ol), len(ol), len(nl)))
    print("  CRLF 一致性: 旧 %d 新 %d（差 = 插入行数 %d）"
          % (old.count("\r\n"), new.count("\r\n"), new.count("\r\n") - old.count("\r\n")))
