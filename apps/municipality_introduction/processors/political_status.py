"""
Political Status Processor

Handles political status data processing, chart generation, and report formatting.
"""

from pathlib import Path
from .base import BaseMunicipalityIntroductionProcessor
from ..models import PoliticalStatus
from apps.reports.utils.nepali_numbers import format_nepali_number


class PoliticalStatusProcessor(BaseMunicipalityIntroductionProcessor):
    """Processor for political status demographics"""

    def __init__(self):
        super().__init__()

    def get_chart_key(self):
        return "political_status"

    def get_section_title(self):
        return "राजनैतिक अवस्था"

    def get_section_number(self):
        return "२.३"

    def get_data(self):
        """Get political status population data with all demographic fields"""
        political_data = {}

        # Get all data from database grouped by year
        for status_obj in PoliticalStatus.objects.all().order_by("year", "ward_number"):
            year = str(status_obj.year)
            if year not in political_data:
                political_data[year] = []

            political_data[year].append(
                {
                    "ward_number": status_obj.ward_number,
                    "ward_name": status_obj.ward_name,
                    "total_population": getattr(status_obj, "total_population", None),
                    "male_population": getattr(status_obj, "male_population", None),
                    "female_population": getattr(status_obj, "female_population", None),
                    "other_population": getattr(status_obj, "other_population", None),
                    "total_households": getattr(status_obj, "total_households", None),
                    "average_household_size": getattr(
                        status_obj, "average_household_size", None
                    ),
                    "sex_ratio": getattr(status_obj, "sex_ratio", None),
                    "year": status_obj.year,
                }
            )

        return political_data

    def generate_report_content(self, data):
        """Generate report content for political status with demographic explanation"""

        # Calculate totals
        total_records = sum(len(year_data) for year_data in data.values())

        # The main analysis text as requested
        analysis_text = (
            "यस तालिकामा प्रत्येक वडाको कुल जनसंख्या, पुरुष/महिला जनसंख्या, घरपरिवार संख्या, औसत घरपरिवार आकार, र लिंगानुपात (sex ratio) को विवरण समावेश गरिएको छ। "
            "यसले वडागत जनसंख्या संरचना, घरपरिवारको औसत आकार, र लिंगानुपातको अवस्थाबारे स्पष्ट जानकारी दिन्छ। "
            "यस विवरणको आधारमा सामाजिक, शैक्षिक, तथा विकासका कार्यक्रमहरूलाई लक्षित गर्न सकिन्छ।"
        )

        return analysis_text

    def generate_chart_svg(self, data, chart_type="pie"):
        """Generate chart SVG - not needed for political status"""
        return None

    def generate_and_save_charts(self, data):
        """Generate and save charts - not needed for political status"""
        return {}

    def process_for_pdf(self):
        """Process political status data for PDF generation"""
        # Get raw data
        data = self.get_data()
        # Generate report content
        report_content = self.generate_report_content(data)

        # Calculate total population across all years and wards
        total_population = 0
        for year_data in data.values():
            for ward_data in year_data:
                total_population += ward_data["population"]

        return {
            "data": data,
            "report_content": report_content,
            "charts": {},
            "total_population": total_population,
            "section_title": self.get_section_title(),
            "section_number": self.get_section_number(),
        }
