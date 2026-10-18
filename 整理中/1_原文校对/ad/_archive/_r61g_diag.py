# -*- coding: utf-8 -*-
"""r61g 诊断：定位引号不一致的标题行 + 列出重名新名的既有出处。"""
import os, re, sys, importlib.util

spec = importlib.util.spec_from_file_location(
    "r", r"D:\Git\Book\整理中\1_原文校对\ad\_r61_rename.py")
rm = importlib.util.module_from_spec(spec)
sys.argv = ["x"]
spec.loader.exec_module(rm)

BASE = rm.BASE
Q = '“”"' + "‘’'"
TRANS = {ord(c): '"' for c in '“”"'}
TRANS.update({ord(c): "'" for c in "‘’'"})
TRANS[0x2014] = 0x2014


def norm(s):
    return s.translate(TRANS)


for fn, edits in rm.PLAN.items():
    lines, _ = rm.load(os.path.join(BASE, fn))
    stripped = [l.strip() for l in lines]
    nstripped = [norm(s) for s in stripped]
    titles = rm.cur_titles(lines)
    print("=" * 70)
    print(fn)
    # 1) 锚不匹配的
    bad = 0
    for lv, old, new in edits:
        t = "\\%s{%s}" % (lv, old)
        if t in stripped:
            continue
        nt = norm(t)
        hits = [i for i, s in enumerate(nstripped) if s == nt]
        bad += 1
        if hits:
            print("  [引号差异] L%d" % (hits[0] + 1))
            print("     给我:  %r" % t[:60])
            print("     实际:  %r" % stripped[hits[0]][:60])
        else:
            # 再宽松：忽略所有引号做子串
            base = re.sub(r'[\u201c\u201d"\'‘’]', '', nt)
            cand = [i for i, s in enumerate(nstripped)
                    if re.sub(r'[\u201c\u201d"\'‘’]', '', s) == base]
            print("  [无命中]  %r  宽松命中=%d" % (t[:50], len(cand)))
            if cand:
                print("     实际:  %r" % stripped[cand[0]][:60])
    print("  锚不匹配合计：", bad)
    # 2) 重名新名的既有出处
    print("  -- 重名检查 --")
    for lv, old, new in edits:
        if new == old:
            continue
        occ = [i + 1 for i, s in enumerate(stripped)
               if s.endswith("{%s}" % new) and rm.HEAD_RE.match(s)]
        if occ and ("\\%s{%s}" % (lv, old)) not in stripped:
            print("     新名 %-30s 既有于 L%s   (旧: %s)" % (new, occ[:5], old))
        elif occ:
            print("     新名 %-30s 既有于 L%s   (旧: %s)" % (new, occ[:5], old))
