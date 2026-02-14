import os
import struct
import re

def extract_text_from_mobi(mobi_file, output_file):
    print(f"Reading MOBI file: {mobi_file}")
    
    with open(mobi_file, 'rb') as f:
        data = f.read()
        
        # Find MOBI header
        mobi_offset = None
        for i in range(len(data) - 4):
            if data[i:i+4] == b'MOBI':
                mobi_offset = i
                print(f"Found MOBI header at offset: {mobi_offset}")
                break
        
        if mobi_offset is None:
            print("MOBI signature not found")
            return False
        
        # Read MOBI header
        f.seek(mobi_offset + 0x4)
        header_length = struct.unpack('>I', f.read(4))[0]
        mobi_type = struct.unpack('>I', f.read(4))[0]
        text_encoding = struct.unpack('>I', f.read(4))[0]
        
        print(f"MOBI Type: {mobi_type}")
        print(f"Text Encoding: {text_encoding}")
        print(f"Header Length: {header_length}")
        
        # Read content offsets
        f.seek(mobi_offset + 0x84)
        first_content_index = struct.unpack('>I', f.read(4))[0]
        last_content_index = struct.unpack('>I', f.read(4))[0]
        
        f.seek(mobi_offset + 0x94)
        huff_rec_offset = struct.unpack('>I', f.read(4))[0]
        huff_rec_count = struct.unpack('>I', f.read(4))[0]
        
        f.seek(mobi_offset + 0x9C)
        datp_offset = struct.unpack('>I', f.read(4))[0]
        datp_count = struct.unpack('>I', f.read(4))[0]
        
        print(f"First content index: {first_content_index}")
        print(f"Last content index: {last_content_index}")
        print(f"Data offset: {datp_offset}")
        
        # Try to extract text records
        # Look for readable text in the data
        text_content = ""
        
        # Search for HTML-like content
        # Look for common HTML patterns
        html_patterns = [
            rb'<p[^>]*>',
            rb'<div[^>]*>',
            rb'<h[1-6][^>]*>',
            rb'<br[^>]*>',
            rb'<title[^>]*>',
        ]
        
        found_patterns = set()
        for pattern in html_patterns:
            matches = re.finditer(pattern, data, re.IGNORECASE)
            for match in matches:
                found_patterns.add(pattern)
        
        print(f"Found HTML patterns: {len(found_patterns)}")
        
        # Extract a large chunk of content starting from the data offset
        if datp_offset > 0 and datp_offset < len(data):
            content_start = datp_offset
            content_end = min(content_start + 500000, len(data))  # Extract up to 500KB
            
            content_data = data[content_start:content_end]
            
            # Try to decode
            try:
                if text_encoding == 65001:  # UTF-8
                    text_content = content_data.decode('utf-8', errors='ignore')
                elif text_encoding == 1252:  # Windows-1252
                    text_content = content_data.decode('cp1252', errors='ignore')
                else:
                    text_content = content_data.decode('latin-1', errors='ignore')
                
                print(f"Extracted {len(text_content)} characters")
            except Exception as e:
                print(f"Decode error: {e}")
                # Try different encodings
                for encoding in ['utf-8', 'cp1252', 'latin-1', 'ascii']:
                    try:
                        text_content = content_data.decode(encoding, errors='ignore')
                        print(f"Successfully decoded with {encoding}")
                        break
                    except:
                        continue
        
        # If still no content, try searching for text throughout the file
        if not text_content or len(text_content) < 1000:
            print("Searching for text throughout the file...")
            
            # Look for sequences of readable ASCII text
            text_pattern = rb'[a-zA-Z0-9\s.,!?;:\-\'"]{100,}'
            matches = re.finditer(text_pattern, data)
            
            text_segments = []
            for match in matches:
                segment = match.group().decode('ascii', errors='ignore')
                if len(segment) > 50:
                    text_segments.append(segment)
            
            if text_segments:
                text_content = '\n\n'.join(text_segments[:100])  # Take first 100 segments
                print(f"Found {len(text_segments)} text segments")
        
        # Clean up the text
        if text_content:
            # Remove binary garbage
            text_content = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text_content)
            
            # Try to extract HTML structure
            # Look for paragraphs
            para_pattern = r'<p[^>]*>(.*?)</p>'
            paragraphs = re.findall(para_pattern, text_content, re.DOTALL | re.IGNORECASE)
            
            if paragraphs:
                print(f"Found {len(paragraphs)} HTML paragraphs")
                cleaned_paragraphs = []
                for p in paragraphs:
                    # Remove HTML tags
                    p = re.sub(r'<[^>]+>', '', p)
                    # Clean up
                    p = re.sub(r'\s+', ' ', p)
                    p = p.strip()
                    if len(p) > 20:
                        cleaned_paragraphs.append(p)
                
                text_content = '\n\n'.join(cleaned_paragraphs)
        
        # Save the extracted text
        if text_content and len(text_content) > 100:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(text_content)
            print(f"Saved text to: {output_file}")
            return True
        else:
            print("No significant text content found")
            return False

if __name__ == "__main__":
    mobi_file = r"D:\Git\Book\整理中\1_原文校对\kk\The Backyard Bowyer The Beginners Guide to Building Bows (Nicholas Tomihama) (z-library.sk, 1lib.sk, z-lib.sk).mobi"
    output_file = r"D:\Git\Book\整理中\1_原文校对\kk\temp_mobi\extracted_text.txt"
    
    extract_text_from_mobi(mobi_file, output_file)