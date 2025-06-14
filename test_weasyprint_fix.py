#!/usr/bin/env python
"""
Fix WeasyPrint CSS loading and test TOC page numbers
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gadhawa_report.settings.development')
django.setup()

from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from apps.reports.models import ReportCategory, ReportFigure, ReportTable, PublicationSettings

def test_toc_page_numbers():
    print("🎯 WeasyPrint CSS Fix & TOC Page Numbers Test")
    print("=" * 55)
    
    # Get data
    try:
        publication_settings = PublicationSettings.objects.first()
    except:
        publication_settings = None
        
    categories = ReportCategory.objects.filter(
        is_active=True,
        sections__is_published=True
    ).distinct().prefetch_related(
        'sections__figures',
        'sections__tables'
    ).order_by('order')
    
    figures = ReportFigure.objects.select_related('section__category').order_by('figure_number')
    tables = ReportTable.objects.select_related('section__category').order_by('table_number')
    
    context = {
        'municipality_name': 'गधावा गाउँपालिका',
        'municipality_name_english': 'Gadhawa Rural Municipality',
        'publication_settings': publication_settings,
        'categories': categories,
        'figures': figures,
        'tables': tables,
        'total_figures': figures.count(),
        'total_tables': tables.count(),
    }
    
    # Create a simple HTML template without Django static tags
    html_template = """
<!DOCTYPE html>
<html lang="ne">
<head>
    <meta charset="UTF-8">
    <title>गढवा गाउँपालिकाको पार्श्वचित्र</title>
    <style>
        /* Custom Nepali counter style */
        @counter-style nepali-numerals {
            system: numeric;
            symbols: "०" "१" "२" "३" "४" "५" "६" "७" "८" "९";
            suffix: "";
        }

        /* Page setup */
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
            @bottom-right { content: ""; }
        }

        /* Base typography */
        body {
            font-family: 'Noto Sans Devanagari', 'DejaVu Sans', sans-serif;
            font-size: 11pt;
            line-height: 1.5;
            color: #333;
            margin: 0;
            padding: 0;
        }

        /* Cover page */
        .cover-page {
            page-break-after: always;
            text-align: center;
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }

        /* TOC */
        .toc-page {
            page-break-before: always;
            page-break-after: always;
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

        /* For anchor-based page references */
        .page-ref a::after {
            content: target-counter(attr(href), page, nepali-numerals);
        }

        .page-ref a {
            color: inherit;
            text-decoration: none;
            font-weight: inherit;
        }

        /* Main content */
        .main-content-start {
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

        .section-break {
            page-break-before: auto;
            page-break-after: avoid;
            page-break-inside: avoid;
        }

        .section-break:first-of-type {
            page-break-before: always;
        }

        .section-header.level-2 {
            font-size: 16pt;
            color: #1e40af;
            border-bottom: 2px solid #0ea5e9;
            padding-bottom: 0.3em;
            margin-top: 2em;
            margin-bottom: 1em;
        }
    </style>
</head>
<body>
    <!-- Cover Page -->
    <div class="cover-page">
        <div style="color: #dc2626; padding: 1.5em; margin: 2cm 0; font-size: 24pt; font-weight: 700;">
            गाउँपालिका पार्श्वचित्र
        </div>
        <div style="color: #0f172a; padding: 1em; margin-top: 1cm;">
            <div style="font-size: 16pt; font-weight: 600;">मस्यौदा प्रतिवेदन</div>
            <div style="font-size: 18pt; font-weight: 700;">२०८१</div>
        </div>
    </div>

    <!-- Table of Contents -->
    <div class="toc-page">
        <h1 class="toc-title">विषयसूची</h1>
        
        """ + "".join([f"""
        <div class="toc-item level-1">
            <span class="toc-link">{category.category_number}. {category.name_nepali or category.name}</span>
            <span class="page-ref">
                <a href="#category-{category.id}"></a>
            </span>
        </div>
        """ for category in categories]) + """
    </div>

    <!-- Main Content -->
    <div class="main-content-start">
        """ + "".join([f"""
        <div class="section-break" id="category-{category.id}">
            <h1 class="category-title">
                परिच्छेद – {category.category_number}ः {category.name_nepali or category.name}
            </h1>
            <p>यो {category.name_nepali or category.name} को सामग्री हो। यसमा विभिन्न खण्डहरू छन्।</p>
            <p>lorem ipsum content to fill the page and create multiple pages for proper testing.</p>
            <p>More content here to ensure we have enough text to span multiple pages and test the page numbering system.</p>
        </div>
        """ for category in categories]) + """
    </div>
</body>
</html>
    """
    
    print(f"📊 Categories found: {categories.count()}")
    print(f"📊 Figures found: {figures.count()}")
    print(f"📊 Tables found: {tables.count()}")
    
    try:
        # Generate PDF
        html_doc = HTML(string=html_template)
        pdf_content = html_doc.write_pdf()
        
        # Save PDF
        filename = "test_toc_fix.pdf"
        with open(filename, 'wb') as f:
            f.write(pdf_content)
        
        print(f"✅ Test PDF generated successfully!")
        print(f"📄 Size: {len(pdf_content)} bytes")
        print(f"📄 Saved as: {filename}")
        print(f"🔍 Check if TOC page numbers are showing in Nepali digits")
        
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_toc_page_numbers()
