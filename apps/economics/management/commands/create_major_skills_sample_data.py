"""
Management command to create sample data for Ward Wise Major Skills.
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from apps.economics.models import WardWiseMajorSkills, SkillTypeChoice
from apps.reports.utils.nepali_numbers import format_nepali_number


class Command(BaseCommand):
    help = "Create sample data for Ward Wise Major Skills"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before creating new data",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write("Clearing existing major skills data...")
            WardWiseMajorSkills.objects.all().delete()

        # Sample data based on provided information
        sample_data = [
            # Ward 1
            (1, "OTHER", 3027),  # Combined OTHER entries
            (1, "SEWING_RELATED", 21),
            (1, "TEACHING_RELATED", 20),
            (1, "CARPENTERY_RELATED", 19),
            (1, "DRIVING_RELATED", 17),
            (1, "AGRICULTURE_RELATED", 16),
            (1, "NONE", 8),
            (1, "PLUMBING", 6),
            (1, "FURNITURE_RELATED", 5),
            (1, "HUMAN_HEALTH_RELATED", 5),
            (1, "MECHANICS_RELATED", 5),
            (1, "MUSIC_DRAMA_RELATED", 5),
            (1, "SELF_PROTECTION_RELATED", 4),
            (1, "ENGINEERING_DESIGN_RELATED", 4),
            (1, "COMPUTER_SCIENCE_RELATED", 1),
            # Ward 2
            (2, "OTHER", 214),  # Combined OTHER entries
            (2, "CARPENTERY_RELATED", 146),
            (2, "TEACHING_RELATED", 145),
            (2, "AGRICULTURE_RELATED", 125),
            (2, "DRIVING_RELATED", 43),
            (2, "SEWING_RELATED", 36),
            (2, "COMPUTER_SCIENCE_RELATED", 34),
            (2, "HOTEL_RESTAURANT_RELATED", 20),
            (2, "NONE", 10),
            (2, "HUMAN_HEALTH_RELATED", 8),
            (2, "PLUMBING", 7),
            (2, "SELF_PROTECTION_RELATED", 6),
            (2, "FURNITURE_RELATED", 5),
            (2, "ELECTRICITY_INSTALLMENT_RELATED", 5),
            (2, "ENGINEERING_DESIGN_RELATED", 4),
            (2, "MECHANICS_RELATED", 4),
            (2, "HANDICRAFT_RELATED", 3),
            (2, "MUSIC_DRAMA_RELATED", 2),
            (2, "BEUATICIAN_RELATED", 2),
            (2, "RADIO_TELEVISION_ELECTRICAL_REPAIR", 2),
            (2, "LAND_SURVEY_RELATED", 1),
            # Ward 3
            (3, "OTHER", 244),  # Combined OTHER entries
            (3, "TEACHING_RELATED", 46),
            (3, "AGRICULTURE_RELATED", 34),
            (3, "CARPENTERY_RELATED", 18),
            (3, "NONE", 17),
            (3, "SEWING_RELATED", 10),
            (3, "ANIMAL_HEALTH_RELATED", 10),
            (3, "HUMAN_HEALTH_RELATED", 8),
            (3, "SELF_PROTECTION_RELATED", 7),
            (3, "DRIVING_RELATED", 7),
            (3, "MUSIC_DRAMA_RELATED", 5),
            (3, "ENGINEERING_DESIGN_RELATED", 4),
            (3, "ELECTRICITY_INSTALLMENT_RELATED", 3),
            (3, "PLUMBING", 2),
            (3, "COMPUTER_SCIENCE_RELATED", 1),
            (3, "LAND_SURVEY_RELATED", 1),
            (3, "PHOTOGRAPHY_RELATED", 1),
            # Ward 4
            (4, "OTHER", 351),  # Combined OTHER entries
            (4, "TEACHING_RELATED", 61),
            (4, "CARPENTERY_RELATED", 44),
            (4, "HOTEL_RESTAURANT_RELATED", 25),
            (4, "DRIVING_RELATED", 20),
            (4, "SEWING_RELATED", 18),
            (4, "HUMAN_HEALTH_RELATED", 16),
            (4, "NONE", 14),
            (4, "AGRICULTURE_RELATED", 11),
            (4, "COMPUTER_SCIENCE_RELATED", 9),
            (4, "FURNITURE_RELATED", 8),
            (4, "ANIMAL_HEALTH_RELATED", 7),
            (4, "SELF_PROTECTION_RELATED", 5),
            (4, "ELECTRICITY_INSTALLMENT_RELATED", 5),
            (4, "MUSIC_DRAMA_RELATED", 5),
            (4, "ENGINEERING_DESIGN_RELATED", 2),
            (4, "LAND_SURVEY_RELATED", 2),
            (4, "LITERARY_CREATION_RELATED", 2),
            (4, "BEUATICIAN_RELATED", 1),
            # Ward 5
            (5, "OTHER", 1446),
            (5, "TEACHING_RELATED", 88),
            (5, "DRIVING_RELATED", 30),
            (5, "NONE", 29),
            (5, "SEWING_RELATED", 24),
            (5, "AGRICULTURE_RELATED", 22),
            (5, "JWELLERY_MAKING_RELATED", 13),
            (5, "CARPENTERY_RELATED", 12),
            (5, "ELECTRICITY_INSTALLMENT_RELATED", 11),
            (5, "COMPUTER_SCIENCE_RELATED", 10),
            (5, "PLUMBING", 5),
            (5, "STONEWORK_WOODWORK", 5),
            (5, "HANDICRAFT_RELATED", 5),
            (5, "SELF_PROTECTION_RELATED", 4),
            (5, "FURNITURE_RELATED", 2),
            (5, "MECHANICS_RELATED", 2),
            (5, "BEUATICIAN_RELATED", 1),
            # Ward 6
            (6, "OTHER", 948),  # Combined OTHER entries
            (6, "TEACHING_RELATED", 389),
            (6, "SEWING_RELATED", 18),
            (6, "NONE", 13),
            (6, "HUMAN_HEALTH_RELATED", 9),
            (6, "COMPUTER_SCIENCE_RELATED", 7),
            (6, "HANDICRAFT_RELATED", 5),
            (6, "AGRICULTURE_RELATED", 4),
            (6, "JWELLERY_MAKING_RELATED", 3),
            (6, "CARPENTERY_RELATED", 2),
            (6, "DRIVING_RELATED", 2),
            (6, "ENGINEERING_DESIGN_RELATED", 2),
            (6, "FURNITURE_RELATED", 2),
            (6, "ELECTRICITY_INSTALLMENT_RELATED", 2),
            (6, "MUSIC_DRAMA_RELATED", 2),
            (6, "SELF_PROTECTION_RELATED", 1),
            (6, "STONEWORK_WOODWORK", 1),
            (6, "MECHANICS_RELATED", 1),
            (6, "PHOTOGRAPHY_RELATED", 1),
            # Ward 7
            (7, "OTHER", 827),
            (7, "TEACHING_RELATED", 21),
            (7, "SEWING_RELATED", 16),
            (7, "HUMAN_HEALTH_RELATED", 11),
            (7, "NONE", 8),
            (7, "COMPUTER_SCIENCE_RELATED", 7),
            (7, "AGRICULTURE_RELATED", 4),
            (7, "DRIVING_RELATED", 4),
            (7, "SELF_PROTECTION_RELATED", 4),
            (7, "BEUATICIAN_RELATED", 4),
            (7, "ELECTRICITY_INSTALLMENT_RELATED", 3),
            (7, "CARPENTERY_RELATED", 2),
            (7, "HANDICRAFT_RELATED", 2),
            (7, "MUSIC_DRAMA_RELATED", 2),
            (7, "HOTEL_RESTAURANT_RELATED", 1),
        ]

        created_count = 0
        updated_count = 0

        with transaction.atomic():
            for ward_number, skill_type, population in sample_data:
                skill_obj, created = WardWiseMajorSkills.objects.get_or_create(
                    ward_number=ward_number,
                    skill_type=skill_type,
                    defaults={"population": population},
                )

                if created:
                    created_count += 1
                    self.stdout.write(
                        f"Created major skills data for Ward {ward_number}, "
                        f"Skill: {skill_type}, Population: {population}"
                    )
                else:
                    if skill_obj.population != population:
                        skill_obj.population = population
                        skill_obj.save()
                        updated_count += 1
                        self.stdout.write(
                            f"Updated major skills data for Ward {ward_number}, "
                            f"Skill: {skill_type}, Population: {population}"
                        )

        # Generate summary statistics
        total_records = WardWiseMajorSkills.objects.count()
        total_population = (
            WardWiseMajorSkills.objects.aggregate(total=models.Sum("population"))[
                "total"
            ]
            or 0
        )

        self.stdout.write("\n" + "=" * 50)
        self.stdout.write("MAJOR SKILLS SAMPLE DATA SUMMARY")
        self.stdout.write("=" * 50)
        self.stdout.write(f"Records created: {created_count}")
        self.stdout.write(f"Records updated: {updated_count}")
        self.stdout.write(f"Total records: {total_records}")
        self.stdout.write(f"Total population: {format_nepali_number(total_population)}")

        # Ward-wise totals
        self.stdout.write(f"\n=== WARD-WISE TOTALS ===")
        for ward_num in range(1, 8):
            ward_total = (
                WardWiseMajorSkills.objects.filter(ward_number=ward_num).aggregate(
                    total=models.Sum("population")
                )["total"]
                or 0
            )
            ward_percentage = (
                (ward_total / total_population * 100) if total_population > 0 else 0
            )
            self.stdout.write(
                f"Ward {ward_num}: {format_nepali_number(ward_total)} ({ward_percentage:.1f}%)"
            )

        # Top 10 skills
        self.stdout.write(f"\n=== TOP 10 SKILLS ===")
        skill_totals = {}
        for skill_choice in SkillTypeChoice.choices:
            skill_code = skill_choice[0]
            skill_name = skill_choice[1]
            skill_total = (
                WardWiseMajorSkills.objects.filter(skill_type=skill_code).aggregate(
                    total=models.Sum("population")
                )["total"]
                or 0
            )
            if skill_total > 0:
                skill_totals[skill_name] = skill_total

        # Sort by population and display top 10
        sorted_skills = sorted(skill_totals.items(), key=lambda x: x[1], reverse=True)
        for i, (skill_name, population) in enumerate(sorted_skills[:10], 1):
            percentage = (
                (population / total_population * 100) if total_population > 0 else 0
            )
            self.stdout.write(
                f"{i:2}. {skill_name}: {format_nepali_number(population)} ({percentage:.1f}%)"
            )

        # Skill diversity by ward
        self.stdout.write(f"\n=== SKILL DIVERSITY BY WARD ===")
        for ward_num in range(1, 8):
            skill_count = (
                WardWiseMajorSkills.objects.filter(ward_number=ward_num)
                .values("skill_type")
                .distinct()
                .count()
            )
            self.stdout.write(f"Ward {ward_num}: {skill_count} different skills")

        self.stdout.write(f"\n✅ Major skills sample data loaded successfully!")


# Import models at the module level for the aggregation
from django.db import models
