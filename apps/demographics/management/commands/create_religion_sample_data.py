"""
Management command to create religion demographics data based on actual data
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db import models
from django.utils import timezone
from apps.demographics.models import (
    MunicipalityWideReligionPopulation,
    ReligionTypeChoice,
)
import uuid


class Command(BaseCommand):
    help = "Create religion demographics data based on actual municipality-wide data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before creating new data",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write(self.style.WARNING("Clearing existing religion data..."))
            MunicipalityWideReligionPopulation.objects.all().delete()

        self.stdout.write(
            "Creating religion demographics data based on actual municipality-wide data..."
        )

        # Raw ward-wise religion data from actual census
        raw_ward_data = [
            (1, "CHRISTIAN", 35),
            (1, "HINDU", 5533),
            (1, "NATURE", 35),
            (2, "HINDU", 4265),
            (3, "BUDDHIST", 12),
            (3, "CHRISTIAN", 46),
            (3, "HINDU", 2980),
            (4, "HINDU", 4050),
            (4, "NATURE", 9),
            (5, "HINDU", 3406),
            (6, "BUDDHIST", 20),
            (6, "HINDU", 4491),
            (7, "BUDDHIST", 45),
            (7, "CHRISTIAN", 40),
            (7, "HINDU", 2506),
            (7, "NATURE", 22),
        ]

        # Aggregate data by religion for municipality-wide totals
        religion_totals = {}
        for ward, religion, population in raw_ward_data:
            if religion not in religion_totals:
                religion_totals[religion] = 0
            religion_totals[religion] += population

        # Convert to the format expected by the rest of the code
        religion_data = []
        for religion_enum, total_population in religion_totals.items():
            religion_data.append(
                {
                    "id": str(uuid.uuid4()),
                    "religion": religion_enum,
                    "population": total_population,
                }
            )

        self.stdout.write(
            f"Processing {len(raw_ward_data)} ward-level records into {len(religion_data)} municipality-wide religion categories..."
        )

        # Check if data already exists
        existing_count = MunicipalityWideReligionPopulation.objects.count()
        if existing_count > 0 and not options["clear"]:
            self.stdout.write(
                self.style.WARNING(
                    f"Found {existing_count} existing records. Use --clear to replace them."
                )
            )
            return

        # Create records using Django ORM
        created_count = 0
        with transaction.atomic():
            for data in religion_data:
                # Create the record with the specified ID
                obj, created = MunicipalityWideReligionPopulation.objects.get_or_create(
                    religion=data["religion"],
                    defaults={
                        "id": data["id"],
                        "population": data["population"],
                    },
                )

                if created:
                    created_count += 1
                    self.stdout.write(
                        f"Created: {data['religion']} ({data['population']} people)"
                    )
                else:
                    # Update existing record
                    obj.population = data["population"]
                    obj.save()
                    self.stdout.write(
                        f"Updated: {data['religion']} ({data['population']} people)"
                    )

        # Print summary
        total_records = MunicipalityWideReligionPopulation.objects.count()
        total_population = sum(
            MunicipalityWideReligionPopulation.objects.values_list(
                "population", flat=True
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nSuccessfully processed {len(religion_data)} religion demographic records "
                f"({created_count} new, {len(religion_data) - created_count} updated)\n"
                f"Total records in database: {total_records}\n"
                f"Total population covered: {total_population:,} people"
            )
        )

        # Print religion breakdown
        self.stdout.write("\nReligion breakdown:")
        for religion_choice in ReligionTypeChoice.choices:
            religion_code = religion_choice[0]
            religion_name = religion_choice[1]
            try:
                religion_obj = MunicipalityWideReligionPopulation.objects.get(
                    religion=religion_code
                )
                religion_pop = religion_obj.population
                percentage = religion_pop / total_population * 100
                self.stdout.write(
                    f"  {religion_name}: {religion_pop:,} ({percentage:.2f}%)"
                )
            except MunicipalityWideReligionPopulation.DoesNotExist:
                self.stdout.write(f"  {religion_name}: 0 (0.00%)")
