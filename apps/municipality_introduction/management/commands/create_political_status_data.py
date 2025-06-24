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

        # New detailed ward-wise political status data
        raw_political_data = [
            {
                "id": "0802de4b-62ba-4cdf-a5bd-b7ff98543b3b",
                "ward_number": 1,
                "ward_name": "गोवरडिहा(१,२,३)",
                "year": 2078,
                "total_population": 7561,
                "male_population": 3619,
                "female_population": 3942,
                "other_population": None,
                "total_households": 1688,
                "average_household_size": "4.48",
                "sex_ratio": "91.81",
            },
            {
                "id": "c5562f44-43bd-48ed-b14a-e9fb050e5456",
                "ward_number": 2,
                "ward_name": "गोवरडिहा(४-६)",
                "year": 2078,
                "total_population": 5596,
                "male_population": 2754,
                "female_population": 2842,
                "other_population": None,
                "total_households": 1169,
                "average_household_size": "4.79",
                "sex_ratio": "96.9",
            },
            {
                "id": "c5b844fa-047b-4d8b-b2c2-b8b58647fe39",
                "ward_number": 3,
                "ward_name": "गोवरडिहा(७,८,९)",
                "year": 2078,
                "total_population": 5049,
                "male_population": 2439,
                "female_population": 2610,
                "other_population": None,
                "total_households": 1135,
                "average_household_size": "4.45",
                "sex_ratio": "93.45",
            },
            {
                "id": "87f2408e-7918-463a-9088-72bccf815d6d",
                "ward_number": 4,
                "ward_name": "गँगापरस्पुर(१,२,३,५)",
                "year": 2078,
                "total_population": 5983,
                "male_population": 2971,
                "female_population": 3012,
                "other_population": None,
                "total_households": 1265,
                "average_household_size": "4.73",
                "sex_ratio": "98.64",
            },
            {
                "id": "eeeb0192-122a-41ab-99fa-13df1dc9fc79",
                "ward_number": 5,
                "ward_name": "गँगापरस्पुर(४,६,७,८,९)",
                "year": 2078,
                "total_population": 6901,
                "male_population": 3374,
                "female_population": 3527,
                "other_population": None,
                "total_households": 1482,
                "average_household_size": "4.66",
                "sex_ratio": "95.66",
            },
            {
                "id": "610d2f3d-f16d-4846-a1b3-fdcfd9321db9",
                "ward_number": 6,
                "ward_name": "गढवा(१,२,३,४,५)",
                "year": 2078,
                "total_population": 7847,
                "male_population": 3819,
                "female_population": 4028,
                "other_population": None,
                "total_households": 1714,
                "average_household_size": "4.58",
                "sex_ratio": "94.81",
            },
            {
                "id": "7c7b50eb-b05d-49bf-a788-c35171142534",
                "ward_number": 7,
                "ward_name": "गढवा(६,७,८,९)",
                "year": 2078,
                "total_population": 6111,
                "male_population": 2925,
                "female_population": 3186,
                "other_population": None,
                "total_households": 1320,
                "average_household_size": "4.63",
                "sex_ratio": "91.81",
            },
            {
                "id": "b6259c7e-e2e1-4ad3-9084-5a529b81ef89",
                "ward_number": 8,
                "ward_name": "कोइलाबास(१ देखि ९)",
                "year": 2078,
                "total_population": 850,
                "male_population": 407,
                "female_population": 443,
                "other_population": None,
                "total_households": 191,
                "average_household_size": "4.45",
                "sex_ratio": "91.87",
            },
            {
                "id": "46a556ba-4742-4ad4-a2f2-07a5fe6d8c85",
                "ward_number": 1,
                "ward_name": "गोवरडिहा(१,२,३)",
                "year": 2081,
                "total_population": 7775,
                "male_population": 3720,
                "female_population": 4052,
                "other_population": 3,
                "total_households": 1735,
                "average_household_size": "4.481268011527377",
                "sex_ratio": "108.92473118279571",
            },
            {
                "id": "2ec0930c-60ae-4729-807e-dc646984421f",
                "ward_number": 2,
                "ward_name": "गोवरडिहा(४-६)",
                "year": 2081,
                "total_population": 5824,
                "male_population": 2902,
                "female_population": 2921,
                "other_population": 1,
                "total_households": 1201,
                "average_household_size": "4.849292256452956",
                "sex_ratio": "100.65472088215024",
            },
            {
                "id": "f98a5a1c-4bba-4f4f-983e-f3d259e37ebf",
                "ward_number": 3,
                "ward_name": "गोवरडिहा(७,८,९)",
                "year": 2081,
                "total_population": 5784,
                "male_population": 2912,
                "female_population": 2872,
                "other_population": 0,
                "total_households": 1294,
                "average_household_size": "4.469860896445131",
                "sex_ratio": "98.62637362637363",
            },
            {
                "id": "ddf24091-7c67-405d-81ef-18e8859df505",
                "ward_number": 4,
                "ward_name": "गँगापरस्पुर(१,२,३,५)",
                "year": 2081,
                "total_population": 6151,
                "male_population": 3054,
                "female_population": 3096,
                "other_population": 1,
                "total_households": 1300,
                "average_household_size": "4.731538461538461",
                "sex_ratio": "101.37524557956779",
            },
            {
                "id": "7dca4979-703a-48f5-b502-22c020efc7fc",
                "ward_number": 5,
                "ward_name": "गँगापरस्पुर(४,६,७,८,९)",
                "year": 2081,
                "total_population": 7168,
                "male_population": 3541,
                "female_population": 3625,
                "other_population": 2,
                "total_households": 1522,
                "average_household_size": "4.709592641261498",
                "sex_ratio": "102.37221123976279",
            },
            {
                "id": "36d509a4-3e31-4c67-b500-1d1904c1be9b",
                "ward_number": 6,
                "ward_name": "गढवा(१,२,३,४,५)",
                "year": 2081,
                "total_population": 8069,
                "male_population": 3926,
                "female_population": 4140,
                "other_population": 3,
                "total_households": 1761,
                "average_household_size": "4.58205565019875",
                "sex_ratio": "105.4508405501783",
            },
            {
                "id": "a1fbdd9b-d6f5-4298-9158-757cfb56deb6",
                "ward_number": 7,
                "ward_name": "गढवा(६,७,८,९)",
                "year": 2081,
                "total_population": 6285,
                "male_population": 3007,
                "female_population": 3275,
                "other_population": 3,
                "total_households": 1357,
                "average_household_size": "4.631540162122329",
                "sex_ratio": "108.91253741270368",
            },
            {
                "id": "3732eb49-5270-4895-bdb9-febbe988b12a",
                "ward_number": 8,
                "ward_name": "कोइलाबास(१ देखि ९)",
                "year": 2081,
                "total_population": 873,
                "male_population": 418,
                "female_population": 455,
                "other_population": 0,
                "total_households": 196,
                "average_household_size": "4.454081632653061",
                "sex_ratio": "108.85167464114834",
            },
        ]

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
            for data in raw_political_data:
                # Only use valid model fields
                valid_data = {
                    "id": data["id"],
                    "ward_number": data["ward_number"],
                    "ward_name": data["ward_name"],
                    "year": data["year"],
                    "population": data[
                        "total_population"
                    ],  # Map total_population to population
                }
                obj, created = PoliticalStatus.objects.get_or_create(
                    ward_number=valid_data["ward_number"],
                    year=valid_data["year"],
                    defaults=valid_data,
                )
                if not created:
                    for k, v in valid_data.items():
                        setattr(obj, k, v)
                    obj.save()
                if created:
                    created_count += 1
                    self.stdout.write(
                        f"Created: Ward {data['ward_number']} ({data['year']}) - {data['total_population']} population"
                    )
                else:
                    self.stdout.write(
                        f"Updated: Ward {data['ward_number']} ({data['year']}) - {data['total_population']} population"
                    )

        total_records = PoliticalStatus.objects.count()
        total_population = sum(
            PoliticalStatus.objects.values_list("population", flat=True)
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nSuccessfully processed {len(raw_political_data)} political status records "
                f"({created_count} new, {len(raw_political_data) - created_count} updated)\n"
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
