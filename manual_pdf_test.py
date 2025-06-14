#!/usr/bin/env python3
"""
Quick test to generate a full PDF and open it for manual inspection
"""
import os
import sys
import webbrowser

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gadhawa_report.settings.development')

import django
django.setup()

from apps.reports.views.pdf import GenerateFullReportPDFView
from django.http import HttpRequest
from django.test import RequestFactory

def generate_and_open_pdf():
    """Generate PDF and open it"""
    print("🔄 Generating full report PDF...")
    
    # Create a proper request
    factory = RequestFactory()
    request = factory.get('/reports/pdf/full/')
    
    # Create view and generate PDF
    view = GenerateFullReportPDFView()
    response = view.get(request)
    
    if response.status_code == 200:
        # Save PDF to current directory with a descriptive name
        pdf_filename = "gadhawa_full_report_test.pdf"
        with open(pdf_filename, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ PDF generated successfully!")
        print(f"📄 PDF saved as: {pdf_filename}")
        print(f"📏 PDF size: {len(response.content):,} bytes")
        
        # Open PDF in default viewer
        abs_path = os.path.abspath(pdf_filename)
        print(f"🖼️  Opening PDF: {abs_path}")
        
        try:
            # Open PDF in default application
            if os.name == 'nt':  # Windows
                os.startfile(abs_path)
            else:  # macOS/Linux
                webbrowser.open(f'file://{abs_path}')
            
            print("📖 PDF opened in default viewer")
            print("👀 Please check:")
            print("   1. Table of Contents shows correct page numbers (not all '१')")
            print("   2. Page numbers are in Nepali digits")
            print("   3. Each section appears on its referenced page")
            
        except Exception as e:
            print(f"⚠️  Could not auto-open PDF: {e}")
            print(f"📁 Please manually open: {abs_path}")
        
        return True
    else:
        print(f"❌ PDF generation failed with status: {response.status_code}")
        if hasattr(response, 'content'):
            print(f"Error content: {response.content}")
        return False

if __name__ == '__main__':
    print("=== Manual PDF Test for Page Numbers ===")
    generate_and_open_pdf()
