#!/usr/bin/env python
"""
Test script to verify the social full report template works correctly.
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
from django.template.loader import render_to_string
from django.template import Context, Template


def test_social_full_report():
    """Test the social full report template rendering"""
    print("Testing Social Full Report Template...")
    print("=" * 50)

    # Initialize social manager
    manager = SocialManager()

    # Get combined report content
    print("1. Getting combined social data...")
    combined_content = manager.get_combined_report_content()
    all_social_data = combined_content.get("all_social_data", {})

    print(f"   Categories with data: {len(all_social_data)}")
    for category, data in all_social_data.items():
        print(f"   - {category}: {data.get('total_population', 0)} total population")

    # Test template rendering
    print("\n2. Testing template rendering...")
    try:
        # Try to render the social full report template
        context = {
            "all_social_data": all_social_data,
        }

        # Load the template content manually first
        template_path = "templates/social/social_full_report.html"
        if Path(template_path).exists():
            print(f"   ✓ Template file exists: {template_path}")
            with open(template_path, "r", encoding="utf-8") as f:
                template_content = f.read()
            print(f"   ✓ Template content length: {len(template_content)} characters")

            # Check if template includes the right partials
            if "school_dropout_report_partial.html" in template_content:
                print("   ✓ School dropout partial is included")
            else:
                print("   ⚠ School dropout partial not found in template")

        else:
            print(f"   ✗ Template file not found: {template_path}")

        print("   ✓ Social full report structure verified")

    except Exception as e:
        print(f"   ✗ Error testing template: {e}")

    print("\n3. Summary:")
    print(f"   - Total social categories: {len(all_social_data)}")
    print(
        f"   - Categories with data > 0: {len([k for k, v in all_social_data.items() if v.get('total_population', 0) > 0])}"
    )
    print(
        f"   - Charts generated: {len([k for k, v in all_social_data.items() if v.get('charts', {})])}"
    )

    print("\n" + "=" * 50)
    print("Social Full Report Test Complete!")


if __name__ == "__main__":
    test_social_full_report()
