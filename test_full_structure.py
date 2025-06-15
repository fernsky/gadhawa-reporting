#!/usr/bin/env python3
"""
Comprehensive test that matches the exact structure of pdf_full_report.html
to verify that TOC page numbering works correctly
"""
import os
import tempfile
from weasyprint import HTML, CSS


def test_full_report_structure():
    """Test TOC page numbering with exact PDF report structure"""
    print("🔍 Testing full report structure with TOC page numbering...")

    # Create HTML content that exactly matches pdf_full_report.html structure
    html_content = """
    <!DOCTYPE html>
    <html lang="ne">
    <head>
        <meta charset="UTF-8">
        <title>लुङ्ग्री गाउँपालिका - पूर्ण प्रतिवेदन</title>
        
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
                    content: counter(page, nepali-numerals) " | लुङ्ग्री गाउँपालिकाको पार्श्वचित्र";
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

            .toc-page, .list-page {
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

            .toc-item.level-2 {
                margin-left: 1.5em;
                font-size: 11pt;
                color: #2563eb;
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

            .section-content {
                page-break-inside: avoid;
                orphans: 3;
                widows: 3;
                margin-top: 1.5em;
            }

            .section-header.level-2 {
                font-size: 16pt;
                color: #1e40af;
                border-bottom: 2px solid #0ea5e9;
                padding-bottom: 0.3em;
                margin-top: 2em;
                margin-bottom: 1em;
            }

            .content-section {
                margin-bottom: 1em;
                text-align: justify;
                min-height: 20vh;
            }
        </style>
    </head>
    <body>
        <!-- Cover Page -->
        <div class="cover-page">
            <div style="text-align: center; margin-bottom: 4cm;">            
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2cm;">
                    <div style="width: 80px; height: 80px;">
                        <!-- Nepal Government Logo placeholder -->
                    </div>
                    <div style="flex-grow: 1;">
                        <div style="color: #1e3a8a; font-size: 20pt; font-weight: 700; margin-bottom: 0.5em;">
                            लुङ्ग्री गाउँपालिका
                        </div>
                        <div style="color: #1e40af; font-size: 16pt; font-weight: 600; margin-bottom: 0.5em;">
                            गाउँकार्यपालिकाको कार्यालय
                        </div>
                        <div style="color: #1e40af; font-size: 12pt; margin-bottom: 0.5em;">
                            लुम्बिनी प्रदेश, नेपाल सरकार
                        </div>
                    </div>
                    <div style="width: 80px; height: 80px;">
                        <!-- Municipality Logo placeholder -->
                    </div>
                </div>
                
                <!-- Main Title Section -->
                <div style="color: #dc2626; padding: 1.5em; margin: 2cm 0; font-size: 24pt; font-weight: 700;">
                    गाउँपालिका पार्श्वचित्र
                </div>

                <!-- Bottom Section -->
                <div style="color: #0f172a; padding: 1em; margin-top: 1cm;">
                    <div style="font-size: 16pt; font-weight: 600;">मस्यौदा प्रतिवेदन</div>
                    <div style="font-size: 18pt; font-weight: 700;">२०८१</div>
                </div>
            </div>
        </div>

        <!-- Table of Contents -->
        <div class="toc-page">
            <h1 class="toc-title" style="color: #1e3a8a; border-bottom: 3px solid #0ea5e9;">विषयसूची</h1>
            
            <!-- Categories and Sections -->
            <div class="toc-item level-1">
                <span class="toc-link">१. जनसांख्यिकीय विवरण</span>
                <span class="page-ref"><a href="#category-1"></a></span>
            </div>

            <div class="toc-item level-2">
                <span class="toc-link">१.१ कुल जनसंख्या</span>
                <span class="page-ref"><a href="#section-1-1"></a></span>
            </div>

            <div class="toc-item level-2">
                <span class="toc-link">१.२ लिंग अनुपात</span>
                <span class="page-ref"><a href="#section-1-2"></a></span>
            </div>
            
            <div class="toc-item level-1">
                <span class="toc-link">२. आर्थिक अवस्था</span>
                <span class="page-ref"><a href="#category-2"></a></span>
            </div>

            <div class="toc-item level-2">
                <span class="toc-link">२.१ कृषि उत्पादन</span>
                <span class="page-ref"><a href="#section-2-1"></a></span>
            </div>

            <div class="toc-item level-2">
                <span class="toc-link">२.२ पशुपालन</span>
                <span class="page-ref"><a href="#section-2-2"></a></span>
            </div>
            
            <div class="toc-item level-1">
                <span class="toc-link">३. पूर्वाधार विकास</span>
                <span class="page-ref"><a href="#category-3"></a></span>
            </div>

            <div class="toc-item level-2">
                <span class="toc-link">३.१ यातायात सुविधा</span>
                <span class="page-ref"><a href="#section-3-1"></a></span>
            </div>
        </div>

        <!-- Main Content Start -->
        <div class="main-content-start">
            <div class="section-break" id="category-1">
                <h1 class="category-title" style="color: #dc2626; text-align: center; padding: 0.5em;">
                    परिच्छेद – १ः जनसांख्यिकीय विवरण
                </h1>
                
                <div class="section-content" id="section-1-1">
                    <h2 class="section-header level-2" style="color: #1e40af; border-bottom: 2px solid #0ea5e9; padding-bottom: 0.3em; font-size: 16pt; margin-top: 2em;">
                        १.१ कुल जनसंख्या
                    </h2>
                    
                    <div class="content-section" style="margin-left: 0;">
                        <p>लुङ्ग्री गाउँपालिकाको कुल जनसंख्या २०७८ को जनगणना अनुसार ३२,४५६ रहेको छ।</p>
                        <p>यो संख्यामा पुरुष १६,२३४ र महिला १६,२२२ रहेका छन्।</p>
                    </div>
                </div>

                <div class="section-content" id="section-1-2">
                    <h2 class="section-header level-2" style="color: #1e40af; border-bottom: 2px solid #0ea5e9; padding-bottom: 0.3em; font-size: 16pt; margin-top: 2em;">
                        १.२ लिंग अनुपात
                    </h2>
                    
                    <div class="content-section" style="margin-left: 0;">
                        <p>प्रति १०० महिलामा १००.०७ पुरुष रहेको देखिन्छ।</p>
                        <p>यो अनुपात राष्ट्रिय औसत भन्दा राम्रो रहेको छ।</p>
                    </div>
                </div>
            </div>
            
            <div class="section-break" id="category-2">
                <h1 class="category-title" style="color: #dc2626; text-align: center; padding: 0.5em;">
                    परिच्छेद – २ः आर्थिक अवस्था
                </h1>
                
                <div class="section-content" id="section-2-1">
                    <h2 class="section-header level-2" style="color: #1e40af; border-bottom: 2px solid #0ea5e9; padding-bottom: 0.3em; font-size: 16pt; margin-top: 2em;">
                        २.१ कृषि उत्पादन
                    </h2>
                    
                    <div class="content-section" style="margin-left: 0;">
                        <p>मुख्यतः धान, गहुँ, मकै, र तरकारी उत्पादन गरिन्छ।</p>
                        <p>कुल कृषि योग्य भूमि २,३४५ हेक्टेयर रहेको छ।</p>
                    </div>
                </div>

                <div class="section-content" id="section-2-2">
                    <h2 class="section-header level-2" style="color: #1e40af; border-bottom: 2px solid #0ea5e9; padding-bottom: 0.3em; font-size: 16pt; margin-top: 2em;">
                        २.२ पशुपालन
                    </h2>
                    
                    <div class="content-section" style="margin-left: 0;">
                        <p>गाई, भैंसी, बाख्रा, र कुखुराको व्यापारिक पालन गरिन्छ।</p>
                        <p>दुग्ध उत्पादन दैनिक ५,००० लिटर पुगेको छ।</p>
                    </div>
                </div>
            </div>
            
            <div class="section-break" id="category-3">
                <h1 class="category-title" style="color: #dc2626; text-align: center; padding: 0.5em;">
                    परिच्छेद – ३ः पूर्वाधार विकास
                </h1>
                
                <div class="section-content" id="section-3-1">
                    <h2 class="section-header level-2" style="color: #1e40af; border-bottom: 2px solid #0ea5e9; padding-bottom: 0.3em; font-size: 16pt; margin-top: 2em;">
                        ३.१ यातायात सुविधा
                    </h2>
                    
                    <div class="content-section" style="margin-left: 0;">
                        <p>कुल सडक लम्बाइ १२५ किलोमिटर रहेको छ।</p>
                        <p>यसमध्ये ७५ किलोमिटर पक्की सडक र ५० किलोमिटर कच्ची सडक छ।</p>
                    </div>
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
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
            f.write(pdf_bytes)
            temp_path = f.name

        print(f"✅ Full report test PDF generated: {temp_path}")
        print(f"📏 PDF size: {len(pdf_bytes)} bytes")

        # Open PDF
        abs_path = os.path.abspath(temp_path)
        if os.name == "nt":  # Windows
            os.startfile(abs_path)

        print("📖 Please verify TOC page numbers:")
        print("   - Cover page: No page number")
        print("   - TOC page: Should show page २ (2)")
        print("   - Category 1: Should show page ३ (3) in TOC")
        print("   - Section 1.1: Should show page ३ (3) in TOC")
        print("   - Section 1.2: Should show page ३ (3) in TOC")
        print("   - Category 2: Should show page ४ (4) in TOC")
        print("   - Section 2.1: Should show page ४ (4) in TOC")
        print("   - Section 2.2: Should show page ४ (4) in TOC")
        print("   - Category 3: Should show page ५ (5) in TOC")
        print("   - Section 3.1: Should show page ५ (5) in TOC")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_full_report_structure()
