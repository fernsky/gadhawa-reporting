"""
Management command to create political status data based on actual data
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from apps.municipality_introduction.models import PoliticalStatus
import uuid


class Command(BaseCommand):
    help = "Create political status data based on actual municipality-wide data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before creating new data",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write(
                self.style.WARNING("Clearing existing political status data...")
            )
            PoliticalStatus.objects.all().delete()

        self.stdout.write(
            "Creating political status data based on actual municipality data..."
        )

        # Raw ward-wise political status data from actual records
        raw_political_data = [
            (1, "पाङ(१-९)", 2078, 5451),
            (2, "सिर्प(१,२,४,६,८,९)", 2078, 3885),
            (3, "सिर्प(३,५,७)", 2078, 2950),
            (4, "बडाचौर (१-३,७) सिर्प (९)", 2078, 3794),
            (5, "बडाचौर(४-६,८,९)", 2078, 3314),
            (6, "गुम्म्चाल(१-९)", 2078, 4389),
            (7, "हारजङ(१-९)", 2078, 2542),
            (6, "गुम्म्चाल(१-९)", 2081, 4511),
            (3, "सिर्प(३,५,७)", 2081, 3038),
            (5, "बडाचौर(४-६,८,९)", 2081, 3406),
            (1, "पाङ(१-९)", 2081, 5603),
            (7, "हारजङ(१-९)", 2081, 2613),
            (2, "सिर्प(१,२,४,६,८,९)", 2081, 4265),
            (4, "बडाचौर (१-३,७) सिर्प (९)", 2081, 4059),
        ]

        # Convert to the format expected by the model
        political_data = []
        for ward_number, ward_name, year, population in raw_political_data:
            political_data.append(
                {
                    "id": str(uuid.uuid4()),
                    "ward_number": ward_number,
                    "ward_name": ward_name,
                    "year": year,
                    "population": population,
                }
            )

        self.stdout.write(
            f"Processing {len(raw_political_data)} records for political status data..."
        )

        existing_count = PoliticalStatus.objects.count()
        if existing_count > 0 and not options["clear"]:
            self.stdout.write(
                self.style.WARNING(
                    f"Found {existing_count} existing records. Use --clear to replace them."
                )
            )
            return

        created_count = 0
        with transaction.atomic():
            for data in political_data:
                obj, created = PoliticalStatus.objects.get_or_create(
                    ward_number=data["ward_number"],
                    year=data["year"],
                    defaults={
                        "id": data["id"],
                        "ward_name": data["ward_name"],
                        "population": data["population"],
                    },
                )

                if created:
                    created_count += 1
                    self.stdout.write(
                        f"Created: Ward {data['ward_number']} ({data['year']}) - {data['population']} population"
                    )
                else:
                    obj.ward_name = data["ward_name"]
                    obj.population = data["population"]
                    obj.save()
                    self.stdout.write(
                        f"Updated: Ward {data['ward_number']} ({data['year']}) - {data['population']} population"
                    )

        total_records = PoliticalStatus.objects.count()
        total_population = sum(
            PoliticalStatus.objects.values_list("population", flat=True)
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nSuccessfully processed {len(political_data)} political status records "
                f"({created_count} new, {len(political_data) - created_count} updated)\n"
                f"Total records in database: {total_records}\n"
                f"Total population covered: {total_population:,} people"
            )
        )

        # Summary by year
        self.stdout.write("\nSummary by year:")
        for year in [2078, 2081]:
            year_records = PoliticalStatus.objects.filter(year=year)
            year_population = sum(year_records.values_list("population", flat=True))
            ward_count = year_records.count()
            self.stdout.write(
                f"  {year}: {ward_count} wards, {year_population:,} total population"
            )
