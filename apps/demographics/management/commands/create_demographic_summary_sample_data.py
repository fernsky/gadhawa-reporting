"""
Management command to create demographic summary data based on actual data
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from apps.demographics.models import DemographicSummary


class Command(BaseCommand):
    help = "Create demographic summary data based on actual municipality-wide data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before creating new data",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write("Clearing existing demographic summary data...")
            DemographicSummary.objects.all().delete()

        self.stdout.write(
            "Creating demographic summary data based on actual municipality-wide data..."
        )

        # Based on the provided JSON data
        demographic_data = {
            "id": "singleton",
            "total_population": 27495,
            "population_male": 12858,
            "population_female": 14637,
            "population_other": 0,
            "population_absentee_total": 0,
            "population_male_absentee": 0,
            "population_female_absentee": 0,
            "population_other_absentee": 0,
            "sex_ratio": 87.85,
            "total_households": 5639,
            "average_household_size": 4.88,
            "population_density": 203.31,
            "population_0_to_14": 7894,
            "population_15_to_59": 16803,
            "population_60_and_above": 2798,
            "growth_rate": None,
            "literacy_rate_above_15": None,
            "literacy_rate_15_to_24": None,
        }

        try:
            with transaction.atomic():
                demographic_summary, created = (
                    DemographicSummary.objects.update_or_create(
                        id="singleton", defaults=demographic_data
                    )
                )

                if created:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"✓ Created demographic summary with total population: {demographic_summary.total_population}"
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"✓ Updated demographic summary with total population: {demographic_summary.total_population}"
                        )
                    )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Error creating demographic summary data: {str(e)}")
            )
            return

        self.stdout.write(
            self.style.SUCCESS("Successfully created demographic summary data!")
        )

        # Print summary
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write("DEMOGRAPHIC SUMMARY CREATION SUMMARY")
        self.stdout.write("=" * 50)
        self.stdout.write(f"Total Population: {demographic_data['total_population']:,}")
        self.stdout.write(f"Male Population: {demographic_data['population_male']:,}")
        self.stdout.write(
            f"Female Population: {demographic_data['population_female']:,}"
        )
        self.stdout.write(f"Sex Ratio: {demographic_data['sex_ratio']}")
        self.stdout.write(f"Total Households: {demographic_data['total_households']:,}")
        self.stdout.write(
            f"Average Household Size: {demographic_data['average_household_size']}"
        )
        self.stdout.write(
            f"Population Density: {demographic_data['population_density']} per sq km"
        )
        self.stdout.write("=" * 50)
