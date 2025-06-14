#!/usr/bin/env python3
"""
Detailed test script to check WeasyPrint functionality and exact page references
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gadhawa_report.settings.development')
django.setup()

from django.test import RequestFactory
from django.template.loader import render_to_string
from apps.reports.views.pdf import GenerateFullReportPDFView
from apps.reports.models import ReportCategory, ReportSection, ReportFigure, ReportTable, PublicationSettings
from weasyprint import HTML
import io

def test_weasyprint_directly():
    """Test WeasyPrint directly with our template"""
    
    print("Testing WeasyPrint directly...")
    
    try:
        # Get data
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
            'municipality_name': "गढवा गाउँपालिका",
            'municipality_name_english': "Gadhawa Rural Municipality",
            'publication_settings': None,
            'categories': categories,
            'figures': figures,
            'tables': tables,
            'total_figures': figures.count(),
            'total_tables': tables.count(),
            'generated_date': '2024-01-01',
        }
        
        # Render template
        html_content = render_to_string('reports/pdf_full_report.html', context)
        
        print(f"✅ Template rendered successfully")
        print(f"HTML content length: {len(html_content)} characters")
        
        # Save HTML for inspection
        with open('test_output.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        print("📄 HTML saved as 'test_output.html' for inspection")
        
        # Generate PDF with WeasyPrint
        pdf_buffer = io.BytesIO()
        HTML(string=html_content).write_pdf(pdf_buffer)
        
        pdf_content = pdf_buffer.getvalue()
        print(f"✅ WeasyPrint PDF generated successfully")
        print(f"PDF size: {len(pdf_content)} bytes")
        
        # Save PDF
        with open('test_weasyprint_direct.pdf', 'wb') as f:
            f.write(pdf_content)
        print("📄 Direct WeasyPrint PDF saved as 'test_weasyprint_direct.pdf'")
        
        return True
        
    except Exception as e:
        print(f"❌ Error with WeasyPrint: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_template_content():
    """Test the template content structure"""
    print("\nTesting template content structure...")
    
    # Basic template test
    simple_context = {
        'municipality_name': "गढवा गाउँपालिका",
        'categories': [],
        'figures': [],
        'tables': [],
        'total_figures': 0,
        'total_tables': 0,
        'generated_date': '2024-01-01',
    }
    
    try:
        html_content = render_to_string('reports/pdf_full_report.html', simple_context)
        
        # Check for key elements
        checks = [
            ('विषयसूची', 'Table of Contents'),
            ('page-ref', 'Page references'),
            ('category-', 'Category anchors'),
            ('section-', 'Section anchors'),
            ('toc-item', 'TOC items'),
            ('main-content-start', 'Main content'),
        ]
        
        for check, description in checks:
            if check in html_content:
                print(f"✅ {description} found")
            else:
                print(f"❌ {description} missing")
        
        return True
        
    except Exception as e:
        print(f"❌ Template error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔍 Detailed WeasyPrint and Template Testing")
    print("=" * 60)
    
    # Test template first
    if test_template_content():
        # Test WeasyPrint
        test_weasyprint_directly()
    
    print("\n✨ Detailed testing completed!")
    print("Check the generated files for analysis:")
    print("- test_output.html (template output)")
    print("- test_weasyprint_direct.pdf (WeasyPrint PDF)")
