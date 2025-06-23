"""
Management command to create disability cause demographics data based on latest actual data (wards 1-8, new cause keys, unknown mapped to OTHER)
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db import models
from apps.demographics.models import WardWiseDisabilityCause
import uuid


class Command(BaseCommand):
    help = "Create disability cause demographics data based on latest actual municipality-wide data (wards 1-8, new cause keys, unknown mapped to OTHER)"

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
            "Creating disability cause demographics data based on latest actual municipality-wide data (wards 1-8, new cause keys, unknown mapped to OTHER)..."
        )

        # Latest sample data (wards 1-8, new cause keys, unknown mapped to OTHER)
        disability_data = [
            {
                "id": "80d8bcf1-f4da-4f9c-8943-c8815bc288c9",
                "ward_number": 1,
                "disability_cause": "accident",
                "population": 24,
            },
            {
                "id": "39021dfc-7b78-4b24-8a34-d98748d706fe",
                "ward_number": 1,
                "disability_cause": "congenital",
                "population": 40,
            },
            {
                "id": "c5ba2f34-565b-4ec4-bd88-616a9d3eae7a",
                "ward_number": 1,
                "disability_cause": "disease",
                "population": 34,
            },
            {
                "id": "ea7fdaaa-7d39-4211-99f1-f0064c8261ff",
                "ward_number": 1,
                "disability_cause": "other",
                "population": 1,
            },
            {
                "id": "788dfb94-247e-4f9c-a9cf-44251d0455bc",
                "ward_number": 1,
                "disability_cause": "unknown",
                "population": 60,
            },
            {
                "id": "cae49efb-560e-457c-93ac-65498b9eb78d",
                "ward_number": 2,
                "disability_cause": "accident",
                "population": 24,
            },
            {
                "id": "3091cc41-5bea-4ad2-a540-fb89416491db",
                "ward_number": 2,
                "disability_cause": "congenital",
                "population": 41,
            },
            {
                "id": "720625ca-a979-4327-ab9c-36ec7d357a83",
                "ward_number": 2,
                "disability_cause": "disease",
                "population": 18,
            },
            {
                "id": "7ef12aa1-b22c-45ec-9d22-b6b1e0f5c3fc",
                "ward_number": 2,
                "disability_cause": "malnutrition",
                "population": 4,
            },
            {
                "id": "7d6d3427-7e00-4976-a918-2ca8f5f36214",
                "ward_number": 2,
                "disability_cause": "unknown",
                "population": 3,
            },
            {
                "id": "01153314-ffb8-4579-ab50-ea451d7de6c8",
                "ward_number": 3,
                "disability_cause": "accident",
                "population": 44,
            },
            {
                "id": "720acd35-2763-4132-965d-00da5857b63e",
                "ward_number": 3,
                "disability_cause": "congenital",
                "population": 47,
            },
            {
                "id": "7e1bf992-cfa7-4c8a-b75c-191479338e8d",
                "ward_number": 3,
                "disability_cause": "disease",
                "population": 64,
            },
            {
                "id": "50ec9c0a-b967-45de-9433-b779bf5b8618",
                "ward_number": 3,
                "disability_cause": "malnutrition",
                "population": 2,
            },
            {
                "id": "4e7f60a0-7dc8-4165-bf7b-15bccb44733a",
                "ward_number": 3,
                "disability_cause": "other",
                "population": 1,
            },
            {
                "id": "dc29e65e-d10f-454d-8e41-d48b23f85bbb",
                "ward_number": 4,
                "disability_cause": "accident",
                "population": 17,
            },
            {
                "id": "7a937be3-a5a4-472b-8ab6-5dcf7298c479",
                "ward_number": 4,
                "disability_cause": "congenital",
                "population": 47,
            },
            {
                "id": "fcd07adb-56b7-4001-97c1-b5518677b231",
                "ward_number": 4,
                "disability_cause": "disease",
                "population": 57,
            },
            {
                "id": "53996fc9-dc36-4cd8-a3d8-1f1e4e82ad01",
                "ward_number": 4,
                "disability_cause": "malnutrition",
                "population": 2,
            },
            {
                "id": "9d850891-d9af-4f16-89dd-108ddf9a81fb",
                "ward_number": 4,
                "disability_cause": "other",
                "population": 7,
            },
            {
                "id": "7b0e3bea-781e-489f-ace8-36b463c69214",
                "ward_number": 4,
                "disability_cause": "unknown",
                "population": 18,
            },
            {
                "id": "209bfb8e-91d2-4415-91b9-d526400a1e51",
                "ward_number": 5,
                "disability_cause": "accident",
                "population": 15,
            },
            {
                "id": "29ceb399-eb76-41cf-9cb9-fda6fb13d1fc",
                "ward_number": 5,
                "disability_cause": "conflict",
                "population": 4,
            },
            {
                "id": "ff1d2599-635a-4e67-bc5a-79224a39443f",
                "ward_number": 5,
                "disability_cause": "congenital",
                "population": 35,
            },
            {
                "id": "d6b3797c-5bf7-4097-ace1-807caaa9d1c9",
                "ward_number": 5,
                "disability_cause": "disease",
                "population": 54,
            },
            {
                "id": "ac400af3-7acd-470d-868c-588125631c11",
                "ward_number": 5,
                "disability_cause": "malnutrition",
                "population": 7,
            },
            {
                "id": "a542ca17-64a1-404b-9921-c29867fb1bdc",
                "ward_number": 5,
                "disability_cause": "other",
                "population": 3,
            },
            {
                "id": "af26e3bb-a148-4a91-8843-c4c9028ad3f2",
                "ward_number": 5,
                "disability_cause": "unknown",
                "population": 16,
            },
            {
                "id": "6d659c33-8aa1-459f-ab30-c4850a8f4207",
                "ward_number": 6,
                "disability_cause": "accident",
                "population": 56,
            },
            {
                "id": "32e13b1e-988a-48da-b72e-ce7c55569a19",
                "ward_number": 6,
                "disability_cause": "conflict",
                "population": 1,
            },
            {
                "id": "48247605-f675-401b-8d75-15b1015c9dd8",
                "ward_number": 6,
                "disability_cause": "congenital",
                "population": 39,
            },
            {
                "id": "e6bcc5d0-0e31-40cf-a17d-1bd0437c4126",
                "ward_number": 6,
                "disability_cause": "disease",
                "population": 43,
            },
            {
                "id": "234683bb-285b-4a09-a5d0-f26861e2c145",
                "ward_number": 6,
                "disability_cause": "malnutrition",
                "population": 1,
            },
            {
                "id": "433e2125-f7e6-4bbf-bf03-e21d31ababeb",
                "ward_number": 6,
                "disability_cause": "other",
                "population": 4,
            },
            {
                "id": "747a43b4-72ba-42ab-8326-5f7caa0563eb",
                "ward_number": 6,
                "disability_cause": "unknown",
                "population": 20,
            },
            {
                "id": "92b912dd-23f7-478f-ad69-a7f76261606a",
                "ward_number": 7,
                "disability_cause": "accident",
                "population": 15,
            },
            {
                "id": "e13cfa07-9c29-43c8-b4cd-92d1f29baa3a",
                "ward_number": 7,
                "disability_cause": "conflict",
                "population": 3,
            },
            {
                "id": "c710dfe0-819a-4578-ab2b-8402653eb5dc",
                "ward_number": 7,
                "disability_cause": "congenital",
                "population": 26,
            },
            {
                "id": "1e707070-da47-4a95-9643-75e5eee82a20",
                "ward_number": 7,
                "disability_cause": "disease",
                "population": 8,
            },
            {
                "id": "345166a6-d012-4c29-9b27-4ce13a6c2066",
                "ward_number": 7,
                "disability_cause": "unknown",
                "population": 40,
            },
            {
                "id": "7a97eb16-2a94-4245-8194-91c789f5aac8",
                "ward_number": 8,
                "disability_cause": "accident",
                "population": 3,
            },
            {
                "id": "96418189-2148-4c99-b839-459422b5db47",
                "ward_number": 8,
                "disability_cause": "congenital",
                "population": 3,
            },
            {
                "id": "d22efa76-eab3-4ec5-82c7-a5055bb4bfef",
                "ward_number": 8,
                "disability_cause": "disease",
                "population": 8,
            },
            {
                "id": "633978d3-b7d9-4e80-a862-143bd9a9635f",
                "ward_number": 8,
                "disability_cause": "unknown",
                "population": 4,
            },
        ]

        # Map all cause keys to uppercase and map 'unknown' to 'OTHER'
        for entry in disability_data:
            cause = entry["disability_cause"].upper()
            if cause == "UNKNOWN":
                cause = "OTHER"
            entry["disability_cause"] = cause

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
                percentage = (
                    cause_population / total_population * 100
                    if total_population > 0
                    else 0
                )
                self.stdout.write(
                    f"  {cause}: {cause_population:,} people ({percentage:.2f}%)"
                )

        # Ward-wise summary
        self.stdout.write("\nWard-wise disability cause summary:")
        for ward_num in range(1, 9):  # Now covering wards 1-8
            ward_population = (
                WardWiseDisabilityCause.objects.filter(ward_number=ward_num).aggregate(
                    total=models.Sum("population")
                )["total"]
                or 0
            )
            if ward_population > 0:
                self.stdout.write(f"  वडा {ward_num}: {ward_population:,} people")
