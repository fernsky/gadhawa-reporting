#!/usr/bin/env python
"""
Test script to generate PDF and verify TOC pages and category page breaks
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to the Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gadhawa_report.settings.development')

# Initialize Django
django.setup()

from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
from apps.reports.models import ReportCategory, ReportSection, ReportFigure, ReportTable, PublicationSettings
from django.utils import timezone

def test_toc_and_page_breaks():
    print("🔍 Testing TOC Page Numbers and Category Page Breaks")
    print("=" * 55)
    
    # Get test data or create some if none exists
    categories = ReportCategory.objects.filter(is_active=True).prefetch_related(
        'sections__figures',
        'sections__tables'
    ).order_by('order')
    
    if not categories.exists():
        print("⚠️  No categories found. Creating test data...")
        # Create test data
        cat1 = ReportCategory.objects.create(
            name="Demographics",
            name_nepali="जनसांख्यिकी",
            category_number=1,
            order=1,
            is_active=True
        )
        
        cat2 = ReportCategory.objects.create(
            name="Economics",
            name_nepali="अर्थतन्त्र",
            category_number=2,
            order=2,
            is_active=True
        )
        
        # Add sections
        section1 = ReportSection.objects.create(
            category=cat1,
            title="Population Overview",
            title_nepali="जनसंख्या विवरण",
            section_number="1.1",
            content="This is test content for population overview. " * 20,
            order=1,
            is_published=True
        )
        
        section2 = ReportSection.objects.create(
            category=cat2,
            title="Economic Analysis",
            title_nepali="आर्थिक विश्लेषण",
            section_number="2.1",
            content="This is test content for economic analysis. " * 20,
            order=1,
            is_published=True
        )
        
        categories = ReportCategory.objects.filter(is_active=True).prefetch_related(
            'sections__figures',
            'sections__tables'
        ).order_by('order')
    
    # Get all figures and tables for lists
    figures = ReportFigure.objects.select_related('section__category').order_by('figure_number')
    tables = ReportTable.objects.select_related('section__category').order_by('table_number')
    
    # Create context
    context = {
        'municipality_name': "गधावा गाउँपालिका",
        'municipality_name_english': "Gadhawa Rural Municipality",
        'publication_settings': None,
        'categories': categories,
        'figures': figures,
        'tables': tables,
        'total_figures': figures.count(),
        'total_tables': tables.count(),
        'generated_date': timezone.now(),
    }
    
    # Render HTML
    print("📝 Rendering HTML template...")
    html_content = render_to_string('reports/pdf_full_report.html', context)
    
    # Save HTML for debugging
    with open('test_toc_output.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("📄 HTML saved as 'test_toc_output.html'")
    
    # Create CSS path
    css_path = project_dir / 'static' / 'css' / 'pdf.css'
    if not css_path.exists():
        print(f"⚠️  CSS file not found at: {css_path}")
        return
    
    print(f"✅ CSS file found: {css_path}")
    
    # Generate PDF with WeasyPrint
    print("🖨️  Generating PDF with WeasyPrint...")
    try:
        font_config = FontConfiguration()
        
        # Create HTML object
        html_doc = HTML(string=html_content, base_url=str(project_dir) + '/')
        
        # Create CSS object
        css_doc = CSS(filename=str(css_path), font_config=font_config)
        
        # Generate PDF
        pdf_bytes = html_doc.write_pdf(stylesheets=[css_doc], font_config=font_config)
        
        # Save PDF
        output_file = 'test_toc_pages.pdf'
        with open(output_file, 'wb') as f:
            f.write(pdf_bytes)
        
        print(f"✅ PDF generated successfully!")
        print(f"PDF size: {len(pdf_bytes)} bytes")
        print(f"📄 PDF saved as '{output_file}'")
        
        # Analysis
        print("\n🔍 Analysis:")
        print(f"   Categories: {categories.count()}")
        print(f"   Total sections: {sum(cat.sections.count() for cat in categories)}")
        print(f"   Figures: {figures.count()}")
        print(f"   Tables: {tables.count()}")
        
        print("\n✨ Testing completed!")
        print("Check the PDF to verify:")
        print("  1. TOC page numbers are showing in Nepali digits")
        print("  2. Categories start immediately without page gaps")
        print("  3. Page numbering is continuous")
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_toc_and_page_breaks()
