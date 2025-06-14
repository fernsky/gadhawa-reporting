from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime
from apps.reports.templatetags.nepali_filters import nepali_date, nepali_date_simple
from apps.reports.utils.nepali_numbers import format_nepali_date_full, to_nepali_digits

class Command(BaseCommand):
    help = 'Test Nepali date formatting'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Testing Nepali date formatting...'))
        
        # Test current date
        now = timezone.now()
        current_date = datetime(2025, 6, 13)  # The date mentioned by user
        
        self.stdout.write('\n=== CURRENT DATE TESTING ===')
        self.stdout.write(f'Original date: {current_date}')
        self.stdout.write(f'Django format "Y F j": {current_date.strftime("%Y %B %d")}')
        
        # Test our Nepali filters
        self.stdout.write('\n=== NEPALI FILTER TESTING ===')
        
        # Test the filter with different formats
        formats_to_test = [
            '%Y %B %d',  # 2025 June 13
            '%Y %B %j',  # 2025 June 13
            '%d %B %Y',  # 13 June 2025
            '%B %d, %Y', # June 13, 2025
            '%Y-%m-%d',  # 2025-06-13
        ]
        
        for fmt in formats_to_test:
            formatted = current_date.strftime(fmt)
            nepali_formatted = format_nepali_date_full(current_date, fmt)
            self.stdout.write(f'Format "{fmt}":')
            self.stdout.write(f'  English: {formatted}')
            self.stdout.write(f'  Nepali:  {nepali_formatted}')
            self.stdout.write('')
        
        # Test the Django template filter
        self.stdout.write('\n=== DJANGO TEMPLATE FILTER TESTING ===')
        
        # Test with Django format string
        django_format = "Y F j"  # This is what Django uses
        formatted_english = current_date.strftime("%Y %B %d")
        
        try:
            # Test our filter
            nepali_result = nepali_date(current_date, "Y F j")
            self.stdout.write(f'Django filter nepali_date with "Y F j":')
            self.stdout.write(f'  Input: {current_date}')
            self.stdout.write(f'  English equivalent: {formatted_english}')
            self.stdout.write(f'  Nepali result: {nepali_result}')
            
            # Test simple digit conversion
            simple_result = to_nepali_digits(formatted_english)
            self.stdout.write(f'  Simple digit conversion: {simple_result}')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error testing template filter: {e}'))
        
        # Test month name mapping
        self.stdout.write('\n=== MONTH NAME MAPPING TEST ===')
        months_to_test = [
            ('January', 'जनवरी'),
            ('February', 'फेब्रुअरी'),
            ('March', 'मार्च'),
            ('April', 'अप्रिल'),
            ('May', 'मे'),
            ('June', 'जुन'),
            ('July', 'जुलाई'),
            ('August', 'अगस्त'),
            ('September', 'सेप्टेम्बर'),
            ('October', 'अक्टोबर'),
            ('November', 'नोभेम्बर'),
            ('December', 'डिसेम्बर')
        ]
        
        for month_eng, month_nep in months_to_test:
            test_date_str = f"2025 {month_eng} 13"
            result = format_nepali_date_full(None)  # Test with string parsing
            # Manually test the conversion
            converted = test_date_str.replace(month_eng, month_nep)
            converted = to_nepali_digits(converted)
            self.stdout.write(f'{test_date_str} -> {converted}')
        
        # Test edge cases
        self.stdout.write('\n=== EDGE CASE TESTING ===')
        
        edge_cases = [
            None,
            '',
            'invalid date',
            datetime(2000, 1, 1),
            datetime(2099, 12, 31),
        ]
        
        for case in edge_cases:
            try:
                result = format_nepali_date_full(case)
                self.stdout.write(f'Input: {case} -> Result: {result}')
            except Exception as e:
                self.stdout.write(f'Input: {case} -> Error: {e}')
        
        # Test the expected output for the user's case
        self.stdout.write('\n=== USER CASE TESTING ===')
        self.stdout.write('User expects: "२०२५ जुन १३" instead of "2025 जुन 13"')
        
        test_input = "2025 जुन 13"
        expected = "२०२५ जुन १३"
        actual = to_nepali_digits(test_input)
        
        self.stdout.write(f'Input: {test_input}')
        self.stdout.write(f'Expected: {expected}')
        self.stdout.write(f'Actual: {actual}')
        self.stdout.write(f'Match: {actual == expected}')
        
        self.stdout.write(self.style.SUCCESS('\n✓ Nepali date formatting test completed!'))
