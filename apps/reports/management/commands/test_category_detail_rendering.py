from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.test import RequestFactory
from apps.reports.models import ReportCategory, ReportSection, ReportFigure, ReportTable
from apps.reports.templatetags.nepali_filters import nepali_digits
import json


class Command(BaseCommand):
    help = "Test category detail rendering with Nepali content"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Testing category detail rendering..."))

        # Get a test category with sections
        try:
            category = ReportCategory.objects.prefetch_related("sections").first()
            if not category:
                self.stdout.write(self.style.ERROR("No categories found in database"))
                return

            self.stdout.write(
                f"Testing category: {category.name} / {category.name_nepali}"
            )

            # Check category Nepali content
            self.stdout.write("\n=== CATEGORY CONTENT ===")
            self.stdout.write(f"English name: {category.name}")
            self.stdout.write(f"Nepali name: {category.name_nepali}")
            self.stdout.write(f"English description: {category.description}")
            self.stdout.write(f"Nepali description: {category.description_nepali}")

            # Check sections
            sections = category.sections.all()
            self.stdout.write(f"\n=== SECTIONS ({len(sections)} total) ===")

            for i, section in enumerate(sections, 1):
                self.stdout.write(f"\nSection {i}:")
                self.stdout.write(f"  English title: {section.title}")
                self.stdout.write(f"  Nepali title: {section.title_nepali}")
                self.stdout.write(f"  English description: {section.summary}")
                self.stdout.write(f"  Nepali description: {section.summary_nepali}")
                self.stdout.write(
                    f"  Section number: {section.section_number} / {nepali_digits(section.section_number)}"
                )

                # Check figures in this section
                figures = section.figures.all()
                if figures:
                    self.stdout.write(f"  Figures ({len(figures)}):")
                    for fig in figures:
                        self.stdout.write(
                            f"    - Figure {fig.figure_number} / {nepali_digits(fig.figure_number)}: {fig.title}"
                        )

                # Check tables in this section
                tables = section.tables.all()
                if tables:
                    self.stdout.write(f"  Tables ({len(tables)}):")
                    for table in tables:
                        self.stdout.write(
                            f"    - Table {table.table_number} / {nepali_digits(table.table_number)}: {table.title}"
                        )

            # Test template rendering (simplified)
            self.stdout.write("\n=== TEMPLATE TESTING ===")

            # Test the Nepali filters directly
            test_numbers = [1, 2, 3, 10, 15, 25, 100, 123]
            self.stdout.write("Number conversion tests:")
            for num in test_numbers:
                nepali_num = nepali_digits(num)
                self.stdout.write(f"  {num} -> {nepali_num}")

            # Create a mock request for template rendering
            factory = RequestFactory()
            request = factory.get(f"/reports/category/{category.slug}/")

            # Test context data that would be used in template
            context = {
                "category": category,
                "request": request,
                "municipality_name": "गढवा गाउँपालिका",
            }

            self.stdout.write("\n=== TEMPLATE CONTEXT TEST ===")
            self.stdout.write("Context variables that would be used in template:")
            self.stdout.write(
                f"  category.name_nepali|default:category.name = {category.name_nepali or category.name}"
            )
            self.stdout.write(
                f"  category.description_nepali|default:category.description = {category.description_nepali or category.description}"
            )

            for section in sections[:3]:  # Test first 3 sections
                title_display = section.title_nepali or section.title
                desc_display = section.summary_nepali or section.summary
                self.stdout.write(
                    f"  section.title_nepali|default:section.title = {title_display}"
                )
                self.stdout.write(
                    f"  section.summary_nepali|default:section.summary = {desc_display}"
                )

            self.stdout.write(
                self.style.SUCCESS("\n✓ Category detail rendering test completed!")
            )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error during testing: {str(e)}"))
            import traceback

            traceback.print_exc()
