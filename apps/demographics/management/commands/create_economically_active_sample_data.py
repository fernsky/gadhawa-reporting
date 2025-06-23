"""
Management command to create economically active population demographics data based on latest actual data (wards 1-8, all genders)
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db import models
from apps.demographics.models import (
    WardAgeWiseEconomicallyActivePopulation,
    EconomicallyActiveAgeGroupChoice,
    GenderChoice,
)
import uuid


class Command(BaseCommand):
    help = "Create economically active population demographics data based on latest actual municipality-wide data (wards 1-8, all genders)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before creating new data",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write(
                self.style.WARNING(
                    "Clearing existing economically active population data..."
                )
            )
            WardAgeWiseEconomicallyActivePopulation.objects.all().delete()

        self.stdout.write(
            "Creating economically active population demographics data based on latest actual municipality-wide data (wards 1-8, all genders)..."
        )

        # Latest sample data (wards 1-8, all genders, including OTHER)
        economically_active_data = [
            {
                "id": "e09d042c-977a-4b53-bf2d-5e03717ff37f",
                "ward_number": 1,
                "age_group": "AGE_0_TO_14",
                "gender": "FEMALE",
                "population": 1318,
            },
            {
                "id": "f9a56b6a-88bd-4e3e-a6c9-021abfd7b86c",
                "ward_number": 1,
                "age_group": "AGE_0_TO_14",
                "gender": "MALE",
                "population": 886,
            },
            {
                "id": "4aae545c-5797-4770-9bb0-85fb9d44e6cd",
                "ward_number": 1,
                "age_group": "AGE_0_TO_14",
                "gender": "OTHER",
                "population": 2,
            },
            {
                "id": "484a5d33-0848-452a-b43f-b95d12afc151",
                "ward_number": 1,
                "age_group": "AGE_15_TO_59",
                "gender": "FEMALE",
                "population": 2469,
            },
            {
                "id": "5d08684b-32b3-4fc9-aa20-bc823a5f6738",
                "ward_number": 1,
                "age_group": "AGE_15_TO_59",
                "gender": "MALE",
                "population": 2512,
            },
            {
                "id": "34abe954-927d-42bb-b745-3c567472d1cf",
                "ward_number": 1,
                "age_group": "AGE_15_TO_59",
                "gender": "OTHER",
                "population": 1,
            },
            {
                "id": "7c895d84-08ee-4862-aef2-d82207661c64",
                "ward_number": 1,
                "age_group": "AGE_60_PLUS",
                "gender": "FEMALE",
                "population": 265,
            },
            {
                "id": "eb52a1d7-002f-49b5-97ae-959f843e3441",
                "ward_number": 1,
                "age_group": "AGE_60_PLUS",
                "gender": "MALE",
                "population": 322,
            },
            {
                "id": "a0ef580a-aa20-47fd-ba2f-ed60dfd789f1",
                "ward_number": 2,
                "age_group": "AGE_0_TO_14",
                "gender": "FEMALE",
                "population": 627,
            },
            {
                "id": "e0add6c9-e234-4a2b-b4a7-ccdc85bb5e69",
                "ward_number": 2,
                "age_group": "AGE_0_TO_14",
                "gender": "MALE",
                "population": 626,
            },
            {
                "id": "a5499fc7-61af-455b-a221-641fad7d728c",
                "ward_number": 2,
                "age_group": "AGE_0_TO_14",
                "gender": "OTHER",
                "population": 1,
            },
            {
                "id": "9863197c-8315-4bf2-a14a-3a4433838dc6",
                "ward_number": 2,
                "age_group": "AGE_15_TO_59",
                "gender": "FEMALE",
                "population": 1996,
            },
            {
                "id": "48e64724-4f87-4196-9250-5460991e3905",
                "ward_number": 2,
                "age_group": "AGE_15_TO_59",
                "gender": "MALE",
                "population": 2004,
            },
            {
                "id": "5714fb04-c76a-4e63-be0e-84fd87b2018a",
                "ward_number": 2,
                "age_group": "AGE_60_PLUS",
                "gender": "FEMALE",
                "population": 298,
            },
            {
                "id": "e543d894-a1ff-452c-810f-012df45310f6",
                "ward_number": 2,
                "age_group": "AGE_60_PLUS",
                "gender": "MALE",
                "population": 272,
            },
            {
                "id": "d28cf538-a41d-43d4-ae7f-69586a9e3193",
                "ward_number": 3,
                "age_group": "AGE_0_TO_14",
                "gender": "FEMALE",
                "population": 578,
            },
            {
                "id": "cc413f70-8835-439c-90d1-fa87c8afd281",
                "ward_number": 3,
                "age_group": "AGE_0_TO_14",
                "gender": "MALE",
                "population": 585,
            },
            {
                "id": "0d487f7d-814c-4af9-8ed5-2997478b9186",
                "ward_number": 3,
                "age_group": "AGE_15_TO_59",
                "gender": "FEMALE",
                "population": 2012,
            },
            {
                "id": "4d0264ae-80ba-4e1b-b15a-70c1ca63bd02",
                "ward_number": 3,
                "age_group": "AGE_15_TO_59",
                "gender": "MALE",
                "population": 2080,
            },
            {
                "id": "080ec408-feca-4aa1-99c5-d82c38b23033",
                "ward_number": 3,
                "age_group": "AGE_60_PLUS",
                "gender": "FEMALE",
                "population": 282,
            },
            {
                "id": "c1529b4b-fc16-4939-a47e-42b355fcd60b",
                "ward_number": 3,
                "age_group": "AGE_60_PLUS",
                "gender": "MALE",
                "population": 247,
            },
            {
                "id": "6b6ac317-f8b9-459a-bb19-050342816490",
                "ward_number": 4,
                "age_group": "AGE_0_TO_14",
                "gender": "FEMALE",
                "population": 757,
            },
            {
                "id": "3542f097-9ac4-4ffb-8e33-b9ddb3e9a32e",
                "ward_number": 4,
                "age_group": "AGE_0_TO_14",
                "gender": "MALE",
                "population": 752,
            },
            {
                "id": "b65e9b62-5085-457f-a106-a0d3afe6e685",
                "ward_number": 4,
                "age_group": "AGE_0_TO_14",
                "gender": "OTHER",
                "population": 1,
            },
            {
                "id": "03476b70-cbeb-4f78-89d4-b1392d1f30d0",
                "ward_number": 4,
                "age_group": "AGE_15_TO_59",
                "gender": "FEMALE",
                "population": 2052,
            },
            {
                "id": "c0637c9c-0c79-49e7-9b24-d70d3bae262b",
                "ward_number": 4,
                "age_group": "AGE_15_TO_59",
                "gender": "MALE",
                "population": 2019,
            },
            {
                "id": "6748b010-c5ad-45ca-ac66-77e8d378ff21",
                "ward_number": 4,
                "age_group": "AGE_60_PLUS",
                "gender": "FEMALE",
                "population": 287,
            },
            {
                "id": "ff2cb15d-ed34-43aa-8a08-8df4305726a7",
                "ward_number": 4,
                "age_group": "AGE_60_PLUS",
                "gender": "MALE",
                "population": 283,
            },
            {
                "id": "e509fe83-ea73-485e-bec1-7cd6ad47fc9f",
                "ward_number": 5,
                "age_group": "AGE_0_TO_14",
                "gender": "FEMALE",
                "population": 779,
            },
            {
                "id": "fb1c8f6e-8bc9-457e-8c99-7d415ee1ffa1",
                "ward_number": 5,
                "age_group": "AGE_0_TO_14",
                "gender": "MALE",
                "population": 788,
            },
            {
                "id": "79d09ce0-6973-43c9-8ba7-46a01187f59c",
                "ward_number": 5,
                "age_group": "AGE_0_TO_14",
                "gender": "OTHER",
                "population": 1,
            },
            {
                "id": "a9915a2e-4071-41ff-8ec4-e38c083e94d6",
                "ward_number": 5,
                "age_group": "AGE_15_TO_59",
                "gender": "FEMALE",
                "population": 2437,
            },
            {
                "id": "08461c13-fb55-45a2-a15a-052554c5bbed",
                "ward_number": 5,
                "age_group": "AGE_15_TO_59",
                "gender": "MALE",
                "population": 2416,
            },
            {
                "id": "c5ec7c55-28c2-438e-a609-13e0ddfc3229",
                "ward_number": 5,
                "age_group": "AGE_60_PLUS",
                "gender": "FEMALE",
                "population": 409,
            },
            {
                "id": "3e7d84a1-5e34-4e67-9554-3ef0c03b5b59",
                "ward_number": 5,
                "age_group": "AGE_60_PLUS",
                "gender": "MALE",
                "population": 337,
            },
            {
                "id": "78bcb1f2-48eb-46b1-ae80-1fdf4407113e",
                "ward_number": 5,
                "age_group": "AGE_60_PLUS",
                "gender": "OTHER",
                "population": 1,
            },
            {
                "id": "ccbcd009-c996-4d83-a189-3b67d7808bba",
                "ward_number": 6,
                "age_group": "AGE_0_TO_14",
                "gender": "FEMALE",
                "population": 846,
            },
            {
                "id": "ca9cabae-c255-40a3-b5d1-9a65372eeca3",
                "ward_number": 6,
                "age_group": "AGE_0_TO_14",
                "gender": "MALE",
                "population": 1068,
            },
            {
                "id": "228ba04b-0bad-47f0-aadc-4a06e36f7ff7",
                "ward_number": 6,
                "age_group": "AGE_0_TO_14",
                "gender": "OTHER",
                "population": 2,
            },
            {
                "id": "db693fe1-c548-4519-8e74-1b153e4cd41a",
                "ward_number": 6,
                "age_group": "AGE_15_TO_59",
                "gender": "FEMALE",
                "population": 2769,
            },
            {
                "id": "05a30f3b-bfa1-421c-b159-0b09b902e6e0",
                "ward_number": 6,
                "age_group": "AGE_15_TO_59",
                "gender": "MALE",
                "population": 2525,
            },
            {
                "id": "1340fc44-d9de-4c51-9a26-c72e595922db",
                "ward_number": 6,
                "age_group": "AGE_15_TO_59",
                "gender": "OTHER",
                "population": 1,
            },
            {
                "id": "fd976189-e437-43b2-b34b-613bbf09d68c",
                "ward_number": 6,
                "age_group": "AGE_60_PLUS",
                "gender": "FEMALE",
                "population": 525,
            },
            {
                "id": "6f9c5179-90e8-4cc6-82b7-f7699b4819f4",
                "ward_number": 6,
                "age_group": "AGE_60_PLUS",
                "gender": "MALE",
                "population": 333,
            },
            {
                "id": "585e8c65-3696-4c8c-83db-fd9694cc6ef8",
                "ward_number": 7,
                "age_group": "AGE_0_TO_14",
                "gender": "FEMALE",
                "population": 981,
            },
            {
                "id": "b0a45dc2-41b3-42d8-ae59-6f2a1d759b24",
                "ward_number": 7,
                "age_group": "AGE_0_TO_14",
                "gender": "MALE",
                "population": 617,
            },
            {
                "id": "f689aa8b-860d-4a32-97b1-5ab9fdeace42",
                "ward_number": 7,
                "age_group": "AGE_0_TO_14",
                "gender": "OTHER",
                "population": 2,
            },
            {
                "id": "a72d97ca-053f-4e85-ab03-30b8730d39d2",
                "ward_number": 7,
                "age_group": "AGE_15_TO_59",
                "gender": "FEMALE",
                "population": 2018,
            },
            {
                "id": "ab836b38-ccd8-4285-93f8-a4633a2b4c08",
                "ward_number": 7,
                "age_group": "AGE_15_TO_59",
                "gender": "MALE",
                "population": 2095,
            },
            {
                "id": "4b2d3680-daf6-4045-8314-94593e94b277",
                "ward_number": 7,
                "age_group": "AGE_15_TO_59",
                "gender": "OTHER",
                "population": 1,
            },
            {
                "id": "e0e5e8cd-26ed-4e70-9122-44034e1524ff",
                "ward_number": 7,
                "age_group": "AGE_60_PLUS",
                "gender": "FEMALE",
                "population": 276,
            },
            {
                "id": "1c4eb2ec-90bc-4f9d-84a4-a2d48702dbed",
                "ward_number": 7,
                "age_group": "AGE_60_PLUS",
                "gender": "MALE",
                "population": 295,
            },
            {
                "id": "6bf95822-afab-4656-b81b-b7aa07c98a20",
                "ward_number": 8,
                "age_group": "AGE_0_TO_14",
                "gender": "FEMALE",
                "population": 168,
            },
            {
                "id": "d9e2123a-475d-42b0-a918-140e4523e684",
                "ward_number": 8,
                "age_group": "AGE_0_TO_14",
                "gender": "MALE",
                "population": 110,
            },
            {
                "id": "8d678a94-6356-472b-aa93-3c9bf13311c6",
                "ward_number": 8,
                "age_group": "AGE_15_TO_59",
                "gender": "FEMALE",
                "population": 251,
            },
            {
                "id": "f87a20bf-856c-4c5b-b27f-c5c51bf446de",
                "ward_number": 8,
                "age_group": "AGE_15_TO_59",
                "gender": "MALE",
                "population": 265,
            },
            {
                "id": "53b4bb6f-25b5-4ac8-b69d-2f4c192b283c",
                "ward_number": 8,
                "age_group": "AGE_60_PLUS",
                "gender": "FEMALE",
                "population": 36,
            },
            {
                "id": "fd6b2a3a-d957-405a-9567-eebfdc78a5fb",
                "ward_number": 8,
                "age_group": "AGE_60_PLUS",
                "gender": "MALE",
                "population": 43,
            },
        ]

        # Check if data already exists
        existing_count = WardAgeWiseEconomicallyActivePopulation.objects.count()
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
            for data in economically_active_data:
                obj, created = (
                    WardAgeWiseEconomicallyActivePopulation.objects.get_or_create(
                        ward_number=data["ward_number"],
                        age_group=data["age_group"],
                        gender=data["gender"],
                        defaults={
                            "id": data["id"],
                            "population": data["population"],
                        },
                    )
                )

                if created:
                    created_count += 1
                    self.stdout.write(
                        f"Created: Ward {data['ward_number']} - {data['age_group']} - {data['gender']} ({data['population']} people)"
                    )
                else:
                    # Update existing record
                    obj.population = data["population"]
                    obj.save()
                    self.stdout.write(
                        f"Updated: Ward {data['ward_number']} - {data['age_group']} - {data['gender']} ({data['population']} people)"
                    )

        # Print summary
        total_records = WardAgeWiseEconomicallyActivePopulation.objects.count()
        total_population = sum(
            WardAgeWiseEconomicallyActivePopulation.objects.values_list(
                "population", flat=True
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nSuccessfully processed {len(economically_active_data)} economically active population demographic records "
                f"({created_count} new, {len(economically_active_data) - created_count} updated)\n"
                f"Total records in database: {total_records}\n"
                f"Total population covered: {total_population:,} people"
            )
        )

        # Print age group breakdown
        self.stdout.write("\nAge group breakdown:")
        for age_choice in EconomicallyActiveAgeGroupChoice.choices:
            age_code = age_choice[0]
            age_name = age_choice[1]
            age_population = (
                WardAgeWiseEconomicallyActivePopulation.objects.filter(
                    age_group=age_code
                ).aggregate(total=models.Sum("population"))["total"]
                or 0
            )

            if age_population > 0:
                percentage = (
                    age_population / total_population * 100
                    if total_population > 0
                    else 0
                )
                self.stdout.write(
                    f"  {age_name}: {age_population:,} people ({percentage:.2f}%)"
                )
            else:
                self.stdout.write(f"  {age_name}: 0 people (0.00%)")

        # Print gender breakdown
        self.stdout.write("\nGender breakdown:")
        for gender_choice in GenderChoice.choices:
            gender_code = gender_choice[0]
            gender_name = gender_choice[1]
            gender_population = (
                WardAgeWiseEconomicallyActivePopulation.objects.filter(
                    gender=gender_code
                ).aggregate(total=models.Sum("population"))["total"]
                or 0
            )

            if gender_population > 0:
                percentage = (
                    gender_population / total_population * 100
                    if total_population > 0
                    else 0
                )
                self.stdout.write(
                    f"  {gender_name}: {gender_population:,} people ({percentage:.2f}%)"
                )
            else:
                self.stdout.write(f"  {gender_name}: 0 people (0.00%)")

        # Ward-wise summary
        self.stdout.write("\nWard-wise economically active population summary:")
        for ward_num in range(1, 9):  # Now covering wards 1-8
            ward_population = (
                WardAgeWiseEconomicallyActivePopulation.objects.filter(
                    ward_number=ward_num
                ).aggregate(total=models.Sum("population"))["total"]
                or 0
            )
            if ward_population > 0:
                self.stdout.write(f"  वडा {ward_num}: {ward_population:,} people")
