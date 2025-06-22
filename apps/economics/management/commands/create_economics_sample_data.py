"""
Management command to create all economics sample data in one go.

This command runs all economics-related sample data creation commands:
- Major Skills Sample Data
- Remittance Expenses Sample Data
"""

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import transaction
import io
import sys


class Command(BaseCommand):
    help = "Create all economics sample data (major skills, remittance expenses)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before creating new data (passed to all commands)",
        )
        parser.add_argument(
            "--quiet",
            action="store_true",
            help="Suppress individual command output (show only summary)",
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS(
                "🔄 Starting consolidated economics sample data creation...\n"
            )
        )

        # List of economics commands to run
        economics_commands = [
            {
                "command": "create_major_skills_sample_data",
                "description": "Major Skills Sample Data",
                "app": "economics",
            },
            {
                "command": "create_remittance_expenses_sample_data",
                "description": "Remittance Expenses Sample Data",
                "app": "economics",
            },
            {
                "command": "create_wardwise_house_ownership_sample_data",
                "description": "Ward Wise House Ownership Sample Data",
                "app": "economics",
            },
            {
                "command": "create_wardwise_house_base_sample_data",
                "description": "Ward Wise House Base Sample Data",
                "app": "economics",
            },
            {
                "command": "create_wardwise_house_outer_wall_sample_data",
                "description": "Ward Wise House Outer Wall Sample Data",
                "app": "economics",
            },
            {
                "command": "create_municipality_wide_foreign_employment_countries_sample_data",
                "description": "Municipality Wide Foreign Employment Countries Sample Data",
                "app": "economics",
            },
        ]

        # Track results
        results = {
            "successful": [],
            "failed": [],
            "total_commands": len(economics_commands),
        }

        # Execute each command
        for i, cmd_info in enumerate(economics_commands, 1):
            command_name = cmd_info["command"]
            description = cmd_info["description"]

            self.stdout.write(
                f"[{i}/{len(economics_commands)}] Running {description}..."
            )

            try:
                # Prepare command arguments
                cmd_args = []
                cmd_kwargs = {}

                if options["clear"]:
                    cmd_kwargs["clear"] = True

                # Capture output if quiet mode
                if options["quiet"]:
                    # Redirect stdout to capture output
                    old_stdout = sys.stdout
                    old_stderr = sys.stderr
                    sys.stdout = io.StringIO()
                    sys.stderr = io.StringIO()

                # Run the command
                with transaction.atomic():
                    call_command(command_name, *cmd_args, **cmd_kwargs)

                # Restore stdout if it was redirected
                if options["quiet"]:
                    captured_output = sys.stdout.getvalue()
                    captured_errors = sys.stderr.getvalue()
                    sys.stdout = old_stdout
                    sys.stderr = old_stderr

                    # Show minimal success message
                    self.stdout.write(
                        self.style.SUCCESS(f"  ✅ {description} completed successfully")
                    )
                else:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"  ✅ {description} completed successfully\n"
                        )
                    )

                results["successful"].append(
                    {"command": command_name, "description": description}
                )

            except Exception as e:
                # Restore stdout if it was redirected and there was an error
                if options["quiet"]:
                    if "old_stdout" in locals():
                        sys.stdout = old_stdout
                        sys.stderr = old_stderr

                error_msg = str(e)
                self.stdout.write(
                    self.style.ERROR(f"  ❌ {description} failed: {error_msg}")
                )

                results["failed"].append(
                    {
                        "command": command_name,
                        "description": description,
                        "error": error_msg,
                    }
                )

        # Print summary
        self.stdout.write("\n" + "=" * 70)
        self.stdout.write(
            self.style.SUCCESS("📊 ECONOMICS SAMPLE DATA CREATION SUMMARY")
        )
        self.stdout.write("=" * 70)

        self.stdout.write(f"Total commands executed: {results['total_commands']}")
        self.stdout.write(
            self.style.SUCCESS(f"✅ Successful: {len(results['successful'])}")
        )

        if results["successful"]:
            for result in results["successful"]:
                self.stdout.write(f"   • {result['description']}")

        if results["failed"]:
            self.stdout.write(self.style.ERROR(f"❌ Failed: {len(results['failed'])}"))
            for result in results["failed"]:
                self.stdout.write(f"   • {result['description']}: {result['error']}")

        # Final status
        if len(results["failed"]) == 0:
            self.stdout.write(
                self.style.SUCCESS(
                    f"\n🎉 All {results['total_commands']} economics sample data commands completed successfully!"
                )
            )

            # Show data summary
            self.stdout.write("\n" + "=" * 50)
            self.stdout.write("📈 ECONOMICS DATA OVERVIEW")
            self.stdout.write("=" * 50)

            try:
                # Import models to show summary
                from apps.economics.models import (
                    WardWiseMajorSkills,
                    WardWiseRemittanceExpenses,
                )
                from django.db.models import Sum

                # Major Skills Summary
                skills_count = WardWiseMajorSkills.objects.count()
                skills_population = (
                    WardWiseMajorSkills.objects.aggregate(total=Sum("population"))[
                        "total"
                    ]
                    or 0
                )

                self.stdout.write(f"Major Skills Records: {skills_count:,}")
                self.stdout.write(f"Total Skills Population: {skills_population:,}")

                # Remittance Expenses Summary
                expenses_count = WardWiseRemittanceExpenses.objects.count()
                expenses_households = (
                    WardWiseRemittanceExpenses.objects.aggregate(
                        total=Sum("households")
                    )["total"]
                    or 0
                )

                self.stdout.write(f"Remittance Expense Records: {expenses_count:,}")
                self.stdout.write(
                    f"Total Remittance Households: {expenses_households:,}"
                )

                # Ward coverage
                skills_wards = (
                    WardWiseMajorSkills.objects.values_list("ward_number", flat=True)
                    .distinct()
                    .count()
                )
                expenses_wards = (
                    WardWiseRemittanceExpenses.objects.values_list(
                        "ward_number", flat=True
                    )
                    .distinct()
                    .count()
                )

                self.stdout.write(f"Wards covered (Skills): {skills_wards}")
                self.stdout.write(f"Wards covered (Remittance): {expenses_wards}")

            except Exception as e:
                self.stdout.write(f"Could not generate data summary: {e}")

        else:
            self.stdout.write(
                self.style.WARNING(
                    f"\n⚠️  {len(results['failed'])} out of {results['total_commands']} commands failed. "
                    "Please check the errors above."
                )
            )
            # Set exit code to indicate partial failure
            sys.exit(1)

        self.stdout.write(
            f"\n💡 Tip: Use --quiet flag to suppress individual command output"
        )
        self.stdout.write(
            f"💡 Tip: Use --clear flag to clear existing data before creation"
        )
