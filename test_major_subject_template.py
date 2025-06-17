#!/usr/bin/env python
"""
Test Major Subject HTML Template Rendering
"""
import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lungri_report.settings.development")
django.setup()

from django.template.loader import render_to_string
from apps.social.processors.major_subject import MajorSubjectProcessor


def test_html_template():
    """Test the major subject HTML template rendering"""
    print("Testing Major Subject HTML Template...")

    try:
        # Get processor and data
        processor = MajorSubjectProcessor()
        data = processor.get_data()
        analysis = processor.generate_analysis_text(data)
        charts = processor.generate_and_save_charts(data)

        # Prepare context for template
        context = {
            "municipality_data": data["municipality_data"],
            "ward_data": data["ward_data"],
            "total_population": data["total_population"],
            "top_subjects": data["top_subjects"],
            "field_categories": data["field_categories"],
            "coherent_analysis": analysis,
            "pdf_charts": {"major_subject": charts},
        }

        # Render template
        print("Rendering HTML template...")
        html_content = render_to_string(
            "social/major_subject/major_subject_report_partial.html", context
        )

        # Save rendered HTML for inspection
        with open("test_major_subject_output.html", "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"✓ Template rendered successfully!")
        print(f"HTML content length: {len(html_content)} characters")
        print(f"Output saved to: test_major_subject_output.html")

        # Check for key elements
        key_elements = [
            "पाँच वर्ष र सोभन्दा माथिको शैक्षिक अवस्था",
            "majorsubject_pie_chart",
            "majorsubject_bar_chart",
            "Municipality Summary",
            "Ward-wise Data",
        ]

        print("\nChecking for key template elements:")
        for element in key_elements:
            if element in html_content:
                print(f"✓ Found: {element}")
            else:
                print(f"✗ Missing: {element}")

        print("\n✅ HTML template test completed!")

    except Exception as e:
        print(f"✗ Error rendering template: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_html_template()
