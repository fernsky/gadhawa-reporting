"""
Consolidated management command to create all social sample data.

This command runs all social-related sample data creation commands:
- Literacy Status Sample Data
- Major Subject Sample Data
- Old Age and Single Women Sample Data
- School Dropout Sample Data
- Solid Waste Management Sample Data
- Toilet Type Sample Data
"""

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import transaction


class Command(BaseCommand):
    help = "Create all social sample data with a single command"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before creating new data (passed to sub-commands that support it)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show which commands would be run without executing them",
        )

    def handle(self, *args, **options):
        # List of all social commands to run with their clear argument patterns
        social_commands = [
            (
                "create_literacy_status_sample_data",
                "Literacy Status Sample Data",
                "reset",
            ),
            (
                "create_educational_institution_sample_data",
                "Educational Institution Sample Data",
                "reset",
            ),
            (
                "create_teacher_staffing_sample_data",
                "Teacher Staffing Sample Data",
                "reset",
            ),
            ("create_major_subject_sample_data", "Major Subject Sample Data", None),
            (
                "create_old_age_single_women_sample_data",
                "Old Age and Single Women Sample Data",
                None,
            ),
            (
                "create_school_dropout_sample_data",
                "School Dropout Sample Data",
                "clear",
            ),
            (
                "create_solid_waste_management_sample_data",
                "Solid Waste Management Sample Data",
                "clear",
            ),
            ("create_toilet_type_sample_data", "Toilet Type Sample Data", "clear"),
        ]

        clear_flag = options.get("clear", False)
        dry_run = options.get("dry_run", False)

        self.stdout.write(self.style.SUCCESS("=" * 70))
        self.stdout.write(self.style.SUCCESS("👥 SOCIAL SAMPLE DATA CREATION"))
        self.stdout.write(self.style.SUCCESS("=" * 70))

        if dry_run:
            self.stdout.write(
                self.style.WARNING("DRY RUN MODE - No commands will be executed")
            )

        if clear_flag:
            self.stdout.write(
                self.style.WARNING(
                    "⚠️  CLEAR MODE: All existing data will be deleted (where supported)"
                )
            )

        self.stdout.write(f"\nRunning {len(social_commands)} social commands...\n")

        # Show commands that will be run
        for i, (command_name, description, clear_arg) in enumerate(social_commands, 1):
            status = "WOULD RUN" if dry_run else "RUNNING"
            self.stdout.write(f"{i}. {status}: {description}")
            if dry_run:
                clear_part = ""
                if clear_flag and clear_arg:
                    clear_part = f" --{clear_arg}"
                elif clear_flag and not clear_arg:
                    clear_part = " (no clear option available)"
                self.stdout.write(
                    f"   Command: python manage.py {command_name}{clear_part}"
                )

        if dry_run:
            self.stdout.write("\n" + "=" * 70)
            self.stdout.write("Use without --dry-run to execute these commands")
            return

        # Execute each command
        success_count = 0
        total_commands = len(social_commands)

        for i, (command_name, description, clear_arg) in enumerate(social_commands, 1):
            self.stdout.write("\n" + "-" * 70)
            self.stdout.write(f"[{i}/{total_commands}] Creating {description}...")
            self.stdout.write("-" * 70)

            try:
                with transaction.atomic():
                    # Prepare command arguments
                    command_args = []
                    command_kwargs = {}

                    # Add clear argument if supported and requested
                    if clear_flag and clear_arg:
                        command_kwargs[clear_arg] = True

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
        self.stdout.write("📊 SOCIAL SAMPLE DATA CREATION SUMMARY")
        self.stdout.write("=" * 70)

        if success_count == total_commands:
            self.stdout.write(
                self.style.SUCCESS(
                    f"🎉 All {total_commands} social commands completed successfully!"
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

        self.stdout.write("\n📋 Social categories processed:")
        for command_name, description, clear_arg in social_commands:
            clear_support = "✓" if clear_arg else "✗"
            self.stdout.write(f"   • {description} (Clear support: {clear_support})")

        self.stdout.write("\n🎯 Social data is now ready for report generation!")
        self.stdout.write("\n📝 Note: Some commands may not support the --clear flag")
        self.stdout.write("=" * 70)
