"""
Management command to create sample data for ward wise major subjects.
"""

from django.core.management.base import BaseCommand
from apps.social.models import WardWiseMajorSubject


class Command(BaseCommand):
    help = "Create sample data for WardWiseMajorSubject"

    def handle(self, *args, **options):
        # Sample data based on the provided JSON
        sample_data = [
            {"ward_number": 1, "subject_type": "COMMERCE", "population": 3},
            {"ward_number": 1, "subject_type": "ECONOMICS", "population": 35},
            {"ward_number": 1, "subject_type": "EDUCATION", "population": 21},
            {"ward_number": 1, "subject_type": "EDUCATIONAL_SCIENCE", "population": 2},
            {"ward_number": 1, "subject_type": "ENGINEERING", "population": 12},
            {"ward_number": 1, "subject_type": "ENGLISH", "population": 18},
            {"ward_number": 1, "subject_type": "HINDI", "population": 2},
            {"ward_number": 1, "subject_type": "HISTORY", "population": 4},
            {"ward_number": 1, "subject_type": "HUMANITIES", "population": 3},
            {"ward_number": 1, "subject_type": "MANAGEMENT", "population": 39},
            {"ward_number": 1, "subject_type": "MEDICINE", "population": 14},
            {"ward_number": 1, "subject_type": "NEPALI", "population": 32},
            {"ward_number": 1, "subject_type": "OTHER", "population": 6},
            {"ward_number": 1, "subject_type": "POPULATION_STUDY", "population": 22},
            {"ward_number": 1, "subject_type": "SCIENCE", "population": 24},
            {"ward_number": 1, "subject_type": "SOCIAL_SCIENCES", "population": 2},
            {"ward_number": 1, "subject_type": "STATISTICS", "population": 3},
            {"ward_number": 2, "subject_type": "CHEMISTRY", "population": 1},
            {"ward_number": 2, "subject_type": "COMMERCE", "population": 5},
            {"ward_number": 2, "subject_type": "ECONOMICS", "population": 24},
            {"ward_number": 2, "subject_type": "EDUCATION", "population": 32},
            {"ward_number": 2, "subject_type": "EDUCATIONAL_SCIENCE", "population": 12},
            {"ward_number": 2, "subject_type": "ENGINEERING", "population": 3},
            {"ward_number": 2, "subject_type": "ENGLISH", "population": 13},
            {
                "ward_number": 2,
                "subject_type": "FORESTRY_AND_AGRICULTRE",
                "population": 2,
            },
            {"ward_number": 2, "subject_type": "HOME_ECONOMICS", "population": 2},
            {"ward_number": 2, "subject_type": "HUMANITIES", "population": 9},
            {
                "ward_number": 2,
                "subject_type": "INFORMATION_TECHNOLOGY",
                "population": 3,
            },
            {"ward_number": 2, "subject_type": "MANAGEMENT", "population": 34},
            {"ward_number": 2, "subject_type": "MEDICINE", "population": 1},
            {"ward_number": 2, "subject_type": "NEPALI", "population": 14},
            {"ward_number": 2, "subject_type": "OTHER", "population": 6},
            {"ward_number": 2, "subject_type": "POLITCAL_SCIENCE", "population": 1},
            {"ward_number": 2, "subject_type": "POPULATION_STUDY", "population": 4},
            {"ward_number": 2, "subject_type": "SCIENCE", "population": 8},
            {"ward_number": 2, "subject_type": "SOCIAL_SCIENCES", "population": 11},
            {"ward_number": 2, "subject_type": "STATISTICS", "population": 5},
            {"ward_number": 3, "subject_type": "ARTS", "population": 1},
            {"ward_number": 3, "subject_type": "CHEMISTRY", "population": 1},
            {"ward_number": 3, "subject_type": "COMMERCE", "population": 14},
            {"ward_number": 3, "subject_type": "ECONOMICS", "population": 44},
            {"ward_number": 3, "subject_type": "EDUCATION", "population": 14},
            {"ward_number": 3, "subject_type": "EDUCATIONAL_SCIENCE", "population": 11},
            {"ward_number": 3, "subject_type": "ENGINEERING", "population": 8},
            {"ward_number": 3, "subject_type": "ENGLISH", "population": 10},
            {
                "ward_number": 3,
                "subject_type": "FORESTRY_AND_AGRICULTRE",
                "population": 2,
            },
            {"ward_number": 3, "subject_type": "GEOGRAPHY", "population": 1},
            {"ward_number": 3, "subject_type": "HISTORY", "population": 1},
            {"ward_number": 3, "subject_type": "HUMANITIES", "population": 10},
            {
                "ward_number": 3,
                "subject_type": "INFORMATION_TECHNOLOGY",
                "population": 1,
            },
            {"ward_number": 3, "subject_type": "MANAGEMENT", "population": 33},
            {"ward_number": 3, "subject_type": "MEDICINE", "population": 3},
            {"ward_number": 3, "subject_type": "NEPALI", "population": 20},
            {"ward_number": 3, "subject_type": "OTHER", "population": 11},
            {"ward_number": 3, "subject_type": "POLITCAL_SCIENCE", "population": 2},
            {"ward_number": 3, "subject_type": "POPULATION_STUDY", "population": 4},
            {"ward_number": 3, "subject_type": "PSYCHOLOGY", "population": 6},
            {"ward_number": 3, "subject_type": "SCIENCE", "population": 11},
            {"ward_number": 3, "subject_type": "SOCIAL_SCIENCES", "population": 3},
            {"ward_number": 3, "subject_type": "STATISTICS", "population": 1},
            {"ward_number": 4, "subject_type": "BOTANY", "population": 2},
            {"ward_number": 4, "subject_type": "COMMERCE", "population": 34},
            {"ward_number": 4, "subject_type": "ECONOMICS", "population": 56},
            {"ward_number": 4, "subject_type": "EDUCATION", "population": 29},
            {"ward_number": 4, "subject_type": "EDUCATIONAL_SCIENCE", "population": 7},
            {"ward_number": 4, "subject_type": "ENGINEERING", "population": 21},
            {"ward_number": 4, "subject_type": "ENGLISH", "population": 31},
            {
                "ward_number": 4,
                "subject_type": "FORESTRY_AND_AGRICULTRE",
                "population": 13,
            },
            {"ward_number": 4, "subject_type": "GEOGRAPHY", "population": 2},
            {"ward_number": 4, "subject_type": "HISTORY", "population": 1},
            {"ward_number": 4, "subject_type": "HOME_ECONOMICS", "population": 1},
            {"ward_number": 4, "subject_type": "HUMANITIES", "population": 3},
            {
                "ward_number": 4,
                "subject_type": "INFORMATION_TECHNOLOGY",
                "population": 4,
            },
            {"ward_number": 4, "subject_type": "MANAGEMENT", "population": 10},
            {"ward_number": 4, "subject_type": "MEDICINE", "population": 32},
            {"ward_number": 4, "subject_type": "NEPALI", "population": 35},
            {"ward_number": 4, "subject_type": "OTHER", "population": 10},
            {"ward_number": 4, "subject_type": "POLITCAL_SCIENCE", "population": 1},
            {"ward_number": 4, "subject_type": "POPULATION_STUDY", "population": 6},
            {"ward_number": 4, "subject_type": "PSYCHOLOGY", "population": 6},
            {"ward_number": 4, "subject_type": "SANSKRIT", "population": 3},
            {"ward_number": 4, "subject_type": "SCIENCE", "population": 21},
            {"ward_number": 4, "subject_type": "SOCIAL_SCIENCES", "population": 5},
            {"ward_number": 5, "subject_type": "BIOLOGY", "population": 2},
            {"ward_number": 5, "subject_type": "BOTANY", "population": 1},
            {"ward_number": 5, "subject_type": "CHEMISTRY", "population": 2},
            {"ward_number": 5, "subject_type": "COMMERCE", "population": 29},
            {"ward_number": 5, "subject_type": "ECONOMICS", "population": 19},
            {"ward_number": 5, "subject_type": "EDUCATION", "population": 25},
            {"ward_number": 5, "subject_type": "EDUCATIONAL_SCIENCE", "population": 10},
            {"ward_number": 5, "subject_type": "ENGINEERING", "population": 7},
            {"ward_number": 5, "subject_type": "ENGLISH", "population": 37},
            {
                "ward_number": 5,
                "subject_type": "FORESTRY_AND_AGRICULTRE",
                "population": 4,
            },
            {"ward_number": 5, "subject_type": "HOME_ECONOMICS", "population": 7},
            {"ward_number": 5, "subject_type": "HUMANITIES", "population": 10},
            {
                "ward_number": 5,
                "subject_type": "INFORMATION_TECHNOLOGY",
                "population": 2,
            },
            {"ward_number": 5, "subject_type": "MANAGEMENT", "population": 33},
            {"ward_number": 5, "subject_type": "MEDICINE", "population": 8},
            {"ward_number": 5, "subject_type": "NEPALI", "population": 25},
            {"ward_number": 5, "subject_type": "OTHER", "population": 3},
            {"ward_number": 5, "subject_type": "PHYSICS", "population": 1},
            {"ward_number": 5, "subject_type": "POPULATION_STUDY", "population": 4},
            {"ward_number": 5, "subject_type": "PSYCHOLOGY", "population": 10},
            {"ward_number": 5, "subject_type": "RURAL_DEVELOPMENT", "population": 1},
            {"ward_number": 5, "subject_type": "SCIENCE", "population": 12},
            {"ward_number": 5, "subject_type": "SOCIAL_SCIENCES", "population": 1},
            {"ward_number": 5, "subject_type": "STATISTICS", "population": 15},
            {"ward_number": 6, "subject_type": "BIOLOGY", "population": 1},
            {"ward_number": 6, "subject_type": "CHEMISTRY", "population": 3},
            {"ward_number": 6, "subject_type": "COMMERCE", "population": 4},
            {"ward_number": 6, "subject_type": "ECONOMICS", "population": 37},
            {"ward_number": 6, "subject_type": "EDUCATION", "population": 35},
            {"ward_number": 6, "subject_type": "EDUCATIONAL_SCIENCE", "population": 9},
            {"ward_number": 6, "subject_type": "ENGINEERING", "population": 31},
            {"ward_number": 6, "subject_type": "ENGLISH", "population": 55},
            {
                "ward_number": 6,
                "subject_type": "FORESTRY_AND_AGRICULTRE",
                "population": 3,
            },
            {"ward_number": 6, "subject_type": "GEOGRAPHY", "population": 3},
            {"ward_number": 6, "subject_type": "HINDI", "population": 1},
            {"ward_number": 6, "subject_type": "HISTORY", "population": 1},
            {"ward_number": 6, "subject_type": "HOME_ECONOMICS", "population": 4},
            {"ward_number": 6, "subject_type": "HUMANITIES", "population": 3},
            {
                "ward_number": 6,
                "subject_type": "INFORMATION_TECHNOLOGY",
                "population": 5,
            },
            {"ward_number": 6, "subject_type": "MANAGEMENT", "population": 57},
            {"ward_number": 6, "subject_type": "MEDICINE", "population": 10},
            {"ward_number": 6, "subject_type": "NEPALI", "population": 56},
            {"ward_number": 6, "subject_type": "OTHER", "population": 15},
            {"ward_number": 6, "subject_type": "PHYSICS", "population": 2},
            {"ward_number": 6, "subject_type": "POLITCAL_SCIENCE", "population": 1},
            {"ward_number": 6, "subject_type": "POPULATION_STUDY", "population": 6},
            {"ward_number": 6, "subject_type": "RURAL_DEVELOPMENT", "population": 9},
            {"ward_number": 6, "subject_type": "SCIENCE", "population": 29},
            {"ward_number": 6, "subject_type": "SOCIAL_SCIENCES", "population": 3},
            {"ward_number": 6, "subject_type": "STATISTICS", "population": 28},
            {"ward_number": 7, "subject_type": "CHEMISTRY", "population": 6},
            {"ward_number": 7, "subject_type": "ECONOMICS", "population": 35},
            {"ward_number": 7, "subject_type": "EDUCATION", "population": 20},
            {"ward_number": 7, "subject_type": "EDUCATIONAL_SCIENCE", "population": 2},
            {"ward_number": 7, "subject_type": "ENGINEERING", "population": 8},
            {"ward_number": 7, "subject_type": "ENGLISH", "population": 33},
            {
                "ward_number": 7,
                "subject_type": "FORESTRY_AND_AGRICULTRE",
                "population": 5,
            },
            {"ward_number": 7, "subject_type": "GEOGRAPHY", "population": 3},
            {"ward_number": 7, "subject_type": "HOME_ECONOMICS", "population": 3},
            {"ward_number": 7, "subject_type": "MANAGEMENT", "population": 98},
            {"ward_number": 7, "subject_type": "MEDICINE", "population": 16},
            {"ward_number": 7, "subject_type": "NEPALI", "population": 24},
            {"ward_number": 7, "subject_type": "OTHER", "population": 6},
            {"ward_number": 7, "subject_type": "PHYSICS", "population": 1},
            {"ward_number": 7, "subject_type": "POPULATION_STUDY", "population": 1},
            {"ward_number": 7, "subject_type": "PSYCHOLOGY", "population": 4},
            {"ward_number": 7, "subject_type": "RURAL_DEVELOPMENT", "population": 2},
            {"ward_number": 7, "subject_type": "SCIENCE", "population": 9},
            {"ward_number": 7, "subject_type": "SOCIAL_SCIENCES", "population": 3},
            {"ward_number": 7, "subject_type": "STATISTICS", "population": 12},
            {"ward_number": 8, "subject_type": "ECONOMICS", "population": 2},
            {"ward_number": 8, "subject_type": "NEPALI", "population": 2},
            {"ward_number": 8, "subject_type": "SCIENCE", "population": 3},
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
        wards_set = set()
        subjects_set = set()

        for data in sample_data:
            ward_num = data["ward_number"]
            subject = data["subject_type"]
            population = data["population"]
            wards_set.add(ward_num)
            subjects_set.add(subject)
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
            self.stdout.write(f"{i:2d}. {subject}: {population:,} ({percentage:.1f}%)")

        # Educational diversity analysis
        unique_subjects_per_ward = {}
        for ward_num in sorted(wards_set):
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
