"""
Management command to create all demographics sample data in one go
"""

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import transaction
import sys


class Command(BaseCommand):
    help = "Create all demographics sample data (religion, language, caste, househead, occupation, economically_active)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before creating new data for all demographics",
        )
        parser.add_argument(
            "--skip-errors",
            action="store_true",
            help="Continue with other commands even if one fails",
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS(
                "\n" + "=" * 80 + "\n"
                "CREATING ALL DEMOGRAPHICS SAMPLE DATA\n" + "=" * 80
            )
        )

        # List of all demographic commands to run
        demographic_commands = [
            ("create_demographic_summary_sample_data", "Demographic Summary"),
            ("create_ward_settlement_sample_data", "Ward Settlement Demographics"),
            ("create_religion_sample_data", "Religion Demographics"),
            ("create_language_sample_data", "Language Demographics"),
            ("create_caste_sample_data", "Caste Demographics"),
            ("create_househead_sample_data", "Househead Demographics"),
            ("create_occupation_sample_data", "Occupation Demographics"),
            (
                "create_economically_active_sample_data",
                "Economically Active Demographics",
            ),
        ]

        successful_commands = []
        failed_commands = []

        # Determine if we should clear data
        clear_data = options.get("clear", False)
        skip_errors = options.get("skip_errors", False)

        if clear_data:
            self.stdout.write(
                self.style.WARNING(
                    "\n⚠️  CLEARING ALL EXISTING DEMOGRAPHIC DATA\n"
                    "This will delete all existing demographic records.\n"
                )
            )

        # Run each command
        for command_name, description in demographic_commands:
            self.stdout.write(
                self.style.HTTP_INFO(f"\n📊 Running: {description}\n" + "-" * 50)
            )

            try:
                # Prepare command arguments
                command_args = []
                if clear_data:
                    command_args.append("--clear")

                # Run the command
                call_command(command_name, *command_args, verbosity=1)

                successful_commands.append((command_name, description))
                self.stdout.write(
                    self.style.SUCCESS(f"✅ Successfully completed: {description}")
                )

            except Exception as e:
                error_msg = f"❌ Failed to run {description}: {str(e)}"
                failed_commands.append((command_name, description, str(e)))

                if skip_errors:
                    self.stdout.write(self.style.ERROR(error_msg))
                    self.stdout.write(
                        self.style.WARNING("⏭️  Continuing with next command...")
                    )
                else:
                    self.stdout.write(self.style.ERROR(error_msg))
                    self.stdout.write(
                        self.style.ERROR(
                            "Use --skip-errors to continue with other commands if one fails."
                        )
                    )
                    sys.exit(1)

        # Print final summary
        self.print_summary(successful_commands, failed_commands)

    def print_summary(self, successful_commands, failed_commands):
        """Print a summary of the command execution"""
        self.stdout.write(
            self.style.SUCCESS(
                "\n" + "=" * 80 + "\n"
                "DEMOGRAPHICS SAMPLE DATA CREATION SUMMARY\n" + "=" * 80
            )
        )

        # Successful commands
        if successful_commands:
            self.stdout.write(
                self.style.SUCCESS(
                    f"\n✅ Successfully completed {len(successful_commands)} commands:\n"
                )
            )
            for command_name, description in successful_commands:
                self.stdout.write(f"   • {description}")

        # Failed commands
        if failed_commands:
            self.stdout.write(
                self.style.ERROR(f"\n❌ Failed {len(failed_commands)} commands:\n")
            )
            for command_name, description, error in failed_commands:
                self.stdout.write(f"   • {description}: {error}")

        # Overall status
        total_commands = len(successful_commands) + len(failed_commands)
        if failed_commands:
            self.stdout.write(
                self.style.WARNING(
                    f"\n⚠️  {len(successful_commands)}/{total_commands} commands completed successfully"
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"\n🎉 All {total_commands} demographic commands completed successfully!"
                )
            )

        self.stdout.write("\n" + "=" * 80 + "\n")

        # Usage examples
        self.stdout.write(
            self.style.HTTP_INFO(
                "Usage examples:\n"
                "  python manage.py create_demographics_sample_data\n"
                "  python manage.py create_demographics_sample_data --clear\n"
                "  python manage.py create_demographics_sample_data --clear --skip-errors\n"
            )
        )
