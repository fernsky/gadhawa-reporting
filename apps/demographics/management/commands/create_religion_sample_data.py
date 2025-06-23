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

        # Updated raw ward-wise religion data from user-provided sample
        raw_ward_data = [
            (1, "BUDDHIST", 47),
            (1, "CHRISTIAN", 86),
            (1, "HINDU", 7625),
            (1, "ISLAM", 13),
            (1, "NATURE", 4),
            (2, "CHRISTIAN", 233),
            (2, "HINDU", 5584),
            (2, "SIKH", 7),
            (3, "BUDDHIST", 5),
            (3, "CHRISTIAN", 352),
            (3, "HINDU", 5407),
            (3, "ISLAM", 13),
            (3, "JAIN", 1),
            (3, "NATURE", 3),
            (3, "SIKH", 3),
            (4, "CHRISTIAN", 158),
            (4, "HINDU", 5695),
            (4, "ISLAM", 274),
            (4, "SIKH", 24),
            (5, "CHRISTIAN", 348),
            (5, "HINDU", 6663),
            (5, "ISLAM", 141),
            (5, "KIRANT", 3),
            (5, "NATURE", 13),
            (6, "BON", 10),
            (6, "CHRISTIAN", 260),
            (6, "HINDU", 7349),
            (6, "ISLAM", 425),
            (6, "NATURE", 25),
            (7, "BON", 14),
            (7, "CHRISTIAN", 201),
            (7, "HINDU", 6055),
            (7, "JAIN", 8),
            (7, "SIKH", 7),
            (8, "BUDDHIST", 12),
            (8, "CHRISTIAN", 15),
            (8, "HINDU", 553),
            (8, "ISLAM", 293),
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
