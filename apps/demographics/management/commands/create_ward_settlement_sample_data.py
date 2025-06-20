"""
Management command to create ward settlement data
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from apps.demographics.models import WardSettlement
import uuid


class Command(BaseCommand):
    help = (
        "Create ward settlement data based on actual municipality ward settlement data"
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before creating new data",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write(
                self.style.WARNING("Clearing existing ward settlement data...")
            )
            WardSettlement.objects.all().delete()

        self.stdout.write(
            "Creating ward settlement data based on actual municipality data..."
        )

        # Ward settlement data as provided
        ward_settlement_data = [
            {
                "ward_number": 1,
                "settlement_areas": [
                    "पाङ",
                    "ऐपे",
                    "छिउदर",
                    "माद्दर",
                    "राजिबाङ",
                    "दाईबाङ",
                    "छिउदर",
                    "खद्दर",
                    "कानाकुतुङ",
                ],
            },
            {
                "ward_number": 2,
                "settlement_areas": [
                    "खालावस्ती",
                    "डाँडा टोल",
                    "आर्यटोल",
                    "मूखिया टोल",
                    "जोगीथरयतका बस्ती",
                    "सार्कि टोल",
                    "सिम भञ्न्याङ",
                    "चिप्लेपाटा",
                    "तासिबाङ",
                    "थातधुङ्गा",
                    "सल्लेधुम",
                ],
            },
            {
                "ward_number": 3,
                "settlement_areas": [
                    "जुतुङखोला",
                    "सिम तोल सिमेगिथा",
                    "सिमलेनी",
                    "अरिन्दे",
                    "गौडा",
                    "चिउरपाखा",
                    "जिमाल तोल",
                    "तालपोखरी",
                    "देउरालि",
                    "धनिपाखा",
                    "धनेखर्क",
                    "सिमेगिथा",
                ],
            },
            {
                "ward_number": 4,
                "settlement_areas": [
                    "नम्जा",
                    "अलधारा",
                    "उतिसे",
                    "गौदा",
                    "चाखुरे धारा",
                    "जुरदुङगा",
                    "जौने पानी",
                    "झाक्रीसल्ला",
                    "थलबाङ",
                    "दमादुङगा",
                    "थाम",
                    "सिमखोला",
                    "रास्थर",
                    "रमिनि",
                    "बिस्ना खर्क",
                    "पुर्ना गाउँ",
                ],
            },
            {
                "ward_number": 5,
                "settlement_areas": [
                    "पिपलचौर",
                    "अमिलेखर्क",
                    "इजारा",
                    "किलाचौर",
                    "गाउँ टोल",
                    "गोठिबाङ",
                    "घोपी",
                    "गोथेखर्क",
                    "चोबाङ",
                    "घोपी",
                    "जुगेपानी",
                    "तामोखोला",
                    "दंगपने",
                    "बलाले",
                    "मछती",
                    "सालघारी",
                ],
            },
            {
                "ward_number": 6,
                "settlement_areas": [
                    "नाम्गी बस्ती",
                    "पाते गुम्चालको लरवाङ",
                    "कमरेपानी",
                    "तल्लो गुम्चाल",
                    "उपल्लो थोक",
                    "घोप्तेचोर",
                    "तलोथोक",
                    "दिमस",
                    "दुल्धरा",
                    "पाते गुम्चाल",
                    "पोखरा",
                    "राजिपाती",
                    "बेरि",
                    "दिमस",
                    "जल्किनी",
                ],
            },
            {
                "ward_number": 7,
                "settlement_areas": [
                    "पल्लीबन",
                    "भुमेथान",
                    "झरीबाङ",
                    "भुपेन्द्र स्मृति टोल",
                    "खोलापार टोल",
                    "छहरेखुङ्ग",
                    "गहिरा टोल",
                    "भुमेथाला टोल",
                    "जेङ्खुङ",
                    "क्वाचिबाङ टोल",
                ],
            },
        ]

        existing_count = WardSettlement.objects.count()
        if existing_count > 0 and not options["clear"]:
            self.stdout.write(
                self.style.WARNING(
                    f"Found {existing_count} existing records. Use --clear to replace them."
                )
            )
            return

        created_count = 0
        updated_count = 0
        total_settlements = 0

        with transaction.atomic():
            for data in ward_settlement_data:
                obj, created = WardSettlement.objects.get_or_create(
                    ward_number=data["ward_number"],
                    defaults={
                        "settlement_areas": data["settlement_areas"],
                    },
                )

                if created:
                    created_count += 1
                    self.stdout.write(
                        f"✓ Created Ward {data['ward_number']} with {len(data['settlement_areas'])} settlements"
                    )
                else:
                    # Update existing record
                    obj.settlement_areas = data["settlement_areas"]
                    obj.save()
                    updated_count += 1
                    self.stdout.write(
                        f"↻ Updated Ward {data['ward_number']} with {len(data['settlement_areas'])} settlements"
                    )

                total_settlements += len(data["settlement_areas"])

        total_records = WardSettlement.objects.count()

        self.stdout.write(
            self.style.SUCCESS(
                f"\nSuccessfully processed {len(ward_settlement_data)} ward settlement records "
                f"({created_count} new, {updated_count} updated)\n"
                f"Total records in database: {total_records}\n"
                f"Total settlements covered: {total_settlements} settlements across {len(ward_settlement_data)} wards"
            )
        )

        # Show breakdown by ward
        self.stdout.write("\nWard-wise settlement breakdown:")
        for ward_settlement in WardSettlement.objects.all().order_by("ward_number"):
            settlement_count = (
                len(ward_settlement.settlement_areas)
                if ward_settlement.settlement_areas
                else 0
            )
            self.stdout.write(
                f"  वडा {ward_settlement.ward_number}: {settlement_count} बस्तीहरु"
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"\n🏘️  Ward Settlement data creation completed successfully!"
            )
        )
