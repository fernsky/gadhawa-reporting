#!/usr/bin/env python3
"""
Test to verify that TOC page numbering works correctly after fixes
"""
import os
import tempfile
from weasyprint import HTML, CSS

def test_toc_page_numbering():
    """Test if TOC page numbering works with the fixed CSS"""
    print("🔍 Testing TOC page numbering with fixed CSS...")
    
    # Create HTML content similar to your PDF report structure
    html_content = """
    <!DOCTYPE html>
    <html lang="ne">
    <head>
        <meta charset="UTF-8">
        <style>
            /* Custom Nepali counter style */
            @counter-style nepali-numerals {
                system: numeric;
                symbols: "०" "१" "२" "३" "४" "५" "६" "७" "८" "९";
                suffix: "";
            }

            /* Simplified page setup with consistent Nepali numerals */
            @page {
                size: A4;
                margin: 2cm 1.5cm 3cm 1.5cm;
                
                @bottom-right {
                    content: counter(page, nepali-numerals) " | गढवा गाउँपालिकाको पार्श्वचित्र";
                    font-size: 9pt;
                    color: #666;
                    font-family: 'Noto Sans Devanagari', 'DejaVu Sans', sans-serif;
                }
            }

            /* Cover page - no page numbers */
            @page :first {
                @top-left { content: ""; }
                @top-right { content: ""; }
                @bottom-center { content: ""; }
                @bottom-right { content: ""; }
            }

            body {
                font-family: 'Noto Sans Devanagari', 'DejaVu Sans', sans-serif;
                font-size: 11pt;
                line-height: 1.5;
                color: #333;
                margin: 0;
                padding: 0;
            }

            .cover-page {
                page-break-after: always;
                text-align: center;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                min-height: 70vh;
            }

            .toc-page {
                page-break-before: always;
                page-break-after: always;
            }

            .main-content-start {
                page-break-before: always;
            }

            .toc-title {
                font-size: 18pt;
                font-weight: 700;
                color: #1e3a8a;
                border-bottom: 3px solid #0ea5e9;
                padding-bottom: 0.5em;
                margin-bottom: 1.5em;
                text-align: center;
            }

            .toc-item {
                display: flex;
                justify-content: space-between;
                align-items: baseline;
                margin-bottom: 0.4em;
                padding: 0.2em 0;
                border-bottom: 1px dotted #d1d5db;
                page-break-inside: avoid;
            }

            .toc-item .toc-link {
                color: #333;
                text-decoration: none;
                flex-grow: 1;
                margin-right: 1em;
            }

            .toc-item.level-1 {
                font-weight: 600;
                font-size: 12pt;
                margin-top: 1em;
                margin-bottom: 0.5em;
                color: #1e40af;
            }

            .page-ref {
                color: #666;
                font-weight: bold;
                min-width: 2em;
                text-align: right;
                margin-left: 1em;
                display: inline-block;
            }

            /* For page references using anchor links */
            .page-ref a::after {
                content: target-counter(attr(href), page, nepali-numerals);
                color: #666;
                font-weight: bold;
            }
            
            /* Hide the actual link text */
            .page-ref a {
                color: #666;
                text-decoration: none;
            }

            .section-break {
                page-break-before: auto;
                page-break-after: avoid;
                page-break-inside: avoid;
            }

            .section-break:first-of-type {
                page-break-before: always;
            }

            .category-title {
                font-size: 18pt;
                font-weight: 700;
                text-align: center;
                color: #dc2626;
                margin: 2em 0 1em 0;
                padding: 0.5em;
                page-break-after: avoid;
            }

            .content-section {
                margin-bottom: 1em;
                text-align: justify;
                min-height: 40vh;
                padding: 1em;
            }
        </style>
    </head>
    <body>
        <!-- Cover Page -->
        <div class="cover-page">
            <div style="color: #dc2626; font-size: 24pt; font-weight: 700;">
                गढवा गाउँपालिका
            </div>
            <div style="color: #1e40af; font-size: 18pt; margin-top: 1em;">
                पार्श्वचित्र प्रतिवेदन
            </div>
        </div>

        <!-- Table of Contents -->
        <div class="toc-page">
            <h1 class="toc-title">विषयसूची</h1>
            
            <div class="toc-item level-1">
                <span class="toc-link">१. जनसांख्यिकीय विवरण</span>
                <span class="page-ref"><a href="#category-1"></a></span>
            </div>
            
            <div class="toc-item level-1">
                <span class="toc-link">२. आर्थिक अवस्था</span>
                <span class="page-ref"><a href="#category-2"></a></span>
            </div>
            
            <div class="toc-item level-1">
                <span class="toc-link">३. पूर्वाधार विकास</span>
                <span class="page-ref"><a href="#category-3"></a></span>
            </div>
            
            <div class="toc-item level-1">
                <span class="toc-link">४. सामाजिक विकास</span>
                <span class="page-ref"><a href="#category-4"></a></span>
            </div>
            
            <div class="toc-item level-1">
                <span class="toc-link">५. वातावरणीय अवस्था</span>
                <span class="page-ref"><a href="#category-5"></a></span>
            </div>
        </div>

        <!-- Main Content Start -->
        <div class="main-content-start">
            <div class="section-break" id="category-1">
                <h1 class="category-title">परिच्छेद – १ः जनसांख्यिकीय विवरण</h1>
                <div class="content-section">
                    <p>गढवा गाउँपालिकाको जनसांख्यिकीय विवरणमा कुल जनसंख्या, घरधुरी संख्या, शिक्षा दर, र अन्य महत्वपूर्ण तथ्याङ्कहरू समावेश छन्।</p>
                    <p>यस क्षेत्रमा पुरुष र महिलाको अनुपात, उमेर समूह अनुसारको विभाजन, र जातीय संरचनाको विस्तृत विश्लेषण प्रस्तुत गरिएको छ।</p>
                </div>
            </div>
            
            <div class="section-break" id="category-2">
                <h1 class="category-title">परिच्छेद – २ः आर्थिक अवस्था</h1>
                <div class="content-section">
                    <p>गाउँपालिकाको आर्थिक अवस्थाको समीक्षामा कृषि, पशुपालन, व्यापार-व्यवसाय, र रोजगारीका अवसरहरूको विस्तृत अध्ययन गरिएको छ।</p>
                    <p>स्थानीय उत्पादन, आय-व्यय, र आर्थिक विकासका लागि आवश्यक नीति र कार्यक्रमहरूको चर्चा यहाँ गरिएको छ।</p>
                </div>
            </div>
            
            <div class="section-break" id="category-3">
                <h1 class="category-title">परिच्छेद – ३ः पूर्वाधार विकास</h1>
                <div class="content-section">
                    <p>यातायात, सञ्चार, सिँचाइ, विद्युत्, र अन्य पूर्वाधारहरूको अवस्था र विकासका योजनाहरूको समीक्षा गरिएको छ।</p>
                    <p>सडक सञ्जाल, पुल-पुलिया, विद्यालय भवन, स्वास्थ्य संस्था, र पानी आपूर्ति प्रणालीको विस्तृत जानकारी प्रदान गरिएको छ।</p>
                </div>
            </div>
            
            <div class="section-break" id="category-4">
                <h1 class="category-title">परिच्छेद – ४ः सामाजिक विकास</h1>
                <div class="content-section">
                    <p>शिक्षा, स्वास्थ्य, संस्कृति, र सामाजिक सेवाहरूको अवस्था र सुधारका उपायहरूको चर्चा यस खण्डमा गरिएको छ।</p>
                    <p>महिला सशक्तिकरण, बालबालिकाको अधिकार, र सामाजिक न्यायका विषयहरूमा विशेष ध्यान दिइएको छ।</p>
                </div>
            </div>
            
            <div class="section-break" id="category-5">
                <h1 class="category-title">परिच्छेद – ५ः वातावरणीय अवस्था</h1>
                <div class="content-section">
                    <p>वन, जैविक विविधता, जलवायु परिवर्तन, र वातावरण संरक्षणका उपायहरूको समीक्षा गरिएको छ।</p>
                    <p>फोहोर व्यवस्थापन, वायु र जल प्रदूषण नियन्त्रण, र दिगो विकासका कार्यक्रमहरूको चर्चा यहाँ समावेश छ।</p>
                </div>
            </div>
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
        
        print("📖 Please check if the TOC shows correct page numbers:")
        print("   - Category 1 should be on page ३ (3)")
        print("   - Category 2 should be on page ४ (4)")
        print("   - Category 3 should be on page ५ (5)")
        print("   - Category 4 should be on page ६ (6)")
        print("   - Category 5 should be on page ७ (7)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    test_toc_page_numbering()
