"""
Management command to create school dropout social data based on actual data
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db import models
from apps.social.models import WardWiseSchoolDropout, SchoolDropoutCauseTypeChoice
import uuid


class Command(BaseCommand):
    help = "Create school dropout social data based on actual municipality-wide data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before creating new data",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write(
                self.style.WARNING("Clearing existing school dropout data...")
            )
            WardWiseSchoolDropout.objects.all().delete()

        self.stdout.write(
            "Creating school dropout social data based on actual municipality-wide data..."
        )

        # Sample data representing actual school dropout patterns by ward and cause
        school_dropout_data = [
            # Ward 1
            {
                "id": str(uuid.uuid4()),
                "ward_number": 1,
                "cause": "EMPLOYMENT",
                "population": 31,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 1,
                "cause": "EXPENSIVE",
                "population": 36,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 1,
                "cause": "FAR",
                "population": 11,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 1,
                "cause": "HOUSE_HELP",
                "population": 203,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 1,
                "cause": "LIMITED_SPACE",
                "population": 1,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 1,
                "cause": "MARRIAGE",
                "population": 311,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 1,
                "cause": "OTHER",
                "population": 128,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 1,
                "cause": "UNKNOWN",
                "population": 2626,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 1,
                "cause": "UNWILLING_PARENTS",
                "population": 12,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 1,
                "cause": "WANTED_STUDY_COMPLETED",
                "population": 100,
            },
            # Ward 2
            {
                "id": str(uuid.uuid4()),
                "ward_number": 2,
                "cause": "EMPLOYMENT",
                "population": 114,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 2,
                "cause": "EXPENSIVE",
                "population": 9,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 2,
                "cause": "FAR",
                "population": 2,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 2,
                "cause": "HOUSE_HELP",
                "population": 307,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 2,
                "cause": "MARRIAGE",
                "population": 243,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 2,
                "cause": "OTHER",
                "population": 20,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 2,
                "cause": "UNKNOWN",
                "population": 219,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 2,
                "cause": "UNWILLING_PARENTS",
                "population": 6,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 2,
                "cause": "WANTED_STUDY_COMPLETED",
                "population": 59,
            },
            # Ward 3
            {
                "id": str(uuid.uuid4()),
                "ward_number": 3,
                "cause": "EMPLOYMENT",
                "population": 59,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 3,
                "cause": "EXPENSIVE",
                "population": 19,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 3,
                "cause": "FAR",
                "population": 8,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 3,
                "cause": "HOUSE_HELP",
                "population": 71,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 3,
                "cause": "LIMITED_SPACE",
                "population": 43,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 3,
                "cause": "MARRIAGE",
                "population": 126,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 3,
                "cause": "OTHER",
                "population": 40,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 3,
                "cause": "UNKNOWN",
                "population": 223,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 3,
                "cause": "UNWILLING_PARENTS",
                "population": 2,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 3,
                "cause": "WANTED_STUDY_COMPLETED",
                "population": 102,
            },
            # Ward 4
            {
                "id": str(uuid.uuid4()),
                "ward_number": 4,
                "cause": "EMPLOYMENT",
                "population": 13,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 4,
                "cause": "EXPENSIVE",
                "population": 6,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 4,
                "cause": "FAR",
                "population": 3,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 4,
                "cause": "HOUSE_HELP",
                "population": 203,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 4,
                "cause": "MARRIAGE",
                "population": 131,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 4,
                "cause": "OTHER",
                "population": 53,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 4,
                "cause": "UNKNOWN",
                "population": 323,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 4,
                "cause": "UNWILLING_PARENTS",
                "population": 7,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 4,
                "cause": "WANTED_STUDY_COMPLETED",
                "population": 80,
            },
            # Ward 5
            {
                "id": str(uuid.uuid4()),
                "ward_number": 5,
                "cause": "EMPLOYMENT",
                "population": 40,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 5,
                "cause": "EXPENSIVE",
                "population": 6,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 5,
                "cause": "FAR",
                "population": 7,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 5,
                "cause": "HOUSE_HELP",
                "population": 42,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 5,
                "cause": "MARRIAGE",
                "population": 92,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 5,
                "cause": "OTHER",
                "population": 288,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 5,
                "cause": "UNKNOWN",
                "population": 1308,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 5,
                "cause": "WANTED_STUDY_COMPLETED",
                "population": 45,
            },
            # Ward 6
            {
                "id": str(uuid.uuid4()),
                "ward_number": 6,
                "cause": "EMPLOYMENT",
                "population": 15,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 6,
                "cause": "EXPENSIVE",
                "population": 11,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 6,
                "cause": "FAR",
                "population": 7,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 6,
                "cause": "HOUSE_HELP",
                "population": 315,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 6,
                "cause": "LIMITED_SPACE",
                "population": 12,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 6,
                "cause": "MARRIAGE",
                "population": 201,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 6,
                "cause": "OTHER",
                "population": 37,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 6,
                "cause": "UNKNOWN",
                "population": 770,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 6,
                "cause": "UNWILLING_PARENTS",
                "population": 2,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 6,
                "cause": "WANTED_STUDY_COMPLETED",
                "population": 77,
            },
            # Ward 7
            {
                "id": str(uuid.uuid4()),
                "ward_number": 7,
                "cause": "EMPLOYMENT",
                "population": 34,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 7,
                "cause": "EXPENSIVE",
                "population": 2,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 7,
                "cause": "FAR",
                "population": 8,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 7,
                "cause": "HOUSE_HELP",
                "population": 70,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 7,
                "cause": "MARRIAGE",
                "population": 191,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 7,
                "cause": "OTHER",
                "population": 74,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 7,
                "cause": "UNKNOWN",
                "population": 691,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 7,
                "cause": "UNWILLING_PARENTS",
                "population": 7,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 7,
                "cause": "WANTED_STUDY_COMPLETED",
                "population": 74,
            },
        ]

        # Check if data already exists
        existing_count = WardWiseSchoolDropout.objects.count()
        if existing_count > 0 and not options["clear"]:
            self.stdout.write(
                self.style.WARNING(
                    f"Found {existing_count} existing records. Use --clear to replace them."
                )
            )
            return

        # Create records using Django ORM
        created_count = 0
        with transaction.atomic():
            for data in school_dropout_data:
                obj, created = WardWiseSchoolDropout.objects.get_or_create(
                    ward_number=data["ward_number"],
                    cause=data["cause"],
                    defaults={
                        "id": data["id"],
                        "population": data["population"],
                    },
                )

                if created:
                    created_count += 1
                    self.stdout.write(
                        f"Created: Ward {data['ward_number']} - {data['cause']} ({data['population']} children)"
                    )
                else:
                    # Update existing record
                    obj.population = data["population"]
                    obj.save()
                    self.stdout.write(
                        f"Updated: Ward {data['ward_number']} - {data['cause']} ({data['population']} children)"
                    )

        # Print summary
        total_records = WardWiseSchoolDropout.objects.count()
        total_children = sum(
            WardWiseSchoolDropout.objects.values_list("population", flat=True)
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nSuccessfully processed {len(school_dropout_data)} school dropout social records "
                f"({created_count} new, {len(school_dropout_data) - created_count} updated)\n"
                f"Total records in database: {total_records}\n"
                f"Total children affected: {total_children:,} children"
            )
        )

        # Print dropout cause breakdown
        self.stdout.write("\nSchool dropout cause breakdown:")
        for dropout_choice in SchoolDropoutCauseTypeChoice.choices:
            dropout_code = dropout_choice[0]
            dropout_name = dropout_choice[1]
            dropout_children = (
                WardWiseSchoolDropout.objects.filter(cause=dropout_code).aggregate(
                    total=models.Sum("population")
                )["total"]
                or 0
            )

            if dropout_children > 0:
                percentage = dropout_children / total_children * 100
                self.stdout.write(
                    f"  {dropout_name}: {dropout_children:,} children ({percentage:.2f}%)"
                )
            else:
                self.stdout.write(f"  {dropout_name}: 0 children (0.00%)")

        # Educational impact analysis
        self.stdout.write("\nEducational Impact Analysis:")

        # Economic factors
        economic_causes = ["EXPENSIVE", "EMPLOYMENT", "HOUSE_HELP"]
        economic_children = sum(
            WardWiseSchoolDropout.objects.filter(cause=cause).aggregate(
                total=models.Sum("population")
            )["total"]
            or 0
            for cause in economic_causes
        )
        economic_percentage = (
            (economic_children / total_children * 100) if total_children > 0 else 0
        )

        self.stdout.write(
            f"  Economic factors: {economic_children:,} children ({economic_percentage:.1f}%)"
        )

        # Social factors
        social_causes = ["MARRIAGE", "UNWILLING_PARENTS"]
        social_children = sum(
            WardWiseSchoolDropout.objects.filter(cause=cause).aggregate(
                total=models.Sum("population")
            )["total"]
            or 0
            for cause in social_causes
        )
        social_percentage = (
            (social_children / total_children * 100) if total_children > 0 else 0
        )

        self.stdout.write(
            f"  Social factors: {social_children:,} children ({social_percentage:.1f}%)"
        )

        # Infrastructure factors
        infrastructure_causes = ["FAR", "LIMITED_SPACE"]
        infrastructure_children = sum(
            WardWiseSchoolDropout.objects.filter(cause=cause).aggregate(
                total=models.Sum("population")
            )["total"]
            or 0
            for cause in infrastructure_causes
        )
        infrastructure_percentage = (
            (infrastructure_children / total_children * 100)
            if total_children > 0
            else 0
        )

        self.stdout.write(
            f"  Infrastructure barriers: {infrastructure_children:,} children ({infrastructure_percentage:.1f}%)"
        )

        # Positive completion
        completed_children = (
            WardWiseSchoolDropout.objects.filter(
                cause="WANTED_STUDY_COMPLETED"
            ).aggregate(total=models.Sum("population"))["total"]
            or 0
        )
        completed_percentage = (
            (completed_children / total_children * 100) if total_children > 0 else 0
        )

        self.stdout.write(
            f"  Study completion (positive): {completed_children:,} children ({completed_percentage:.1f}%)"
        )

        # Unknown reasons
        unknown_children = (
            WardWiseSchoolDropout.objects.filter(cause="UNKNOWN").aggregate(
                total=models.Sum("population")
            )["total"]
            or 0
        )
        unknown_percentage = (
            (unknown_children / total_children * 100) if total_children > 0 else 0
        )

        self.stdout.write(
            f"  Unknown reasons: {unknown_children:,} children ({unknown_percentage:.1f}%)"
        )

        # Ward-wise summary
        self.stdout.write("\nWard-wise school dropout summary:")
        for ward_num in range(1, 8):
            ward_children = (
                WardWiseSchoolDropout.objects.filter(ward_number=ward_num).aggregate(
                    total=models.Sum("population")
                )["total"]
                or 0
            )
            if ward_children > 0:
                self.stdout.write(f"  वडा {ward_num}: {ward_children:,} children")

        # Critical insights
        self.stdout.write("\nCritical Educational Insights:")
        if unknown_percentage > 50:
            self.stdout.write(
                "  ⚠️  CRITICAL: Over 50% of dropouts have unknown reasons - data collection needs improvement"
            )

        if economic_percentage > 30:
            self.stdout.write(
                "  💰 Economic burden is a major factor - scholarship programs needed"
            )

        marriage_children = (
            WardWiseSchoolDropout.objects.filter(cause="MARRIAGE").aggregate(
                total=models.Sum("population")
            )["total"]
            or 0
        )
        marriage_percentage = (
            (marriage_children / total_children * 100) if total_children > 0 else 0
        )

        if marriage_percentage > 15:
            self.stdout.write(
                "  👰 High marriage-related dropouts - child marriage prevention programs needed"
            )

        if infrastructure_percentage > 10:
            self.stdout.write(
                "  🏫 Infrastructure barriers significant - school accessibility needs improvement"
            )

        self.stdout.write(
            f"\n📊 Overall dropout rate analysis shows {total_children:,} children are out of school"
        )
        self.stdout.write(
            "🎯 Focus areas: Economic support, infrastructure development, and awareness programs"
        )
