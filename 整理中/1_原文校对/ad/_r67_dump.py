# -*- coding: utf-8 -*-
"""dump 预览文件的指定区段，检查插节与结构改动效果。"""
import io

s = io.open(r"D:\Git\Book\整理中\1_原文校对\ad\_r67_preview.txt", encoding="utf-8").read().split("\n")

TARGETS = ["\\chapter{前戏与爱抚}", "\\chapter{性功能障碍}", "\\chapter{性爱的多样实践}",
           "\\chapter{求助与资源导航}", "\\part*{附录}", "\\iffalse", "\\fi", "\\chapter{性与年龄}"]
for t in TARGETS:
    idx = [i for i, l in enumerate(s) if l.strip().startswith(t)]
    for i in idx:
        print("\n" + "=" * 74)
        print(">>> %s  @L%d" % (t, i + 1))
        for j in range(max(0, i - 2), min(len(s), i + 46)):
            print("L%5d| %s" % (j + 1, s[j][:100]))
