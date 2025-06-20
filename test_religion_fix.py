#!/usr/bin/env python3
"""
Test Religion Processor Chart Generation

Quick test to verify the religion processor generates charts correctly.
"""

import os
import sys
import django

# Setup Django
sys.path.append(
    "/Users/trilochan/Desktop/final-delivery/digital-profile/lungri/lungri-report"
)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lungri_report.settings")
django.setup()

from apps.demographics.processors.religion import ReligionProcessor


def test_religion_processor():
    """Test religion processor chart generation"""
    print("🧪 Testing Religion Processor...")

    # Initialize processor
    processor = ReligionProcessor()
    print("✓ ReligionProcessor initialized successfully")

    # Get data
    print("\n📊 Testing data retrieval...")
    data = processor.get_data()

    # Print sample data
    print(f"📊 Found {len(data)} religion categories")
    for religion, info in list(data.items())[:3]:  # Show first 3
        if isinstance(info, dict) and "population" in info:
            print(
                f"   - {info.get('name_nepali', religion)}: {info['population']} ({info.get('percentage', 0):.1f}%)"
            )

    # Test chart generation
    print("🎨 Testing chart generation...")
    try:
        charts = processor.generate_and_save_charts(data)
        print(f"✅ Chart generation completed!")

        for chart_type, url in charts.items():
            print(f"   - {chart_type}: {url}")

        # Test PDF processing
        print("\n📄 Testing PDF processing...")
        pdf_data = processor.process_for_pdf()
        print(f"✅ PDF processing completed!")
        print(f"   - Section: {pdf_data.get('section_title')}")
        print(f"   - Total population: {pdf_data.get('total_population', 0)}")
        print(f"   - Charts generated: {len(pdf_data.get('charts', {}))}")

    except Exception as e:
        print(f"❌ Error during chart generation: {e}")
        import traceback

        traceback.print_exc()
        return False

    print("✅ Religion processor test completed successfully!")
    return True


if __name__ == "__main__":
    success = test_religion_processor()
    sys.exit(0 if success else 1)
