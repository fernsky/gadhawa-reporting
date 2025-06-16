"""
Management command to create religion demographics data based on actual data
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db import models
from django.utils import timezone
from apps.demographics.models import WardWiseReligionPopulation, ReligionTypeChoice
import uuid


class Command(BaseCommand):
    help = 'Create religion demographics data based on actual ward data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before creating new data',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing religion data...'))
            WardWiseReligionPopulation.objects.all().delete()

        self.stdout.write('Creating religion demographics data based on actual ward data...')

        # Actual data from the SQL script
        religion_data = [
            # Ward 1
            {'id': '6897a374-5f1b-4905-8123-03bc1418094c', 'ward_number': 1, 'religion_type': 'CHRISTIAN', 'population': 35},
            {'id': 'ae1c5381-18fe-4a52-a042-f66b94af0b8d', 'ward_number': 1, 'religion_type': 'HINDU', 'population': 5533},
            {'id': '97027b07-fda1-4368-a604-b5a9a0a46b2a', 'ward_number': 1, 'religion_type': 'NATURE', 'population': 35},
            
            # Ward 2
            {'id': '759bd991-9972-4cc9-b772-9a4129b44ce7', 'ward_number': 2, 'religion_type': 'HINDU', 'population': 4265},
            
            # Ward 3
            {'id': '5864c7c9-3409-43e4-8c37-de5195f3c96b', 'ward_number': 3, 'religion_type': 'BUDDHIST', 'population': 12},
            {'id': 'f9dfd9c6-e63c-42f0-b042-627c81856ea8', 'ward_number': 3, 'religion_type': 'CHRISTIAN', 'population': 46},
            {'id': 'ca3f4b09-4664-4ac3-909f-a400e861aac6', 'ward_number': 3, 'religion_type': 'HINDU', 'population': 2980},
            
            # Ward 4
            {'id': '1c7f925e-62a0-4c1a-b0ba-48564559bd2a', 'ward_number': 4, 'religion_type': 'HINDU', 'population': 4050},
            {'id': 'a7cf5699-d008-462e-b6f3-7927f830be4d', 'ward_number': 4, 'religion_type': 'NATURE', 'population': 9},
            
            # Ward 5
            {'id': '987211ef-5fca-48fe-a7be-5e7d0e781166', 'ward_number': 5, 'religion_type': 'HINDU', 'population': 3406},
            
            # Ward 6
            {'id': '0902f424-4c18-463b-aece-34e8afbf67c9', 'ward_number': 6, 'religion_type': 'BUDDHIST', 'population': 20},
            {'id': 'efad71e2-0cc2-442d-9399-60fe9e142aee', 'ward_number': 6, 'religion_type': 'HINDU', 'population': 4491},
            
            # Ward 7
            {'id': '60648b4c-d704-4e06-8516-4272052e6659', 'ward_number': 7, 'religion_type': 'BUDDHIST', 'population': 45},
            {'id': '4eb1000b-26b1-4d2d-8de7-1cb1246ae496', 'ward_number': 7, 'religion_type': 'CHRISTIAN', 'population': 40},
            {'id': '4fe51fd6-da20-422b-a0d6-e13b6d9f0db8', 'ward_number': 7, 'religion_type': 'HINDU', 'population': 2506},
            {'id': 'c89be2a3-0995-4d5a-86a0-b36a3fdedf7d', 'ward_number': 7, 'religion_type': 'NATURE', 'population': 22},
        ]

        # Check if data already exists
        existing_count = WardWiseReligionPopulation.objects.count()
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
            for data in religion_data:
                # Create the record with the specified ID
                obj, created = WardWiseReligionPopulation.objects.get_or_create(
                    ward_number=data['ward_number'],
                    religion_type=data['religion_type'],
                    defaults={
                        'id': data['id'],
                        'population': data['population'],
                    }
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(
                        f"Created: Ward {data['ward_number']} - {data['religion_type']} ({data['population']} people)"
                    )
                else:
                    # Update existing record
                    obj.population = data['population']
                    obj.save()
                    self.stdout.write(
                        f"Updated: Ward {data['ward_number']} - {data['religion_type']} ({data['population']} people)"
                    )

        # Print summary
        total_records = WardWiseReligionPopulation.objects.count()
        total_population = sum(WardWiseReligionPopulation.objects.values_list('population', flat=True))
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully processed {len(religion_data)} religion demographic records '
                f'({created_count} new, {len(religion_data) - created_count} updated)\n'
                f'Total records in database: {total_records}\n'
                f'Total population covered: {total_population:,} people'
            )
        )

        # Print religion breakdown
        self.stdout.write('\nReligion breakdown:')
        for religion_choice in ReligionTypeChoice.choices:
            religion_code = religion_choice[0]
            religion_name = religion_choice[1]
            religion_pop = WardWiseReligionPopulation.objects.filter(
                religion_type=religion_code
            ).aggregate(total=models.Sum('population'))['total'] or 0
            
            if religion_pop > 0:
                percentage = religion_pop / total_population * 100
                ward_count = WardWiseReligionPopulation.objects.filter(
                    religion_type=religion_code
                ).count()
                self.stdout.write(
                    f'  {religion_name}: {religion_pop:,} ({percentage:.2f}%) in {ward_count} wards'
                )

        # Print ward breakdown
        self.stdout.write('\nWard breakdown:')
        for ward_num in sorted(set(data['ward_number'] for data in religion_data)):
            ward_pop = WardWiseReligionPopulation.objects.filter(
                ward_number=ward_num
            ).aggregate(total=models.Sum('population'))['total'] or 0
            religion_count = WardWiseReligionPopulation.objects.filter(
                ward_number=ward_num
            ).count()
            self.stdout.write(
                f'  Ward {ward_num}: {ward_pop:,} people across {religion_count} religions'
            )
