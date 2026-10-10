# -*- coding: utf-8 -*-
r"""r76 收尾：把「原始内容区」转为注释存档（\iffalse … \fi），不物理删除。

用法: python _r76_archive.py male [dry-run|apply]
"""
import io
import re
import shutil
import sys
import time

sys.stdout.reconfigure(encoding="utf-8")

VOL = sys.argv[1] if len(sys.argv) > 1 else "male"
MODE = sys.argv[2] if len(sys.argv) > 2 else "dry-run"
fname = VOL + ".tex"

raw = io.open(fname, encoding="utf-8", newline="").read()
assert raw.count("\r\n") == raw.count("\n"), fname + " 应为纯 CRLF"
lines = raw.split("\n")

oi = next(i for i, l in enumerate(lines) if l.rstrip("\r").strip().startswith("\\part*{原始内容}"))
# 归档终点：旧区末尾的「参考资料」章之前（该章保留在卷尾编译）
bk = next(i for i in range(oi, len(lines)) if re.match(r"^%\s*参考资料", lines[i].rstrip("\r").strip()))
assert bk > oi
# 旧区内不得含 \fi（否则会提前终止 \iffalse 跳过）
bad = [i + 1 for i in range(oi, bk) if re.search(r"\\fi\b", lines[i])]
assert not bad, "旧区内含 \\fi，位于 L%s，不能直接 \\iffalse 包裹" % bad[:5]

print("=" * 78)
print("%s  旧区 L%d ~ L%d（保存 L%d「%s」之后的内容）" % (fname, oi + 1, bk, bk + 1, lines[bk].rstrip("\r")[:40]))

INS = {
    oi: ["\\iffalse  % ── 原始内容区（内容已迁入上方 r72 骨架，此处转为注释存档；如需核对可编译时改 \\iftrue）\r"],
    bk: ["\\fi  % ── 原始内容区存档结束\r"],
}
out = []
for i, l in enumerate(lines):
    if i in INS:
        out.extend(INS[i])
    out.append(l)

ns = "\n".join(out)
assert "\n" not in ns.replace("\r\n", ""), fname + " 出现裸 \\n"
assert ns.count("\r\n") == raw.count("\r\n") + sum(len(v) for v in INS.values()), "CRLF 数异常"
assert raw.count("{") - raw.count("}") == ns.count("{") - ns.count("}"), "花括号 delta 变"
print("  行数 %d -> %d；CRLF %d -> %d；delta 不变  [OK]"
      % (len(lines), len(out), raw.count("\r\n"), ns.count("\r\n")))
print("  插入：L%d 「 \\iffalse … 」／ L%d 「 \\fi 」" % (oi + 1, bk + 2))

if MODE == "apply":
    st = time.strftime("%Y%m%d_%H%M%S")
    shutil.copy2(fname, fname + ".arcbak_" + st)
    io.open(fname, "w", encoding="utf-8", newline="").write(ns)
    print("  已写盘（备份 %s.arcbak_%s）" % (fname, st))
else:
    print("  DRY-RUN，未写盘。")
