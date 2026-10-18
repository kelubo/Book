# -*- coding: utf-8 -*-
import io, re
lines = [x.rstrip("\r") for x in io.open("2_female.tex", encoding="utf-8").read().split("\n")]
# 框架区 L285..6490
starts = []
for i in range(285, 6490):
    m = re.match(r"^\\(chapter|section)\{([^}]*)\}", lines[i])
    if m:
        starts.append((i, m.group(1), m.group(2)))
for k, (i, lv, t) in enumerate(starts):
    e = starts[k + 1][0] if k + 1 < len(starts) else 6490
    subs = []
    for j in range(i + 1, e):
        m2 = re.match(r"^\\subsection\{([^}]*)\}", lines[j])
        if m2:
            subs.append(m2.group(1))
    print("L%d %s %s (%d行) 子节: %s" % (i + 1, lv, t, e - i, " | ".join(subs) if subs else "-"))
