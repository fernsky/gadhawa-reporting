#!/usr/bin/env python
"""
Quick test script to verify infrastructure data processing and PDF generation
"""

import os
import sys
import django

# Add the project root directory to Python path
sys.path.insert(0, os.path.abspath('.'))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lungri_report.settings.development')
django.setup()

from apps.infrastructure.processors.manager import get_infrastructure_manager
from apps.infrastructure.processors.market_center_time import MarketCenterTimeProcessor

def test_infrastructure_processing():
    print("=== Testing Infrastructure Data Processing ===")
    
    # Test manager
    print("\n1. Testing Infrastructure Manager:")
    manager = get_infrastructure_manager()
    print(f"   - Manager created: {type(manager).__name__}")
    print(f"   - Available processors: {list(manager.processors.keys())}")
    
    # Test market center time processor
    print("\n2. Testing Market Center Time Processor:")
    processor = MarketCenterTimeProcessor()
    data = processor.get_data()
    print(f"   - Total households: {data['total_households']}")
    print(f"   - Municipality data categories: {len(data['municipality_data'])}")
    print(f"   - Wards with data: {len(data['ward_data'])}")
    
    # Test analysis generation
    print("\n3. Testing Analysis Generation:")
    analysis = processor.generate_analysis_text(data)
    print(f"   - Analysis length: {len(analysis)} characters")
    print(f"   - Analysis preview: {analysis[:200]}...")
    
    # Test chart generation
    print("\n4. Testing Chart Generation:")
    pie_chart = processor.generate_pie_chart(data)
    print(f"   - Pie chart generated: {pie_chart is not None}")
    
    # Test full processing
    print("\n5. Testing Full Processing:")
    full_data = processor.process_for_pdf()
    print(f"   - Full data keys: {list(full_data.keys())}")
    print(f"   - Has report content: {'report_content' in full_data}")
    print(f"   - Has coherent analysis: {'coherent_analysis' in full_data}")
    print(f"   - Has charts: {'pdf_charts' in full_data}")
    
    # Test manager processing
    print("\n6. Testing Manager Processing:")
    manager.generate_all_charts()
    all_data = manager.process_all_for_pdf()
    print(f"   - Processed categories: {list(all_data.keys())}")
    
    if 'market_center_time' in all_data:
        market_data = all_data['market_center_time']
        print(f"   - Market center data structure: {list(market_data.keys())}")
        if 'data' in market_data:
            print(f"   - Market center households: {market_data['data']['total_households']}")
    
    print("\n=== Infrastructure Processing Test Complete ===")
    return True

if __name__ == "__main__":
    try:
        test_infrastructure_processing()
        print("\n✅ All tests passed successfully!")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
