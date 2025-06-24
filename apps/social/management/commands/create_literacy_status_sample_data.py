"""
Management command to create sample data for Ward Wise Literacy Status

This command creates comprehensive sample data for literacy status across all wards
based on the provided data structure for Section 5.1.1.
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from apps.social.models import WardWiseLiteracyStatus, LiteracyTypeChoice


class Command(BaseCommand):
    help = "Create sample data for Ward Wise Literacy Status (५.१.१)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete existing data before creating new data",
        )

    def handle(self, *args, **options):
        if options["reset"]:
            self.stdout.write(
                self.style.WARNING("Deleting existing literacy status data...")
            )
            WardWiseLiteracyStatus.objects.all().delete()

        # Use provided JSON data for sample_data
        sample_data = [
            {
                "id": "3cd04775-5304-475d-ae55-e0a6870453d1",
                "ward_number": 1,
                "literacy_type": "BOTH_READING_AND_WRITING",
                "population": 6130,
            },
            {
                "id": "01b5369e-9584-44ac-b678-2b227b8e3f3c",
                "ward_number": 1,
                "literacy_type": "ILLITERATE",
                "population": 1624,
            },
            {
                "id": "cf4c5208-a474-4afd-adf4-5edae2e4f8c2",
                "ward_number": 1,
                "literacy_type": "READING_ONLY",
                "population": 21,
            },
            {
                "id": "3a0647a4-dbc7-4b2e-9add-0d783adbd3a0",
                "ward_number": 2,
                "literacy_type": "BOTH_READING_AND_WRITING",
                "population": 4614,
            },
            {
                "id": "de9a00cd-7bad-4862-8293-ce1ac4d52ca9",
                "ward_number": 2,
                "literacy_type": "ILLITERATE",
                "population": 1107,
            },
            {
                "id": "b9030a8e-4736-410f-8330-00f18ab1650d",
                "ward_number": 2,
                "literacy_type": "READING_ONLY",
                "population": 103,
            },
            {
                "id": "55421400-f615-4916-874f-a6d87f00f71d",
                "ward_number": 3,
                "literacy_type": "BOTH_READING_AND_WRITING",
                "population": 4722,
            },
            {
                "id": "4f3f209e-d715-4dbd-80ea-2dbf6d2d89fe",
                "ward_number": 3,
                "literacy_type": "ILLITERATE",
                "population": 1028,
            },
            {
                "id": "1a82abfd-5579-40c4-af06-06e200c122b1",
                "ward_number": 3,
                "literacy_type": "READING_ONLY",
                "population": 34,
            },
            {
                "id": "d14c044d-9319-4e86-b1c7-556fa4b9000a",
                "ward_number": 4,
                "literacy_type": "BOTH_READING_AND_WRITING",
                "population": 4989,
            },
            {
                "id": "26fa7c07-73f9-461a-9df9-60532b53bbe3",
                "ward_number": 4,
                "literacy_type": "ILLITERATE",
                "population": 1157,
            },
            {
                "id": "717943b0-75e2-4ccc-8198-4f9c119df492",
                "ward_number": 4,
                "literacy_type": "READING_ONLY",
                "population": 5,
            },
            {
                "id": "d5ae5b2f-cf32-4baf-8004-b772b7397772",
                "ward_number": 5,
                "literacy_type": "BOTH_READING_AND_WRITING",
                "population": 5684,
            },
            {
                "id": "f6aa3314-600a-4fea-bb56-5e8cfead91ff",
                "ward_number": 5,
                "literacy_type": "ILLITERATE",
                "population": 1473,
            },
            {
                "id": "a00698c6-4bbe-4934-884b-11c2d1a031dd",
                "ward_number": 5,
                "literacy_type": "READING_ONLY",
                "population": 11,
            },
            {
                "id": "e0fd3f17-5a79-4065-be4d-a2b4e86373c1",
                "ward_number": 6,
                "literacy_type": "BOTH_READING_AND_WRITING",
                "population": 6409,
            },
            {
                "id": "93569261-7ab6-4dc4-bc53-58e87f7327e3",
                "ward_number": 6,
                "literacy_type": "ILLITERATE",
                "population": 1624,
            },
            {
                "id": "0434aa79-262e-49bf-89b9-46097451d310",
                "ward_number": 6,
                "literacy_type": "READING_ONLY",
                "population": 36,
            },
            {
                "id": "09865bba-3109-4951-8214-3fe4c4aa0f39",
                "ward_number": 7,
                "literacy_type": "BOTH_READING_AND_WRITING",
                "population": 4652,
            },
            {
                "id": "702d5737-940b-46ba-b7f6-9d668a9c95fd",
                "ward_number": 7,
                "literacy_type": "ILLITERATE",
                "population": 1624,
            },
            {
                "id": "2837b856-f036-48e5-aa25-6495aa13a420",
                "ward_number": 7,
                "literacy_type": "READING_ONLY",
                "population": 9,
            },
            {
                "id": "ca52827e-27fd-4e04-9f90-4bfba5782eb3",
                "ward_number": 8,
                "literacy_type": "BOTH_READING_AND_WRITING",
                "population": 760,
            },
            {
                "id": "28c889da-1d03-4018-a5b0-ab1b7e6f084d",
                "ward_number": 8,
                "literacy_type": "ILLITERATE",
                "population": 113,
            },
        ]

        created_count = 0
        updated_count = 0

        with transaction.atomic():
            for entry in sample_data:
                # Map string to enum
                literacy_type_enum = getattr(LiteracyTypeChoice, entry["literacy_type"])
                record, created = WardWiseLiteracyStatus.objects.update_or_create(
                    id=entry["id"],
                    defaults={
                        "ward_number": entry["ward_number"],
                        "literacy_type": literacy_type_enum,
                        "population": entry["population"],
                    },
                )
                if created:
                    created_count += 1
                    self.stdout.write(
                        f"Created literacy status data for Ward {entry['ward_number']}, "
                        f"Type: {literacy_type_enum.value}, Population: {entry['population']}"
                    )
                else:
                    updated_count += 1
                    self.stdout.write(
                        f"Updated literacy status data for Ward {entry['ward_number']}, "
                        f"Type: {literacy_type_enum.value}, Population: {entry['population']}"
                    )

        # Generate summary statistics
        self.generate_summary()

        self.stdout.write("\n" + "=" * 50)
        self.stdout.write("LITERACY STATUS SAMPLE DATA SUMMARY")
        self.stdout.write("=" * 50)
        self.stdout.write(f"Records created: {created_count}")
        self.stdout.write(f"Records updated: {updated_count}")
        self.stdout.write(f"Total records: {WardWiseLiteracyStatus.objects.count()}")

        # Calculate and display totals
        total_population = sum(
            record.population for record in WardWiseLiteracyStatus.objects.all()
        )
        self.stdout.write(f"Total population: {self.nepali_number(total_population)}")

        self.stdout.write(
            self.style.SUCCESS("\n✅ Literacy status sample data loaded successfully!")
        )

    def generate_summary(self):
        """Generate detailed summary of literacy status data"""
        all_records = WardWiseLiteracyStatus.objects.all()

        # Ward-wise totals
        ward_totals = {}
        for record in all_records:
            if record.ward_number not in ward_totals:
                ward_totals[record.ward_number] = 0
            ward_totals[record.ward_number] += record.population

        total_population = sum(ward_totals.values())

        self.stdout.write("\n=== WARD-WISE TOTALS ===")
        for ward_num in sorted(ward_totals.keys()):
            population = ward_totals[ward_num]
            percentage = (
                (population / total_population * 100) if total_population > 0 else 0
            )
            self.stdout.write(
                f"Ward {ward_num}: {self.nepali_number(population)} ({percentage:.1f}%)"
            )

        # Literacy type totals
        literacy_totals = {}
        for record in all_records:
            if record.literacy_type not in literacy_totals:
                literacy_totals[record.literacy_type] = 0
            literacy_totals[record.literacy_type] += record.population

        self.stdout.write("\n=== LITERACY STATUS BREAKDOWN ===")
        literacy_labels = {
            LiteracyTypeChoice.BOTH_READING_AND_WRITING: "पढ्न र लेख्न दुवै",
            LiteracyTypeChoice.READING_ONLY: "पढ्न मात्र",
            LiteracyTypeChoice.ILLITERATE: "निरक्षर",
        }

        for literacy_type, label in literacy_labels.items():
            count = literacy_totals.get(literacy_type, 0)
            percentage = (count / total_population * 100) if total_population > 0 else 0
            self.stdout.write(
                f"{label}: {self.nepali_number(count)} ({percentage:.1f}%)"
            )

        # Calculate literacy rates by ward
        self.stdout.write("\n=== WARD-WISE LITERACY RATES ===")
        for ward_num in sorted(ward_totals.keys()):
            ward_records = all_records.filter(ward_number=ward_num)
            total_pop = sum(r.population for r in ward_records)
            literate_pop = sum(
                r.population
                for r in ward_records
                if r.literacy_type
                in [
                    LiteracyTypeChoice.BOTH_READING_AND_WRITING,
                    LiteracyTypeChoice.READING_ONLY,
                ]
            )
            literacy_rate = (literate_pop / total_pop * 100) if total_pop > 0 else 0
            self.stdout.write(f"Ward {ward_num}: {literacy_rate:.1f}% literacy rate")

    def nepali_number(self, num):
        """Convert English numbers to Nepali"""
        english_to_nepali = {
            "0": "०",
            "1": "१",
            "2": "२",
            "3": "३",
            "4": "४",
            "5": "५",
            "6": "६",
            "7": "७",
            "8": "८",
            "9": "९",
        }
        return "".join(english_to_nepali.get(digit, digit) for digit in str(num))
