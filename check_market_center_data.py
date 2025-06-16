#!/usr/bin/env python
"""
Check time duration values in database
"""

import os
import sys
import django

# Add the project root directory to Python path
sys.path.insert(0, os.path.abspath('.'))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lungri_report.settings.development')
django.setup()

from apps.infrastructure.models import WardWiseTimeToMarketCenter, TimeDurationChoice

def check_data():
    print("=== Checking Market Center Time Data ===")
    
    print(f"Total records: {WardWiseTimeToMarketCenter.objects.count()}")
    
    print("\nDistinct time_duration values in database:")
    for val in WardWiseTimeToMarketCenter.objects.values_list('time_duration', flat=True).distinct():
        print(f"  '{val}'")
    
    print("\nTimeDurationChoice choices defined in model:")
    for choice in TimeDurationChoice.choices:
        print(f"  '{choice[0]}' -> '{choice[1]}'")
    
    print("\nSample records:")
    for record in WardWiseTimeToMarketCenter.objects.all()[:5]:
        print(f"  Ward {record.ward_number}, Duration: '{record.time_duration}', Households: {record.households}")

if __name__ == "__main__":
    check_data()
