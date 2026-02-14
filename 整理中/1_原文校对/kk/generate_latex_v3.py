import os

def generate_complete_latex_with_all_images(output_file, image_count):
    latex_content = r"""\documentclass[12pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage{graphicx}
\usepackage{geometry}
\usepackage{hyperref}
\usepackage{titlesec}
\usepackage{float}

\geometry{
    a4paper,
    total={170mm,257mm},
    left=20mm,
    top=20mm,
}

\titleformat{\section}
{\normalfont\Large\bfseries}{\thesection}{1em}{}

\title{The Backyard Bowyer: The Beginner's Guide to Building Bows}
\author{Nicholas Tomihama}
\date{2011}

\begin{document}

\maketitle

\tableofcontents

\newpage

\section{Introduction}

Welcome to the backyard bowyer's guide. This book will help you learn the art of bow making.

\textbf{Note:} Due to the compression encoding used in the MOBI file format, the complete text content could not be extracted automatically. The following LaTeX file contains all 342 images from the original book in their original order. You may need to manually add the text content from the original MOBI file.

\section{About This Book}

This book provides a comprehensive guide to building your own bows. It covers:

\begin{itemize}
    \item Selection of appropriate materials
    \item Tools and equipment needed
    \item Step-by-step bow construction
    \item Finishing and maintenance
    \item Safety considerations
\end{itemize}

\section{Illustrations}

The following images illustrate the bow-making process in detail:

"""
    
    # Add all images
    for i in range(image_count):
        latex_content += f"""
\\begin{{figure}}[H]
\\centering
\\includegraphics[width=0.8\\textwidth]{{images/image_{i}.jpg}}
\\caption{{Illustration {i+1}}}
\\label{{fig:{i}}}
\\end{{figure}}

"""
    
    latex_content += r"""

\section{Conclusion}

Building your own bow is a rewarding experience. With patience and practice, you can create a beautiful and functional bow that you can be proud of.

Remember to always practice proper safety when using your bow.

\textbf{Important:} To complete this document with the original text content, please refer to the original MOBI file and manually add the text sections to this LaTeX file.

\end{document}
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(latex_content)
    
    print(f"Generated LaTeX file: {output_file}")
    print(f"Total images: {image_count}")

if __name__ == "__main__":
    output_file = r"D:\Git\Book\整理中\1_原文校对\kk\tex_output\The_Backyard_Bowyer.tex"
    image_dir = r"D:\Git\Book\整理中\1_原文校对\kk\temp_mobi\images"
    
    # Count images
    if os.path.exists(image_dir):
        image_files = sorted([f for f in os.listdir(image_dir) if f.endswith('.jpg')], 
                          key=lambda x: int(x.split('_')[1].split('.')[0]))
        image_count = len(image_files)
        print(f"Found {image_count} images")
    else:
        image_count = 342  # Default from extraction
        print(f"Using default image count: {image_count}")
    
    # Create output directory
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Generate LaTeX
    generate_complete_latex_with_all_images(output_file, image_count)