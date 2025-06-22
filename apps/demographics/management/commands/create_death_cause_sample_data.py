"""
Management command to create death cause sample data based on provided data
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from apps.demographics.models import WardWiseDeathCause, DeathCauseChoice
import uuid
from datetime import datetime

SAMPLE_DATA = [
    {
        "id": "da98b524-c4ba-48ed-9223-105d4899095d",
        "ward_number": 1,
        "death_cause": "CANCER",
        "population": 3,
    },
    {
        "id": "4e00e46e-92bd-4b4f-a61a-e38d8c010159",
        "ward_number": 1,
        "death_cause": "DEATH_BY_OLD_AGE",
        "population": 8,
    },
    {
        "id": "2cc378e0-ff66-45a3-9ec3-9a2f9afed414",
        "ward_number": 1,
        "death_cause": "HEART_RELATED_DISEASES",
        "population": 2,
    },
    {
        "id": "a77a03dd-b9c7-4a0f-a7e8-9b00837a569b",
        "ward_number": 1,
        "death_cause": "LEPROSY",
        "population": 1,
    },
    {
        "id": "3ca415e8-cfc8-4a30-bbae-3ae1dcbf4872",
        "ward_number": 1,
        "death_cause": "NOT_STATED",
        "population": 1,
    },
    {
        "id": "9f60f38a-545c-47cd-b474-a0b5d8f33be7",
        "ward_number": 1,
        "death_cause": "OTHER_ACCIDENTS",
        "population": 1,
    },
    {
        "id": "5d299ab1-8356-4544-8f0b-1e4975894907",
        "ward_number": 1,
        "death_cause": "PNEUMONIA",
        "population": 3,
    },
    {
        "id": "0b793626-9b19-4cca-b5a4-08916e26c09b",
        "ward_number": 1,
        "death_cause": "TRAFFIC_ACCIDENT",
        "population": 1,
    },
    {
        "id": "d45f3651-538e-4e70-a31e-a04808b126a7",
        "ward_number": 2,
        "death_cause": "ASTHMA",
        "population": 6,
    },
    {
        "id": "e820ee95-56ff-4c75-b259-88ab5b9da768",
        "ward_number": 2,
        "death_cause": "BLOOD_PRESSURE_HIGH_AND_LOW_BLOOD_PRESSURE",
        "population": 3,
    },
    {
        "id": "ebc889e6-47d6-455c-ae1a-1b170f4deecf",
        "ward_number": 2,
        "death_cause": "CANCER",
        "population": 4,
    },
    {
        "id": "dbffe49e-a53d-4286-bb50-0412c1f3238a",
        "ward_number": 2,
        "death_cause": "DEATH_BY_OLD_AGE",
        "population": 7,
    },
    {
        "id": "b6273dfa-156e-472e-9702-08692e3775a2",
        "ward_number": 2,
        "death_cause": "DIABETES",
        "population": 2,
    },
    {
        "id": "9fca7bf4-2a71-4dc6-936f-b7ff0b029c75",
        "ward_number": 2,
        "death_cause": "GASTRIC_ULCER_INTESTINAL_DISEASE",
        "population": 1,
    },
    {
        "id": "f8826d83-9836-4b78-bb50-e445cf1b66e4",
        "ward_number": 2,
        "death_cause": "HEART_RELATED_DISEASES",
        "population": 3,
    },
    {
        "id": "46c523ca-b422-45c9-8ddd-961dbb1e2e3b",
        "ward_number": 2,
        "death_cause": "KALA_AZAR",
        "population": 1,
    },
    {
        "id": "95fd268c-dd32-4208-bb64-e9ebacd3c43f",
        "ward_number": 2,
        "death_cause": "KIDNEY_RELATED_DISEASES",
        "population": 3,
    },
    {
        "id": "33d0146a-1bbb-4045-a038-bcd7d72b5d20",
        "ward_number": 2,
        "death_cause": "LEPROSY",
        "population": 1,
    },
    {
        "id": "5dbb3f7b-3699-4bc5-b886-8dbca21851b3",
        "ward_number": 2,
        "death_cause": "NOT_STATED",
        "population": 1,
    },
    {
        "id": "900b63b4-f1d9-4194-b949-b2adc36f3327",
        "ward_number": 2,
        "death_cause": "PNEUMONIA",
        "population": 5,
    },
    {
        "id": "f3f493e4-3dcb-44ee-bd60-a72616b61c93",
        "ward_number": 2,
        "death_cause": "RESPIRATORY_DISEASES",
        "population": 2,
    },
    {
        "id": "7aa80bc9-d3d2-4f43-8e08-661e46753e86",
        "ward_number": 2,
        "death_cause": "TRAFFIC_ACCIDENT",
        "population": 1,
    },
    {
        "id": "101e125f-165f-4b15-b58d-4bb68268f57a",
        "ward_number": 2,
        "death_cause": "TYPHOID",
        "population": 8,
    },
    {
        "id": "524bc9eb-e89b-447e-ba56-795182d8b597",
        "ward_number": 3,
        "death_cause": "ASTHMA",
        "population": 1,
    },
    {
        "id": "9913c058-9e95-47a9-bfde-2bf1433b7b48",
        "ward_number": 3,
        "death_cause": "BLOOD_PRESSURE_HIGH_AND_LOW_BLOOD_PRESSURE",
        "population": 2,
    },
    {
        "id": "f8da57ae-5f71-4293-83dd-f91182775242",
        "ward_number": 3,
        "death_cause": "EPILEPSY",
        "population": 1,
    },
    {
        "id": "790754ea-3749-48c6-b6d5-edd83f2345a4",
        "ward_number": 3,
        "death_cause": "HEART_RELATED_DISEASES",
        "population": 2,
    },
    {
        "id": "6bd95197-b787-42c5-b15b-42f39f2a4aa5",
        "ward_number": 3,
        "death_cause": "NOT_STATED",
        "population": 0,
    },
    {
        "id": "32149f01-901c-43cf-85c5-c4c7f0327eaa",
        "ward_number": 3,
        "death_cause": "OTHER_ACCIDENTS",
        "population": 1,
    },
    {
        "id": "c68f6cbf-2b1e-443e-bc93-f6e005640735",
        "ward_number": 4,
        "death_cause": "ASTHMA",
        "population": 2,
    },
    {
        "id": "dbda6527-8a4a-4a1c-93ff-dcccde10f8e0",
        "ward_number": 4,
        "death_cause": "BLOOD_PRESSURE_HIGH_AND_LOW_BLOOD_PRESSURE",
        "population": 4,
    },
    {
        "id": "3467da89-5351-40d0-a0de-7b408a165955",
        "ward_number": 4,
        "death_cause": "DEATH_BY_OLD_AGE",
        "population": 4,
    },
    {
        "id": "cd97585a-7f2b-46dc-a729-c6925b713107",
        "ward_number": 4,
        "death_cause": "KALA_AZAR",
        "population": 1,
    },
    {
        "id": "1524e3c6-cae8-4e45-b721-787cb5fdf930",
        "ward_number": 4,
        "death_cause": "NOT_STATED",
        "population": 2,
    },
    {
        "id": "f18150b8-fb15-4436-be14-86eeef5dacd2",
        "ward_number": 4,
        "death_cause": "PNEUMONIA",
        "population": 1,
    },
    {
        "id": "7bd8dd5f-6730-43b1-b5eb-eab98612c3c1",
        "ward_number": 5,
        "death_cause": "DEATH_BY_OLD_AGE",
        "population": 3,
    },
    {
        "id": "0b3edbd8-3bd8-4709-a36f-cc892edaeb81",
        "ward_number": 5,
        "death_cause": "HEART_RELATED_DISEASES",
        "population": 2,
    },
    {
        "id": "8514496c-dee7-4ec3-a995-da852a200dce",
        "ward_number": 5,
        "death_cause": "KIDNEY_RELATED_DISEASES",
        "population": 1,
    },
    {
        "id": "546b13f7-7744-4550-80f2-e11f801ea20f",
        "ward_number": 5,
        "death_cause": "NOT_STATED",
        "population": 2,
    },
    {
        "id": "5590f4d4-a984-4907-8532-6612c4f45eea",
        "ward_number": 6,
        "death_cause": "ASTHMA",
        "population": 1,
    },
    {
        "id": "8c49a698-8a2d-40a4-ad38-f500b7825278",
        "ward_number": 6,
        "death_cause": "BLOOD_PRESSURE_HIGH_AND_LOW_BLOOD_PRESSURE",
        "population": 1,
    },
    {
        "id": "7b21f2fa-4ff7-424a-9ca2-830b2b64c860",
        "ward_number": 6,
        "death_cause": "DEATH_BY_OLD_AGE",
        "population": 3,
    },
    {
        "id": "d6ef4c16-3c61-4f3e-9b45-018070fe154d",
        "ward_number": 6,
        "death_cause": "FLU",
        "population": 1,
    },
    {
        "id": "873d7c23-b304-4ac8-b1ec-7c8ff8e0c3a8",
        "ward_number": 6,
        "death_cause": "OTHER_ACCIDENTS",
        "population": 1,
    },
    {
        "id": "7078e570-244f-44cb-80a6-3b51613a342c",
        "ward_number": 6,
        "death_cause": "SCABIES",
        "population": 1,
    },
    {
        "id": "c3c747a0-acef-44dd-96dd-3e9eebed92d1",
        "ward_number": 6,
        "death_cause": "SUICIDE",
        "population": 1,
    },
    {
        "id": "95625aca-e958-4190-9133-af2d0f45b176",
        "ward_number": 6,
        "death_cause": "TRAFFIC_ACCIDENT",
        "population": 1,
    },
    {
        "id": "ecdb0ab8-47b9-4d6e-bd0d-c72ad8b4312b",
        "ward_number": 6,
        "death_cause": "TUBERCULOSIS",
        "population": 1,
    },
    {
        "id": "b7f48b0b-d6c5-45fe-855b-dca14170c524",
        "ward_number": 7,
        "death_cause": "ASTHMA",
        "population": 2,
    },
    {
        "id": "892b7f54-a3d6-4dcf-9f30-227fc9ea106e",
        "ward_number": 7,
        "death_cause": "DEATH_BY_OLD_AGE",
        "population": 2,
    },
    {
        "id": "e14a2326-dea0-4d37-8b4d-a43cf7553329",
        "ward_number": 7,
        "death_cause": "LIVER_RELATED_DISEASES",
        "population": 1,
    },
    {
        "id": "d920ea19-59b5-4772-92ef-b79404aff6e2",
        "ward_number": 7,
        "death_cause": "NATURAL_DISASTER",
        "population": 1,
    },
    {
        "id": "27cf74ad-8764-47ef-89f9-899fc45e8338",
        "ward_number": 7,
        "death_cause": "NOT_STATED",
        "population": 1,
    },
    {
        "id": "960ed36b-728d-44f4-9c09-b23f5f2ea663",
        "ward_number": 7,
        "death_cause": "OTHER_ACCIDENTS",
        "population": 1,
    },
    {
        "id": "f83b844e-9b9c-4222-9475-0177826d67df",
        "ward_number": 7,
        "death_cause": "SUICIDE",
        "population": 1,
    },
]


class Command(BaseCommand):
    help = "Create death cause sample data for wards"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before creating new data",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write(
                self.style.WARNING("Clearing existing death cause data...")
            )
            WardWiseDeathCause.objects.all().delete()

        self.stdout.write("Creating death cause sample data for wards...")

        created_count = 0
        with transaction.atomic():
            for data in SAMPLE_DATA:
                obj, created = WardWiseDeathCause.objects.get_or_create(
                    id=data["id"],
                    ward_number=data["ward_number"],
                    death_cause=data["death_cause"],
                    defaults={"population": data["population"]},
                )
                if not created:
                    obj.population = data["population"]
                    obj.save()
                created_count += 1
                self.stdout.write(
                    f"Added: वडा {data['ward_number']} - {data['death_cause']} ({data['population']})"
                )

        total_records = WardWiseDeathCause.objects.count()
        self.stdout.write(
            self.style.SUCCESS(
                f"\nSuccessfully processed {created_count} death cause records. Total records: {total_records}"
            )
        )
