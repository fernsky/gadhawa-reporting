#!/usr/bin/env python
"""
Test PDF generation with Major Subject Processor
"""
import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lungri_report.settings.development")
django.setup()

from apps.reports.views.pdf import generate_full_pdf_report


def test_pdf_generation():
    """Test PDF generation with major subject processor"""
    print("Testing PDF generation with Major Subject processor...")

    try:
        # Generate PDF report
        print("Generating PDF report...")
        response = generate_full_pdf_report(None)  # No request object needed for test

        if response.status_code == 200:
            print("✓ PDF generated successfully")
            print(f"Content type: {response.get('Content-Type')}")
            print(f"Response length: {len(response.content)} bytes")
        else:
            print(f"✗ PDF generation failed with status: {response.status_code}")

    except Exception as e:
        print(f"✗ Error generating PDF: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_pdf_generation()
