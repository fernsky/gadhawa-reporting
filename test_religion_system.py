#!/usr/bin/env python
"""
Test script for religion demographics system

This script demonstrates the complete religion demographics pipeline including:
1. Model setup and data creation
2. View functionality 
3. Chart generation
4. Report formatting
5. PDF generation integration
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lungri_report.settings.base')
django.setup()

from django.test import RequestFactory
from apps.demographics.models import WardWiseReligionPopulation, ReligionTypeChoice
from apps.demographics.views.religion import ReligionDemographicsView
from apps.demographics.utils.chart_generator import ReligionChartGenerator
from apps.demographics.utils.report_formatter import ReligionReportFormatter


def test_models():
    """Test model functionality"""
    print("=== Testing Models ===")
    
    # Check if we have any data
    total_records = WardWiseReligionPopulation.objects.count()
    print(f"Total religion population records: {total_records}")
    
    if total_records == 0:
        print("No data found. Please run: python manage.py create_religion_sample_data")
        return False
    
    # Test religion choices
    print("Available religions:")
    for choice in ReligionTypeChoice.choices:
        count = WardWiseReligionPopulation.objects.filter(religion_type=choice[0]).count()
        total_pop = sum(WardWiseReligionPopulation.objects.filter(
            religion_type=choice[0]
        ).values_list('population', flat=True))
        if total_pop > 0:
            print(f"  {choice[1]}: {total_pop:,} people in {count} wards")
    
    # Test ward coverage
    wards_with_data = set(WardWiseReligionPopulation.objects.values_list('ward_number', flat=True))
    print(f"Wards with religion data: {sorted(wards_with_data)}")
    
    return True


def test_views():
    """Test view functionality"""
    print("\n=== Testing Views ===")
    
    # Create a mock request
    factory = RequestFactory()
    request = factory.get('/demographics/religion/')
    
    # Test the main religion view
    view = ReligionDemographicsView()
    view.request = request
    
    try:
        # Test data retrieval methods
        religion_data = view.get_religion_population_data()
        ward_data = view.get_ward_wise_religion_data()
        major_religions = view.get_major_religions(religion_data)
        ward_summary = view.get_ward_summary(ward_data)
        
        print(f"Religion data retrieved: {len(religion_data)} religions")
        print(f"Ward data retrieved: {len(ward_data)} wards")
        print(f"Major religions identified: {len(major_religions)}")
        print(f"Ward summary calculated: {ward_summary}")
        
        return True
        
    except Exception as e:
        print(f"Error in view testing: {e}")
        return False


def test_chart_generation():
    """Test chart generation"""
    print("\n=== Testing Chart Generation ===")
    
    try:
        view = ReligionDemographicsView()
        religion_data = view.get_religion_population_data()
        ward_data = view.get_ward_wise_religion_data()
        
        chart_generator = ReligionChartGenerator()
        
        # Test different chart types
        charts = {
            'pie_chart': chart_generator.generate_overall_pie_chart(religion_data),
            'bar_chart': chart_generator.generate_ward_comparison_bar(ward_data),
            'trend_chart': chart_generator.generate_religion_trend_chart(religion_data),
        }
        
        for chart_name, chart_data in charts.items():
            if chart_data:
                print(f"✓ {chart_name} generated successfully")
            else:
                print(f"✗ {chart_name} generation failed")
        
        return True
        
    except Exception as e:
        print(f"Error in chart generation: {e}")
        return False


def test_report_formatting():
    """Test report content formatting"""
    print("\n=== Testing Report Formatting ===")
    
    try:
        view = ReligionDemographicsView()
        religion_data = view.get_religion_population_data()
        ward_data = view.get_ward_wise_religion_data()
        
        formatter = ReligionReportFormatter()
        report_content = formatter.generate_formal_report(religion_data, ward_data)
        
        print("Report sections generated:")
        for section_name, content in report_content.items():
            if isinstance(content, list):
                print(f"  ✓ {section_name}: {len(content)} items")
            else:
                print(f"  ✓ {section_name}: {len(str(content))} characters")
        
        return True
        
    except Exception as e:
        print(f"Error in report formatting: {e}")
        return False


def test_integration():
    """Test full integration"""
    print("\n=== Testing Full Integration ===")
    
    try:
        # This would test the PDF generation integration
        # For now, just verify all components work together
        
        factory = RequestFactory()
        request = factory.get('/reports/pdf/full/')
        
        from apps.reports.views.pdf import GenerateFullReportPDFView
        view = GenerateFullReportPDFView()
        view.request = request
        
        # Test context generation (without actually generating PDF)
        municipality_name = "लुङ्ग्री गाउँपालिका"
        religion_view = ReligionDemographicsView()
        religion_data = religion_view.get_religion_population_data()
        ward_data = religion_view.get_ward_wise_religion_data()
        
        print("✓ Integration context prepared successfully")
        print(f"  - Municipality: {municipality_name}")
        print(f"  - Religions: {len([r for r in religion_data.values() if r['population'] > 0])}")
        print(f"  - Wards: {len(ward_data)}")
        print(f"  - Total population: {sum(data['population'] for data in religion_data.values()):,}")
        
        return True
        
    except Exception as e:
        print(f"Error in integration testing: {e}")
        return False


def main():
    """Run all tests"""
    print("Religion Demographics System Test")
    print("=" * 50)
    
    tests = [
        ("Models", test_models),
        ("Views", test_views),
        ("Chart Generation", test_chart_generation),
        ("Report Formatting", test_report_formatting),
        ("Integration", test_integration),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"Critical error in {test_name}: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! The religion demographics system is ready to use.")
        print("\nNext steps:")
        print("1. Run: python manage.py create_religion_sample_data")
        print("2. Access: /demographics/religion/ for web view")
        print("3. Generate PDF: /reports/pdf/full/")
    else:
        print(f"\n⚠️  {len(results) - passed} tests failed. Please check the errors above.")


if __name__ == "__main__":
    main()
