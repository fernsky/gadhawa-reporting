"""
Management command to create sample data for Ward Wise Educational Institutions

This command creates comprehensive sample data for educational institutions
and student enrollment based on the provided JSON data for Section 5.1.2.
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from apps.social.models import (
    WardWiseEducationalInstitution,
    EducationalInstitutionTypeChoice,
    SchoolLevelChoice,
)
from apps.reports.utils.nepali_numbers import to_nepali_digits
import os
import glob
import json


class Command(BaseCommand):
    help = "Create sample data for Ward Wise Educational Institutions (५.१.२)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete existing data before creating new data",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete all educational institution data and exit",
        )

    def handle(self, *args, **options):
        if options.get("clear"):
            self.stdout.write("Clearing all educational institution data...")
            WardWiseEducationalInstitution.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("✓ All data cleared successfully"))
            return
        if options["reset"]:
            self.stdout.write("Clearing existing educational institution data...")
            WardWiseEducationalInstitution.objects.all().delete()
            self.stdout.write(
                self.style.SUCCESS("✓ Existing data cleared successfully")
            )

        # Load all JSON fixture files for all years
        fixtures_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "fixtures"
        )
        json_files = glob.glob(
            os.path.join(fixtures_dir, "educational_institution_*.json")
        )
        all_data = []
        for file_path in json_files:
            with open(file_path, "r", encoding="utf-8") as f:
                all_data.extend(json.load(f))

        # Prepare bulk create/update
        to_create = []
        to_update = []
        existing = {
            (obj.ward_number, obj.data_year, obj.institution_name): obj
            for obj in WardWiseEducationalInstitution.objects.all()
        }
        for entry in all_data:
            ward_number = entry.get("ward_number")
            data_year = entry.get("data_year")
            institution_name = entry.get("institution_name")
            grades = entry.get("student_counts", {})
            school_level = entry.get("school_level")
            school_type = entry.get("school_type") or "COMMUNITY_SCHOOL"
            # Aggregate total male/female for the school using 'total' from each grade
            male_students = sum(
                g.get("boys", 0)
                for k, g in grades.items()
                if isinstance(g, dict) and "boys" in g
            )
            female_students = sum(
                g.get("girls", 0)
                for k, g in grades.items()
                if isinstance(g, dict) and "girls" in g
            )
            is_operational = (male_students + female_students) > 0
            key = (ward_number, data_year, institution_name)
            defaults = {
                "male_students": male_students,
                "female_students": female_students,
                "school_level": school_level,
                "institution_type": getattr(
                    EducationalInstitutionTypeChoice,
                    str(school_type),
                    EducationalInstitutionTypeChoice.COMMUNITY_SCHOOL,
                ),
                "is_operational": is_operational,
            }
            if key in existing:
                obj = existing[key]
                for k, v in defaults.items():
                    setattr(obj, k, v)
                to_update.append(obj)
            else:
                to_create.append(
                    WardWiseEducationalInstitution(
                        ward_number=ward_number,
                        data_year=data_year,
                        institution_name=institution_name,
                        **defaults,
                    )
                )
        # Bulk operations
        if to_create:
            WardWiseEducationalInstitution.objects.bulk_create(to_create)
        if to_update:
            WardWiseEducationalInstitution.objects.bulk_update(
                to_update,
                [
                    "male_students",
                    "female_students",
                    "school_level",
                    "institution_type",
                    "is_operational",
                ],
            )
        self.stdout.write(
            self.style.SUCCESS(
                f"Created: {len(to_create)}, Updated: {len(to_update)} records."
            )
        )
        self.generate_summary()

    def generate_summary(self):
        """Generate and display summary statistics"""
        from django.db.models import Sum, Count, Avg

        self.stdout.write("\n" + "📈 SUMMARY STATISTICS")
        self.stdout.write("-" * 50)

        # Overall statistics
        total_institutions = WardWiseEducationalInstitution.objects.count()
        total_male_students = (
            WardWiseEducationalInstitution.objects.aggregate(Sum("male_students"))[
                "male_students__sum"
            ]
            or 0
        )
        total_female_students = (
            WardWiseEducationalInstitution.objects.aggregate(Sum("female_students"))[
                "female_students__sum"
            ]
            or 0
        )
        total_students = total_male_students + total_female_students

        self.stdout.write(
            f"🏫 कुल शैक्षिक संस्थाहरू: {to_nepali_digits(str(total_institutions))}"
        )
        self.stdout.write(
            f"👨‍🎓 कुल पुरुष विद्यार्थी: {to_nepali_digits(str(total_male_students))}"
        )
        self.stdout.write(
            f"👩‍🎓 कुल महिला विद्यार्थी: {to_nepali_digits(str(total_female_students))}"
        )
        self.stdout.write(
            f"📚 कुल विद्यार्थी संख्या: {to_nepali_digits(str(total_students))}"
        )

        if total_students > 0:
            gender_ratio = round((total_female_students / total_students) * 100, 1)
            self.stdout.write(
                f"⚖️ लैङ्गिक अनुपात (महिला %): {to_nepali_digits(str(gender_ratio))}%"
            )

        # Ward-wise summary
        self.stdout.write("\n🗺️ वडागत सारांश:")
        for ward_num in range(1, 8):
            ward_institutions = WardWiseEducationalInstitution.objects.filter(
                ward_number=ward_num
            )
            if ward_institutions.exists():
                ward_total_students = ward_institutions.aggregate(
                    male_sum=Sum("male_students"), female_sum=Sum("female_students")
                )
                ward_male = ward_total_students["male_sum"] or 0
                ward_female = ward_total_students["female_sum"] or 0
                ward_total = ward_male + ward_female
                ward_institution_count = (
                    ward_institutions.values("institution_name").distinct().count()
                )

                self.stdout.write(
                    f"   वडा {to_nepali_digits(str(ward_num))}: "
                    f"{to_nepali_digits(str(ward_institution_count))} संस्था, "
                    f"{to_nepali_digits(str(ward_total))} विद्यार्थी"
                )

        self.stdout.write("\n✅ Data creation completed successfully!")
