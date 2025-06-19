#!/usr/bin/env python
"""
Test Religion Report Partial Template Integration

This script tests the religion_report_partial.html template with chart management system.
"""

import os
import django
from pathlib import Path

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lungri_report.settings.development")
django.setup()

from django.template.loader import render_to_string
from django.template import Context, Template
from apps.demographics.processors.religion import ReligionProcessor


def test_religion_report_partial():
    """Test religion report partial template with chart management"""
    print("=== Testing Religion Report Partial Template ===\n")

    # Get religion processor data
    processor = ReligionProcessor()
    pdf_data = processor.process_for_pdf()

    print(f"✓ Religion processor data ready")
    print(f"  - Total population: {pdf_data['total_population']}")
    print(f"  - Charts available: {list(pdf_data['charts'].keys())}")
    print(f"  - Chart management status: {pdf_data['chart_management_status']}")

    # Prepare context data similar to what would be passed to the template
    context = {
        "religion_data": pdf_data["data"],
        "total_population": pdf_data["total_population"],
        "charts": pdf_data["charts"],
        "chart_management_status": pdf_data["chart_management_status"],
        "coherent_analysis": pdf_data["report_content"],
        "pdf_charts": {"religion": pdf_data["charts"]},
    }

    print(f"\n--- Context Data ---")
    print(f"  - religion_data keys: {list(context['religion_data'].keys())}")
    print(f"  - charts: {context['charts']}")
    print(f"  - coherent_analysis length: {len(context['coherent_analysis'])} chars")

    # Test the template rendering
    try:
        rendered_html = render_to_string(
            "demographics/religion/religion_report_partial.html", context
        )

        print(f"\n✓ Template rendered successfully!")
        print(f"  - HTML length: {len(rendered_html)} characters")

        # Check for key elements in the rendered HTML
        checks = [
            (
                "Chart management tag",
                '{% chart_url "demographics_religion_pie"' in rendered_html
                or "chart_url" in rendered_html,
            ),
            ("Chart image", "<img src=" in rendered_html),
            ("Section header", "३.५ धर्म अनुसार जनसंख्याको विवरण" in rendered_html),
            ("Data table", "religion-summary-table" in rendered_html),
            ("Chart section", "chart-section" in rendered_html),
            ("Static URL", "/static/images/charts/" in rendered_html),
        ]

        print(f"\n--- Template Content Checks ---")
        for check_name, result in checks:
            status = "✓" if result else "⚠"
            print(f"  {status} {check_name}: {'PASS' if result else 'FAIL'}")

        # Check for chart management system usage
        if "/static/images/charts/religion_pie_chart.svg" in rendered_html:
            print(f"✓ Chart management system URLs found in template")
        else:
            print(f"⚠ Chart management system URLs not found")

        # Check for template tags
        if (
            "chart_tags"
            in open(
                "/Users/trilochan/Desktop/final-delivery/digital-profile/lungri/lungri-report/templates/demographics/religion/religion_report_partial.html"
            ).read()
        ):
            print(f"✓ Chart management template tags loaded")
        else:
            print(f"⚠ Chart management template tags not loaded")

        # Save a sample of the rendered HTML for inspection
        sample_file = Path(
            "/Users/trilochan/Desktop/final-delivery/digital-profile/lungri/lungri-report/religion_template_sample.html"
        )
        with open(sample_file, "w", encoding="utf-8") as f:
            f.write(rendered_html)
        print(f"✓ Sample HTML saved to: {sample_file}")

    except Exception as e:
        print(f"⚠ Template rendering error: {e}")
        import traceback

        traceback.print_exc()

    print(f"\n=== Template Test Completed ===")


def test_context_variables():
    """Test if all required context variables are available"""
    print("\n=== Testing Context Variables ===")

    processor = ReligionProcessor()
    pdf_data = processor.process_for_pdf()

    required_vars = [
        "data",
        "charts",
        "chart_management_status",
        "total_population",
        "section_title",
        "section_number",
        "report_content",
    ]

    print("Required variables check:")
    for var in required_vars:
        if var in pdf_data:
            print(f"  ✓ {var}: {type(pdf_data[var])}")
        else:
            print(f"  ⚠ {var}: MISSING")

    # Check chart URLs specifically
    if "charts" in pdf_data:
        charts = pdf_data["charts"]
        chart_checks = [
            ("pie_chart_url", "pie_chart_url" in charts),
            ("bar_chart_url", "bar_chart_url" in charts),
            ("pie_chart_svg", "pie_chart_svg" in charts),
            ("bar_chart_svg", "bar_chart_svg" in charts),
        ]

        print("\nChart availability check:")
        for chart_name, available in chart_checks:
            status = "✓" if available else "⚠"
            value = charts.get(chart_name, "N/A") if available else "MISSING"
            print(f"  {status} {chart_name}: {value}")


if __name__ == "__main__":
    test_context_variables()
    test_religion_report_partial()
