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

        # Ward settlement data as provided (updated for all 8 wards, Unicode Nepali values)
        ward_settlement_data = [
            {
                "ward_number": 1,
                "settlement_areas": [
                    "मलमला",
                    "बढहरा",
                    "जेठानगाउँ",
                    "चिसापानी",
                    "जुरौनी",
                    "पत्रिङ्गा",
                    "बनबारी",
                    "बनघुसरी",
                    "कालाकाटे",
                    "रङ्गसिङ्ग",
                    "कलोनी",
                    "जुरैनी",
                    "धानखैला",
                    "बैहरहा",
                ],
            },
            {
                "ward_number": 2,
                "settlement_areas": [
                    "पचहिया",
                    "महदेवा",
                    "कोठरी",
                    "बाघमारुवा",
                    "डाडाटोल",
                    "घुस्रा",
                    "चिमचिमे",
                    "बाघमारवा",
                    "चिमचिमे",
                    "पाचहिया",
                ],
            },
            {
                "ward_number": 3,
                "settlement_areas": [
                    "गोबरडिहा",
                    "खैरेनी",
                    "धैरेनी",
                    "रत्नपुर",
                    "सुपैला",
                    "माधपुर",
                    "खैरा",
                    "गोवरडिहा",
                ],
            },
            {
                "ward_number": 4,
                "settlement_areas": [
                    "अजगढवा",
                    "पर्सेनी",
                    "पर्सा",
                    "कतियान गाउँ",
                    "रामनगर",
                    "परस्पुर",
                    "नयाँ बस्ती",
                    "खदकपुर",
                    "उठैया",
                    "मग्रोता",
                    "हदैया",
                    "खडकपुर",
                    "हडैया",
                    "छुटकी पर्सेनी",
                    "बुटेनि",
                    "घुसुरपुरवा",
                    "पर्सेनी",
                    "सुताहिया",
                ],
            },
            {
                "ward_number": 5,
                "settlement_areas": [
                    "बाकी",
                    "चैनपुर",
                    "धर्मपुर",
                    "मघरी",
                    "पर्नाहा",
                    "पर्सिया",
                    "खजरौटा",
                    "सुनपुरुवा",
                    "कक्र्हवा",
                    "बाँकी",
                    "सिमलतारा",
                    "लोखर पुर",
                    "ठुलीचौर",
                    "भवानी बस्ती",
                    "लालपुर",
                    "लोखारपुर",
                    "बाकि",
                    "जमुनिबास",
                    "मघर",
                    "तकिया पुर",
                    "वाँकी",
                ],
            },
            {
                "ward_number": 6,
                "settlement_areas": [
                    "मनिकापुर",
                    "गढवा",
                    "बालापुर",
                    "खबरी",
                    "हासीपुर",
                    "बालाखुटी",
                    "मदपुर",
                    "सिबिर",
                    "आँटीपाकर",
                    "बनकट्टी",
                    "कुमाल टोल",
                    "अतरबेदुवा",
                    "रामपुर",
                    "आटीपाकर",
                    "पिपल दारा",
                    "झिंगा",
                    "पर्नाहा गौडी",
                    "उप्ल्नो मदपुर",
                    "नयाँ बस्ती",
                    "पर्नाहा गौडी",
                    "थानदेउखर",
                    "सालघारी",
                    "थान्देउखर",
                    "घोराहा",
                    "सालघारी",
                ],
            },
            {
                "ward_number": 7,
                "settlement_areas": [
                    "घोराहा",
                    "मानपुर",
                    "चन्दनपुर",
                    "शान्तिपुर",
                    "भोजपुर",
                    "लक्षिणपुर",
                    "झारबैरा",
                    "सेमरी",
                    "बिजयपुर",
                    "मोतीपुर",
                ],
            },
            {
                "ward_number": 8,
                "settlement_areas": [
                    "कोइलाबास",
                    "मुसिनाका",
                    "दादा गाउँ",
                    "कोइलाबास बजार",
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
