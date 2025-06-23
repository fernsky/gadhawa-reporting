#!/usr/bin/env python
"""
Quick test script to verify the TOC page numbers and section breaks are working
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to the Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

# Set Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gadhawa_report.settings.development")

# Initialize Django
django.setup()

from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from apps.reports.models import ReportCategory
from django.utils import timezone


def quick_test():
    print("🧪 Quick Test - TOC & Page Breaks")
    print("=" * 40)

    # Simple test data
    categories = ReportCategory.objects.filter(is_active=True).prefetch_related(
        "sections"
    )[:2]

    context = {
        "municipality_name": "गढवा गाउँपालिका",
        "categories": categories,
        "figures": [],
        "tables": [],
        "generated_date": timezone.now(),
    }

    html_content = render_to_string("reports/pdf_full_report.html", context)
    css_path = project_dir / "static" / "css" / "pdf.css"

    # Generate PDF
    try:
        html_doc = HTML(string=html_content, base_url=str(project_dir) + "/")
        css_doc = CSS(filename=str(css_path))
        pdf_bytes = html_doc.write_pdf(stylesheets=[css_doc])

        with open("quick_test.pdf", "wb") as f:
            f.write(pdf_bytes)

        print("✅ PDF Generated Successfully!")
        print(f"📄 Size: {len(pdf_bytes)} bytes")
        print("📄 Saved as: quick_test.pdf")

        print("\n🔍 Check the PDF to verify:")
        print("  ✓ TOC has page numbers in Nepali digits")
        print("  ✓ Categories don't start on separate pages")
        print("  ✓ Page numbering is continuous")
        print("  ✓ No page gaps between categories")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    quick_test()
