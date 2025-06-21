"""
Management command to create househead demographics data based on actual data
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db import models
from apps.demographics.models import WardWiseHouseheadGender, GenderChoice
import uuid


class Command(BaseCommand):
    help = "Create househead demographics data based on actual municipality-wide data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before creating new data",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write(self.style.WARNING("Clearing existing househead data..."))
            WardWiseHouseheadGender.objects.all().delete()

        self.stdout.write(
            "Creating househead demographics data based on actual municipality-wide data..."
        )

        # Raw ward-wise househead gender data from actual census
        raw_ward_data = [
            (1, "MALE", 267),
            (1, "FEMALE", 654),
            (2, "MALE", 584),
            (2, "FEMALE", 561),
            (3, "MALE", 830),
            (3, "FEMALE", 64),
            (4, "MALE", 603),
            (4, "FEMALE", 337),
            (5, "MALE", 199),
            (5, "FEMALE", 177),
            (6, "MALE", 499),
            (6, "FEMALE", 397),
            (7, "MALE", 289),
            (7, "FEMALE", 178),
        ]

        # Convert to the format expected by the rest of the code
        househead_data = []
        for ward_number, gender, population in raw_ward_data:
            ward_name_map = {
                1: "वडा नं. १",
                2: "वडा नं. २",
                3: "वडा नं. ३",
                4: "वडा नं. ४",
                5: "वडा नं. ५",
                6: "वडा नं. ६",
                7: "वडा नं. ७",
            }

            househead_data.append(
                {
                    "id": str(uuid.uuid4()),
                    "ward_number": ward_number,
                    "ward_name": ward_name_map.get(
                        ward_number, f"वडा नं. {ward_number}"
                    ),
                    "gender": gender,
                    "population": population,
                }
            )

        self.stdout.write(
            f"Processing {len(raw_ward_data)} ward-level records for househead demographics..."
        )

        existing_count = WardWiseHouseheadGender.objects.count()
        if existing_count > 0 and not options["clear"]:
            self.stdout.write(
                self.style.WARNING(
                    f"Found {existing_count} existing records. Use --clear to replace them."
                )
            )
            return

        created_count = 0
        with transaction.atomic():
            for data in househead_data:
                obj, created = WardWiseHouseheadGender.objects.get_or_create(
                    ward_number=data["ward_number"],
                    gender=data["gender"],
                    defaults={
                        "id": data["id"],
                        "ward_name": data["ward_name"],
                        "population": data["population"],
                    },
                )

                if created:
                    created_count += 1
                    self.stdout.write(
                        f"Created: Ward {data['ward_number']} - {data['gender']} ({data['population']} households)"
                    )
                else:
                    obj.population = data["population"]
                    obj.ward_name = data["ward_name"]
                    obj.save()
                    self.stdout.write(
                        f"Updated: Ward {data['ward_number']} - {data['gender']} ({data['population']} households)"
                    )

        total_records = WardWiseHouseheadGender.objects.count()
        total_households = sum(
            WardWiseHouseheadGender.objects.values_list("population", flat=True)
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nSuccessfully processed {len(househead_data)} househead demographic records "
                f"({created_count} new, {len(househead_data) - created_count} updated)\n"
                f"Total records in database: {total_records}\n"
                f"Total households covered: {total_households:,} households"
            )
        )

        # Calculate and display gender-wise summary
        self.stdout.write("\nHousehead gender breakdown:")
        gender_totals = {}
        for gender_choice in GenderChoice.choices:
            gender_code = gender_choice[0]
            gender_name = gender_choice[1]
            gender_households = (
                WardWiseHouseheadGender.objects.filter(gender=gender_code).aggregate(
                    total=models.Sum("population")
                )["total"]
                or 0
            )
            gender_totals[gender_code] = gender_households

            if gender_households > 0:
                percentage = gender_households / total_households * 100
                self.stdout.write(
                    f"  {gender_name}: {gender_households:,} households ({percentage:.2f}%)"
                )
            else:
                self.stdout.write(f"  {gender_name}: 0 households (0.00%)")

        # Ward-wise summary
        self.stdout.write("\nWard-wise household summary:")
        for ward_num in range(1, 8):  # Only covering wards 1-7 based on actual data
            ward_households = (
                WardWiseHouseheadGender.objects.filter(ward_number=ward_num).aggregate(
                    total=models.Sum("population")
                )["total"]
                or 0
            )
            if ward_households > 0:
                self.stdout.write(f"  वडा {ward_num}: {ward_households:,} households")
