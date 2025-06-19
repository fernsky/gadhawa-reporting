#!/usr/bin/env python
"""
Test script to verify demographics chart management system
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lungri_report.settings")
django.setup()

from apps.demographics.processors.manager import DemographicsManager


def test_demographics_chart_management():
    """Test that all demographics processors support chart management"""
    print("🧪 Testing Demographics Chart Management System...")

    # Create manager
    manager = DemographicsManager()

    # Test each processor
    for category, processor in manager.processors.items():
        print(f"\n📊 Testing {category} processor...")

        # Check if processor has chart management methods
        has_chart_key = hasattr(processor, "get_chart_key")
        has_needs_generation = hasattr(processor, "needs_generation")
        has_generate_and_track = hasattr(processor, "generate_and_track_charts")
        has_mark_generated = hasattr(processor, "mark_generated")

        print(f"  ✓ get_chart_key: {has_chart_key}")
        print(f"  ✓ needs_generation: {has_needs_generation}")
        print(f"  ✓ generate_and_track_charts: {has_generate_and_track}")
        print(f"  ✓ mark_generated: {has_mark_generated}")

        if has_chart_key:
            chart_key = processor.get_chart_key()
            print(f"  📈 Chart key: {chart_key}")

        # Check if processor can get data
        try:
            data = processor.get_data()
            print(
                f"  📋 Data retrieval: ✅ (got {len(data) if isinstance(data, dict) else 'data'})"
            )
        except Exception as e:
            print(f"  📋 Data retrieval: ❌ {str(e)}")

        # Test chart generation methods
        chart_methods = ["generate_and_track_charts", "generate_and_save_charts"]
        for method in chart_methods:
            if hasattr(processor, method):
                print(f"  🎨 {method}: ✅")
                break
        else:
            print(f"  🎨 Chart generation methods: ❌")

        print(
            f"  {'✅' if all([has_chart_key, has_needs_generation, has_generate_and_track, has_mark_generated]) else '⚠️'} Chart management support: {'Complete' if all([has_chart_key, has_needs_generation, has_generate_and_track, has_mark_generated]) else 'Partial'}"
        )

    # Test manager methods
    print(f"\n🔧 Testing Manager Methods...")

    try:
        available_categories = manager.get_available_categories()
        print(f"  📋 Available categories: {available_categories}")
    except Exception as e:
        print(f"  📋 Available categories: ❌ {str(e)}")

    try:
        # Test PDF processing (without actually generating charts)
        print(f"  📄 Testing PDF processing...")
        for category in ["religion", "language"]:  # Test a couple
            result = manager.process_category_for_pdf(category)
            if result:
                keys = result.keys()
                print(f"    {category}: ✅ (keys: {list(keys)})")
            else:
                print(f"    {category}: ❌")
    except Exception as e:
        print(f"  📄 PDF processing: ❌ {str(e)}")

    print(f"\n✅ Demographics chart management test completed!")


if __name__ == "__main__":
    test_demographics_chart_management()
