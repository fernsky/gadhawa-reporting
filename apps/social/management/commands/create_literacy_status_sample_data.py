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

        # Sample data structure: [ward_number, literacy_type, population]
        sample_data = [
            # Ward 1
            (1, LiteracyTypeChoice.BOTH_READING_AND_WRITING, 3320),
            (1, LiteracyTypeChoice.ILLITERATE, 2256),
            (1, LiteracyTypeChoice.READING_ONLY, 27),
            # Ward 2
            (2, LiteracyTypeChoice.BOTH_READING_AND_WRITING, 2557),
            (2, LiteracyTypeChoice.ILLITERATE, 1703),
            (2, LiteracyTypeChoice.READING_ONLY, 5),
            # Ward 3
            (3, LiteracyTypeChoice.BOTH_READING_AND_WRITING, 1945),
            (3, LiteracyTypeChoice.ILLITERATE, 1071),
            (3, LiteracyTypeChoice.READING_ONLY, 22),
            # Ward 4
            (4, LiteracyTypeChoice.BOTH_READING_AND_WRITING, 2941),
            (4, LiteracyTypeChoice.ILLITERATE, 1109),
            (4, LiteracyTypeChoice.READING_ONLY, 9),
            # Ward 5
            (5, LiteracyTypeChoice.BOTH_READING_AND_WRITING, 2485),
            (5, LiteracyTypeChoice.ILLITERATE, 899),
            (5, LiteracyTypeChoice.READING_ONLY, 22),
            # Ward 6
            (6, LiteracyTypeChoice.BOTH_READING_AND_WRITING, 2926),
            (6, LiteracyTypeChoice.ILLITERATE, 1575),
            (6, LiteracyTypeChoice.READING_ONLY, 10),
            # Ward 7
            (7, LiteracyTypeChoice.BOTH_READING_AND_WRITING, 1579),
            (7, LiteracyTypeChoice.ILLITERATE, 1025),
            (7, LiteracyTypeChoice.READING_ONLY, 9),
        ]

        created_count = 0
        updated_count = 0

        with transaction.atomic():
            for ward_number, literacy_type, population in sample_data:
                record, created = WardWiseLiteracyStatus.objects.update_or_create(
                    ward_number=ward_number,
                    literacy_type=literacy_type,
                    defaults={"population": population},
                )

                if created:
                    created_count += 1
                    self.stdout.write(
                        f"Created literacy status data for Ward {ward_number}, "
                        f"Type: {literacy_type.value}, Population: {population}"
                    )
                else:
                    updated_count += 1
                    self.stdout.write(
                        f"Updated literacy status data for Ward {ward_number}, "
                        f"Type: {literacy_type.value}, Population: {population}"
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
