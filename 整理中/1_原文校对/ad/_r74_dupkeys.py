# -*- coding: utf-8 -*-
"""r74 数据层重复键体检：找出所有跨章重名的 \subsection 标题。

用途：数据层的 NEW 以"小节标题"为 key，而 apply 执行器按标题在骨架区定位锚行。
若同一标题在全骨架区出现多次，就会出现歧义（可能命中已有正文的那一个）。
本脚本列出所有重名小节，供撰写前核对，避免 dry-run 被跳过。
"""

import re
import collections

P = "book.tex"
raw = open(P, "r", encoding="utf-8", newline="").read()
lines = raw.split("\n")

old = next(i for i, l in enumerate(lines) if l.startswith("\\part{old}"))
skel = lines[:old]

SUB = re.compile(r"^\\subsection\{(.*)\}\s*(%.*)?$")

hits = collections.defaultdict(list)  # 标题 -> [行号]
for i, l in enumerate(skel):
    m = SUB.match(l)
    if m:
        hits[m.group(1).strip()].append(i + 1)

dup = {k: v for k, v in hits.items() if len(v) > 1}

print("骨架区 \\subsection 总数 = %d，去重后 = %d，重名 %d 个"
      % (sum(len(v) for v in hits.values()), len(hits), len(dup)))
print()

if dup:
    for k, v in sorted(dup.items(), key=lambda x: x[1][0]):
        print("  %-28s  x%d  行号: %s" % (k, len(v), ", ".join(map(str, v))))
else:
    print("  无重名小节。")
