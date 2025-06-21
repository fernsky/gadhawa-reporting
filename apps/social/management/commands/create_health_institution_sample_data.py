"""
Management command to create health institution sample data

This command creates comprehensive sample data for health institutions
based on the provided JSON data structure for Section 5.2.1.
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from apps.social.models import WardWiseHealthInstitution, HealthInstitutionTypeChoice


class Command(BaseCommand):
    help = "Create sample data for Health Institution Details (५.२.१)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete existing data before creating new data",
        )

    def handle(self, *args, **options):
        if options["reset"]:
            self.stdout.write("Clearing existing health institution data...")
            WardWiseHealthInstitution.objects.all().delete()

        self.stdout.write(
            "Creating health institution sample data based on actual data..."
        )

        # Sample data representing actual health institutions
        health_institution_data = [
            {"s_n": 1, "name": "पाङ लुङ्ग्री चौकी", "ward_number": 1},
            {"s_n": 2, "name": "सिर्प लुङ्ग्री चौकी", "ward_number": 2},
            {"s_n": 3, "name": "बडाचौर लुङ्ग्री चौकी", "ward_number": 5},
            {"s_n": 4, "name": "गुम्चाल लुङ्ग्री चौकी", "ward_number": 6},
            {"s_n": 5, "name": "हार्जङ लुङ्ग्री चौकी", "ward_number": 7},
            {"s_n": 6, "name": "आ.स्वा.से.के.जुतुङखोला", "ward_number": 3},
            {"s_n": 7, "name": "आ.स्वा.से.के.नम्जा", "ward_number": 4},
            {"s_n": 8, "name": "सा.स्वा.इकाइ हार्जङ", "ward_number": 7},
            {"s_n": 9, "name": "सा.स्वा.इकाइ गोठेखर्क", "ward_number": 5},
            {"s_n": 10, "name": "सा.स्वा.इकाइ तल्लो सेवार", "ward_number": 5},
            {"s_n": 11, "name": "सा.स्वा.इकाइ पातेगुम्चाल", "ward_number": 6},
            {"s_n": 12, "name": "सा.स्वा.इकाइ बेरी", "ward_number": 6},
            {"s_n": 13, "name": "सा.स्वा.इकाइ गोठिबाङ", "ward_number": 5},
            {"s_n": 14, "name": "सा.स्वा.इकाइ लालुवाङ", "ward_number": 5},
            {"s_n": 15, "name": "सा.स्वा.इकाइ तल्लो सिर्प", "ward_number": 2},
            {"s_n": 16, "name": "सा.स्वा.इकाइ सिम्लेनी", "ward_number": 3},
            {"s_n": 17, "name": "सा.स्वा.इकाइ गोठेचौर", "ward_number": 3},
            {"s_n": 18, "name": "सा.स्वा.इकाइ पाङ", "ward_number": 1},
            {"s_n": 19, "name": "सा.स्वा.इकाइ ऐपे", "ward_number": 1},
            {"s_n": 20, "name": "सा.स्वा.इकाइ सालडाडाँ", "ward_number": 4},
        ]

        # Create health institutions
        with transaction.atomic():
            for institution_data in health_institution_data:
                health_institution = WardWiseHealthInstitution(
                    ward_number=institution_data["ward_number"],
                    name=institution_data["name"],
                    # institution_type will be auto-determined by the model's save method
                )
                health_institution.save()

                self.stdout.write(
                    f"Created: {health_institution.name} (वडा {health_institution.ward_number}) - {health_institution.get_institution_type_display()}"
                )

        self.stdout.write("Creating health institution summary for analysis...")

        self.generate_summary()

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {len(health_institution_data)} health institution records"
            )
        )

    def generate_summary(self):
        """Generate and display summary statistics"""
        total_institutions = WardWiseHealthInstitution.objects.count()

        # Count by institution type
        type_counts = {}
        for choice in HealthInstitutionTypeChoice:
            count = WardWiseHealthInstitution.objects.filter(
                institution_type=choice.value
            ).count()
            if count > 0:
                type_counts[choice.label] = count

        # Count by ward
        ward_counts = {}
        for ward in range(1, 8):  # Assuming 7 wards
            count = WardWiseHealthInstitution.objects.filter(ward_number=ward).count()
            if count > 0:
                ward_counts[f"वडा {ward}"] = count

        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("HEALTH INSTITUTION SUMMARY")
        self.stdout.write("=" * 60)
        self.stdout.write(f"Total Health Institutions: {total_institutions}")

        self.stdout.write(f"\nBy Institution Type:")
        for type_name, count in type_counts.items():
            self.stdout.write(f"  {type_name}: {count}")

        self.stdout.write(f"\nBy Ward:")
        for ward_name, count in ward_counts.items():
            self.stdout.write(f"  {ward_name}: {count}")

        self.stdout.write("=" * 60)
