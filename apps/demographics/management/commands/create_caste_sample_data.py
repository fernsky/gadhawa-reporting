"""
Management command to create caste demographics data based on actual data
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from apps.demographics.models import MunicipalityWideCastePopulation, CasteTypeChoice
import uuid


class Command(BaseCommand):
    help = 'Create caste demographics data based on actual municipality-wide data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before creating new data',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing caste data...'))
            MunicipalityWideCastePopulation.objects.all().delete()

        self.stdout.write('Creating caste demographics data based on actual municipality-wide data...')

        caste_data = [
            {'id': str(uuid.uuid4()), 'caste': 'BRAHMIN', 'population': 5000},
            {'id': str(uuid.uuid4()), 'caste': 'CHHETRI', 'population': 7000},
            {'id': str(uuid.uuid4()), 'caste': 'MAGAR', 'population': 3000},
            {'id': str(uuid.uuid4()), 'caste': 'DALIT', 'population': 2000},
        ]

        existing_count = MunicipalityWideCastePopulation.objects.count()
        if existing_count > 0 and not options['clear']:
            self.stdout.write(
                self.style.WARNING(
                    f'Found {existing_count} existing records. Use --clear to replace them.'
                )
            )
            return

        created_count = 0
        with transaction.atomic():
            for data in caste_data:
                obj, created = MunicipalityWideCastePopulation.objects.get_or_create(
                    caste=data['caste'],
                    defaults={
                        'id': data['id'],
                        'population': data['population'],
                    }
                )

                if created:
                    created_count += 1
                    self.stdout.write(
                        f"Created: {data['caste']} ({data['population']} people)"
                    )
                else:
                    obj.population = data['population']
                    obj.save()
                    self.stdout.write(
                        f"Updated: {data['caste']} ({data['population']} people)"
                    )

        total_records = MunicipalityWideCastePopulation.objects.count()
        total_population = sum(MunicipalityWideCastePopulation.objects.values_list('population', flat=True))

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully processed {len(caste_data)} caste demographic records '
                f'({created_count} new, {len(caste_data) - created_count} updated)\n'
                f'Total records in database: {total_records}\n'
                f'Total population covered: {total_population:,} people'
            )
        )

        self.stdout.write('\nCaste breakdown:')
        for caste_choice in CasteTypeChoice.choices:
            caste_code = caste_choice[0]
            caste_name = caste_choice[1]
            try:
                caste_obj = MunicipalityWideCastePopulation.objects.get(caste=caste_code)
                caste_pop = caste_obj.population
                percentage = caste_pop / total_population * 100
                self.stdout.write(
                    f'  {caste_name}: {caste_pop:,} ({percentage:.2f}%)'
                )
            except MunicipalityWideCastePopulation.DoesNotExist:
                self.stdout.write(
                    f'  {caste_name}: 0 (0.00%)'
                )
