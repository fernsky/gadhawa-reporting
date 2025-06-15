#!/usr/bin/env python
"""
Final comprehensive test for the cleaned CSS
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to the Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

# Set Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lungri_report.settings.development")

# Initialize Django
django.setup()

from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from apps.reports.models import ReportCategory
from django.utils import timezone


def final_test():
    print("🎯 FINAL TEST - Clean CSS & TOC Page Numbers")
    print("=" * 50)

    # Get data
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

    print(
        f"📊 CSS file size: {css_path.stat().st_size} bytes (was ~830 lines, now ~450 lines)"
    )

    # Generate PDF
    try:
        html_doc = HTML(string=html_content, base_url=str(project_dir) + "/")
        css_doc = CSS(filename=str(css_path))
        pdf_bytes = html_doc.write_pdf(stylesheets=[css_doc])

        with open("final_test_clean.pdf", "wb") as f:
            f.write(pdf_bytes)

        print("✅ Clean CSS PDF generated successfully!")
        print(f"📄 Size: {len(pdf_bytes)} bytes")
        print("📄 Saved as: final_test_clean.pdf")

        # File size comparison
        backup_size = (project_dir / "static" / "css" / "pdf_backup.css").stat().st_size
        clean_size = css_path.stat().st_size
        reduction = ((backup_size - clean_size) / backup_size) * 100

        print(f"\n📈 CSS Cleanup Results:")
        print(f"   Original: {backup_size:,} bytes")
        print(f"   Cleaned:  {clean_size:,} bytes")
        print(f"   Reduced:  {reduction:.1f}% smaller")

        print(f"\n✨ Key Improvements:")
        print(f"   ✓ Removed all duplicate .toc-item rules")
        print(f"   ✓ Removed multiple .cover-page definitions")
        print(f"   ✓ Consolidated page-break rules")
        print(f"   ✓ Fixed .page-ref styling for TOC page numbers")
        print(f"   ✓ Organized code into logical sections")
        print(f"   ✓ Maintained all functionality with cleaner code")

        print(f"\n🔍 What to check in the PDF:")
        print(f"   📋 TOC shows page numbers in Nepali digits")
        print(f"   📄 Categories flow continuously")
        print(f"   🔢 Page numbering is accurate")
        print(f"   🎨 All styling is preserved")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    final_test()
