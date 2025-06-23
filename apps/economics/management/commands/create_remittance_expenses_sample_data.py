"""
Management command to create remittance expenses economics data based on actual data
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db import models
from apps.economics.models import (
    WardWiseRemittanceExpenses,
    RemittanceExpenseTypeChoice,
)
import uuid


class Command(BaseCommand):
    help = "Create remittance expenses economics data based on actual municipality-wide data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before creating new data",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write(
                self.style.WARNING("Clearing existing remittance expenses data...")
            )
            WardWiseRemittanceExpenses.objects.all().delete()

        self.stdout.write(
            "Creating remittance expenses economics data based on actual municipality-wide data..."
        )

        # Sample data representing actual remittance expense patterns by ward and type
        remittance_expenses_data = [
            # Ward 1
            {
                "id": str(uuid.uuid4()),
                "ward_number": 1,
                "remittance_expense": "business_investment",
                "households": 4,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 1,
                "remittance_expense": "education",
                "households": 335,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 1,
                "remittance_expense": "festivals",
                "households": 16,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 1,
                "remittance_expense": "goods_purchase",
                "households": 2,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 1,
                "remittance_expense": "health",
                "households": 350,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 1,
                "remittance_expense": "house_construction",
                "households": 43,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 1,
                "remittance_expense": "household_use",
                "households": 419,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 1,
                "remittance_expense": "land_ownership",
                "households": 8,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 1,
                "remittance_expense": "loan_payment",
                "households": 125,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 1,
                "remittance_expense": "loaned_others",
                "households": 50,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 1,
                "remittance_expense": "other",
                "households": 1,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 1,
                "remittance_expense": "saving",
                "households": 57,
            },
            # Ward 2
            {
                "id": str(uuid.uuid4()),
                "ward_number": 2,
                "remittance_expense": "education",
                "households": 200,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 2,
                "remittance_expense": "festivals",
                "households": 1,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 2,
                "remittance_expense": "health",
                "households": 222,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 2,
                "remittance_expense": "house_construction",
                "households": 27,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 2,
                "remittance_expense": "household_use",
                "households": 267,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 2,
                "remittance_expense": "loan_payment",
                "households": 126,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 2,
                "remittance_expense": "saving",
                "households": 121,
            },
            # Ward 3
            {
                "id": str(uuid.uuid4()),
                "ward_number": 3,
                "remittance_expense": "business_investment",
                "households": 1,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 3,
                "remittance_expense": "education",
                "households": 163,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 3,
                "remittance_expense": "festivals",
                "households": 2,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 3,
                "remittance_expense": "health",
                "households": 175,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 3,
                "remittance_expense": "house_construction",
                "households": 28,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 3,
                "remittance_expense": "household_use",
                "households": 247,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 3,
                "remittance_expense": "jwellery_purchase",
                "households": 2,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 3,
                "remittance_expense": "land_ownership",
                "households": 8,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 3,
                "remittance_expense": "loan_payment",
                "households": 133,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 3,
                "remittance_expense": "loaned_others",
                "households": 4,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 3,
                "remittance_expense": "other",
                "households": 3,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 3,
                "remittance_expense": "saving",
                "households": 28,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 3,
                "remittance_expense": "unknown",
                "households": 1,
            },
            # Ward 4
            {
                "id": str(uuid.uuid4()),
                "ward_number": 4,
                "remittance_expense": "education",
                "households": 264,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 4,
                "remittance_expense": "festivals",
                "households": 3,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 4,
                "remittance_expense": "goods_purchase",
                "households": 3,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 4,
                "remittance_expense": "health",
                "households": 286,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 4,
                "remittance_expense": "house_construction",
                "households": 22,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 4,
                "remittance_expense": "household_use",
                "households": 340,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 4,
                "remittance_expense": "jwellery_purchase",
                "households": 1,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 4,
                "remittance_expense": "land_ownership",
                "households": 4,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 4,
                "remittance_expense": "loan_payment",
                "households": 158,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 4,
                "remittance_expense": "loaned_others",
                "households": 1,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 4,
                "remittance_expense": "other",
                "households": 1,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 4,
                "remittance_expense": "saving",
                "households": 49,
            },
            # Ward 5
            {
                "id": str(uuid.uuid4()),
                "ward_number": 5,
                "remittance_expense": "business_investment",
                "households": 1,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 5,
                "remittance_expense": "education",
                "households": 194,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 5,
                "remittance_expense": "festivals",
                "households": 13,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 5,
                "remittance_expense": "goods_purchase",
                "households": 1,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 5,
                "remittance_expense": "health",
                "households": 198,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 5,
                "remittance_expense": "house_construction",
                "households": 28,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 5,
                "remittance_expense": "household_use",
                "households": 226,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 5,
                "remittance_expense": "land_ownership",
                "households": 15,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 5,
                "remittance_expense": "loan_payment",
                "households": 167,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 5,
                "remittance_expense": "loaned_others",
                "households": 1,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 5,
                "remittance_expense": "saving",
                "households": 6,
            },
            # Ward 6
            {
                "id": str(uuid.uuid4()),
                "ward_number": 6,
                "remittance_expense": "business_investment",
                "households": 4,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 6,
                "remittance_expense": "education",
                "households": 296,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 6,
                "remittance_expense": "festivals",
                "households": 6,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 6,
                "remittance_expense": "goods_purchase",
                "households": 8,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 6,
                "remittance_expense": "health",
                "households": 270,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 6,
                "remittance_expense": "house_construction",
                "households": 26,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 6,
                "remittance_expense": "household_use",
                "households": 362,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 6,
                "remittance_expense": "jwellery_purchase",
                "households": 1,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 6,
                "remittance_expense": "land_ownership",
                "households": 5,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 6,
                "remittance_expense": "loan_payment",
                "households": 177,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 6,
                "remittance_expense": "other",
                "households": 4,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 6,
                "remittance_expense": "saving",
                "households": 17,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 6,
                "remittance_expense": "unknown",
                "households": 7,
            },
            # Ward 7
            {
                "id": str(uuid.uuid4()),
                "ward_number": 7,
                "remittance_expense": "education",
                "households": 118,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 7,
                "remittance_expense": "health",
                "households": 153,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 7,
                "remittance_expense": "house_construction",
                "households": 13,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 7,
                "remittance_expense": "household_use",
                "households": 149,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 7,
                "remittance_expense": "jwellery_purchase",
                "households": 1,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 7,
                "remittance_expense": "land_ownership",
                "households": 3,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 7,
                "remittance_expense": "loan_payment",
                "households": 9,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 7,
                "remittance_expense": "other",
                "households": 1,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 7,
                "remittance_expense": "saving",
                "households": 6,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 7,
                "remittance_expense": "unknown",
                "households": 2,
            },
            # Ward 8
            {
                "id": str(uuid.uuid4()),
                "ward_number": 8,
                "remittance_expense": "education",
                "households": 22,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 8,
                "remittance_expense": "health",
                "households": 26,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 8,
                "remittance_expense": "household_use",
                "households": 28,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 8,
                "remittance_expense": "loan_payment",
                "households": 2,
            },
        ]

        # Check if data already exists
        existing_count = WardWiseRemittanceExpenses.objects.count()
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
            for data in remittance_expenses_data:
                obj, created = WardWiseRemittanceExpenses.objects.get_or_create(
                    ward_number=data["ward_number"],
                    remittance_expense=data["remittance_expense"],
                    defaults={
                        "id": data["id"],
                        "households": data["households"],
                    },
                )

                if created:
                    created_count += 1
                    self.stdout.write(
                        f"Created: Ward {data['ward_number']} - {data['remittance_expense']} ({data['households']} households)"
                    )
                else:
                    # Update existing record
                    obj.households = data["households"]
                    obj.save()
                    self.stdout.write(
                        f"Updated: Ward {data['ward_number']} - {data['remittance_expense']} ({data['households']} households)"
                    )

        # Print summary
        total_records = WardWiseRemittanceExpenses.objects.count()
        total_households = sum(
            WardWiseRemittanceExpenses.objects.values_list("households", flat=True)
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nSuccessfully processed {len(remittance_expenses_data)} remittance expenses economics records "
                f"({created_count} new, {len(remittance_expenses_data) - created_count} updated)\n"
                f"Total records in database: {total_records}\n"
                f"Total households using remittances: {total_households:,} households"
            )
        )

        # Print expense type breakdown
        self.stdout.write("\nRemittance expense type breakdown:")
        for expense_choice in RemittanceExpenseTypeChoice.choices:
            expense_code = expense_choice[0]
            expense_name = expense_choice[1]
            expense_households = (
                WardWiseRemittanceExpenses.objects.filter(
                    remittance_expense=expense_code
                ).aggregate(total=models.Sum("households"))["total"]
                or 0
            )

            if expense_households > 0:
                percentage = expense_households / total_households * 100
                self.stdout.write(
                    f"  {expense_name}: {expense_households:,} households ({percentage:.2f}%)"
                )
            else:
                self.stdout.write(f"  {expense_name}: 0 households (0.00%)")

        # Economic impact analysis
        self.stdout.write("\nEconomic Impact Analysis:")

        # Essential services
        essential_expenses = ["education", "health", "household_use"]
        essential_households = sum(
            WardWiseRemittanceExpenses.objects.filter(
                remittance_expense=expense
            ).aggregate(total=models.Sum("households"))["total"]
            or 0
            for expense in essential_expenses
        )
        essential_percentage = (
            (essential_households / total_households * 100)
            if total_households > 0
            else 0
        )

        self.stdout.write(
            f"  Essential services: {essential_households:,} households ({essential_percentage:.1f}%)"
        )

        # Investment activities
        investment_expenses = [
            "business_investment",
            "house_construction",
            "land_ownership",
        ]
        investment_households = sum(
            WardWiseRemittanceExpenses.objects.filter(
                remittance_expense=expense
            ).aggregate(total=models.Sum("households"))["total"]
            or 0
            for expense in investment_expenses
        )
        investment_percentage = (
            (investment_households / total_households * 100)
            if total_households > 0
            else 0
        )

        self.stdout.write(
            f"  Investment activities: {investment_households:,} households ({investment_percentage:.1f}%)"
        )

        # Financial obligations
        obligation_expenses = ["loan_payment"]
        obligation_households = sum(
            WardWiseRemittanceExpenses.objects.filter(
                remittance_expense=expense
            ).aggregate(total=models.Sum("households"))["total"]
            or 0
            for expense in obligation_expenses
        )
        obligation_percentage = (
            (obligation_households / total_households * 100)
            if total_households > 0
            else 0
        )

        self.stdout.write(
            f"  Financial obligations: {obligation_households:,} households ({obligation_percentage:.1f}%)"
        )

        # Savings
        saving_households = (
            WardWiseRemittanceExpenses.objects.filter(
                remittance_expense="saving"
            ).aggregate(total=models.Sum("households"))["total"]
            or 0
        )
        saving_percentage = (
            (saving_households / total_households * 100) if total_households > 0 else 0
        )

        self.stdout.write(
            f"  Savings: {saving_households:,} households ({saving_percentage:.1f}%)"
        )

        # Ward-wise summary
        self.stdout.write("\nWard-wise remittance usage summary:")
        for ward_num in range(1, 9):
            ward_households = (
                WardWiseRemittanceExpenses.objects.filter(
                    ward_number=ward_num
                ).aggregate(total=models.Sum("households"))["total"]
                or 0
            )
            if ward_households > 0:
                self.stdout.write(f"  वडा {ward_num}: {ward_households:,} households")

        # Economic insights
        self.stdout.write("\nEconomic Development Insights:")
        if essential_percentage > 60:
            self.stdout.write(
                "  📚 High essential service spending indicates basic needs prioritization"
            )

        if investment_percentage > 15:
            self.stdout.write(
                "  🏗️  Significant investment activity shows forward-looking financial behavior"
            )

        if obligation_percentage > 30:
            self.stdout.write("  ⚠️  High loan payment burden indicates debt stress")

        if saving_percentage > 10:
            self.stdout.write(
                "  💰 Good savings behavior indicates financial planning awareness"
            )

        self.stdout.write(
            f"\n💡 Remittance utilization shows {total_households:,} households benefiting from foreign employment"
        )
        self.stdout.write(
            "🎯 Focus areas: Productive investment, financial literacy, and local job creation"
        )
