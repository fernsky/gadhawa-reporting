#!/usr/bin/env python3
"""
Test script for Nepali number conversion
"""
import os
import sys
import django

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lungri_report.settings.development')
django.setup()

from apps.reports.utils.nepali_numbers import (
    to_nepali_digits, 
    format_nepali_number, 
    format_nepali_percentage,
    format_nepali_currency,
    format_nepali_date_parts
)

def test_conversions():
    print("=== Nepali Number Conversion Tests ===\n")
    
    # Basic digit conversion
    test_cases = [
        "123",
        "456789",
        "0",
        "1.23",
        "99.99",
        "2024",
        "15.5%",
        "1,000",
        "123.456.789"
    ]
    
    print("Basic Digit Conversion:")
    for case in test_cases:
        nepali = to_nepali_digits(case)
        print(f"  {case:>12} → {nepali}")
    
    print("\nNumber Formatting:")
    numbers = [123, 1234, 12345, 123456, 1234567]
    for num in numbers:
        formatted = format_nepali_number(num)
        print(f"  {num:>8} → {formatted}")
    
    print("\nPercentage Formatting:")
    percentages = [12.5, 78.9, 100.0, 0.1]
    for pct in percentages:
        formatted = format_nepali_percentage(pct)
        print(f"  {pct:>6}% → {formatted}")
    
    print("\nCurrency Formatting:")
    amounts = [1000, 12500, 123456, 1000000]
    for amount in amounts:
        formatted = format_nepali_currency(amount)
        print(f"  Rs.{amount:>8} → {formatted}")
    
    print("\nDate Formatting:")
    from datetime import date
    test_date = date(2024, 12, 15)
    formatted_date = format_nepali_date_parts(test_date)
    print(f"  {test_date} → {formatted_date}")

if __name__ == "__main__":
    test_conversions()
