#!/usr/bin/env python
"""
Quick test script for literacy status processor
"""
import os
import sys
import django

# Add the project root to Python path
sys.path.append(
    "/Users/trilochan/Desktop/final-delivery/digital-profile/lungri/lungri-report"
)

# Configure Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lungri_report.settings.development")
django.setup()

# Now we can import Django models and processors
from apps.social.processors.literacy_status import LiteracyStatusProcessor


def test_literacy_processor():
    print("=" * 50)
    print("TESTING LITERACY STATUS PROCESSOR")
    print("=" * 50)

    try:
        processor = LiteracyStatusProcessor()

        # Test data retrieval
        print("1. Testing data retrieval...")
        data = processor.get_data()
        print(f"   Total population: {data['total_population']}")
        print(f"   Municipality data keys: {list(data['municipality_data'].keys())}")
        print(f"   Number of wards: {len(data['ward_data'])}")

        # Test chart generation
        print("\n2. Testing chart generation...")
        charts = processor.generate_and_save_charts(data)
        print(f"   Charts generated: {list(charts.keys())}")
        for chart_name, path in charts.items():
            print(f"   - {chart_name}: {path}")

        # Test analysis generation
        print("\n3. Testing analysis generation...")
        analysis = processor.generate_analysis(data)
        print(f"   Analysis length: {len(analysis)} characters")
        print(f"   Analysis preview: {analysis[:200]}...")

        # Test full PDF processing
        print("\n4. Testing full PDF processing...")
        pdf_data = processor.process_for_pdf()
        print(f"   PDF data keys: {list(pdf_data.keys())}")

        print("\n✅ All tests passed! Literacy status processor is working correctly.")
        return True

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_literacy_processor()
