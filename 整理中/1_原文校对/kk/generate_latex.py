import os
import re
import html

def clean_html_content(html_file):
    with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Remove binary garbage
    content = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', content)
    
    # Extract HTML tags and text
    # Look for <img> tags
    img_pattern = r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>'
    images = re.findall(img_pattern, content)
    
    # Look for text content
    # Extract paragraphs
    text_pattern = r'<p[^>]*>(.*?)</p>'
    paragraphs = re.findall(text_pattern, content, re.DOTALL)
    
    # Clean paragraphs
    cleaned_paragraphs = []
    for p in paragraphs:
        # Remove HTML tags
        p = re.sub(r'<[^>]+>', '', p)
        # Decode HTML entities
        p = html.unescape(p)
        # Remove extra whitespace
        p = ' '.join(p.split())
        if p and len(p) > 10:
            cleaned_paragraphs.append(p)
    
    return images, cleaned_paragraphs

def generate_latex(images, paragraphs, output_file):
    latex_content = r"""\documentclass[12pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage{graphicx}
\usepackage{geometry}
\usepackage{hyperref}

\geometry{
    a4paper,
    total={170mm,257mm},
    left=20mm,
    top=20mm,
}

\title{The Backyard Bowyer: The Beginner's Guide to Building Bows}
\author{Nicholas Tomihama}
\date{}

\begin{document}

\maketitle

\tableofcontents

\newpage

\section{Introduction}

Welcome to the backyard bowyer's guide. This book will help you learn the art of bow making.

"""
    
    # Add content
    for i, para in enumerate(paragraphs[:50]):  # Limit to first 50 paragraphs
        latex_content += f"\n{para}\n\n"
    
    # Add images section
    latex_content += r"""

\section{Illustrations}

The following images illustrate the bow-making process:

"""
    
    for i in range(min(len(images), 50)):  # Limit to first 50 images
        latex_content += f"""
\\begin{{figure}}[h]
\\centering
\\includegraphics[width=0.8\\textwidth]{{images/image_{i}.jpg}}
\\caption{{Illustration {i+1}}}
\\end{{figure}}

"""
    
    latex_content += r"""
\end{document}
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(latex_content)
    
    print(f"Generated LaTeX file: {output_file}")

if __name__ == "__main__":
    html_file = r"D:\Git\Book\整理中\1_原文校对\kk\temp_mobi\content.html"
    output_file = r"D:\Git\Book\整理中\1_原文校对\kk\tex_output\The_Backyard_Bowyer.tex"
    
    # Create output directory
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Clean HTML content
    images, paragraphs = clean_html_content(html_file)
    
    print(f"Found {len(images)} image references")
    print(f"Found {len(paragraphs)} paragraphs")
    
    # Generate LaTeX
    generate_latex(images, paragraphs, output_file)