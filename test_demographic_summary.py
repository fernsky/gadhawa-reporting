#!/usr/bin/env python
"""
Test script for demographic summary processor
"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(
    "/Users/trilochan/Desktop/final-delivery/digital-profile/lungri/lungri-report"
)

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lungri_report.settings.base")
django.setup()

from apps.demographics.processors.demographic_summary import DemographicSummaryProcessor


def test_demographic_summary_processor():
    print("Testing Demographic Summary Processor")
    print("=" * 50)

    # Initialize processor
    processor = DemographicSummaryProcessor()

    # Test basic methods
    print(f"Section Title: {processor.get_section_title()}")
    print(f"Section Number: {processor.get_section_number()}")

    # Get data
    data = processor.get_data()
    if data:
        print(f"Data found: Total Population = {data.total_population}")
        print(f"Male Population = {data.population_male}")
        print(f"Female Population = {data.population_female}")
        print(f"Sex Ratio = {data.sex_ratio}")
        print(f"Average Household Size = {data.average_household_size}")

        # Generate report content
        content = processor.generate_report_content(data)
        print(f"Generated content length: {len(content)} characters")
        print("Report generation successful!")

        # Save a sample of the content to file for review
        with open("/tmp/demographic_summary_sample.html", "w", encoding="utf-8") as f:
            f.write(content)
        print("Sample content saved to /tmp/demographic_summary_sample.html")

    else:
        print("No data found - please run the sample data creation command first")


if __name__ == "__main__":
    test_demographic_summary_processor()
