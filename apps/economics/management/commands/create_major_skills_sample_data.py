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
            (1, "SELF_PROTECTION_RELATED", 21),
            (1, "ENGINEERING_DESIGN_RELATED", 10),
            (1, "COMPUTER_SCIENCE_RELATED", 5),
            (1, "AGRICULTURE_RELATED", 30),
            (1, "BEUATICIAN_RELATED", 16),
            (1, "SEWING_RELATED", 59),
            (1, "PLUMBING", 2),
            (1, "ELECTRICITY_INSTALLMENT_RELATED", 10),
            (1, "HUMAN_HEALTH_RELATED", 35),
            (1, "MECHANICS_RELATED", 3),
            (1, "TEACHING_RELATED", 64),
            (1, "DRIVING_RELATED", 50),
            (1, "LITERARY_CREATION_RELATED", 3),
            (1, "CARPENTERY_RELATED", 31),
            (1, "HOTEL_RESTAURANT_RELATED", 28),
            (2, "SELF_PROTECTION_RELATED", 38),
            (2, "ENGINEERING_DESIGN_RELATED", 5),
            (2, "COMPUTER_SCIENCE_RELATED", 15),
            (2, "AGRICULTURE_RELATED", 24),
            (2, "BEUATICIAN_RELATED", 3),
            (2, "MUSIC_DRAMA_RELATED", 1),
            (2, "SHOEMAKING_RELATED", 2),
            (2, "ANIMAL_HEALTH_RELATED", 3),
            (2, "SEWING_RELATED", 59),
            (2, "PLUMBING", 3),
            (2, "FURNITURE_RELATED", 3),
            (2, "ELECTRICITY_INSTALLMENT_RELATED", 8),
            (2, "HUMAN_HEALTH_RELATED", 8),
            (2, "MECHANICS_RELATED", 3),
            (2, "RADIO_TELEVISION_ELECTRICAL_REPAIR", 2),
            (2, "TEACHING_RELATED", 59),
            (2, "DRIVING_RELATED", 38),
            (2, "LITERARY_CREATION_RELATED", 1),
            (2, "CARPENTERY_RELATED", 23),
            (2, "HANDICRAFT_RELATED", 3),
            (2, "HOTEL_RESTAURANT_RELATED", 14),
            (3, "SELF_PROTECTION_RELATED", 32),
            (3, "ENGINEERING_DESIGN_RELATED", 15),
            (3, "COMPUTER_SCIENCE_RELATED", 16),
            (3, "AGRICULTURE_RELATED", 40),
            (3, "BEUATICIAN_RELATED", 8),
            (3, "MUSIC_DRAMA_RELATED", 4),
            (3, "PRINTING_RELATED", 1),
            (3, "ANIMAL_HEALTH_RELATED", 1),
            (3, "SEWING_RELATED", 154),
            (3, "PLUMBING", 8),
            (3, "FURNITURE_RELATED", 5),
            (3, "ELECTRICITY_INSTALLMENT_RELATED", 18),
            (3, "HUMAN_HEALTH_RELATED", 17),
            (3, "MECHANICS_RELATED", 3),
            (3, "RADIO_TELEVISION_ELECTRICAL_REPAIR", 5),
            (3, "TEACHING_RELATED", 68),
            (3, "DRIVING_RELATED", 44),
            (3, "CARPENTERY_RELATED", 46),
            (3, "HANDICRAFT_RELATED", 2),
            (3, "HOTEL_RESTAURANT_RELATED", 36),
            (4, "SELF_PROTECTION_RELATED", 11),
            (4, "ENGINEERING_DESIGN_RELATED", 16),
            (4, "COMPUTER_SCIENCE_RELATED", 8),
            (4, "AGRICULTURE_RELATED", 79),
            (4, "BEUATICIAN_RELATED", 6),
            (4, "PRINTING_RELATED", 2),
            (4, "LAND_SURVEY_RELATED", 1),
            (4, "ANIMAL_HEALTH_RELATED", 4),
            (4, "SEWING_RELATED", 94),
            (4, "PLUMBING", 5),
            (4, "FURNITURE_RELATED", 3),
            (4, "ELECTRICITY_INSTALLMENT_RELATED", 11),
            (4, "HUMAN_HEALTH_RELATED", 37),
            (4, "MECHANICS_RELATED", 11),
            (4, "RADIO_TELEVISION_ELECTRICAL_REPAIR", 7),
            (4, "TEACHING_RELATED", 75),
            (4, "DRIVING_RELATED", 52),
            (4, "CARPENTERY_RELATED", 76),
            (4, "HANDICRAFT_RELATED", 2),
            (4, "HOTEL_RESTAURANT_RELATED", 22),
            (5, "SELF_PROTECTION_RELATED", 42),
            (5, "ENGINEERING_DESIGN_RELATED", 9),
            (5, "COMPUTER_SCIENCE_RELATED", 41),
            (5, "AGRICULTURE_RELATED", 112),
            (5, "BEUATICIAN_RELATED", 13),
            (5, "JWELLERY_MAKING_RELATED", 1),
            (5, "MUSIC_DRAMA_RELATED", 14),
            (5, "PRINTING_RELATED", 3),
            (5, "LAND_SURVEY_RELATED", 7),
            (5, "SHOEMAKING_RELATED", 5),
            (5, "ANIMAL_HEALTH_RELATED", 12),
            (5, "SEWING_RELATED", 205),
            (5, "PLUMBING", 19),
            (5, "FURNITURE_RELATED", 11),
            (5, "ELECTRICITY_INSTALLMENT_RELATED", 21),
            (5, "HUMAN_HEALTH_RELATED", 35),
            (5, "MECHANICS_RELATED", 25),
            (5, "RADIO_TELEVISION_ELECTRICAL_REPAIR", 4),
            (5, "TEACHING_RELATED", 172),
            (5, "PHOTOGRAPHY_RELATED", 3),
            (5, "DRIVING_RELATED", 111),
            (5, "LITERARY_CREATION_RELATED", 1),
            (5, "CARPENTERY_RELATED", 319),
            (5, "HANDICRAFT_RELATED", 5),
            (5, "HOTEL_RESTAURANT_RELATED", 103),
            (6, "SELF_PROTECTION_RELATED", 7),
            (6, "ENGINEERING_DESIGN_RELATED", 10),
            (6, "COMPUTER_SCIENCE_RELATED", 44),
            (6, "AGRICULTURE_RELATED", 66),
            (6, "BEUATICIAN_RELATED", 18),
            (6, "JWELLERY_MAKING_RELATED", 5),
            (6, "MUSIC_DRAMA_RELATED", 12),
            (6, "PRINTING_RELATED", 3),
            (6, "LAND_SURVEY_RELATED", 2),
            (6, "ANIMAL_HEALTH_RELATED", 13),
            (6, "SEWING_RELATED", 106),
            (6, "PLUMBING", 16),
            (6, "FURNITURE_RELATED", 12),
            (6, "ELECTRICITY_INSTALLMENT_RELATED", 20),
            (6, "HUMAN_HEALTH_RELATED", 33),
            (6, "STONEWORK_WOODWORK", 8),
            (6, "MECHANICS_RELATED", 10),
            (6, "RADIO_TELEVISION_ELECTRICAL_REPAIR", 3),
            (6, "TEACHING_RELATED", 568),
            (6, "PHOTOGRAPHY_RELATED", 1),
            (6, "DRIVING_RELATED", 56),
            (6, "LITERARY_CREATION_RELATED", 3),
            (6, "CARPENTERY_RELATED", 47),
            (6, "HANDICRAFT_RELATED", 5),
            (6, "HOTEL_RESTAURANT_RELATED", 63),
            (7, "SELF_PROTECTION_RELATED", 4),
            (7, "ENGINEERING_DESIGN_RELATED", 5),
            (7, "COMPUTER_SCIENCE_RELATED", 11),
            (7, "AGRICULTURE_RELATED", 31),
            (7, "JWELLERY_MAKING_RELATED", 2),
            (7, "MUSIC_DRAMA_RELATED", 3),
            (7, "ANIMAL_HEALTH_RELATED", 7),
            (7, "SEWING_RELATED", 62),
            (7, "PLUMBING", 2),
            (7, "FURNITURE_RELATED", 4),
            (7, "ELECTRICITY_INSTALLMENT_RELATED", 2),
            (7, "HUMAN_HEALTH_RELATED", 11),
            (7, "STONEWORK_WOODWORK", 2),
            (7, "MECHANICS_RELATED", 4),
            (7, "RADIO_TELEVISION_ELECTRICAL_REPAIR", 3),
            (7, "TEACHING_RELATED", 98),
            (7, "PHOTOGRAPHY_RELATED", 1),
            (7, "DRIVING_RELATED", 22),
            (7, "CARPENTERY_RELATED", 43),
            (7, "HOTEL_RESTAURANT_RELATED", 9),
            (8, "ANIMAL_HEALTH_RELATED", 1),
            (8, "SEWING_RELATED", 1),
            (8, "ELECTRICITY_INSTALLMENT_RELATED", 4),
            (8, "HUMAN_HEALTH_RELATED", 2),
            (8, "STONEWORK_WOODWORK", 1),
            (8, "TEACHING_RELATED", 3),
            (8, "CARPENTERY_RELATED", 5),
            (8, "HOTEL_RESTAURANT_RELATED", 12),
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
