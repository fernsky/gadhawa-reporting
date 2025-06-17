"""
Economically Active Population Demographics Processor

Handles economically active population demographic data processing, chart generation, and report formatting.
"""

import subprocess
from django.db import models
from .base import BaseDemographicsProcessor, BaseReportFormatter
from ..models import (
    WardAgeWiseEconomicallyActivePopulation,
    EconomicallyActiveAgeGroupChoice,
    GenderChoice,
)
from ..utils.svg_chart_generator import DEFAULT_COLORS
from apps.reports.utils.nepali_numbers import (
    format_nepali_number,
    format_nepali_percentage,
)


class EconomicallyActiveProcessor(BaseDemographicsProcessor):
    """Processor for economically active population demographics"""

    def __init__(self):
        super().__init__()
        # Customize chart dimensions for economically active population
        self.pie_chart_width = 800
        self.pie_chart_height = 400
        self.chart_radius = 120
        # Set age group-specific colors
        self.chart_generator.colors = {
            "AGE_0_TO_14": "#FFB6C1",  # Light Pink
            "AGE_15_TO_59": "#32CD32",  # Lime Green
            "AGE_60_PLUS": "#4169E1",  # Royal Blue
            "MALE": "#1E90FF",  # Dodger Blue
            "FEMALE": "#FF1493",  # Deep Pink
        }

    def get_section_title(self):
        return "आर्थिक रूपले सक्रिय जनसंख्या विवरण"

    def get_section_number(self):
        return "३.९"

    def get_data(self):
        """Get economically active population data - both municipality-wide and ward-wise"""
        # Municipality-wide summary by age group
        age_group_data = {}
        total_population = 0

        for age_choice in EconomicallyActiveAgeGroupChoice.choices:
            age_code = age_choice[0]
            age_name = age_choice[1]

            age_population = (
                WardAgeWiseEconomicallyActivePopulation.objects.filter(
                    age_group=age_code
                ).aggregate(total=models.Sum("population"))["total"]
                or 0
            )

            age_group_data[age_code] = {
                "name_english": age_code,
                "name_nepali": age_name,
                "population": age_population,
                "percentage": 0,  # Will be calculated below
            }
            total_population += age_population

        # Calculate percentages
        for age_code in age_group_data:
            if total_population > 0:
                age_group_data[age_code]["percentage"] = (
                    age_group_data[age_code]["population"] / total_population * 100
                )

        # Municipality-wide summary by gender
        gender_data = {}

        for gender_choice in GenderChoice.choices:
            gender_code = gender_choice[0]
            gender_name = gender_choice[1]

            gender_population = (
                WardAgeWiseEconomicallyActivePopulation.objects.filter(
                    gender=gender_code
                ).aggregate(total=models.Sum("population"))["total"]
                or 0
            )

            if gender_population > 0:  # Only include genders with population
                gender_data[gender_code] = {
                    "name_english": gender_code,
                    "name_nepali": gender_name,
                    "population": gender_population,
                    "percentage": (
                        (gender_population / total_population * 100)
                        if total_population > 0
                        else 0
                    ),
                }

        # Ward-wise data
        ward_data = {}
        for ward_num in range(1, 8):  # Wards 1-7
            ward_population = (
                WardAgeWiseEconomicallyActivePopulation.objects.filter(
                    ward_number=ward_num
                ).aggregate(total=models.Sum("population"))["total"]
                or 0
            )

            if ward_population > 0:
                ward_data[ward_num] = {
                    "ward_number": ward_num,
                    "ward_name": f"वडा नं. {ward_num}",
                    "total_population": ward_population,
                    "age_groups": {},
                    "genders": {},
                }

                # Age group breakdown for this ward
                for age_choice in EconomicallyActiveAgeGroupChoice.choices:
                    age_code = age_choice[0]
                    age_name = age_choice[1]

                    age_pop = (
                        WardAgeWiseEconomicallyActivePopulation.objects.filter(
                            ward_number=ward_num, age_group=age_code
                        ).aggregate(total=models.Sum("population"))["total"]
                        or 0
                    )

                    if age_pop > 0:
                        ward_data[ward_num]["age_groups"][age_code] = {
                            "name_nepali": age_name,
                            "population": age_pop,
                            "percentage": (
                                (age_pop / ward_population * 100)
                                if ward_population > 0
                                else 0
                            ),
                        }

                # Gender breakdown for this ward
                for gender_choice in GenderChoice.choices:
                    gender_code = gender_choice[0]
                    gender_name = gender_choice[1]

                    gender_pop = (
                        WardAgeWiseEconomicallyActivePopulation.objects.filter(
                            ward_number=ward_num, gender=gender_code
                        ).aggregate(total=models.Sum("population"))["total"]
                        or 0
                    )

                    if gender_pop > 0:
                        ward_data[ward_num]["genders"][gender_code] = {
                            "name_nepali": gender_name,
                            "population": gender_pop,
                            "percentage": (
                                (gender_pop / ward_population * 100)
                                if ward_population > 0
                                else 0
                            ),
                        }

        return {
            "age_group_data": age_group_data,
            "gender_data": gender_data,
            "ward_data": ward_data,
            "total_population": total_population,
        }

    def generate_analysis_text(self, data):
        """Generate coherent analysis text for economically active population"""
        if not data or data["total_population"] == 0:
            return "आर्थिक रूपले सक्रिय जनसंख्याको तथ्याङ्क उपलब्ध छैन।"

        total_pop = data["total_population"]
        age_group_data = data["age_group_data"]
        gender_data = data["gender_data"]
        ward_data = data["ward_data"]

        analysis_parts = []

        # Overall summary
        analysis_parts.append(
            f"लुङ्ग्री गाउँपालिकामा कुल {format_nepali_number(total_pop)} जना आर्थिक रूपले सक्रिय जनसंख्या रहेको छ।"
        )

        # Age group analysis
        if age_group_data:
            # Find the most dominant age group
            dominant_age = max(age_group_data.items(), key=lambda x: x[1]["population"])
            analysis_parts.append(
                f"उमेर समूहको आधारमा हेर्दा, {dominant_age[1]['name_nepali']} उमेर समूहमा सबैभन्दा बढी "
                f"{format_nepali_number(dominant_age[1]['population'])} जना "
                f"({format_nepali_percentage(dominant_age[1]['percentage'])}) आर्थिक रूपले सक्रिय जनसंख्या रहेको छ।"
            )

            # Working age population (15-59)
            if "AGE_15_TO_59" in age_group_data:
                working_age = age_group_data["AGE_15_TO_59"]
                analysis_parts.append(
                    f"कामदार उमेर समूह (१५-५९ वर्ष) मा {format_nepali_number(working_age['population'])} जना "
                    f"({format_nepali_percentage(working_age['percentage'])}) आर्थिक रूपले सक्रिय छन्।"
                )

        # Gender analysis
        if gender_data and len(gender_data) >= 2:
            male_pop = gender_data.get("MALE", {}).get("population", 0)
            female_pop = gender_data.get("FEMALE", {}).get("population", 0)

            if male_pop > 0 and female_pop > 0:
                if male_pop > female_pop:
                    analysis_parts.append(
                        f"लिङ्गको आधारमा हेर्दा, पुरुषको संख्या {format_nepali_number(male_pop)} जना "
                        f"({format_nepali_percentage(gender_data['MALE']['percentage'])}) र "
                        f"महिलाको संख्या {format_nepali_number(female_pop)} जना "
                        f"({format_nepali_percentage(gender_data['FEMALE']['percentage'])}) रहेको छ।"
                    )
                else:
                    analysis_parts.append(
                        f"लिङ्गको आधारमा हेर्दा, महिलाको संख्या {format_nepali_number(female_pop)} जना "
                        f"({format_nepali_percentage(gender_data['FEMALE']['percentage'])}) र "
                        f"पुरुषको संख्या {format_nepali_number(male_pop)} जना "
                        f"({format_nepali_percentage(gender_data['MALE']['percentage'])}) रहेको छ।"
                    )

        # Ward-wise analysis
        if ward_data:
            # Find wards with highest and lowest population
            highest_ward = max(
                ward_data.items(), key=lambda x: x[1]["total_population"]
            )
            lowest_ward = min(ward_data.items(), key=lambda x: x[1]["total_population"])

            analysis_parts.append(
                f"वडाको आधारमा हेर्दा, वडा नं. {highest_ward[0]} मा सबैभन्दा बढी "
                f"{format_nepali_number(highest_ward[1]['total_population'])} जना आर्थिक रूपले सक्रिय जनसंख्या छ "
                f"भने वडा नं. {lowest_ward[0]} मा सबैभन्दा कम "
                f"{format_nepali_number(lowest_ward[1]['total_population'])} जना छ।"
            )

        # Additional insights
        analysis_parts.append(
            "यो तथ्याङ्कले गाउँपालिकाको श्रमशक्तिको उपलब्धता र उत्पादक उमेर समूहको वितरणलाई प्रतिनिधित्व गर्दछ।"
        )

        return " ".join(analysis_parts)

    def generate_report_content(self, data):
        """Generate report content specific to economically active population"""
        return self.generate_analysis_text(data)

    def generate_pie_chart(self, data, title="आर्थिक रूपले सक्रिय जनसंख्या - उमेर समूह अनुसार"):
        """Generate pie chart for age group distribution"""
        if not data or not data["age_group_data"]:
            return None

        # Prepare data for chart in the format expected by SVGChartGenerator
        chart_data = {}
        for age_code, age_info in data["age_group_data"].items():
            if age_info["population"] > 0:
                chart_data[age_code] = {
                    "population": age_info["population"],
                    "name_nepali": age_info["name_nepali"],
                }

        if not chart_data:
            return None

        return self.chart_generator.generate_pie_chart_svg(
            demographic_data=chart_data,
            include_title=False,
            title_nepali=title,
            title_english="",
        )

    def process_for_pdf(self):
        """Process data for PDF generation"""
        data = self.get_data()

        # Generate analysis text
        coherent_analysis = self.generate_analysis_text(data)

        # Generate pie chart
        pie_chart_svg = self.generate_pie_chart(data)

        # Prepare chart data for template
        pdf_charts = {
            "economically_active": {
                "pie_chart_svg": pie_chart_svg,
                "pie_chart_png": None,  # Can be generated if needed
            }
        }

        return {
            "age_group_data": data["age_group_data"],
            "gender_data": data["gender_data"],
            "ward_data": data["ward_data"],
            "total_population": data["total_population"],
            "coherent_analysis": coherent_analysis,
            "pdf_charts": pdf_charts,
            "section_title": self.get_section_title(),
            "section_number": self.get_section_number(),
        }


class EconomicallyActiveReportFormatter(BaseReportFormatter):
    """Report formatter for economically active population demographics"""

    def __init__(self, processor_data):
        super().__init__(processor_data)

    def format_for_html(self):
        """Format data for HTML template rendering"""
        return {
            "age_group_data": self.data["age_group_data"],
            "gender_data": self.data["gender_data"],
            "ward_data": self.data["ward_data"],
            "total_population": self.data["total_population"],
            "coherent_analysis": self.data["coherent_analysis"],
            "pdf_charts": self.data["pdf_charts"],
        }

    def format_for_api(self):
        """Format data for API response"""
        return {
            "section": self.data["section_number"],
            "title": self.data["section_title"],
            "summary": {
                "total_population": self.data["total_population"],
                "age_groups": len(self.data["age_group_data"]),
                "wards": len(self.data["ward_data"]),
            },
            "age_group_breakdown": self.data["age_group_data"],
            "gender_breakdown": self.data["gender_data"],
            "ward_breakdown": self.data["ward_data"],
            "analysis": self.data["coherent_analysis"],
        }
