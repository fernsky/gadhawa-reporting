"""
Age-Gender Demographics Processor

Handles age-gender demographic data processing, population pyramid chart generation, and detailed report formatting.
"""

from pathlib import Path
from .base import BaseDemographicsProcessor, BaseReportFormatter
from ..models import WardAgeWisePopulation, AgeGroupChoice, GenderChoice
from ..utils.svg_chart_generator import DEFAULT_COLORS
from apps.reports.utils.nepali_numbers import (
    format_nepali_number,
    format_nepali_percentage,
)
from apps.chart_management.processors import SimpleChartProcessor


class AgeGenderProcessor(BaseDemographicsProcessor, SimpleChartProcessor):
    """Processor for age-gender demographics with population pyramid"""

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
            self.static_charts_dir = Path("static/images/charts")

        self.static_charts_dir.mkdir(parents=True, exist_ok=True)

        # Customize chart dimensions for population pyramid
        self.pyramid_chart_width = 1200
        self.pyramid_chart_height = 800
        self.bar_chart_width = 1000
        self.bar_chart_height = 600

        # Age-gender specific colors
        self.chart_generator.colors = {
            "MALE": "#3498db",  # Blue for males
            "FEMALE": "#e74c3c",  # Red for females
            "OTHER": "#95a5a6",  # Gray for others
            "TOTAL": "#34495e",  # Dark gray for totals
        }

    def get_chart_key(self):
        """Return unique chart key for this processor"""
        return "demographics_age_gender"

    def get_section_title(self):
        return "उमेर तथा लिङ्गको आधारमा जनसंख्या विवरण"

    def get_section_number(self):
        return "३.३"

    def get_data(self):
        """Get age-gender population data with comprehensive analysis"""
        # Initialize data structures
        age_gender_data = {}
        ward_data = {}

        # Initialize age groups
        for age_choice in AgeGroupChoice.choices:
            age_code = age_choice[0]
            age_name = age_choice[1]
            age_gender_data[age_code] = {
                "name_nepali": age_name,
                "male": 0,
                "female": 0,
                "other": 0,
                "total": 0,
                "male_percentage": 0.0,
                "female_percentage": 0.0,
                "other_percentage": 0.0,
            }

        # Initialize ward data
        for ward_num in range(1, 8):
            ward_data[str(ward_num)] = {
                "male": 0,
                "female": 0,
                "other": 0,
                "total": 0,
                "age_groups": {},
            }

            # Initialize age groups for each ward
            for age_choice in AgeGroupChoice.choices:
                age_code = age_choice[0]
                ward_data[str(ward_num)]["age_groups"][age_code] = {
                    "male": 0,
                    "female": 0,
                    "other": 0,
                    "total": 0,
                }

        # Get actual data from database
        total_population = 0
        total_male = 0
        total_female = 0
        total_other = 0

        for population_obj in WardAgeWisePopulation.objects.all():
            age_group = population_obj.age_group
            gender = population_obj.gender
            population = population_obj.population
            ward_num = str(
                population_obj.ward_number
            )  # Convert to string for consistency

            # Update totals
            total_population += population
            if gender == "MALE":
                total_male += population
            elif gender == "FEMALE":
                total_female += population
            else:
                total_other += population

            # Update age-gender data
            if gender == "MALE":
                age_gender_data[age_group]["male"] += population
            elif gender == "FEMALE":
                age_gender_data[age_group]["female"] += population
            else:
                age_gender_data[age_group]["other"] += population

            age_gender_data[age_group]["total"] += population

            # Update ward data (fix: always update nested age_groups)
            if gender == "MALE":
                ward_data[ward_num]["male"] += population
                ward_data[ward_num]["age_groups"][age_group]["male"] += population
            elif gender == "FEMALE":
                ward_data[ward_num]["female"] += population
                ward_data[ward_num]["age_groups"][age_group]["female"] += population
            else:
                ward_data[ward_num]["other"] += population
                ward_data[ward_num]["age_groups"][age_group]["other"] += population

            ward_data[ward_num]["total"] += population
            ward_data[ward_num]["age_groups"][age_group]["total"] += population

        # Calculate percentages
        if total_population > 0:
            for age_group in age_gender_data:
                age_total = age_gender_data[age_group]["total"]
                if age_total > 0:
                    age_gender_data[age_group]["male_percentage"] = (
                        age_gender_data[age_group]["male"] / age_total
                    ) * 100
                    age_gender_data[age_group]["female_percentage"] = (
                        age_gender_data[age_group]["female"] / age_total
                    ) * 100
                    age_gender_data[age_group]["other_percentage"] = (
                        age_gender_data[age_group]["other"] / age_total
                    ) * 100

        # Calculate ward percentages
        for ward_num, ward_info in ward_data.items():
            ward_total = ward_info["total"]
            if ward_total > 0:
                ward_info["male_percentage"] = (ward_info["male"] / ward_total) * 100
                ward_info["female_percentage"] = (
                    ward_info["female"] / ward_total
                ) * 100
                ward_info["other_percentage"] = (ward_info["other"] / ward_total) * 100

        # Calculate dependency ratios and other demographic indicators
        dependency_ratios = self._calculate_dependency_ratios(age_gender_data)
        demographic_indicators = self._calculate_demographic_indicators(
            age_gender_data, total_population, total_male, total_female, total_other
        )

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
            "dependency_ratios": dependency_ratios,
            "demographic_indicators": demographic_indicators,
        }

    def _calculate_dependency_ratios(self, age_gender_data):
        """Calculate various dependency ratios"""
        # Child dependency ratio (0-14 years)
        child_population = 0
        for age_group in ["AGE_0_4", "AGE_5_9", "AGE_10_14"]:
            child_population += age_gender_data[age_group]["total"]

        # Working age population (15-64 years)
        working_age_population = 0
        working_age_groups = [
            "AGE_15_19",
            "AGE_20_24",
            "AGE_25_29",
            "AGE_30_34",
            "AGE_35_39",
            "AGE_40_44",
            "AGE_45_49",
            "AGE_50_54",
            "AGE_55_59",
            "AGE_60_64",
        ]
        for age_group in working_age_groups:
            working_age_population += age_gender_data[age_group]["total"]

        # Elderly population (65+ years)
        elderly_population = 0
        for age_group in ["AGE_65_69", "AGE_70_74", "AGE_75_AND_ABOVE"]:
            elderly_population += age_gender_data[age_group]["total"]

        # Calculate ratios
        child_dependency_ratio = (
            (child_population / working_age_population * 100)
            if working_age_population > 0
            else 0
        )
        elderly_dependency_ratio = (
            (elderly_population / working_age_population * 100)
            if working_age_population > 0
            else 0
        )
        total_dependency_ratio = child_dependency_ratio + elderly_dependency_ratio

        return {
            "child_population": child_population,
            "working_age_population": working_age_population,
            "elderly_population": elderly_population,
            "child_dependency_ratio": child_dependency_ratio,
            "elderly_dependency_ratio": elderly_dependency_ratio,
            "total_dependency_ratio": total_dependency_ratio,
        }

    def _calculate_demographic_indicators(
        self, age_gender_data, total_pop, total_male, total_female, total_other
    ):
        """Calculate demographic indicators"""
        # Gender ratio (males per 100 females)
        gender_ratio = (total_male / total_female * 100) if total_female > 0 else 0

        # Youth population (15-39 years)
        youth_population = 0
        youth_groups = ["AGE_15_19", "AGE_20_24", "AGE_25_29", "AGE_30_34", "AGE_35_39"]
        for age_group in youth_groups:
            youth_population += age_gender_data[age_group]["total"]

        youth_percentage = (youth_population / total_pop * 100) if total_pop > 0 else 0

        # Reproductive age women (15-49 years)
        reproductive_age_women = 0
        reproductive_groups = [
            "AGE_15_19",
            "AGE_20_24",
            "AGE_25_29",
            "AGE_30_34",
            "AGE_35_39",
            "AGE_40_44",
            "AGE_45_49",
        ]
        for age_group in reproductive_groups:
            reproductive_age_women += age_gender_data[age_group]["female"]

        reproductive_women_percentage = (
            (reproductive_age_women / total_female * 100) if total_female > 0 else 0
        )

        return {
            "gender_ratio": gender_ratio,
            "youth_population": youth_population,
            "youth_percentage": youth_percentage,
            "reproductive_age_women": reproductive_age_women,
            "reproductive_women_percentage": reproductive_women_percentage,
        }

    def generate_report_content(self, data):
        """Generate age-gender specific detailed report content"""
        formatter = self.AgeGenderReportFormatter()
        return formatter.generate_detailed_analysis(data)

    def generate_population_pyramid_svg(self, data):
        """Generate population pyramid SVG chart"""
        from ..utils.population_pyramid_generator import PopulationPyramidGenerator

        pyramid_generator = PopulationPyramidGenerator()
        return pyramid_generator.generate_pyramid_svg(
            data["age_gender_data"],
            width=self.pyramid_chart_width,
            height=self.pyramid_chart_height,
            title_nepali="उमेर तथा लिङ्गको आधारमा जनसंख्या पिरामिड",
            title_english="Population Pyramid by Age and Gender",
        )

    def generate_chart_svg(self, data, chart_type="pyramid"):
        """Generate age-gender chart SVG"""
        if chart_type == "pyramid":
            return self.generate_population_pyramid_svg(data)
        return None

    def generate_and_track_charts(self, data):
        """Generate charts as PNG files directly using population pyramid generator"""
        charts = {}

        # Ensure static charts directory exists
        self.static_charts_dir.mkdir(parents=True, exist_ok=True)

        # Check and generate population pyramid only if needed
        if self.needs_generation("pyramid"):
            try:
                from ..utils.population_pyramid_generator import (
                    PopulationPyramidGenerator,
                )

                pyramid_generator = PopulationPyramidGenerator()
                pyramid_filename = f"{self.get_chart_key()}_pyramid.png"
                pyramid_path = self.static_charts_dir / pyramid_filename

                # Generate PNG directly
                png_path = pyramid_generator.save_pyramid_to_png(
                    data["age_gender_data"],
                    pyramid_path,
                    width=self.pyramid_chart_width,
                    height=self.pyramid_chart_height,
                    title_nepali="उमेर तथा लिङ्गको आधारमा जनसंख्या पिरामिड",
                    title_english="Population Pyramid by Age and Gender",
                    dpi=300,
                )

                if png_path and png_path.exists():
                    charts["pyramid_chart_png"] = f"images/charts/{png_path.name}"
                    charts["pyramid_chart_url"] = (
                        f"/static/images/charts/{png_path.name}"
                    )
                    print(f"  ✅ Generated population pyramid PNG chart")
                else:
                    print(f"  ❌ Failed to generate population pyramid PNG chart")

            except Exception as e:
                print(f"  ❌ Error generating population pyramid: {e}")
        else:
            png_path = self.static_charts_dir / f"{self.get_chart_key()}_pyramid.png"
            if png_path.exists():
                charts["pyramid_chart_png"] = f"images/charts/{png_path.name}"
                charts["pyramid_chart_url"] = f"/static/images/charts/{png_path.name}"
            print(f"  ♻️  Using existing population pyramid PNG chart")

        # Check and generate bar chart only if needed
        if self.needs_generation("bar"):
            try:
                bar_svg = self.generate_chart_svg(data, "bar")
                if bar_svg:
                    bar_filename = f"{self.get_chart_key()}_bar.svg"
                    bar_path = self.static_charts_dir / bar_filename
                    with open(bar_path, "w", encoding="utf-8") as f:
                        f.write(bar_svg)

                    # Convert to PNG using chart management
                    png_path = self.convert_svg_to_png(bar_path)
                    if png_path:
                        charts["bar_chart_png"] = f"images/charts/{png_path.name}"
                        charts["bar_chart_url"] = (
                            f"/static/images/charts/{png_path.name}"
                        )
                        print(f"  ✅ Generated ward-wise gender bar PNG chart")
                    else:
                        print(
                            f"  ❌ Failed to convert ward-wise gender bar chart to PNG"
                        )
                else:
                    print(f"  ❌ Failed to generate ward-wise gender bar chart")
            except Exception as e:
                print(f"  ❌ Error generating ward-wise gender bar chart: {e}")
        else:
            png_path = self.static_charts_dir / f"{self.get_chart_key()}_bar.png"
            if png_path.exists():
                charts["bar_chart_png"] = f"images/charts/{png_path.name}"
                charts["bar_chart_url"] = f"/static/images/charts/{png_path.name}"
            print(f"  ♻️  Using existing ward-wise gender bar PNG chart")

        return charts

    def generate_and_save_charts(self, data):
        """Legacy method - calls new chart management method"""
        return self.generate_and_track_charts(data)

    def process_for_pdf(self):
        """Process age-gender data for PDF generation with comprehensive analysis"""
        # Get raw data
        data = self.get_data()

        # Generate detailed report content
        report_content = self.generate_report_content(data)

        # Generate charts only if needed
        charts = self.generate_and_track_charts(data)

        # Create template-friendly ward table data
        ward_table_data = self._create_ward_table_data(
            data["ward_data"], data["age_gender_data"]
        )

        return {
            "data": data,
            "age_gender_data": data["age_gender_data"],
            "ward_data": data["ward_data"],
            "ward_table_data": ward_table_data,  # New flattened structure for templates
            "report_content": report_content,
            "coherent_analysis": report_content,
            "charts": charts,
            "total_population": data["total_population"],
            "total_male": data["total_male"],
            "total_female": data["total_female"],
            "total_other": data["total_other"],
            "male_percentage": data["male_percentage"],
            "female_percentage": data["female_percentage"],
            "other_percentage": data["other_percentage"],
            "dependency_ratios": data["dependency_ratios"],
            "demographic_indicators": data["demographic_indicators"],
            "section_title": self.get_section_title(),
            "section_number": self.get_section_number(),
        }

    def _create_ward_table_data(self, ward_data, age_gender_data):
        """Create a flattened data structure for easy template access"""
        ward_table_rows = []

        for ward_num_str, ward_info in ward_data.items():
            ward_num = int(ward_num_str)

            # Add ward header row
            ward_table_rows.append(
                {
                    "type": "ward_header",
                    "ward_number": ward_num,
                    "ward_number_nepali": ward_num_str,
                    "colspan": 5,
                }
            )

            # Add age group rows for this ward
            for age_group_code, age_group_info in age_gender_data.items():
                age_group_data = ward_info["age_groups"].get(
                    age_group_code, {"male": 0, "female": 0, "other": 0, "total": 0}
                )

                ward_table_rows.append(
                    {
                        "type": "age_group",
                        "ward_number": ward_num,
                        "age_group_code": age_group_code,
                        "age_group_name": age_group_info["name_nepali"],
                        "male": age_group_data["male"],
                        "female": age_group_data["female"],
                        "other": age_group_data["other"],
                        "total": age_group_data["total"],
                    }
                )

            # Add ward total row
            ward_table_rows.append(
                {
                    "type": "ward_total",
                    "ward_number": ward_num,
                    "male": ward_info["male"],
                    "female": ward_info["female"],
                    "other": ward_info["other"],
                    "total": ward_info["total"],
                }
            )

        return ward_table_rows

    class AgeGenderReportFormatter(BaseReportFormatter):
        """Age-gender specific report formatter with detailed analysis"""

        def generate_detailed_analysis(self, data):
            """Generate comprehensive age-gender demographic analysis"""
            total_pop = data["total_population"]
            total_male = data["total_male"]
            total_female = data["total_female"]
            total_other = data["total_other"]
            male_pct = data["male_percentage"]
            female_pct = data["female_percentage"]
            other_pct = data["other_percentage"]

            dependency_ratios = data["dependency_ratios"]
            indicators = data["demographic_indicators"]
            age_gender_data = data["age_gender_data"]
            ward_data = data["ward_data"]

            analysis_parts = []

            # Overall demographic overview
            analysis_parts.append(
                f"लुङ्ग्री गाउँपालिकामा रहेका कूल {format_nepali_number(total_pop)} जनसंख्या मध्ये "
                f"{format_nepali_number(total_male)} पुरुष ({format_nepali_percentage(male_pct)}%), "
                f"{format_nepali_number(total_female)} जना महिला ({format_nepali_percentage(female_pct)}%)"
            )

            if total_other > 0:
                analysis_parts[
                    -1
                ] += f" र {format_nepali_number(total_other)} जना अन्य ({format_nepali_percentage(other_pct)}%)"

            analysis_parts[-1] += " जनसंख्या रहेका छन् ।"

            # Gender ratio analysis
            gender_ratio = indicators["gender_ratio"]
            if gender_ratio > 103:
                gender_analysis = "पुरुषको बाहुल्यता रहेको"
            elif gender_ratio < 97:
                gender_analysis = "महिलाको बाहुल्ता रहेको"
            else:
                gender_analysis = "लिङ्गीय सन्तुलन रहेको"

            analysis_parts.append(
                f"लिङ्गीय अनुपातका आधारमा हेर्दा प्रति सय महिलामा {format_nepali_number(int(gender_ratio))} पुरुष रहेका छन्, "
                f"जसले गाउँपालिकामा {gender_analysis} देखाउँछ ।"
            )

            # Age group analysis
            age_dominance = []
            for age_group, age_data in age_gender_data.items():
                if age_data["male"] > age_data["female"]:
                    age_dominance.append((age_group, "पुरुष", age_data["name_nepali"]))
                elif age_data["female"] > age_data["male"]:
                    age_dominance.append((age_group, "महिला", age_data["name_nepali"]))

            male_dominant_ages = [item[2] for item in age_dominance if item[1] == "पुरुष"]
            female_dominant_ages = [
                item[2] for item in age_dominance if item[1] == "महिला"
            ]

            if male_dominant_ages:
                analysis_parts.append(
                    f"उमेर समूह अनुसार हेर्दा {', '.join(str(x) for x in male_dominant_ages)} उमेर समूहमा पुरुषको बाहुल्यता रहेको छ ।"
                )

            if female_dominant_ages:
                analysis_parts.append(
                    f"बाँकी उमेर समूहमा {', '.join(str(x) for x in female_dominant_ages)} उमेर समूहमा महिलाको बाहुल्ता रहेको छ ।"
                )

            # Youth and reproductive age analysis
            youth_pop = indicators["youth_population"]
            youth_pct = indicators["youth_percentage"]
            reproductive_women = indicators["reproductive_age_women"]
            reproductive_pct = indicators["reproductive_women_percentage"]

            analysis_parts.append(
                f"युवा उमेरको (१५ देखि ३९ वर्ष) जनसंख्या {format_nepali_number(youth_pop)} "
                f"({format_nepali_percentage(youth_pct)}%) रहेको छ, जसले जनसंख्याको लाभांशको संकेत गर्दछ ।"
            )

            analysis_parts.append(
                f"प्रजनन उमेरका महिलाहरू (१५ देखि ४९ वर्ष) {format_nepali_number(reproductive_women)} "
                f"({format_nepali_percentage(reproductive_pct)}%) रहेका छन्, जसले प्रजनन स्वास्थ्य सेवाको आवश्यकतालाई जनाउँछ ।"
            )

            # Dependency ratio analysis
            child_dep = dependency_ratios["child_dependency_ratio"]
            elderly_dep = dependency_ratios["elderly_dependency_ratio"]
            total_dep = dependency_ratios["total_dependency_ratio"]

            analysis_parts.append(
                f"निर्भरता अनुपातका आधारमा हेर्दा बाल निर्भरता अनुपात {format_nepali_percentage(child_dep)}% र "
                f"वृद्ध निर्भरता अनुपात {format_nepali_percentage(elderly_dep)}% रहेको छ । "
                f"कुल निर्भरता अनुपात {format_nepali_percentage(total_dep)}% रहेको छ ।"
            )

            # Age-specific policy recommendations
            analysis_parts.append(
                "उमेर समूह अनुसार हेर्दा १५ देखि ३९ वर्ष उमेर समूह भित्रका किशोरी र महिलाहरूको जनसंख्यामा र "
                "उमेर पुगेका महिलाहरूको शारिरिक, मानसिक, सामाजिक तथा आर्थिक मुद्दाहरूलाई सम्बोधन गर्ने प्रकारको "
                "योजनाहरू निर्माण गर्नु जरुरी छ ।"
            )

            # Specific women's health and rights issues
            analysis_parts.append(
                "प्रजनन स्वास्थ्य, यौन स्वास्थ्य, रजस्वला सम्बन्धी समस्याहरू, महिला मैत्री शौचालय, परामर्श केन्द्रहरू, "
                "महिला हिंसा, छाउपडी प्रथा, घरेलु लैङ्गिक हिंसा, पाठेघर खस्ने समस्या, दाइजो प्रथा, बाल विवाह, "
                "महिला सशक्तिकरण तथा अधिकार जस्ता विषयहरू आम महिलाका लागि प्रमुख तथा संवेदनशील विषय भएकाले "
                "गाउँपालिकाले यी विषयहरूको प्रभावकारी योजना निर्माण गरी कार्यान्वयन गर्नुपर्ने संकेत समग्र तथ्याङ्कले गर्दछ ।"
            )

            # Youth demographic dividend and challenges
            analysis_parts.append(
                f"युवा उमेरको (१५ देखि ३९ वर्ष) जनसंख्या {format_nepali_percentage(youth_pct)}% "
                "हुनु राम्रो भए तापनि उनीहरूको शिक्षा, स्वास्थ्य तथा मानव संसाधन विकासमा राज्यले व्यापक लगानी गर्नुपर्ने हुन्छ । "
                "युवा उमेर समूह धेरै हुनुलाई जनसंख्याको लाभांश भनिन्छ । अर्कोतर्फ युवाहरूलाई सही दिशातर्फ उन्मुख बनाउन र "
                "रोजगारीका अवसरहरू सिर्जना गरी राष्ट्र निर्माणमा सहभागी बनाउनु समाज र राज्यको दायित्व हुन आउँछ ।"
            )

            # Child and elderly population analysis
            child_pop = dependency_ratios["child_population"]
            elderly_pop = dependency_ratios["elderly_population"]
            working_age_pop = dependency_ratios["working_age_population"]

            analysis_parts.append(
                f"बालबालिका तथा शिशुहरूको संख्या {format_nepali_number(child_pop)} "
                f"({format_nepali_percentage(child_pop/total_pop*100)}%) हुनुले क्रमशः प्रजनन दर घट्दै गएको संकेत गर्दछ "
                f"भने वृद्धवृद्धाहरूको संख्या {format_nepali_number(elderly_pop)} "
                f"({format_nepali_percentage(elderly_pop/total_pop*100)}%) हुनुले औसत आयु अन्य देशहरूको तुलनामा कम हुनु र "
                "प्रौढ अवस्थामा लाग्ने रोगका कारण पाका उमेरको जनसंख्याको मृत्युदर बढी हुनु भन्ने जनाउँछ ।"
            )

            # Service delivery implications
            analysis_parts.append(
                "उमेरअनुसारको जनसंख्याको विश्लेषण गर्दा प्रत्येक उमेर समूहका आवश्यकताहरू सम्बोधन गरी उनीहरूको उचित "
                "व्यवस्थापन गर्नु नै चुनौतीपूर्ण हुन्छ । बालबालिकाको पोषण र स्याहार तथा शिक्षा, युवालाई उचित रोजगारी र "
                "वृद्धहरूलाई आवश्यक सामाजिक सुरक्षा तथा स्वास्थ्य सेवा र स्याहार राज्यले निर्वाह गर्नुपर्ने दायित्वहरू भित्र आउँछन् ।"
            )

            # Ward-wise analysis
            ward_analysis = []
            for ward_num_str, ward_info in ward_data.items():
                ward_num = int(ward_num_str)  # Convert back to int for display
                ward_total = ward_info["total"]
                ward_male = ward_info["male"]
                ward_female = ward_info["female"]
                ward_male_pct = ward_info["male_percentage"]
                ward_female_pct = ward_info["female_percentage"]
                ward_analysis.append(
                    f"वडा नं. {format_nepali_number(ward_num)} मा कुल {format_nepali_number(ward_total)} जनसंख्या रहेको छ, "
                    f"जसमा {format_nepali_number(ward_male)} पुरुष ({format_nepali_percentage(ward_male_pct)}%) र "
                    f"{format_nepali_number(ward_female)} महिला ({format_nepali_percentage(ward_female_pct)}%) छन् ।"
                )

            analysis_parts.append(
                "वडागत विवरणमा "
                + " ".join(ward_analysis)
                + " यस विवरणलाई तालिकामा प्रस्तुत गरिएको छ ।"
            )

            # Conclusion and recommendations
            analysis_parts.append(
                "गाउँपालिकाले यसतर्फ ध्यान पुर्‍याउन आवश्यक छ । विशेष गरी महिला र बालबालिकाका मुद्दाहरूलाई प्राथमिकता दिएर "
                "उनीहरूको सामाजिक, आर्थिक र राजनीतिक सशक्तिकरणका लागि ठोस कार्यक्रमहरू सञ्चालन गर्नुपर्दछ । "
                "साथै युवाहरूलाई उत्पादनशील काममा लगाउन र वृद्धहरूको स्याहारका लागि उचित व्यवस्था मिलाउनुपर्दछ ।"
            )

            return " ".join(analysis_parts)

        def generate_formal_report(self, data):
            """Formal report for age-gender (required by abstract base class)."""
            # You can implement a formal report here if needed
            return ""
