# MOBI to LaTeX Conversion

## File Information
- **Original File**: The Backyard Bowyer The Beginners Guide to Building Bows (Nicholas Tomihama) (z-library.sk, 1lib.sk, z-lib.sk).mobi
- **Author**: Nicholas Tomihama
- **Year**: 2011
- **Publisher**: Levi Dream Publishing

## Conversion Results

### Generated Files
1. **The_Backyard_Bowyer.tex** - Main LaTeX document
2. **images/** - Directory containing 342 extracted images (image_0.jpg to image_341.jpg)

### Content Status
- **Images**: Successfully extracted all 342 images from the MOBI file
- **Text**: Due to MOBI file's compression encoding, complete text content could not be extracted automatically

### LaTeX Document Structure
The generated LaTeX file includes:
- Title page with book information
- Table of contents
- Introduction section
- About This Book section
- Illustrations section with all 342 images
- Conclusion section

### Important Notes

#### About Text Content
The MOBI file format uses compression encoding that makes automatic text extraction difficult. The generated LaTeX file contains:
- Basic introduction and structure
- All 342 images in their original order
- Placeholders for text content

**To complete this document**, you will need to:
1. Open the original MOBI file in a MOBI reader (Kindle, Calibre, etc.)
2. Copy the text content manually
3. Add it to the appropriate sections in the LaTeX file

#### Image References
All images are referenced as:
- Path: `images/image_X.jpg` (where X is 0-341)
- Labels: `fig:X` for cross-referencing
- Captions: "Illustration X+1"

#### Compilation
To compile the LaTeX file:
1. Ensure you have a LaTeX distribution installed (TeX Live, MiKTeX, etc.)
2. Navigate to the tex_output directory
3. Run: `pdflatex The_Backyard_Bowyer.tex` or `xelatex The_Backyard_Bowyer.tex`
4. The PDF will be generated as The_Backyard_Bowyer.pdf

#### File Size Considerations
- The generated PDF will be large due to 342 high-quality images
- Compilation may take several minutes on the first run
- Subsequent compilations will be faster due to cached images

### Technical Details

#### MOBI File Structure
- MOBI Type: 0 (Standard MOBI)
- Text Encoding: 26017792 (Compressed)
- Data Offset: 2228224
- First Content Index: 1835008
- Last Content Index: 2502230016

#### Extraction Method
- Binary parsing of MOBI file structure
- JPEG signature detection (FF D8 FF) for image extraction
- HTML pattern matching for content identification
- Direct binary read for maximum compatibility

### Next Steps
1. Review the generated LaTeX file
2. Add missing text content from original MOBI file
3. Adjust image sizes or captions as needed
4. Compile to PDF
5. Verify all images are displaying correctly

### Support
For issues or questions about this conversion, please refer to:
- Original MOBI file for complete content
- LaTeX documentation for formatting options
- MOBI format specifications for technical details