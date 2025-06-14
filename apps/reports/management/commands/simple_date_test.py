from django.core.management.base import BaseCommand
from datetime import datetime
from apps.reports.templatetags.nepali_filters import nepali_date

class Command(BaseCommand):
    help = 'Simple test for nepali_date filter'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Testing nepali_date filter directly...'))
        
        # Test date
        test_date = datetime(2025, 6, 13)
        
        self.stdout.write(f'Input date: {test_date}')
        
        # Test the filter
        result = nepali_date(test_date, "Y F j")
        self.stdout.write(f'nepali_date(test_date, "Y F j"): {result}')
        
        # Test without format string
        result_no_format = nepali_date(test_date)
        self.stdout.write(f'nepali_date(test_date): {result_no_format}')
        
        # Test manual formatting (Windows compatible)
        formatted_manual = test_date.strftime("%Y %B %d")
        self.stdout.write(f'Manual strftime("%Y %B %d"): {formatted_manual}')
        
        # Test the utility function directly
        from apps.reports.utils.nepali_numbers import format_nepali_date_full
        
        result_util = format_nepali_date_full(formatted_manual)
        self.stdout.write(f'format_nepali_date_full("{formatted_manual}"): {result_util}')
        
        result_util_date = format_nepali_date_full(test_date, "%Y %B %d")
        self.stdout.write(f'format_nepali_date_full(date, "%Y %B %d"): {result_util_date}')
        
        self.stdout.write(self.style.SUCCESS('Test completed!'))
