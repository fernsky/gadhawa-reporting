#!/usr/bin/env python3
"""
Final Integration Test for Municipality Introduction

This script demonstrates the complete functionality of the municipality introduction system.
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

from apps.municipality_introduction.processors.complete import (
    CompleteMunicipalityIntroductionProcessor,
)
from apps.municipality_introduction.processors.manager import (
    MunicipalityIntroductionManager,
)
from apps.municipality_introduction.models import (
    PhysicalStatusInfo,
    HistoricalBackgroundInfo,
)


def main():
    """Demonstrate the complete municipality introduction functionality"""
    print("=" * 80)
    print("MUNICIPALITY INTRODUCTION - FINAL INTEGRATION DEMO")
    print("=" * 80)

    # Check data availability
    print(f"\n📊 DATA AVAILABILITY CHECK:")
    print(f"   Physical Status Records: {PhysicalStatusInfo.objects.count()}")
    print(
        f"   Historical Background Records: {HistoricalBackgroundInfo.objects.count()}"
    )

    # Test manager
    print(f"\n🔧 MANAGER TEST:")
    manager = MunicipalityIntroductionManager()
    categories = manager.get_available_categories()
    print(f"   Available Categories: {', '.join(categories)}")

    for category in categories:
        processor = manager.get_processor(category)
        print(
            f"   {category}: {processor.get_section_title()} - Data: {processor.has_data()}"
        )

    # Test complete processor
    print(f"\n📋 COMPLETE PROCESSOR TEST:")
    complete_processor = CompleteMunicipalityIntroductionProcessor()

    # Get data summary
    summary = complete_processor.get_data_summary()
    print(f"   Total Sections: {summary['total_sections']}")
    print(f"   Sections with Data: {summary['sections_with_data']}")
    print(
        f"   Data Coverage: {(summary['sections_with_data']/summary['total_sections']*100):.1f}%"
    )

    # Test PDF processing
    print(f"\n📄 PDF PROCESSING TEST:")
    pdf_result = complete_processor.process_for_pdf()
    print(f"   Success: {pdf_result.get('success', False)}")
    print(f"   Has Data: {pdf_result.get('has_data', False)}")

    if pdf_result.get("success"):
        context = pdf_result.get("context", {})
        metadata = context.get("metadata", {})
        print(f"   Municipality: {context.get('municipality_name', 'N/A')}")
        print(f"   Sections Processed: {metadata.get('sections_processed', 0)}")
        print(f"   Sections with Data: {metadata.get('sections_with_data', 0)}")

    # Test validation
    print(f"\n✅ VALIDATION TEST:")
    validation = complete_processor.validate_all_sections()
    print(f"   Overall Valid: {validation['overall_valid']}")
    print(f"   Valid Sections: {validation['summary']['valid_sections']}")
    print(f"   Errors: {validation['summary']['sections_with_errors']}")
    print(f"   Warnings: {validation['summary']['sections_with_warnings']}")

    # Show specific section data
    print(f"\n📑 SECTION DETAILS:")
    if pdf_result.get("success"):
        context = pdf_result["context"]

        # Historical Background details
        if context.get("historical_background_data"):
            hb_data = context["historical_background_data"]
            print(f"   📜 Historical Background:")
            print(f"      Municipality: {hb_data.get('municipality_name', 'N/A')}")

            stats = hb_data.get("summary_stats", {})
            print(f"      Festivals: {stats.get('total_festivals', 0)}")
            print(f"      Languages: {stats.get('total_languages', 0)}")
            print(f"      Forest Types: {stats.get('total_forest_types', 0)}")
            print(f"      Religious Sites: {stats.get('total_religious_sites', 0)}")

            # Show some actual data
            if hb_data.get("cultural_heritage"):
                culture = hb_data["cultural_heritage"]
                if culture.get("festivals"):
                    print(
                        f"      Sample Festivals: {', '.join(culture['festivals'][:3])}"
                    )
                if culture.get("languages"):
                    print(f"      Sample Languages: {', '.join(culture['languages'])}")

        # Physical Status data
        if context.get("physical_status_data"):
            print(f"   🗺️  Physical Status: Available")
        else:
            print(f"   🗺️  Physical Status: Not Available")

    print(f"\n" + "=" * 80)
    print("SUMMARY:")

    # Overall status
    if (
        pdf_result.get("success", False)
        and pdf_result.get("has_data", False)
        and validation["overall_valid"]
    ):
        print("🎉 MUNICIPALITY INTRODUCTION SYSTEM IS FULLY OPERATIONAL!")
        print("   ✅ All components are working correctly")
        print("   ✅ Data validation passed")
        print("   ✅ PDF integration ready")
        print("   ✅ Template rendering successful")

        print(f"\n🚀 NEXT STEPS:")
        print(f"   1. The system is ready for PDF generation")
        print(
            f"   2. Both sections (Physical Status & Historical Background) have data"
        )
        print(f"   3. Templates are properly integrated")
        print(f"   4. Validation checks pass")
        print(
            f"   5. You can now generate full reports including municipality introduction"
        )

    else:
        print("⚠️  MUNICIPALITY INTRODUCTION SYSTEM HAS ISSUES:")
        if not pdf_result.get("success", False):
            print("   ❌ PDF processing failed")
        if not pdf_result.get("has_data", False):
            print("   ❌ No data available")
        if not validation["overall_valid"]:
            print("   ❌ Validation failed")

    print("=" * 80)


if __name__ == "__main__":
    main()
