#!/usr/bin/env python3
"""
Simple test script for the simplified chart management system
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lungri_report.settings")
django.setup()

from apps.demographics.processors.manager import get_demographics_manager


def test_simplified_chart_management():
    """Test the simplified chart management system"""
    print("🧪 Testing simplified chart management system...")

    # Get the demographics manager
    demographics_manager = get_demographics_manager()

    print(f"📊 Available categories: {demographics_manager.get_available_categories()}")

    # Test chart generation for specific categories
    test_categories = ["religion", "househead"]

    for category in test_categories:
        print(f"\n🔍 Testing {category} processor...")

        processor = demographics_manager.get_processor(category)
        if processor:
            # Check if processor has the new methods
            has_chart_management = hasattr(processor, "needs_generation") and hasattr(
                processor, "generate_and_track_charts"
            )
            has_legacy = hasattr(processor, "generate_and_save_charts")

            print(f"  ✓ Processor found")
            print(f"  📈 Has chart management: {has_chart_management}")
            print(f"  📊 Has legacy charts: {has_legacy}")

            if has_chart_management:
                # Test the needs_generation method
                needs_pie = processor.needs_generation("pie")
                needs_bar = processor.needs_generation("bar")
                print(f"  🎯 Needs pie generation: {needs_pie}")
                print(f"  🎯 Needs bar generation: {needs_bar}")

                # Get chart URLs if they exist
                pie_url = processor.get_chart_url("pie")
                bar_url = processor.get_chart_url("bar")
                print(f"  🔗 Pie chart URL: {pie_url}")
                print(f"  🔗 Bar chart URL: {bar_url}")
        else:
            print(f"  ❌ Processor not found")

    print(f"\n🎯 Testing full chart generation...")
    try:
        # Test the full chart generation
        chart_urls = demographics_manager.generate_all_charts()
        print(f"✅ Chart generation completed!")
        print(f"📊 Generated charts for {len(chart_urls)} categories")

        for category, charts in chart_urls.items():
            print(f"  {category}: {len(charts)} charts")

    except Exception as e:
        print(f"❌ Error during chart generation: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_simplified_chart_management()
