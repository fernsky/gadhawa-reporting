#!/usr/bin/env python3
"""
Test script for PDF Integration

Tests that the municipality introduction section is properly integrated into the PDF report system.
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
from django.utils import timezone
from apps.municipality_introduction.processors.complete import (
    CompleteMunicipalityIntroductionProcessor,
)


def test_pdf_integration():
    """Test that municipality introduction integrates properly with PDF system"""
    print("=" * 80)
    print("TESTING PDF INTEGRATION FOR MUNICIPALITY INTRODUCTION")
    print("=" * 80)

    # Initialize municipality introduction processor
    municipality_processor = CompleteMunicipalityIntroductionProcessor()

    # Test processor functionality
    print(f"\n1. Processor Basic Tests:")
    print(f"   Section Title: {municipality_processor.get_section_title()}")
    print(f"   Template Name: {municipality_processor.get_template_name()}")
    print(f"   Has Data: {municipality_processor.has_data()}")

    # Test PDF processing
    print(f"\n2. PDF Processing Test:")
    municipality_result = municipality_processor.process_for_pdf()
    print(f"   Success: {municipality_result.get('success', False)}")
    print(f"   Has Data: {municipality_result.get('has_data', False)}")

    if municipality_result.get("success"):
        context = municipality_result.get("context", {})
        print(f"   Municipality: {context.get('municipality_name', 'N/A')}")
        print(
            f"   Physical Status Data: {'Available' if context.get('physical_status_data') else 'Not Available'}"
        )
        print(
            f"   Historical Background Data: {'Available' if context.get('historical_background_data') else 'Not Available'}"
        )

        metadata = context.get("metadata", {})
        print(f"   Sections Processed: {metadata.get('sections_processed', 0)}")
        print(f"   Sections with Data: {metadata.get('sections_with_data', 0)}")

    # Test template rendering with simulated PDF context
    print(f"\n3. Template Integration Test:")
    try:
        # Simulate the context that would be passed to the main PDF template
        pdf_context = {
            "municipality_name": "लुङ्ग्री गाउँपालिका",
            "municipality_name_english": "Lungri Rural Municipality",
            "generated_date": timezone.now(),
            "municipality_introduction_data": (
                municipality_result.get("context")
                if municipality_result.get("success")
                else None
            ),
        }

        # Test rendering just the municipality introduction section
        if pdf_context["municipality_introduction_data"]:
            intro_template = municipality_processor.get_template_name()
            intro_html = render_to_string(
                intro_template, pdf_context["municipality_introduction_data"]
            )
            print(f"   ✅ Municipality introduction template rendered successfully!")
            print(f"   ✅ HTML length: {len(intro_html)} characters")
        else:
            print(
                f"   ❌ No municipality introduction data available for template rendering"
            )

        # Test that key elements would be present in full PDF
        key_integration_elements = [
            "municipality_introduction_data" in pdf_context,
            pdf_context.get("municipality_introduction_data") is not None,
        ]

        if all(key_integration_elements):
            print(f"   ✅ All integration elements present")
        else:
            print(f"   ❌ Some integration elements missing")

    except Exception as e:
        print(f"   ❌ Template integration test failed: {str(e)}")
        import traceback

        traceback.print_exc()

    # Test data quality check
    print(f"\n4. Data Quality Check:")
    try:
        validation_result = municipality_processor.validate_all_sections()
        print(f"   Overall Valid: {validation_result.get('overall_valid', False)}")

        summary = validation_result.get("summary", {})
        print(f"   Total Sections: {summary.get('total_sections', 0)}")
        print(f"   Valid Sections: {summary.get('valid_sections', 0)}")
        print(f"   Sections with Errors: {summary.get('sections_with_errors', 0)}")
        print(f"   Sections with Warnings: {summary.get('sections_with_warnings', 0)}")

        if validation_result.get("overall_valid"):
            print(f"   ✅ All data quality checks passed")
        else:
            print(f"   ⚠️  Some data quality issues found")

    except Exception as e:
        print(f"   ❌ Data quality check failed: {str(e)}")

    # Test section coverage
    print(f"\n5. Section Coverage Analysis:")
    data_summary = municipality_processor.get_data_summary()
    print(f"   Total Sections Available: {data_summary.get('total_sections', 0)}")
    print(f"   Sections with Data: {data_summary.get('sections_with_data', 0)}")

    coverage_percentage = 0
    if data_summary.get("total_sections", 0) > 0:
        coverage_percentage = (
            data_summary.get("sections_with_data", 0)
            / data_summary.get("total_sections", 1)
        ) * 100

    print(f"   Data Coverage: {coverage_percentage:.1f}%")

    if coverage_percentage >= 80:
        print(f"   ✅ Excellent data coverage")
    elif coverage_percentage >= 50:
        print(f"   ⚠️  Good data coverage")
    else:
        print(f"   ❌ Poor data coverage")

    # Show section details
    print(f"\n6. Section Details:")
    for section_name, section_info in data_summary.get("sections", {}).items():
        print(f"   📋 {section_name}:")
        print(f"      Title: {section_info.get('title', 'N/A')}")
        print(f"      Records: {section_info.get('record_count', 0)}")
        print(f"      Has Data: {section_info.get('has_data', False)}")
        print(f"      Template: {section_info.get('template', 'N/A')}")

    print("\n" + "=" * 80)
    print("PDF INTEGRATION TEST COMPLETED")
    print("=" * 80)

    # Summary
    integration_success = (
        municipality_result.get("success", False)
        and municipality_result.get("has_data", False)
        and validation_result.get("overall_valid", False)
    )

    if integration_success:
        print(
            "🎉 INTEGRATION SUCCESS: Municipality introduction is ready for PDF generation!"
        )
    else:
        print(
            "❌ INTEGRATION ISSUES: Some problems need to be resolved before PDF generation"
        )

    return integration_success


if __name__ == "__main__":
    test_pdf_integration()
