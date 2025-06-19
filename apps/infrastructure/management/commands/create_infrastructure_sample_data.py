"""
Consolidated management command to create all infrastructure sample data.

This command runs all infrastructure-related sample data creation commands:
- Market Center Time Sample Data
- Public Transport Sample Data
- Road Status Sample Data
"""

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import transaction


class Command(BaseCommand):
    help = "Create all infrastructure sample data with a single command"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before creating new data (passed to all sub-commands)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show which commands would be run without executing them",
        )

    def handle(self, *args, **options):
        # List of all infrastructure commands to run
        infrastructure_commands = [
            ("create_market_center_time_sample_data", "Market Center Time Sample Data"),
            ("create_public_transport_sample_data", "Public Transport Sample Data"),
            ("create_road_status_sample_data", "Road Status Sample Data"),
        ]

        clear_flag = options.get("clear", False)
        dry_run = options.get("dry_run", False)

        self.stdout.write(self.style.SUCCESS("=" * 70))
        self.stdout.write(self.style.SUCCESS("🏗️  INFRASTRUCTURE SAMPLE DATA CREATION"))
        self.stdout.write(self.style.SUCCESS("=" * 70))

        if dry_run:
            self.stdout.write(
                self.style.WARNING("DRY RUN MODE - No commands will be executed")
            )

        if clear_flag:
            self.stdout.write(
                self.style.WARNING("⚠️  CLEAR MODE: All existing data will be deleted")
            )

        self.stdout.write(
            f"\nRunning {len(infrastructure_commands)} infrastructure commands...\n"
        )

        # Show commands that will be run
        for i, (command_name, description) in enumerate(infrastructure_commands, 1):
            status = "WOULD RUN" if dry_run else "RUNNING"
            self.stdout.write(f"{i}. {status}: {description}")
            if dry_run:
                self.stdout.write(
                    f'   Command: python manage.py {command_name}{"" if not clear_flag else " --clear"}'
                )

        if dry_run:
            self.stdout.write("\n" + "=" * 70)
            self.stdout.write("Use without --dry-run to execute these commands")
            return

        # Execute each command
        success_count = 0
        total_commands = len(infrastructure_commands)

        for i, (command_name, description) in enumerate(infrastructure_commands, 1):
            self.stdout.write("\n" + "-" * 70)
            self.stdout.write(f"[{i}/{total_commands}] Creating {description}...")
            self.stdout.write("-" * 70)

            try:
                with transaction.atomic():
                    # Prepare command arguments
                    command_args = []
                    command_kwargs = {}

                    if clear_flag:
                        command_kwargs["clear"] = True

                    # Execute the command
                    call_command(command_name, *command_args, **command_kwargs)

                success_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"✅ Successfully completed: {description}")
                )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"❌ Failed to run {command_name}: {str(e)}")
                )
                continue

        # Final summary
        self.stdout.write("\n" + "=" * 70)
        self.stdout.write("📊 INFRASTRUCTURE SAMPLE DATA CREATION SUMMARY")
        self.stdout.write("=" * 70)

        if success_count == total_commands:
            self.stdout.write(
                self.style.SUCCESS(
                    f"🎉 All {total_commands} infrastructure commands completed successfully!"
                )
            )
        else:
            failed_count = total_commands - success_count
            self.stdout.write(
                self.style.WARNING(
                    f"⚠️  {success_count}/{total_commands} commands completed successfully. "
                    f"{failed_count} failed."
                )
            )

        self.stdout.write("\n📋 Infrastructure categories processed:")
        for command_name, description in infrastructure_commands:
            self.stdout.write(f"   • {description}")

        self.stdout.write(
            "\n🎯 Infrastructure data is now ready for report generation!"
        )
        self.stdout.write("=" * 70)
