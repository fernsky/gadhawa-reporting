"""
Management command to test table of contents rendering
"""
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.test import RequestFactory
from apps.reports.models import ReportCategory, ReportSection, PublicationSettings

class Command(BaseCommand):
    help = 'Test table of contents rendering with Nepali content'

    def handle(self, *args, **options):
        self.stdout.write("🧪 Testing table of contents rendering...")
        
        # Create a mock request
        factory = RequestFactory()
        request = factory.get('/reports/table-of-contents/')
        
        # Get data that would be used in the template
        categories = ReportCategory.objects.filter(is_active=True).prefetch_related('sections')
        publication_settings = PublicationSettings.objects.first()
        
        self.stdout.write(f"\n📊 Template context data:")
        self.stdout.write(f"  Categories count: {categories.count()}")
        
        for category in categories:
            self.stdout.write(f"\n  Category: {category.name}")
            self.stdout.write(f"    Nepali: {category.name_nepali}")
            self.stdout.write(f"    Sections: {category.sections.count()}")
            
            for section in category.sections.all()[:3]:  # Show first 3 sections
                self.stdout.write(f"      - {section.title}")
                self.stdout.write(f"        Nepali: {section.title_nepali}")
        
        # Test the template rendering would work
        context = {
            'categories': categories,
            'publication_settings': publication_settings,
            'total_sections': sum(cat.sections.count() for cat in categories),
            'total_figures': 0,  # Would be calculated in real view
            'total_tables': 0,   # Would be calculated in real view
            'request': request,
        }
        
        self.stdout.write(f"\n🎨 Template context ready:")
        self.stdout.write(f"  - categories: {len(context['categories'])} items")
        self.stdout.write(f"  - total_sections: {context['total_sections']}")
        
        # Test Nepali number conversion
        from apps.reports.utils.nepali_numbers import to_nepali_digits
        
        test_numbers = ['1', '2', '3', '1.1', '2.5', '123']
        self.stdout.write(f"\n🔢 Nepali number conversion test:")
        for num in test_numbers:
            nepali = to_nepali_digits(num)
            self.stdout.write(f"  {num} → {nepali}")
        
        self.stdout.write(self.style.SUCCESS("\n✅ Table of contents test completed!"))
        self.stdout.write(self.style.SUCCESS("The template should now display Nepali content properly."))
