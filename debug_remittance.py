#!/usr/bin/env python3
"""
Debug script for remittance expenses data
"""
import os
import sys
import django

# Add the project directory to the Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_dir)

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lungri_report.settings.development")
django.setup()

from apps.economics.processors.remittance_expenses import RemittanceExpensesProcessor


def debug_remittance_expenses():
    print("=== Debugging Remittance Expenses Data ===")

    processor = RemittanceExpensesProcessor()

    # Get raw data
    print("\n1. Getting raw data...")
    data = processor.get_data()

    print(f"Municipality data keys: {list(data['municipality_data'].keys())}")
    print(f"Ward data keys: {list(data['ward_data'].keys())}")
    print(f"Total households: {data['total_households']}")

    # Check municipality data
    print("\n2. Municipality data details:")
    for expense_type, expense_data in data["municipality_data"].items():
        print(f"  {expense_type}: {expense_data}")

    # Check ward data
    print("\n3. Ward data details:")
    for ward_num, ward_data in data["ward_data"].items():
        print(f"  Ward {ward_num}: {ward_data}")

    # Process for PDF
    print("\n4. Processing for PDF...")
    pdf_data = processor.process_for_pdf()

    print(f"PDF data keys: {list(pdf_data.keys())}")
    print(f"Municipality data in PDF: {len(pdf_data.get('municipality_data', {}))}")
    print(f"Ward data in PDF: {len(pdf_data.get('ward_data', {}))}")

    # Check if data structure matches expected template format
    print("\n5. Data structure validation:")
    for expense_type, expense_data in pdf_data.get("municipality_data", {}).items():
        print(
            f"  {expense_type}: households={expense_data.get('households')}, name_nepali={expense_data.get('name_nepali')}"
        )

    print("\n=== Debug Complete ===")


if __name__ == "__main__":
    debug_remittance_expenses()
