import os
import zipfile
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

# 定义函数：提取EPUB文件内容
def extract_epub_content(epub_path, output_path):
    try:
        # 打开EPUB文件（本质是ZIP文件）
        with zipfile.ZipFile(epub_path, 'r') as zf:
            # 查找内容文件
            content_files = []
            for file_info in zf.infolist():
                if file_info.filename.endswith('.html') or file_info.filename.endswith('.xhtml'):
                    content_files.append(file_info.filename)
            
            # 按文件名排序（尽量按章节顺序）
            content_files.sort()
            
            # 提取内容
            content = []
            for file_path in content_files:
                with zf.open(file_path, 'r') as f:
                    html_content = f.read().decode('utf-8', errors='ignore')
                    # 使用BeautifulSoup解析HTML
                    soup = BeautifulSoup(html_content, 'html.parser')
                    # 提取文本
                    text = soup.get_text(separator='\n', strip=True)
                    if text:
                        content.append(text)
            
            # 保存提取的内容
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('\n\n'.join(content))
            
            print(f"成功提取EPUB内容到：{output_path}")
            return True
    except Exception as e:
        print(f"提取EPUB内容失败：{e}")
        return False

# 获取当前目录
current_dir = os.path.dirname(os.path.abspath(__file__))
yy_dir = current_dir

# 查找电子书文件
epub_files = []
azw3_files = []

for file in os.listdir(yy_dir):
    file_path = os.path.join(yy_dir, file)
    if os.path.isfile(file_path):
        if file.endswith('.epub'):
            epub_files.append(file_path)
        elif file.endswith('.azw3'):
            azw3_files.append(file_path)

print(f"找到的EPUB文件：{epub_files}")
print(f"找到的AZW3文件：{azw3_files}")

# 处理EPUB文件
for epub_file in epub_files:
    # 生成输出文件名
    base_name = os.path.basename(epub_file)
    output_name = base_name.replace('.epub', '_content.txt')
    output_path = os.path.join(yy_dir, output_name)
    
    extract_epub_content(epub_file, output_path)

print("\n提取完成！")
