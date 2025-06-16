#!/usr/bin/env python
"""
Test script for chart generation system
"""
import os
import sys
import django

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lungri_report.settings.base')
django.setup()

from apps.demographics.processors.manager import get_demographics_manager
from apps.demographics.processors.religion import ReligionProcessor
from apps.demographics.processors.language import LanguageProcessor  
from apps.demographics.processors.caste import CasteProcessor


def test_chart_generation():
    """Test chart generation for all demographic categories"""
    print("Testing chart generation system...")
    
    # Test Religion Processor
    print("\n=== Testing Religion Processor ===")
    religion_processor = ReligionProcessor()
    try:
        religion_data = religion_processor.get_data()
        print(f"Religion data keys: {list(religion_data.keys())}")
        
        # Test if we have any data
        total_pop = sum(data['population'] for data in religion_data.values())
        print(f"Total religion population: {total_pop}")
        
        if total_pop > 0:
            # Generate charts
            processed_data = religion_processor.process_for_pdf()
            charts = processed_data.get('charts', {})
            print(f"Generated religion charts: {list(charts.keys())}")
            
            # Check if PNG was generated
            if 'pie_chart_png' in charts:
                print(f"✓ PNG chart generated: {charts['pie_chart_png']}")
            elif 'pie_chart_svg' in charts:
                print(f"⚠ SVG fallback used: {charts['pie_chart_svg']}")
            else:
                print("✗ No charts generated")
        else:
            print("No religion data available for chart generation")
            
    except Exception as e:
        print(f"Error testing religion processor: {e}")
    
    # Test Language Processor
    print("\n=== Testing Language Processor ===")
    language_processor = LanguageProcessor()
    try:
        language_data = language_processor.get_data()
        print(f"Language data keys: {list(language_data.keys())}")
        
        total_pop = sum(data['population'] for data in language_data.values())
        print(f"Total language population: {total_pop}")
        
        if total_pop > 0:
            processed_data = language_processor.process_for_pdf()
            charts = processed_data.get('charts', {})
            print(f"Generated language charts: {list(charts.keys())}")
            
            if 'pie_chart_png' in charts:
                print(f"✓ PNG chart generated: {charts['pie_chart_png']}")
            elif 'pie_chart_svg' in charts:
                print(f"⚠ SVG fallback used: {charts['pie_chart_svg']}")
            else:
                print("✗ No charts generated")
        else:
            print("No language data available for chart generation")
            
    except Exception as e:
        print(f"Error testing language processor: {e}")
    
    # Test Caste Processor
    print("\n=== Testing Caste Processor ===")
    caste_processor = CasteProcessor()
    try:
        caste_data = caste_processor.get_data()
        print(f"Caste data keys: {list(caste_data.keys())}")
        
        total_pop = sum(data['population'] for data in caste_data.values())
        print(f"Total caste population: {total_pop}")
        
        if total_pop > 0:
            processed_data = caste_processor.process_for_pdf()
            charts = processed_data.get('charts', {})
            print(f"Generated caste charts: {list(charts.keys())}")
            
            if 'pie_chart_png' in charts:
                print(f"✓ PNG chart generated: {charts['pie_chart_png']}")
            elif 'pie_chart_svg' in charts:
                print(f"⚠ SVG fallback used: {charts['pie_chart_svg']}")
            else:
                print("✗ No charts generated")
        else:
            print("No caste data available for chart generation")
            
    except Exception as e:
        print(f"Error testing caste processor: {e}")
    
    # Test Manager
    print("\n=== Testing Demographics Manager ===")
    try:
        manager = get_demographics_manager()
        all_data = manager.process_all_for_pdf()
        
        print(f"Processed categories: {list(all_data.keys())}")
        
        for category, data in all_data.items():
            charts = data.get('charts', {})
            print(f"{category.capitalize()}: {list(charts.keys())}")
            
    except Exception as e:
        print(f"Error testing demographics manager: {e}")
    
    print("\nChart generation test completed!")


def test_inkscape_availability():
    """Test if Inkscape is available for PNG conversion"""
    print("\n=== Testing Inkscape Availability ===")
    try:
        import subprocess
        result = subprocess.run(['inkscape', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✓ Inkscape is available: {result.stdout.strip()}")
            return True
        else:
            print("✗ Inkscape command failed")
            return False
    except FileNotFoundError:
        print("✗ Inkscape is not installed or not in PATH")
        return False
    except Exception as e:
        print(f"✗ Error checking Inkscape: {e}")
        return False


if __name__ == '__main__':
    test_inkscape_availability()
    test_chart_generation()
