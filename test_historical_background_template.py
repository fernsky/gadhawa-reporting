#!/usr/bin/env python3
"""
Test script for Historical Background Template

Tests the template rendering for the २.२ ऐतिहासिक पृष्ठभूमि तथा नामाकरण section.
"""

import os
import sys
import django

# Add the project root directory to Python path
sys.path.append(
    "/Users/trilochan/Desktop/final-delivery/digital-profile/lungri/lungri-report"
)

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lungri_report.settings.base")
django.setup()

from django.template.loader import render_to_string
from apps.municipality_introduction.processors.historical_background import (
    HistoricalBackgroundProcessor,
)


def test_template():
    """Test the historical background template rendering"""
    print("=" * 80)
    print("TESTING HISTORICAL BACKGROUND TEMPLATE")
    print("=" * 80)

    # Initialize processor
    processor = HistoricalBackgroundProcessor()

    # Get context for template
    context = processor.get_context_for_template()
    template_name = processor.get_template_name()

    print(f"\n1. Template Name: {template_name}")
    print(f"2. Context Keys: {list(context.keys())}")

    # Test basic context values
    print(f"\n3. Basic Context Values:")
    print(f"   Section Title: {context.get('section_title', 'N/A')}")
    print(f"   Municipality: {context.get('municipality_name', 'N/A')}")

    # Test nested context values
    print(f"\n4. Historical Narrative:")
    historical = context.get("historical_narrative", {})
    print(f"   Has Narrative: {'narrative' in historical}")
    print(f"   Has Naming Story: {'naming_story' in historical}")
    print(f"   Formation Date: {historical.get('formation_date', 'N/A')}")
    print(f"   Merged VDCs Count: {len(historical.get('merged_vdcs', []))}")

    print(f"\n5. Geographic Features:")
    geo = context.get("geographic_features", {})
    print(f"   Main River: {geo.get('main_river', 'N/A')}")
    print(f"   Forest Types Count: {len(geo.get('forest_types', []))}")
    print(f"   Has Wildlife Info: {'wildlife' in geo}")

    print(f"\n6. Cultural Heritage:")
    culture = context.get("cultural_heritage", {})
    print(f"   Festivals Count: {len(culture.get('festivals', []))}")
    print(f"   Languages Count: {len(culture.get('languages', []))}")
    print(f"   Has Costume Info: {'traditional_costume' in culture}")

    print(f"\n7. Religious Heritage:")
    religion = context.get("religious_heritage", {})
    print(f"   Religious Sites Count: {len(religion.get('religious_sites', []))}")
    print(f"   Has Practices Info: {'religious_practices' in religion}")

    print(f"\n8. Summary Stats:")
    stats = context.get("summary_stats", {})
    if stats:
        print(f"   Total Festivals: {stats.get('total_festivals', 0)}")
        print(f"   Total Languages: {stats.get('total_languages', 0)}")
        print(f"   Total Forest Types: {stats.get('total_forest_types', 0)}")
        print(f"   Total Religious Sites: {stats.get('total_religious_sites', 0)}")
    else:
        print("   No summary stats available")

    # Try to render the template
    print(f"\n9. Template Rendering Test:")
    try:
        rendered_html = render_to_string(template_name, context)
        print(f"   ✅ Template rendered successfully!")
        print(f"   ✅ HTML length: {len(rendered_html)} characters")

        # Check for key elements in rendered HTML
        if "२.२ ऐतिहासिक पृष्ठभूमि तथा नामाकरण" in rendered_html:
            print(f"   ✅ Section title found in rendered HTML")
        else:
            print(f"   ❌ Section title NOT found in rendered HTML")

        if context.get("municipality_name", "") in rendered_html:
            print(f"   ✅ Municipality name found in rendered HTML")
        else:
            print(f"   ❌ Municipality name NOT found in rendered HTML")

        # Save rendered HTML for inspection
        output_file = "/Users/trilochan/Desktop/final-delivery/digital-profile/lungri/lungri-report/test_historical_background_output.html"
        with open(output_file, "w", encoding="utf-8") as f:
            # Add basic HTML structure for standalone viewing
            full_html = f"""<!DOCTYPE html>
<html lang="ne">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Historical Background Test Output</title>
</head>
<body>
{rendered_html}
</body>
</html>"""
            f.write(full_html)

        print(f"   📄 Rendered HTML saved to: {output_file}")

    except Exception as e:
        print(f"   ❌ Template rendering failed: {str(e)}")
        import traceback

        traceback.print_exc()

    print("\n" + "=" * 80)
    print("HISTORICAL BACKGROUND TEMPLATE TEST COMPLETED")
    print("=" * 80)


if __name__ == "__main__":
    test_template()
