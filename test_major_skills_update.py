#!/usr/bin/env python
"""
Test script to verify major skills processor updates are working correctly.
"""

import os
import sys
import django

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lungri_report.settings.development")
django.setup()

from apps.economics.processors.major_skills import MajorSkillsProcessor


def test_major_skills_processor():
    """Test the major skills processor"""
    print("Testing Major Skills Processor...")

    # Initialize processor
    processor = MajorSkillsProcessor()

    # Test basic attributes
    print(f"Section Title: {processor.get_section_title()}")
    print(f"Section Number: {processor.get_section_number()}")
    print(f"Chart Key: {processor.get_chart_key()}")

    # Test chart dimensions
    print(
        f"Pie Chart Dimensions: {processor.pie_chart_width}x{processor.pie_chart_height}"
    )
    print(
        f"Bar Chart Dimensions: {processor.bar_chart_width}x{processor.bar_chart_height}"
    )

    # Test data retrieval
    try:
        data = processor.get_data()
        print(f"Data structure keys: {list(data.keys())}")
        print(f"Total population: {data.get('total_population', 0)}")

        # Test chart generation method
        charts = processor.generate_and_save_charts(data)
        print(f"Generated charts: {list(charts.keys())}")

        # Test PDF processing
        pdf_result = processor.process_for_pdf()
        print(f"PDF result keys: {list(pdf_result.keys())}")

        print("✅ Major Skills Processor test passed!")
        return True

    except Exception as e:
        print(f"❌ Major Skills Processor test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_major_skills_processor()
    sys.exit(0 if success else 1)
