#!/usr/bin/env python
"""
Quick test for Major Subject Processor
"""
import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lungri_report.settings.development")
django.setup()

from apps.social.processors.major_subject import MajorSubjectProcessor


def test_major_subject_processor():
    """Test the Major Subject processor"""
    print("Testing Major Subject Processor...")

    processor = MajorSubjectProcessor()

    # Test data retrieval
    print("\n1. Testing data retrieval...")
    data = processor.get_data()
    print(f"Municipality data keys: {list(data['municipality_data'].keys())}")
    print(f"Ward data count: {len(data['ward_data'])}")
    print(f"Total population: {data['total_population']}")

    # Test top subjects
    print("\n2. Testing top subjects...")
    top_subjects = data["top_subjects"][:5]
    for i, subject in enumerate(top_subjects, 1):
        print(
            f"{i}. {subject['subject_name']}: {subject['population']} ({subject['percentage']:.1f}%)"
        )

    # Test PDF processing
    print("\n3. Testing PDF processing...")
    pdf_data = processor.process_for_pdf()
    print(f"PDF data keys: {list(pdf_data.keys())}")

    # Test analysis generation
    print("\n4. Testing analysis generation...")
    analysis = processor.generate_analysis_text(data)
    print(f"Analysis length: {len(analysis)} characters")
    print(f"First 200 characters: {analysis[:200]}...")

    # Test chart generation
    print("\n5. Testing chart generation...")
    charts = processor.generate_and_save_charts(data)
    print(f"Generated charts: {list(charts.keys())}")

    print("\n✅ All tests passed!")


if __name__ == "__main__":
    test_major_subject_processor()
