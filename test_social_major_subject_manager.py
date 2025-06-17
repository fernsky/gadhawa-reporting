#!/usr/bin/env python
"""
Test Social Manager with Major Subject Processor
"""
import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lungri_report.settings.development")
django.setup()

from apps.social.processors.manager import SocialManager


def test_social_manager():
    """Test the Social Manager with major subject processor"""
    print("Testing Social Manager...")

    manager = SocialManager()

    # Test processor availability
    print("\n1. Testing available processors...")
    print(f"Available processors: {list(manager.processors.keys())}")

    # Test major subject processor
    print("\n2. Testing major subject processor...")
    major_subject_processor = manager.get_processor("major_subject")
    if major_subject_processor:
        print("✓ Major subject processor found")

        # Test data retrieval
        data = major_subject_processor.get_data()
        print(f"Total population: {data['total_population']}")
        print(f"Number of subjects: {len(data['municipality_data'])}")
        print(f"Number of wards: {len(data['ward_data'])}")
    else:
        print("✗ Major subject processor not found")

    # Test processing all categories
    print("\n3. Testing process all categories...")
    try:
        results = manager.process_all_for_pdf()
        print(f"Processed categories: {list(results.keys())}")
        if "major_subject" in results:
            print("✓ Major subject included in results")
        else:
            print("✗ Major subject not included in results")
    except Exception as e:
        print(f"✗ Error processing categories: {e}")

    print("\n✅ Social Manager test completed!")


if __name__ == "__main__":
    test_social_manager()
