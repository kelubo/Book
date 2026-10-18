# -*- coding: utf-8 -*-
import io
b = io.open('book.tex', encoding='utf-8', newline='').read()
CR = '\r\n'
a = '把这些反应当作"需要了解的身体信息"，而不是"羞于启齿的秘密"。' + CR + '\\end{tcolorbox}'
print('anchor count:', b.count(a))
a2 = '\\part{避孕与性健康}' + CR + CR + '\\chapter{避孕方法}'
print('anchor2 count:', b.count(a2))
