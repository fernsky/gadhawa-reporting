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

        # Updated sample data representing actual school dropout patterns by ward and cause (including ward 8)
        school_dropout_data = [
            {
                "id": "eddee593-22b4-4e35-a60a-bee327a3e37a",
                "ward_number": 1,
                "cause": "EMPLOYMENT",
                "population": 28,
            },
            {
                "id": "c6f7c476-636a-441e-b5c5-1cf62a1bdb83",
                "ward_number": 1,
                "cause": "EXPENSIVE",
                "population": 4,
            },
            {
                "id": "b5982561-e33a-45d4-a2a7-52b087175bb2",
                "ward_number": 1,
                "cause": "FAR",
                "population": 18,
            },
            {
                "id": "6d7c4b4d-46f4-4c91-8a1f-9b09e0a57cf3",
                "ward_number": 1,
                "cause": "HOUSE_HELP",
                "population": 352,
            },
            {
                "id": "d7762748-9a6b-42d2-9e94-92e8de8d7332",
                "ward_number": 1,
                "cause": "LIMITED_SPACE",
                "population": 6,
            },
            {
                "id": "4556f29e-bbb2-4c1f-b569-d96311db597a",
                "ward_number": 1,
                "cause": "MARRIAGE",
                "population": 294,
            },
            {
                "id": "91dbec93-943a-4caf-a045-cd4e9d896fcd",
                "ward_number": 1,
                "cause": "OTHER",
                "population": 177,
            },
            {
                "id": "ecba8aec-0aaf-490d-bbf0-cbc35fde6404",
                "ward_number": 1,
                "cause": "UNWILLING_PARENTS",
                "population": 28,
            },
            {
                "id": "c94c5632-96ff-4853-8dce-dc257e5c032e",
                "ward_number": 1,
                "cause": "WANTED_STUDY_COMPLETED",
                "population": 341,
            },
            {
                "id": "a72a2af3-68d8-4547-883a-8ff6bedae9c9",
                "ward_number": 2,
                "cause": "EMPLOYMENT",
                "population": 63,
            },
            {
                "id": "2ed1b8cc-8cfc-449d-8891-fc0ef0a15342",
                "ward_number": 2,
                "cause": "EXPENSIVE",
                "population": 13,
            },
            {
                "id": "66779c82-8ebb-49a1-97b5-c25e7c09862f",
                "ward_number": 2,
                "cause": "FAR",
                "population": 2,
            },
            {
                "id": "a3775a8f-7515-4d6c-ae1c-e1b20b49c10d",
                "ward_number": 2,
                "cause": "HOUSE_HELP",
                "population": 72,
            },
            {
                "id": "87e6c666-1c8e-470e-8969-a74add500bb9",
                "ward_number": 2,
                "cause": "LIMITED_SPACE",
                "population": 1,
            },
            {
                "id": "335e25eb-f95c-439f-9fa1-8c71afd94517",
                "ward_number": 2,
                "cause": "MARRIAGE",
                "population": 272,
            },
            {
                "id": "0ea7920e-0d69-41fa-9a4c-3d4cc00fef0e",
                "ward_number": 2,
                "cause": "OTHER",
                "population": 231,
            },
            {
                "id": "2948320f-b8dd-4277-8a16-ffebf3451c47",
                "ward_number": 2,
                "cause": "UNWILLING_PARENTS",
                "population": 13,
            },
            {
                "id": "14e42a96-0b03-4b52-a0b6-0108c1c387e5",
                "ward_number": 2,
                "cause": "WANTED_STUDY_COMPLETED",
                "population": 90,
            },
            {
                "id": "4597c8d3-f7c2-4cfc-a133-6b2b93899764",
                "ward_number": 3,
                "cause": "EMPLOYMENT",
                "population": 69,
            },
            {
                "id": "6d069a77-2b1b-4a28-8881-e247c69e5858",
                "ward_number": 3,
                "cause": "FAR",
                "population": 2,
            },
            {
                "id": "a10c703d-01c8-4e64-b263-4a90a9e42a6e",
                "ward_number": 3,
                "cause": "HOUSE_HELP",
                "population": 169,
            },
            {
                "id": "465c25a2-74d1-437a-8dee-4b87378edeea",
                "ward_number": 3,
                "cause": "MARRIAGE",
                "population": 290,
            },
            {
                "id": "ebfd885a-a51d-42c4-9e55-3a8021013f15",
                "ward_number": 3,
                "cause": "OTHER",
                "population": 95,
            },
            {
                "id": "187cf684-0c6a-4ad1-a14d-68b7aeb9fdd6",
                "ward_number": 3,
                "cause": "UNWILLING_PARENTS",
                "population": 34,
            },
            {
                "id": "a15505f3-da18-4429-b75e-dcdca26401b2",
                "ward_number": 3,
                "cause": "WANTED_STUDY_COMPLETED",
                "population": 129,
            },
            {
                "id": "1a702358-14f5-4874-95b3-b86c0536a5e2",
                "ward_number": 4,
                "cause": "EMPLOYMENT",
                "population": 56,
            },
            {
                "id": "5bc2eccd-3226-44b2-95a1-603856fc9188",
                "ward_number": 4,
                "cause": "EXPENSIVE",
                "population": 12,
            },
            {
                "id": "340fd38b-9c44-4eaf-810d-50a583267644",
                "ward_number": 4,
                "cause": "FAR",
                "population": 3,
            },
            {
                "id": "b553b89f-20b2-4b1f-a813-189da49571ca",
                "ward_number": 4,
                "cause": "HOUSE_HELP",
                "population": 115,
            },
            {
                "id": "e1f10d40-c8a9-45ed-be0f-d9828eb9bfbc",
                "ward_number": 4,
                "cause": "LIMITED_SPACE",
                "population": 1,
            },
            {
                "id": "41b0eba7-ab25-482d-b1c5-267a7a6beca2",
                "ward_number": 4,
                "cause": "MARRIAGE",
                "population": 316,
            },
            {
                "id": "cd554e9c-73bd-4d39-8e2f-71067fd8f594",
                "ward_number": 4,
                "cause": "OTHER",
                "population": 132,
            },
            {
                "id": "fb9117ca-d8c1-4c46-8a3a-50cb3e6040d5",
                "ward_number": 4,
                "cause": "UNWILLING_PARENTS",
                "population": 6,
            },
            {
                "id": "649626e1-ede5-4b79-85df-fa478e465673",
                "ward_number": 4,
                "cause": "WANTED_STUDY_COMPLETED",
                "population": 135,
            },
            {
                "id": "169def63-0b1d-4514-b247-69a23b97cb09",
                "ward_number": 5,
                "cause": "EMPLOYMENT",
                "population": 135,
            },
            {
                "id": "c08453bd-a99e-4a99-ac61-2e2b17ff82ce",
                "ward_number": 5,
                "cause": "EXPENSIVE",
                "population": 25,
            },
            {
                "id": "a4ab3a13-8ed1-43b3-8a04-a615d2913ad4",
                "ward_number": 5,
                "cause": "FAR",
                "population": 2,
            },
            {
                "id": "f38ac86c-4244-4c93-b6ce-5dfceabffe81",
                "ward_number": 5,
                "cause": "HOUSE_HELP",
                "population": 181,
            },
            {
                "id": "5ed5d1e2-7d2b-494f-be1e-d0ef85047598",
                "ward_number": 5,
                "cause": "MARRIAGE",
                "population": 239,
            },
            {
                "id": "4f8b6e20-78f7-49d9-ae90-f30b8f6c0018",
                "ward_number": 5,
                "cause": "OTHER",
                "population": 42,
            },
            {
                "id": "0177e8ab-61b8-4a6b-8207-ae5383bf2b61",
                "ward_number": 5,
                "cause": "UNWILLING_PARENTS",
                "population": 17,
            },
            {
                "id": "68ad3f74-0328-43ce-b51a-bc3a6f8c7b67",
                "ward_number": 5,
                "cause": "WANTED_STUDY_COMPLETED",
                "population": 273,
            },
            {
                "id": "6c50aaf9-dc55-4bda-9733-a1c536c3f00d",
                "ward_number": 6,
                "cause": "EMPLOYMENT",
                "population": 161,
            },
            {
                "id": "7c690999-745b-4287-8707-5df23512f1b3",
                "ward_number": 6,
                "cause": "EXPENSIVE",
                "population": 102,
            },
            {
                "id": "3ffeb959-e7d2-43b4-893e-22dbbecff62d",
                "ward_number": 6,
                "cause": "FAR",
                "population": 46,
            },
            {
                "id": "c99421a7-c55b-45bc-bfc1-2891d7e540bc",
                "ward_number": 6,
                "cause": "HOUSE_HELP",
                "population": 137,
            },
            {
                "id": "6a8e455d-57ba-4774-8774-2c99408643e5",
                "ward_number": 6,
                "cause": "LIMITED_SPACE",
                "population": 2,
            },
            {
                "id": "69cbabb0-e49b-4d45-b86c-e0c741981383",
                "ward_number": 6,
                "cause": "MARRIAGE",
                "population": 325,
            },
            {
                "id": "286748d2-c049-4e9d-8377-656453fada44",
                "ward_number": 6,
                "cause": "OTHER",
                "population": 144,
            },
            {
                "id": "75fc6e34-b8e7-4b6e-b5a3-52c706a27630",
                "ward_number": 6,
                "cause": "UNWILLING_PARENTS",
                "population": 9,
            },
            {
                "id": "fe787b7a-e908-4b25-9d64-b0f38b427faf",
                "ward_number": 6,
                "cause": "WANTED_STUDY_COMPLETED",
                "population": 81,
            },
            {
                "id": "e0106d9f-1f15-433f-b161-bc71ba7a2411",
                "ward_number": 7,
                "cause": "EMPLOYMENT",
                "population": 277,
            },
            {
                "id": "05cae1b3-b034-4084-ad38-95345012f130",
                "ward_number": 7,
                "cause": "EXPENSIVE",
                "population": 1,
            },
            {
                "id": "14c41013-6a7d-434e-96de-e8a5acd883a8",
                "ward_number": 7,
                "cause": "FAR",
                "population": 1,
            },
            {
                "id": "2c0e2a87-2f6b-44ba-8e10-c968a0ae40c7",
                "ward_number": 7,
                "cause": "HOUSE_HELP",
                "population": 93,
            },
            {
                "id": "8608a43d-0b61-4bf0-b8a5-5537a5241907",
                "ward_number": 7,
                "cause": "MARRIAGE",
                "population": 271,
            },
            {
                "id": "8ed7f49e-3b65-42c9-a1cb-9fe1f3612a2d",
                "ward_number": 7,
                "cause": "OTHER",
                "population": 52,
            },
            {
                "id": "4ac8e0a4-40fb-41c6-ad85-c2b265e5e7ef",
                "ward_number": 7,
                "cause": "WANTED_STUDY_COMPLETED",
                "population": 6,
            },
            {
                "id": "60a16162-6729-46e0-8a76-10a433e07c6e",
                "ward_number": 8,
                "cause": "EMPLOYMENT",
                "population": 18,
            },
            {
                "id": "ce3550e8-0ed4-470c-8dc1-451664d44123",
                "ward_number": 8,
                "cause": "FAR",
                "population": 1,
            },
            {
                "id": "c0ac67ba-e7fc-4c10-933f-acab56c346da",
                "ward_number": 8,
                "cause": "HOUSE_HELP",
                "population": 4,
            },
            {
                "id": "642410b9-8aa2-43ff-8a65-cc1f77a5fa54",
                "ward_number": 8,
                "cause": "MARRIAGE",
                "population": 67,
            },
            {
                "id": "6a6246da-9a21-4933-a2c7-1b1cfca6153d",
                "ward_number": 8,
                "cause": "OTHER",
                "population": 1,
            },
            {
                "id": "95f91702-25da-4d20-a55c-690ccd19b31b",
                "ward_number": 8,
                "cause": "WANTED_STUDY_COMPLETED",
                "population": 26,
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
