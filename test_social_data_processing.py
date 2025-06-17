#!/usr/bin/env python
"""
Test Social Data Processing for Major Subject
"""
import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lungri_report.settings.development")
django.setup()

from apps.social.processors.manager import get_social_manager


def test_social_data_processing():
    """Test social data processing including major subject"""
    print("Testing Social Data Processing...")

    try:
        # Get social manager
        social_manager = get_social_manager()

        print("Processing all social data for PDF...")
        all_social_data = social_manager.process_all_for_pdf()

        print(f"Processed categories: {list(all_social_data.keys())}")

        if "major_subject" in all_social_data:
            print("\n✓ Major Subject data found!")
            major_subject_data = all_social_data["major_subject"]
            print(f"Data keys: {list(major_subject_data.keys())}")

            if "data" in major_subject_data:
                data = major_subject_data["data"]
                print(f"Total population: {data.get('total_population', 'N/A')}")
                print(
                    f"Municipality subjects: {len(data.get('municipality_data', {}))}"
                )
                print(f"Ward data: {len(data.get('ward_data', {}))}")

            if "coherent_analysis" in major_subject_data:
                analysis = major_subject_data["coherent_analysis"]
                print(f"Analysis length: {len(analysis)} characters")
                print(f"Analysis preview: {analysis[:100]}...")

            if "pdf_charts" in major_subject_data:
                charts = major_subject_data["pdf_charts"]
                print(f"Charts available: {list(charts.keys()) if charts else 'None'}")
        else:
            print("✗ Major Subject data not found")

        print("\n✅ Social data processing test completed!")

    except Exception as e:
        print(f"✗ Error processing social data: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_social_data_processing()
