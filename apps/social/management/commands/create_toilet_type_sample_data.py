"""
Management command to create toilet type social data based on actual data
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db import models
from apps.social.models import WardWiseToiletType, ToiletTypeChoice
import uuid


class Command(BaseCommand):
    help = 'Create toilet type social data based on actual municipality-wide data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before creating new data',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing toilet type data...'))
            WardWiseToiletType.objects.all().delete()

        self.stdout.write('Creating toilet type social data based on actual municipality-wide data...')

        # Sample data representing actual toilet type patterns by ward
        toilet_type_data = [
            # Ward 1
            {'id': str(uuid.uuid4()), 'ward_number': 1, 'toilet_type': 'FLUSH_WITH_SEPTIC_TANK', 'households': 15},
            {'id': str(uuid.uuid4()), 'ward_number': 1, 'toilet_type': 'NORMAL', 'households': 1101},
            {'id': str(uuid.uuid4()), 'ward_number': 1, 'toilet_type': 'NO_TOILET', 'households': 23},
            
            # Ward 2
            {'id': str(uuid.uuid4()), 'ward_number': 2, 'toilet_type': 'FLUSH_WITH_SEPTIC_TANK', 'households': 5},
            {'id': str(uuid.uuid4()), 'ward_number': 2, 'toilet_type': 'NORMAL', 'households': 870},
            {'id': str(uuid.uuid4()), 'ward_number': 2, 'toilet_type': 'NO_TOILET', 'households': 39},
            {'id': str(uuid.uuid4()), 'ward_number': 2, 'toilet_type': 'PUBLIC_EILANI', 'households': 4},
            
            # Ward 3
            {'id': str(uuid.uuid4()), 'ward_number': 3, 'toilet_type': 'NORMAL', 'households': 550},
            {'id': str(uuid.uuid4()), 'ward_number': 3, 'toilet_type': 'NO_TOILET', 'households': 9},
            {'id': str(uuid.uuid4()), 'ward_number': 3, 'toilet_type': 'PUBLIC_EILANI', 'households': 5},
            
            # Ward 4
            {'id': str(uuid.uuid4()), 'ward_number': 4, 'toilet_type': 'FLUSH_WITH_SEPTIC_TANK', 'households': 26},
            {'id': str(uuid.uuid4()), 'ward_number': 4, 'toilet_type': 'NORMAL', 'households': 785},
            {'id': str(uuid.uuid4()), 'ward_number': 4, 'toilet_type': 'NO_TOILET', 'households': 28},
            {'id': str(uuid.uuid4()), 'ward_number': 4, 'toilet_type': 'PUBLIC_EILANI', 'households': 9},
            
            # Ward 5
            {'id': str(uuid.uuid4()), 'ward_number': 5, 'toilet_type': 'FLUSH_WITH_SEPTIC_TANK', 'households': 28},
            {'id': str(uuid.uuid4()), 'ward_number': 5, 'toilet_type': 'NORMAL', 'households': 670},
            {'id': str(uuid.uuid4()), 'ward_number': 5, 'toilet_type': 'NO_TOILET', 'households': 18},
            {'id': str(uuid.uuid4()), 'ward_number': 5, 'toilet_type': 'PUBLIC_EILANI', 'households': 3},
            
            # Ward 6
            {'id': str(uuid.uuid4()), 'ward_number': 6, 'toilet_type': 'FLUSH_WITH_SEPTIC_TANK', 'households': 3},
            {'id': str(uuid.uuid4()), 'ward_number': 6, 'toilet_type': 'NORMAL', 'households': 809},
            {'id': str(uuid.uuid4()), 'ward_number': 6, 'toilet_type': 'NO_TOILET', 'households': 49},
            {'id': str(uuid.uuid4()), 'ward_number': 6, 'toilet_type': 'PUBLIC_EILANI', 'households': 3},
            
            # Ward 7
            {'id': str(uuid.uuid4()), 'ward_number': 7, 'toilet_type': 'FLUSH_WITH_SEPTIC_TANK', 'households': 18},
            {'id': str(uuid.uuid4()), 'ward_number': 7, 'toilet_type': 'NORMAL', 'households': 470},
            {'id': str(uuid.uuid4()), 'ward_number': 7, 'toilet_type': 'NO_TOILET', 'households': 96},
            {'id': str(uuid.uuid4()), 'ward_number': 7, 'toilet_type': 'PUBLIC_EILANI', 'households': 3},
        ]

        # Check if data already exists
        existing_count = WardWiseToiletType.objects.count()
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
            for data in toilet_type_data:
                obj, created = WardWiseToiletType.objects.get_or_create(
                    ward_number=data['ward_number'],
                    toilet_type=data['toilet_type'],
                    defaults={
                        'id': data['id'],
                        'households': data['households'],
                    }
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(
                        f"Created: Ward {data['ward_number']} - {data['toilet_type']} ({data['households']} households)"
                    )
                else:
                    # Update existing record
                    obj.households = data['households']
                    obj.save()
                    self.stdout.write(
                        f"Updated: Ward {data['ward_number']} - {data['toilet_type']} ({data['households']} households)"
                    )

        # Print summary
        total_records = WardWiseToiletType.objects.count()
        total_households = sum(WardWiseToiletType.objects.values_list('households', flat=True))
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully processed {len(toilet_type_data)} toilet type social records '
                f'({created_count} new, {len(toilet_type_data) - created_count} updated)\n'
                f'Total records in database: {total_records}\n'
                f'Total households covered: {total_households:,} households'
            )
        )

        # Print toilet type breakdown
        self.stdout.write('\nToilet type breakdown:')
        for toilet_choice in ToiletTypeChoice.choices:
            toilet_code = toilet_choice[0]
            toilet_name = toilet_choice[1]
            toilet_households = WardWiseToiletType.objects.filter(toilet_type=toilet_code).aggregate(
                total=models.Sum('households')
            )['total'] or 0
            
            if toilet_households > 0:
                percentage = toilet_households / total_households * 100
                self.stdout.write(
                    f'  {toilet_name}: {toilet_households:,} households ({percentage:.2f}%)'
                )
            else:
                self.stdout.write(
                    f'  {toilet_name}: 0 households (0.00%)'
                )

        # Ward-wise summary
        self.stdout.write('\nWard-wise toilet summary:')
        for ward_num in range(1, 8):
            ward_households = WardWiseToiletType.objects.filter(ward_number=ward_num).aggregate(
                total=models.Sum('households')
            )['total'] or 0
            if ward_households > 0:
                self.stdout.write(f'  वडा {ward_num}: {ward_households:,} households')
