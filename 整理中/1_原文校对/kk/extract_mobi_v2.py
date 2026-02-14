import os
import sys

def try_extract_with_ebooklib(mobi_file, output_dir):
    try:
        import ebooklib
        from ebooklib import epub
        
        print("Trying to read MOBI file with ebooklib...")
        
        # Try to read as EPUB (some MOBI files are actually EPUB)
        try:
            book = epub.read_epub(mobi_file)
            print(f"Successfully read as EPUB format")
            
            # Extract content
            for item in book.get_items():
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    filename = os.path.join(output_dir, item.get_name())
                    os.makedirs(os.path.dirname(filename), exist_ok=True)
                    with open(filename, 'wb') as f:
                        f.write(item.get_content())
                    print(f"Extracted: {filename}")
                elif item.get_type() == ebooklib.ITEM_IMAGE:
                    filename = os.path.join(output_dir, item.get_name())
                    os.makedirs(os.path.dirname(filename), exist_ok=True)
                    with open(filename, 'wb') as f:
                        f.write(item.get_content())
                    print(f"Extracted image: {filename}")
            
            return True
        except Exception as e:
            print(f"Not an EPUB file: {e}")
            return False
            
    except ImportError:
        print("ebooklib not installed")
        return False

def try_extract_with_pymobi(mobi_file, output_dir):
    try:
        import pymobi
        
        print("Trying to read MOBI file with pymobi...")
        
        mobi = pymobi.Mobi(mobi_file)
        
        print(f"Title: {mobi.title()}")
        print(f"Author: {mobi.author()}")
        
        # Extract HTML content
        html_content = mobi.get_html()
        html_file = os.path.join(output_dir, "content.html")
        os.makedirs(output_dir, exist_ok=True)
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Extracted HTML to: {html_file}")
        
        # Extract images if available
        images = mobi.get_images()
        if images:
            for i, img in enumerate(images):
                img_file = os.path.join(output_dir, f"image_{i}.jpg")
                with open(img_file, 'wb') as f:
                    f.write(img)
                print(f"Extracted image: {img_file}")
        
        return True
        
    except ImportError:
        print("pymobi not installed")
        return False
    except Exception as e:
        print(f"Error with pymobi: {e}")
        return False

if __name__ == "__main__":
    mobi_file = r"D:\Git\Book\整理中\1_原文校对\kk\The Backyard Bowyer The Beginners Guide to Building Bows (Nicholas Tomihama) (z-library.sk, 1lib.sk, z-lib.sk).mobi"
    output_dir = r"D:\Git\Book\整理中\1_原文校对\kk\temp_mobi"
    
    # Try different extraction methods
    if not try_extract_with_ebooklib(mobi_file, output_dir):
        if not try_extract_with_pymobi(mobi_file, output_dir):
            print("Failed to extract MOBI file with available libraries")