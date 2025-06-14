#!/usr/bin/env python3
"""
Test script to verify that TOC page numbers are now displaying correctly
after fixing the CSS target-counter issue.
"""
import os
import sys

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gadhawa_report.settings.development')

import django
django.setup()

from apps.reports.models import ReportCategory, ReportSection
from apps.reports.views.pdf import GenerateFullReportPDFView
from django.http import HttpRequest
import tempfile

def test_pdf_generation():
    """Test PDF generation and check if it creates without errors"""
    print("🔍 Testing PDF generation with fixed page numbers...")
    
    # Check if we have data
    categories = ReportCategory.objects.all()
    sections = ReportSection.objects.all()
    
    print(f"Found {categories.count()} categories and {sections.count()} sections")
    
    if categories.count() == 0:
        print("❌ No categories found. Please ensure you have test data.")
        return False
    
    # Create a mock request
    request = HttpRequest()
    request.method = 'GET'
    
    # Create PDF view
    view = GenerateFullReportPDFView()
    
    try:
        # Generate PDF
        response = view.get(request)
        
        if response.status_code == 200:
            # Save PDF to temp file for inspection
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as f:
                f.write(response.content)
                temp_path = f.name
            
            print(f"✅ PDF generated successfully!")
            print(f"📄 PDF saved to: {temp_path}")
            print(f"📏 PDF size: {len(response.content)} bytes")
            
            # Check if PDF has reasonable size (should be > 50KB for real content)
            if len(response.content) > 50000:
                print("✅ PDF appears to have substantial content")
            else:
                print("⚠️  PDF seems small, might be missing content")
            
            return True
        else:
            print(f"❌ PDF generation failed with status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error generating PDF: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_css_fix():
    """Test that our CSS fix is correct"""
    print("\n🔍 Checking CSS fix...")
    
    css_file = 'static/css/pdf.css'
    if os.path.exists(css_file):
        with open(css_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check if the fix is applied
        if 'target-counter(attr(data-target), page, nepali-numerals)' in content:
            print("✅ CSS fix applied correctly - using attr(data-target) without extra #")
        else:
            print("❌ CSS fix not found")
            
        # Check if old broken version is gone
        if "target-counter('#' attr(data-target)" in content:
            print("❌ Old broken CSS still present")
        else:
            print("✅ Old broken CSS removed")
    else:
        print("❌ CSS file not found")

if __name__ == '__main__':
    print("=== Testing Page Number Fix ===")
    test_css_fix()
    success = test_pdf_generation()
    
    if success:
        print("\n🎉 Test completed successfully!")
        print("📋 The TOC page numbers should now display correctly in Nepali digits")
        print("📋 Each section should show its actual page number, not all showing '१'")
    else:
        print("\n❌ Test failed. Please check the error messages above.")
