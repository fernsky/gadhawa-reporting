"""
Old Age Population and Single Women Social Processor

Handles old age population and single women data processing, chart generation, and report formatting.
"""

from django.db import models
from .base import BaseSocialProcessor, BaseSocialReportFormatter
from ..models import WardWiseOldAgePopulationAndSingleWomen
from apps.reports.utils.nepali_numbers import (
    format_nepali_number,
    format_nepali_percentage,
    to_nepali_digits,
)


class OldAgeAndSingleWomenProcessor(BaseSocialProcessor):
    """Processor for old age population and single women data"""

    def __init__(self):
        super().__init__()
        # Customize chart dimensions for old age and single women data
        self.pie_chart_width = 900
        self.pie_chart_height = 500
        self.bar_chart_width = 1000
        self.bar_chart_height = 600
        self.chart_radius = 150

        # Set specific colors for different demographics
        self.chart_generator.colors = {
            "male_old_age": "#2196F3",  # Blue - Male elderly
            "female_old_age": "#E91E63",  # Pink - Female elderly
            "single_women": "#FF9800",  # Orange - Single women
            "total_old_age": "#4CAF50",  # Green - Total elderly
        }

    def get_section_title(self):
        return "जेष्ठ नागरिक तथा एकल महिला"

    def get_section_number(self):
        return "५.४.१०"

    def get_data(self):
        """Get old age population and single women data"""
        # Get all ward data
        ward_data = {}
        total_male_old_age = 0
        total_female_old_age = 0
        total_single_women = 0

        for ward_num in range(1, 8):  # Wards 1-7
            try:
                ward_obj = WardWiseOldAgePopulationAndSingleWomen.objects.get(
                    ward_number=ward_num
                )

                ward_data[ward_num] = {
                    "ward_number": ward_num,
                    "ward_name": f"वडा नं. {to_nepali_digits(ward_num)}",
                    "total_population": ward_obj.total_old_age_population
                    + ward_obj.single_women_population,
                    "demographics": {
                        "male_old_age": {
                            "name_nepali": "पुरुष जेष्ठ नागरिक",
                            "population": ward_obj.male_old_age_population,
                            "percentage": (
                                (
                                    ward_obj.male_old_age_population
                                    / ward_obj.total_old_age_population
                                    * 100
                                )
                                if ward_obj.total_old_age_population > 0
                                else 0
                            ),
                        },
                        "female_old_age": {
                            "name_nepali": "महिला जेष्ठ नागरिक",
                            "population": ward_obj.female_old_age_population,
                            "percentage": (
                                (
                                    ward_obj.female_old_age_population
                                    / ward_obj.total_old_age_population
                                    * 100
                                )
                                if ward_obj.total_old_age_population > 0
                                else 0
                            ),
                        },
                        "single_women": {
                            "name_nepali": "एकल महिला",
                            "population": ward_obj.single_women_population,
                            "percentage": 0,  # Separate category
                        },
                    },
                }

                total_male_old_age += ward_obj.male_old_age_population
                total_female_old_age += ward_obj.female_old_age_population
                total_single_women += ward_obj.single_women_population

            except WardWiseOldAgePopulationAndSingleWomen.DoesNotExist:
                # Skip wards with no data
                continue

        # Municipality-wide summary
        total_old_age_population = total_male_old_age + total_female_old_age

        municipality_data = {}

        if total_old_age_population > 0:
            municipality_data = {
                "male_old_age": {
                    "name_nepali": "पुरुष जेष्ठ नागरिक",
                    "name_english": "Male Elderly",
                    "population": total_male_old_age,
                    "percentage": (
                        (total_male_old_age / total_old_age_population * 100)
                        if total_old_age_population > 0
                        else 0
                    ),
                },
                "female_old_age": {
                    "name_nepali": "महिला जेष्ठ नागरिक",
                    "name_english": "Female Elderly",
                    "population": total_female_old_age,
                    "percentage": (
                        (total_female_old_age / total_old_age_population * 100)
                        if total_old_age_population > 0
                        else 0
                    ),
                },
            }

        # Single women data (separate from elderly comparison)
        single_women_data = {
            "single_women": {
                "name_nepali": "एकल महिला",
                "name_english": "Single Women",
                "population": total_single_women,
            }
        }

        return {
            "municipality_data": municipality_data,
            "single_women_data": single_women_data,
            "ward_data": ward_data,
            "total_male_old_age": total_male_old_age,
            "total_female_old_age": total_female_old_age,
            "total_old_age_population": total_old_age_population,
            "total_single_women": total_single_women,
        }

    def generate_analysis_text(self, data):
        """Generate comprehensive analysis text for old age population and single women"""
        if not data or data["total_old_age_population"] == 0:
            return "जेष्ठ नागरिक तथा एकल महिलाको तथ्याङ्क उपलब्ध छैन।"

        total_old_age = data["total_old_age_population"]
        total_male_old_age = data["total_male_old_age"]
        total_female_old_age = data["total_female_old_age"]
        total_single_women = data["total_single_women"]
        ward_data = data["ward_data"]

        analysis_parts = []

        # Overall summary
        analysis_parts.append(
            f"लुङ्ग्री गाउँपालिकामा कुल {format_nepali_number(total_old_age)} जना जेष्ठ नागरिकहरू छन्। "
            f"यसमध्ये {format_nepali_number(total_male_old_age)} जना पुरुष र "
            f"{format_nepali_number(total_female_old_age)} जना महिला जेष्ठ नागरिकहरू छन्।"
        )

        # Gender distribution analysis
        if total_old_age > 0:
            male_percentage = total_male_old_age / total_old_age * 100
            female_percentage = total_female_old_age / total_old_age * 100

            analysis_parts.append(
                f"लैङ्गिक वितरणको आधारमा विश्लेषण गर्दा, पुरुष जेष्ठ नागरिकहरूको संख्या "
                f"{format_nepali_percentage(male_percentage)}% र महिला जेष्ठ नागरिकहरूको संख्या "
                f"{format_nepali_percentage(female_percentage)}% रहेको छ।"
            )

            # Gender gap analysis
            if abs(male_percentage - female_percentage) > 10:
                if female_percentage > male_percentage:
                    analysis_parts.append(
                        f"महिला जेष्ठ नागरिकहरूको संख्या पुरुषको तुलनामा "
                        f"{format_nepali_percentage(female_percentage - male_percentage)}% बढी छ। "
                        f"यसले महिलाहरूको औसत आयु पुरुषहरूको तुलनामा बढी भएको संकेत गर्छ।"
                    )
                else:
                    analysis_parts.append(
                        f"पुरुष जेष्ठ नागरिकहरूको संख्या महिलाको तुलनामा "
                        f"{format_nepali_percentage(male_percentage - female_percentage)}% बढी छ।"
                    )

        # Single women analysis
        if total_single_women > 0:
            analysis_parts.append(
                f"एकल महिलाको संख्या {format_nepali_number(total_single_women)} जना छ। "
                f"यी महिलाहरूलाई विशेष सामाजिक सुरक्षा र सहायताको आवश्यकता छ।"
            )

            # Single women in context of elderly women
            if total_female_old_age > 0:
                single_women_elderly_ratio = (
                    total_single_women / total_female_old_age * 100
                )
                if single_women_elderly_ratio > 0:
                    analysis_parts.append(
                        f"एकल महिलाको संख्या कुल महिला जेष्ठ नागरिकको तुलनामा "
                        f"{format_nepali_percentage(single_women_elderly_ratio)}% छ।"
                    )

        # Ward-wise analysis
        if ward_data and len(ward_data) > 1:
            # Find wards with highest and lowest elderly population
            ward_elderly_counts = {}
            ward_single_women_counts = {}

            for ward_num, ward_info in ward_data.items():
                ward_elderly_counts[ward_num] = (
                    ward_info["demographics"]["male_old_age"]["population"]
                    + ward_info["demographics"]["female_old_age"]["population"]
                )
                ward_single_women_counts[ward_num] = ward_info["demographics"][
                    "single_women"
                ]["population"]

            # Elderly population analysis
            if ward_elderly_counts:
                highest_elderly_ward = max(
                    ward_elderly_counts.items(), key=lambda x: x[1]
                )
                lowest_elderly_ward = min(
                    ward_elderly_counts.items(), key=lambda x: x[1]
                )

                if highest_elderly_ward[0] != lowest_elderly_ward[0]:
                    analysis_parts.append(
                        f"वडागत विश्लेषणमा, वडा नं. {highest_elderly_ward[0]} मा सबैभन्दा बढी "
                        f"{format_nepali_number(highest_elderly_ward[1])} जना जेष्ठ नागरिकहरू छन् "
                        f"भने वडा नं. {lowest_elderly_ward[0]} मा सबैभन्दा कम "
                        f"{format_nepali_number(lowest_elderly_ward[1])} जना जेष्ठ नागरिकहरू छन्।"
                    )

            # Single women ward analysis
            if ward_single_women_counts and max(ward_single_women_counts.values()) > 0:
                highest_single_women_ward = max(
                    ward_single_women_counts.items(), key=lambda x: x[1]
                )
                lowest_single_women_ward = min(
                    ward_single_women_counts.items(), key=lambda x: x[1]
                )

                if highest_single_women_ward[0] != lowest_single_women_ward[0]:
                    analysis_parts.append(
                        f"एकल महिलाको वडागत वितरणमा, वडा नं. {highest_single_women_ward[0]} मा सबैभन्दा बढी "
                        f"{format_nepali_number(highest_single_women_ward[1])} जना एकल महिलाहरू छन् "
                        f"भने वडा नं. {lowest_single_women_ward[0]} मा सबैभन्दा कम "
                        f"{format_nepali_number(lowest_single_women_ward[1])} जना एकल महिलाहरू छन्।"
                    )

        # Social security and welfare analysis
        analysis_parts.append(
            "जेष्ठ नागरिकहरूको बढ्दो संख्याले स्वास्थ्य सेवा, सामाजिक सुरक्षा र विशेष हेरचाहको आवश्यकतालाई बढाएको छ।"
        )

        # Care and support needs
        analysis_parts.append(
            "एकल महिलाहरूको अवस्थाले विशेष सामाजिक सहायता, आर्थिक सहयोग र सुरक्षाको आवश्यकतालाई देखाउँछ।"
        )

        # Policy implications
        analysis_parts.append(
            "जेष्ठ नागरिक र एकल महिलाहरूका लागि विशेष कार्यक्रम, भत्ता र सेवाहरूको विस्तार आवश्यक छ।"
        )

        # Health and care services
        analysis_parts.append(
            "जेष्ठ नागरिकहरूको स्वास्थ्य सेवा, घरेलु हेरचाह र सामुदायिक सहयोग कार्यक्रमहरूको विकास गर्नुपर्छ।"
        )

        # Economic support
        analysis_parts.append(
            "एकल महिलाहरूको आर्थिक सशक्तिकरणका लागि सीप विकास, रोजगारी र आय आर्जनका अवसरहरू सिर्जना गर्नुपर्छ।"
        )

        # Community integration
        analysis_parts.append(
            "जेष्ठ नागरिक र एकल महिलाहरूको सामुदायिक सहभागिता बढाउने र सामाजिक एकीकरणमा योगदान पुर्याउने कार्यक्रमहरू आवश्यक छन्।"
        )

        return " ".join(analysis_parts)

    def generate_pie_chart(self, data, title="जेष्ठ नागरिकको लैङ्गिक वितरण"):
        """Generate pie chart for elderly population gender distribution"""
        if not data.get("municipality_data"):
            return None

        chart_data = {}
        for key, value in data["municipality_data"].items():
            chart_data[key] = {
                "name_nepali": value["name_nepali"],
                "population": value["population"],
            }

        return self.chart_generator.generate_pie_chart_svg(
            chart_data,
            include_title=False,
            title_nepali=title,
            title_english="Gender Distribution of Elderly Population",
        )

    def generate_bar_chart(self, data, title="वडागत जेष्ठ नागरिक र एकल महिला वितरण"):
        """Generate bar chart for ward-wise elderly and single women distribution"""
        if not data.get("ward_data"):
            return None

        chart_data = {}
        for ward_num, ward_info in data["ward_data"].items():
            chart_data[f"ward_{ward_num}"] = {
                "name_nepali": f"वडा {ward_num}",
                "male_elderly": ward_info["demographics"]["male_old_age"]["population"],
                "female_elderly": ward_info["demographics"]["female_old_age"][
                    "population"
                ],
                "single_women": ward_info["demographics"]["single_women"]["population"],
                "total_elderly": (
                    ward_info["demographics"]["male_old_age"]["population"]
                    + ward_info["demographics"]["female_old_age"]["population"]
                ),
            }

        return self.chart_generator.generate_bar_chart_svg(
            chart_data,
            include_title=False,
            title_nepali=title,
            title_english="Ward-wise Elderly and Single Women Distribution",
        )

    def process_for_pdf(self):
        """Process old age and single women data for PDF generation including charts"""
        # Get raw data
        data = self.get_data()

        # Generate analysis text
        coherent_analysis = self.generate_analysis_text(data)

        # Generate and save charts
        charts = self.generate_and_save_charts(data)

        return {
            "municipality_data": data.get("municipality_data", {}),
            "single_women_data": data.get("single_women_data", {}),
            "ward_data": data.get("ward_data", {}),
            "total_male_old_age": data.get("total_male_old_age", 0),
            "total_female_old_age": data.get("total_female_old_age", 0),
            "total_old_age_population": data.get("total_old_age_population", 0),
            "total_single_women": data.get("total_single_women", 0),
            "coherent_analysis": coherent_analysis,
            "pdf_charts": {"old_age_and_single_women": charts},
            "section_title": self.get_section_title(),
            "section_number": self.get_section_number(),
        }


class OldAgeAndSingleWomenReportFormatter(BaseSocialReportFormatter):
    """Report formatter for old age population and single women data"""

    def __init__(self, processor_data):
        super().__init__(processor_data)

    def format_for_html(self):
        """Format data for HTML template rendering"""
        return {
            "municipality_data": self.data["municipality_data"],
            "single_women_data": self.data["single_women_data"],
            "ward_data": self.data["ward_data"],
            "total_male_old_age": self.data["total_male_old_age"],
            "total_female_old_age": self.data["total_female_old_age"],
            "total_old_age_population": self.data["total_old_age_population"],
            "total_single_women": self.data["total_single_women"],
            "coherent_analysis": self.data["coherent_analysis"],
            "pdf_charts": self.data["pdf_charts"],
        }

    def format_for_api(self):
        """Format data for API response"""
        return {
            "section": self.data["section_number"],
            "title": self.data["section_title"],
            "summary": {
                "total_elderly": self.data["total_old_age_population"],
                "male_elderly": self.data["total_male_old_age"],
                "female_elderly": self.data["total_female_old_age"],
                "single_women": self.data["total_single_women"],
                "wards": len(self.data["ward_data"]),
            },
            "gender_distribution": self.data["municipality_data"],
            "single_women_info": self.data["single_women_data"],
            "ward_breakdown": self.data["ward_data"],
            "analysis": self.data["coherent_analysis"],
        }
