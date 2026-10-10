# -*- coding: utf-8 -*-
"""r41 插入后验证：新节定位、术语表、静态校验、行尾检查"""
import io, os, re

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
FN = "book.tex"

with io.open(os.path.join(BASE, FN), "r", encoding="utf-8", newline="") as f:
    raw = f.read()

print("== 1. bare LF / CR 残留 ==")
print("  bare LF 数:", raw.count("\n") - raw.count("\r\n"))
print("  单独 CR 数:", raw.replace("\r\n", "").count("\r"))

lines = raw.split("\r\n")
print("总行数:", len(lines))

print("\n== 2. 五个新节标题行首匹配（各应=1） ==")
titles = [
    "\\section{丁克家庭：选择不育生活的亲密关系经营}",
    "\\section{性行为中的意外损伤与家庭急救}",
    "\\section{烧伤、毁容与截肢者的性重建：当身体图式被改变}",
    "\\section{异地恋与长期分离的亲密维护}",
    "\\section{数字遗产与身后的亲密痕迹}",
]
for t in titles:
    hits = [i for i, ln in enumerate(lines, 1) if ln.strip() == t]
    status = "OK" if len(hits) == 1 else "!!"
    print(f"  [{status}] x{len(hits)} @L{hits} {t[:40]}")

print("\n== 3. 术语表新词条（应=1 且在 description 环境内） ==")
gterms = ["CSBD（强迫性性行为障碍）", "丁克家庭（DINK）", "延续性联结（Continuing Bonds）",
          "数字遗产（Digital Legacy）", "幻肢感（Phantom Limb Sensation）", "异地恋（Long-Distance Relationship）"]
for t in gterms:
    hits = [i for i, ln in enumerate(lines, 1) if ln.strip().startswith("\\item[" + t + "]")]
    status = "OK" if len(hits) == 1 else "!!"
    print(f"  [{status}] x{len(hits)} @L{hits} {t}")

print("\n== 4. 插入点上下文抽查 ==")
checks = [
    ("丁克节开头+锚后", [l for l in titles][0]),
    ("急救节前一行应为空/后接时长节", "\\section{性交时长、频率与\"正常\"的标准}"),
]
# 丁克节首尾
idx = next(i for i, ln in enumerate(lines) if ln.strip() == titles[0])
print(f"--- 丁克节 @L{idx+1}（前2行/首行/末3行） ---")
for j in range(idx-2, idx+1):
    print(f"  L{j+1}: {lines[j].strip()[:60]!r}")
tail = idx
cnt = 0
while cnt < 3 or not lines[tail].strip().startswith("\\end{tcolorbox}"):
    tail += 1
    cnt += 1
for j in range(tail, tail+4):
    print(f"  L{j+1}: {lines[j].strip()[:60]!r}")

print("\n== 5. 静态校验（剔注释后括号配平 + 环境栈） ==")
# 复用 _r15_verify2 的核心逻辑
code_lines = []
for ln in lines:
    # 去注释行（行首%）与行内注释
    s = ln
    # 简化处理：按历轮脚本同款——剔除 % 之后内容（忽略 \%）
    out, i, inesc = [], 0, False
    while i < len(s):
        ch = s[i]
        if ch == "\\":
            out.append(ch)
            if i + 1 < len(s):
                out.append(s[i+1])
            i += 2
            continue
        if ch == "%":
            break
        out.append(ch)
        i += 1
    code_lines.append("".join(out))
text = "\n".join(code_lines)
delta = text.count("{") - text.count("}")
print("  花括号配平 delta =", delta)
stack, env_ok, errs = [], True, 0
env_re = re.compile(r"\\(begin|end)\{([^}]+)\}")
for ln in code_lines:
    for m in env_re.finditer(ln):
        if m.group(1) == "begin":
            stack.append(m.group(2))
        else:
            if not stack or stack[-1] != m.group(2):
                env_ok = False
                errs += 1
                if errs <= 5:
                    print("  环境错配:", m.group(2), "栈顶:", stack[-1] if stack else None)
            elif stack:
                stack.pop()
print("  环境栈零错配:", env_ok, "| 未闭合:", len(stack), "| 错配数:", errs)

print("\n== 6. markdown 残留检查 ==")
md = sum(1 for ln in lines if re.match(r"^\s*(#{1,4}\s|\*\*|\|.*\||-\s\*\*)", ln))
print("  可疑 markdown 行:", md)
