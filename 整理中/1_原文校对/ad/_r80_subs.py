# -*- coding: utf-8 -*-
import io, re
lines = [x.rstrip("\r") for x in io.open("2_female.tex", encoding="utf-8").read().split("\n")]
secs = []
for i in range(7083, len(lines)):
    m = re.match(r"^\\section\{([^}]*)\}", lines[i])
    if m:
        secs.append((i, m.group(1)))
for k, (i, t) in enumerate(secs):
    e = secs[k + 1][0] if k + 1 < len(secs) else len(lines)
    subs = []
    for j in range(i + 1, e):
        m2 = re.match(r"^\\subsection\{([^}]*)\}", lines[j])
        if m2:
            subs.append(m2.group(1))
    print("L%d %s (%d行, %d子节)" % (i + 1, t, e - i, len(subs)))
    for s in subs:
        print("    - " + s)
