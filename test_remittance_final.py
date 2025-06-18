#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lungri_report.settings.development")
django.setup()

# Test the remittance expenses processor
try:
    from apps.economics.processors.remittance_expenses import (
        RemittanceExpensesProcessor,
    )

    print("✓ RemittanceExpensesProcessor imported successfully")

    # Test initialization
    processor = RemittanceExpensesProcessor()
    print(f"✓ Processor initialized successfully")
    print(f"✓ Section title: {processor.get_section_title()}")
    print(f"✓ Section number: {processor.get_section_number()}")

    # Test data retrieval
    print("\n=== Testing data retrieval ===")
    data = processor.get_data()
    print(f"✓ Data retrieved successfully")
    print(f"✓ Total households: {data.get('total_households', 0)}")
    print(f"✓ Municipality data keys: {list(data.get('municipality_data', {}).keys())}")
    print(f"✓ Ward data keys: {list(data.get('ward_data', {}).keys())}")

    # Test analysis text generation
    print("\n=== Testing analysis text generation ===")
    try:
        analysis = processor.generate_analysis_text(data)
        print(f"✓ Analysis text generated successfully (length: {len(analysis)} chars)")
        print(f"✓ First 200 chars: {analysis[:200]}...")
    except Exception as e:
        print(f"✗ Error generating analysis text: {e}")

    # Test PDF processing
    print("\n=== Testing PDF processing ===")
    try:
        pdf_data = processor.process_for_pdf()
        print(f"✓ PDF data processed successfully")
        print(f"✓ PDF data keys: {list(pdf_data.keys())}")
        print(f"✓ Total households in PDF: {pdf_data.get('total_households', 0)}")
    except Exception as e:
        print(f"✗ Error processing PDF data: {e}")

    print("\n=== All tests completed ===")

except ImportError as e:
    print(f"✗ Import error: {e}")
except Exception as e:
    print(f"✗ Unexpected error: {e}")
