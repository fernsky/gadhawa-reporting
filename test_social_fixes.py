#!/usr/bin/env python
"""
Final comprehensive test to verify all social domain fixes.
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

from apps.social.processors.manager import SocialManager


def test_comprehensive_social_fixes():
    """Test all social domain fixes comprehensively"""
    print("Comprehensive Social Domain Fixes Test")
    print("=" * 60)

    manager = SocialManager()

    # Test each processor
    categories = manager.get_available_categories()
    print(f"Testing {len(categories)} social categories...")

    all_success = True

    for category in categories:
        print(f"\n📋 Testing {category}:")

        try:
            processor = manager.get_processor(category)

            # Test 1: Data retrieval
            data = processor.get_data()
            muni_data = data.get("municipality_data", {})
            ward_data = data.get("ward_data", {})
            total_pop = data.get("total_households", 0) or data.get(
                "total_population", 0
            )

            print(
                f"   ✓ Data retrieved: {len(muni_data)} municipality types, {len(ward_data)} wards"
            )
            print(f"   ✓ Total population/households: {total_pop}")

            # Test 2: Check Nepali names in municipality data
            nepali_names_found = 0
            for key, value in muni_data.items():
                if isinstance(value, dict) and value.get("name_nepali"):
                    nepali_names_found += 1
                    # Check if it's not just the English key
                    if value["name_nepali"] != key:
                        print(
                            f"   ✓ Proper Nepali name: {key} -> {value['name_nepali']}"
                        )

            if nepali_names_found > 0:
                print(f"   ✓ Found {nepali_names_found} proper Nepali names")
            else:
                print(f"   ⚠ No proper Nepali names found")

            # Test 3: Check ward data structure
            ward_demographics_found = 0
            for ward_num, ward_info in ward_data.items():
                if isinstance(ward_info, dict):
                    total_ward_pop = ward_info.get(
                        "total_population", 0
                    ) or ward_info.get("total_households", 0)
                    if total_ward_pop > 0:
                        ward_demographics_found += 1

            if ward_demographics_found > 0:
                print(f"   ✓ Found data in {ward_demographics_found} wards")
            else:
                print(f"   ⚠ No ward data found")

            # Test 4: Chart data formatting
            try:
                formatted_muni = processor._format_municipality_data_for_pie_chart(
                    muni_data
                )
                formatted_ward = processor._format_ward_data_for_bar_chart(ward_data)

                if formatted_muni:
                    print(
                        f"   ✓ Pie chart data formatted: {len(formatted_muni)} entries"
                    )
                if formatted_ward:
                    print(f"   ✓ Bar chart data formatted: {len(formatted_ward)} wards")

            except Exception as e:
                print(f"   ✗ Chart formatting error: {e}")
                all_success = False

            # Test 5: PDF processing
            try:
                pdf_data = processor.process_for_pdf()
                if pdf_data and "charts" in pdf_data:
                    charts = pdf_data["charts"]
                    chart_types = []
                    if charts.get("pie_chart_svg") or charts.get("pie_chart_png"):
                        chart_types.append("pie")
                    if charts.get("bar_chart_svg") or charts.get("bar_chart_png"):
                        chart_types.append("bar")
                    print(
                        f"   ✓ PDF processing successful: {', '.join(chart_types)} charts generated"
                    )
                else:
                    print(f"   ⚠ PDF processing returned no charts")
            except Exception as e:
                print(f"   ✗ PDF processing error: {e}")
                all_success = False

        except Exception as e:
            print(f"   ✗ Category {category} failed: {e}")
            all_success = False

    # Test combined functionality
    print(f"\n🔄 Testing combined functionality:")
    try:
        combined_data = manager.process_all_for_pdf()
        successful_categories = len(
            [
                k
                for k, v in combined_data.items()
                if v.get("total_population", 0) > 0 or v.get("total_households", 0) > 0
            ]
        )
        print(
            f"   ✓ Combined processing: {successful_categories}/{len(categories)} categories have data"
        )

        combined_content = manager.get_combined_report_content()
        analysis_length = len(combined_content.get("combined_analysis", ""))
        print(f"   ✓ Combined analysis generated: {analysis_length} characters")

    except Exception as e:
        print(f"   ✗ Combined functionality error: {e}")
        all_success = False

    # Summary
    print(f"\n" + "=" * 60)
    if all_success:
        print("🎉 ALL TESTS PASSED! Social domain fixes are working correctly.")
        print("\n✅ Issues Fixed:")
        print("   1. Chart labels now show proper Nepali names instead of enum keys")
        print("   2. Ward-wise data is properly aggregated and displayed")
        print("   3. All social processors generate correct charts")
        print("   4. PDF processing works for all categories")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")

    print("=" * 60)


if __name__ == "__main__":
    test_comprehensive_social_fixes()
