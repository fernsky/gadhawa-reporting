#!/usr/bin/env python
"""
Test script to generate chart images using Inkscape
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

def test_chart_image_generation():
    """Test chart image generation with Inkscape conversion"""
    
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
    
    # Test pie chart image generation
    print("Testing pie chart image generation...")
    success, png_path, svg_path = svg_generator.generate_chart_image(
        religion_data=sample_religion_data,
        output_name="religion_pie_chart",
        static_dir="static/images",
        chart_type="pie",
        include_title=False
    )
    
    if success:
        print(f"✓ Pie chart image generated successfully: {png_path}")
    else:
        print(f"✗ Failed to generate pie chart image. SVG saved at: {svg_path}")
    
    # Test with title
    print("\nTesting pie chart with title...")
    success, png_path, svg_path = svg_generator.generate_chart_image(
        religion_data=sample_religion_data,
        output_name="religion_pie_chart_with_title",
        static_dir="static/images",
        chart_type="pie",
        include_title=True
    )
    
    if success:
        print(f"✓ Pie chart with title generated successfully: {png_path}")
    else:
        print(f"✗ Failed to generate pie chart with title. SVG saved at: {svg_path}")
    
    print("\nTesting completed!")

if __name__ == '__main__':
    test_chart_image_generation()
