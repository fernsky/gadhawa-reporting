#!/usr/bin/env python3
"""
Debug script to check the HTML content being generated for the PDF
to verify the data-target attributes and CSS are correct
"""
import os
import sys
# गाउँ कार्यपालिकाको कार्यालय, वडाचौर, रोल्पा, लुम्बिनी प्रदेश
# पूर्वाधार, कृषि र पर्यटनः समृद्ध लुङ्ग्रीको मुख्य साधन
# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lungri_report.settings.development')

import django
django.setup()

from django.template.loader import render_to_string
from apps.reports.models import ReportCategory, ReportSection, ReportFigure, ReportTable, PublicationSettings

def debug_html_output():
    """Debug the HTML template to check data-target attributes"""
    print("🔍 Debugging HTML template output...")
    
    # Get context data
    categories = ReportCategory.objects.prefetch_related('sections').filter(is_active=True).order_by('order')
    figures = ReportFigure.objects.select_related('section__category').order_by('figure_number')
    tables = ReportTable.objects.select_related('section__category').order_by('table_number')
    
    try:
        publication_settings = PublicationSettings.objects.first()
    except:
        publication_settings = None
    
    context = {
        'categories': categories,
        'figures': figures,
        'tables': tables,
        'publication_settings': publication_settings,
    }
    
    print(f"📊 Found {categories.count()} categories, {figures.count()} figures, {tables.count()} tables")
    
    # Render the template
    try:
        html_content = render_to_string('reports/pdf_full_report.html', context)
        
        # Save HTML for inspection
        with open('debug_html_output.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("✅ HTML template rendered successfully")
        print("📄 HTML saved as: debug_html_output.html")
        
        # Check for key elements
        toc_refs = html_content.count('data-target="#category-')
        section_refs = html_content.count('data-target="#section-')
        figure_refs = html_content.count('data-target="#figure-')
        table_refs = html_content.count('data-target="#table-')
        
        print(f"🔗 Found {toc_refs} category references")
        print(f"🔗 Found {section_refs} section references") 
        print(f"🔗 Found {figure_refs} figure references")
        print(f"🔗 Found {table_refs} table references")
        
        # Check for actual target IDs
        category_ids = html_content.count('id="category-')
        section_ids = html_content.count('id="section-')
        figure_ids = html_content.count('id="figure-')
        table_ids = html_content.count('id="table-')
        
        print(f"🎯 Found {category_ids} category target IDs")
        print(f"🎯 Found {section_ids} section target IDs")
        print(f"🎯 Found {figure_ids} figure target IDs")
        print(f"🎯 Found {table_ids} table target IDs")
        
        # Check CSS
        if 'target-counter(attr(data-target), page, nepali-numerals)' in html_content:
            print("✅ Correct CSS found in HTML")
        else:
            print("❌ CSS might be missing or incorrect")
            
        if 'page-ref' in html_content:
            print("✅ page-ref class found in HTML")
        else:
            print("❌ page-ref class missing")
            
        # Show first few TOC entries for debugging
        print("\n🔍 Sample TOC entries:")
        lines = html_content.split('\n')
        in_toc = False
        toc_count = 0
        for line in lines:
            if 'toc-item' in line and toc_count < 5:
                print(f"   {line.strip()}")
                toc_count += 1
            if 'toc-page' in line:
                in_toc = True
            elif 'main-content-start' in line:
                in_toc = False
                
        return True
        
    except Exception as e:
        print(f"❌ Error rendering template: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("=== Debugging HTML Template ===")
    debug_html_output()
