"""
Management command to test Nepali number conversion in templates
"""
from django.core.management.base import BaseCommand
from django.template import Context, Template
from apps.reports.templatetags.nepali_filters import (
    nepali_digits, nepali_number, nepali_percentage, 
    nepali_currency, nepali_ordinal_filter, nepali_file_size
)

class Command(BaseCommand):
    help = 'Test Nepali number conversion in Django templates'

    def handle(self, *args, **options):
        self.stdout.write("=== Testing Nepali Template Filters ===\n")
        
        # Test template with Nepali filters
        template_content = """
{% load nepali_filters %}
Number: {{ number|nepali_digits }}
Formatted: {{ number|nepali_number }}
Percentage: {{ percentage|nepali_percentage }}
Currency: {{ amount|nepali_currency }}
Ordinal: {{ position|nepali_ordinal_filter }}
File Size: {{ file_size|nepali_file_size }}
"""
        
        template = Template(template_content)
        context = Context({
            'number': 12345,
            'percentage': 78.5,
            'amount': 50000,
            'position': 3,
            'file_size': 1048576,  # 1MB in bytes
        })
        
        result = template.render(context)
        self.stdout.write("Template rendering result:")
        self.stdout.write(result)
        
        # Test individual filters
        self.stdout.write("\n=== Individual Filter Tests ===")
        
        test_cases = [
            ("nepali_digits", "123456", nepali_digits),
            ("nepali_number", 123456, nepali_number),
            ("nepali_percentage", 78.5, nepali_percentage),
            ("nepali_currency", 50000, nepali_currency),
            ("nepali_ordinal_filter", 5, nepali_ordinal_filter),
            ("nepali_file_size", 2048576, nepali_file_size),
        ]
        
        for filter_name, value, filter_func in test_cases:
            try:
                result = filter_func(value)
                self.stdout.write(f"{filter_name}({value}) → {result}")
            except Exception as e:
                self.stdout.write(f"ERROR in {filter_name}({value}): {e}")
        
        self.stdout.write("\n✅ Template filter testing completed")
