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
        "id": "8fc34e1d-6c8f-4a82-9ac4-4d712c32bc07",
        "ward_number": 1,
        "death_cause": "ASTHMA",
        "population": 2,
    },
    {
        "id": "df959316-fdcb-408f-99c5-bd89f972be97",
        "ward_number": 1,
        "death_cause": "BLOOD_PRESSURE_HIGH_AND_LOW_BLOOD_PRESSURE",
        "population": 1,
    },
    {
        "id": "45230335-d3b1-4011-9fb7-1948f72e0b45",
        "ward_number": 1,
        "death_cause": "CANCER",
        "population": 2,
    },
    {
        "id": "5ca2bd90-c391-401b-8a3e-9e8e3947f219",
        "ward_number": 1,
        "death_cause": "NOT_STATED",
        "population": 2,
    },
    {
        "id": "c455675c-f1a0-4737-873e-ebd8b844472a",
        "ward_number": 1,
        "death_cause": "OTHER_ACCIDENTS",
        "population": 2,
    },
    {
        "id": "77f3f2e7-450e-4874-aba6-a68aad39e54f",
        "ward_number": 2,
        "death_cause": "BLOOD_PRESSURE_HIGH_AND_LOW_BLOOD_PRESSURE",
        "population": 5,
    },
    {
        "id": "934aafa5-c10e-4ad5-92e3-237617796d09",
        "ward_number": 2,
        "death_cause": "DEATH_BY_OLD_AGE",
        "population": 1,
    },
    {
        "id": "88317e47-3c4d-4fde-ad34-bd4f1e1d2a98",
        "ward_number": 2,
        "death_cause": "DIABETES",
        "population": 1,
    },
    {
        "id": "3c3d39fa-4e5e-4462-8a88-0aff038613ed",
        "ward_number": 2,
        "death_cause": "FLU",
        "population": 1,
    },
    {
        "id": "88f315d4-e97e-48fb-ab06-131e63c8268a",
        "ward_number": 2,
        "death_cause": "HEART_RELATED_DISEASES",
        "population": 2,
    },
    {
        "id": "cdbebbc0-93d4-4633-97ec-a81eb939cb52",
        "ward_number": 2,
        "death_cause": "KIDNEY_RELATED_DISEASES",
        "population": 1,
    },
    {
        "id": "77c2a9fe-44c3-4329-9fa2-6f06d04064c3",
        "ward_number": 2,
        "death_cause": "NOT_STATED",
        "population": 3,
    },
    {
        "id": "225f9603-fc8f-4594-a5c6-e3407d388d5f",
        "ward_number": 3,
        "death_cause": "ASTHMA",
        "population": 1,
    },
    {
        "id": "b33ee5c0-16c7-4bd4-83e3-22c4677097ad",
        "ward_number": 3,
        "death_cause": "BLOOD_PRESSURE_HIGH_AND_LOW_BLOOD_PRESSURE",
        "population": 2,
    },
    {
        "id": "967d68a6-0a1c-4e22-82d7-eabf52c0f3bc",
        "ward_number": 3,
        "death_cause": "CANCER",
        "population": 4,
    },
    {
        "id": "23418ec8-7913-4905-88f8-7ab2dfc8220d",
        "ward_number": 3,
        "death_cause": "DEATH_BY_OLD_AGE",
        "population": 5,
    },
    {
        "id": "5daf8e71-a47a-4b3a-90a3-6e4df87b66ca",
        "ward_number": 3,
        "death_cause": "DIABETES",
        "population": 2,
    },
    {
        "id": "15a0b51a-e8a9-4b09-bd21-350016efd959",
        "ward_number": 3,
        "death_cause": "EPILEPSY",
        "population": 1,
    },
    {
        "id": "0f6653d1-7996-4daf-afa9-5b00ff388fef",
        "ward_number": 3,
        "death_cause": "FLU",
        "population": 1,
    },
    {
        "id": "647bce36-fd84-465c-8a61-c12fbb8c0a67",
        "ward_number": 3,
        "death_cause": "JAUNDICE_HEPATITIS",
        "population": 1,
    },
    {
        "id": "904fa37b-d4ae-4311-a71c-0809ddca693b",
        "ward_number": 3,
        "death_cause": "NOT_STATED",
        "population": 2,
    },
    {
        "id": "fa843e53-5dcb-4589-b8a6-516a3b8f9365",
        "ward_number": 3,
        "death_cause": "OTHER_ACCIDENTS",
        "population": 1,
    },
    {
        "id": "45e13535-c56c-415e-8277-39afc7502f48",
        "ward_number": 3,
        "death_cause": "OTHER_SEXUALLY_TRANSMITTED_DISEASES",
        "population": 1,
    },
    {
        "id": "38aa06bb-8994-484a-94d2-40b8efdc3a3b",
        "ward_number": 3,
        "death_cause": "RESPIRATORY_DISEASES",
        "population": 1,
    },
    {
        "id": "d219c882-ff84-4c00-b38b-4ae1983184de",
        "ward_number": 4,
        "death_cause": "ASTHMA",
        "population": 2,
    },
    {
        "id": "1b7dc524-0319-4074-bef6-4d3d79fc2fbb",
        "ward_number": 4,
        "death_cause": "BLOOD_PRESSURE_HIGH_AND_LOW_BLOOD_PRESSURE",
        "population": 1,
    },
    {
        "id": "075c3afc-e172-42f7-814b-cfa5698e5112",
        "ward_number": 4,
        "death_cause": "DEATH_BY_OLD_AGE",
        "population": 1,
    },
    {
        "id": "7441ee11-cda3-4da1-9667-5749e65fe53e",
        "ward_number": 4,
        "death_cause": "DIABETES",
        "population": 1,
    },
    {
        "id": "1859023c-d78e-4606-a258-378f3805dbc6",
        "ward_number": 4,
        "death_cause": "GASTRIC_ULCER_INTESTINAL_DISEASE",
        "population": 1,
    },
    {
        "id": "9f34d35e-e2ea-4c96-9046-6dfe31d21f5a",
        "ward_number": 4,
        "death_cause": "HEART_RELATED_DISEASES",
        "population": 2,
    },
    {
        "id": "a0e81ae7-dbe1-450b-aba8-f19917519613",
        "ward_number": 4,
        "death_cause": "JAUNDICE_HEPATITIS",
        "population": 1,
    },
    {
        "id": "65e95e7c-4017-4af4-a2a9-0add2f6c2be3",
        "ward_number": 4,
        "death_cause": "NOT_STATED",
        "population": 6,
    },
    {
        "id": "9434ec6f-9060-4e43-9353-2abab5f71a25",
        "ward_number": 4,
        "death_cause": "RESPIRATORY_DISEASES",
        "population": 1,
    },
    {
        "id": "08866fcf-bf28-47a4-bf96-98b772d50f81",
        "ward_number": 5,
        "death_cause": "ASTHMA",
        "population": 1,
    },
    {
        "id": "eb759dfb-81e5-4e81-a695-b2d37fa84291",
        "ward_number": 5,
        "death_cause": "BLOOD_PRESSURE_HIGH_AND_LOW_BLOOD_PRESSURE",
        "population": 2,
    },
    {
        "id": "1ba34976-cc30-4403-b412-d284751e63bc",
        "ward_number": 5,
        "death_cause": "CANCER",
        "population": 2,
    },
    {
        "id": "d1af4f8f-2e3e-46c1-bd62-e3b6ebe37c47",
        "ward_number": 5,
        "death_cause": "DEATH_BY_OLD_AGE",
        "population": 10,
    },
    {
        "id": "652862b6-d803-4be2-9b27-1017771d10cc",
        "ward_number": 5,
        "death_cause": "GASTRIC_ULCER_INTESTINAL_DISEASE",
        "population": 1,
    },
    {
        "id": "770f0205-7f56-4240-a201-ca97ad473c31",
        "ward_number": 5,
        "death_cause": "HAIJA",
        "population": 1,
    },
    {
        "id": "58eb0a10-0b1c-4652-b1f3-85019a21d389",
        "ward_number": 5,
        "death_cause": "HEART_RELATED_DISEASES",
        "population": 3,
    },
    {
        "id": "5d30583f-b0f5-44d2-9435-6fc36d1dff0d",
        "ward_number": 5,
        "death_cause": "KIDNEY_RELATED_DISEASES",
        "population": 1,
    },
    {
        "id": "8419a6c7-a373-4d3f-b151-da8014dde50b",
        "ward_number": 5,
        "death_cause": "LEPROSY",
        "population": 1,
    },
    {
        "id": "c300015b-df44-408e-8d84-6c239fb87dbc",
        "ward_number": 5,
        "death_cause": "NATURAL_DISASTER",
        "population": 2,
    },
    {
        "id": "8c838f46-f475-450c-833c-7ea1060b1e0b",
        "ward_number": 5,
        "death_cause": "NOT_STATED",
        "population": 1,
    },
    {
        "id": "e7997acf-d4ed-4257-a424-6e11bd6950ae",
        "ward_number": 5,
        "death_cause": "OTHER_ACCIDENTS",
        "population": 2,
    },
    {
        "id": "cd1605ba-e524-45c2-8901-950cb66ec0af",
        "ward_number": 5,
        "death_cause": "PNEUMONIA",
        "population": 1,
    },
    {
        "id": "8e9751a4-5628-4c87-90d4-1d69d5296cee",
        "ward_number": 5,
        "death_cause": "SUICIDE",
        "population": 4,
    },
    {
        "id": "229ae26a-c1e4-41b8-8d94-0973d33b8c1a",
        "ward_number": 5,
        "death_cause": "TRAFFIC_ACCIDENT",
        "population": 1,
    },
    {
        "id": "28c3ce52-4cf7-4240-a878-0df09509caee",
        "ward_number": 5,
        "death_cause": "TUBERCULOSIS",
        "population": 3,
    },
    {
        "id": "e7e93bcf-28d8-465a-a3ed-34ecb073cb9b",
        "ward_number": 5,
        "death_cause": "TYPHOID",
        "population": 1,
    },
    {
        "id": "933d7f67-84f5-438c-9558-7c653f517fa4",
        "ward_number": 6,
        "death_cause": "ASTHMA",
        "population": 4,
    },
    {
        "id": "6d2409e8-ccb6-432f-b1b4-98152c969dbc",
        "ward_number": 6,
        "death_cause": "BLOOD_PRESSURE_HIGH_AND_LOW_BLOOD_PRESSURE",
        "population": 1,
    },
    {
        "id": "24770207-bab2-48b1-bd2d-b9963f1b32d2",
        "ward_number": 6,
        "death_cause": "CANCER",
        "population": 5,
    },
    {
        "id": "f0618df4-ff5a-4efb-8c6f-efddeb922e87",
        "ward_number": 6,
        "death_cause": "DEATH_BY_OLD_AGE",
        "population": 8,
    },
    {
        "id": "e04d835d-e2fa-44a0-aa3d-b9202cf4bcae",
        "ward_number": 6,
        "death_cause": "DIABETES",
        "population": 2,
    },
    {
        "id": "f6b8efc0-50ff-4134-842b-ee8653785de6",
        "ward_number": 6,
        "death_cause": "HEART_RELATED_DISEASES",
        "population": 3,
    },
    {
        "id": "e954c437-30ba-4d82-b9df-7af9a982e81d",
        "ward_number": 6,
        "death_cause": "KALA_AZAR",
        "population": 2,
    },
    {
        "id": "c23ee6ff-3273-4085-9e51-0546637c359b",
        "ward_number": 6,
        "death_cause": "KIDNEY_RELATED_DISEASES",
        "population": 3,
    },
    {
        "id": "b9e40c5e-1b74-4ac4-b4c0-00da09d104e2",
        "ward_number": 6,
        "death_cause": "LIVER_RELATED_DISEASES",
        "population": 1,
    },
    {
        "id": "f8206581-761a-4cd7-9662-8fbec9277791",
        "ward_number": 6,
        "death_cause": "NOT_STATED",
        "population": 2,
    },
    {
        "id": "49230ca1-4acb-476f-b09a-e7b338c07d1e",
        "ward_number": 6,
        "death_cause": "SUICIDE",
        "population": 1,
    },
    {
        "id": "3d2ab799-55f1-4cde-ac91-7ba3d3633339",
        "ward_number": 7,
        "death_cause": "ASTHMA",
        "population": 1,
    },
    {
        "id": "e04c0213-108c-44d7-bb5c-dc7f38426976",
        "ward_number": 7,
        "death_cause": "BLOOD_PRESSURE_HIGH_AND_LOW_BLOOD_PRESSURE",
        "population": 2,
    },
    {
        "id": "ec286551-5549-47c8-a37f-cfaf75e66452",
        "ward_number": 7,
        "death_cause": "CANCER",
        "population": 1,
    },
    {
        "id": "c7babfe8-e96a-41bc-bbdd-4dcdb3d26020",
        "ward_number": 7,
        "death_cause": "DEATH_BY_OLD_AGE",
        "population": 3,
    },
    {
        "id": "4ffc99b5-5093-4dff-b39d-1436d7fd9e87",
        "ward_number": 7,
        "death_cause": "HAIJA",
        "population": 1,
    },
    {
        "id": "9f5a8e55-2179-4a1f-8f91-f30a67028acc",
        "ward_number": 7,
        "death_cause": "HEART_RELATED_DISEASES",
        "population": 1,
    },
    {
        "id": "f8aa8b39-dfc0-4ad3-a26a-0ec23dafb4cb",
        "ward_number": 7,
        "death_cause": "KIDNEY_RELATED_DISEASES",
        "population": 1,
    },
    {
        "id": "f7da4398-a29d-4620-aca0-58b98f9fa251",
        "ward_number": 7,
        "death_cause": "PNEUMONIA",
        "population": 1,
    },
    {
        "id": "412289d2-863d-4e39-8aef-cd353c7ed4c7",
        "ward_number": 7,
        "death_cause": "TRAFFIC_ACCIDENT",
        "population": 1,
    },
    {
        "id": "eb54409d-28d6-4738-a3ea-f25579bede62",
        "ward_number": 7,
        "death_cause": "TYPHOID",
        "population": 1,
    },
    {
        "id": "66936cb2-5bf3-4f47-86f1-0c8ca9fc9c7f",
        "ward_number": 8,
        "death_cause": "DEATH_BY_OLD_AGE",
        "population": 1,
    },
    {
        "id": "8885e479-309a-4c3d-8f44-6e7c4aba8df5",
        "ward_number": 8,
        "death_cause": "HEART_RELATED_DISEASES",
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
