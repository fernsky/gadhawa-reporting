#!/usr/bin/env python3
"""
Test script to check remittance expenses data structure
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lungri_report.settings.development")
sys.path.append(
    "/Users/trilochan/Desktop/final-delivery/digital-profile/lungri/lungri-report"
)
django.setup()


def test_remittance_data():
    """Test remittance expenses data"""
    from apps.economics.processors.remittance_expenses import (
        RemittanceExpensesProcessor,
    )

    print("=== Testing Remittance Expenses Data ===")

    processor = RemittanceExpensesProcessor()

    # Get raw data
    data = processor.get_data()
    print(f"Data keys: {list(data.keys())}")
    print(f"Total households: {data.get('total_households', 'Not found')}")

    # Check municipality data
    print(f"\nMunicipality data has {len(data['municipality_data'])} expense types")
    municipality_total = sum(
        item["households"] for item in data["municipality_data"].values()
    )
    print(f"Municipality total households: {municipality_total}")

    # Check ward data
    print(f"\nWard data has {len(data['ward_data'])} wards")
    for ward_num, ward_info in data["ward_data"].items():
        ward_total = ward_info.get("total_households", 0)
        print(f"Ward {ward_num}: {ward_total} households")

        # Check if expense_types exist
        if "expense_types" in ward_info:
            expense_total = sum(
                exp["households"] for exp in ward_info["expense_types"].values()
            )
            print(f"  Expense types total: {expense_total}")
        else:
            print(f"  No expense_types found")

    # Process for PDF
    pdf_data = processor.process_for_pdf()
    print(f"\nPDF data keys: {list(pdf_data.keys())}")
    print(f"PDF total_population: {pdf_data.get('total_population', 'Not found')}")
    print(f"PDF total_households: {pdf_data.get('total_households', 'Not found')}")


if __name__ == "__main__":
    test_remittance_data()
