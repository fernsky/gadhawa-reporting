"""
Management command to create public transport accessibility data based on actual data
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db import models
from apps.infrastructure.models import WardWiseTimeToPublicTransport, TimeDurationChoice
import uuid


class Command(BaseCommand):
    help = 'Create public transport accessibility data based on actual municipality-wide data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before creating new data',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing public transport data...'))
            WardWiseTimeToPublicTransport.objects.all().delete()

        self.stdout.write('Creating public transport accessibility data based on actual municipality-wide data...')

        # Sample data representing actual public transport accessibility patterns by ward and time duration
        public_transport_data = [
            # Ward 1
            {'id': str(uuid.uuid4()), 'ward_number': 1, 'time_duration': '1_HOUR_OR_MORE', 'households': 258},
            {'id': str(uuid.uuid4()), 'ward_number': 1, 'time_duration': 'UNDER_15_MIN', 'households': 533},
            {'id': str(uuid.uuid4()), 'ward_number': 1, 'time_duration': 'UNDER_1_HOUR', 'households': 51},
            {'id': str(uuid.uuid4()), 'ward_number': 1, 'time_duration': 'UNDER_30_MIN', 'households': 202},
            
            # Ward 2
            {'id': str(uuid.uuid4()), 'ward_number': 2, 'time_duration': 'UNDER_15_MIN', 'households': 694},
            {'id': str(uuid.uuid4()), 'ward_number': 2, 'time_duration': 'UNDER_1_HOUR', 'households': 65},
            {'id': str(uuid.uuid4()), 'ward_number': 2, 'time_duration': 'UNDER_30_MIN', 'households': 179},
            
            # Ward 3
            {'id': str(uuid.uuid4()), 'ward_number': 3, 'time_duration': '1_HOUR_OR_MORE', 'households': 195},
            {'id': str(uuid.uuid4()), 'ward_number': 3, 'time_duration': 'UNDER_15_MIN', 'households': 297},
            {'id': str(uuid.uuid4()), 'ward_number': 3, 'time_duration': 'UNDER_1_HOUR', 'households': 32},
            {'id': str(uuid.uuid4()), 'ward_number': 3, 'time_duration': 'UNDER_30_MIN', 'households': 115},
            
            # Ward 4
            {'id': str(uuid.uuid4()), 'ward_number': 4, 'time_duration': '1_HOUR_OR_MORE', 'households': 6},
            {'id': str(uuid.uuid4()), 'ward_number': 4, 'time_duration': 'UNDER_15_MIN', 'households': 530},
            {'id': str(uuid.uuid4()), 'ward_number': 4, 'time_duration': 'UNDER_1_HOUR', 'households': 188},
            {'id': str(uuid.uuid4()), 'ward_number': 4, 'time_duration': 'UNDER_30_MIN', 'households': 124},
            
            # Ward 5
            {'id': str(uuid.uuid4()), 'ward_number': 5, 'time_duration': '1_HOUR_OR_MORE', 'households': 76},
            {'id': str(uuid.uuid4()), 'ward_number': 5, 'time_duration': 'UNDER_15_MIN', 'households': 300},
            {'id': str(uuid.uuid4()), 'ward_number': 5, 'time_duration': 'UNDER_1_HOUR', 'households': 215},
            {'id': str(uuid.uuid4()), 'ward_number': 5, 'time_duration': 'UNDER_30_MIN', 'households': 128},
            
            # Ward 6
            {'id': str(uuid.uuid4()), 'ward_number': 6, 'time_duration': '1_HOUR_OR_MORE', 'households': 29},
            {'id': str(uuid.uuid4()), 'ward_number': 6, 'time_duration': 'UNDER_15_MIN', 'households': 341},
            {'id': str(uuid.uuid4()), 'ward_number': 6, 'time_duration': 'UNDER_1_HOUR', 'households': 324},
            {'id': str(uuid.uuid4()), 'ward_number': 6, 'time_duration': 'UNDER_30_MIN', 'households': 170},
            
            # Ward 7
            {'id': str(uuid.uuid4()), 'ward_number': 7, 'time_duration': '1_HOUR_OR_MORE', 'households': 177},
            {'id': str(uuid.uuid4()), 'ward_number': 7, 'time_duration': 'UNDER_15_MIN', 'households': 175},
            {'id': str(uuid.uuid4()), 'ward_number': 7, 'time_duration': 'UNDER_1_HOUR', 'households': 58},
            {'id': str(uuid.uuid4()), 'ward_number': 7, 'time_duration': 'UNDER_30_MIN', 'households': 177},
        ]

        # Check if data already exists
        existing_count = WardWiseTimeToPublicTransport.objects.count()
        if existing_count > 0 and not options['clear']:
            self.stdout.write(
                self.style.WARNING(
                    f'Found {existing_count} existing records. Use --clear to replace them.'
                )
            )
            return

        # Create records using Django ORM
        created_count = 0
        with transaction.atomic():
            for data in public_transport_data:
                obj, created = WardWiseTimeToPublicTransport.objects.get_or_create(
                    ward_number=data['ward_number'],
                    time_duration=data['time_duration'],
                    defaults={
                        'id': data['id'],
                        'households': data['households'],
                    }
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(
                        f"Created: Ward {data['ward_number']} - {data['time_duration']} ({data['households']} households)"
                    )
                else:
                    # Update existing record
                    obj.households = data['households']
                    obj.save()
                    self.stdout.write(
                        f"Updated: Ward {data['ward_number']} - {data['time_duration']} ({data['households']} households)"
                    )

        # Print summary
        total_records = WardWiseTimeToPublicTransport.objects.count()
        total_households = sum(WardWiseTimeToPublicTransport.objects.values_list('households', flat=True))
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully processed {len(public_transport_data)} public transport accessibility records '
                f'({created_count} new, {len(public_transport_data) - created_count} updated)\n'
                f'Total records in database: {total_records}\n'
                f'Total households covered: {total_households:,} households'
            )
        )

        # Print time duration breakdown
        self.stdout.write('\nTime duration breakdown:')
        for time_choice in TimeDurationChoice.choices:
            time_code = time_choice[0]
            time_name = time_choice[1]
            time_households = WardWiseTimeToPublicTransport.objects.filter(time_duration=time_code).aggregate(
                total=models.Sum('households')
            )['total'] or 0
            
            if time_households > 0:
                percentage = time_households / total_households * 100
                self.stdout.write(
                    f'  {time_name}: {time_households:,} households ({percentage:.2f}%)'
                )
            else:
                self.stdout.write(
                    f'  {time_name}: 0 households (0.00%)'
                )

        # Ward-wise summary
        self.stdout.write('\nWard-wise public transport accessibility summary:')
        for ward_num in range(1, 8):
            ward_households = WardWiseTimeToPublicTransport.objects.filter(ward_number=ward_num).aggregate(
                total=models.Sum('households')
            )['total'] or 0
            if ward_households > 0:
                self.stdout.write(f'  वडा {ward_num}: {ward_households:,} households')

        # Accessibility analysis
        excellent_access = WardWiseTimeToPublicTransport.objects.filter(time_duration='UNDER_15_MIN').aggregate(
            total=models.Sum('households')
        )['total'] or 0
        good_access = WardWiseTimeToPublicTransport.objects.filter(time_duration='UNDER_30_MIN').aggregate(
            total=models.Sum('households')
        )['total'] or 0
        poor_access = WardWiseTimeToPublicTransport.objects.filter(time_duration='1_HOUR_OR_MORE').aggregate(
            total=models.Sum('households')
        )['total'] or 0

        combined_good_access = excellent_access + good_access
        good_access_percentage = (combined_good_access / total_households * 100) if total_households > 0 else 0
        poor_access_percentage = (poor_access / total_households * 100) if total_households > 0 else 0

        self.stdout.write('\nAccessibility Analysis:')
        self.stdout.write(f'  Excellent access (under 15 min): {excellent_access:,} households')
        self.stdout.write(f'  Good access (under 30 min total): {combined_good_access:,} households ({good_access_percentage:.1f}%)')
        self.stdout.write(f'  Poor access (1 hour or more): {poor_access:,} households ({poor_access_percentage:.1f}%)')
        
        if good_access_percentage >= 60:
            self.stdout.write(self.style.SUCCESS('  ✓ Good overall accessibility'))
        else:
            self.stdout.write(self.style.WARNING('  ⚠ Accessibility improvements needed'))
