import os
from html.parser import HTMLParser

class TestConverter(HTMLParser):
    def __init__(self):
        super().__init__()
        self.latex_content = []
        self.in_body = False
        self.skip_tags = ['head', 'style', 'script', 'meta', 'link']
        self.debug_info = []
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        self.debug_info.append(f"START TAG: {tag}, in_body: {self.in_body}")
        
        if tag in self.skip_tags:
            self.debug_info.append(f"SKIPPING TAG: {tag}")
            return
            
        if tag == 'body':
            self.in_body = True
            self.debug_info.append(f"SET in_body to True")
            return
            
        if not self.in_body:
            self.debug_info.append(f"NOT IN BODY, SKIPPING TAG: {tag}")
            return
        
        self.debug_info.append(f"PROCESSING TAG: {tag}")
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
        self.debug_info.append(f"END TAG: {tag}, in_body: {self.in_body}")
        if tag == 'body':
            self.in_body = False
            self.debug_info.append(f"SET in_body to False")
            return
            
        if not self.in_body:
            return
        
        if tag in ['h1', 'h2', 'h4']:
            self.latex_content.append('}')
        elif tag == 'a':
            self.latex_content.append('}')
    
    def handle_data(self, data):
        data = data.strip()
        if data:
            self.debug_info.append(f"DATA: '{data}', in_body: {self.in_body}")
        if not self.in_body:
            return
        
        data = data.strip()
        if data:
            self.latex_content.append(data)
    
    def get_latex(self):
        return ''.join(self.latex_content)

# Test with the first XHTML file
test_file = 'temp_extract/OEBPS/text00003.html'

with open(test_file, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"HTML Content:\n{content}")
print("\n" + "="*80 + "\n")

converter = TestConverter()
converter.feed(content)

print("Debug Info:")
for line in converter.debug_info:
    print(line)

print("\n" + "="*80 + "\n")
print("Generated LaTeX:")
print(converter.get_latex())