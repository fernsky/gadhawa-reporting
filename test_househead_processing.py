#!/usr/bin/env python3
"""
Test script for househead demographics processing

Run this script to test the househead processor with sample data.
"""

import os
import sys
import django

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lungri_report.settings.development')
django.setup()

from apps.demographics.processors.househead import HouseheadProcessor
from apps.demographics.models import WardWiseHouseheadGender, GenderChoice


def test_househead_processing():
    """Test househead demographics processing"""
    
    print("=== Testing Househead Demographics Processing ===\n")
    
    # Check if we have data
    total_records = WardWiseHouseheadGender.objects.count()
    if total_records == 0:
        print("❌ No househead data found in database!")
        print("Run: python manage.py create_househead_sample_data")
        return False
    
    print(f"✅ Found {total_records} househead records in database")
    
    # Initialize processor
    processor = HouseheadProcessor()
    
    # Test data retrieval
    print("\n--- Testing Data Retrieval ---")
    househead_data = processor.get_data()
    
    if not househead_data:
        print("❌ Failed to retrieve househead data")
        return False
    
    print(f"✅ Retrieved data for {len(househead_data)} gender categories")
    
    # Display data
    total_households = sum(data['population'] for data in househead_data.values())
    print(f"📊 Total households: {total_households:,}")
    
    for gender_code, data in househead_data.items():
        if data['population'] > 0:
            gender_name = data['name_nepali']
            population = data['population']
            percentage = data['percentage']
            print(f"   {gender_name}: {population:,} households ({percentage:.1f}%)")
    
    # Test report generation
    print("\n--- Testing Report Generation ---")
    try:
        report_content = processor.generate_report_content(househead_data)
        if report_content and len(report_content) > 100:
            print("✅ Report content generated successfully")
            print(f"📝 Report length: {len(report_content)} characters")
            print(f"📄 First 200 chars: {report_content[:200]}...")
        else:
            print("❌ Report content too short or empty")
            return False
    except Exception as e:
        print(f"❌ Report generation failed: {e}")
        return False
    
    # Test chart generation
    print("\n--- Testing Chart Generation ---")
    try:
        # Test SVG generation
        pie_svg = processor.generate_chart_svg(househead_data, "pie")
        if pie_svg and len(pie_svg) > 100:
            print("✅ Pie chart SVG generated successfully")
        else:
            print("❌ Pie chart SVG generation failed")
    except Exception as e:
        print(f"❌ Chart generation failed: {e}")
        return False
    
    # Test full PDF processing
    print("\n--- Testing Full PDF Processing ---")
    try:
        pdf_data = processor.process_for_pdf()
        if pdf_data and all(key in pdf_data for key in ['data', 'report_content', 'section_title']):
            print("✅ PDF processing completed successfully")
            print(f"📊 Section: {pdf_data['section_number']} {pdf_data['section_title']}")
            print(f"📈 Total households: {pdf_data['total_population']:,}")
        else:
            print("❌ PDF processing failed - missing required keys")
            return False
    except Exception as e:
        print(f"❌ PDF processing failed: {e}")
        return False
    
    print("\n=== All Tests Passed! ===")
    return True


def display_database_summary():
    """Display summary of househead data in database"""
    
    print("\n=== Database Summary ===")
    
    # Total records
    total_records = WardWiseHouseheadGender.objects.count()
    print(f"📊 Total records: {total_records}")
    
    if total_records == 0:
        print("No data available")
        return
    
    # Gender breakdown
    print("\n🚻 Gender breakdown:")
    for gender_choice in GenderChoice.choices:
        gender_code = gender_choice[0]
        gender_name = gender_choice[1]
        households = WardWiseHouseheadGender.objects.filter(gender=gender_code).aggregate(
            total=models.Sum('population')
        )['total'] or 0
        
        if households > 0:
            print(f"   {gender_name}: {households:,} households")
    
    # Ward breakdown
    print("\n🏘️  Ward breakdown:")
    for ward_num in range(1, 10):
        ward_households = WardWiseHouseheadGender.objects.filter(ward_number=ward_num).aggregate(
            total=models.Sum('population')
        )['total'] or 0
        if ward_households > 0:
            print(f"   वडा {ward_num}: {ward_households:,} households")


if __name__ == '__main__':
    from django.db import models
    
    display_database_summary()
    test_househead_processing()
