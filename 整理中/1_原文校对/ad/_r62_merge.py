# -*- coding: utf-8 -*-
"""r62：合并空壳章「两性生殖系统」入「性生理基础」。

改动（book.tex 仅 3 处，正文段落逐字保留，不增删任何文字内容）：
  1) \chapter{两性生殖系统}（L398）-> 注释行（保留痕迹，便于溯源）
  2) 原概述段（本章详细介绍了男性和女性生殖系统…，L400）-> 整行移出
  3) 「性生理基础」章首引言段之后插入：空行 + 原概述段（逐字不动）
行数守恒（56622 -> 56622）。
用法：python _r62_merge.py [apply]   （不带参数 = dry-run）
"""
import io, os, sys

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
PATH = os.path.join(BASE, "book.tex")

CH_LINE = "\\chapter{两性生殖系统}"
PARA_SIG = "本章详细介绍了男性和女性生殖系统的结构、功能及相关生理过程。"
INTRO_SIG = "性生理基础是理解人类性行为与性功能的重要起点。"
NOTE = "% r62（2026-09-18）：空壳章「两性生殖系统」已并入下章「性生理基础」，原概述段移至其章首引言之后。"


def load(p):
    raw = io.open(p, encoding="utf-8", newline="").read()
    assert "\r\n" in raw, "源文件应为 CRLF"
    lines = raw.replace("\r\n", "\n").split("\n")
    if lines and lines[-1] == "":
        lines.pop()
        tail_nl = True
    else:
        tail_nl = False
    return lines, tail_nl


def save(p, lines, tail_nl):
    s = "\r\n".join(lines) + ("\r\n" if tail_nl else "")  # 源文件为 CRLF，必须按 CRLF 写回
    io.open(p, "w", encoding="utf-8", newline="").write(s)
    b = io.open(p, "rb").read()
    assert b.count(b"\r\n") == b.count(b"\n") and b.count(b"\r") == b.count(b"\r\n"), "CRLF 写回失败"


def transform(lines):
    """返回 (新行列表, 说明)。全部改动基于内容签名，命中必须唯一。"""
    ch_idx = [i for i, l in enumerate(lines) if l.strip() == CH_LINE]
    assert len(ch_idx) == 1, ("chapter 锚不唯一", ch_idx)
    ci = ch_idx[0]

    para_idx = [i for i, l in enumerate(lines) if PARA_SIG in l]
    assert len(para_idx) == 1, ("概述段锚不唯一", para_idx)
    pi = para_idx[0]
    assert ci < pi < ci + 5, ("概述段不在壳章内", ci, pi)

    intro_idx = [i for i, l in enumerate(lines) if INTRO_SIG in l]
    assert len(intro_idx) == 1, ("引言段锚不唯一", intro_idx)
    ii = intro_idx[0]
    assert ii == pi + 4, ("引言段与壳章相对位置异常", pi, ii)

    para = lines[pi]
    assert lines[ci + 1].strip() == "" and lines[pi + 1].strip() == "", "壳章空行结构异常"
    assert lines[ii + 1].strip() == "", "引言段后应有空行"

    out = list(lines)
    notes = []
    # 1) 章标题行 -> 注释行
    out[ci] = NOTE
    notes.append("L%d: \\chapter{两性生殖系统} -> 注释行" % (ci + 1))
    # 2) 删除概述段整行（连同其后空行，避免连续双空行）
    del out[pi]
    assert out[pi].strip() == ""
    del out[pi]
    notes.append("L%d: 概述段整行移出" % (pi + 1))
    # 3) 引言段（新下标 ii-2 之后）插入：概述段 + 空行
    ii2 = [k for k, l in enumerate(out) if INTRO_SIG in l]
    assert len(ii2) == 1
    j = ii2[0]
    assert out[j + 1].strip() == ""
    out[j + 1:j + 1] = ["", para]
    notes.append("L%d: 章首引言后插入原概述段（逐字未动）" % (j + 2))
    return out, notes


def main():
    apply = len(sys.argv) > 1 and sys.argv[1] == "apply"
    lines, tail_nl = load(PATH)
    n0 = len(lines)
    out, notes = transform(lines)
    for x in notes:
        print(x)
    print("行数 %d -> %d" % (n0, len(out)))
    # 守恒校验：删除行集与插入行集
    removed = [l for l in lines if l not in out or out.count(l) < lines.count(l)]
    print("多重集差（应仅为章标题行与空行）:")
    a = list(lines); b = list(out)
    for x in [NOTE]:
        pass
    import collections
    ca, cb = collections.Counter(lines), collections.Counter(out)
    diff = ca - cb
    add = cb - ca
    for k, v in diff.items():
        print("  -", v, repr(k[:60]))
    for k, v in add.items():
        print("  +", v, repr(k[:60]))
    assert diff == collections.Counter({CH_LINE: 1}), "意外删除: %r" % dict(diff)
    assert add == collections.Counter({NOTE: 1}), "意外新增: %r" % dict(add)
    if apply:
        save(PATH, out, tail_nl)
        print("APPLIED")
    else:
        print("DRY-RUN（加 apply 落盘）")


if __name__ == "__main__":
    main()
