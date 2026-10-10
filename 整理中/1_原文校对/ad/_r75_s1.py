# -*- coding: utf-8 -*-
r"""r75 S1：修两卷 preamble 的 ctex 编号损坏 + 统一 \part + 剥离"第X篇："冗余前缀。

用法: python _r75_s1.py [dry-run|apply]

改动项：
  A. ctexset：part/name={。卷}->{第,篇}；chapter/name={。章}->{第,章}；删除损坏的 section/name 与
     section/subsection 编号覆盖（与 book.tex 对齐，用 ctexbook 默认）。
  B. 所有 \part{第X篇：NAME} / \part*{第X篇：NAME} -> \part{NAME}。
  C. 紧跟其后的重复 \addcontentsline{toc}{part}{...} 行删除（否则 part 的目录项出现两次）。
  D. 更新「使用说明」第 4 条（原文写"篇一律用 \part*…待授权修正"，现已修正）。

不变量：
  · 两卷为纯 CRLF，写回后不得出现裸 \n，CRLF 数按插入/删除行数精确核对
  · \part*{原始内容} 起逐字一致
  · 花括号 delta 不变
"""
import io
import re
import shutil
import sys
import time

sys.stdout.reconfigure(encoding="utf-8")

MODE = sys.argv[1] if len(sys.argv) > 1 else "dry-run"
assert MODE in ("dry-run", "apply"), MODE

PART_RE = re.compile(r"^\\part\*?\{第[一二三四五六七八九十]+篇[：:]\s*(.*)\}$")
ADDC_RE = re.compile(r"^\\addcontentsline\{toc\}\{part\}\{.*\}$")

OLDSET = "\r\n".join([
    "\\ctexset{",
    "    part/name={。卷},",
    "    part/number={\\chinese{part}},",
    "    chapter/name={。章},",
    "    chapter/number={\\chinese{chapter}},",
    "    section/name={。节},",
    "    section/number={\\arabic{section}},",
    "    subsection/number={\\arabic{section}.\\arabic{subsection}},",
]) + "\r"
NEWSET = "\r\n".join([
    "\\ctexset{",
    "    part/name={第,篇},",
    "    part/number={\\chinese{part}},",
    "    chapter/name={第,章},",
    "    chapter/number={\\chinese{chapter}},",
]) + "\r"

OLDNOTE = "\r\n".join([
    "%   4. 篇一律用 \\part*（不带编号），避免触发 preamble 中 part/name={。卷} 的可疑格式；",
    "%      建议后续（待授权）把 {。卷}/{。章} 修正为 {第,卷}/{第,章}。",
]) + "\r"
NEWNOTE = "\r\n".join([
    "%   4. 篇用 \\part（带编号），编号格式见 preamble 的 ctexset（part/name={第,篇}）。",
    "%      （2026-09-22 已修正原损坏的 {。卷}/{。章}/{。节}；此前为规避该格式一律改用 \\part*，现已恢复编号。）",
]) + "\r"

for fname in ("female.tex", "male.tex"):
    print("=" * 78)
    print("文件:", fname)
    raw = io.open(fname, encoding="utf-8", newline="").read()
    assert raw.count("\r\n") == raw.count("\n"), fname + " 应为纯 CRLF"
    lines = raw.split("\n")
    new = list(lines)

    # --- A. ctexset ---
    txt = "\n".join(lines)
    assert txt.count(OLDSET) == 1, "%s ctexset 锚命中 %d" % (fname, txt.count(OLDSET))
    txt = txt.replace(OLDSET, NEWSET)
    assert txt.count(OLDNOTE) == 1, "%s 使用说明锚命中 %d" % (fname, txt.count(OLDNOTE))
    txt = txt.replace(OLDNOTE, NEWNOTE)
    new = txt.split("\n")
    print("  A. ctexset：{。卷}/{。章}/{。节} -> {第,篇}/{第,章}，删 section 覆盖  [OK]")
    print("  D. 使用说明第 4 条已更新                                   [OK]")

    # --- B/C. 篇标题与重复 addcontentsline ---
    drop = set()
    conv = 0
    for i, l in enumerate(new):
        s = l.rstrip("\r")
        m = PART_RE.match(s)
        if not m:
            continue
        title = m.group(1).strip()
        assert title, "%s L%d 篇标题为空" % (fname, i + 1)
        new[i] = "\\part{%s}\r" % title
        conv += 1
        # 紧跟其后的重复 addcontentsline
        j = i + 1
        if j < len(new) and ADDC_RE.match(new[j].rstrip("\r")):
            drop.add(j)
            print("      L%-6d \\part{%s}  (删去 L%d 重复目录项)" % (i + 1, title, j + 1))
        else:
            print("      L%-6d \\part{%s}" % (i + 1, title))
    print("  B. 转换篇标题 %d 个；C. 删除重复 \\addcontentsline %d 行" % (conv, len(drop)))
    exp_conv = {"female.tex": 10, "male.tex": 9}[fname]   # 框架区 female 5 / male 4，另加编译骨架各 5
    assert conv == exp_conv, "%s 篇标题应为 %d 个，实为 %d" % (fname, exp_conv, conv)
    assert len(drop) == 5, "%s 重复 \\addcontentsline 应为 5 行，实为 %d" % (fname, len(drop))

    out = [l for i, l in enumerate(new) if i not in drop]

    # --- 不变量 ---
    ns = "\n".join(out)
    ns_no_cr = ns.replace("\r\n", "")
    assert "\n" not in ns_no_cr, fname + " 出现裸 \\n"
    exp = len(drop) + OLDSET.count("\r\n") - NEWSET.count("\r\n")
    assert raw.count("\r\n") - ns.count("\r\n") == exp, \
        "%s CRLF 数异常：实减 %d，预期 %d" % (fname, raw.count("\r\n") - ns.count("\r\n"), exp)
    assert raw.count("{") - raw.count("}") == ns.count("{") - ns.count("}"), fname + " 花括号 delta 变"
    oi0 = next(i for i, l in enumerate(lines) if l.rstrip("\r").strip().startswith("\\part*{原始内容}"))
    oi1 = next(i for i, l in enumerate(out) if l.rstrip("\r").strip().startswith("\\part*{原始内容}"))
    assert lines[oi0:] == out[oi1:], fname + " 原始内容区被改动"
    # 全文必须再无损坏格式（仅允许出现在说明性注释里）
    for i, l in enumerate(out):
        s = l.rstrip("\r").strip()
        if s.startswith("%"):
            continue
        assert "{。卷}" not in s and "{。章}" not in s and "{。节}" not in s, \
            "%s L%d 仍有损坏格式: %s" % (fname, i + 1, s[:80])
    print("  不变量：CRLF %d->%d  delta 不变  原始内容区逐字一致  [OK]"
          % (raw.count("\r\n"), ns.count("\r\n")))
    print("  行数 %d -> %d" % (len(lines), len(out)))

    if MODE == "apply":
        stamp = time.strftime("%Y%m%d_%H%M%S")
        shutil.copy2(fname, fname + ".s1bak_" + stamp)
        io.open(fname, "w", encoding="utf-8", newline="").write(ns)
        print("  已写盘（备份 %s.s1bak_%s）" % (fname, stamp))
    else:
        print("  DRY-RUN，未写盘。")
