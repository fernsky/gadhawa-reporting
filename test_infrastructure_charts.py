#!/usr/bin/env python3
"""
Test Infrastructure Chart Generation

This script tests if infrastructure charts are being properly generated and saved.
"""

import os
import sys
import django
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lungri_report.settings.development")
django.setup()

from apps.infrastructure.processors.manager import get_infrastructure_manager


def test_infrastructure_charts():
    """Test infrastructure chart generation"""
    print("Testing Infrastructure Chart Generation...")
    print("=" * 50)

    # Get the infrastructure manager
    manager = get_infrastructure_manager()

    # Test each processor
    for category in manager.get_available_categories():
        print(f"\nTesting {category}...")

        try:
            # Process for PDF (this should generate and save charts)
            result = manager.process_category_for_pdf(category)

            if result:
                print(f"✓ {category} processor executed successfully")
                print(f"  - Total households: {result.get('total_households', 0)}")
                print(
                    f"  - Has analysis: {'Yes' if result.get('coherent_analysis') else 'No'}"
                )

                # Check for generated charts
                pdf_charts = result.get("pdf_charts", {})
                if pdf_charts:
                    category_charts = pdf_charts.get(
                        result.get("section_number", "").lower().replace(".", "_"), {}
                    )
                    if category_charts:
                        print(f"  - Charts generated:")
                        for chart_type, chart_path in category_charts.items():
                            if chart_path:
                                print(f"    * {chart_type}: {chart_path}")
                                # Check if file actually exists
                                full_path = Path("static") / chart_path.replace(
                                    "images/", ""
                                )
                                if full_path.exists():
                                    print(f"      ✓ File exists: {full_path}")
                                else:
                                    print(f"      ✗ File missing: {full_path}")
                    else:
                        print(f"  - No charts found in category")
                else:
                    print(f"  - No pdf_charts in result")
            else:
                print(f"✗ {category} processor returned no result")

        except Exception as e:
            print(f"✗ {category} processor failed: {str(e)}")
            import traceback

            traceback.print_exc()

    print("\n" + "=" * 50)
    print("Test completed!")

    # Check static directory structure
    print("\nChecking static directory structure...")
    static_dir = Path("static")
    if static_dir.exists():
        print(f"✓ Static directory exists: {static_dir}")

        images_dir = static_dir / "images" / "charts"
        if images_dir.exists():
            print(f"✓ Images directory exists: {images_dir}")

            charts_dir = images_dir / "charts"
            if charts_dir.exists():
                print(f"✓ Charts directory exists: {charts_dir}")

                # List all chart files
                chart_files = list(charts_dir.glob("*"))
                if chart_files:
                    print(f"✓ Found {len(chart_files)} chart files:")
                    for file in sorted(chart_files):
                        print(f"  - {file.name}")
                else:
                    print("✗ No chart files found")
            else:
                print(f"✗ Charts directory missing: {charts_dir}")
        else:
            print(f"✗ Images directory missing: {images_dir}")
    else:
        print(f"✗ Static directory missing: {static_dir}")


if __name__ == "__main__":
    test_infrastructure_charts()
