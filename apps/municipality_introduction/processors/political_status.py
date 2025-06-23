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
        """Get political status population data"""
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
                    "population": status_obj.population,
                    "year": status_obj.year,
                }
            )

        return political_data

    def generate_report_content(self, data):
        """Generate report content for political status"""

        # Calculate totals
        total_records = sum(len(year_data) for year_data in data.values())

        # The main analysis text as requested
        analysis_text = """गाउँपालिकाको भौतिक अवस्थाको विवरण तयार पार्दा यहाँको धरातलीय अवस्थाका बारेमा उल्लेख गर्नु अनिवार्य हुन्छ । क्षेत्रफलका हिसाबले सानो भए तापनि नेपाल धरातलीय विविधताका हिसाबले विश्वमै सम्पन्न मानिन्छ । विशेषतः भौगर्भिक प्रक्रियाका दौरान पछिल्लो समयमा निर्माण भएको महालङ्गुर हिमश्रृंखला निर्माण हुँदा तिब्बतीयन भू–खण्ड र भारतीय उपमहाद्वीपको एक आपसमा टकराव हुँदा यी दुई भू–खण्डका बिचमा रहेको टेथिस सागरको अस्तित्व समाप्त भई उच्च हिमालय पर्वत, मध्यम महाभारत पर्वत श्रृंखला तथा होचा चुरे पर्वत श्रृंखला र सबैभन्दा दक्षिण भेगमा फैलिएको विशाल गंगाको मैदानको अंशको रुपमा रहेको तराई भू–भाग मिलेर समग्र देशको भू–सतह निर्माण भएको छ । यो भू–धरातलको वस्तुगत चरित्रहरू मध्ये एक वा अर्को प्रकारको भू–धरातलको प्रधानता नेपालका गाउँपालिका वा नगरपालिकामा रहेको पाईन्छ । यस अनुसार गढवाे गाउँपालिकाको सम्पूर्ण भू–भाग मध्ये पहाडी खण्डमा अवस्थित छ ।

भू–धरातलीय स्वरुपले विकास निर्माणमा अहम् भूमिका खेल्दछ । भू–धरातलको विवरण अन्तर्गत विशेषतः भिरालोपन, मोहडा, उचाई, भू–आवरण, माटोको बनावट जस्ता आधारभूत पक्षहरू पर्दछन् ।"""

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
