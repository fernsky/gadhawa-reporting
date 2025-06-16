"""
Management command to create religion demographics data based on actual data
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db import models
from django.utils import timezone
from apps.demographics.models import MunicipalityWideReligionPopulation, ReligionTypeChoice
import uuid


class Command(BaseCommand):
    help = 'Create religion demographics data based on actual municipality-wide data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before creating new data',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing religion data...'))
            MunicipalityWideReligionPopulation.objects.all().delete()

        self.stdout.write('Creating religion demographics data based on actual municipality-wide data...')

        # Aggregate the ward data to municipality level
        # Based on the original ward data, calculate totals
        religion_data = [
            {'id': '6897a374-5f1b-4905-8123-03bc1418094c', 'religion': 'CHRISTIAN', 'population': 121},  
            {'id': 'ae1c5381-18fe-4a52-a042-f66b94af0b8d', 'religion': 'HINDU', 'population': 26713},   
            {'id': '97027b07-fda1-4368-a604-b5a9a0a46b2a', 'religion': 'NATURE', 'population': 61},     
            {'id': '5864c7c9-3409-43e4-8c37-de5195f3c96b', 'religion': 'BUDDHIST', 'population': 535},  
        ]

        # Check if data already exists
        existing_count = MunicipalityWideReligionPopulation.objects.count()
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
                obj, created = MunicipalityWideReligionPopulation.objects.get_or_create(
                    religion=data['religion'],
                    defaults={
                        'id': data['id'],
                        'population': data['population'],
                    }
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(
                        f"Created: {data['religion']} ({data['population']} people)"
                    )
                else:
                    # Update existing record
                    obj.population = data['population']
                    obj.save()
                    self.stdout.write(
                        f"Updated: {data['religion']} ({data['population']} people)"
                    )

        # Print summary
        total_records = MunicipalityWideReligionPopulation.objects.count()
        total_population = sum(MunicipalityWideReligionPopulation.objects.values_list('population', flat=True))
        
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
            try:
                religion_obj = MunicipalityWideReligionPopulation.objects.get(religion=religion_code)
                religion_pop = religion_obj.population
                percentage = religion_pop / total_population * 100
                self.stdout.write(
                    f'  {religion_name}: {religion_pop:,} ({percentage:.2f}%)'
                )
            except MunicipalityWideReligionPopulation.DoesNotExist:
                self.stdout.write(
                    f'  {religion_name}: 0 (0.00%)'
                )
