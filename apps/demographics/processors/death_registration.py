"""
Death Registration Demographics Processor

Handles age-gender death registration data processing, population pyramid chart generation, and detailed report formatting.
"""

from pathlib import Path
from .base import BaseDemographicsProcessor, BaseReportFormatter
from ..models import WardAgeGenderWiseDeceasedPopulation, AgeGroupChoice, GenderChoice
from ..utils.svg_chart_generator import DEFAULT_COLORS
from apps.reports.utils.nepali_numbers import (
    format_nepali_number,
    format_nepali_percentage,
)
from apps.chart_management.processors import SimpleChartProcessor


class DeathRegistrationProcessor(BaseDemographicsProcessor, SimpleChartProcessor):
    """Processor for age-gender death registration with population pyramid"""

    def __init__(self):
        super().__init__()
        SimpleChartProcessor.__init__(self)

        # Ensure we use the same directory as the chart service
        from django.conf import settings

        if hasattr(settings, "STATICFILES_DIRS") and settings.STATICFILES_DIRS:
            self.static_charts_dir = (
                Path(settings.STATICFILES_DIRS[0]) / "images" / "charts"
            )
        else:
            self.static_charts_dir = Path(settings.STATIC_ROOT) / "images" / "charts"

        self.static_charts_dir.mkdir(parents=True, exist_ok=True)

        # Customize chart dimensions for population pyramid
        self.pyramid_chart_width = 1200
        self.pyramid_chart_height = 800
        self.bar_chart_width = 1000
        self.bar_chart_height = 600

        # Age-gender specific colors
        self.chart_generator.colors = {
            "MALE": "#3498db",
            "FEMALE": "#e74c3c",
            "OTHER": "#95a5a6",
            "TOTAL": "#34495e",
        }

    def get_chart_key(self):
        return "demographics_death_registration"

    def get_section_title(self):
        return "मृत्यु दर्ता (उमेर तथा लिङ्ग अनुसार) विवरण"

    def get_section_number(self):
        return "३.४"

    def get_data(self):
        age_gender_data = {}
        ward_data = {}

        # Initialize age groups
        for age_choice in AgeGroupChoice.choices:
            age_gender_data[age_choice[0]] = {
                "code": age_choice[0],
                "name_nepali": age_choice[1],
                "MALE": 0,
                "FEMALE": 0,
                "OTHER": 0,
                "TOTAL": 0,
                "male_percentage": 0.0,
                "female_percentage": 0.0,
                "other_percentage": 0.0,
                "total_percentage": 0.0,
            }

        # Initialize ward data for wards 1-8 (dynamic for new data)
        for ward_num in range(1, 9):
            ward_data[ward_num] = {
                "ward_number": ward_num,
                "age_groups": {},
                "MALE": 0,
                "FEMALE": 0,
                "OTHER": 0,
                "TOTAL": 0,
            }
            for age_choice in AgeGroupChoice.choices:
                ward_data[ward_num][age_choice[0]] = {
                    "MALE": 0,
                    "FEMALE": 0,
                    "OTHER": 0,
                    "TOTAL": 0,
                }

        total_population = 0
        total_male = 0
        total_female = 0
        total_other = 0

        for obj in WardAgeGenderWiseDeceasedPopulation.objects.all():
            age_group = obj.age_group
            gender = obj.gender
            ward_number = obj.ward_number
            count = obj.deceased_population or 0

            # Fix: If age_group is not in age_gender_data, initialize it on the fly
            if age_group not in age_gender_data:
                age_gender_data[age_group] = {
                    "code": age_group,
                    "name_nepali": age_group,
                    "MALE": 0,
                    "FEMALE": 0,
                    "OTHER": 0,
                    "TOTAL": 0,
                    "male_percentage": 0.0,
                    "female_percentage": 0.0,
                    "other_percentage": 0.0,
                    "total_percentage": 0.0,
                }

            if age_group in age_gender_data and gender in ["MALE", "FEMALE", "OTHER"]:
                age_gender_data[age_group][gender] += count
                age_gender_data[age_group]["TOTAL"] += count
                if ward_number in ward_data:
                    ward_data[ward_number][age_group][gender] += count
                    ward_data[ward_number][age_group]["TOTAL"] += count
                    ward_data[ward_number][gender] += count
                    ward_data[ward_number]["TOTAL"] += count

            if gender == "MALE":
                total_male += count
            elif gender == "FEMALE":
                total_female += count
            elif gender == "OTHER":
                total_other += count
            total_population += count

        # Calculate percentages
        if total_population > 0:
            for age_group, data in age_gender_data.items():
                data["male_percentage"] = (
                    data["MALE"] / total_population * 100 if total_population > 0 else 0
                )
                data["female_percentage"] = (
                    data["FEMALE"] / total_population * 100
                    if total_population > 0
                    else 0
                )
                data["other_percentage"] = (
                    data["OTHER"] / total_population * 100
                    if total_population > 0
                    else 0
                )
                data["total_percentage"] = (
                    data["TOTAL"] / total_population * 100
                    if total_population > 0
                    else 0
                )

        for ward_num, ward_info in ward_data.items():
            if ward_info["TOTAL"] > 0:
                ward_info["male_percentage"] = (
                    ward_info["MALE"] / ward_info["TOTAL"] * 100
                )
                ward_info["female_percentage"] = (
                    ward_info["FEMALE"] / ward_info["TOTAL"] * 100
                )
                ward_info["other_percentage"] = (
                    ward_info["OTHER"] / ward_info["TOTAL"] * 100
                )
            else:
                ward_info["male_percentage"] = 0
                ward_info["female_percentage"] = 0
                ward_info["other_percentage"] = 0

        return {
            "age_gender_data": age_gender_data,
            "ward_data": ward_data,
            "total_population": total_population,
            "total_male": total_male,
            "total_female": total_female,
            "total_other": total_other,
            "male_percentage": (
                (total_male / total_population * 100) if total_population > 0 else 0
            ),
            "female_percentage": (
                (total_female / total_population * 100) if total_population > 0 else 0
            ),
            "other_percentage": (
                (total_other / total_population * 100) if total_population > 0 else 0
            ),
        }

    def generate_report_content(self, data):
        formatter = self.DeathRegistrationReportFormatter()
        return formatter.generate_detailed_analysis(data)

    def generate_population_pyramid_svg(self, data):
        # Use the dedicated death pyramid generator
        from ..utils.death_pyramid_generator import DeathPyramidGenerator

        generator = DeathPyramidGenerator()
        return generator.generate_pyramid_svg(
            data["age_gender_data"],
            width=self.pyramid_chart_width,
            height=self.pyramid_chart_height,
            title_nepali="मृत्यु दर्ता पिरामिड",
            title_english="Death Registration Pyramid",
        )

    def generate_chart_svg(self, data, chart_type="pyramid"):
        if chart_type == "pyramid":
            return self.generate_population_pyramid_svg(data)
        return None

    def generate_and_track_charts(self, data):
        charts = {}
        from ..utils.death_pyramid_generator import DeathPyramidGenerator

        generator = DeathPyramidGenerator()
        png_path = (
            self.static_charts_dir / "demographics_death_registration_pyramid.png"
        )
        svg_path = (
            self.static_charts_dir / "demographics_death_registration_pyramid.svg"
        )

        # Use the generator's PNG method (which uses Inkscape)
        png_result = generator.save_pyramid_to_png(
            data["age_gender_data"],
            png_path,
            width=self.pyramid_chart_width,
            height=self.pyramid_chart_height,
            title_nepali="मृत्यु दर्ता पिरामिड",
            title_english="Death Registration Pyramid",
        )
        if png_result and png_path.exists():
            charts["pyramid_chart_png"] = (
                f"images/charts/demographics_death_registration_pyramid.png"
            )
        else:
            # Fallback: generate SVG and use that
            svg = generator.generate_pyramid_svg(
                data["age_gender_data"],
                width=self.pyramid_chart_width,
                height=self.pyramid_chart_height,
                title_nepali="मृत्यु दर्ता पिरामिड",
                title_english="Death Registration Pyramid",
            )
            with open(svg_path, "w", encoding="utf-8") as f:
                f.write(svg)
            charts["pyramid_chart_svg"] = (
                f"images/charts/demographics_death_registration_pyramid.svg"
            )
        return charts

    def generate_and_save_charts(self, data):
        return self.generate_and_track_charts(data)

    def _create_ward_table_data(self, ward_data, age_gender_data):
        """Create a flattened data structure for easy template access (ward headers, age group rows, totals)"""
        ward_table_rows = []
        for ward_num, ward_info in ward_data.items():
            # Add ward header row
            ward_table_rows.append(
                {
                    "type": "ward_header",
                    "ward_number": ward_num,
                    "colspan": 5,
                }
            )
            # Add age group rows for this ward
            for age_group_code, age_group_info in age_gender_data.items():
                ward_age_group = ward_info.get(age_group_code, {})
                ward_table_rows.append(
                    {
                        "type": "age_group",
                        "ward_number": ward_num,
                        "age_group_code": age_group_code,
                        "age_group_name": age_group_info.get(
                            "name_nepali", age_group_code
                        ),
                        "male": ward_age_group.get("MALE", 0),
                        "female": ward_age_group.get("FEMALE", 0),
                        "total": ward_age_group.get("TOTAL", 0),
                    }
                )
            # Add ward total row
            ward_table_rows.append(
                {
                    "type": "ward_total",
                    "ward_number": ward_num,
                    "male": ward_info.get("MALE", 0),
                    "female": ward_info.get("FEMALE", 0),
                    "total": ward_info.get("TOTAL", 0),
                }
            )
        return ward_table_rows

    def process_for_pdf(self):
        data = self.get_data()
        report_content = self.generate_report_content(data)
        charts = self.generate_and_track_charts(data)
        ward_table_data = self._create_ward_table_data(
            data["ward_data"], data["age_gender_data"]
        )
        total_population = data.get("total_population", 0)
        return {
            "data": data,
            "death_registration_data": data["age_gender_data"],
            "ward_data": data["ward_data"],
            "ward_table_data": ward_table_data,
            "report_content": report_content,
            "coherent_analysis": report_content,
            "charts": charts,
            "total_population": total_population,
            "section_title": self.get_section_title(),
            "section_number": self.get_section_number(),
        }

    class DeathRegistrationReportFormatter(BaseReportFormatter):
        def generate_detailed_analysis(self, data):
            total = data["total_population"]
            male = data["total_male"]
            female = data["total_female"]
            other = data["total_other"]
            male_pct = data["male_percentage"]
            female_pct = data["female_percentage"]
            other_pct = data["other_percentage"]
            age_gender_data = data["age_gender_data"]

            # Find age group with highest and lowest deaths
            max_group = max(age_gender_data.items(), key=lambda x: x[1]["TOTAL"])
            min_group = min(age_gender_data.items(), key=lambda x: x[1]["TOTAL"])
            max_group_label = max_group[1]["name_nepali"]
            min_group_label = min_group[1]["name_nepali"]
            max_group_total = max_group[1]["TOTAL"]
            min_group_total = min_group[1]["TOTAL"]

            return (
                f"गढवा गाउँपालिकामा मृत्यु दर्ता भएका कुल जनसंख्या {format_nepali_number(total)} जना छन् । "
                f"जसमध्ये पुरुष {format_nepali_number(male)} जना ({format_nepali_percentage(male_pct)}) र महिला {format_nepali_number(female)} जना ({format_nepali_percentage(female_pct)}) रहेका छन् । \n\n"
                f"मृत्यु दर्ता पिरामिडले उमेर समूह र लिङ्ग अनुसार मृत्यु हुनेको वितरण देखाउँछ । सबैभन्दा बढी मृत्यु दर्ता '{max_group_label}' उमेर समूहमा {format_nepali_number(max_group_total)} जना र सबैभन्दा कम '{min_group_label}' उमेर समूहमा {format_nepali_number(min_group_total)} जना रहेका छन् ।\n\n"
                f"यस विवरणले स्वास्थ्य नीति, सामाजिक सुरक्षा, तथा लक्षित कार्यक्रम निर्माणमा महत्वपूर्ण आधार प्रदान गर्छ । मृत्यु हुनेको उमेर समूह, लिङ्ग, र वडागत वितरणको विश्लेषणले जोखिम समूह पहिचान गर्न र आवश्यक हस्तक्षेप योजना बनाउन सहयोग पुर्‍याउँछ ।\n\n"
                f"मृत्यु दर्ता विवरणको आधारमा बालबालिका, वृद्धवृद्धा, र कामकाजी उमेर समूहमा देखिएको मृत्यु दरले स्वास्थ्य सेवा पहुँच, रोग नियन्त्रण, तथा सामाजिक-आर्थिक अवस्थाको झलक दिन्छ । यसले स्थानीय सरकारलाई प्राथमिकता निर्धारण, सचेतना कार्यक्रम, र स्वास्थ्य पूर्वाधार सुदृढीकरणमा मार्गदर्शन गर्छ ।"
            )

        def generate_formal_report(self, data):
            # Kept for legacy/summary use
            total = data["total_population"]
            male = data["total_male"]
            female = data["total_female"]
            return f"""गढवा गाउँपालिकामा मृत्यु दर्ता भएका कुल जनसंख्या {format_nepali_number(total)} जना छन् । जसमध्ये पुरुष {format_nepali_number(male)} जना र महिला {format_nepali_number(female)} जना रहेका छन् । मृत्यु दर्ता पिरामिडले उमेर समूह र लिङ्ग अनुसार मृत्यु हुनेको वितरण देखाउँछ । यसले स्वास्थ्य नीति तथा कार्यक्रम निर्माणमा महत्वपूर्ण आधार प्रदान गर्छ ।"""
