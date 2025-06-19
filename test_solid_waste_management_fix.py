#!/usr/bin/env python3
"""
Test script to verify solid waste management processor ward data
"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.append('/Users/trilochan/Desktop/final-delivery/digital-profile/lungri/lungri-report')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lungri_report.settings.development')
django.setup()

from apps.social.processors.solid_waste_management import SolidWasteManagementProcessor


def test_solid_waste_management_processor():
    """Test solid waste management processor data structure"""
    print("=== Testing Solid Waste Management Processor ===")
    
    processor = SolidWasteManagementProcessor()
    data = processor.get_data()
    
    print(f"Total households: {data.get('total_households', 0)}")
    print(f"Municipality data keys: {list(data.get('municipality_data', {}).keys())}")
    print(f"Ward data available: {len(data.get('ward_data', {}))}")
    
    # Check ward data structure
    ward_data = data.get('ward_data', {})
    for ward_num, ward_info in ward_data.items():
        print(f"\nWard {ward_num}:")
        print(f"  Total population: {ward_info.get('total_population', 0)}")
        print(f"  Demographics field present: {'demographics' in ward_info}")
        if 'demographics' in ward_info:
            demographics = ward_info['demographics']
            print(f"  Demographics keys: {list(demographics.keys())}")
            # Show first few entries
            for method, method_data in list(demographics.items())[:3]:
                print(f"    {method}: {method_data.get('population', 0)} households")
        else:
            print("  WARNING: No demographics field found!")
    
    print("\n=== Test Complete ===")
    return data


if __name__ == "__main__":
    test_solid_waste_management_processor()
