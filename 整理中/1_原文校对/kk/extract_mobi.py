import os
import struct
import sys

def read_mobi_header(mobi_file):
    with open(mobi_file, 'rb') as f:
        # Read PalmDOC header
        f.seek(0x3C)
        mobi_offset = struct.unpack('>I', f.read(4))[0]
        
        # Read MOBI header
        f.seek(mobi_offset)
        signature = f.read(4)
        if signature != b'MOBI':
            print("Not a valid MOBI file")
            return None
        
        header_length = struct.unpack('>I', f.read(4))[0]
        mobi_type = struct.unpack('>I', f.read(4))[0]
        text_encoding = struct.unpack('>I', f.read(4))[0]
        
        print(f"MOBI Type: {mobi_type}")
        print(f"Text Encoding: {text_encoding}")
        print(f"Header Length: {header_length}")
        
        return {
            'mobi_offset': mobi_offset,
            'header_length': header_length,
            'mobi_type': mobi_type,
            'text_encoding': text_encoding
        }

def extract_mobi_content(mobi_file, output_dir):
    try:
        header = read_mobi_header(mobi_file)
        if header is None:
            return False
        
        print(f"MOBI header read successfully")
        print(f"Output directory: {output_dir}")
        
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    mobi_file = r"D:\Git\Book\整理中\1_原文校对\kk\The Backyard Bowyer The Beginners Guide to Building Bows (Nicholas Tomihama) (z-library.sk, 1lib.sk, z-lib.sk).mobi"
    output_dir = r"D:\Git\Book\整理中\1_原文校对\kk\temp_mobi"
    
    extract_mobi_content(mobi_file, output_dir)