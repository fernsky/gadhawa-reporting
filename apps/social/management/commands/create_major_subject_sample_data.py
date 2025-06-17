"""
Management command to create sample data for ward wise major subjects.
"""

from django.core.management.base import BaseCommand
from apps.social.models import WardWiseMajorSubject


class Command(BaseCommand):
    help = "Create sample data for WardWiseMajorSubject"

    def handle(self, *args, **options):
        # Sample data based on the provided information
        sample_data = [
            # Ward 1
            {"ward_number": 1, "subject_type": "ECONOMICS", "population": 3},
            {"ward_number": 1, "subject_type": "EDUCATION", "population": 11},
            {"ward_number": 1, "subject_type": "ENGLISH", "population": 6},
            {"ward_number": 1, "subject_type": "NEPALI", "population": 24},
            {"ward_number": 1, "subject_type": "OTHER", "population": 3082},
            {"ward_number": 1, "subject_type": "POPULATION_STUDY", "population": 1},
            # Ward 2
            {"ward_number": 2, "subject_type": "EDUCATION", "population": 5},
            {"ward_number": 2, "subject_type": "ENGINEERING", "population": 2},
            {"ward_number": 2, "subject_type": "ENGLISH", "population": 20},
            {"ward_number": 2, "subject_type": "GEOGRAPHY", "population": 4},
            {"ward_number": 2, "subject_type": "HOME_ECONOMICS", "population": 1},
            {
                "ward_number": 2,
                "subject_type": "INFORMATION_TECHNOLOGY",
                "population": 1,
            },
            {"ward_number": 2, "subject_type": "MEDICINE", "population": 1},
            {"ward_number": 2, "subject_type": "NEPALI", "population": 7},
            {"ward_number": 2, "subject_type": "OTHER", "population": 241},
            {"ward_number": 2, "subject_type": "POPULATION_STUDY", "population": 2},
            {"ward_number": 2, "subject_type": "SCIENCE", "population": 1},
            # Ward 3
            {"ward_number": 3, "subject_type": "EDUCATION", "population": 2},
            {"ward_number": 3, "subject_type": "ENGINEERING", "population": 3},
            {"ward_number": 3, "subject_type": "ENGLISH", "population": 3},
            {"ward_number": 3, "subject_type": "HISTORY", "population": 1},
            {"ward_number": 3, "subject_type": "NEPALI", "population": 9},
            {"ward_number": 3, "subject_type": "OTHER", "population": 264},
            {"ward_number": 3, "subject_type": "PHYSICS", "population": 1},
            {"ward_number": 3, "subject_type": "POPULATION_STUDY", "population": 1},
            {"ward_number": 3, "subject_type": "SCIENCE", "population": 2},
            # Ward 4
            {"ward_number": 4, "subject_type": "COMMERCE", "population": 4},
            {"ward_number": 4, "subject_type": "EDUCATION", "population": 3},
            {"ward_number": 4, "subject_type": "ENGINEERING", "population": 1},
            {"ward_number": 4, "subject_type": "ENGLISH", "population": 3},
            {"ward_number": 4, "subject_type": "HOME_ECONOMICS", "population": 2},
            {"ward_number": 4, "subject_type": "MEDICINE", "population": 2},
            {"ward_number": 4, "subject_type": "NEPALI", "population": 5},
            {"ward_number": 4, "subject_type": "OTHER", "population": 370},
            {"ward_number": 4, "subject_type": "POPULATION_STUDY", "population": 1},
            {"ward_number": 4, "subject_type": "SCIENCE", "population": 1},
            {"ward_number": 4, "subject_type": "SOCIAL_SCIENCES", "population": 1},
            # Ward 5
            {"ward_number": 5, "subject_type": "BIOLOGY", "population": 8},
            {"ward_number": 5, "subject_type": "ECONOMICS", "population": 10},
            {"ward_number": 5, "subject_type": "EDUCATION", "population": 3},
            {"ward_number": 5, "subject_type": "ENGINEERING", "population": 10},
            {"ward_number": 5, "subject_type": "ENGLISH", "population": 13},
            {
                "ward_number": 5,
                "subject_type": "FORESTRY_AND_AGRICULTURE",
                "population": 5,
            },
            {"ward_number": 5, "subject_type": "MEDICINE", "population": 4},
            {"ward_number": 5, "subject_type": "NEPALI", "population": 13},
            {"ward_number": 5, "subject_type": "OTHER", "population": 1552},
            {"ward_number": 5, "subject_type": "PSYCHOLOGY", "population": 1},
            {"ward_number": 5, "subject_type": "SCIENCE", "population": 14},
            {"ward_number": 5, "subject_type": "STATISTICS", "population": 3},
            # Ward 6
            {"ward_number": 6, "subject_type": "EDUCATION", "population": 1},
            {"ward_number": 6, "subject_type": "ENGLISH", "population": 8},
            {"ward_number": 6, "subject_type": "HOME_ECONOMICS", "population": 3},
            {"ward_number": 6, "subject_type": "MEDICINE", "population": 1},
            {"ward_number": 6, "subject_type": "NEPALI", "population": 6},
            {"ward_number": 6, "subject_type": "OTHER", "population": 893},
            {"ward_number": 6, "subject_type": "SCIENCE", "population": 6},
            # Ward 7
            {"ward_number": 7, "subject_type": "ECONOMICS", "population": 3},
            {"ward_number": 7, "subject_type": "EDUCATION", "population": 7},
            {"ward_number": 7, "subject_type": "ENGLISH", "population": 18},
            {"ward_number": 7, "subject_type": "HOME_ECONOMICS", "population": 1},
            {"ward_number": 7, "subject_type": "MANAGEMENT", "population": 1},
            {"ward_number": 7, "subject_type": "NEPALI", "population": 9},
            {"ward_number": 7, "subject_type": "OTHER", "population": 847},
        ]

        created_count = 0
        updated_count = 0

        for data in sample_data:
            obj, created = WardWiseMajorSubject.objects.update_or_create(
                ward_number=data["ward_number"],
                subject_type=data["subject_type"],
                defaults={
                    "population": data["population"],
                },
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created major subject data for Ward {data['ward_number']}, "
                        f"Subject: {data['subject_type']}, Population: {data['population']}"
                    )
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(
                        f"Updated major subject data for Ward {data['ward_number']}, "
                        f"Subject: {data['subject_type']}, Population: {data['population']}"
                    )
                )

        # Calculate summary statistics
        ward_totals = {}
        subject_totals = {}
        total_population = 0

        for data in sample_data:
            ward_num = data["ward_number"]
            subject = data["subject_type"]
            population = data["population"]

            # Ward totals
            if ward_num not in ward_totals:
                ward_totals[ward_num] = 0
            ward_totals[ward_num] += population

            # Subject totals
            if subject not in subject_totals:
                subject_totals[subject] = 0
            subject_totals[subject] += population

            total_population += population

        self.stdout.write(
            self.style.SUCCESS(f"\n=== MAJOR SUBJECT SAMPLE DATA SUMMARY ===")
        )
        self.stdout.write(f"Records created: {created_count}")
        self.stdout.write(f"Records updated: {updated_count}")
        self.stdout.write(f"Total records: {created_count + updated_count}")
        self.stdout.write(f"Total population: {total_population:,}")

        self.stdout.write(f"\n=== WARD-WISE TOTALS ===")
        for ward_num in sorted(ward_totals.keys()):
            percentage = (
                (ward_totals[ward_num] / total_population * 100)
                if total_population > 0
                else 0
            )
            self.stdout.write(
                f"Ward {ward_num}: {ward_totals[ward_num]:,} ({percentage:.1f}%)"
            )

        # Show top subjects
        sorted_subjects = sorted(
            subject_totals.items(), key=lambda x: x[1], reverse=True
        )
        self.stdout.write(f"\n=== TOP 10 SUBJECTS ===")
        for i, (subject, population) in enumerate(sorted_subjects[:10], 1):
            percentage = (
                (population / total_population * 100) if total_population > 0 else 0
            )
            subject_display = dict(
                WardWiseMajorSubject._meta.get_field("subject_type").choices
            ).get(subject, subject)
            self.stdout.write(
                f"{i:2d}. {subject_display}: {population:,} ({percentage:.1f}%)"
            )

        # Educational diversity analysis
        unique_subjects_per_ward = {}
        for ward_num in range(1, 8):
            unique_subjects = len(
                [d for d in sample_data if d["ward_number"] == ward_num]
            )
            unique_subjects_per_ward[ward_num] = unique_subjects

        self.stdout.write(f"\n=== EDUCATIONAL DIVERSITY BY WARD ===")
        for ward_num in sorted(unique_subjects_per_ward.keys()):
            self.stdout.write(
                f"Ward {ward_num}: {unique_subjects_per_ward[ward_num]} different subjects"
            )

        self.stdout.write(
            self.style.SUCCESS(f"\n✅ Major subject sample data loaded successfully!")
        )
