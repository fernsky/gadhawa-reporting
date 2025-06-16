#!/usr/bin/env python
"""
Demo script to test chart generation with sample data
"""
import os
import sys
import django

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lungri_report.settings.base')
django.setup()

from apps.demographics.processors.religion import ReligionProcessor
from apps.demographics.processors.language import LanguageProcessor
from apps.demographics.processors.caste import CasteProcessor


def create_sample_religion_data():
    """Create sample religion data for testing"""
    return {
        'HINDU': {
            'population': 1500,
            'percentage': 75.0,
            'name_nepali': 'हिन्दू',
        },
        'BUDDHIST': {
            'population': 300,
            'percentage': 15.0,
            'name_nepali': 'बौद्ध',
        },
        'KIRANT': {
            'population': 150,
            'percentage': 7.5,
            'name_nepali': 'किरात',
        },
        'CHRISTIAN': {
            'population': 50,
            'percentage': 2.5,
            'name_nepali': 'इसाई',
        },
    }


def create_sample_language_data():
    """Create sample language data for testing"""
    return {
        'NEPALI': {
            'population': 1200,
            'percentage': 60.0,
            'name_nepali': 'नेपाली',
        },
        'LIMBU': {
            'population': 400,
            'percentage': 20.0,
            'name_nepali': 'लिम्बू',
        },
        'RAI': {
            'population': 200,
            'percentage': 10.0,
            'name_nepali': 'राई',
        },
        'HINDI': {
            'population': 100,
            'percentage': 5.0,
            'name_nepali': 'हिन्दी',
        },
        'SHERPA': {
            'population': 100,
            'percentage': 5.0,
            'name_nepali': 'शेर्पा',
        },
    }


def create_sample_caste_data():
    """Create sample caste data for testing"""
    return {
        'CHHETRI': {
            'code': 'CHHETRI',
            'name_nepali': 'क्षेत्री',
            'population': 800,
            'percentage': 40.0,
        },
        'BRAHMIN': {
            'code': 'BRAHMIN',
            'name_nepali': 'ब्राह्मण',
            'population': 400,
            'percentage': 20.0,
        },
        'MAGAR': {
            'code': 'MAGAR',
            'name_nepali': 'मगर',
            'population': 300,
            'percentage': 15.0,
        },
        'TAMANG': {
            'code': 'TAMANG',
            'name_nepali': 'तामाङ',
            'population': 200,
            'percentage': 10.0,
        },
        'RAI': {
            'code': 'RAI',
            'name_nepali': 'राई',
            'population': 150,
            'percentage': 7.5,
        },
        'LIMBU': {
            'code': 'LIMBU',
            'name_nepali': 'लिम्बू',
            'population': 150,
            'percentage': 7.5,
        },
    }


def test_chart_generation_with_sample_data():
    """Test chart generation with sample data"""
    print("Testing chart generation with sample data...")
    
    # Test Religion Charts
    print("\n=== Testing Religion Charts ===")
    try:
        religion_processor = ReligionProcessor()
        sample_religion_data = create_sample_religion_data()
        
        # Generate SVG chart
        svg_content = religion_processor.generate_chart_svg(sample_religion_data, "pie")
        if svg_content:
            print("✓ Religion SVG chart generated successfully")
            
            # Save to file
            charts_dir = religion_processor.static_charts_dir
            svg_path = charts_dir / "sample_religion_pie_chart.svg"
            png_path = charts_dir / "sample_religion_pie_chart.png"
            
            religion_processor.save_svg_to_file(svg_content, svg_path)
            print(f"✓ SVG saved to: {svg_path}")
            
            # Try to convert to PNG
            if religion_processor.convert_svg_to_png(svg_path, png_path):
                print(f"✓ PNG converted successfully: {png_path}")
            else:
                print("⚠ PNG conversion failed, SVG available")
        else:
            print("✗ Failed to generate religion SVG chart")
            
    except Exception as e:
        print(f"Error testing religion charts: {e}")
    
    # Test Language Charts
    print("\n=== Testing Language Charts ===")
    try:
        language_processor = LanguageProcessor()
        sample_language_data = create_sample_language_data()
        
        # Generate SVG chart
        svg_content = language_processor.generate_chart_svg(sample_language_data, "pie")
        if svg_content:
            print("✓ Language SVG chart generated successfully")
            
            # Save to file
            charts_dir = language_processor.static_charts_dir
            svg_path = charts_dir / "sample_language_pie_chart.svg"
            png_path = charts_dir / "sample_language_pie_chart.png"
            
            language_processor.save_svg_to_file(svg_content, svg_path)
            print(f"✓ SVG saved to: {svg_path}")
            
            # Try to convert to PNG
            if language_processor.convert_svg_to_png(svg_path, png_path):
                print(f"✓ PNG converted successfully: {png_path}")
            else:
                print("⚠ PNG conversion failed, SVG available")
        else:
            print("✗ Failed to generate language SVG chart")
            
    except Exception as e:
        print(f"Error testing language charts: {e}")
    
    # Test Caste Charts
    print("\n=== Testing Caste Charts ===")
    try:
        caste_processor = CasteProcessor()
        sample_caste_data = create_sample_caste_data()
        
        # Generate SVG chart
        svg_content = caste_processor.generate_chart_svg(sample_caste_data, "pie")
        if svg_content:
            print("✓ Caste SVG chart generated successfully")
            
            # Save to file
            charts_dir = caste_processor.static_charts_dir
            svg_path = charts_dir / "sample_caste_pie_chart.svg"
            png_path = charts_dir / "sample_caste_pie_chart.png"
            
            caste_processor.save_svg_to_file(svg_content, svg_path)
            print(f"✓ SVG saved to: {svg_path}")
            
            # Try to convert to PNG
            if caste_processor.convert_svg_to_png(svg_path, png_path):
                print(f"✓ PNG converted successfully: {png_path}")
            else:
                print("⚠ PNG conversion failed, SVG available")
        else:
            print("✗ Failed to generate caste SVG chart")
            
    except Exception as e:
        print(f"Error testing caste charts: {e}")
    
    print("\nSample data chart generation test completed!")


if __name__ == '__main__':
    test_chart_generation_with_sample_data()
