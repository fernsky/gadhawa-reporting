#!/usr/bin/env python3
"""
Test script for infrastructure processors
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(
    "/Users/trilochan/Desktop/final-delivery/digital-profile/lungri/lungri-report"
)

# Configure Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lungri_report.settings.development")
django.setup()

# Now we can import Django models and processors
from apps.infrastructure.processors.manager import get_infrastructure_manager


def test_infrastructure_processors():
    print("Testing Infrastructure Processors...")

    # Get the infrastructure manager
    manager = get_infrastructure_manager()

    # Test each processor
    categories = manager.get_available_categories()
    print(f"Available categories: {categories}")

    # Test each category
    for category in categories:
        print(f"\n--- Testing {category} ---")
        processor = manager.get_processor(category)

        # Test data retrieval
        try:
            data = processor.get_data()
            print(f"Data keys: {list(data.keys())}")
            print(f"Total households: {data.get('total_households', 0)}")

            # Test analysis generation
            analysis = processor.generate_analysis_text(data)
            print(f"Analysis length: {len(analysis)} characters")
            print(f"Analysis preview: {analysis[:200]}...")

            # Test PDF processing
            pdf_data = processor.process_for_pdf()
            print(f"PDF data keys: {list(pdf_data.keys())}")

        except Exception as e:
            print(f"Error testing {category}: {str(e)}")

    # Test full processing
    print("\n--- Testing Full Processing ---")
    try:
        all_data = manager.process_all_for_pdf()
        print(f"Full processing completed. Categories: {list(all_data.keys())}")

        for category, data in all_data.items():
            print(f"{category}: {data.get('total_households', 0)} households")

    except Exception as e:
        print(f"Error in full processing: {str(e)}")


if __name__ == "__main__":
    test_infrastructure_processors()
