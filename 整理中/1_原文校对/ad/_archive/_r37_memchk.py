# -*- coding: utf-8 -*-
import io, os, glob
D = r'D:\Git\Book\.workbuddy\memory'
print('=== dir listing ===')
for f in sorted(glob.glob(os.path.join(D, '*'))):
    st = os.stat(f)
    print('%8d  %s  %s' % (st.st_size, __import__('time').strftime('%m-%d %H:%M:%S', __import__('time').localtime(st.st_mtime)), f))

P = os.path.join(D, '2026-09-14.md')
raw = open(P, 'rb').read()
print()
print('=== 2026-09-14.md raw bytes =', len(raw))
print('has BOM:', raw[:3] == b'\xef\xbb\xbf')
print('CRLF count =', raw.count(b'\r\n'), ' LF count =', raw.count(b'\n'))
t = io.open(P, encoding='utf-8', newline='').read()
print('contains r25:', '第二十五轮' in t, ' r30:', '第三十轮' in t, ' r36:', '第三十六轮' in t, ' r37:', '第三十七轮' in t)
print()
print('=== full text (first 500 chars) ===')
print(t[:500])
