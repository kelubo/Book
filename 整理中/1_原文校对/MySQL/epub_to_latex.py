import os
import re
from html.parser import HTMLParser
import xml.etree.ElementTree as ET

class XHTMLToLaTeXConverter(HTMLParser):
    def __init__(self):
        super().__init__()
        self.latex_content = []
        self.in_body = False
        self.skip_tags = ['head', 'style', 'script', 'meta', 'link']
        self.current_class = None
        self.current_id = None
        self.list_level = 0
        self.current_list_type = None
        self.in_table = False
        self.in_table_row = False
        self.in_table_cell = False
        self.table_cell_count = 0
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        if tag in self.skip_tags:
            return
            
        if tag == 'body':
            self.in_body = True
            return
            
        if not self.in_body:
            return
            
        if 'class' in attrs_dict:
            self.current_class = attrs_dict['class']
        if 'id' in attrs_dict:
            self.current_id = attrs_dict['id']
            
        if tag == 'p':
            self.latex_content.append('\n\\par ')
            
        elif tag == 'div':
            if 'class' in attrs_dict:
                cls = attrs_dict['class']
                if 'contents-title' in cls:
                    self.latex_content.append('\n\\chapter*{目录}\n')
                elif 'contents1' in cls:
                    self.latex_content.append('\n\\section*{')
                elif 'contents2' in cls:
                    self.latex_content.append('\n\\subsection*{')
                elif 'contents3' in cls:
                    self.latex_content.append('\n\\subsubsection*{')
                    
        elif tag == 'a':
            href = attrs_dict.get('href', '')
            if href:
                self.latex_content.append(f'\\href{{{href}}}{{')
                
        elif tag == 'img':
            src = attrs_dict.get('src', '')
            if src:
                self.latex_content.append(f'\n\\begin{{figure}}[htbp]\n\\centering\n\\includegraphics[width=0.8\\textwidth]{{{src}}}\n\\end{{figure}}\n')
                
        elif tag == 'h1':
            self.latex_content.append('\n\\chapter{')
        elif tag == 'h2':
            self.latex_content.append('\n\\section{')
        elif tag == 'h3':
            self.latex_content.append('\n\\subsection{')
        elif tag == 'h4':
            self.latex_content.append('\n\\subsubsection{')
        elif tag == 'h5':
            self.latex_content.append('\n\\paragraph{')
        elif tag == 'h6':
            self.latex_content.append('\n\\subparagraph{')
            
        elif tag == 'strong' or tag == 'b':
            self.latex_content.append('\\textbf{')
        elif tag == 'em' or tag == 'i':
            self.latex_content.append('\\textit{')
        elif tag == 'u':
            self.latex_content.append('\\underline{')
        elif tag == 'code':
            self.latex_content.append('\\texttt{')
        elif tag == 'pre':
            self.latex_content.append('\n\\begin{verbatim}')
        elif tag == 'blockquote':
            self.latex_content.append('\n\\begin{quote}\n')
            
        elif tag == 'ul':
            self.list_level += 1
            self.current_list_type = 'ul'
            self.latex_content.append('\n\\begin{itemize}\n')
        elif tag == 'ol':
            self.list_level += 1
            self.current_list_type = 'ol'
            self.latex_content.append('\n\\begin{enumerate}\n')
        elif tag == 'li':
            self.latex_content.append('\\item ')
            
        elif tag == 'table':
            self.in_table = True
            self.latex_content.append('\n\\begin{table}[htbp]\n\\centering\n')
        elif tag == 'tr':
            self.in_table_row = True
            self.table_cell_count = 0
        elif tag == 'td' or tag == 'th':
            self.in_table_cell = True
            if self.table_cell_count > 0:
                self.latex_content.append(' & ')
            self.table_cell_count += 1
            
        elif tag == 'br':
            self.latex_content.append('\\\n')
            
        elif tag == 'hr':
            self.latex_content.append('\n\\noindent\\rule{\\textwidth}{0.4pt}\n')
            
    def handle_endtag(self, tag):
        if tag in self.skip_tags:
            return
            
        if tag == 'body':
            self.in_body = False
            return
            
        if not self.in_body:
            return
            
        if tag == 'div':
            if self.current_class:
                if 'contents1' in self.current_class or 'contents2' in self.current_class or 'contents3' in self.current_class:
                    self.latex_content.append('}\n')
            self.current_class = None
            
        elif tag == 'a':
            self.latex_content.append('}')
            
        elif tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self.latex_content.append('}\n')
            
        elif tag in ['strong', 'b', 'em', 'i', 'u', 'code']:
            self.latex_content.append('}')
            
        elif tag == 'pre':
            self.latex_content.append('\n\\end{verbatim}\n')
        elif tag == 'blockquote':
            self.latex_content.append('\n\\end{quote}\n')
            
        elif tag == 'ul':
            self.list_level -= 1
            self.latex_content.append('\n\\end{itemize}\n')
        elif tag == 'ol':
            self.list_level -= 1
            self.latex_content.append('\n\\end{enumerate}\n')
            
        elif tag == 'table':
            self.in_table = False
            self.latex_content.append('\n\\end{table}\n')
        elif tag == 'tr':
            self.in_table_row = False
            self.latex_content.append(' \\\n')
        elif tag == 'td' or tag == 'th':
            self.in_table_cell = False
            
    def handle_data(self, data):
        if not self.in_body:
            return
            
        data = data.replace('&nbsp;', ' ')
        data = data.replace('&lt;', '<')
        data = data.replace('&gt;', '>')
        data = data.replace('&amp;', '&')
        data = data.replace('&quot;', '"')
        data = data.replace('&apos;', "'")
        
        data = re.sub(r'\\', r'\\textbackslash{}', data)
        data = re.sub(r'\$', r'\\$', data)
        data = re.sub(r'%', r'\\%', data)
        data = re.sub(r'#', r'\\#', data)
        data = re.sub(r'_', r'\\_', data)
        data = re.sub(r'\{', r'\\{', data)
        data = re.sub(r'\}', r'\\}', data)
        data = re.sub(r'~', r'\\textasciitilde{}', data)
        data = re.sub(r'\^', r'\\textasciicircum{}', data)
        
        self.latex_content.append(data)
        
    def get_latex(self):
        return ''.join(self.latex_content)

def convert_xhtml_to_latex(xhtml_file_path):
    with open(xhtml_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    converter = XHTMLToLaTeXConverter()
    converter.feed(content)
    return converter.get_latex()

def process_epub_to_latex(epub_extract_dir, output_tex_file):
    oebps_dir = os.path.join(epub_extract_dir, 'OEBPS')
    
    content_opf = os.path.join(oebps_dir, 'content.opf')
    tree = ET.parse(content_opf)
    root = tree.getroot()
    
    manifest = root.find('.//{http://www.idpf.org/2007/opf}manifest')
    spine = root.find('.//{http://www.idpf.org/2007/opf}spine')
    
    html_files = []
    for itemref in spine.findall('.//{http://www.idpf.org/2007/opf}itemref'):
        idref = itemref.get('idref')
        for item in manifest.findall('.//{http://www.idpf.org/2007/opf}item'):
            if item.get('id') == idref:
                href = item.get('href')
                html_files.append(os.path.join(oebps_dir, href))
                break
    
    latex_content = []
    latex_content.append(r'\documentclass{book}')
    latex_content.append(r'\usepackage{ctex}')
    latex_content.append(r'\usepackage{graphicx}')
    latex_content.append(r'\usepackage{hyperref}')
    latex_content.append(r'\usepackage{longtable}')
    latex_content.append(r'\usepackage{booktabs}')
    latex_content.append(r'\graphicspath{{./temp_extract/OEBPS/}}')
    latex_content.append(r'\begin{document}')
    latex_content.append(r'\title{跟老男孩学Linux运维：MySQL入门与提高实践}')
    latex_content.append(r'\author{老男孩}')
    latex_content.append(r'\maketitle')
    latex_content.append(r'\tableofcontents')
    latex_content.append('')
    
    for html_file in html_files:
        print(f'Processing: {html_file}')
        latex_content.append(f'\n% From {os.path.basename(html_file)}')
        try:
            chapter_latex = convert_xhtml_to_latex(html_file)
            latex_content.append(chapter_latex)
        except Exception as e:
            print(f'Error processing {html_file}: {e}')
            continue
    
    latex_content.append(r'\end{document}')
    
    with open(output_tex_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(latex_content))
    
    print(f'LaTeX file generated: {output_tex_file}')

if __name__ == '__main__':
    epub_extract_dir = r'D:\Git\Book\整理中\1_原文校对\MySQL\temp_extract'
    output_tex_file = r'D:\Git\Book\整理中\1_原文校对\MySQL\MySQL.tex'
    
    process_epub_to_latex(epub_extract_dir, output_tex_file)