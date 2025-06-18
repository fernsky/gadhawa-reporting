#!/usr/bin/env python3
"""
Debug script to check remittance expenses data structure
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lungri_report.settings.development")
django.setup()

from apps.economics.processors.remittance_expenses import RemittanceExpensesProcessor


def debug_remittance_data():
    """Debug remittance expenses data"""
    print("=== Debugging Remittance Expenses Data ===")

    processor = RemittanceExpensesProcessor()

    # Get raw data
    data = processor.get_data()
    print(f"\nData keys: {data.keys()}")

    # Check municipality data
    print(f"\nMunicipality data keys: {list(data['municipality_data'].keys())}")
    for key, value in list(data["municipality_data"].items())[:3]:  # First 3 items
        print(f"  {key}: {value}")

    # Check ward data
    print(f"\nWard data keys: {list(data['ward_data'].keys())}")
    if data["ward_data"]:
        first_ward = list(data["ward_data"].keys())[0]
        ward_info = data["ward_data"][first_ward]
        print(f"First ward ({first_ward}) structure:")
        print(f"  Keys: {ward_info.keys()}")
        if "expense_types" in ward_info:
            print(f"  Expense types keys: {list(ward_info['expense_types'].keys())}")
            first_expense = list(ward_info["expense_types"].keys())[0]
            print(
                f"  First expense ({first_expense}): {ward_info['expense_types'][first_expense]}"
            )

    print(f"\nTotal households: {data.get('total_households', 'Not found')}")

    # Process for PDF
    pdf_data = processor.process_for_pdf()
    print(f"\nPDF data keys: {pdf_data.keys()}")
    print(
        f"Total population in PDF data: {pdf_data.get('total_population', 'Not found')}"
    )


if __name__ == "__main__":
    debug_remittance_data()
