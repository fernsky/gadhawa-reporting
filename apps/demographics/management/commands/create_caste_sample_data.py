"""
Management command to create caste demographics data based on actual data
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from apps.demographics.models import MunicipalityWideCastePopulation, CasteTypeChoice
import uuid


class Command(BaseCommand):
    help = "Create caste demographics data based on actual municipality-wide data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before creating new data",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write(self.style.WARNING("Clearing existing caste data..."))
            MunicipalityWideCastePopulation.objects.all().delete()

        self.stdout.write(
            "Creating caste demographics data based on actual municipality-wide data..."
        )

        # Actual municipality-wide caste population data
        municipality_caste_data = [
            (3679, "कामी"),
            (12640, "क्षेत्री"),
            (196, "गुरुङ"),
            (6, "थकाली"),
            (600, "दमाई/ढोली"),
            (5, "नेवार"),
            (170, "ब्राह्मण पहाड"),
            (9819, "मगर"),
            (61, "माझी"),
            (160, "सार्की"),
            (159, "सुनार"),
        ]

        # Mapping Nepali caste names to specific model enum choices
        caste_mapping = {
            "कामी": "KAMI",  # Direct mapping to KAMI enum
            "क्षेत्री": "CHHETRI",
            "गुरुङ": "GURUNG",
            "थकाली": "THAKALI",  # Direct mapping to THAKALI enum
            "दमाई/ढोली": "DAMAI",  # Direct mapping to DAMAI enum
            "नेवार": "NEWAR",
            "ब्राह्मण पहाड": "BRAHMIN_HILL",  # Direct mapping to BRAHMIN_HILL enum
            "मगर": "MAGAR",
            "माझी": "MAJHI",  # Direct mapping to MAJHI enum
            "सार्की": "SARKI",  # Direct mapping to SARKI enum
            "सुनार": "SONAR",  # Direct mapping to SONAR enum
        }

        # Use direct municipality-wide data with specific caste enums
        caste_data = []
        for population, nepali_caste in municipality_caste_data:
            enum_caste = caste_mapping.get(nepali_caste, "OTHER")
            caste_data.append(
                {
                    "id": str(uuid.uuid4()),
                    "caste": enum_caste,
                    "population": population,
                }
            )

        self.stdout.write(
            f"Processing {len(municipality_caste_data)} municipality-wide caste records..."
        )

        existing_count = MunicipalityWideCastePopulation.objects.count()
        if existing_count > 0 and not options["clear"]:
            self.stdout.write(
                self.style.WARNING(
                    f"Found {existing_count} existing records. Use --clear to replace them."
                )
            )
            return

        created_count = 0
        with transaction.atomic():
            for data in caste_data:
                obj, created = MunicipalityWideCastePopulation.objects.get_or_create(
                    caste=data["caste"],
                    defaults={
                        "id": data["id"],
                        "population": data["population"],
                    },
                )

                if created:
                    created_count += 1
                    self.stdout.write(
                        f"Created: {data['caste']} ({data['population']} people)"
                    )
                else:
                    obj.population = data["population"]
                    obj.save()
                    self.stdout.write(
                        f"Updated: {data['caste']} ({data['population']} people)"
                    )

        total_records = MunicipalityWideCastePopulation.objects.count()
        total_population = sum(
            MunicipalityWideCastePopulation.objects.values_list("population", flat=True)
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nSuccessfully processed {len(caste_data)} caste demographic records "
                f"({created_count} new, {len(caste_data) - created_count} updated)\n"
                f"Total records in database: {total_records}\n"
                f"Total population covered: {total_population:,} people"
            )
        )

        self.stdout.write("\nCaste breakdown:")
        for caste_choice in CasteTypeChoice.choices:
            caste_code = caste_choice[0]
            caste_name = caste_choice[1]
            try:
                caste_obj = MunicipalityWideCastePopulation.objects.get(
                    caste=caste_code
                )
                caste_pop = caste_obj.population
                percentage = caste_pop / total_population * 100
                self.stdout.write(f"  {caste_name}: {caste_pop:,} ({percentage:.2f}%)")
            except MunicipalityWideCastePopulation.DoesNotExist:
                self.stdout.write(f"  {caste_name}: 0 (0.00%)")
