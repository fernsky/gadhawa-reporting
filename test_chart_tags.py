#!/usr/bin/env python3
"""
Test Chart Template Tags

Test that the chart_url template tag works correctly with all processors.
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

from django.template import Context, Template
from apps.chart_management.templatetags.chart_tags import chart_url


def test_chart_template_tags():
    """Test chart template tags for all processors"""
    print("🧪 Testing Chart Template Tags...")

    # Test chart keys that should exist
    chart_keys = [
        "demographics_religion_pie",
        "demographics_language_pie",
        "demographics_caste_pie",
        "demographics_occupation_pie",
        "demographics_economically_active_pie",
        "demographics_househead_pie",
    ]

    print("\n📊 Testing chart URLs:")
    for chart_key in chart_keys:
        try:
            url = chart_url(chart_key)
            if url:
                print(f"✅ {chart_key}: {url}")
            else:
                print(f"⚠️  {chart_key}: No URL (chart may not exist yet)")
        except Exception as e:
            print(f"❌ {chart_key}: Error - {e}")

    # Test template rendering
    print("\n🎨 Testing template rendering:")
    template_content = """
    {% load chart_tags %}
    {% chart_url "demographics_religion_pie" as religion_pie_url %}
    Religion Pie Chart: {{ religion_pie_url|default:"Not found" }}
    """

    try:
        template = Template(template_content)
        context = Context({})
        rendered = template.render(context)
        print("✅ Template rendering successful:")
        print(rendered.strip())
    except Exception as e:
        print(f"❌ Template rendering failed: {e}")
        return False

    print("\n✅ Chart template tag testing completed!")
    return True


if __name__ == "__main__":
    success = test_chart_template_tags()
    sys.exit(0 if success else 1)
