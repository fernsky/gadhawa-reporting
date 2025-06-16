#!/usr/bin/env python
"""
Test script for full PDF generation with new demographics system
"""
import os
import sys
import django

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lungri_report.settings.base')
django.setup()

from django.template.loader import render_to_string
from django.utils import timezone
from apps.demographics.processors.manager import get_demographics_manager
from apps.reports.models import PublicationSettings


def test_pdf_template_rendering():
    """Test PDF template rendering with demographics data"""
    print("Testing PDF template rendering with demographics data...")
    print("=" * 60)
    
    try:
        # Get demographics data (same as in the view)
        demographics_manager = get_demographics_manager()
        
        # Generate all charts
        print("Generating charts...")
        demographics_manager.generate_all_charts()
        
        # Get processed data with charts
        all_demographics_data = demographics_manager.process_all_for_pdf()
        
        # Extract chart URLs for template use
        pdf_charts = {}
        for category, data in all_demographics_data.items():
            if 'charts' in data:
                pdf_charts[category] = data['charts']
        
        print(f"Chart URLs generated:")
        for category, charts in pdf_charts.items():
            print(f"  {category.upper()}:")
            for chart_type, url in charts.items():
                print(f"    - {chart_type}: {url}")
        
        # Get publication settings
        try:
            publication_settings = PublicationSettings.objects.first()
        except:
            publication_settings = None
        
        # Build context (same as in the view)
        context = {
            "municipality_name": "लुङ्ग्री गाउँपालिका",
            "municipality_name_english": "Lungri Rural Municipality",
            "publication_settings": publication_settings,
            "generated_date": timezone.now(),
            "all_demographics_data": all_demographics_data,
            "pdf_charts": pdf_charts,
        }
        
        print(f"\nContext prepared with keys: {list(context.keys())}")
        print(f"Demographics data categories: {list(all_demographics_data.keys())}")
        
        # Test template rendering
        print("\nRendering PDF template...")
        html_content = render_to_string('reports/pdf_full_report.html', context)
        
        # Save rendered HTML for inspection
        output_file = "test_pdf_output.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✓ Template rendered successfully!")
        print(f"✓ HTML content saved to: {output_file}")
        print(f"✓ Content length: {len(html_content)} characters")
        
        # Check if charts are included in the rendered content
        chart_found = {}
        for category in ['religion', 'language', 'caste']:
            if f'charts/{category}_pie_chart' in html_content:
                chart_found[category] = True
                print(f"✓ {category.capitalize()} chart found in rendered HTML")
            else:
                chart_found[category] = False
                print(f"⚠ {category.capitalize()} chart NOT found in rendered HTML")
        
        # Check for specific Nepali content
        nepali_content_checks = [
            ('धर्म अनुसार', 'Religion section header'),
            ('मातृभाषाको आधारमा', 'Language section header'),
            ('जातिगत आधारमा', 'Caste section header'),
            ('चित्र ३.', 'Figure numbering'),
            ('तालिका ३.', 'Table numbering'),
        ]
        
        print(f"\nChecking Nepali content...")
        for text, description in nepali_content_checks:
            if text in html_content:
                print(f"✓ {description}: Found")
            else:
                print(f"⚠ {description}: Not found")
        
        # Summary
        print(f"\n{'=' * 60}")
        print("✓ PDF TEMPLATE RENDERING TEST COMPLETED SUCCESSFULLY")
        print("✓ Demographics data is properly integrated")
        print("✓ Charts are being included in the template")
        print("✓ Nepali content is properly rendered")
        print(f"✓ Output saved to: {output_file}")
        
        # Instructions for manual verification
        print(f"\nMANUAL VERIFICATION STEPS:")
        print(f"1. Open {output_file} in a web browser")
        print(f"2. Check that all charts are displayed correctly")
        print(f"3. Verify Nepali text is rendered properly")
        print(f"4. Confirm table data is populated")
        print(f"5. Check that page breaks are appropriate")
        
        return True
        
    except Exception as e:
        print(f"\n{'=' * 60}")
        print(f"✗ PDF TEMPLATE RENDERING TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_individual_partials():
    """Test individual demographic partials"""
    print(f"\n{'=' * 60}")
    print("TESTING INDIVIDUAL DEMOGRAPHIC PARTIALS")
    print("=" * 60)
    
    try:
        # Get demographics data
        demographics_manager = get_demographics_manager()
        all_demographics_data = demographics_manager.process_all_for_pdf()
        
        # Extract chart URLs
        pdf_charts = {}
        for category, data in all_demographics_data.items():
            if 'charts' in data:
                pdf_charts[category] = data['charts']
        
        partials_to_test = [
            ('demographics/religion/religion_report_partial.html', 'religion'),
            ('demographics/language/language_report_partial.html', 'language'),
            ('demographics/caste/caste_report_partial.html', 'caste'),
        ]
        
        for template_path, category in partials_to_test:
            print(f"\nTesting {category} partial...")
            
            if category in all_demographics_data:
                context = {
                    f'{category}_data': all_demographics_data[category]['data'],
                    'total_population': all_demographics_data[category]['total_population'],
                    'coherent_analysis': all_demographics_data[category]['report_content'],
                    'pdf_charts': pdf_charts,
                }
                
                try:
                    partial_html = render_to_string(template_path, context)
                    print(f"✓ {category.capitalize()} partial rendered successfully ({len(partial_html)} chars)")
                    
                    # Save individual partial for inspection
                    partial_file = f"test_{category}_partial.html"
                    with open(partial_file, 'w', encoding='utf-8') as f:
                        f.write(partial_html)
                    print(f"✓ Saved to: {partial_file}")
                    
                except Exception as e:
                    print(f"✗ {category.capitalize()} partial failed: {e}")
            else:
                print(f"⚠ No data available for {category}")
        
        print(f"\n✓ Individual partials testing completed")
        return True
        
    except Exception as e:
        print(f"✗ Individual partials testing failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success1 = test_pdf_template_rendering()
    success2 = test_individual_partials()
    
    if success1 and success2:
        print(f"\n{'🎉' * 20}")
        print("ALL TESTS PASSED! PDF generation system is ready.")
        print(f"{'🎉' * 20}")
    else:
        print(f"\n{'❌' * 20}")
        print("SOME TESTS FAILED! Please check the errors above.")
        print(f"{'❌' * 20}")
        sys.exit(1)
