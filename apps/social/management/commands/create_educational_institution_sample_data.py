"""
Management command to create sample data for Ward Wise Educational Institutions

This command creates comprehensive sample data for educational institutions
and student enrollment based on the provided JSON data for Section 5.1.2.
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from apps.social.models import (
    WardWiseEducationalInstitution,
    EducationalInstitutionTypeChoice,
    SchoolLevelChoice,
)
from apps.reports.utils.nepali_numbers import to_nepali_digits


class Command(BaseCommand):
    help = "Create sample data for Ward Wise Educational Institutions (५.१.२)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete existing data before creating new data",
        )

    def handle(self, *args, **options):
        if options["reset"]:
            self.stdout.write("Clearing existing educational institution data...")
            WardWiseEducationalInstitution.objects.all().delete()
            self.stdout.write(
                self.style.SUCCESS("✓ Existing data cleared successfully")
            )

        # Sample data from the provided JSON
        sample_data = [
            {
                "ward_number": 1,
                "data_year": "2079",
                "male_students": 276,
                "female_students": 208,
                "name": "नेपाल राष्ट्रिय मा.वि., लुग्री-१",
            },
            {
                "ward_number": 1,
                "data_year": "2080",
                "male_students": 179,
                "female_students": 240,
                "name": "नेपाल राष्ट्रिय मा.वि., लुग्री-१",
            },
            {
                "ward_number": 1,
                "data_year": "2081",
                "male_students": 160,
                "female_students": 190,
                "name": "नेपाल राष्ट्रिय मा.वि., लुग्री-१",
            },
            {
                "ward_number": 1,
                "data_year": "2079",
                "male_students": 203,
                "female_students": 262,
                "name": "मा.वि., लुग्री-१",
            },
            {
                "ward_number": 1,
                "data_year": "2080",
                "male_students": 228,
                "female_students": 285,
                "name": "मा.वि., लुग्री-१",
            },
            {
                "ward_number": 1,
                "data_year": "2081",
                "male_students": 231,
                "female_students": 224,
                "name": "मा.वि., लुग्री-१",
            },
            {
                "ward_number": 1,
                "data_year": "2079",
                "male_students": 122,
                "female_students": 108,
                "name": "युबबर्ष मा.वि., लुग्री-१",
            },
            {
                "ward_number": 1,
                "data_year": "2080",
                "male_students": 103,
                "female_students": 90,
                "name": "युबबर्ष मा.वि., लुग्री-१",
            },
            {
                "ward_number": 1,
                "data_year": "2081",
                "male_students": 102,
                "female_students": 95,
                "name": "युबबर्ष मा.वि., लुग्री-१",
            },
            {
                "ward_number": 1,
                "data_year": "2079",
                "male_students": 19,
                "female_students": 17,
                "name": "बालकल्याण प्रा.वि., लुग्री-१",
            },
            {
                "ward_number": 1,
                "data_year": "2080",
                "male_students": 18,
                "female_students": 16,
                "name": "बालकल्याण प्रा.वि., लुग्री-१",
            },
            {
                "ward_number": 1,
                "data_year": "2081",
                "male_students": 13,
                "female_students": 17,
                "name": "बालकल्याण प्रा.वि., लुग्री-१",
            },
            {
                "ward_number": 1,
                "data_year": "2079",
                "male_students": 12,
                "female_students": 13,
                "name": "दोरकोट शिवालय आ.वि., लुग्री-१",
            },
            {
                "ward_number": 1,
                "data_year": "2080",
                "male_students": 8,
                "female_students": 13,
                "name": "दोरकोट शिवालय आ.वि., लुग्री-१",
            },
            {
                "ward_number": 1,
                "data_year": "2081",
                "male_students": 9,
                "female_students": 9,
                "name": "दोरकोट शिवालय आ.वि., लुग्री-१",
            },
            {
                "ward_number": 1,
                "data_year": "2079",
                "male_students": 7,
                "female_students": 8,
                "name": "दुखीचोली दोभान आ.वि., लुग्री-१",
            },
            {
                "ward_number": 1,
                "data_year": "2080",
                "male_students": 7,
                "female_students": 8,
                "name": "दुखीचोली दोभान आ.वि., लुग्री-१",
            },
            {
                "ward_number": 1,
                "data_year": "2081",
                "male_students": 5,
                "female_students": 12,
                "name": "दुखीचोली दोभान आ.वि., लुग्री-१",
            },
            {
                "ward_number": 1,
                "data_year": "2079",
                "male_students": 23,
                "female_students": 33,
                "name": "हिमाल प्रा.वि., लुग्री-१",
            },
            {
                "ward_number": 1,
                "data_year": "2080",
                "male_students": 23,
                "female_students": 33,
                "name": "हिमाल प्रा.वि., लुग्री-१",
            },
            {
                "ward_number": 1,
                "data_year": "2081",
                "male_students": 16,
                "female_students": 34,
                "name": "हिमाल प्रा.वि., लुग्री-१",
            },
            {
                "ward_number": 1,
                "data_year": "2079",
                "male_students": 62,
                "female_students": 58,
                "name": "जन कल्याण प्रा.वि., लुग्री-१",
            },
            {
                "ward_number": 1,
                "data_year": "2080",
                "male_students": 61,
                "female_students": 63,
                "name": "जन कल्याण प्रा.वि., लुग्री-१",
            },
            {
                "ward_number": 1,
                "data_year": "2081",
                "male_students": 85,
                "female_students": 69,
                "name": "जन कल्याण प्रा.वि., लुग्री-१",
            },
            {
                "ward_number": 1,
                "data_year": "2079",
                "male_students": 10,
                "female_students": 16,
                "name": "जनजागृति आ.वि., लुग्री-१",
            },
            {
                "ward_number": 1,
                "data_year": "2080",
                "male_students": 10,
                "female_students": 16,
                "name": "जनजागृति आ.वि., लुग्री-१",
            },
            {
                "ward_number": 1,
                "data_year": "2081",
                "male_students": 11,
                "female_students": 8,
                "name": "जनजागृति आ.वि., लुग्री-१",
            },
            {
                "ward_number": 1,
                "data_year": "2079",
                "male_students": 261,
                "female_students": 254,
                "name": "सरस्वती मा.वि., लुग्री-१",
            },
            {
                "ward_number": 1,
                "data_year": "2080",
                "male_students": 236,
                "female_students": 239,
                "name": "सरस्वती मा.वि., लुग्री-१",
            },
            {
                "ward_number": 1,
                "data_year": "2081",
                "male_students": 228,
                "female_students": 218,
                "name": "सरस्वती मा.वि., लुग्री-१",
            },
            {
                "ward_number": 2,
                "data_year": "2079",
                "male_students": 0,
                "female_students": 0,
                "name": "रिजनशिल आ.वि., लुग्री-२",
            },
            {
                "ward_number": 2,
                "data_year": "2080",
                "male_students": 0,
                "female_students": 0,
                "name": "रिजनशिल आ.वि., लुग्री-२",
            },
            {
                "ward_number": 2,
                "data_year": "2081",
                "male_students": 26,
                "female_students": 27,
                "name": "रिजनशिल आ.वि., लुग्री-२",
            },
            {
                "ward_number": 2,
                "data_year": "2079",
                "male_students": 195,
                "female_students": 215,
                "name": "हिमस्वेकर मा.वि., लुग्री-२",
            },
            {
                "ward_number": 2,
                "data_year": "2080",
                "male_students": 200,
                "female_students": 213,
                "name": "हिमस्वेकर मा.वि., लुग्री-२",
            },
            {
                "ward_number": 2,
                "data_year": "2081",
                "male_students": 192,
                "female_students": 213,
                "name": "हिमस्वेकर मा.वि., लुग्री-२",
            },
            {
                "ward_number": 2,
                "data_year": "2079",
                "male_students": 34,
                "female_students": 27,
                "name": "बालिकाास प्रा.वि., लुग्री-२",
            },
            {
                "ward_number": 2,
                "data_year": "2080",
                "male_students": 37,
                "female_students": 35,
                "name": "बालिकाास प्रा.वि., लुग्री-२",
            },
            {
                "ward_number": 2,
                "data_year": "2081",
                "male_students": 50,
                "female_students": 38,
                "name": "बालिकाास प्रा.वि., लुग्री-२",
            },
            {
                "ward_number": 2,
                "data_year": "2079",
                "male_students": 484,
                "female_students": 542,
                "name": "गोकुल मा.वि., लुग्री-२",
            },
            {
                "ward_number": 2,
                "data_year": "2080",
                "male_students": 412,
                "female_students": 472,
                "name": "गोकुल मा.वि., लुग्री-२",
            },
            {
                "ward_number": 2,
                "data_year": "2081",
                "male_students": 301,
                "female_students": 371,
                "name": "गोकुल मा.वि., लुग्री-२",
            },
            {
                "ward_number": 2,
                "data_year": "2079",
                "male_students": 32,
                "female_students": 21,
                "name": "जनशिक्षा प्रा.वि., लुग्री-२",
            },
            {
                "ward_number": 2,
                "data_year": "2080",
                "male_students": 31,
                "female_students": 28,
                "name": "जनशिक्षा प्रा.वि., लुग्री-२",
            },
            {
                "ward_number": 2,
                "data_year": "2081",
                "male_students": 43,
                "female_students": 36,
                "name": "जनशिक्षा प्रा.वि., लुग्री-२",
            },
            {
                "ward_number": 2,
                "data_year": "2079",
                "male_students": 19,
                "female_students": 23,
                "name": "सरस्वती प्रा.वि., लुग्री-२",
            },
            {
                "ward_number": 2,
                "data_year": "2080",
                "male_students": 19,
                "female_students": 23,
                "name": "सरस्वती प्रा.वि., लुग्री-२",
            },
            {
                "ward_number": 2,
                "data_year": "2081",
                "male_students": 24,
                "female_students": 24,
                "name": "सरस्वती प्रा.वि., लुग्री-२",
            },
            {
                "ward_number": 2,
                "data_year": "2079",
                "male_students": 49,
                "female_students": 30,
                "name": "सगरकोट प्रा.वि., लुग्री-२",
            },
            {
                "ward_number": 2,
                "data_year": "2080",
                "male_students": 41,
                "female_students": 30,
                "name": "सगरकोट प्रा.वि., लुग्री-२",
            },
            {
                "ward_number": 2,
                "data_year": "2081",
                "male_students": 29,
                "female_students": 29,
                "name": "सगरकोट प्रा.वि., लुग्री-२",
            },
            {
                "ward_number": 2,
                "data_year": "2079",
                "male_students": 184,
                "female_students": 126,
                "name": "शिवज्योति प्रा.वि., लुग्री-२",
            },
            {
                "ward_number": 2,
                "data_year": "2080",
                "male_students": 213,
                "female_students": 223,
                "name": "शिवज्योति प्रा.वि., लुग्री-२",
            },
            {
                "ward_number": 2,
                "data_year": "2081",
                "male_students": 185,
                "female_students": 179,
                "name": "शिवज्योति प्रा.वि., लुग्री-२",
            },
            {
                "ward_number": 3,
                "data_year": "2079",
                "male_students": 70,
                "female_students": 54,
                "name": "भुमिका प्रा.वि., लुग्री-३",
            },
            {
                "ward_number": 3,
                "data_year": "2080",
                "male_students": 66,
                "female_students": 51,
                "name": "भुमिका प्रा.वि., लुग्री-३",
            },
            {
                "ward_number": 3,
                "data_year": "2081",
                "male_students": 64,
                "female_students": 53,
                "name": "भुमिका प्रा.वि., लुग्री-३",
            },
            {
                "ward_number": 3,
                "data_year": "2079",
                "male_students": 80,
                "female_students": 61,
                "name": "जनजाति प्रा.वि., लुग्री-३",
            },
            {
                "ward_number": 3,
                "data_year": "2080",
                "male_students": 74,
                "female_students": 69,
                "name": "जनजाति प्रा.वि., लुग्री-३",
            },
            {
                "ward_number": 3,
                "data_year": "2081",
                "male_students": 52,
                "female_students": 54,
                "name": "जनजाति प्रा.वि., लुग्री-३",
            },
            {
                "ward_number": 3,
                "data_year": "2079",
                "male_students": 111,
                "female_students": 105,
                "name": "राष्ट्रिय प्रा.वि., लुग्री-३",
            },
            {
                "ward_number": 3,
                "data_year": "2080",
                "male_students": 122,
                "female_students": 111,
                "name": "राष्ट्रिय प्रा.वि., लुग्री-३",
            },
            {
                "ward_number": 3,
                "data_year": "2081",
                "male_students": 127,
                "female_students": 111,
                "name": "राष्ट्रिय प्रा.वि., लुग्री-३",
            },
            {
                "ward_number": 3,
                "data_year": "2079",
                "male_students": 311,
                "female_students": 331,
                "name": "सामाजिक मा.वि., लुग्री-३",
            },
            {
                "ward_number": 3,
                "data_year": "2080",
                "male_students": 319,
                "female_students": 319,
                "name": "सामाजिक मा.वि., लुग्री-३",
            },
            {
                "ward_number": 3,
                "data_year": "2081",
                "male_students": 268,
                "female_students": 216,
                "name": "सामाजिक मा.वि., लुग्री-३",
            },
            {
                "ward_number": 3,
                "data_year": "2079",
                "male_students": 16,
                "female_students": 15,
                "name": "सिस्नेनी बाालािकास आ.वि., लुग्री-३",
            },
            {
                "ward_number": 3,
                "data_year": "2080",
                "male_students": 17,
                "female_students": 14,
                "name": "सिस्नेनी बाालािकास आ.वि., लुग्री-३",
            },
            {
                "ward_number": 3,
                "data_year": "2081",
                "male_students": 24,
                "female_students": 20,
                "name": "सिस्नेनी बाालािकास आ.वि., लुग्री-३",
            },
            {
                "ward_number": 4,
                "data_year": "2079",
                "male_students": 162,
                "female_students": 208,
                "name": "विजयश्वरी मा.वि., लुग्री-४",
            },
            {
                "ward_number": 4,
                "data_year": "2080",
                "male_students": 176,
                "female_students": 203,
                "name": "विजयश्वरी मा.वि., लुग्री-४",
            },
            {
                "ward_number": 4,
                "data_year": "2081",
                "male_students": 186,
                "female_students": 181,
                "name": "विजयश्वरी मा.वि., लुग्री-४",
            },
            {
                "ward_number": 4,
                "data_year": "2079",
                "male_students": 319,
                "female_students": 281,
                "name": "गौरी शंकर मा.वि., लुग्री-४",
            },
            {
                "ward_number": 4,
                "data_year": "2080",
                "male_students": 301,
                "female_students": 309,
                "name": "गौरी शंकर मा.वि., लुग्री-४",
            },
            {
                "ward_number": 4,
                "data_year": "2081",
                "male_students": 284,
                "female_students": 267,
                "name": "गौरी शंकर मा.वि., लुग्री-४",
            },
            {
                "ward_number": 4,
                "data_year": "2079",
                "male_students": 54,
                "female_students": 48,
                "name": "बाल कल्याण प्रा.वि., लुग्री-४",
            },
            {
                "ward_number": 4,
                "data_year": "2080",
                "male_students": 65,
                "female_students": 55,
                "name": "बाल कल्याण प्रा.वि., लुग्री-४",
            },
            {
                "ward_number": 4,
                "data_year": "2081",
                "male_students": 77,
                "female_students": 52,
                "name": "बाल कल्याण प्रा.वि., लुग्री-४",
            },
            {
                "ward_number": 4,
                "data_year": "2079",
                "male_students": 53,
                "female_students": 53,
                "name": "बालज्योति प्रा.वि., लुग्री-४",
            },
            {
                "ward_number": 4,
                "data_year": "2080",
                "male_students": 49,
                "female_students": 39,
                "name": "बालज्योति प्रा.वि., लुग्री-४",
            },
            {
                "ward_number": 4,
                "data_year": "2081",
                "male_students": 40,
                "female_students": 36,
                "name": "बालज्योति प्रा.वि., लुग्री-४",
            },
            {
                "ward_number": 4,
                "data_year": "2079",
                "male_students": 48,
                "female_students": 37,
                "name": "शहिदस्मृति प्रा.वि., लुग्री-४",
            },
            {
                "ward_number": 4,
                "data_year": "2080",
                "male_students": 46,
                "female_students": 39,
                "name": "शहिदस्मृति प्रा.वि., लुग्री-४",
            },
            {
                "ward_number": 4,
                "data_year": "2081",
                "male_students": 35,
                "female_students": 34,
                "name": "शहिदस्मृति प्रा.वि., लुग्री-४",
            },
            {
                "ward_number": 4,
                "data_year": "2079",
                "male_students": 324,
                "female_students": 421,
                "name": "बराहक्षेत्र मा.वि., लुग्री-४",
            },
            {
                "ward_number": 4,
                "data_year": "2080",
                "male_students": 331,
                "female_students": 441,
                "name": "बराहक्षेत्र मा.वि., लुग्री-४",
            },
            {
                "ward_number": 4,
                "data_year": "2081",
                "male_students": 266,
                "female_students": 333,
                "name": "बराहक्षेत्र मा.वि., लुग्री-४",
            },
            {
                "ward_number": 4,
                "data_year": "2079",
                "male_students": 72,
                "female_students": 64,
                "name": "जनता प्रा.वि., लुग्री-४",
            },
            {
                "ward_number": 4,
                "data_year": "2080",
                "male_students": 68,
                "female_students": 67,
                "name": "जनता प्रा.वि., लुग्री-४",
            },
            {
                "ward_number": 4,
                "data_year": "2081",
                "male_students": 51,
                "female_students": 52,
                "name": "जनता प्रा.वि., लुग्री-४",
            },
            {
                "ward_number": 4,
                "data_year": "2079",
                "male_students": 144,
                "female_students": 167,
                "name": "ज्योति आ.वि., लुग्री-४",
            },
            {
                "ward_number": 4,
                "data_year": "2080",
                "male_students": 136,
                "female_students": 143,
                "name": "ज्योति आ.वि., लुग्री-४",
            },
            {
                "ward_number": 4,
                "data_year": "2081",
                "male_students": 136,
                "female_students": 140,
                "name": "ज्योति आ.वि., लुग्री-४",
            },
            {
                "ward_number": 4,
                "data_year": "2079",
                "male_students": 78,
                "female_students": 69,
                "name": "शिशु कल्याण प्रा.वि., लुग्री-४",
            },
            {
                "ward_number": 4,
                "data_year": "2080",
                "male_students": 70,
                "female_students": 64,
                "name": "शिशु कल्याण प्रा.वि., लुग्री-४",
            },
            {
                "ward_number": 4,
                "data_year": "2081",
                "male_students": 61,
                "female_students": 64,
                "name": "शिशु कल्याण प्रा.वि., लुग्री-४",
            },
            {
                "ward_number": 6,
                "data_year": "2079",
                "male_students": 301,
                "female_students": 385,
                "name": "जनज्योति मा.वि., लुग्री-६",
            },
            {
                "ward_number": 6,
                "data_year": "2080",
                "male_students": 304,
                "female_students": 344,
                "name": "जनज्योति मा.वि., लुग्री-६",
            },
            {
                "ward_number": 6,
                "data_year": "2081",
                "male_students": 244,
                "female_students": 283,
                "name": "जनज्योति मा.वि., लुग्री-६",
            },
            {
                "ward_number": 6,
                "data_year": "2079",
                "male_students": 0,
                "female_students": 0,
                "name": "जनचेतना बाालािकास आ.वि., लुग्री-६",
            },
            {
                "ward_number": 6,
                "data_year": "2080",
                "male_students": 0,
                "female_students": 0,
                "name": "जनचेतना बाालािकास आ.वि., लुग्री-६",
            },
            {
                "ward_number": 6,
                "data_year": "2081",
                "male_students": 12,
                "female_students": 11,
                "name": "जनचेतना बाालािकास आ.वि., लुग्री-६",
            },
            {
                "ward_number": 6,
                "data_year": "2079",
                "male_students": 183,
                "female_students": 184,
                "name": "ज्योति आ.वि., लुग्री-६",
            },
            {
                "ward_number": 6,
                "data_year": "2080",
                "male_students": 166,
                "female_students": 169,
                "name": "ज्योति आ.वि., लुग्री-६",
            },
            {
                "ward_number": 6,
                "data_year": "2081",
                "male_students": 140,
                "female_students": 143,
                "name": "ज्योति आ.वि., लुग्री-६",
            },
            {
                "ward_number": 6,
                "data_year": "2079",
                "male_students": 20,
                "female_students": 15,
                "name": "नमुना बाल प्रा.वि., लुग्री-६",
            },
            {
                "ward_number": 6,
                "data_year": "2080",
                "male_students": 33,
                "female_students": 28,
                "name": "नमुना बाल प्रा.वि., लुग्री-६",
            },
            {
                "ward_number": 6,
                "data_year": "2081",
                "male_students": 12,
                "female_students": 16,
                "name": "नमुना बाल प्रा.वि., लुग्री-६",
            },
            {
                "ward_number": 6,
                "data_year": "2079",
                "male_students": 170,
                "female_students": 184,
                "name": "नेपाल राष्ट्रिय मा.वि., लुग्री-६",
            },
            {
                "ward_number": 6,
                "data_year": "2080",
                "male_students": 175,
                "female_students": 175,
                "name": "नेपाल राष्ट्रिय मा.वि., लुग्री-६",
            },
            {
                "ward_number": 6,
                "data_year": "2081",
                "male_students": 188,
                "female_students": 177,
                "name": "नेपाल राष्ट्रिय मा.वि., लुग्री-६",
            },
            {
                "ward_number": 6,
                "data_year": "2079",
                "male_students": 0,
                "female_students": 0,
                "name": "शिवशक्ति ईङ्लिस बोर्डिङ, लुग्री-६",
            },
            {
                "ward_number": 6,
                "data_year": "2080",
                "male_students": 90,
                "female_students": 60,
                "name": "शिवशक्ति ईङ्लिस बोर्डिङ, लुग्री-६",
            },
            {
                "ward_number": 6,
                "data_year": "2081",
                "male_students": 98,
                "female_students": 62,
                "name": "शिवशक्ति ईङ्लिस बोर्डिङ, लुग्री-६",
            },
            {
                "ward_number": 7,
                "data_year": "2079",
                "male_students": 245,
                "female_students": 205,
                "name": "नेपाल राष्ट्रिय मा.वि., लुग्री-७",
            },
            {
                "ward_number": 7,
                "data_year": "2080",
                "male_students": 237,
                "female_students": 207,
                "name": "नेपाल राष्ट्रिय मा.वि., लुग्री-७",
            },
            {
                "ward_number": 7,
                "data_year": "2081",
                "male_students": 235,
                "female_students": 216,
                "name": "नेपाल राष्ट्रिय मा.वि., लुग्री-७",
            },
            {
                "ward_number": 7,
                "data_year": "2079",
                "male_students": 125,
                "female_students": 104,
                "name": "फुलवारी प्रा.वि., लुग्री-७",
            },
            {
                "ward_number": 7,
                "data_year": "2080",
                "male_students": 124,
                "female_students": 101,
                "name": "फुलवारी प्रा.वि., लुग्री-७",
            },
            {
                "ward_number": 7,
                "data_year": "2081",
                "male_students": 103,
                "female_students": 85,
                "name": "फुलवारी प्रा.वि., लुग्री-७",
            },
            {
                "ward_number": 7,
                "data_year": "2079",
                "male_students": 0,
                "female_students": 0,
                "name": "जलवराह बा.वि.के., लुग्री-७",
            },
            {
                "ward_number": 7,
                "data_year": "2080",
                "male_students": 9,
                "female_students": 5,
                "name": "जलवराह बा.वि.के., लुग्री-७",
            },
            {
                "ward_number": 7,
                "data_year": "2081",
                "male_students": 10,
                "female_students": 8,
                "name": "जलवराह बा.वि.के., लुग्री-७",
            },
            {
                "ward_number": 7,
                "data_year": "2079",
                "male_students": 16,
                "female_students": 16,
                "name": "ज्योति प्रा.वि., लुग्री-७",
            },
            {
                "ward_number": 7,
                "data_year": "2080",
                "male_students": 21,
                "female_students": 12,
                "name": "ज्योति प्रा.वि., लुग्री-७",
            },
            {
                "ward_number": 7,
                "data_year": "2081",
                "male_students": 14,
                "female_students": 10,
                "name": "ज्योति प्रा.वि., लुग्री-७",
            },
            {
                "ward_number": 7,
                "data_year": "2079",
                "male_students": 7,
                "female_students": 9,
                "name": "लालज्योति आ.वि., लुग्री-७",
            },
            {
                "ward_number": 7,
                "data_year": "2080",
                "male_students": 0,
                "female_students": 0,
                "name": "लालज्योति आ.वि., लुग्री-७",
            },
            {
                "ward_number": 7,
                "data_year": "2081",
                "male_students": 7,
                "female_students": 7,
                "name": "लालज्योति आ.वि., लुग्री-७",
            },
        ]

        created_count = 0
        updated_count = 0

        with transaction.atomic():
            for data in sample_data:
                institution, created = (
                    WardWiseEducationalInstitution.objects.get_or_create(
                        ward_number=data["ward_number"],
                        data_year=data["data_year"],
                        institution_name=data["name"],
                        defaults={
                            "male_students": data["male_students"],
                            "female_students": data["female_students"],
                            "institution_type": EducationalInstitutionTypeChoice.COMMUNITY_SCHOOL,
                            "is_operational": (
                                True
                                if (data["male_students"] + data["female_students"]) > 0
                                else False
                            ),
                        },
                    )
                )

                if created:
                    created_count += 1
                    self.stdout.write(f"✓ Created: {institution}")
                else:
                    # Update existing record
                    institution.male_students = data["male_students"]
                    institution.female_students = data["female_students"]
                    institution.is_operational = (
                        True
                        if (data["male_students"] + data["female_students"]) > 0
                        else False
                    )
                    institution.save()
                    updated_count += 1
                    self.stdout.write(f"↻ Updated: {institution}")

        self.stdout.write("\n" + "=" * 70)
        self.stdout.write(
            self.style.SUCCESS("📊 EDUCATIONAL INSTITUTION DATA CREATION COMPLETED")
        )
        self.stdout.write("=" * 70)
        self.stdout.write(
            f"📝 Total records created: {to_nepali_digits(str(created_count))}"
        )
        self.stdout.write(
            f"🔄 Total records updated: {to_nepali_digits(str(updated_count))}"
        )
        self.stdout.write(
            f"📁 Total records processed: {to_nepali_digits(str(created_count + updated_count))}"
        )

        # Generate summary
        self.generate_summary()

    def generate_summary(self):
        """Generate and display summary statistics"""
        from django.db.models import Sum, Count, Avg

        self.stdout.write("\n" + "📈 SUMMARY STATISTICS")
        self.stdout.write("-" * 50)

        # Overall statistics
        total_institutions = WardWiseEducationalInstitution.objects.count()
        total_male_students = (
            WardWiseEducationalInstitution.objects.aggregate(Sum("male_students"))[
                "male_students__sum"
            ]
            or 0
        )
        total_female_students = (
            WardWiseEducationalInstitution.objects.aggregate(Sum("female_students"))[
                "female_students__sum"
            ]
            or 0
        )
        total_students = total_male_students + total_female_students

        self.stdout.write(
            f"🏫 कुल शैक्षिक संस्थाहरू: {to_nepali_digits(str(total_institutions))}"
        )
        self.stdout.write(
            f"👨‍🎓 कुल पुरुष विद्यार्थी: {to_nepali_digits(str(total_male_students))}"
        )
        self.stdout.write(
            f"👩‍🎓 कुल महिला विद्यार्थी: {to_nepali_digits(str(total_female_students))}"
        )
        self.stdout.write(
            f"📚 कुल विद्यार्थी संख्या: {to_nepali_digits(str(total_students))}"
        )

        if total_students > 0:
            gender_ratio = round((total_female_students / total_students) * 100, 1)
            self.stdout.write(
                f"⚖️ लैङ्गिक अनुपात (महिला %): {to_nepali_digits(str(gender_ratio))}%"
            )

        # Ward-wise summary
        self.stdout.write("\n🗺️ वडागत सारांश:")
        for ward_num in range(1, 8):
            ward_institutions = WardWiseEducationalInstitution.objects.filter(
                ward_number=ward_num
            )
            if ward_institutions.exists():
                ward_total_students = ward_institutions.aggregate(
                    male_sum=Sum("male_students"), female_sum=Sum("female_students")
                )
                ward_male = ward_total_students["male_sum"] or 0
                ward_female = ward_total_students["female_sum"] or 0
                ward_total = ward_male + ward_female
                ward_institution_count = (
                    ward_institutions.values("institution_name").distinct().count()
                )

                self.stdout.write(
                    f"   वडा {to_nepali_digits(str(ward_num))}: "
                    f"{to_nepali_digits(str(ward_institution_count))} संस्था, "
                    f"{to_nepali_digits(str(ward_total))} विद्यार्थी"
                )

        self.stdout.write("\n✅ Data creation completed successfully!")
