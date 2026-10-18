# -*- coding: utf-8 -*-
"""r77: 抽查待提取块的首尾边界。"""
import io

lines = [x.rstrip("\r") for x in io.open("book.tex", encoding="utf-8", newline="").read().split("\n")]

def show(a, b, lab):
    print("=" * 96)
    print("%s  L%d~L%d" % (lab, a, b))
    print("---- 首 12 行 ----")
    for i in range(a - 1, min(a + 11, b)):
        print("  %-6d| %s" % (i + 1, lines[i][:116]))
    print("---- 末 8 行 ----")
    for i in range(max(b - 8, a), b):
        print("  %-6d| %s" % (i + 1, lines[i][:116]))

show(3867, 4221, "骨架 新婚首夜")
show(5874, 5938, "骨架 体位基础节")
show(27247, 27320, "旧区 体位基础章")
show(59379, 59412, "巨块 男上女下")
show(53691, 53701, "巨块 前戏与爱抚 section 首")
