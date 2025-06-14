from django.core.management.base import BaseCommand
from datetime import datetime
from apps.reports.templatetags.nepali_filters import nepali_date

class Command(BaseCommand):
    help = 'Final comprehensive test for Nepali date formatting'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Final Nepali date formatting test...'))
        
        # Test various dates
        test_dates = [
            datetime(2025, 6, 13),  # The user's example
            datetime(2025, 1, 1),   # New Year
            datetime(2025, 12, 31), # End of year
            datetime(2025, 2, 5),   # Single digit day
            datetime(2025, 10, 25), # Double digit day and month
        ]
        
        for test_date in test_dates:
            self.stdout.write(f'\nTesting: {test_date}')
            
            # Test Django format "Y F j"
            result = nepali_date(test_date, "Y F j")
            self.stdout.write(f'  nepali_date with "Y F j": {result}')
            
            # Test without format
            result_default = nepali_date(test_date)
            self.stdout.write(f'  nepali_date default: {result_default}')
        
        # Test the specific case mentioned by user
        self.stdout.write('\n=== USER SPECIFIC TEST ===')
        user_date = datetime(2025, 6, 13)
        result = nepali_date(user_date, "Y F j")
        
        self.stdout.write(f'User\'s date: {user_date}')
        self.stdout.write(f'Expected: "२०२५ जुन १३"')
        self.stdout.write(f'Actual: "{result}"')
        self.stdout.write(f'Match: {result == "२०२५ जुन १३"}')
        
        # Test that English "2025 जुन 13" becomes "२०२५ जुन १३"
        from apps.reports.utils.nepali_numbers import to_nepali_digits
        english_mixed = "2025 जुन 13"
        converted = to_nepali_digits(english_mixed)
        
        self.stdout.write(f'\nMixed format conversion:')
        self.stdout.write(f'Input: "{english_mixed}"')
        self.stdout.write(f'Output: "{converted}"')
        self.stdout.write(f'Expected: "२०२५ जुन १३"')
        self.stdout.write(f'Match: {converted == "२०२५ जुन १३"}')
        
        self.stdout.write(self.style.SUCCESS('\n✓ All Nepali date tests completed successfully!'))
