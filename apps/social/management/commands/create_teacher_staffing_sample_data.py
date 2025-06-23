"""
Management command to create teacher and educational manpower sample data

This command creates comprehensive sample data for teacher staffing details
based on the provided JSON data structure for Section 5.1.5.
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from apps.social.models import (
    WardWiseTeacherStaffing,
    WardWiseTeacherSummary,
    TeacherLevelChoice,
    TeacherPositionTypeChoice,
    SchoolLevelChoice,
)


class Command(BaseCommand):
    help = "Create sample data for Teacher and Educational Manpower Details (५.१.५)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete existing data before creating new data",
        )

    def handle(self, *args, **options):
        if options["reset"]:
            self.stdout.write("Clearing existing teacher staffing data...")
            WardWiseTeacherStaffing.objects.all().delete()
            WardWiseTeacherSummary.objects.all().delete()

        self.stdout.write(
            "Creating teacher and educational manpower sample data based on actual data..."
        )

        # Sample data representing actual teacher staffing by school
        teacher_data = [
            {
                "s_n": "१",
                "school_name_full": "नेपाल राष्ट्रिय मा.वि., गढवा-१",
                "ward_number": 1,
                "institution_level": "SECONDARY",
                "staffing_by_level": {
                    "child_development": {"rm_grant": 1},
                    "basic_1_5": {"approved_quota": 3},
                    "basic_6_8": {
                        "approved_quota": 1,
                        "federal_grant": 1,
                        "rm_grant": 1,
                    },
                    "basic_9_10": {"relief": 1},
                },
                "grand_total": 8,
            },
            {
                "s_n": "२",
                "school_name_full": "मा.वि., गढवा-१",
                "ward_number": 1,
                "institution_level": "SECONDARY",
                "staffing_by_level": {
                    "child_development": {"rm_grant": 1},
                    "basic_1_5": {"approved_quota": 3, "private_source": 2},
                    "basic_6_8": {"federal_grant": 1, "rm_grant": 3},
                    "basic_9_10": {"relief": 1},
                },
                "grand_total": 12,
            },
            {
                "s_n": "३",
                "school_name_full": "युवावर्ष मा.वि., गढवा-१",
                "ward_number": 1,
                "institution_level": "SECONDARY",
                "staffing_by_level": {
                    "child_development": {"rm_grant": 1},
                    "basic_1_5": {"approved_quota": 3},
                    "basic_6_8": {
                        "approved_quota": 1,
                        "federal_grant": 1,
                        "rm_grant": 1,
                    },
                    "basic_9_10": {"approved_quota": 2},
                },
                "grand_total": 10,
            },
            {
                "s_n": "४",
                "school_name_full": "बालकल्याण प्रा.वि., गढवा-१",
                "ward_number": 1,
                "institution_level": "PRIMARY",
                "staffing_by_level": {
                    "child_development": {"rm_grant": 1},
                    "basic_1_5": {"federal_grant": 1, "rm_grant": 1},
                },
                "grand_total": 3,
            },
            {
                "s_n": "५",
                "school_name_full": "देउराली शिवालय आ.वि., गढवा-१",
                "ward_number": 1,
                "institution_level": "LOWER_SECONDARY",
                "staffing_by_level": {
                    "child_development": {"rm_grant": 1},
                },
                "grand_total": 1,
            },
            {
                "s_n": "६",
                "school_name_full": "दुङ्खानी दोभान आ.वि., गढवा-१",
                "ward_number": 1,
                "institution_level": "LOWER_SECONDARY",
                "staffing_by_level": {
                    "child_development": {"rm_grant": 1},
                },
                "grand_total": 1,
            },
            {
                "s_n": "७",
                "school_name_full": "हिमाल प्रा.वि., गढवा-१",
                "ward_number": 1,
                "institution_level": "PRIMARY",
                "staffing_by_level": {
                    "child_development": {"rm_grant": 1},
                    "basic_1_5": {"federal_grant": 1},
                },
                "grand_total": 2,
            },
            {
                "s_n": "८",
                "school_name_full": "जन कल्याण प्रा.वि., गढवा-१",
                "ward_number": 1,
                "institution_level": "PRIMARY",
                "staffing_by_level": {
                    "child_development": {"rm_grant": 1},
                    "basic_1_5": {"federal_grant": 1, "private_source": 2},
                },
                "grand_total": 4,
            },
            {
                "s_n": "९",
                "school_name_full": "जनजागृति आ.वि., गढवा-१",
                "ward_number": 1,
                "institution_level": "LOWER_SECONDARY",
                "staffing_by_level": {
                    "child_development": {"rm_grant": 1},
                },
                "grand_total": 1,
            },
            {
                "s_n": "१०",
                "school_name_full": "सरस्वति मा.वि., गढवा-१",
                "ward_number": 1,
                "institution_level": "SECONDARY",
                "staffing_by_level": {
                    "child_development": {"rm_grant": 1},
                    "basic_1_5": {"approved_quota": 3},
                    "basic_6_8": {"approved_quota": 1, "relief": 2, "rm_grant": 3},
                    "basic_9_10": {"approved_quota": 2, "relief": 1},
                },
                "grand_total": 13,
            },
            # Ward 2 data
            {
                "s_n": "१३",
                "school_name_full": "झिमरुकलेस्वर मा.वि., गढवा-२",
                "ward_number": 2,
                "institution_level": "SECONDARY",
                "staffing_by_level": {
                    "child_development": {"rm_grant": 1},
                    "basic_1_5": {"approved_quota": 4, "relief": 2},
                    "basic_6_8": {
                        "approved_quota": 1,
                        "federal_grant": 1,
                        "rm_grant": 1,
                    },
                    "basic_9_10": {"relief": 1},
                },
                "grand_total": 12,
            },
            {
                "s_n": "१५",
                "school_name_full": "गोकुल मा.वि., गढवा-२",
                "ward_number": 2,
                "institution_level": "SECONDARY",
                "staffing_by_level": {
                    "child_development": {"rm_grant": 1},
                    "basic_1_5": {
                        "approved_quota": 4,
                        "relief": 1,
                        "private_source": 2,
                    },
                    "basic_6_8": {"approved_quota": 2, "relief": 2},
                    "basic_9_10": {
                        "approved_quota": 1,
                        "relief": 4,
                        "federal_grant": 1,
                    },
                },
                "grand_total": 20,
            },
            # Ward 3 data
            {
                "s_n": "२२",
                "school_name_full": "सामाजिक मा.वि., गढवा-३",
                "ward_number": 3,
                "institution_level": "SECONDARY",
                "staffing_by_level": {
                    "child_development": {"rm_grant": 1},
                    "basic_1_5": {
                        "approved_quota": 4,
                        "relief": 3,
                        "private_source": 2,
                    },
                    "basic_6_8": {"federal_grant": 1},
                    "basic_9_10": {"relief": 2, "federal_grant": 1},
                },
                "grand_total": 14,
            },
            # Ward 4 data
            {
                "s_n": "२४",
                "school_name_full": "विजयश्वरी मा.वि., गढवा-४",
                "ward_number": 4,
                "institution_level": "SECONDARY",
                "staffing_by_level": {
                    "child_development": {"rm_grant": 1},
                    "basic_1_5": {"approved_quota": 3},
                    "basic_6_8": {"federal_grant": 1, "rm_grant": 3},
                    "basic_9_10": {"relief": 1},
                },
                "grand_total": 12,
            },
            {
                "s_n": "२५",
                "school_name_full": "गौरी शंकर मा.वि., गढवा-४",
                "ward_number": 4,
                "institution_level": "SECONDARY",
                "staffing_by_level": {
                    "child_development": {"rm_grant": 1},
                    "basic_1_5": {"approved_quota": 4, "relief": 2},
                    "basic_6_8": {"approved_quota": 2, "relief": 2},
                    "basic_9_10": {"relief": 2},
                },
                "grand_total": 14,
            },
            # Ward 5 data
            {
                "s_n": "२९",
                "school_name_full": "बराहक्षेत्र मा.वि., गढवा-५",
                "ward_number": 5,
                "institution_level": "SECONDARY",
                "staffing_by_level": {
                    "child_development": {"rm_grant": 1},
                    "basic_1_5": {
                        "approved_quota": 3,
                        "rm_grant": 2,
                        "private_source": 4,
                    },
                    "basic_6_8": {
                        "federal_grant": 1,
                        "rm_grant": 4,
                        "private_source": 1,
                    },
                    "basic_9_10": {"relief": 1, "rm_grant": 2},
                },
                "grand_total": 22,
            },
            # Ward 6 data
            {
                "s_n": "३३",
                "school_name_full": "जनज्योति मा.वि., गढवा-६",
                "ward_number": 6,
                "institution_level": "SECONDARY",
                "staffing_by_level": {
                    "child_development": {"rm_grant": 2},
                    "basic_1_5": {
                        "approved_quota": 5,
                        "federal_grant": 1,
                        "rm_grant": 1,
                        "private_source": 3,
                    },
                    "basic_6_8": {
                        "federal_grant": 1,
                        "rm_grant": 2,
                        "private_source": 1,
                    },
                },
                "grand_total": 17,
            },
            {
                "s_n": "３७",
                "school_name_full": "नेपाल राष्ट्रिय मा.वि., गढवा-६",
                "ward_number": 6,
                "institution_level": "SECONDARY",
                "staffing_by_level": {
                    "child_development": {"rm_grant": 1},
                    "basic_1_5": {"approved_quota": 3},
                    "basic_6_8": {
                        "approved_quota": 2,
                        "federal_grant": 1,
                        "rm_grant": 1,
                        "private_source": 3,
                    },
                },
                "grand_total": 11,
            },
            # Ward 7 data
            {
                "s_n": "३८",
                "school_name_full": "नेपाल राष्ट्रिय मा.वि., गढवा-७",
                "ward_number": 7,
                "institution_level": "SECONDARY",
                "staffing_by_level": {
                    "child_development": {"rm_grant": 1},
                    "basic_1_5": {"approved_quota": 4, "relief": 3},
                    "basic_6_8": {"approved_quota": 2, "relief": 3},
                    "basic_9_10": {"relief": 2, "federal_grant": 1},
                },
                "grand_total": 17,
            },
        ]

        # Position type mapping
        position_mapping = {
            "approved_quota": TeacherPositionTypeChoice.APPROVED_QUOTA,
            "relief": TeacherPositionTypeChoice.RELIEF,
            "federal_grant": TeacherPositionTypeChoice.FEDERAL_GRANT,
            "rm_grant": TeacherPositionTypeChoice.RM_GRANT,
            "private_source": TeacherPositionTypeChoice.PRIVATE_SOURCE,
        }

        # Level mapping
        level_mapping = {
            "child_development": TeacherLevelChoice.CHILD_DEVELOPMENT,
            "basic_1_5": TeacherLevelChoice.BASIC_1_5,
            "basic_6_8": TeacherLevelChoice.BASIC_6_8,
            "basic_9_10": TeacherLevelChoice.BASIC_9_10,
            "basic_11_12": TeacherLevelChoice.BASIC_11_12,
        }

        created_count = 0

        with transaction.atomic():
            for school_data in teacher_data:
                school_name = school_data["school_name_full"]
                ward_number = school_data["ward_number"]
                institution_level = school_data["institution_level"]

                for level_key, level_data in school_data["staffing_by_level"].items():
                    teacher_level = level_mapping[level_key]

                    for position_key, count in level_data.items():
                        if count and count > 0:
                            position_type = position_mapping[position_key]

                            staffing, created = (
                                WardWiseTeacherStaffing.objects.update_or_create(
                                    ward_number=ward_number,
                                    school_name=school_name,
                                    teacher_level=teacher_level,
                                    position_type=position_type,
                                    defaults={
                                        "institution_level": institution_level,
                                        "teacher_count": count,
                                    },
                                )
                            )

                            if created:
                                created_count += 1

        # Generate summary data
        self.generate_summary()

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {created_count} teacher staffing records"
            )
        )

    def generate_summary(self):
        """Generate summary statistics"""
        # Clear existing summary
        WardWiseTeacherSummary.objects.all().delete()

        # Aggregate by level and position type
        from django.db.models import Sum

        for level_choice in TeacherLevelChoice.choices:
            level_code = level_choice[0]
            for position_choice in TeacherPositionTypeChoice.choices:
                position_code = position_choice[0]

                total_teachers = (
                    WardWiseTeacherStaffing.objects.filter(
                        teacher_level=level_code, position_type=position_code
                    ).aggregate(total=Sum("teacher_count"))["total"]
                    or 0
                )

                if total_teachers > 0:
                    WardWiseTeacherSummary.objects.create(
                        teacher_level=level_code,
                        position_type=position_code,
                        total_teachers=total_teachers,
                    )

        self.stdout.write("Generated teacher summary statistics")

    def nepali_number(self, num):
        """Convert English numbers to Nepali"""
        mapping = str.maketrans("0123456789", "०१२३४५६७८९")
        return str(num).translate(mapping)
