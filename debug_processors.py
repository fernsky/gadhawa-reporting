#!/usr/bin/env python
"""
Debug script to test the demographic processors
"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(
    "/Users/trilochan/Desktop/final-delivery/digital-profile/lungri/lungri-report"
)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lungri_report.settings.development")

# Setup Django
django.setup()

from apps.demographics.processors.caste import CasteProcessor
from apps.demographics.processors.religion import ReligionProcessor
from apps.demographics.processors.language import LanguageProcessor


def test_processors():
    print("🔍 Testing Caste Processor...")
    caste_processor = CasteProcessor()
    caste_data = caste_processor.get_data()
    print(f"Caste data structure:")
    print(f"Total population: {caste_data.get('total_population', 0)}")
    print(
        f"Municipality data keys: {list(caste_data.get('municipality_data', {}).keys())}"
    )

    # Show first few entries with population > 0
    municipality_data = caste_data.get("municipality_data", {})
    populated_castes = [
        (k, v) for k, v in municipality_data.items() if v.get("population", 0) > 0
    ]
    print(f"Populated castes count: {len(populated_castes)}")
    for i, (key, data) in enumerate(populated_castes[:3]):
        print(f"  {i+1}. {key}: {data}")

    print("\n🔍 Testing Religion Processor...")
    religion_processor = ReligionProcessor()
    religion_data = religion_processor.get_data()
    print(f"Religion data structure:")
    print(f"Total population: {religion_data.get('total_population', 0)}")
    print(
        f"Municipality data keys: {list(religion_data.get('municipality_data', {}).keys())}"
    )

    # Show first few entries with population > 0
    municipality_data = religion_data.get("municipality_data", {})
    populated_religions = [
        (k, v) for k, v in municipality_data.items() if v.get("population", 0) > 0
    ]
    print(f"Populated religions count: {len(populated_religions)}")
    for i, (key, data) in enumerate(populated_religions[:3]):
        print(f"  {i+1}. {key}: {data}")

    print("\n🔍 Testing Language Processor...")
    language_processor = LanguageProcessor()
    language_data = language_processor.get_data()
    print(f"Language data structure:")
    print(f"Total population: {language_data.get('total_population', 0)}")
    print(
        f"Municipality data keys: {list(language_data.get('municipality_data', {}).keys())}"
    )

    # Show first few entries with population > 0
    municipality_data = language_data.get("municipality_data", {})
    populated_languages = [
        (k, v) for k, v in municipality_data.items() if v.get("population", 0) > 0
    ]
    print(f"Populated languages count: {len(populated_languages)}")
    for i, (key, data) in enumerate(populated_languages[:3]):
        print(f"  {i+1}. {key}: {data}")

    print("\n🔍 Testing process_for_pdf methods...")

    # Test caste process_for_pdf
    caste_pdf_data = caste_processor.process_for_pdf()
    print(f"Caste PDF data keys: {list(caste_pdf_data.keys())}")
    if "caste_data" in caste_pdf_data:
        print(f"Caste PDF caste_data type: {type(caste_pdf_data['caste_data'])}")
        print(
            f"Caste PDF caste_data keys: {list(caste_pdf_data['caste_data'].keys())[:5] if caste_pdf_data['caste_data'] else 'None'}"
        )


if __name__ == "__main__":
    test_processors()
