#!/usr/bin/env python
"""
Test ward settlement data structure for debugging
"""

import os
import sys
import django

# Add the project directory to the path
sys.path.append(
    "/Users/trilochan/Desktop/final-delivery/digital-profile/gadhawa/gadhawa-report"
)

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gadhawa_report.settings.development")
django.setup()

from apps.demographics.processors.ward_settlement import WardSettlementProcessor


def test_ward_settlement_data():
    """Test ward settlement data structure"""
    processor = WardSettlementProcessor()

    print("=== Testing Ward Settlement Data ===")

    # Test get_data method
    print("\n1. Testing get_data():")
    data = processor.get_data()
    print(f"Data keys: {list(data.keys())}")
    print(f"Total settlements: {data.get('total_settlements', 0)}")
    print(f"Total wards: {data.get('total_wards', 0)}")

    if "ward_data" in data:
        print(f"Ward data type: {type(data['ward_data'])}")
        print(f"Ward data keys: {list(data['ward_data'].keys())}")

        # Show first ward data
        for ward_num, ward_info in list(data["ward_data"].items())[:2]:
            print(f"Ward {ward_num}: {ward_info}")

    # Test process_for_pdf method
    print("\n2. Testing process_for_pdf():")
    pdf_data = processor.process_for_pdf()
    print(f"PDF data keys: {list(pdf_data.keys())}")

    if "report_content" in pdf_data:
        print(f"Report content type: {type(pdf_data['report_content'])}")
        print(f"Report content keys: {list(pdf_data['report_content'].keys())}")

        if "coherent_analysis" in pdf_data["report_content"]:
            analysis = pdf_data["report_content"]["coherent_analysis"]
            print(f"Coherent analysis length: {len(analysis)}")
            print(f"First 200 chars: {analysis[:200]}...")


if __name__ == "__main__":
    test_ward_settlement_data()
