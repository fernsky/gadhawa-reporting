"""
Management command to create market center time infrastructure data based on actual data
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db import models
from apps.infrastructure.models import WardWiseTimeToMarketCenter, TimeDurationChoice
import uuid


class Command(BaseCommand):
    help = 'Create market center time infrastructure data based on actual municipality-wide data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before creating new data',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing market center time data...'))
            WardWiseTimeToMarketCenter.objects.all().delete()

        self.stdout.write('Creating market center time infrastructure data based on actual municipality-wide data...')

        # Sample data representing actual market center accessibility patterns by ward
        market_center_time_data = [
            # Ward 1
            {'id': str(uuid.uuid4()), 'ward_number': 1, 'time_duration': '1_HOUR_OR_MORE', 'households': 808},
            {'id': str(uuid.uuid4()), 'ward_number': 1, 'time_duration': 'UNDER_15_MIN', 'households': 189},
            {'id': str(uuid.uuid4()), 'ward_number': 1, 'time_duration': 'UNDER_1_HOUR', 'households': 34},
            {'id': str(uuid.uuid4()), 'ward_number': 1, 'time_duration': 'UNDER_30_MIN', 'households': 13},
            
            # Ward 2
            {'id': str(uuid.uuid4()), 'ward_number': 2, 'time_duration': '1_HOUR_OR_MORE', 'households': 16},
            {'id': str(uuid.uuid4()), 'ward_number': 2, 'time_duration': 'UNDER_15_MIN', 'households': 517},
            {'id': str(uuid.uuid4()), 'ward_number': 2, 'time_duration': 'UNDER_1_HOUR', 'households': 260},
            {'id': str(uuid.uuid4()), 'ward_number': 2, 'time_duration': 'UNDER_30_MIN', 'households': 145},
            
            # Ward 3
            {'id': str(uuid.uuid4()), 'ward_number': 3, 'time_duration': '1_HOUR_OR_MORE', 'households': 569},
            {'id': str(uuid.uuid4()), 'ward_number': 3, 'time_duration': 'UNDER_15_MIN', 'households': 7},
            {'id': str(uuid.uuid4()), 'ward_number': 3, 'time_duration': 'UNDER_1_HOUR', 'households': 58},
            {'id': str(uuid.uuid4()), 'ward_number': 3, 'time_duration': 'UNDER_30_MIN', 'households': 5},
            
            # Ward 4
            {'id': str(uuid.uuid4()), 'ward_number': 4, 'time_duration': '1_HOUR_OR_MORE', 'households': 68},
            {'id': str(uuid.uuid4()), 'ward_number': 4, 'time_duration': 'UNDER_15_MIN', 'households': 273},
            {'id': str(uuid.uuid4()), 'ward_number': 4, 'time_duration': 'UNDER_1_HOUR', 'households': 448},
            {'id': str(uuid.uuid4()), 'ward_number': 4, 'time_duration': 'UNDER_30_MIN', 'households': 59},
            
            # Ward 5
            {'id': str(uuid.uuid4()), 'ward_number': 5, 'time_duration': '1_HOUR_OR_MORE', 'households': 117},
            {'id': str(uuid.uuid4()), 'ward_number': 5, 'time_duration': 'UNDER_15_MIN', 'households': 205},
            {'id': str(uuid.uuid4()), 'ward_number': 5, 'time_duration': 'UNDER_1_HOUR', 'households': 212},
            {'id': str(uuid.uuid4()), 'ward_number': 5, 'time_duration': 'UNDER_30_MIN', 'households': 185},
            
            # Ward 6
            {'id': str(uuid.uuid4()), 'ward_number': 6, 'time_duration': '1_HOUR_OR_MORE', 'households': 18},
            {'id': str(uuid.uuid4()), 'ward_number': 6, 'time_duration': 'UNDER_15_MIN', 'households': 528},
            {'id': str(uuid.uuid4()), 'ward_number': 6, 'time_duration': 'UNDER_1_HOUR', 'households': 158},
            {'id': str(uuid.uuid4()), 'ward_number': 6, 'time_duration': 'UNDER_30_MIN', 'households': 160},
            
            # Ward 7
            {'id': str(uuid.uuid4()), 'ward_number': 7, 'time_duration': '1_HOUR_OR_MORE', 'households': 390},
            {'id': str(uuid.uuid4()), 'ward_number': 7, 'time_duration': 'UNDER_15_MIN', 'households': 138},
            {'id': str(uuid.uuid4()), 'ward_number': 7, 'time_duration': 'UNDER_1_HOUR', 'households': 47},
            {'id': str(uuid.uuid4()), 'ward_number': 7, 'time_duration': 'UNDER_30_MIN', 'households': 12},
        ]

        # Check if data already exists
        existing_count = WardWiseTimeToMarketCenter.objects.count()
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
            for data in market_center_time_data:
                obj, created = WardWiseTimeToMarketCenter.objects.get_or_create(
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
        total_records = WardWiseTimeToMarketCenter.objects.count()
        total_households = sum(WardWiseTimeToMarketCenter.objects.values_list('households', flat=True))
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully processed {len(market_center_time_data)} market center time infrastructure records '
                f'({created_count} new, {len(market_center_time_data) - created_count} updated)\n'
                f'Total records in database: {total_records}\n'
                f'Total households covered: {total_households:,} households'
            )
        )

        # Print time duration breakdown
        self.stdout.write('\nMarket center access time breakdown:')
        for time_choice in TimeDurationChoice.choices:
            time_code = time_choice[0]
            time_name = time_choice[1]
            time_households = WardWiseTimeToMarketCenter.objects.filter(time_duration=time_code).aggregate(
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

        # Accessibility analysis
        self.stdout.write('\nAccessibility Analysis:')
        excellent_access = WardWiseTimeToMarketCenter.objects.filter(time_duration='UNDER_15_MIN').aggregate(
            total=models.Sum('households')
        )['total'] or 0
        good_access = WardWiseTimeToMarketCenter.objects.filter(time_duration='UNDER_30_MIN').aggregate(
            total=models.Sum('households')
        )['total'] or 0
        
        good_accessibility = excellent_access + good_access
        good_percentage = (good_accessibility / total_households * 100) if total_households > 0 else 0
        
        self.stdout.write(f'  Excellent Access (< 15 min): {excellent_access:,} households')
        self.stdout.write(f'  Good Access (< 30 min total): {good_accessibility:,} households ({good_percentage:.1f}%)')

        # Ward-wise summary
        self.stdout.write('\nWard-wise market center accessibility summary:')
        for ward_num in range(1, 8):
            ward_households = WardWiseTimeToMarketCenter.objects.filter(ward_number=ward_num).aggregate(
                total=models.Sum('households')
            )['total'] or 0
            if ward_households > 0:
                self.stdout.write(f'  वडा {ward_num}: {ward_households:,} households')
