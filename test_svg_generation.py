#!/usr/bin/env python
"""
Test script to verify SVG chart generation works correctly
"""

import os
import sys
import django

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lungri_report.settings.development')
django.setup()

# Now import and test
from apps.demographics.utils.svg_chart_generator import SVGChartGenerator

def test_svg_generation():
    """Test SVG chart generation with sample data"""
    
    # Sample religion data
    sample_religion_data = {
        'HINDU': {
            'code': 'HINDU',
            'name_nepali': 'हिन्दू',
            'population': 1200,
            'percentage': 60.0,
        },
        'BUDDHIST': {
            'code': 'BUDDHIST', 
            'name_nepali': 'बौद्ध',
            'population': 500,
            'percentage': 25.0,
        },
        'CHRISTIAN': {
            'code': 'CHRISTIAN',
            'name_nepali': 'क्रिस्चियन',
            'population': 200,
            'percentage': 10.0,
        },
        'KIRANT': {
            'code': 'KIRANT',
            'name_nepali': 'किरात',
            'population': 100,
            'percentage': 5.0,
        },
        'OTHER': {
            'code': 'OTHER',
            'name_nepali': 'अन्य',
            'population': 0,
            'percentage': 0.0,
        }
    }
    
    # Create SVG chart generator
    svg_generator = SVGChartGenerator()
    
    # Test pie chart generation
    print("Testing SVG pie chart generation...")
    pie_chart_svg = svg_generator.generate_pie_chart_svg(sample_religion_data)
    
    if pie_chart_svg:
        print("✓ Pie chart SVG generated successfully")
        print(f"SVG length: {len(pie_chart_svg)} characters")
        
        # Save to file for inspection
        with open('test_pie_chart.svg', 'w', encoding='utf-8') as f:
            f.write(pie_chart_svg)
        print("✓ Pie chart saved to test_pie_chart.svg")
        
        # Show first few lines
        lines = pie_chart_svg.split('\n')[:10]
        print("First 10 lines of SVG:")
        for line in lines:
            print(f"  {line}")
            
    else:
        print("✗ Failed to generate pie chart SVG")
    
    # Test bar chart generation (with empty ward data)
    print("\nTesting SVG bar chart generation...")
    bar_chart_svg = svg_generator.generate_bar_chart_svg({})
    
    if bar_chart_svg:
        print("✓ Bar chart SVG generated successfully")
    else:
        print("✓ Bar chart returned None (expected for empty data)")
    
    print("\nTesting completed!")

if __name__ == '__main__':
    test_svg_generation()
