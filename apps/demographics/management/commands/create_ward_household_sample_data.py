"""
Management command to create ward household demographics data based on actual data
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from apps.demographics.models import WardTimeSeriesPopulation


class Command(BaseCommand):
    help = "Create ward household demographics data based on actual municipality time series data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before creating new data",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write(
                self.style.WARNING("Clearing existing ward household data...")
            )
            WardTimeSeriesPopulation.objects.all().delete()

        self.stdout.write(
            "Creating ward household demographics data based on actual municipality time series data..."
        )

        # Actual ward household time series data
        # Format: (ward_number, ward_name, year, total_population, male_population, female_population, other_population, total_households, average_household_size, area_sq_km, population_density, sex_ratio)
        ward_household_data = [
            # 2078 Data
            (1, "पाङ(१-९)", 2078, 5451, 2619, 2832, 0, 1108, 4.92, 42.5, 128.26, 92.48),
            (
                2,
                "सिर्प(१,२,४,६,८,९)",
                2078,
                3885,
                1778,
                2107,
                0,
                894,
                4.35,
                15.8,
                245.25,
                84.39,
            ),
            (
                3,
                "सिर्प(३,५,७)",
                2078,
                2950,
                1385,
                1565,
                0,
                548,
                5.38,
                16.13,
                182.87,
                88.50,
            ),
            (
                4,
                "बडाचौर (१-३,७) सिर्प (९)",
                2078,
                3794,
                1653,
                2141,
                0,
                825,
                4.60,
                14.34,
                264.52,
                77.21,
            ),
            (
                5,
                "बडाचौर(४-६,८,९)",
                2078,
                3314,
                1480,
                1834,
                0,
                699,
                4.74,
                12.34,
                268.64,
                80.70,
            ),
            (
                6,
                "गुम्म्चाल(१-९)",
                2078,
                4389,
                2025,
                2364,
                0,
                841,
                5.22,
                14.35,
                305.85,
                85.66,
            ),
            (
                7,
                "हारजङ(१-९)",
                2078,
                2542,
                1205,
                1337,
                0,
                571,
                4.45,
                19.78,
                128.52,
                90.13,
            ),
            # 2081 Data
            (1, "पाङ(१-९)", 2081, 5603, 2692, 2911, 0, 1139, 4.92, 42.5, 131.83, 92.48),
            (
                2,
                "सिर्प(१,२,४,६,८,९)",
                2081,
                4265,
                2038,
                2227,
                0,
                918,
                4.65,
                15.8,
                269.94,
                91.51,
            ),
            (
                3,
                "सिर्प(३,५,७)",
                2081,
                3038,
                1429,
                1609,
                0,
                564,
                5.39,
                16.13,
                188.36,
                88.81,
            ),
            (
                4,
                "बडाचौर (१-३,७) सिर्प (९)",
                2081,
                4059,
                1858,
                2201,
                0,
                848,
                4.79,
                14.34,
                283.08,
                84.42,
            ),
            (
                5,
                "बडाचौर(४-६,८,९)",
                2081,
                3406,
                1521,
                1885,
                0,
                719,
                4.74,
                12.34,
                276.01,
                80.69,
            ),
            (
                6,
                "गुम्म्चाल(१-९)",
                2081,
                4511,
                2081,
                2430,
                0,
                864,
                5.22,
                14.35,
                314.36,
                85.64,
            ),
            (
                7,
                "हारजङ(१-९)",
                2081,
                2613,
                1239,
                1374,
                0,
                587,
                4.45,
                19.78,
                132.11,
                90.17,
            ),
        ]

        self.stdout.write(
            f"Processing {len(ward_household_data)} ward household time series records..."
        )

        existing_count = WardTimeSeriesPopulation.objects.count()
        if existing_count > 0 and not options["clear"]:
            self.stdout.write(
                self.style.WARNING(
                    f"Found {existing_count} existing records. Use --clear to replace them."
                )
            )
            return

        created_count = 0
        updated_count = 0

        with transaction.atomic():
            for (
                ward_num,
                ward_name,
                year,
                total_pop,
                male_pop,
                female_pop,
                other_pop,
                households,
                avg_size,
                area,
                density,
                sex_ratio,
            ) in ward_household_data:
                # Calculate additional metrics
                growth_rate = 0.0
                if year == 2081:
                    # Find 2078 data for same ward to calculate growth rate
                    try:
                        previous_record = WardTimeSeriesPopulation.objects.get(
                            ward_number=ward_num, year=2078
                        )
                        if (
                            previous_record.total_population
                            and previous_record.total_population > 0
                        ):
                            growth_rate = (
                                (total_pop - previous_record.total_population)
                                / previous_record.total_population
                            ) * 100
                    except WardTimeSeriesPopulation.DoesNotExist:
                        pass

                # Create or update record
                record, created = WardTimeSeriesPopulation.objects.update_or_create(
                    ward_number=ward_num,
                    year=year,
                    defaults={
                        "ward_name": ward_name,
                        "total_population": total_pop,
                        "male_population": male_pop,
                        "female_population": female_pop,
                        "other_population": other_pop,
                        "total_households": households,
                        "average_household_size": avg_size,
                        "area_sq_km": area,
                        "population_density": density,
                        "sex_ratio": sex_ratio,
                        "growth_rate": growth_rate,
                        # Default values for fields not in source data
                        "population_0_to_14": None,
                        "population_15_to_59": None,
                        "population_60_and_above": None,
                        "literacy_rate": None,
                        "male_literacy_rate": None,
                        "female_literacy_rate": None,
                    },
                )

                if created:
                    created_count += 1
                else:
                    updated_count += 1

        total_records = WardTimeSeriesPopulation.objects.count()
        total_population_2078 = sum(
            WardTimeSeriesPopulation.objects.filter(year=2078).values_list(
                "total_population", flat=True
            )
        )
        total_population_2081 = sum(
            WardTimeSeriesPopulation.objects.filter(year=2081).values_list(
                "total_population", flat=True
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nSuccessfully processed {len(ward_household_data)} ward household demographic records "
                f"({created_count} new, {updated_count} updated)\n"
                f"Total records in database: {total_records}\n"
                f"Total population 2078: {total_population_2078:,} people\n"
                f"Total population 2081: {total_population_2081:,} people"
            )
        )

        # Display year-wise summary
        self.stdout.write("\nYear-wise summary:")
        for year in [2078, 2081]:
            year_records = WardTimeSeriesPopulation.objects.filter(year=year)
            year_population = sum(
                year_records.values_list("total_population", flat=True)
            )
            year_households = sum(
                year_records.values_list("total_households", flat=True)
            )

            self.stdout.write(
                f"  वर्ष {year}: {year_records.count()} वडा, "
                f"{year_population:,} जनसंख्या, {year_households:,} घरपरिवार"
            )

        # Ward-wise summary for latest year
        self.stdout.write(f"\nWard-wise summary for 2081:")
        for ward_num in range(1, 8):
            try:
                ward_record = WardTimeSeriesPopulation.objects.get(
                    ward_number=ward_num, year=2081
                )
                self.stdout.write(
                    f"  वडा {ward_num}: {ward_record.total_population:,} जनसंख्या, "
                    f"{ward_record.total_households:,} घरपरिवार, "
                    f"घनत्व: {ward_record.population_density:.2f}"
                )
            except WardTimeSeriesPopulation.DoesNotExist:
                self.stdout.write(f"  वडा {ward_num}: डाटा उपलब्ध छैन")
