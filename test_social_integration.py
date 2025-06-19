#!/usr/bin/env python
"""
Test script to verify the social domain integration works correctly.
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


def test_social_integration():
    """Test social integration and data processing"""
    print("Testing Social Domain Integration...")
    print("=" * 50)

    # Initialize social manager
    manager = SocialManager()

    # Test 1: Check available categories
    print("1. Available Categories:")
    categories = manager.get_available_categories()
    for category in categories:
        print(f"   - {category}")
    print()

    # Test 2: Test individual processor initialization
    print("2. Testing Individual Processors:")
    for category in categories:
        processor = manager.get_processor(category)
        if processor:
            print(f"   ✓ {category}: {processor.__class__.__name__}")
            try:
                section_title = processor.get_section_title()
                section_number = processor.get_section_number()
                print(f"     Title: {section_title}")
                print(f"     Number: {section_number}")
            except Exception as e:
                print(f"     ✗ Error getting section info: {e}")
        else:
            print(f"   ✗ {category}: Not found")
    print()

    # Test 3: Test data processing (without full chart generation)
    print("3. Testing Data Processing:")
    for category in categories:
        processor = manager.get_processor(category)
        if processor:
            try:
                # Test get_data method
                data = processor.get_data()
                print(f"   ✓ {category}: Data retrieved successfully")
                print(
                    f"     Municipality data keys: {list(data.get('municipality_data', {}).keys())}"
                )
                print(f"     Ward data available: {bool(data.get('ward_data'))}")
                print(
                    f"     Total count: {data.get('total_households', 0) or data.get('total_population', 0)}"
                )
            except Exception as e:
                print(f"   ✗ {category}: Error processing data - {e}")
        print()

    # Test 4: Test combined report content
    print("4. Testing Combined Report Content:")
    try:
        combined_content = manager.get_combined_report_content()
        print(f"   ✓ Combined content generated successfully")
        print(
            f"   Categories with data: {len(combined_content.get('all_social_data', {}))}"
        )
        print(
            f"   Available categories: {len(combined_content.get('available_categories', []))}"
        )
        print(
            f"   Combined analysis length: {len(combined_content.get('combined_analysis', ''))}"
        )
    except Exception as e:
        print(f"   ✗ Error generating combined content: {e}")
    print()

    print("=" * 50)
    print("Social Domain Integration Test Complete!")


if __name__ == "__main__":
    test_social_integration()
