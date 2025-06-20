#!/usr/bin/env python3
"""
Test All Demographic Processors Chart Management

Comprehensive test to ensure all demographic processors work with the unified chart system.
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

from apps.demographics.processors.religion import ReligionProcessor
from apps.demographics.processors.language import LanguageProcessor
from apps.demographics.processors.caste import CasteProcessor
from apps.demographics.processors.occupation import OccupationProcessor
from apps.demographics.processors.economically_active import EconomicallyActiveProcessor
from apps.demographics.processors.househead import HouseheadProcessor


def test_processor(processor_class, name):
    """Test a single processor"""
    print(f"\n🧪 Testing {name} Processor...")

    try:
        # Initialize processor
        processor = processor_class()

        # Test chart key
        chart_key = processor.get_chart_key()
        print(f"📊 Chart key: {chart_key}")

        # Test required methods exist
        assert hasattr(processor, "get_data"), f"{name} missing get_data method"
        assert hasattr(
            processor, "generate_and_track_charts"
        ), f"{name} missing generate_and_track_charts method"
        assert hasattr(
            processor, "needs_generation"
        ), f"{name} missing needs_generation method"
        assert hasattr(
            processor, "mark_generated"
        ), f"{name} missing mark_generated method"
        assert hasattr(
            processor, "process_for_pdf"
        ), f"{name} missing process_for_pdf method"

        # Get data
        data = processor.get_data()
        print(f"📊 Data retrieved: {type(data).__name__}")

        # Test chart generation
        charts = processor.generate_and_track_charts(data)
        print(f"🎨 Charts generated: {len(charts)}")

        # Test PDF processing
        pdf_data = processor.process_for_pdf()
        print(f"📄 PDF data keys: {list(pdf_data.keys())}")

        print(f"✅ {name} processor test passed!")
        return True

    except Exception as e:
        print(f"❌ {name} processor test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Run all processor tests"""
    print("🔬 Testing All Demographic Processors...")

    processors = [
        (ReligionProcessor, "Religion"),
        (LanguageProcessor, "Language"),
        (CasteProcessor, "Caste"),
        (OccupationProcessor, "Occupation"),
        (EconomicallyActiveProcessor, "Economically Active"),
        (HouseheadProcessor, "Househead"),
    ]

    results = []

    for processor_class, name in processors:
        success = test_processor(processor_class, name)
        results.append((name, success))

    # Summary
    print(f"\n📊 Test Results Summary:")
    print("=" * 50)

    passed = 0
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{name:<20} {status}")
        if success:
            passed += 1

    print("=" * 50)
    print(f"Total: {passed}/{len(results)} passed")

    if passed == len(results):
        print("\n🎉 All demographic processors are working correctly!")
        print("✅ Unified chart management system is fully implemented!")
        return True
    else:
        print(f"\n⚠️  {len(results) - passed} processors need attention")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
