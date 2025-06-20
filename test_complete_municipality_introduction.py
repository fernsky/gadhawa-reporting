#!/usr/bin/env python3
"""
Test script for Complete Municipality Introduction Processor

Tests the complete municipality introduction processor that combines all sections.
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
from apps.municipality_introduction.processors.complete import (
    CompleteMunicipalityIntroductionProcessor,
)


def test_complete_processor():
    """Test the complete municipality introduction processor"""
    print("=" * 80)
    print("TESTING COMPLETE MUNICIPALITY INTRODUCTION PROCESSOR")
    print("=" * 80)

    # Initialize processor
    processor = CompleteMunicipalityIntroductionProcessor()

    # Test basic methods
    print(f"\n1. Basic Information:")
    print(f"   Section Title: {processor.get_section_title()}")
    print(f"   Template Name: {processor.get_template_name()}")
    print(f"   Has Data: {processor.has_data()}")

    # Test data summary
    print(f"\n2. Data Summary:")
    summary = processor.get_data_summary()
    print(f"   Total Sections: {summary.get('total_sections', 0)}")
    print(f"   Sections with Data: {summary.get('sections_with_data', 0)}")
    print(f"   Available Sections:")
    for section_name, section_info in summary.get("sections", {}).items():
        print(f"     • {section_name}: {section_info.get('title', 'N/A')}")
        print(f"       Records: {section_info.get('record_count', 0)}")
        print(f"       Has Data: {section_info.get('has_data', False)}")

    # Test PDF processing
    print(f"\n3. PDF Processing:")
    pdf_result = processor.process_for_pdf()
    print(f"   Success: {pdf_result.get('success', False)}")
    print(f"   Has Data: {pdf_result.get('has_data', False)}")

    if pdf_result.get("success"):
        context = pdf_result.get("context", {})
        metadata = context.get("metadata", {})
        print(f"   Sections Processed: {metadata.get('sections_processed', 0)}")
        print(f"   Sections with Data: {metadata.get('sections_with_data', 0)}")
        print(
            f"   Available Sections: {', '.join(metadata.get('available_sections', []))}"
        )

        # Check individual section data
        print(f"\n4. Individual Section Data:")
        print(
            f"   Physical Status: {'Available' if context.get('physical_status_data') else 'Not Available'}"
        )
        print(
            f"   Historical Background: {'Available' if context.get('historical_background_data') else 'Not Available'}"
        )

        # If historical background data is available, show some details
        if context.get("historical_background_data"):
            hb_data = context["historical_background_data"]
            print(f"   Historical Background Details:")
            print(f"     Municipality: {hb_data.get('municipality_name', 'N/A')}")
            if hb_data.get("summary_stats"):
                stats = hb_data["summary_stats"]
                print(f"     Festivals: {stats.get('total_festivals', 0)}")
                print(f"     Languages: {stats.get('total_languages', 0)}")
                print(f"     Forest Types: {stats.get('total_forest_types', 0)}")
    else:
        print(f"   Error: {pdf_result.get('error', 'Unknown error')}")

    # Test template rendering
    print(f"\n5. Template Rendering Test:")
    try:
        context = processor.get_context_for_pdf()
        template_name = processor.get_template_name()

        rendered_html = render_to_string(template_name, context)
        print(f"   ✅ Template rendered successfully!")
        print(f"   ✅ HTML length: {len(rendered_html)} characters")

        # Check for key elements
        key_elements = [
            "परिच्छेद – २ः गाउँपालिका/नगरपालिकाको चिनारी",
            "लुङ्ग्री गाउँपालिका",
            "२.१ भौगोलिक अवस्थिति",
            "२.२ ऐतिहासिक पृष्ठभूमि तथा नामाकरण",
        ]

        for element in key_elements:
            if element in rendered_html:
                print(f"   ✅ Found: {element}")
            else:
                print(f"   ❌ Missing: {element}")

        # Save rendered HTML for inspection
        output_file = "/Users/trilochan/Desktop/final-delivery/digital-profile/lungri/lungri-report/test_complete_municipality_introduction_output.html"
        with open(output_file, "w", encoding="utf-8") as f:
            full_html = f"""<!DOCTYPE html>
<html lang="ne">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Complete Municipality Introduction Test Output</title>
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

    # Test validation
    print(f"\n6. Validation Test:")
    try:
        validation_result = processor.validate_all_sections()
        print(f"   Overall Valid: {validation_result.get('overall_valid', False)}")

        summary = validation_result.get("summary", {})
        print(f"   Total Sections: {summary.get('total_sections', 0)}")
        print(f"   Valid Sections: {summary.get('valid_sections', 0)}")
        print(f"   Sections with Warnings: {summary.get('sections_with_warnings', 0)}")
        print(f"   Sections with Errors: {summary.get('sections_with_errors', 0)}")

        # Show section-specific validation
        for section_name, section_validation in validation_result.get(
            "sections", {}
        ).items():
            print(f"   {section_name}:")
            print(f"     Valid: {section_validation.get('is_valid', False)}")
            print(f"     Errors: {len(section_validation.get('errors', []))}")
            print(f"     Warnings: {len(section_validation.get('warnings', []))}")

    except Exception as e:
        print(f"   ❌ Validation failed: {str(e)}")

    print("\n" + "=" * 80)
    print("COMPLETE MUNICIPALITY INTRODUCTION PROCESSOR TEST COMPLETED")
    print("=" * 80)


if __name__ == "__main__":
    test_complete_processor()
