import os
from html.parser import HTMLParser

class TestConverter(HTMLParser):
    def __init__(self):
        super().__init__()
        self.latex_content = []
        self.in_body = False
        self.skip_tags = ['head', 'style', 'script', 'meta', 'link']
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        if tag in self.skip_tags:
            return
            
        if tag == 'body':
            self.in_body = True
            print(f"Found body tag, in_body = {self.in_body}")
            return
            
        if not self.in_body:
            print(f"Not in body, skipping tag: {tag}")
            return
        
        print(f"Processing start tag: {tag}")
        if tag == 'p':
            self.latex_content.append('\n\\par ')
        elif tag == 'h1':
            self.latex_content.append('\n\\chapter{')
        elif tag == 'h2':
            self.latex_content.append('\n\\section{')
        elif tag == 'h4':
            self.latex_content.append('\n\\subsubsection{')
        elif tag == 'a':
            href = attrs_dict.get('href', '')
            if href:
                self.latex_content.append(f'\\href{{{href}}}{{')
    
    def handle_endtag(self, tag):
        if tag == 'body':
            self.in_body = False
            print(f"End of body tag, in_body = {self.in_body}")
            return
            
        if not self.in_body:
            return
        
        print(f"Processing end tag: {tag}")
        if tag in ['h1', 'h2', 'h4']:
            self.latex_content.append('}')
        elif tag == 'a':
            self.latex_content.append('}')
    
    def handle_data(self, data):
        if not self.in_body:
            return
        
        data = data.strip()
        if data:
            print(f"Processing data: '{data}'")
            self.latex_content.append(data)
    
    def get_latex(self):
        return ''.join(self.latex_content)

# Test with the first XHTML file
test_file = 'temp_extract/OEBPS/text00003.html'

with open(test_file, 'r', encoding='utf-8') as f:
    content = f.read()

converter = TestConverter()
converter.feed(content)

print("\nGenerated LaTeX:")
print(converter.get_latex())