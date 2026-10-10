# -*- coding: utf-8 -*-
r"""r74 两卷执行器：把正文插到 female.tex / male.tex 骨架区的 \subsection 行之后。

用法: python _r74_volapply.py <data_module> [dry-run|apply]
数据模块需定义 VOL = { "female.tex": {小节: 正文}, "male.tex": {...} }

关键差异（与 book.tex 不同）：
  · 两卷为纯 CRLF，必须 newline="" 读写并保持 CRLF
  · 骨架区边界 = \part*{原始内容} 之前；其后逐字不得改动
"""
import io, sys, importlib, re

sys.stdout.reconfigure(encoding="utf-8")

MOD_NAME = sys.argv[1]
MODE = sys.argv[2] if len(sys.argv) > 2 else "dry-run"
assert MODE in ("dry-run", "apply"), MODE

mod = importlib.import_module(MOD_NAME)
VOL = mod.VOL

H = re.compile(r"^\\(part|chapter|section|subsection)\*?\{(.*?)\}")
ALLOW_EN = set("""
STI HIV HPV HSV HBV HCV PPND TRT SHBG GnRH TSH CO2
""".split())

for fname, JOBS in VOL.items():
    print("=" * 70)
    print("文件:", fname)
    raw = io.open(fname, encoding="utf-8", newline="").read()
    assert raw.count("\r\n") > 0, fname + " 预期为 CRLF"
    lines = raw.split("\n")
    # 骨架区边界
    skel_end = next(i for i, l in enumerate(lines)
                    if l.rstrip("\r").strip().startswith("\\part*{原始内容}"))

    print("=== 校验 1：锚行定位 ===")
    POS = {}
    for t in JOBS:
        loc = [i + 1 for i in range(skel_end)
               if lines[i].rstrip("\r").strip() == "\\subsection{%s}" % t]
        assert len(loc) == 1, "%s 小节 %s 命中 %d 处（应恰好 1 处）" % (fname, t, len(loc))
        POS[t] = loc[0]
        print("    + %s @L%d" % (t, loc[0]))

    print("=== 校验 2：空槽确认（幂等）===")
    plan, skip = [], []
    for t, ln in POS.items():
        j = ln
        while j < skel_end and (not lines[j].strip() or lines[j].strip().startswith("%")):
            j += 1
        has = j < skel_end and not re.match(
            r"^\\(part|chapter|section|subsection)\*?\{", lines[j].rstrip("\r").strip())
        (skip if has else plan).append((ln, t))
    print("    待插入 %d，已有正文（跳过）%d" % (len(plan), len(skip)))
    for ln, t in skip:
        print("      - 跳过:", t)

    print("=== 校验 3：内容洁净度 ===")
    for t, body in JOBS.items():
        assert not body.lstrip().startswith("\\subsection"), t + " 内容自带标题"
        assert "**" not in body, t + " 含 **"
        assert body.count("{") - body.count("}") == 0, t + " 花括号不配平"
        for c in body:
            o = ord(c)
            if (o < 32 and c != "\n") or o == 127 or 0x80 <= o <= 0x9F:
                raise AssertionError("%s 含非法控制字符 U+%04X" % (t, o))
        for i, l in enumerate(body.split("\n")):
            s = l.strip()
            if s.startswith("%"):
                continue
            j = 0
            while True:
                p = l.find("%", j)
                if p < 0:
                    break
                if p > 0 and l[p - 1] == "\\":
                    j = p + 1
                    continue
                raise AssertionError("%s 第%d行未转义 %%" % (t, i + 1))
        # 列表首行必须是 \item
        depth, started = 0, False
        for i, l in enumerate(body.split("\n")):
            s = l.strip()
            if re.match(r"^\\begin\{(itemize|enumerate)\}", s):
                depth += 1
                if depth == 1:
                    started = False
                continue
            if re.match(r"^\\end\{(itemize|enumerate)\}", s):
                depth = max(0, depth - 1)
                continue
            if depth > 0 and s and not s.startswith("%"):
                if not started and not s.startswith("\\item"):
                    raise AssertionError("%s 第%d行列表首行缺 \\item" % (t, i + 1))
                started = True
        # 英文词
        for m in re.finditer(r"(?<![A-Za-z\\{])([A-Za-z]{3,})(?![A-Za-z}])", body):
            w = m.group(1)
            if w in ALLOW_EN:
                continue
            if re.match(r"^[A-Za-z]*(col|title|font|rule|skin|arc|width|height)[A-Za-z]*$", w):
                continue
            if w in ("pink", "white", "black", "red", "blue", "green"):
                continue
            raise AssertionError("%s 疑似混入英文词: %s" % (t, w))
    print("    [OK] %d 条通过（%d 行）" % (len(JOBS), sum(len(v.split("\n")) for v in JOBS.values())))

    # 预演插入（倒序，正文行尾部补 \r 以维持 CRLF）
    out = list(lines)
    added = 0
    for ln, t in sorted(plan, key=lambda x: -x[0]):
        body = [x for x in JOBS[t].split("\n")]
        while body and not body[0].strip():
            body.pop(0)
        while body and not body[-1].strip():
            body.pop()
        ins = ["\r"] + [x + "\r" for x in body]
        added += len(ins)
        out[ln:ln] = ins

    new_text = "\n".join(out)
    print("=== 预演统计 ===")
    print("  行数 %d -> %d（净增 %d）" % (len(lines), len(out), len(out) - len(lines)))
    bd = raw.count("{") - raw.count("}")
    nd = new_text.count("{") - new_text.count("}")
    print("  花括号 delta: %d -> %d" % (bd, nd))
    assert bd == nd, "花括号净值改变"
    # 原始内容区逐字一致
    new_end = next(i for i, l in enumerate(out)
                   if l.rstrip("\r").strip().startswith("\\part*{原始内容}"))
    ok = lines[skel_end:] == out[new_end:]
    print("  \\part*{原始内容} 起逐字一致:", ok)
    assert ok, "原始内容区被改动"
    assert new_text.count("\r\n") == raw.count("\r\n") + added, "CRLF 数量异常"
    assert "\n" not in new_text.replace("\r\n", ""), "出现裸 \\n（破坏 CRLF）"

    if MODE == "dry-run":
        print("DRY-RUN 完成，未写盘。")
    else:
        io.open(fname, "w", encoding="utf-8", newline="").write(new_text)
        print("已写盘: %s  %d 行 %d 字节" % (fname, len(out), len(new_text.encode("utf-8"))))
