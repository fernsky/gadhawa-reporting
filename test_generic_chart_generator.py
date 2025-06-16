#!/usr/bin/env python3
"""
Test script for the generic SVGChartGenerator

This script tests the updated SVGChartGenerator with different demographic data types.
"""

import os
import sys
import django

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lungri_report.settings')
django.setup()

from apps.demographics.utils.svg_chart_generator import SVGChartGenerator, RELIGION_COLORS, LANGUAGE_COLORS, CASTE_COLORS

def test_religion_chart():
    """Test religion chart generation"""
    print("Testing Religion Chart Generation...")
    
    # Sample religion data
    religion_data = {
        'HINDU': {'name_nepali': 'हिन्दू', 'population': 1500, 'percentage': 75.0},
        'BUDDHIST': {'name_nepali': 'बौद्ध', 'population': 300, 'percentage': 15.0},
        'KIRANT': {'name_nepali': 'किरात', 'population': 150, 'percentage': 7.5},
        'CHRISTIAN': {'name_nepali': 'क्रिस्चियन', 'population': 50, 'percentage': 2.5},
    }
    
    # Create generator with religion colors
    generator = SVGChartGenerator(colors=RELIGION_COLORS)
    
    # Generate charts
    success, png_path, svg_path = generator.generate_chart_image(
        demographic_data=religion_data,
        output_name="test_religion_chart",
        chart_type="pie",
        include_title=True,
        title_nepali="धर्म अनुसार जनसंख्या वितरण",
        title_english="Population Distribution by Religion"
    )
    
    if success:
        print(f"✓ Religion chart generated successfully: {png_path}")
    else:
        print(f"✗ Religion chart generation failed, SVG available: {svg_path}")
    
    return success

def test_language_chart():
    """Test language chart generation"""
    print("Testing Language Chart Generation...")
    
    # Sample language data
    language_data = {
        'NEPALI': {'name_nepali': 'नेपाली', 'population': 1200, 'percentage': 60.0},
        'LIMBU': {'name_nepali': 'लिम्बु', 'population': 400, 'percentage': 20.0},
        'RAI': {'name_nepali': 'राई', 'population': 300, 'percentage': 15.0},
        'HINDI': {'name_nepali': 'हिन्दी', 'population': 100, 'percentage': 5.0},
    }
    
    # Create generator with language colors
    generator = SVGChartGenerator(colors=LANGUAGE_COLORS)
    
    # Generate charts
    success, png_path, svg_path = generator.generate_chart_image(
        demographic_data=language_data,
        output_name="test_language_chart",
        chart_type="pie",
        include_title=True,
        title_nepali="मातृभाषाको आधारमा जनसंख्या वितरण",
        title_english="Population Distribution by Mother Tongue"
    )
    
    if success:
        print(f"✓ Language chart generated successfully: {png_path}")
    else:
        print(f"✗ Language chart generation failed, SVG available: {svg_path}")
    
    return success

def test_caste_chart():
    """Test caste chart generation"""
    print("Testing Caste Chart Generation...")
    
    # Sample caste data
    caste_data = {
        'BRAHMIN': {'name_nepali': 'ब्राह्मण', 'population': 800, 'percentage': 40.0},
        'CHHETRI': {'name_nepali': 'क्षेत्री', 'population': 600, 'percentage': 30.0},
        'MAGAR': {'name_nepali': 'मगर', 'population': 400, 'percentage': 20.0},
        'TAMANG': {'name_nepali': 'तामाङ', 'population': 200, 'percentage': 10.0},
    }
    
    # Create generator with caste colors
    generator = SVGChartGenerator(colors=CASTE_COLORS)
    
    # Generate charts
    success, png_path, svg_path = generator.generate_chart_image(
        demographic_data=caste_data,
        output_name="test_caste_chart",
        chart_type="pie",
        include_title=True,
        title_nepali="जातिगत आधारमा जनसंख्या वितरण",
        title_english="Population Distribution by Caste"
    )
    
    if success:
        print(f"✓ Caste chart generated successfully: {png_path}")
    else:
        print(f"✗ Caste chart generation failed, SVG available: {svg_path}")
    
    return success

def main():
    """Run all tests"""
    print("=" * 60)
    print("Testing Generic SVGChartGenerator")
    print("=" * 60)
    
    # Test different demographic types
    religion_success = test_religion_chart()
    print()
    language_success = test_language_chart()
    print()
    caste_success = test_caste_chart()
    
    print("\n" + "=" * 60)
    print("Test Results Summary:")
    print(f"Religion Chart: {'✓ PASS' if religion_success else '✗ FAIL'}")
    print(f"Language Chart: {'✓ PASS' if language_success else '✗ FAIL'}")
    print(f"Caste Chart: {'✓ PASS' if caste_success else '✗ FAIL'}")
    
    if all([religion_success, language_success, caste_success]):
        print("\n🎉 All tests passed! The generic SVGChartGenerator is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
        print("Note: If PNG generation failed but SVG is available, it's likely that")
        print("Inkscape is not installed or not in PATH. SVG charts will still work.")

if __name__ == "__main__":
    main()
