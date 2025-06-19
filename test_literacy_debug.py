#!/usr/bin/env python
"""
Test literacy status processor specifically
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lungri_report.settings.development")
django.setup()

from apps.social.processors.literacy_status import LiteracyStatusProcessor


def test_literacy_processor():
    print("Testing literacy status processor...")

    try:
        processor = LiteracyStatusProcessor()
        data = processor.get_data()
        print(f"Data retrieved: {list(data.keys())}")
        print(f"Municipality data type: {type(data.get('municipality_data', {}))}")
        if data.get("municipality_data"):
            for key, value in data["municipality_data"].items():
                print(f"  {key}: {type(value)} = {value}")

        pdf_data = processor.process_for_pdf()
        print("PDF processing successful")

    except Exception as e:
        import traceback

        print(f"Error: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    test_literacy_processor()
