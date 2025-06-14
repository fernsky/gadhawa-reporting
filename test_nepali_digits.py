#!/usr/bin/env python3
"""
Test script to verify Nepali digit page numbering
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gadhawa_report.settings.development')
django.setup()

from django.template.loader import render_to_string
from apps.reports.models import ReportCategory, ReportSection, ReportFigure, ReportTable
from weasyprint import HTML
import io

def test_nepali_digit_pdf():
    """Test PDF generation with Nepali digits"""
    
    print("Testing PDF generation with Nepali digits...")
    
    try:
        # Get minimal data for testing
        categories = ReportCategory.objects.filter(
            is_active=True,
            sections__is_published=True
        ).distinct().prefetch_related(
            'sections__figures',
            'sections__tables'
        ).order_by('order')[:2]  # Just first 2 categories for testing
        
        context = {
            'municipality_name': "गढवा गाउँपालिका",
            'municipality_name_english': "Gadhawa Rural Municipality",
            'publication_settings': None,
            'categories': categories,
            'figures': [],
            'tables': [],
            'total_figures': 0,
            'total_tables': 0,
            'generated_date': '२०८१',  # Already in Nepali
        }
        
        # Render template
        html_content = render_to_string('reports/pdf_full_report.html', context)
        
        # Generate PDF with WeasyPrint
        pdf_buffer = io.BytesIO()
        
        # Use base URL for static files
        base_url = "file://" + os.path.abspath(".") + "/"
        HTML(string=html_content, base_url=base_url).write_pdf(pdf_buffer)
        
        pdf_content = pdf_buffer.getvalue()
        print(f"✅ PDF with Nepali digits generated successfully")
        print(f"PDF size: {len(pdf_content)} bytes")
        
        # Save PDF
        with open('test_nepali_digits.pdf', 'wb') as f:
            f.write(pdf_content)
        print("📄 PDF with Nepali digits saved as 'test_nepali_digits.pdf'")
        
        # Also save HTML for inspection
        with open('test_nepali_output.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        print("📄 HTML saved as 'test_nepali_output.html'")
        
        return True
        
    except Exception as e:
        print(f"❌ Error generating PDF with Nepali digits: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def check_css_path():
    """Check if CSS file is accessible"""
    import os
    css_path = os.path.join("static", "css", "pdf.css")
    
    if os.path.exists(css_path):
        print(f"✅ CSS file found: {css_path}")
        return True
    else:
        print(f"❌ CSS file not found: {css_path}")
        print("Current directory:", os.getcwd())
        print("Files in static/css/:", os.listdir("static/css/") if os.path.exists("static/css/") else "Directory not found")
        return False

if __name__ == "__main__":
    print("🔍 Testing Nepali Digit Page Numbering")
    print("=" * 50)
    
    if check_css_path():
        test_nepali_digit_pdf()
    else:
        print("❌ Cannot proceed without CSS file")
    
    print("\n✨ Testing completed!")
    print("Check 'test_nepali_digits.pdf' to verify Nepali page numbers")
