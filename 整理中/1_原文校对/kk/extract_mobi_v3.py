import os
import struct
import re
import html

def parse_mobi_file(mobi_file, output_dir):
    print(f"Reading MOBI file: {mobi_file}")
    
    with open(mobi_file, 'rb') as f:
        # Read file header
        data = f.read()
        
        # Check for PalmDOC database header
        # Look for MOBI signature
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
        f.seek(mobi_offset)
        signature = f.read(4)
        header_length = struct.unpack('>I', f.read(4))[0]
        mobi_type = struct.unpack('>I', f.read(4))[0]
        text_encoding = struct.unpack('>I', f.read(4))[0]
        id_ = struct.unpack('>I', f.read(4))[0]
        gen = struct.unpack('>I', f.read(4))[0]
        
        print(f"MOBI Type: {mobi_type}")
        print(f"Text Encoding: {text_encoding}")
        print(f"Header Length: {header_length}")
        
        # Read more header fields
        f.seek(mobi_offset + 0x60)
        full_name_offset = struct.unpack('>I', f.read(4))[0]
        full_name_length = struct.unpack('>I', f.read(4))[0]
        
        f.seek(mobi_offset + 0x68)
        locale_offset = struct.unpack('>I', f.read(4))[0]
        locale_length = struct.unpack('>I', f.read(4))[0]
        
        f.seek(mobi_offset + 0x70)
        dict_offset = struct.unpack('>I', f.read(4))[0]
        dict_length = struct.unpack('>I', f.read(4))[0]
        
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
        print(f"Huffman record offset: {huff_rec_offset}")
        print(f"Data offset: {datp_offset}")
        
        # Try to extract text content
        # Look for HTML-like content
        html_content = ""
        
        # Search for HTML tags in the data
        html_pattern = rb'<[^>]+>'
        matches = list(re.finditer(html_pattern, data))
        
        if matches:
            print(f"Found {len(matches)} HTML tags")
            
            # Extract a reasonable chunk of HTML content
            start_pos = matches[0].start()
            # Find a reasonable end point (look for closing body or html tag)
            end_pattern = rb'</(body|html)>'
            end_match = re.search(end_pattern, data[start_pos:])
            
            if end_match:
                end_pos = start_pos + end_match.end()
            else:
                end_pos = min(start_pos + 100000, len(data))
            
            html_data = data[start_pos:end_pos]
            
            # Try to decode as UTF-8 or Latin-1
            try:
                html_content = html_data.decode('utf-8')
            except:
                try:
                    html_content = html_data.decode('latin-1')
                except:
                    html_content = html_data.decode('ascii', errors='ignore')
            
            print(f"Extracted {len(html_content)} characters of HTML content")
        else:
            print("No HTML content found")
            return False
        
        # Save HTML content
        os.makedirs(output_dir, exist_ok=True)
        html_file = os.path.join(output_dir, "content.html")
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Saved HTML content to: {html_file}")
        
        # Try to extract images
        # Look for image signatures (JPEG, PNG, GIF)
        images = []
        
        # JPEG signature: FF D8 FF
        jpeg_pattern = rb'\xFF\xD8\xFF'
        for match in re.finditer(jpeg_pattern, data):
            start = match.start()
            # Find end of JPEG (FF D9)
            end = data.find(b'\xFF\xD9', start)
            if end != -1:
                img_data = data[start:end+2]
                images.append(('jpg', img_data))
        
        # PNG signature: 89 50 4E 47
        png_pattern = rb'\x89PNG'
        for match in re.finditer(png_pattern, data):
            start = match.start()
            # Find IEND chunk
            end = data.find(b'IEND', start)
            if end != -1:
                img_data = data[start:end+8]
                images.append(('png', img_data))
        
        print(f"Found {len(images)} images")
        
        # Save images
        img_dir = os.path.join(output_dir, "images")
        os.makedirs(img_dir, exist_ok=True)
        
        for i, (img_type, img_data) in enumerate(images):
            img_file = os.path.join(img_dir, f"image_{i}.{img_type}")
            with open(img_file, 'wb') as f:
                f.write(img_data)
            print(f"Saved image: {img_file}")
        
        return True

if __name__ == "__main__":
    mobi_file = r"D:\Git\Book\整理中\1_原文校对\kk\The Backyard Bowyer The Beginners Guide to Building Bows (Nicholas Tomihama) (z-library.sk, 1lib.sk, z-lib.sk).mobi"
    output_dir = r"D:\Git\Book\整理中\1_原文校对\kk\temp_mobi"
    
    parse_mobi_file(mobi_file, output_dir)