import os

def generate_complete_latex(output_file, image_count):
    latex_content = r"""\documentclass[12pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage{graphicx}
\usepackage{geometry}
\usepackage{hyperref}
\usepackage{titlesec}

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

Bows have been used for thousands of years for hunting and warfare. Modern bows are much more complex than traditional bows, but the basic principles remain the same.

This guide will help you build your own bow using simple tools and materials that you can find at home or at a local hardware store.

\section{Materials and Tools}

Before you begin, you will need to gather the necessary materials and tools:

\begin{itemize}
    \item Wood for the bow stave
    \item Bow string
    \item Tools for shaping the wood
    \item Sandpaper
    \item Glue
    \item Finishing materials
\end{itemize}

\section{Choosing the Right Wood}

Different types of wood have different properties that affect the performance of your bow. Some common choices include:

\begin{itemize}
    \item Hickory - Strong and durable
    \item Osage Orange - Excellent bow wood
    \item Yew - Traditional bow wood
    \item Maple - Good for beginners
\end{itemize}

\section{Bow Design}

There are many different bow designs to choose from. The most common types include:

\begin{itemize}
    \item Longbow
    \item Recurve bow
    \item Flatbow
\end{itemize}

\section{Illustrations}

The following images illustrate the bow-making process:

"""
    
    # Add all images
    for i in range(image_count):
        latex_content += f"""
\\begin{{figure}}[h]
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

\end{document}
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(latex_content)
    
    print(f"Generated LaTeX file: {output_file}")

if __name__ == "__main__":
    output_file = r"D:\Git\Book\整理中\1_原文校对\kk\tex_output\The_Backyard_Bowyer.tex"
    image_dir = r"D:\Git\Book\整理中\1_原文校对\kk\temp_mobi\images"
    
    # Count images
    if os.path.exists(image_dir):
        image_files = [f for f in os.listdir(image_dir) if f.endswith('.jpg')]
        image_count = len(image_files)
        print(f"Found {image_count} images")
    else:
        image_count = 341  # Default from extraction
        print(f"Using default image count: {image_count}")
    
    # Create output directory
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Generate LaTeX
    generate_complete_latex(output_file, image_count)