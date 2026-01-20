import re

# 读取Images目录中的图片文件列表
with open('images_list.txt', 'r', encoding='utf-8') as file:
    existing_images = [line.strip() for line in file if line.strip()]

# 读取LaTeX文件
with open('converted_69_positions.tex', 'rb') as file:
    content_bytes = file.read()

content = content_bytes.decode('latin-1')

# 提取所有引用的图片文件名
referenced_images = re.findall(r'\\includegraphics\{Images/(.*?)\}', content)

# 找出缺少的图片文件
missing_images = []
for img in referenced_images:
    if img not in existing_images:
        missing_images.append(img)

# 输出结果
print(f"LaTeX文件中引用的图片总数: {len(referenced_images)}")
print(f"Images目录中实际存在的图片总数: {len(existing_images)}")

if missing_images:
    print(f"缺少的图片文件 ({len(missing_images)} 个):")
    for img in missing_images:
        print(f"  - {img}")
else:
    print("所有引用的图片文件都存在！")
