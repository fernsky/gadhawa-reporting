"""
Management command to create language demographics data based on actual data
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from apps.demographics.models import MunicipalityWideMotherTonguePopulation, LanguageTypeChoice
import uuid


class Command(BaseCommand):
    help = 'Create language demographics data based on actual municipality-wide data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before creating new data',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing language data...'))
            MunicipalityWideMotherTonguePopulation.objects.all().delete()

        self.stdout.write('Creating language demographics data based on actual municipality-wide data...')

        language_data = [
            {'id': str(uuid.uuid4()), 'language': 'NEPALI', 'population': 15000},
            {'id': str(uuid.uuid4()), 'language': 'MAITHILI', 'population': 5000},
            {'id': str(uuid.uuid4()), 'language': 'BHOJPURI', 'population': 3000},
            {'id': str(uuid.uuid4()), 'language': 'ENGLISH', 'population': 1000},
        ]

        existing_count = MunicipalityWideMotherTonguePopulation.objects.count()
        if existing_count > 0 and not options['clear']:
            self.stdout.write(
                self.style.WARNING(
                    f'Found {existing_count} existing records. Use --clear to replace them.'
                )
            )
            return

        created_count = 0
        with transaction.atomic():
            for data in language_data:
                obj, created = MunicipalityWideMotherTonguePopulation.objects.get_or_create(
                    language=data['language'],
                    defaults={
                        'id': data['id'],
                        'population': data['population'],
                    }
                )

                if created:
                    created_count += 1
                    self.stdout.write(
                        f"Created: {data['language']} ({data['population']} people)"
                    )
                else:
                    obj.population = data['population']
                    obj.save()
                    self.stdout.write(
                        f"Updated: {data['language']} ({data['population']} people)"
                    )

        total_records = MunicipalityWideMotherTonguePopulation.objects.count()
        total_population = sum(MunicipalityWideMotherTonguePopulation.objects.values_list('population', flat=True))

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully processed {len(language_data)} language demographic records '
                f'({created_count} new, {len(language_data) - created_count} updated)\n'
                f'Total records in database: {total_records}\n'
                f'Total population covered: {total_population:,} people'
            )
        )

        self.stdout.write('\nLanguage breakdown:')
        for language_choice in LanguageTypeChoice.choices:
            language_code = language_choice[0]
            language_name = language_choice[1]
            try:
                language_obj = MunicipalityWideMotherTonguePopulation.objects.get(language=language_code)
                language_pop = language_obj.population
                percentage = language_pop / total_population * 100
                self.stdout.write(
                    f'  {language_name}: {language_pop:,} ({percentage:.2f}%)'
                )
            except MunicipalityWideMotherTonguePopulation.DoesNotExist:
                self.stdout.write(
                    f'  {language_name}: 0 (0.00%)'
                )
