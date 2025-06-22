"""
Management command to create disability cause demographics data based on actual data
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db import models
from apps.demographics.models import WardWiseDisabilityCause
import uuid


class Command(BaseCommand):
    help = "Create disability cause demographics data based on actual municipality-wide data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before creating new data",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write(
                self.style.WARNING("Clearing existing disability cause data...")
            )
            WardWiseDisabilityCause.objects.all().delete()

        self.stdout.write(
            "Creating disability cause demographics data based on actual municipality-wide data..."
        )

        # Sample data representing actual disability cause patterns by ward
        disability_data = [
            # Ward 1
            {
                "id": "84bb751d-af1b-4a9e-a977-fce853431c03",
                "ward_number": 1,
                "disability_cause": "ACCIDENT",
                "population": 11,
            },
            {
                "id": "0c9a0b39-eb06-47d4-809d-8b744e8b7a8f",
                "ward_number": 1,
                "disability_cause": "CONGENITAL",
                "population": 55,
            },
            {
                "id": "3a435a50-4ca5-47bd-94fc-b72b34e0c5c6",
                "ward_number": 1,
                "disability_cause": "DISEASE",
                "population": 52,
            },
            {
                "id": "1f9340dd-b87b-4759-a27f-fe94cc27fdb2",
                "ward_number": 1,
                "disability_cause": "MALNUTRITION",
                "population": 2,
            },
            {
                "id": "cb5697a5-84ad-435f-8183-6799e62a779e",
                "ward_number": 1,
                "disability_cause": "OTHER",
                "population": 4,
            },
            {
                "id": "a26f7963-2a12-4776-a155-94af5f976950",
                "ward_number": 1,
                "disability_cause": "OTHER",
                "population": 69,
            },  # unknown mapped to OTHER
            # Ward 2
            {
                "id": "463e605a-fce1-41f6-9b95-f5e67e4fc918",
                "ward_number": 2,
                "disability_cause": "ACCIDENT",
                "population": 18,
            },
            {
                "id": "dc2a7b61-4024-46bb-ac14-7c3f3258025f",
                "ward_number": 2,
                "disability_cause": "CONGENITAL",
                "population": 43,
            },
            {
                "id": "f8b5f973-f4a9-431b-9a0c-efa8dcdecb26",
                "ward_number": 2,
                "disability_cause": "DISEASE",
                "population": 24,
            },
            {
                "id": "5c0e3c4f-d581-4b49-aab9-012f439cd109",
                "ward_number": 2,
                "disability_cause": "MALNUTRITION",
                "population": 2,
            },
            {
                "id": "d8241848-0da9-435d-8edf-972323c3c4a5",
                "ward_number": 2,
                "disability_cause": "OTHER",
                "population": 3,
            },
            {
                "id": "9bf7afec-57b4-482d-b304-e9640579b613",
                "ward_number": 2,
                "disability_cause": "OTHER",
                "population": 7,
            },  # unknown mapped to OTHER
            # Ward 3
            {
                "id": "7322676f-13a7-428d-82cf-1208012e0d65",
                "ward_number": 3,
                "disability_cause": "ACCIDENT",
                "population": 16,
            },
            {
                "id": "2d00c089-70c7-4459-90ca-7f6047ea78d3",
                "ward_number": 3,
                "disability_cause": "CONGENITAL",
                "population": 18,
            },
            {
                "id": "62b9859f-4244-430b-ad16-da9a2ecacde0",
                "ward_number": 3,
                "disability_cause": "DISEASE",
                "population": 13,
            },
            {
                "id": "8a029e6e-6e1b-4e74-8396-d23856700dab",
                "ward_number": 3,
                "disability_cause": "MALNUTRITION",
                "population": 1,
            },
            {
                "id": "c3d4cb6b-1ea3-4b57-bde4-7fc3abc0fa62",
                "ward_number": 3,
                "disability_cause": "OTHER",
                "population": 4,
            },  # unknown mapped to OTHER
            # Ward 4
            {
                "id": "d997892d-709d-4660-afb8-1452778024e8",
                "ward_number": 4,
                "disability_cause": "ACCIDENT",
                "population": 18,
            },
            {
                "id": "6764eb8d-9108-44e0-8b29-6166f3d0abe5",
                "ward_number": 4,
                "disability_cause": "CONFLICT",
                "population": 1,
            },
            {
                "id": "2f73f48e-5bf9-4260-b918-e8ac291be925",
                "ward_number": 4,
                "disability_cause": "CONGENITAL",
                "population": 26,
            },
            {
                "id": "fb79ae79-8234-460e-a24c-906fb5105523",
                "ward_number": 4,
                "disability_cause": "DISEASE",
                "population": 15,
            },
            {
                "id": "0d725a86-d3d0-475b-a0c4-8d15e3ac27a5",
                "ward_number": 4,
                "disability_cause": "MALNUTRITION",
                "population": 3,
            },
            {
                "id": "0c06504d-aea8-4681-9ad9-95607aa7cd26",
                "ward_number": 4,
                "disability_cause": "OTHER",
                "population": 4,
            },  # unknown mapped to OTHER
            # Ward 5
            {
                "id": "b88c2e09-3d59-41f3-af2c-726c72fd6711",
                "ward_number": 5,
                "disability_cause": "ACCIDENT",
                "population": 36,
            },
            {
                "id": "36ff0853-251d-4965-a840-17f510cacc5f",
                "ward_number": 5,
                "disability_cause": "CONFLICT",
                "population": 2,
            },
            {
                "id": "361f74c9-33c2-454b-81b1-04cc8bf833ff",
                "ward_number": 5,
                "disability_cause": "CONGENITAL",
                "population": 36,
            },
            {
                "id": "b9caf33f-6e7e-4b2f-81b9-bf1d7bd6cf20",
                "ward_number": 5,
                "disability_cause": "DISEASE",
                "population": 36,
            },
            {
                "id": "4798cb86-6cb9-450e-a915-1c3e304e1a79",
                "ward_number": 5,
                "disability_cause": "MALNUTRITION",
                "population": 2,
            },
            {
                "id": "07ac5161-0659-4afa-ba33-a0f059fcff83",
                "ward_number": 5,
                "disability_cause": "OTHER",
                "population": 7,
            },
            {
                "id": "a56f234b-3497-481c-8ff7-028cfba7bf5c",
                "ward_number": 5,
                "disability_cause": "OTHER",
                "population": 36,
            },  # unknown mapped to OTHER
            # Ward 6
            {
                "id": "f10cf7c2-bb42-4f39-8673-87502ac2fdc7",
                "ward_number": 6,
                "disability_cause": "ACCIDENT",
                "population": 4,
            },
            {
                "id": "430c7ffa-2a19-4a82-affd-964f3752f778",
                "ward_number": 6,
                "disability_cause": "CONFLICT",
                "population": 2,
            },
            {
                "id": "8fd478f0-566c-49b2-87b2-b5aa3e9453ff",
                "ward_number": 6,
                "disability_cause": "CONGENITAL",
                "population": 27,
            },
            {
                "id": "b7501919-11a2-4295-bdfa-b72871edd8eb",
                "ward_number": 6,
                "disability_cause": "DISEASE",
                "population": 9,
            },
            {
                "id": "97376caa-9574-4c07-8288-191e8e190d83",
                "ward_number": 6,
                "disability_cause": "OTHER",
                "population": 12,
            },  # unknown mapped to OTHER
            # Ward 7
            {
                "id": "4031562d-fd0b-431f-af5e-ae671a54d770",
                "ward_number": 7,
                "disability_cause": "ACCIDENT",
                "population": 48,
            },
            {
                "id": "274584e1-302a-4077-80db-172aa84b779d",
                "ward_number": 7,
                "disability_cause": "CONFLICT",
                "population": 1,
            },
            {
                "id": "cbcdac07-4e4f-4325-939c-25fa9dc315be",
                "ward_number": 7,
                "disability_cause": "CONGENITAL",
                "population": 36,
            },
            {
                "id": "b2e58d38-ba2a-4c36-bb8e-49fbfbed8904",
                "ward_number": 7,
                "disability_cause": "DISEASE",
                "population": 44,
            },
            {
                "id": "1de7af53-0708-4134-8dfa-5c48bbc7f090",
                "ward_number": 7,
                "disability_cause": "OTHER",
                "population": 2,
            },
            {
                "id": "114222a9-0cc8-4652-90a5-af5fa902446c",
                "ward_number": 7,
                "disability_cause": "OTHER",
                "population": 32,
            },  # unknown mapped to OTHER
        ]

        existing_count = WardWiseDisabilityCause.objects.count()
        if existing_count > 0 and not options["clear"]:
            self.stdout.write(
                self.style.WARNING(
                    f"Found {existing_count} existing records. Use --clear to replace them."
                )
            )
            return

        created_count = 0
        with transaction.atomic():
            for data in disability_data:
                obj, created = WardWiseDisabilityCause.objects.get_or_create(
                    ward_number=data["ward_number"],
                    disability_cause=data["disability_cause"],
                    defaults={
                        "id": data["id"],
                        "population": data["population"],
                    },
                )

                if created:
                    created_count += 1
                    self.stdout.write(
                        f"Created: Ward {data['ward_number']} - {data['disability_cause']} ({data['population']} people)"
                    )
                else:
                    obj.population = data["population"]
                    obj.save()
                    self.stdout.write(
                        f"Updated: Ward {data['ward_number']} - {data['disability_cause']} ({data['population']} people)"
                    )

        total_records = WardWiseDisabilityCause.objects.count()
        total_population = sum(
            WardWiseDisabilityCause.objects.values_list("population", flat=True)
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nSuccessfully processed {len(disability_data)} disability cause demographic records "
                f"({created_count} new, {len(disability_data) - created_count} updated)\n"
                f"Total records in database: {total_records}\n"
                f"Total population covered: {total_population:,} people"
            )
        )

        # Calculate and display disability cause-wise summary
        self.stdout.write("\nDisability cause-wise summary:")
        disability_totals = {}
        for cause in [
            "ACCIDENT",
            "CONGENITAL",
            "DISEASE",
            "MALNUTRITION",
            "CONFLICT",
            "OTHER",
        ]:
            cause_population = (
                WardWiseDisabilityCause.objects.filter(
                    disability_cause=cause
                ).aggregate(total=models.Sum("population"))["total"]
                or 0
            )
            disability_totals[cause] = cause_population

            if cause_population > 0:
                percentage = cause_population / total_population * 100
                self.stdout.write(
                    f"  {cause}: {cause_population:,} people ({percentage:.2f}%)"
                )

        # Ward-wise summary
        self.stdout.write("\nWard-wise disability cause summary:")
        for ward_num in range(1, 8):  # Wards 1-7 based on data
            ward_population = (
                WardWiseDisabilityCause.objects.filter(ward_number=ward_num).aggregate(
                    total=models.Sum("population")
                )["total"]
                or 0
            )
            if ward_population > 0:
                self.stdout.write(f"  वडा {ward_num}: {ward_population:,} people")
