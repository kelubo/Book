#!/usr/bin/env python3
import os
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

class HTMLToLaTeXConverter(HTMLParser):
    def __init__(self):
        super().__init__()
        self.latex_content = []
        self.in_paragraph = False
        self.in_heading = False
        self.heading_level = 0
        self.in_blockquote = False
        self.in_div = False
        self.current_class = None
        self.in_image = False
        self.image_src = None
        self.in_title = False
        self.in_list = False
        self.list_type = None
        self.in_list_item = False
        self.current_text = []
        self.ignore_tags = {'svg', 'link', 'meta', 'div'}
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        if tag in self.ignore_tags:
            return
            
        if tag == 'h1':
            self.latex_content.append('\\chapter{')
            self.in_heading = True
            self.heading_level = 1
        elif tag == 'h2':
            self.latex_content.append('\\section{')
            self.in_heading = True
            self.heading_level = 2
        elif tag == 'h3':
            self.latex_content.append('\\subsection{')
            self.in_heading = True
            self.heading_level = 3
        elif tag == 'h4':
            self.latex_content.append('\\subsubsection{')
            self.in_heading = True
            self.heading_level = 4
        elif tag == 'p':
            class_name = attrs_dict.get('class', '')
            if class_name == 'p_title':
                self.latex_content.append('\\vspace{0.5em}\\textbf{')
                self.in_paragraph = True
            elif class_name == 'picture':
                pass
            else:
                self.latex_content.append('\\par ')
                self.in_paragraph = True
        elif tag == 'br':
            self.latex_content.append('\\\\')
        elif tag == 'blockquote':
            self.latex_content.append('\\begin{quote}')
            self.in_blockquote = True
        elif tag == 'img':
            src = attrs_dict.get('src', '')
            if src:
                if src.startswith('../'):
                    src = src[3:]
                self.latex_content.append(f'\\begin{{figure}}[htbp]\\centering\\includegraphics[width=0.8\\textwidth]{{{src}}}\\end{{figure}}')
        elif tag == 'span':
            class_name = attrs_dict.get('class', '')
            if class_name == 'border':
                self.latex_content.append('\\fbox{')
            elif class_name == 'underline':
                self.latex_content.append('\\underline{')
        elif tag == 'strong' or tag == 'b':
            self.latex_content.append('\\textbf{')
        elif tag == 'em' or tag == 'i':
            self.latex_content.append('\\textit{')
        elif tag == 'ul':
            self.latex_content.append('\\begin{itemize}')
            self.in_list = True
            self.list_type = 'ul'
        elif tag == 'ol':
            self.latex_content.append('\\begin{enumerate}')
            self.in_list = True
            self.list_type = 'ol'
        elif tag == 'li':
            self.latex_content.append('\\item ')
            self.in_list_item = True
            
    def handle_endtag(self, tag):
        if tag in self.ignore_tags:
            return
            
        if tag in ['h1', 'h2', 'h3', 'h4']:
            self.latex_content.append('}\n\n')
            self.in_heading = False
        elif tag == 'p':
            class_name = self.current_class
            if class_name == 'p_title':
                self.latex_content.append('}')
            elif class_name == 'picture':
                pass
            else:
                self.latex_content.append('\n')
            self.in_paragraph = False
            self.current_class = None
        elif tag == 'blockquote':
            self.latex_content.append('\\end{quote}\n\n')
            self.in_blockquote = False
        elif tag == 'span':
            class_name = self.current_class
            if class_name in ['border', 'underline']:
                self.latex_content.append('}')
            self.current_class = None
        elif tag in ['strong', 'b']:
            self.latex_content.append('}')
        elif tag in ['em', 'i']:
            self.latex_content.append('}')
        elif tag == 'ul':
            self.latex_content.append('\\end{itemize}\n\n')
            self.in_list = False
        elif tag == 'ol':
            self.latex_content.append('\\end{enumerate}\n\n')
            self.in_list = False
        elif tag == 'li':
            self.latex_content.append('\n')
            self.in_list_item = False
            
    def handle_data(self, data):
        if data.strip():
            self.latex_content.append(data)
            
    def get_latex(self):
        return ''.join(self.latex_content)

def convert_html_to_latex(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    converter = HTMLToLaTeXConverter()
    converter.feed(html_content)
    return converter.get_latex()

def process_epub_to_latex(epub_extracted_path, output_latex_path):
    text_dir = os.path.join(epub_extracted_path, 'text')
    images_dir = os.path.join(epub_extracted_path, 'images')
    
    if not os.path.exists(text_dir):
        print(f"Text directory not found: {text_dir}")
        return
    
    html_files = sorted([f for f in os.listdir(text_dir) if f.endswith('.html')])
    
    latex_content = []
    
    latex_content.append(r'''\documentclass[a4paper,12pt]{ctexart}
\usepackage{graphicx}
\usepackage{geometry}
\usepackage{hyperref}
\usepackage{titlesec}

\geometry{left=2.5cm,right=2.5cm,top=2.5cm,bottom=2.5cm}

\title{明朝那些事儿（图文增补版）}
\author{当年明月}
\date{}

\begin{document}

\maketitle

\tableofcontents

\newpage
''')
    
    for html_file in html_files:
        html_path = os.path.join(text_dir, html_file)
        print(f"Processing: {html_file}")
        
        try:
            latex_part = convert_html_to_latex(html_path)
            if latex_part.strip():
                latex_content.append(f"% From {html_file}\n")
                latex_content.append(latex_part)
                latex_content.append("\n\n")
        except Exception as e:
            print(f"Error processing {html_file}: {e}")
    
    latex_content.append(r'\end{document}')
    
    with open(output_latex_path, 'w', encoding='utf-8') as f:
        f.write(''.join(latex_content))
    
    print(f"\nLaTeX file created: {output_latex_path}")
    print(f"Processed {len(html_files)} HTML files")

if __name__ == '__main__':
    epub_extracted_path = r'D:\Git\Book\整理中\1_原文校对\明朝那些事儿\epub_extracted'
    output_latex_path = r'D:\Git\Book\整理中\1_原文校对\明朝那些事儿\明朝那些事儿.tex'
    
    process_epub_to_latex(epub_extracted_path, output_latex_path)
