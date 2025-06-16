"""
Management command to create occupation demographics data based on actual data
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db import models
from apps.demographics.models import WardWiseMajorOccupation
import uuid


class Command(BaseCommand):
    help = 'Create occupation demographics data based on actual municipality-wide data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before creating new data',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing occupation data...'))
            WardWiseMajorOccupation.objects.all().delete()

        self.stdout.write('Creating occupation demographics data based on actual municipality-wide data...')

        # Sample data representing actual occupation patterns by ward
        occupation_data = [
            # Ward 1
            {'id': str(uuid.uuid4()), 'ward_number': 1, 'occupation': 'ANIMAL_HUSBANDRY', 'population': 546},
            {'id': str(uuid.uuid4()), 'ward_number': 1, 'occupation': 'BUSINESS', 'population': 49},
            {'id': str(uuid.uuid4()), 'ward_number': 1, 'occupation': 'DAILY_WAGE', 'population': 727},
            {'id': str(uuid.uuid4()), 'ward_number': 1, 'occupation': 'FOREIGN_EMPLOYMENT', 'population': 734},
            {'id': str(uuid.uuid4()), 'ward_number': 1, 'occupation': 'GOVERNMENT_SERVICE', 'population': 99},
            {'id': str(uuid.uuid4()), 'ward_number': 1, 'occupation': 'HOUSEHOLD_WORK', 'population': 202},
            {'id': str(uuid.uuid4()), 'ward_number': 1, 'occupation': 'INDUSTRY', 'population': 22},
            {'id': str(uuid.uuid4()), 'ward_number': 1, 'occupation': 'NON_GOVERNMENT_SERVICE', 'population': 43},
            {'id': str(uuid.uuid4()), 'ward_number': 1, 'occupation': 'OTHER', 'population': 1224},
            {'id': str(uuid.uuid4()), 'ward_number': 1, 'occupation': 'OTHER_SELF_EMPLOYMENT', 'population': 41},
            {'id': str(uuid.uuid4()), 'ward_number': 1, 'occupation': 'OTHER_UNEMPLOYMENT', 'population': 8},
            {'id': str(uuid.uuid4()), 'ward_number': 1, 'occupation': 'STUDENT', 'population': 601},
            
            # Ward 2
            {'id': str(uuid.uuid4()), 'ward_number': 2, 'occupation': 'ANIMAL_HUSBANDRY', 'population': 25},
            {'id': str(uuid.uuid4()), 'ward_number': 2, 'occupation': 'BUSINESS', 'population': 62},
            {'id': str(uuid.uuid4()), 'ward_number': 2, 'occupation': 'DAILY_WAGE', 'population': 564},
            {'id': str(uuid.uuid4()), 'ward_number': 2, 'occupation': 'FOREIGN_EMPLOYMENT', 'population': 461},
            {'id': str(uuid.uuid4()), 'ward_number': 2, 'occupation': 'GOVERNMENT_SERVICE', 'population': 55},
            {'id': str(uuid.uuid4()), 'ward_number': 2, 'occupation': 'HOUSEHOLD_WORK', 'population': 269},
            {'id': str(uuid.uuid4()), 'ward_number': 2, 'occupation': 'INDUSTRY', 'population': 11},
            {'id': str(uuid.uuid4()), 'ward_number': 2, 'occupation': 'NON_GOVERNMENT_SERVICE', 'population': 11},
            {'id': str(uuid.uuid4()), 'ward_number': 2, 'occupation': 'OTHER', 'population': 225},
            {'id': str(uuid.uuid4()), 'ward_number': 2, 'occupation': 'OTHER_SELF_EMPLOYMENT', 'population': 20},
            {'id': str(uuid.uuid4()), 'ward_number': 2, 'occupation': 'OTHER_UNEMPLOYMENT', 'population': 5},
            {'id': str(uuid.uuid4()), 'ward_number': 2, 'occupation': 'STUDENT', 'population': 155},
            
            # Ward 3
            {'id': str(uuid.uuid4()), 'ward_number': 3, 'occupation': 'ANIMAL_HUSBANDRY', 'population': 2},
            {'id': str(uuid.uuid4()), 'ward_number': 3, 'occupation': 'BUSINESS', 'population': 15},
            {'id': str(uuid.uuid4()), 'ward_number': 3, 'occupation': 'DAILY_WAGE', 'population': 135},
            {'id': str(uuid.uuid4()), 'ward_number': 3, 'occupation': 'FOREIGN_EMPLOYMENT', 'population': 277},
            {'id': str(uuid.uuid4()), 'ward_number': 3, 'occupation': 'GOVERNMENT_SERVICE', 'population': 64},
            {'id': str(uuid.uuid4()), 'ward_number': 3, 'occupation': 'HOUSEHOLD_WORK', 'population': 3},
            {'id': str(uuid.uuid4()), 'ward_number': 3, 'occupation': 'INDUSTRY', 'population': 8},
            {'id': str(uuid.uuid4()), 'ward_number': 3, 'occupation': 'NON_GOVERNMENT_SERVICE', 'population': 2},
            {'id': str(uuid.uuid4()), 'ward_number': 3, 'occupation': 'OTHER', 'population': 257},
            {'id': str(uuid.uuid4()), 'ward_number': 3, 'occupation': 'OTHER_SELF_EMPLOYMENT', 'population': 5},
            {'id': str(uuid.uuid4()), 'ward_number': 3, 'occupation': 'STUDENT', 'population': 1},
            
            # Ward 4
            {'id': str(uuid.uuid4()), 'ward_number': 4, 'occupation': 'ANIMAL_HUSBANDRY', 'population': 340},
            {'id': str(uuid.uuid4()), 'ward_number': 4, 'occupation': 'BUSINESS', 'population': 52},
            {'id': str(uuid.uuid4()), 'ward_number': 4, 'occupation': 'DAILY_WAGE', 'population': 257},
            {'id': str(uuid.uuid4()), 'ward_number': 4, 'occupation': 'FOREIGN_EMPLOYMENT', 'population': 341},
            {'id': str(uuid.uuid4()), 'ward_number': 4, 'occupation': 'GOVERNMENT_SERVICE', 'population': 46},
            {'id': str(uuid.uuid4()), 'ward_number': 4, 'occupation': 'HOUSEHOLD_WORK', 'population': 197},
            {'id': str(uuid.uuid4()), 'ward_number': 4, 'occupation': 'INDUSTRY', 'population': 20},
            {'id': str(uuid.uuid4()), 'ward_number': 4, 'occupation': 'NON_GOVERNMENT_SERVICE', 'population': 18},
            {'id': str(uuid.uuid4()), 'ward_number': 4, 'occupation': 'OTHER', 'population': 371},
            {'id': str(uuid.uuid4()), 'ward_number': 4, 'occupation': 'OTHER_SELF_EMPLOYMENT', 'population': 37},
            {'id': str(uuid.uuid4()), 'ward_number': 4, 'occupation': 'OTHER_UNEMPLOYMENT', 'population': 2},
            {'id': str(uuid.uuid4()), 'ward_number': 4, 'occupation': 'STUDENT', 'population': 32},
            
            # Ward 5
            {'id': str(uuid.uuid4()), 'ward_number': 5, 'occupation': 'ANIMAL_HUSBANDRY', 'population': 8},
            {'id': str(uuid.uuid4()), 'ward_number': 5, 'occupation': 'BUSINESS', 'population': 56},
            {'id': str(uuid.uuid4()), 'ward_number': 5, 'occupation': 'DAILY_WAGE', 'population': 168},
            {'id': str(uuid.uuid4()), 'ward_number': 5, 'occupation': 'FOREIGN_EMPLOYMENT', 'population': 280},
            {'id': str(uuid.uuid4()), 'ward_number': 5, 'occupation': 'GOVERNMENT_SERVICE', 'population': 87},
            {'id': str(uuid.uuid4()), 'ward_number': 5, 'occupation': 'HOUSEHOLD_WORK', 'population': 21},
            {'id': str(uuid.uuid4()), 'ward_number': 5, 'occupation': 'INDUSTRY', 'population': 35},
            {'id': str(uuid.uuid4()), 'ward_number': 5, 'occupation': 'NON_GOVERNMENT_SERVICE', 'population': 11},
            {'id': str(uuid.uuid4()), 'ward_number': 5, 'occupation': 'OTHER', 'population': 1318},
            {'id': str(uuid.uuid4()), 'ward_number': 5, 'occupation': 'OTHER_SELF_EMPLOYMENT', 'population': 8},
            {'id': str(uuid.uuid4()), 'ward_number': 5, 'occupation': 'OTHER_UNEMPLOYMENT', 'population': 6},
            {'id': str(uuid.uuid4()), 'ward_number': 5, 'occupation': 'STUDENT', 'population': 26},
            
            # Ward 6
            {'id': str(uuid.uuid4()), 'ward_number': 6, 'occupation': 'ANIMAL_HUSBANDRY', 'population': 25},
            {'id': str(uuid.uuid4()), 'ward_number': 6, 'occupation': 'BUSINESS', 'population': 43},
            {'id': str(uuid.uuid4()), 'ward_number': 6, 'occupation': 'DAILY_WAGE', 'population': 965},
            {'id': str(uuid.uuid4()), 'ward_number': 6, 'occupation': 'FOREIGN_EMPLOYMENT', 'population': 369},
            {'id': str(uuid.uuid4()), 'ward_number': 6, 'occupation': 'GOVERNMENT_SERVICE', 'population': 96},
            {'id': str(uuid.uuid4()), 'ward_number': 6, 'occupation': 'HOUSEHOLD_WORK', 'population': 46},
            {'id': str(uuid.uuid4()), 'ward_number': 6, 'occupation': 'INDUSTRY', 'population': 30},
            {'id': str(uuid.uuid4()), 'ward_number': 6, 'occupation': 'NON_GOVERNMENT_SERVICE', 'population': 22},
            {'id': str(uuid.uuid4()), 'ward_number': 6, 'occupation': 'OTHER', 'population': 627},
            {'id': str(uuid.uuid4()), 'ward_number': 6, 'occupation': 'OTHER_SELF_EMPLOYMENT', 'population': 9},
            {'id': str(uuid.uuid4()), 'ward_number': 6, 'occupation': 'OTHER_UNEMPLOYMENT', 'population': 4},
            {'id': str(uuid.uuid4()), 'ward_number': 6, 'occupation': 'STUDENT', 'population': 56},
            
            # Ward 7
            {'id': str(uuid.uuid4()), 'ward_number': 7, 'occupation': 'ANIMAL_HUSBANDRY', 'population': 54},
            {'id': str(uuid.uuid4()), 'ward_number': 7, 'occupation': 'BUSINESS', 'population': 27},
            {'id': str(uuid.uuid4()), 'ward_number': 7, 'occupation': 'DAILY_WAGE', 'population': 273},
            {'id': str(uuid.uuid4()), 'ward_number': 7, 'occupation': 'FOREIGN_EMPLOYMENT', 'population': 196},
            {'id': str(uuid.uuid4()), 'ward_number': 7, 'occupation': 'GOVERNMENT_SERVICE', 'population': 27},
            {'id': str(uuid.uuid4()), 'ward_number': 7, 'occupation': 'INDUSTRY', 'population': 392},
            {'id': str(uuid.uuid4()), 'ward_number': 7, 'occupation': 'NON_GOVERNMENT_SERVICE', 'population': 4},
            {'id': str(uuid.uuid4()), 'ward_number': 7, 'occupation': 'OTHER', 'population': 522},
            {'id': str(uuid.uuid4()), 'ward_number': 7, 'occupation': 'OTHER_SELF_EMPLOYMENT', 'population': 21},
            {'id': str(uuid.uuid4()), 'ward_number': 7, 'occupation': 'OTHER_UNEMPLOYMENT', 'population': 8},
            {'id': str(uuid.uuid4()), 'ward_number': 7, 'occupation': 'STUDENT', 'population': 2},
        ]

        existing_count = WardWiseMajorOccupation.objects.count()
        if existing_count > 0 and not options['clear']:
            self.stdout.write(
                self.style.WARNING(
                    f'Found {existing_count} existing records. Use --clear to replace them.'
                )
            )
            return

        created_count = 0
        with transaction.atomic():
            for data in occupation_data:
                obj, created = WardWiseMajorOccupation.objects.get_or_create(
                    ward_number=data['ward_number'],
                    occupation=data['occupation'],
                    defaults={
                        'id': data['id'],
                        'population': data['population'],
                    }
                )

                if created:
                    created_count += 1
                    self.stdout.write(
                        f"Created: Ward {data['ward_number']} - {data['occupation']} ({data['population']} people)"
                    )
                else:
                    obj.population = data['population']
                    obj.save()
                    self.stdout.write(
                        f"Updated: Ward {data['ward_number']} - {data['occupation']} ({data['population']} people)"
                    )

        total_records = WardWiseMajorOccupation.objects.count()
        total_population = sum(WardWiseMajorOccupation.objects.values_list('population', flat=True))

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully processed {len(occupation_data)} occupation demographic records '
                f'({created_count} new, {len(occupation_data) - created_count} updated)\n'
                f'Total records in database: {total_records}\n'
                f'Total population covered: {total_population:,} people'
            )
        )

        # Calculate and display occupation-wise summary
        self.stdout.write('\nOccupation-wise summary:')
        occupation_totals = {}
        for occupation in ['ANIMAL_HUSBANDRY', 'BUSINESS', 'DAILY_WAGE', 'FOREIGN_EMPLOYMENT', 
                          'GOVERNMENT_SERVICE', 'HOUSEHOLD_WORK', 'INDUSTRY', 'NON_GOVERNMENT_SERVICE',
                          'OTHER', 'OTHER_SELF_EMPLOYMENT', 'OTHER_UNEMPLOYMENT', 'STUDENT']:
            occupation_population = WardWiseMajorOccupation.objects.filter(occupation=occupation).aggregate(
                total=models.Sum('population')
            )['total'] or 0
            occupation_totals[occupation] = occupation_population
            
            if occupation_population > 0:
                percentage = occupation_population / total_population * 100
                self.stdout.write(
                    f'  {occupation}: {occupation_population:,} people ({percentage:.2f}%)'
                )

        # Ward-wise summary
        self.stdout.write('\nWard-wise occupation summary:')
        for ward_num in range(1, 8):  # Wards 1-7 based on data
            ward_population = WardWiseMajorOccupation.objects.filter(ward_number=ward_num).aggregate(
                total=models.Sum('population')
            )['total'] or 0
            if ward_population > 0:
                self.stdout.write(f'  वडा {ward_num}: {ward_population:,} people')
