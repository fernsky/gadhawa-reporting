#!/usr/bin/env python
"""
Test Religion Report Partial View with Chart Management

This script tests the updated ReligionReportPartialView with chart management integration.
"""

import os
import django
from pathlib import Path

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lungri_report.settings.development")
django.setup()

from django.test import RequestFactory
from apps.demographics.views.religion import ReligionReportPartialView


def test_religion_report_partial_view():
    """Test the updated ReligionReportPartialView"""
    print("=== Testing Updated ReligionReportPartialView ===\n")

    # Create a request factory
    factory = RequestFactory()
    request = factory.get("/demographics/religion/report-partial/")

    # Create view instance
    view = ReligionReportPartialView()
    view.request = request

    # Get context data
    context = view.get_context_data()

    print("✓ View context generated successfully")
    print(f"  - Context keys: {list(context.keys())}")

    # Check required context variables
    required_vars = [
        "religion_data",
        "total_population",
        "coherent_analysis",
        "charts",
        "chart_management_status",
        "pdf_charts",
        "section_title",
        "section_number",
    ]

    print(f"\n--- Context Variables Check ---")
    all_present = True
    for var in required_vars:
        if var in context:
            print(f"  ✓ {var}: {type(context[var])}")
            if var == "charts":
                print(f"    Charts available: {list(context[var].keys())}")
            elif var == "chart_management_status":
                print(f"    Status: {context[var]}")
        else:
            print(f"  ⚠ {var}: MISSING")
            all_present = False

    if all_present:
        print(f"\n✓ All required context variables present")
    else:
        print(f"\n⚠ Some context variables missing")

    # Test chart URLs
    if "charts" in context:
        charts = context["charts"]
        print(f"\n--- Chart URLs ---")
        for chart_name, url in charts.items():
            print(f"  {chart_name}: {url}")

    # Test backward compatibility
    if "pdf_charts" in context and "religion" in context["pdf_charts"]:
        print(f"\n✓ Backward compatibility maintained")
        print(f"  pdf_charts.religion: {context['pdf_charts']['religion']}")

    print(f"\n=== View Test Completed ===")


if __name__ == "__main__":
    test_religion_report_partial_view()
