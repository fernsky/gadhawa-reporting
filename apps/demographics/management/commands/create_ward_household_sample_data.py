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

        # Actual ward household time series data for Gadhawa
        # Each dict matches the model fields
        ward_household_data = [
            {
                "ward_number": 1,
                "ward_name": "गोवरडिहा(१,२,३)",
                "year": 2078,
                "total_population": 7561,
                "male_population": 3619,
                "female_population": 3942,
                "other_population": None,
                "total_households": 1688,
                "average_household_size": 4.48,
                "population_0_to_14": None,
                "population_15_to_59": None,
                "population_60_and_above": None,
                "literacy_rate": None,
                "male_literacy_rate": None,
                "female_literacy_rate": None,
                "growth_rate": None,
                "area_sq_km": None,
                "population_density": None,
                "sex_ratio": 91.81,
            },
            {
                "ward_number": 2,
                "ward_name": "गोवरडिहा(४-६)",
                "year": 2078,
                "total_population": 5596,
                "male_population": 2754,
                "female_population": 2842,
                "other_population": None,
                "total_households": 1169,
                "average_household_size": 4.79,
                "population_0_to_14": None,
                "population_15_to_59": None,
                "population_60_and_above": None,
                "literacy_rate": None,
                "male_literacy_rate": None,
                "female_literacy_rate": None,
                "growth_rate": None,
                "area_sq_km": None,
                "population_density": None,
                "sex_ratio": 96.9,
            },
            {
                "ward_number": 3,
                "ward_name": "गोवरडिहा(७,८,९)",
                "year": 2078,
                "total_population": 5049,
                "male_population": 2439,
                "female_population": 2610,
                "other_population": None,
                "total_households": 1135,
                "average_household_size": 4.45,
                "population_0_to_14": None,
                "population_15_to_59": None,
                "population_60_and_above": None,
                "literacy_rate": None,
                "male_literacy_rate": None,
                "female_literacy_rate": None,
                "growth_rate": None,
                "area_sq_km": None,
                "population_density": None,
                "sex_ratio": 93.45,
            },
            {
                "ward_number": 4,
                "ward_name": "गँगापरस्पुर(१,२,३,५)",
                "year": 2078,
                "total_population": 5983,
                "male_population": 2971,
                "female_population": 3012,
                "other_population": None,
                "total_households": 1265,
                "average_household_size": 4.73,
                "population_0_to_14": None,
                "population_15_to_59": None,
                "population_60_and_above": None,
                "literacy_rate": None,
                "male_literacy_rate": None,
                "female_literacy_rate": None,
                "growth_rate": None,
                "area_sq_km": None,
                "population_density": None,
                "sex_ratio": 98.64,
            },
            {
                "ward_number": 5,
                "ward_name": "गँगापरस्पुर(४,६,७,८,९)",
                "year": 2078,
                "total_population": 6901,
                "male_population": 3374,
                "female_population": 3527,
                "other_population": None,
                "total_households": 1482,
                "average_household_size": 4.66,
                "population_0_to_14": None,
                "population_15_to_59": None,
                "population_60_and_above": None,
                "literacy_rate": None,
                "male_literacy_rate": None,
                "female_literacy_rate": None,
                "growth_rate": None,
                "area_sq_km": None,
                "population_density": None,
                "sex_ratio": 95.66,
            },
            {
                "ward_number": 6,
                "ward_name": "गढवा(१,२,३,४,५)",
                "year": 2078,
                "total_population": 7847,
                "male_population": 3819,
                "female_population": 4028,
                "other_population": None,
                "total_households": 1714,
                "average_household_size": 4.58,
                "population_0_to_14": None,
                "population_15_to_59": None,
                "population_60_and_above": None,
                "literacy_rate": None,
                "male_literacy_rate": None,
                "female_literacy_rate": None,
                "growth_rate": None,
                "area_sq_km": None,
                "population_density": None,
                "sex_ratio": 94.81,
            },
            {
                "ward_number": 7,
                "ward_name": "गढवा(६,७,८,९)",
                "year": 2078,
                "total_population": 6111,
                "male_population": 2925,
                "female_population": 3186,
                "other_population": None,
                "total_households": 1320,
                "average_household_size": 4.63,
                "population_0_to_14": None,
                "population_15_to_59": None,
                "population_60_and_above": None,
                "literacy_rate": None,
                "male_literacy_rate": None,
                "female_literacy_rate": None,
                "growth_rate": None,
                "area_sq_km": None,
                "population_density": None,
                "sex_ratio": 91.81,
            },
            {
                "ward_number": 8,
                "ward_name": "कोइलाबास(१ देखि ९)",
                "year": 2078,
                "total_population": 850,
                "male_population": 407,
                "female_population": 443,
                "other_population": None,
                "total_households": 191,
                "average_household_size": 4.45,
                "population_0_to_14": None,
                "population_15_to_59": None,
                "population_60_and_above": None,
                "literacy_rate": None,
                "male_literacy_rate": None,
                "female_literacy_rate": None,
                "growth_rate": None,
                "area_sq_km": None,
                "population_density": None,
                "sex_ratio": 91.87,
            },
            {
                "ward_number": 1,
                "ward_name": "गोवरडिहा(१,२,३)",
                "year": 2081,
                "total_population": 7775,
                "male_population": 3720,
                "female_population": 4052,
                "other_population": 3,
                "total_households": 1735,
                "average_household_size": 4.481268011527377,
                "population_0_to_14": 2206,
                "population_15_to_59": 4982,
                "population_60_and_above": 587,
                "literacy_rate": 79.89083596667625,
                "male_literacy_rate": 83.12937062937063,
                "female_literacy_rate": 76.73561915556814,
                "growth_rate": None,
                "area_sq_km": None,
                "population_density": None,
                "sex_ratio": 108.92473118279571,
            },
            {
                "ward_number": 2,
                "ward_name": "गोवरडिहा(४-६)",
                "year": 2081,
                "total_population": 5824,
                "male_population": 2902,
                "female_population": 2921,
                "other_population": 1,
                "total_households": 1201,
                "average_household_size": 4.849292256452956,
                "population_0_to_14": 1254,
                "population_15_to_59": 4000,
                "population_60_and_above": 570,
                "literacy_rate": 80.21569356638155,
                "male_literacy_rate": 86.30239520958084,
                "female_literacy_rate": 74.23290203327171,
                "growth_rate": None,
                "area_sq_km": None,
                "population_density": None,
                "sex_ratio": 100.65472088215024,
            },
            {
                "ward_number": 3,
                "ward_name": "गोवरडिहा(७,८,९)",
                "year": 2081,
                "total_population": 5784,
                "male_population": 2912,
                "female_population": 2872,
                "other_population": 0,
                "total_households": 1294,
                "average_household_size": 4.469860896445131,
                "population_0_to_14": 1163,
                "population_15_to_59": 4092,
                "population_60_and_above": 529,
                "literacy_rate": 82.90406868234416,
                "male_literacy_rate": 88.23529411764706,
                "female_literacy_rate": 77.54491017964071,
                "growth_rate": None,
                "area_sq_km": None,
                "population_density": None,
                "sex_ratio": 98.62637362637363,
            },
            {
                "ward_number": 4,
                "ward_name": "गँगापरस्पुर(१,२,३,५)",
                "year": 2081,
                "total_population": 6151,
                "male_population": 3054,
                "female_population": 3096,
                "other_population": 1,
                "total_households": 1300,
                "average_household_size": 4.731538461538461,
                "population_0_to_14": 1510,
                "population_15_to_59": 4071,
                "population_60_and_above": 570,
                "literacy_rate": 82.59555555555555,
                "male_literacy_rate": 87.9685826490539,
                "female_literacy_rate": 77.26628895184136,
                "growth_rate": None,
                "area_sq_km": None,
                "population_density": None,
                "sex_ratio": 101.37524557956779,
            },
            {
                "ward_number": 5,
                "ward_name": "गँगापरस्पुर(४,६,७,८,९)",
                "year": 2081,
                "total_population": 7168,
                "male_population": 3541,
                "female_population": 3625,
                "other_population": 2,
                "total_households": 1522,
                "average_household_size": 4.709592641261498,
                "population_0_to_14": 1568,
                "population_15_to_59": 4853,
                "population_60_and_above": 747,
                "literacy_rate": 79.72747918243755,
                "male_literacy_rate": 84.41917639827903,
                "female_literacy_rate": 75.16417910447761,
                "growth_rate": None,
                "area_sq_km": None,
                "population_density": None,
                "sex_ratio": 102.37221123976279,
            },
            {
                "ward_number": 6,
                "ward_name": "गढवा(१,२,३,४,५)",
                "year": 2081,
                "total_population": 8069,
                "male_population": 3926,
                "female_population": 4140,
                "other_population": 3,
                "total_households": 1761,
                "average_household_size": 4.58205565019875,
                "population_0_to_14": 1916,
                "population_15_to_59": 5295,
                "population_60_and_above": 858,
                "literacy_rate": 78.11019358332206,
                "male_literacy_rate": 84.79931682322801,
                "female_literacy_rate": 72.06300025819779,
                "growth_rate": None,
                "area_sq_km": None,
                "population_density": None,
                "sex_ratio": 105.4508405501783,
            },
            {
                "ward_number": 7,
                "ward_name": "गढवा(६,७,८,९)",
                "year": 2081,
                "total_population": 6285,
                "male_population": 3007,
                "female_population": 3275,
                "other_population": 3,
                "total_households": 1357,
                "average_household_size": 4.631540162122329,
                "population_0_to_14": 1600,
                "population_15_to_59": 4114,
                "population_60_and_above": 571,
                "literacy_rate": 75.00878734622144,
                "male_literacy_rate": 82.64790764790764,
                "female_literacy_rate": 67.76406035665295,
                "growth_rate": None,
                "area_sq_km": None,
                "population_density": None,
                "sex_ratio": 108.91253741270368,
            },
            {
                "ward_number": 8,
                "ward_name": "कोइलाबास(१ देखि ९)",
                "year": 2081,
                "total_population": 873,
                "male_population": 418,
                "female_population": 455,
                "other_population": 0,
                "total_households": 196,
                "average_household_size": 4.454081632653061,
                "population_0_to_14": 278,
                "population_15_to_59": 516,
                "population_60_and_above": 79,
                "literacy_rate": 89.1566265060241,
                "male_literacy_rate": 94.21052631578948,
                "female_literacy_rate": 83.92370572207084,
                "growth_rate": None,
                "area_sq_km": None,
                "population_density": None,
                "sex_ratio": 108.85167464114834,
            },
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
            for entry in ward_household_data:
                # Create or update record
                record, created = WardTimeSeriesPopulation.objects.update_or_create(
                    ward_number=entry["ward_number"],
                    year=entry["year"],
                    defaults={
                        "ward_name": entry["ward_name"],
                        "total_population": entry["total_population"],
                        "male_population": entry["male_population"],
                        "female_population": entry["female_population"],
                        "other_population": entry["other_population"],
                        "total_households": entry["total_households"],
                        "average_household_size": entry["average_household_size"],
                        "population_0_to_14": entry["population_0_to_14"],
                        "population_15_to_59": entry["population_15_to_59"],
                        "population_60_and_above": entry["population_60_and_above"],
                        "literacy_rate": entry["literacy_rate"],
                        "male_literacy_rate": entry["male_literacy_rate"],
                        "female_literacy_rate": entry["female_literacy_rate"],
                        "growth_rate": entry["growth_rate"],
                        "area_sq_km": entry["area_sq_km"],
                        "population_density": entry["population_density"],
                        "sex_ratio": entry["sex_ratio"],
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
