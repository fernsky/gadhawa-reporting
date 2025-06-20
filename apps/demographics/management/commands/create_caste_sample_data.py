"""
Management command to create caste demographics data based on actual data
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from apps.demographics.models import MunicipalityWideCastePopulation, CasteTypeChoice
import uuid


class Command(BaseCommand):
    help = "Create caste demographics data based on actual municipality-wide data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before creating new data",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write(self.style.WARNING("Clearing existing caste data..."))
            MunicipalityWideCastePopulation.objects.all().delete()

        self.stdout.write(
            "Creating caste demographics data based on actual municipality-wide data..."
        )

        # Raw ward-wise caste data from actual census
        raw_ward_data = [
            (1, "कामी", 441),
            (1, "क्षेत्री", 1234),
            (1, "गुरुङ", 5),
            (1, "दमाई/ढोली", 115),
            (1, "मगर", 3764),
            (1, "सार्की", 3),
            (1, "सुनुवार", 41),
            (2, "कामी", 557),
            (2, "क्षेत्री", 2118),
            (2, "दमाई/ढोली", 131),
            (2, "ब्राह्मण पहाड", 30),
            (2, "मगर", 1287),
            (2, "सार्की", 142),
            (3, "कामी", 84),
            (3, "क्षेत्री", 1417),
            (3, "गुरुङ", 51),
            (3, "दमाई/ढोली", 23),
            (3, "नेवार", 5),
            (3, "ब्राह्मण पहाड", 51),
            (3, "मगर", 1392),
            (3, "सार्की", 15),
            (4, "कामी", 894),
            (4, "क्षेत्री", 3007),
            (4, "गुरुङ", 3),
            (4, "दमाई/ढोली", 49),
            (4, "ब्राह्मण पहाड", 4),
            (4, "मगर", 102),
            (5, "कामी", 422),
            (5, "क्षेत्री", 1545),
            (5, "गुरुङ", 75),
            (5, "दमाई/ढोली", 41),
            (5, "ब्राह्मण पहाड", 85),
            (5, "मगर", 1117),
            (5, "माझी", 3),
            (5, "सुनुवार", 118),
            (6, "कामी", 596),
            (6, "क्षेत्री", 3056),
            (6, "गुरुङ", 21),
            (6, "दमाई/ढोली", 119),
            (6, "मगर", 719),
            (7, "कामी", 685),
            (7, "क्षेत्री", 263),
            (7, "गुरुङ", 41),
            (7, "थकाली", 6),
            (7, "दमाई/ढोली", 122),
            (7, "मगर", 1438),
            (7, "माझी", 58),
        ]

        # Mapping Nepali caste names to model enum choices
        caste_mapping = {
            "कामी": "DALIT",  # Kami is traditionally considered Dalit
            "क्षेत्री": "CHHETRI",
            "गुरुङ": "GURUNG",
            "दमाई/ढोली": "DALIT",  # Damai/Dholi is traditionally considered Dalit
            "मगर": "MAGAR",
            "सार्की": "DALIT",  # Sarki is traditionally considered Dalit
            "सुनुवार": "OTHER",  # Sunuwar not in enum, categorized as OTHER
            "ब्राह्मण पहाड": "BRAHMIN",
            "नेवार": "NEWAR",
            "माझी": "OTHER",  # Majhi not in enum, categorized as OTHER
            "थकाली": "OTHER",  # Thakali not in enum, categorized as OTHER
        }

        # Aggregate data by caste type for municipality-wide totals
        caste_totals = {}
        for ward, nepali_caste, population in raw_ward_data:
            enum_caste = caste_mapping.get(nepali_caste, "OTHER")
            if enum_caste not in caste_totals:
                caste_totals[enum_caste] = 0
            caste_totals[enum_caste] += population

        # Convert to the format expected by the rest of the code
        caste_data = []
        for caste_enum, total_population in caste_totals.items():
            caste_data.append(
                {
                    "id": str(uuid.uuid4()),
                    "caste": caste_enum,
                    "population": total_population,
                }
            )

        self.stdout.write(
            f"Processing {len(raw_ward_data)} ward-level records into {len(caste_data)} municipality-wide caste categories..."
        )

        existing_count = MunicipalityWideCastePopulation.objects.count()
        if existing_count > 0 and not options["clear"]:
            self.stdout.write(
                self.style.WARNING(
                    f"Found {existing_count} existing records. Use --clear to replace them."
                )
            )
            return

        created_count = 0
        with transaction.atomic():
            for data in caste_data:
                obj, created = MunicipalityWideCastePopulation.objects.get_or_create(
                    caste=data["caste"],
                    defaults={
                        "id": data["id"],
                        "population": data["population"],
                    },
                )

                if created:
                    created_count += 1
                    self.stdout.write(
                        f"Created: {data['caste']} ({data['population']} people)"
                    )
                else:
                    obj.population = data["population"]
                    obj.save()
                    self.stdout.write(
                        f"Updated: {data['caste']} ({data['population']} people)"
                    )

        total_records = MunicipalityWideCastePopulation.objects.count()
        total_population = sum(
            MunicipalityWideCastePopulation.objects.values_list("population", flat=True)
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nSuccessfully processed {len(caste_data)} caste demographic records "
                f"({created_count} new, {len(caste_data) - created_count} updated)\n"
                f"Total records in database: {total_records}\n"
                f"Total population covered: {total_population:,} people"
            )
        )

        self.stdout.write("\nCaste breakdown:")
        for caste_choice in CasteTypeChoice.choices:
            caste_code = caste_choice[0]
            caste_name = caste_choice[1]
            try:
                caste_obj = MunicipalityWideCastePopulation.objects.get(
                    caste=caste_code
                )
                caste_pop = caste_obj.population
                percentage = caste_pop / total_population * 100
                self.stdout.write(f"  {caste_name}: {caste_pop:,} ({percentage:.2f}%)")
            except MunicipalityWideCastePopulation.DoesNotExist:
                self.stdout.write(f"  {caste_name}: 0 (0.00%)")
