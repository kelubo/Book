# -*- coding: utf-8 -*-
"""r39 扫描：三卷 Markdown 格式残留全量分类统计
1. 裸 ection 基线（用户称已自修，应为 0）
2. **bold** 对（环境内/外、跨行奇数风险）
3. 行首 bullet（- / *），区分在 itemize/enumerate 环境内/外
4. 行首数字列表 1. （环境内/外）
5. 行首 # 标题、表格 | 开头、代码块 ```
"""
import io, os, re
BASE = r'D:\Git\Book\整理中\1_原文校对\ad'
FILES = ['book.tex', 'female.tex', 'male.tex']

LIST_ENVS = {'itemize', 'enumerate', 'description'}

for fn in FILES:
    lines = io.open(os.path.join(BASE, fn), encoding='utf-8', newline='').read().split('\r\n')
    print('=' * 20, fn, '(%d lines)' % len(lines), '=' * 20)

    ect = [(i+1, l.strip()[:50]) for i, l in enumerate(lines) if re.match(r'^\s*ection\{', l)]
    print('0. bare ection{ =', len(ect), ect[:6])

    bold_lines = 0; bold_pairs = 0; bold_odd = []
    in_env_stack = []
    b_in = b_out = 0
    dash_in = dash_out = 0; star_in = star_out = 0
    num_in = num_out = 0
    dash_lines_out = []; star_lines_out = []
    num_lines_out = []
    hash_lines = []; table_lines = 0; code_lines = 0
    sample_in_dash = []; sample_out_dash = []

    for i, l in enumerate(lines):
        st = l.strip()
        # 环境栈更新（先处理本行的 begin/end，再判断行的归属——简化：以行为单位，先记录判断前的栈）
        was_in_list = any(e in LIST_ENVS for e in in_env_stack)
        for m in re.finditer(r'\\(begin|end)\{([a-zA-Z*]+)\}', l):
            if m.group(1) == 'begin':
                in_env_stack.append(m.group(2))
            else:
                if in_env_stack and in_env_stack[-1] == m.group(2):
                    in_env_stack.pop()
                elif m.group(2) in in_env_stack:
                    # 弹到匹配处
                    while in_env_stack:
                        top = in_env_stack.pop()
                        if top == m.group(2):
                            break
        now_in_list = any(e in LIST_ENVS for e in in_env_stack)
        in_list = was_in_list or now_in_list

        # **bold**
        stars = l.count('**')
        if stars:
            bold_lines += 1
            bold_pairs += len(re.findall(r'\*\*[^*]+\*\*', l))
            if stars % 2 == 1:
                bold_odd.append(i+1)
            if in_list: b_in += 1
            else: b_out += 1
        # 行首 bullet -
        if re.match(r'^-\s+', st):
            if in_list:
                dash_in += 1
                if len(sample_in_dash) < 3: sample_in_dash.append((i+1, st[:60]))
            else:
                dash_out += 1
                if len(dash_lines_out) < 200: dash_lines_out.append(i+1)
        # 行首 bullet *
        if re.match(r'^\*\s+', st):
            if in_list: star_in += 1
            else:
                star_out += 1
                if len(star_lines_out) < 200: star_lines_out.append(i+1)
        # 行首数字列表
        if re.match(r'^\d{1,2}[.、)]\s*\S', st) and not st.startswith('1.'):
            pass
        if re.match(r'^\d{1,2}\.\s+\S', st):
            if in_list: num_in += 1
            else:
                num_out += 1
                if len(num_lines_out) < 200: num_lines_out.append(i+1)
        # # 标题
        if re.match(r'^#{1,6}\s', st):
            hash_lines.append((i+1, st[:50]))
        # 表格/代码块
        if st.startswith('|'): table_lines += 1
        if st.startswith('```'): code_lines += 1

    print('1. **bold**: lines=%d, pairs=%d, in_list_lines=%d, out_lines=%d, odd_star_lines(跨行风险)=%s' % (
        bold_lines, bold_pairs, b_in, b_out, bold_odd[:10]))
    print('2. bullet "- ": in_list=%d, out_list=%d' % (dash_in, dash_out))
    print('   sample in_list:', sample_in_dash)
    print('   out_list 行号样本:', dash_lines_out[:25], '...' if len(dash_lines_out) > 25 else '')
    print('3. bullet "* ": in_list=%d, out_list=%d' % (star_in, star_out))
    print('   out_list 行号样本:', star_lines_out[:25], '...' if len(star_lines_out) > 25 else '')
    print('4. "N. " 数字列表: in_list=%d, out_list=%d' % (num_in, num_out))
    print('   out_list 行号样本:', num_lines_out[:20], '...' if len(num_lines_out) > 20 else '')
    print('5. "# " 标题行 =', len(hash_lines), hash_lines[:6])
    print('6. 表格 | 行 =', table_lines, ' 代码块 ``` 行 =', code_lines)
    print()
