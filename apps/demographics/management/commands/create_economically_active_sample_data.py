"""
Management command to create economically active population demographics data based on actual data
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db import models
from apps.demographics.models import WardAgeWiseEconomicallyActivePopulation, EconomicallyActiveAgeGroupChoice, GenderChoice
import uuid


class Command(BaseCommand):
    help = 'Create economically active population demographics data based on actual municipality-wide data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before creating new data',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing economically active population data...'))
            WardAgeWiseEconomicallyActivePopulation.objects.all().delete()

        self.stdout.write('Creating economically active population demographics data based on actual municipality-wide data...')

        # Sample data representing actual economically active population patterns by ward, age, and gender
        economically_active_data = [
            # Ward 1
            {'id': str(uuid.uuid4()), 'ward_number': 1, 'age_group': 'AGE_0_TO_14', 'gender': 'FEMALE', 'population': 1049},
            {'id': str(uuid.uuid4()), 'ward_number': 1, 'age_group': 'AGE_0_TO_14', 'gender': 'MALE', 'population': 582},
            {'id': str(uuid.uuid4()), 'ward_number': 1, 'age_group': 'AGE_15_TO_59', 'gender': 'FEMALE', 'population': 1633},
            {'id': str(uuid.uuid4()), 'ward_number': 1, 'age_group': 'AGE_15_TO_59', 'gender': 'MALE', 'population': 1717},
            {'id': str(uuid.uuid4()), 'ward_number': 1, 'age_group': 'AGE_60_PLUS', 'gender': 'FEMALE', 'population': 229},
            {'id': str(uuid.uuid4()), 'ward_number': 1, 'age_group': 'AGE_60_PLUS', 'gender': 'MALE', 'population': 393},
            
            # Ward 2
            {'id': str(uuid.uuid4()), 'ward_number': 2, 'age_group': 'AGE_0_TO_14', 'gender': 'FEMALE', 'population': 666},
            {'id': str(uuid.uuid4()), 'ward_number': 2, 'age_group': 'AGE_0_TO_14', 'gender': 'MALE', 'population': 636},
            {'id': str(uuid.uuid4()), 'ward_number': 2, 'age_group': 'AGE_15_TO_59', 'gender': 'FEMALE', 'population': 1331},
            {'id': str(uuid.uuid4()), 'ward_number': 2, 'age_group': 'AGE_15_TO_59', 'gender': 'MALE', 'population': 1234},
            {'id': str(uuid.uuid4()), 'ward_number': 2, 'age_group': 'AGE_60_PLUS', 'gender': 'FEMALE', 'population': 230},
            {'id': str(uuid.uuid4()), 'ward_number': 2, 'age_group': 'AGE_60_PLUS', 'gender': 'MALE', 'population': 168},
            
            # Ward 3
            {'id': str(uuid.uuid4()), 'ward_number': 3, 'age_group': 'AGE_0_TO_14', 'gender': 'FEMALE', 'population': 537},
            {'id': str(uuid.uuid4()), 'ward_number': 3, 'age_group': 'AGE_0_TO_14', 'gender': 'MALE', 'population': 481},
            {'id': str(uuid.uuid4()), 'ward_number': 3, 'age_group': 'AGE_15_TO_59', 'gender': 'FEMALE', 'population': 955},
            {'id': str(uuid.uuid4()), 'ward_number': 3, 'age_group': 'AGE_15_TO_59', 'gender': 'MALE', 'population': 844},
            {'id': str(uuid.uuid4()), 'ward_number': 3, 'age_group': 'AGE_60_PLUS', 'gender': 'FEMALE', 'population': 117},
            {'id': str(uuid.uuid4()), 'ward_number': 3, 'age_group': 'AGE_60_PLUS', 'gender': 'MALE', 'population': 104},
            
            # Ward 4
            {'id': str(uuid.uuid4()), 'ward_number': 4, 'age_group': 'AGE_0_TO_14', 'gender': 'FEMALE', 'population': 661},
            {'id': str(uuid.uuid4()), 'ward_number': 4, 'age_group': 'AGE_0_TO_14', 'gender': 'MALE', 'population': 552},
            {'id': str(uuid.uuid4()), 'ward_number': 4, 'age_group': 'AGE_15_TO_59', 'gender': 'FEMALE', 'population': 1349},
            {'id': str(uuid.uuid4()), 'ward_number': 4, 'age_group': 'AGE_15_TO_59', 'gender': 'MALE', 'population': 1136},
            {'id': str(uuid.uuid4()), 'ward_number': 4, 'age_group': 'AGE_60_PLUS', 'gender': 'FEMALE', 'population': 191},
            {'id': str(uuid.uuid4()), 'ward_number': 4, 'age_group': 'AGE_60_PLUS', 'gender': 'MALE', 'population': 170},
            
            # Ward 5
            {'id': str(uuid.uuid4()), 'ward_number': 5, 'age_group': 'AGE_0_TO_14', 'gender': 'FEMALE', 'population': 455},
            {'id': str(uuid.uuid4()), 'ward_number': 5, 'age_group': 'AGE_0_TO_14', 'gender': 'MALE', 'population': 281},
            {'id': str(uuid.uuid4()), 'ward_number': 5, 'age_group': 'AGE_15_TO_59', 'gender': 'FEMALE', 'population': 1246},
            {'id': str(uuid.uuid4()), 'ward_number': 5, 'age_group': 'AGE_15_TO_59', 'gender': 'MALE', 'population': 1046},
            {'id': str(uuid.uuid4()), 'ward_number': 5, 'age_group': 'AGE_60_PLUS', 'gender': 'FEMALE', 'population': 184},
            {'id': str(uuid.uuid4()), 'ward_number': 5, 'age_group': 'AGE_60_PLUS', 'gender': 'MALE', 'population': 194},
            
            # Ward 6
            {'id': str(uuid.uuid4()), 'ward_number': 6, 'age_group': 'AGE_0_TO_14', 'gender': 'FEMALE', 'population': 643},
            {'id': str(uuid.uuid4()), 'ward_number': 6, 'age_group': 'AGE_0_TO_14', 'gender': 'MALE', 'population': 559},
            {'id': str(uuid.uuid4()), 'ward_number': 6, 'age_group': 'AGE_15_TO_59', 'gender': 'FEMALE', 'population': 1503},
            {'id': str(uuid.uuid4()), 'ward_number': 6, 'age_group': 'AGE_15_TO_59', 'gender': 'MALE', 'population': 1250},
            {'id': str(uuid.uuid4()), 'ward_number': 6, 'age_group': 'AGE_60_PLUS', 'gender': 'FEMALE', 'population': 284},
            {'id': str(uuid.uuid4()), 'ward_number': 6, 'age_group': 'AGE_60_PLUS', 'gender': 'MALE', 'population': 272},
            
            # Ward 7
            {'id': str(uuid.uuid4()), 'ward_number': 7, 'age_group': 'AGE_0_TO_14', 'gender': 'FEMALE', 'population': 328},
            {'id': str(uuid.uuid4()), 'ward_number': 7, 'age_group': 'AGE_0_TO_14', 'gender': 'MALE', 'population': 464},
            {'id': str(uuid.uuid4()), 'ward_number': 7, 'age_group': 'AGE_15_TO_59', 'gender': 'FEMALE', 'population': 873},
            {'id': str(uuid.uuid4()), 'ward_number': 7, 'age_group': 'AGE_15_TO_59', 'gender': 'MALE', 'population': 686},
            {'id': str(uuid.uuid4()), 'ward_number': 7, 'age_group': 'AGE_60_PLUS', 'gender': 'FEMALE', 'population': 173},
            {'id': str(uuid.uuid4()), 'ward_number': 7, 'age_group': 'AGE_60_PLUS', 'gender': 'MALE', 'population': 89},
        ]

        # Check if data already exists
        existing_count = WardAgeWiseEconomicallyActivePopulation.objects.count()
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
            for data in economically_active_data:
                obj, created = WardAgeWiseEconomicallyActivePopulation.objects.get_or_create(
                    ward_number=data['ward_number'],
                    age_group=data['age_group'],
                    gender=data['gender'],
                    defaults={
                        'id': data['id'],
                        'population': data['population'],
                    }
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(
                        f"Created: Ward {data['ward_number']} - {data['age_group']} - {data['gender']} ({data['population']} people)"
                    )
                else:
                    # Update existing record
                    obj.population = data['population']
                    obj.save()
                    self.stdout.write(
                        f"Updated: Ward {data['ward_number']} - {data['age_group']} - {data['gender']} ({data['population']} people)"
                    )

        # Print summary
        total_records = WardAgeWiseEconomicallyActivePopulation.objects.count()
        total_population = sum(WardAgeWiseEconomicallyActivePopulation.objects.values_list('population', flat=True))
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully processed {len(economically_active_data)} economically active population demographic records '
                f'({created_count} new, {len(economically_active_data) - created_count} updated)\n'
                f'Total records in database: {total_records}\n'
                f'Total population covered: {total_population:,} people'
            )
        )

        # Print age group breakdown
        self.stdout.write('\nAge group breakdown:')
        for age_choice in EconomicallyActiveAgeGroupChoice.choices:
            age_code = age_choice[0]
            age_name = age_choice[1]
            age_population = WardAgeWiseEconomicallyActivePopulation.objects.filter(age_group=age_code).aggregate(
                total=models.Sum('population')
            )['total'] or 0
            
            if age_population > 0:
                percentage = age_population / total_population * 100
                self.stdout.write(
                    f'  {age_name}: {age_population:,} people ({percentage:.2f}%)'
                )
            else:
                self.stdout.write(
                    f'  {age_name}: 0 people (0.00%)'
                )

        # Print gender breakdown
        self.stdout.write('\nGender breakdown:')
        for gender_choice in GenderChoice.choices:
            gender_code = gender_choice[0]
            gender_name = gender_choice[1]
            gender_population = WardAgeWiseEconomicallyActivePopulation.objects.filter(gender=gender_code).aggregate(
                total=models.Sum('population')
            )['total'] or 0
            
            if gender_population > 0:
                percentage = gender_population / total_population * 100
                self.stdout.write(
                    f'  {gender_name}: {gender_population:,} people ({percentage:.2f}%)'
                )

        # Ward-wise summary
        self.stdout.write('\nWard-wise economically active population summary:')
        for ward_num in range(1, 8):
            ward_population = WardAgeWiseEconomicallyActivePopulation.objects.filter(ward_number=ward_num).aggregate(
                total=models.Sum('population')
            )['total'] or 0
            if ward_population > 0:
                self.stdout.write(f'  वडा {ward_num}: {ward_population:,} people')
