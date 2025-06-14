"""
Management command to check current categories and sections in the database
"""
from django.core.management.base import BaseCommand
from apps.reports.models import ReportCategory, ReportSection

class Command(BaseCommand):
    help = 'Check current categories and sections in the database'

    def handle(self, *args, **options):
        self.stdout.write("🔍 Checking current database content...")
        
        categories = ReportCategory.objects.all()
        sections = ReportSection.objects.all()
        
        self.stdout.write(f"\n📊 Found {categories.count()} categories:")
        for i, category in enumerate(categories, 1):
            self.stdout.write(f"  {i}. English: '{category.name}'")
            self.stdout.write(f"     Nepali: '{category.name_nepali or 'NOT SET'}'")
            self.stdout.write(f"     Active: {category.is_active}")
            self.stdout.write(f"     Order: {category.order}")
            self.stdout.write("")
        
        self.stdout.write(f"📝 Found {sections.count()} sections:")
        for i, section in enumerate(sections[:10], 1):  # Show only first 10
            self.stdout.write(f"  {i}. English: '{section.title}'")
            self.stdout.write(f"     Nepali: '{section.title_nepali or 'NOT SET'}'")
            self.stdout.write(f"     Category: {section.category.name if section.category else 'No category'}")
            self.stdout.write("")
        
        if sections.count() > 10:
            self.stdout.write(f"     ... and {sections.count() - 10} more sections")
        
        if not categories.exists():
            self.stdout.write(self.style.WARNING("⚠️  No categories found! Creating sample data..."))
            self.call_command('populate_nepali_translations')
        
        self.stdout.write(self.style.SUCCESS("✅ Database check completed!"))
