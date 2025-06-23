"""
Management command to create language demographics data based on actual data
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from apps.demographics.models import (
    MunicipalityWideMotherTonguePopulation,
    LanguageTypeChoice,
)
import uuid


class Command(BaseCommand):
    help = "Create language demographics data based on actual municipality-wide data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before creating new data",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write(self.style.WARNING("Clearing existing language data..."))
            MunicipalityWideMotherTonguePopulation.objects.all().delete()

        self.stdout.write(
            "Creating language demographics data based on actual municipality-wide data..."
        )

        # Use only the provided municipality-wide language sample data
        language_sample_data = [
            {
                "id": "12d794c2-6e6e-45ef-ac5c-efdb172ca8e9",
                "language_type": "ARABI",
                "population": 3,
            },
            {
                "id": "e0b8859c-3c64-4ed8-b1b8-78963ea42faa",
                "language_type": "AWADI",
                "population": 4425,
            },
            {
                "id": "6e5d2e5e-af84-4c28-b20d-e039f3b942eb",
                "language_type": "BAJJIKA",
                "population": 4,
            },
            {
                "id": "91940f8c-9cb4-4bd4-ba2d-5cdb940cfd48",
                "language_type": "BHOJPURI",
                "population": 10,
            },
            {
                "id": "f8748def-bbfb-443e-89b8-54c72fe2661a",
                "language_type": "BOTE",
                "population": 95,
            },
            {
                "id": "3f847e82-9813-46e3-adf8-9333a79b87eb",
                "language_type": "DOTELI",
                "population": 9,
            },
            {
                "id": "d887dbf8-d7f6-493d-a425-6d8c44e32b69",
                "language_type": "GURUNG",
                "population": 67,
            },
            {
                "id": "1f5f67de-d601-4b57-8cc6-696087812f44",
                "language_type": "HINDI",
                "population": 440,
            },
            {
                "id": "ae9a1840-0f5a-4750-885c-49a06881a6b3",
                "language_type": "KHAM",
                "population": 162,
            },
            {
                "id": "8be37094-2e92-4403-abd5-851bc0273c56",
                "language_type": "KHARIYA",
                "population": 4,
            },
            {
                "id": "a6631fc3-79c6-44d3-9846-bf75f62019b5",
                "language_type": "KUMAL",
                "population": 1263,
            },
            {
                "id": "478e31b2-9fab-46b5-a15d-f4b3a5345371",
                "language_type": "MAGAR",
                "population": 1165,
            },
            {
                "id": "6c1a885e-a788-4c77-aca4-4fd37fd2d844",
                "language_type": "MAITHILI",
                "population": 10,
            },
            {
                "id": "ad383e40-9aee-48f3-ba15-883522b2f42a",
                "language_type": "MAJHI",
                "population": 21,
            },
            {
                "id": "bbec91ca-da3a-42bc-9c07-4d3b3a8a4d95",
                "language_type": "MUSALMAN",
                "population": 116,
            },
            {
                "id": "d5241ecf-40b6-4017-940e-8fecffbf10cb",
                "language_type": "NEPALI",
                "population": 20143,
            },
            {
                "id": "c6abbe37-b9eb-451e-845c-bed57d49a23a",
                "language_type": "NEWARI",
                "population": 8,
            },
            {
                "id": "13bf9c0a-1512-468b-b049-b1fa5f78556f",
                "language_type": "RAI",
                "population": 13,
            },
            {
                "id": "7b5a4b59-0186-4e9d-8573-4bb5294c231f",
                "language_type": "SUNUWAR",
                "population": 66,
            },
            {
                "id": "79e359f7-3f1c-4780-80f9-3345bcff03ba",
                "language_type": "SYMBOLIC_LANGUAGE",
                "population": 4,
            },
            {
                "id": "3d15140f-1081-4ffd-a1d9-5546d20d028e",
                "language_type": "TAMANG",
                "population": 25,
            },
            {
                "id": "056e3bb9-df13-40e6-96cc-edd167307bea",
                "language_type": "THARU",
                "population": 19819,
            },
            {
                "id": "7c29af6b-317e-483c-a6d0-1adcdf2ceaac",
                "language_type": "URDU",
                "population": 57,
            },
        ]

        # Remove all previous language data (if any)
        MunicipalityWideMotherTonguePopulation.objects.all().delete()

        # Create language records using Django ORM
        created_count = 0
        with transaction.atomic():
            for entry in language_sample_data:
                obj, created = (
                    MunicipalityWideMotherTonguePopulation.objects.get_or_create(
                        language=entry["language_type"],
                        defaults={
                            "id": entry["id"],
                            "population": entry["population"],
                        },
                    )
                )
                if created:
                    created_count += 1
                    self.stdout.write(
                        f"Created: {entry['language_type']} ({entry['population']} people)"
                    )
                else:
                    obj.population = entry["population"]
                    obj.save()
                    self.stdout.write(
                        f"Updated: {entry['language_type']} ({entry['population']} people)"
                    )

        total_records = MunicipalityWideMotherTonguePopulation.objects.count()
        total_population = sum(
            MunicipalityWideMotherTonguePopulation.objects.values_list(
                "population", flat=True
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nSuccessfully processed {len(language_sample_data)} language demographic records "
                f"({created_count} new, {len(language_sample_data) - created_count} updated)\n"
                f"Total records in database: {total_records}\n"
                f"Total population covered: {total_population:,} people"
            )
        )

        # Print language breakdown
        self.stdout.write("\nLanguage breakdown:")
        for entry in language_sample_data:
            language_code = entry["language_type"]
            language_population = entry["population"]
            try:
                language_obj = MunicipalityWideMotherTonguePopulation.objects.get(
                    language=language_code
                )
                language_pop = language_obj.population
                percentage = language_pop / total_population * 100
                self.stdout.write(
                    f"  {language_code}: {language_pop:,} ({percentage:.2f}%)"
                )
            except MunicipalityWideMotherTonguePopulation.DoesNotExist:
                self.stdout.write(f"  {language_code}: 0 (0.00%)")
