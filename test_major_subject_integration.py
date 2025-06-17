#!/usr/bin/env python
"""
Comprehensive test for Major Subject functionality
"""
import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lungri_report.settings.development")
django.setup()

from apps.social.processors.manager import get_social_manager


def test_major_subject_integration():
    """Test complete major subject integration"""
    print("🔍 Testing Major Subject Complete Integration...")

    try:
        # Test social manager
        print("\n1. Testing Social Manager Integration...")
        social_manager = get_social_manager()
        processors = list(social_manager.processors.keys())
        print(f"Available processors: {processors}")

        if "major_subject" in processors:
            print("✅ Major subject processor registered")
        else:
            print("❌ Major subject processor NOT registered")
            return False

        # Test data processing for PDF
        print("\n2. Testing PDF Data Processing...")
        all_social_data = social_manager.process_all_for_pdf()

        if "major_subject" in all_social_data:
            major_subject_data = all_social_data["major_subject"]
            print("✅ Major subject data processed for PDF")

            # Verify data structure
            required_keys = [
                "municipality_data",
                "ward_data",
                "total_population",
                "coherent_analysis",
                "pdf_charts",
                "section_title",
                "section_number",
            ]

            missing_keys = []
            for key in required_keys:
                if key not in major_subject_data:
                    missing_keys.append(key)

            if missing_keys:
                print(f"❌ Missing keys in major subject data: {missing_keys}")
                return False
            else:
                print("✅ All required data keys present")

            # Verify actual data content
            if major_subject_data["total_population"] > 0:
                print(
                    f"✅ Population data: {major_subject_data['total_population']} students"
                )
            else:
                print("❌ No population data")
                return False

            if major_subject_data["municipality_data"]:
                print(
                    f"✅ Municipality data: {len(major_subject_data['municipality_data'])} subjects"
                )
            else:
                print("❌ No municipality data")
                return False

            if major_subject_data["ward_data"]:
                print(f"✅ Ward data: {len(major_subject_data['ward_data'])} wards")
            else:
                print("❌ No ward data")
                return False

            if major_subject_data["coherent_analysis"]:
                print(
                    f"✅ Analysis: {len(major_subject_data['coherent_analysis'])} characters"
                )
            else:
                print("❌ No analysis generated")
                return False

            if (
                major_subject_data["pdf_charts"]
                and "major_subject" in major_subject_data["pdf_charts"]
            ):
                charts = major_subject_data["pdf_charts"]["major_subject"]
                print(f"✅ Charts: {list(charts.keys())}")
            else:
                print("❌ No charts generated")
                return False
        else:
            print("❌ Major subject data NOT found in PDF processing")
            return False

        # Test chart generation specifically
        print("\n3. Testing Chart Generation...")
        major_subject_processor = social_manager.get_processor("major_subject")
        data = major_subject_processor.get_data()
        charts = major_subject_processor.generate_and_save_charts(data)

        expected_charts = [
            "pie_chart_png",
            "pie_chart_svg",
            "bar_chart_png",
            "bar_chart_svg",
        ]
        missing_charts = []
        for chart in expected_charts:
            if chart not in charts:
                missing_charts.append(chart)

        if missing_charts:
            print(f"❌ Missing charts: {missing_charts}")
            return False
        else:
            print("✅ All charts generated successfully")

        # Test field categorization
        print("\n4. Testing Field Categorization...")
        if "field_categories" in data:
            categories = data["field_categories"]
            print(f"✅ Field categories: {list(categories.keys())}")

            # Check if categories have data
            total_categorized = sum(cat["population"] for cat in categories.values())
            if total_categorized > 0:
                print(f"✅ Categorized population: {total_categorized}")
            else:
                print("❌ No population in categories")
                return False
        else:
            print("❌ Field categories not found")
            return False

        # Summary
        print(f"\n🎉 SUCCESS: Major Subject integration test passed!")
        print(f"📊 Total students: {major_subject_data['total_population']:,}")
        print(f"📚 Total subjects: {len(major_subject_data['municipality_data'])}")
        print(f"🏘️ Total wards: {len(major_subject_data['ward_data'])}")
        print(f"📈 Charts generated: {len(charts)}")
        print(f"🏷️ Categories: {len(categories)}")

        return True

    except Exception as e:
        print(f"❌ Error in integration test: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_major_subject_integration()
    if success:
        print("\n✅ All tests passed! Major Subject functionality is ready.")
    else:
        print("\n❌ Some tests failed! Please check the implementation.")
