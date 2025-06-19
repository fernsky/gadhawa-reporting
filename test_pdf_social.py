#!/usr/bin/env python
"""
Test script to generate a PDF report and verify social section inclusion.
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to the Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lungri_report.settings.development")
django.setup()

from django.test import RequestFactory
from apps.reports.views.pdf import PDFReportView


def test_pdf_generation():
    """Test PDF generation with social section"""
    print("Testing PDF Generation with Social Section...")
    print("=" * 60)

    # Create a mock request
    factory = RequestFactory()
    request = factory.get("/reports/pdf/full/")

    # Initialize PDF view
    view = PDFReportView()
    view.request = request

    print("1. Testing context data generation...")
    try:
        # Test getting context data (this processes all sections including social)
        context = view.get_context_data()

        print("   ✓ Context data generated successfully")
        print(f"   Available sections: {list(context.keys())}")

        # Check if social data is included
        if "all_social_data" in context:
            print("   ✓ Social data found in context")
            social_data = context["all_social_data"]
            print(f"   Social categories: {list(social_data.keys())}")

            # Check each social category
            for category, data in social_data.items():
                has_charts = "charts" in data and data["charts"]
                municipality_data = bool(data.get("municipality_data"))
                ward_data = bool(data.get("ward_data"))
                total_count = data.get("total_population", 0) or data.get(
                    "total_households", 0
                )

                print(f"   - {category}:")
                print(f"     Charts: {'✓' if has_charts else '✗'}")
                print(f"     Municipality data: {'✓' if municipality_data else '✗'}")
                print(f"     Ward data: {'✓' if ward_data else '✗'}")
                print(f"     Total count: {total_count}")
        else:
            print("   ✗ Social data NOT found in context")

        print()

    except Exception as e:
        print(f"   ✗ Error generating context: {e}")
        import traceback

        traceback.print_exc()

    print("2. Testing template rendering...")
    try:
        # Test template rendering (this uses the social_full_report.html)
        response = view.get(request)

        if response.status_code == 200:
            print("   ✓ PDF template rendered successfully")
            print(f"   Response content type: {response.get('Content-Type', 'N/A')}")

            # Check if social section is in the HTML content
            content = response.content.decode("utf-8")

            # Check for social section markers
            social_markers = [
                "परिच्छेद – ५ः सामाजिक अवस्था",  # Social chapter title
                "social_full_report.html",  # Template inclusion
                "शौचालय प्रयोगको अवस्था",  # Toilet type section
                "साक्षरता विवरण",  # Literacy section
            ]

            found_markers = []
            for marker in social_markers:
                if marker in content:
                    found_markers.append(marker)

            if found_markers:
                print(
                    f"   ✓ Social section markers found: {len(found_markers)}/{len(social_markers)}"
                )
                for marker in found_markers:
                    print(f"     - {marker}")
            else:
                print("   ✗ No social section markers found")

        else:
            print(f"   ✗ PDF template rendering failed: {response.status_code}")

    except Exception as e:
        print(f"   ✗ Error rendering template: {e}")
        import traceback

        traceback.print_exc()

    print("=" * 60)
    print("PDF Generation Test Complete!")


if __name__ == "__main__":
    test_pdf_generation()
