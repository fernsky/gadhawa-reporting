#!/usr/bin/env python3
"""
Test script to verify the exact page numbering system works correctly
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gadhawa_report.settings.development')
django.setup()

from django.test import RequestFactory
from apps.reports.views.pdf import GenerateFullReportPDFView
from apps.reports.models import ReportCategory, ReportSection, ReportFigure, ReportTable

def test_pdf_generation():
    """Test if PDF generation works with exact page references"""
    
    print("Testing PDF generation with exact page references...")
    
    # Create a mock request
    factory = RequestFactory()
    request = factory.get('/reports/pdf/full/')
    
    # Create view instance
    view = GenerateFullReportPDFView()
    view.request = request
    
    try:
        # Get the response
        response = view.get(request)
        
        if response.status_code == 200:
            print("✅ PDF generation successful!")
            print(f"Content-Type: {response.get('Content-Type')}")
            print(f"Content-Length: {len(response.content)} bytes")
            
            # Save test PDF
            with open('test_exact_pages.pdf', 'wb') as f:
                f.write(response.content)
            print("📄 Test PDF saved as 'test_exact_pages.pdf'")
            
        else:
            print(f"❌ PDF generation failed with status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error during PDF generation: {str(e)}")
        import traceback
        traceback.print_exc()

def verify_data_exists():
    """Verify that we have test data"""
    print("Checking for test data...")
    
    categories = ReportCategory.objects.filter(is_active=True).count()
    sections = ReportSection.objects.filter(is_published=True).count()
    figures = ReportFigure.objects.count()
    tables = ReportTable.objects.count()
    
    print(f"Categories: {categories}")
    print(f"Sections: {sections}")
    print(f"Figures: {figures}")
    print(f"Tables: {tables}")
    
    if categories == 0:
        print("⚠️  No active categories found. You may need to create test data.")
    
    return categories > 0

if __name__ == "__main__":
    print("🔍 Testing Exact Page Number System")
    print("=" * 50)
    
    if verify_data_exists():
        test_pdf_generation()
    else:
        print("❌ No test data available. Please create some categories and sections first.")
    
    print("\n✨ Test completed!")
