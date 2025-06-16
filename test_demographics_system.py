"""
Test script for the new demographics processor system
"""

import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lungri_report.settings')
django.setup()

from apps.demographics.processors.manager import get_demographics_manager


def test_demographics_system():
    """Test the new demographics processing system"""
    print("Testing Demographics Processing System")
    print("=" * 50)
    
    # Get manager
    manager = get_demographics_manager()
    
    # Test available categories
    categories = manager.get_available_categories()
    print(f"Available categories: {categories}")
    
    # Test processing all data
    print("\nProcessing all demographics data...")
    all_data = manager.process_all_for_pdf()
    
    for category, data in all_data.items():
        print(f"\n{category.upper()} Demographics:")
        print(f"  Section: {data.get('section_number')} {data.get('section_title')}")
        print(f"  Total Population: {data.get('total_population', 0)}")
        print(f"  Has Report Content: {bool(data.get('report_content'))}")
        print(f"  Has Charts: {bool(data.get('charts', {}).get('pie_chart'))}")
        
        # Show summary stats
        stats = data.get('summary_stats', {})
        if stats.get('top_categories'):
            print(f"  Top categories: {len(stats['top_categories'])}")
            for i, (key, cat_data) in enumerate(stats['top_categories'][:2]):
                if isinstance(cat_data, dict):
                    print(f"    {i+1}. {cat_data.get('name_nepali', key)}: {cat_data.get('population', 0)}")
    
    print("\n" + "=" * 50)
    print("Test completed successfully!")


if __name__ == "__main__":
    test_demographics_system()
