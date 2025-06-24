"""
Major Skills Economics Processor

Handles major skills economics data processing, chart generation, and report formatting.
"""

from .base import BaseEconomicsProcessor, BaseEconomicsReportFormatter
from ..models import WardWiseMajorSkills, SkillTypeChoice
from apps.demographics.utils.svg_chart_generator import DEFAULT_COLORS
from apps.reports.utils.nepali_numbers import (
    format_nepali_number,
    format_nepali_percentage,
)


class MajorSkillsProcessor(BaseEconomicsProcessor):
    """Processor for major skills economics data"""

    def __init__(self):
        super().__init__()
        # Customize chart dimensions for major skills
        self.pie_chart_width = 900
        self.pie_chart_height = 450
        self.bar_chart_width = 1000
        self.bar_chart_height = 600
        self.chart_radius = 130
        # Set skill-specific colors with meaningful associations
        self.chart_generator.colors = {
            # Professional/Technical Skills
            "TEACHING_RELATED": "#2196F3",  # Blue - Education
            "ENGINEERING_DESIGN_RELATED": "#3F51B5",  # Indigo - Technical
            "COMPUTER_SCIENCE_RELATED": "#673AB7",  # Deep Purple - IT
            "HUMAN_HEALTH_RELATED": "#E91E63",  # Pink - Healthcare
            "ANIMAL_HEALTH_RELATED": "#9C27B0",  # Purple - Veterinary
            # Skilled Trades
            "CARPENTERY_RELATED": "#795548",  # Brown - Woodwork
            "PLUMBING": "#00BCD4",  # Cyan - Water/Plumbing
            "ELECTRICITY_INSTALLMENT_RELATED": "#FFC107",  # Amber - Electrical
            "MECHANICS_RELATED": "#607D8B",  # Blue Grey - Machinery
            "FURNITURE_RELATED": "#8BC34A",  # Light Green - Crafts
            # Agriculture & Primary
            "AGRICULTURE_RELATED": "#4CAF50",  # Green - Agriculture
            "LAND_SURVEY_RELATED": "#009688",  # Teal - Surveying
            # Service Industry
            "DRIVING_RELATED": "#FF5722",  # Deep Orange - Transport
            "HOTEL_RESTAURANT_RELATED": "#FF9800",  # Orange - Hospitality
            "PHOTOGRAPHY_RELATED": "#9E9E9E",  # Grey - Services
            # Creative & Cultural
            "MUSIC_DRAMA_RELATED": "#E1BEE7",  # Light Purple - Arts
            "LITERARY_CREATION_RELATED": "#F8BBD9",  # Light Pink - Literature
            "HANDICRAFT_RELATED": "#DCEDC8",  # Light Green - Crafts
            # Personal Services
            "SEWING_RELATED": "#FCE4EC",  # Light Pink - Textiles
            "BEUATICIAN_RELATED": "#F3E5F5",  # Light Purple - Beauty
            "JWELLERY_MAKING_RELATED": "#FFF9C4",  # Light Yellow - Jewelry
            # Specialized Skills
            "SELF_PROTECTION_RELATED": "#FFCDD2",  # Light Red - Security
            "STONEWORK_WOODWORK": "#EFEBE9",  # Light Brown - Construction
            "RADIO_TELEVISION_ELECTRICAL_REPAIR": "#E0F2F1",  # Light Teal - Repair
            "PRINTING_RELATED": "#E8F5E8",  # Light Green - Printing
            "SHOEMAKING_RELATED": "#FFF3E0",  # Light Orange - Leather
            # General Categories
            "OTHER": "#9E9E9E",  # Grey - Other
            "NONE": "#757575",  # Medium Grey - No Skills
        }

    def get_section_title(self):
        return "प्राविधिक, सीपयुक्त तथा विशेष दक्षता भएका मानव संशाधनको विवरण"

    def get_section_number(self):
        return "४.१.१"

    def get_data(self):
        """Get major skills data - both municipality-wide and ward-wise"""
        # Municipality-wide summary
        municipality_data = {}
        skill_types = dict(SkillTypeChoice.choices)
        for skill_code, skill_name in skill_types.items():
            municipality_data[skill_code] = {
                "population": 0,
                "percentage": 0.0,
                "name_nepali": skill_name,
            }

        # Dynamically determine all ward numbers from the data (now supports up to 8 wards)
        all_wards = sorted(
            set(WardWiseMajorSkills.objects.values_list("ward_number", flat=True))
        )
        ward_data = {}
        for ward_num in all_wards:
            ward_data[ward_num] = {
                "ward_name": f"वडा नं. {ward_num}",
                "demographics": {},
            }
            # Initialize skills for each ward
            for skill_code, skill_name in skill_types.items():
                ward_data[ward_num]["demographics"][skill_code] = {
                    "population": 0,
                    "percentage": 0.0,
                    "name_nepali": skill_name,
                }

        # Get actual data from database
        total_population = 0
        for skill_obj in WardWiseMajorSkills.objects.all():
            skill = skill_obj.skill_type
            ward_num = skill_obj.ward_number
            population = skill_obj.population

            # Add to municipality-wide totals
            if skill in municipality_data:
                municipality_data[skill]["population"] += population
                total_population += population

            # Add to ward-wise data
            if ward_num in ward_data and skill in ward_data[ward_num]["demographics"]:
                ward_data[ward_num]["demographics"][skill]["population"] += population

        # Calculate percentages for municipality-wide data
        if total_population > 0:
            for skill, data in municipality_data.items():
                data["percentage"] = (data["population"] / total_population) * 100

        # Calculate ward totals and percentages
        for ward_num, ward_info in ward_data.items():
            ward_total = sum(
                demo["population"] for demo in ward_info["demographics"].values()
            )
            ward_info["total_population"] = ward_total

            # Calculate percentages within each ward
            if ward_total > 0:
                for skill, demo in ward_info["demographics"].items():
                    demo["percentage"] = (demo["population"] / ward_total) * 100

        return {
            "municipality_data": municipality_data,
            "ward_data": ward_data,
            "total_population": total_population,
        }

    def generate_report_content(self, data):
        """Generate major skills-specific report content"""
        formatter = self.MajorSkillsReportFormatter()
        return formatter.generate_formal_report(
            data["municipality_data"], data["ward_data"], data["total_population"]
        )

    def get_chart_key(self):
        """Get the key for storing charts in PDF context"""
        return "major_skills"

    def generate_chart_svg(self, data, chart_type="pie"):
        """Generate major skills chart SVG using SVGChartGenerator"""
        if chart_type == "pie":
            return self.chart_generator.generate_pie_chart_svg(
                data["municipality_data"],
                include_title=False,
                title_nepali="मुख्य सीपका आधारमा वितरण",
                title_english="Distribution by Major Skills",
            )
        elif chart_type == "bar":
            return self.chart_generator.generate_bar_chart_svg(
                data["ward_data"],
                include_title=False,
                title_nepali="वडा अनुसार मुख्य सीपका आधारमा वितरण",
                title_english="Major Skills Distribution by Ward",
            )
        return None

    def generate_and_save_charts(self, data):
        """Generate and save both pie and bar charts for major skills data"""
        charts = {}
        category_name = "major_skills"

        # Determine data structure - check if it's standard format or simple format
        if (
            isinstance(data, dict)
            and "municipality_data" in data
            and "ward_data" in data
        ):
            # Standard format with both municipality and ward data
            pie_data = data["municipality_data"]
            bar_data = data["ward_data"]
        else:
            # Simple format - use the data as is for pie chart
            pie_data = data
            bar_data = None  # No ward data available for bar chart

        # Transform data for chart generator (population -> population)
        transformed_pie_data = {}
        for key, value in pie_data.items():
            if isinstance(value, dict) and value.get("population", 0) > 0:
                transformed_pie_data[key] = {
                    "population": value["population"],
                    "name_nepali": value.get("name_nepali", key),
                    "percentage": value.get("percentage", 0),
                }

        # Transform ward data for bar chart
        transformed_bar_data = None
        if bar_data:
            transformed_bar_data = {}
            for ward_num, ward_info in bar_data.items():
                transformed_bar_data[ward_num] = {
                    "ward_name": ward_info.get("ward_name", f"वडा नं. {ward_num}"),
                    "demographics": {},
                }
                # Transform demographics to demographics with population
                if "demographics" in ward_info:
                    for skill_code, skill_data in ward_info["demographics"].items():
                        if skill_data.get("population", 0) > 0:
                            transformed_bar_data[ward_num]["demographics"][
                                skill_code
                            ] = {
                                "population": skill_data["population"],
                                "name_nepali": skill_data.get(
                                    "name_nepali", skill_code
                                ),
                                "percentage": skill_data.get("percentage", 0),
                            }

        # Generate pie chart using SVGChartGenerator
        success, png_path, svg_path = self.chart_generator.generate_chart_image(
            demographic_data=transformed_pie_data,
            output_name=f"{category_name}_pie_chart",
            static_dir=str(self.static_charts_dir),
            chart_type="pie",
            include_title=False,
        )

        if success and png_path:
            charts["pie_chart_png"] = f"images/charts/{category_name}_pie_chart.png"
            charts["pie_chart_svg"] = f"images/charts/{category_name}_pie_chart.svg"
        elif svg_path:
            # Fallback to SVG if PNG conversion fails
            charts["pie_chart_svg"] = f"images/charts/{category_name}_pie_chart.svg"

        # Generate bar chart only if ward data is available
        if transformed_bar_data:
            success, png_path, svg_path = self.chart_generator.generate_chart_image(
                demographic_data=transformed_bar_data,
                output_name=f"{category_name}_bar_chart",
                static_dir=str(self.static_charts_dir),
                chart_type="bar",
                include_title=False,
            )

            if success and png_path:
                charts["bar_chart_png"] = f"images/charts/{category_name}_bar_chart.png"
                charts["bar_chart_svg"] = f"images/charts/{category_name}_bar_chart.svg"
            elif svg_path:
                # Fallback to SVG if PNG conversion fails
                charts["bar_chart_svg"] = f"images/charts/{category_name}_bar_chart.svg"

        return charts

    class MajorSkillsReportFormatter(BaseEconomicsReportFormatter):
        """Major skills-specific report formatter"""

        def generate_formal_report(self, skills_data, ward_data, total_population):
            """Generate major skills formal report content"""

            # Find major skills
            major_skills = []
            for skill_type, data in skills_data.items():
                if data["population"] > 0:
                    major_skills.append(
                        (data["name_nepali"], data["population"], data["percentage"])
                    )

            major_skills.sort(key=lambda x: x[1], reverse=True)

            # Build comprehensive analysis
            content = []

            # Introduction
            nepali_total = format_nepali_number(total_population)
            content.append(
                f"""गढवा गाउँपालिकामा कुल {nepali_total} जनसंख्यासँग विभिन्न सीप र कौशलताहरू छन् । मुख्य सीपका आधारमा जनसंख्याको वितरण गर्दा गाउँपालिकाको मानव संसाधनको गुणस्तर र आर्थिक क्षमताको अवस्था देखिन्छ ।"""
            )

            # Top skills analysis
            if len(major_skills) >= 3:
                top_three = major_skills[:3]
                first_skill = top_three[0]
                second_skill = top_three[1]
                third_skill = top_three[2]

                first_pop = format_nepali_number(first_skill[1])
                first_pct = format_nepali_percentage(first_skill[2])
                second_pop = format_nepali_number(second_skill[1])
                second_pct = format_nepali_percentage(second_skill[2])
                third_pop = format_nepali_number(third_skill[1])
                third_pct = format_nepali_percentage(third_skill[2])

                content.append(
                    f"""सबैभन्दा बढी {first_pop} जनसंख्या अर्थात् {first_pct} प्रतिशत {first_skill[0]} सीप भएका छन् भने दोस्रोमा {second_pop} जनसंख्या अर्थात् {second_pct} प्रतिशत {second_skill[0]} र तेस्रोमा {third_pop} जनसंख्या अर्थात् {third_pct} प्रतिशत {third_skill[0]} सीप भएका छन् ।"""
                )

            # Technical and professional skills
            technical_keywords = ["शिक्षा", "इन्जिनियरिङ", "कम्प्युटर", "स्वास्थ्य"]
            technical_skills = []
            for skill in major_skills:
                if any(keyword in skill[0] for keyword in technical_keywords):
                    technical_skills.append(skill)

            if technical_skills:
                technical_total = sum(skill[1] for skill in technical_skills)
                technical_pct = (
                    (technical_total / total_population * 100)
                    if total_population > 0
                    else 0
                )
                content.append(
                    f"""प्राविधिक र व्यावसायिक सीपमा {format_nepali_number(technical_total)} जनसंख्या ({format_nepali_percentage(technical_pct)} प्रतिशत) संलग्न छन् जसले गाउँपालिकामा उच्च गुणस्तरको मानव संसाधनको उपस्थिति देखाउँछ ।"""
                )

            # Skilled crafts and trades
            craft_keywords = ["काष्ठकला", "प्लम्बिङ", "बिजुली", "मेकानिक"]
            craft_skills = []
            for skill in major_skills:
                if any(keyword in skill[0] for keyword in craft_keywords):
                    craft_skills.append(skill)

            if craft_skills:
                craft_total = sum(skill[1] for skill in craft_skills)
                craft_pct = (
                    (craft_total / total_population * 100)
                    if total_population > 0
                    else 0
                )
                content.append(
                    f"""दक्ष शिल्पकारी र हस्तकलामा {format_nepali_number(craft_total)} जनसंख्या ({format_nepali_percentage(craft_pct)} प्रतिशत) संलग्न छन् जसले स्थानीय उत्पादन र निर्माण क्षेत्रमा योगदान पुर्याइरहेको छ ।"""
                )

            # Agricultural skills
            agriculture_skills = next(
                (skill for skill in major_skills if "कृषि" in skill[0]), None
            )
            if agriculture_skills:
                agri_pop = format_nepali_number(agriculture_skills[1])
                agri_pct = format_nepali_percentage(agriculture_skills[2])
                content.append(
                    f"""कृषि सम्बन्धी सीपमा {agri_pop} जनसंख्या ({agri_pct} प्रतिशत) संलग्न छन् जसले गाउँपालिकाको मुख्य आर्थिक आधार कृषिको विकासमा महत्वपूर्ण भूमिका खेलिरहेको छ ।"""
                )

            # Service sector skills
            service_keywords = ["ड्राइभिङ", "होटल", "फोटोग्राफी"]
            service_skills = []
            for skill in major_skills:
                if any(keyword in skill[0] for keyword in service_keywords):
                    service_skills.append(skill)

            if service_skills:
                service_total = sum(skill[1] for skill in service_skills)
                service_pct = (
                    (service_total / total_population * 100)
                    if total_population > 0
                    else 0
                )
                content.append(
                    f"""सेवा उद्योगमा {format_nepali_number(service_total)} जनसंख्या ({format_nepali_percentage(service_pct)} प्रतिशत) संलग्न छन् जसले पर्यटन र सेवा क्षेत्रको विकासमा योगदान पुर्याइरहेको छ ।"""
                )

            # Creative and cultural skills
            creative_skills = next(
                (
                    skill
                    for skill in major_skills
                    if "संगीत" in skill[0]
                    or "साहित्य" in skill[0]
                    or "हस्तशिल्प" in skill[0]
                ),
                None,
            )
            if creative_skills:
                creative_pop = format_nepali_number(creative_skills[1])
                creative_pct = format_nepali_percentage(creative_skills[2])
                content.append(
                    f"""सिर्जनशील र सांस्कृतिक सीपमा {creative_pop} जनसंख्या ({creative_pct} प्रतिशत) संलग्न छन् जसले सांस्कृतिक संरक्षण र सिर्जनशील अर्थतन्त्रको विकासमा योगदान पुर्याइरहेको छ ।"""
                )

            # Economic development potential
            content.append(
                """मुख्य सीपको यो विविधताले गाउँपालिकामा बहुआयामिक आर्थिक विकासको सम्भावना देखाउँछ । प्राविधिक सीप, दक्ष शिल्पकारी र सेवा उद्योगको संयोजनले संतुलित आर्थिक संरचना निर्माण गर्न सहयोग पुर्याएको छ ।"""
            )

            # Skills development recommendations
            content.append(
                """भविष्यमा सीप विकास कार्यक्रमहरू मार्फत युवाहरूलाई आधुनिक प्रविधि र बजार माग अनुकूलका सीपहरू सिकाएर रोजगारीको अवसर बृद्धि गर्न सकिन्छ । विशेष गरी डिजिटल सीप, उद्यमशीलता र नवाचार क्षेत्रमा जोड दिनुपर्छ ।"""
            )

            # Human resource utilization
            content.append(
                """वडागत रूपमा सीपको वितरणमा भिन्नता रहेको देखिन्छ । यो विविधताले गाउँपालिकामा मानव संसाधनको संतुलित उपयोगमा योगदान पुर्याएको छ र स्थानीय आर्थिक गतिविधिलाई गतिशील बनाएको छ ।"""
            )

            # Future opportunities
            content.append(
                """स्थानीय सीप र ज्ञानको आधारमा साना उद्योग, कुटीर उद्योग र सामुदायिक उद्यमहरू स्थापना गरी आत्मनिर्भर अर्थतन्त्रको विकास गर्न सकिने सम्भावना छ । सहकारी संस्थाहरूको माध्यमबाट सीपमूलक व्यवसाय प्रवर्द्धन गर्नुपर्छ ।"""
            )

            return " ".join(content)

    def process_for_pdf(self):
        """Process major skills data for PDF generation including charts"""
        # Get raw data
        data = self.get_data()

        # Generate analysis text
        coherent_analysis = self.generate_report_content(data)

        # Generate and save charts
        charts = self.generate_and_save_charts(data)

        # Calculate total population
        total_count = data.get("total_population", 0)

        return {
            "data": data,
            "report_content": coherent_analysis,
            "charts": charts,
            "total_population": total_count,
            "section_title": self.get_section_title(),
            "section_number": self.get_section_number(),
        }
