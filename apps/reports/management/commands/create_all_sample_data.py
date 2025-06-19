"""
Master consolidated management command to create ALL sample data across all domains.

This command runs all sample data creation commands from all domains:
- Demographics Sample Data (religion, language, caste, househead, occupation, economically_active)
- Economics Sample Data (major skills, remittance expenses)
- Infrastructure Sample Data (market center time, public transport, road status)
- Social Sample Data (literacy, major subjects, old age, school dropout, solid waste, toilet type)
"""

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import transaction
import time


class Command(BaseCommand):
    help = "Create ALL sample data across all domains with a single command"

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
        parser.add_argument(
            "--skip-errors",
            action="store_true",
            help="Continue with other domains even if one domain fails",
        )

    def handle(self, *args, **options):
        # List of all consolidated domain commands
        domain_commands = [
            (
                "create_demographics_sample_data",
                "Demographics Sample Data",
                "demographics",
            ),
            ("create_economics_sample_data", "Economics Sample Data", "economics"),
            (
                "create_infrastructure_sample_data",
                "Infrastructure Sample Data",
                "infrastructure",
            ),
            ("create_social_sample_data", "Social Sample Data", "social"),
        ]

        clear_flag = options.get("clear", False)
        dry_run = options.get("dry_run", False)
        skip_errors = options.get("skip_errors", False)

        self.stdout.write(self.style.SUCCESS("=" * 80))
        self.stdout.write(
            self.style.SUCCESS("🌟 MASTER SAMPLE DATA CREATION - ALL DOMAINS")
        )
        self.stdout.write(self.style.SUCCESS("=" * 80))

        if dry_run:
            self.stdout.write(
                self.style.WARNING("🔍 DRY RUN MODE - No commands will be executed")
            )

        if clear_flag:
            self.stdout.write(
                self.style.WARNING(
                    "⚠️  CLEAR MODE: All existing data will be deleted across all domains"
                )
            )

        if skip_errors:
            self.stdout.write(
                self.style.HTTP_INFO(
                    "🔄 SKIP ERRORS MODE: Will continue with other domains if one fails"
                )
            )

        self.stdout.write(f"\n🚀 Running {len(domain_commands)} domain commands...\n")

        # Show commands that will be run
        for i, (command_name, description, domain) in enumerate(domain_commands, 1):
            status = "WOULD RUN" if dry_run else "RUNNING"
            self.stdout.write(f"{i}. {status}: {description} ({domain})")
            if dry_run:
                flags = []
                if clear_flag:
                    flags.append("--clear")
                if skip_errors and domain == "demographics":
                    flags.append("--skip-errors")
                flag_str = " " + " ".join(flags) if flags else ""
                self.stdout.write(
                    f"   Command: python manage.py {command_name}{flag_str}"
                )

        if dry_run:
            self.stdout.write("\n" + "=" * 80)
            self.stdout.write("Use without --dry-run to execute these commands")
            self.stdout.write("=" * 80)
            return

        # Execute each domain command
        start_time = time.time()
        success_count = 0
        total_commands = len(domain_commands)
        results = []

        for i, (command_name, description, domain) in enumerate(domain_commands, 1):
            self.stdout.write("\n" + "=" * 80)
            self.stdout.write(
                f"[{i}/{total_commands}] 🏗️  CREATING {description.upper()}"
            )
            self.stdout.write("=" * 80)

            domain_start_time = time.time()

            try:
                # Prepare command arguments
                command_args = []
                command_kwargs = {}

                # Add clear argument
                if clear_flag:
                    command_kwargs["clear"] = True

                # Add skip-errors flag for demographics
                if skip_errors and domain == "demographics":
                    command_kwargs["skip_errors"] = True

                # Execute the command
                call_command(command_name, *command_args, **command_kwargs)

                domain_duration = time.time() - domain_start_time
                success_count += 1

                result = {
                    "domain": domain,
                    "description": description,
                    "status": "success",
                    "duration": domain_duration,
                }
                results.append(result)

                self.stdout.write(
                    self.style.SUCCESS(
                        f"✅ Successfully completed: {description} "
                        f"(took {domain_duration:.1f}s)"
                    )
                )

            except Exception as e:
                domain_duration = time.time() - domain_start_time
                error_msg = str(e)

                result = {
                    "domain": domain,
                    "description": description,
                    "status": "failed",
                    "error": error_msg,
                    "duration": domain_duration,
                }
                results.append(result)

                self.stdout.write(
                    self.style.ERROR(
                        f"❌ Failed to run {command_name}: {error_msg} "
                        f"(took {domain_duration:.1f}s)"
                    )
                )

                if not skip_errors:
                    self.stdout.write(
                        self.style.ERROR(
                            "Use --skip-errors to continue with other domains if one fails."
                        )
                    )
                    break
                else:
                    self.stdout.write(
                        self.style.WARNING("⏭️  Continuing with next domain...")
                    )

        # Calculate total duration
        total_duration = time.time() - start_time

        # Final summary
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write("📊 MASTER SAMPLE DATA CREATION SUMMARY")
        self.stdout.write("=" * 80)

        # Success/failure counts
        failed_count = total_commands - success_count
        if success_count == total_commands:
            self.stdout.write(
                self.style.SUCCESS(
                    f"🎉 ALL {total_commands} domain commands completed successfully!"
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f"⚠️  {success_count}/{total_commands} domain commands completed successfully. "
                    f"{failed_count} failed."
                )
            )

        # Detailed results
        self.stdout.write(f"\n📋 Domain execution results:")
        for result in results:
            if result["status"] == "success":
                self.stdout.write(
                    f"   ✅ {result['description']}: SUCCESS ({result['duration']:.1f}s)"
                )
            else:
                self.stdout.write(
                    f"   ❌ {result['description']}: FAILED ({result['duration']:.1f}s)"
                )
                self.stdout.write(f"      Error: {result['error']}")

        # Performance summary
        self.stdout.write(f"\n⏱️  Total execution time: {total_duration:.1f} seconds")
        if success_count > 0:
            avg_time = (
                sum(r["duration"] for r in results if r["status"] == "success")
                / success_count
            )
            self.stdout.write(f"📈 Average time per domain: {avg_time:.1f} seconds")

        # Data overview
        if success_count == total_commands:
            self.stdout.write(
                f"\n🎯 All sample data is now ready for report generation!"
            )
            self.stdout.write(f"\n📦 Data domains created:")
            for command_name, description, domain in domain_commands:
                self.stdout.write(f"   • {description}")

            try:
                # Try to provide a quick data summary
                self.stdout.write(f"\n📊 Quick data overview:")

                # Demographics
                from apps.demographics.models import (
                    MunicipalityWideReligionPopulation,
                    MunicipalityWideMotherTonguePopulation,
                    MunicipalityWideCastePopulation,
                )

                religion_count = MunicipalityWideReligionPopulation.objects.count()
                language_count = MunicipalityWideMotherTonguePopulation.objects.count()
                caste_count = MunicipalityWideCastePopulation.objects.count()
                self.stdout.write(
                    f"   📈 Demographics: {religion_count + language_count + caste_count} records"
                )

                # Economics
                from apps.economics.models import (
                    WardWiseMajorSkills,
                    WardWiseRemittanceExpenses,
                )

                skills_count = WardWiseMajorSkills.objects.count()
                remittance_count = WardWiseRemittanceExpenses.objects.count()
                self.stdout.write(
                    f"   💰 Economics: {skills_count + remittance_count} records"
                )

                # Infrastructure
                from apps.infrastructure.models import (
                    WardWiseTimeToMarketCenter,
                    WardWiseTimeToPublicTransport,
                    WardWiseRoadStatus,
                )

                market_count = WardWiseTimeToMarketCenter.objects.count()
                transport_count = WardWiseTimeToPublicTransport.objects.count()
                road_count = WardWiseRoadStatus.objects.count()
                self.stdout.write(
                    f"   🏗️  Infrastructure: {market_count + transport_count + road_count} records"
                )

                # Social
                from apps.social.models import (
                    WardWiseLiteracyStatus,
                    WardWiseMajorSubject,
                    WardWiseToiletType,
                )

                literacy_count = WardWiseLiteracyStatus.objects.count()
                subject_count = WardWiseMajorSubject.objects.count()
                toilet_count = WardWiseToiletType.objects.count()
                self.stdout.write(
                    f"   👥 Social: {literacy_count + subject_count + toilet_count} records"
                )

            except Exception as e:
                self.stdout.write(f"   (Could not generate detailed overview: {e})")

        self.stdout.write("\n" + "=" * 80)
        self.stdout.write("💡 Tips:")
        self.stdout.write("   • Use --dry-run to preview what would be executed")
        self.stdout.write("   • Use --clear to fresh start with clean data")
        self.stdout.write(
            "   • Use --skip-errors to continue if individual domains fail"
        )
        self.stdout.write("=" * 80)
