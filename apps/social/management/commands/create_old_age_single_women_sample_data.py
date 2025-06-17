"""
Management command to create sample data for old age population and single women.
"""

from django.core.management.base import BaseCommand
from apps.social.models import WardWiseOldAgePopulationAndSingleWomen


class Command(BaseCommand):
    help = "Create sample data for WardWiseOldAgePopulationAndSingleWomen"

    def handle(self, *args, **options):
        # Sample data based on the provided information
        sample_data = [
            {
                "ward_number": 1,
                "male_old_age_population": 393,
                "female_old_age_population": 229,
                "single_women_population": 0,
            },  # Single women data not provided, using 0
            {
                "ward_number": 2,
                "male_old_age_population": 168,
                "female_old_age_population": 230,
                "single_women_population": 0,
            },
            {
                "ward_number": 3,
                "male_old_age_population": 104,
                "female_old_age_population": 117,
                "single_women_population": 0,
            },
            {
                "ward_number": 4,
                "male_old_age_population": 170,
                "female_old_age_population": 191,
                "single_women_population": 0,
            },
            {
                "ward_number": 5,
                "male_old_age_population": 194,
                "female_old_age_population": 184,
                "single_women_population": 0,
            },
            {
                "ward_number": 6,
                "male_old_age_population": 272,
                "female_old_age_population": 284,
                "single_women_population": 0,
            },
            {
                "ward_number": 7,
                "male_old_age_population": 89,
                "female_old_age_population": 173,
                "single_women_population": 0,
            },
        ]

        created_count = 0
        updated_count = 0

        for data in sample_data:
            obj, created = (
                WardWiseOldAgePopulationAndSingleWomen.objects.update_or_create(
                    ward_number=data["ward_number"],
                    defaults={
                        "male_old_age_population": data["male_old_age_population"],
                        "female_old_age_population": data["female_old_age_population"],
                        "single_women_population": data["single_women_population"],
                    },
                )
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created old age and single women data for Ward {data['ward_number']}: "
                        f"Male elderly: {data['male_old_age_population']}, "
                        f"Female elderly: {data['female_old_age_population']}, "
                        f"Single women: {data['single_women_population']}"
                    )
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(
                        f"Updated old age and single women data for Ward {data['ward_number']}: "
                        f"Male elderly: {data['male_old_age_population']}, "
                        f"Female elderly: {data['female_old_age_population']}, "
                        f"Single women: {data['single_women_population']}"
                    )
                )

        # Summary
        total_male_elderly = sum(
            item["male_old_age_population"] for item in sample_data
        )
        total_female_elderly = sum(
            item["female_old_age_population"] for item in sample_data
        )
        total_elderly = total_male_elderly + total_female_elderly
        total_single_women = sum(
            item["single_women_population"] for item in sample_data
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"\n=== OLD AGE POPULATION AND SINGLE WOMEN SAMPLE DATA SUMMARY ==="
            )
        )
        self.stdout.write(f"Records created: {created_count}")
        self.stdout.write(f"Records updated: {updated_count}")
        self.stdout.write(f"Total records: {created_count + updated_count}")
        self.stdout.write(f"\n=== POPULATION STATISTICS ===")
        self.stdout.write(f"Total Male Elderly: {total_male_elderly:,}")
        self.stdout.write(f"Total Female Elderly: {total_female_elderly:,}")
        self.stdout.write(f"Total Elderly Population: {total_elderly:,}")
        self.stdout.write(f"Total Single Women: {total_single_women:,}")
        self.stdout.write(
            f"Gender Ratio (Female:Male): {total_female_elderly/total_male_elderly:.2f}:1"
        )

        # Ward-wise summary
        self.stdout.write(f"\n=== WARD-WISE BREAKDOWN ===")
        for data in sample_data:
            total_ward_elderly = (
                data["male_old_age_population"] + data["female_old_age_population"]
            )
            female_percentage = (
                (data["female_old_age_population"] / total_ward_elderly * 100)
                if total_ward_elderly > 0
                else 0
            )
            self.stdout.write(
                f"Ward {data['ward_number']}: "
                f"Total elderly: {total_ward_elderly:,} "
                f"(Male: {data['male_old_age_population']:,}, "
                f"Female: {data['female_old_age_population']:,} - {female_percentage:.1f}%)"
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"\n✅ Old age population and single women sample data loaded successfully!"
            )
        )
