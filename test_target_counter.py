#!/usr/bin/env python3
"""
Test to check WeasyPrint support for target-counter with a minimal example
"""
import os
import tempfile
from weasyprint import HTML, CSS

def test_target_counter_support():
    """Test if WeasyPrint supports target-counter"""
    print("🔍 Testing WeasyPrint target-counter support...")
    
    # Create minimal HTML with target-counter
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            @counter-style nepali-numerals {
                system: numeric;
                symbols: "०" "१" "२" "३" "४" "५" "६" "७" "८" "९";
                suffix: "";
            }
            
            @page {
                size: A4;
                margin: 2cm;
                @bottom-right {
                    content: counter(page, nepali-numerals);
                }
            }
            
            .toc-item {
                display: flex;
                justify-content: space-between;
                margin: 1em 0;
            }
            
            .page-ref a::after {
                content: target-counter(attr(href), page, nepali-numerals);
            }
            
            .page-ref a {
                color: #666;
                text-decoration: none;
            }
            
            .section {
                page-break-before: always;
                height: 50vh;
            }
        </style>
    </head>
    <body>
        <div class="toc">
            <h1>Table of Contents</h1>
            <div class="toc-item">
                <span>Section 1</span>
                <span class="page-ref"><a href="#section1"></a></span>
            </div>
            <div class="toc-item">
                <span>Section 2</span>
                <span class="page-ref"><a href="#section2"></a></span>
            </div>
            <div class="toc-item">
                <span>Section 3</span>
                <span class="page-ref"><a href="#section3"></a></span>
            </div>
        </div>
        
        <div class="section" id="section1">
            <h2>Section 1</h2>
            <p>This is section 1 content.</p>
        </div>
        
        <div class="section" id="section2">
            <h2>Section 2</h2>
            <p>This is section 2 content.</p>
        </div>
        
        <div class="section" id="section3">
            <h2>Section 3</h2>
            <p>This is section 3 content.</p>
        </div>
    </body>
    </html>
    """
    
    try:
        # Generate PDF
        html_doc = HTML(string=html_content)
        pdf_bytes = html_doc.write_pdf()
        
        # Save to file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as f:
            f.write(pdf_bytes)
            temp_path = f.name
        
        print(f"✅ Test PDF generated: {temp_path}")
        print(f"📏 PDF size: {len(pdf_bytes)} bytes")
        
        # Open PDF
        abs_path = os.path.abspath(temp_path)
        if os.name == 'nt':  # Windows
            os.startfile(abs_path)
        
        print("📖 Please check if the TOC shows correct page numbers (२, ३, ४) instead of all showing १")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    test_target_counter_support()
