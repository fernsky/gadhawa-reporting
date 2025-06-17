"""
Major Skills Economics Processor

Handles major skills economics data processing, chart generation, and report formatting.
"""

from django.db import models
from .base import BaseEconomicsProcessor, BaseEconomicsReportFormatter
from ..models import WardWiseMajorSkills, SkillTypeChoice
from apps.reports.utils.nepali_numbers import (
    format_nepali_number,
    format_nepali_percentage,
)


class MajorSkillsProcessor(BaseEconomicsProcessor):
    """Processor for major skills economics data"""

    def __init__(self):
        super().__init__()
        # Customize chart dimensions for major skills
        self.pie_chart_width = 950
        self.pie_chart_height = 500
        self.chart_radius = 150
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
        """Get ward wise major skills data"""
        # Municipality-wide summary
        skill_data = {}
        total_population = 0

        for skill_choice in SkillTypeChoice.choices:
            skill_code = skill_choice[0]
            skill_name = skill_choice[1]

            skill_population = (
                WardWiseMajorSkills.objects.filter(skill_type=skill_code).aggregate(
                    total=models.Sum("population")
                )["total"]
                or 0
            )

            if skill_population > 0:  # Only include skills with population
                skill_data[skill_code] = {
                    "name_english": skill_code,
                    "name_nepali": skill_name,
                    "population": skill_population,
                    "percentage": 0,  # Will be calculated below
                }
                total_population += skill_population

        # Calculate percentages
        for skill_code in skill_data:
            if total_population > 0:
                skill_data[skill_code]["percentage"] = (
                    skill_data[skill_code]["population"] / total_population * 100
                )

        # Ward-wise data
        ward_data = {}
        for ward_num in range(1, 8):  # Wards 1-7
            ward_population = (
                WardWiseMajorSkills.objects.filter(ward_number=ward_num).aggregate(
                    total=models.Sum("population")
                )["total"]
                or 0
            )

            if ward_population > 0:
                ward_data[ward_num] = {
                    "ward_number": ward_num,
                    "ward_name": f"वडा नं. {ward_num}",
                    "total_population": ward_population,
                    "skill_types": {},
                }

                # Skill type breakdown for this ward
                for skill_choice in SkillTypeChoice.choices:
                    skill_code = skill_choice[0]
                    skill_name = skill_choice[1]

                    skill_population_ward = (
                        WardWiseMajorSkills.objects.filter(
                            ward_number=ward_num, skill_type=skill_code
                        ).aggregate(total=models.Sum("population"))["total"]
                        or 0
                    )

                    if skill_population_ward > 0:
                        ward_data[ward_num]["skill_types"][skill_code] = {
                            "name_nepali": skill_name,
                            "population": skill_population_ward,
                            "percentage": (
                                (skill_population_ward / ward_population * 100)
                                if ward_population > 0
                                else 0
                            ),
                        }

        # Prepare top skills list
        top_skills = []
        for skill_code, skill_info in skill_data.items():
            top_skills.append(
                {
                    "skill_code": skill_code,
                    "skill_name": skill_info["name_nepali"],
                    "population": skill_info["population"],
                    "percentage": skill_info["percentage"],
                }
            )

        # Sort by population (descending)
        top_skills.sort(key=lambda x: x["population"], reverse=True)

        # Categorize skills by economic sector
        skill_categories = self._categorize_skills_by_sector(
            skill_data, total_population
        )

        return {
            "municipality_data": skill_data,
            "ward_data": ward_data,
            "total_population": total_population,
            "top_skills": top_skills,
            "skill_categories": skill_categories,
        }

    def _categorize_skills_by_sector(self, skill_data, total_population):
        """Categorize skills into economic sectors"""
        categories = {
            "professional_technical": {
                "name": "व्यावसायिक र प्राविधिक",
                "skills": [
                    "TEACHING_RELATED",
                    "ENGINEERING_DESIGN_RELATED",
                    "COMPUTER_SCIENCE_RELATED",
                    "HUMAN_HEALTH_RELATED",
                    "ANIMAL_HEALTH_RELATED",
                    "LAND_SURVEY_RELATED",
                ],
                "population": 0,
                "percentage": 0,
                "economic_impact": "उच्च",
            },
            "skilled_trades": {
                "name": "दक्ष शिल्पकारी",
                "skills": [
                    "CARPENTERY_RELATED",
                    "PLUMBING",
                    "ELECTRICITY_INSTALLMENT_RELATED",
                    "MECHANICS_RELATED",
                    "FURNITURE_RELATED",
                    "STONEWORK_WOODWORK",
                ],
                "population": 0,
                "percentage": 0,
                "economic_impact": "मध्यम-उच्च",
            },
            "agriculture_primary": {
                "name": "कृषि र प्राथमिक",
                "skills": ["AGRICULTURE_RELATED"],
                "population": 0,
                "percentage": 0,
                "economic_impact": "मध्यम",
            },
            "service_industry": {
                "name": "सेवा उद्योग",
                "skills": [
                    "DRIVING_RELATED",
                    "HOTEL_RESTAURANT_RELATED",
                    "PHOTOGRAPHY_RELATED",
                    "BEUATICIAN_RELATED",
                ],
                "population": 0,
                "percentage": 0,
                "economic_impact": "मध्यम",
            },
            "creative_cultural": {
                "name": "सिर्जनशील र सांस्कृतिक",
                "skills": [
                    "MUSIC_DRAMA_RELATED",
                    "LITERARY_CREATION_RELATED",
                    "HANDICRAFT_RELATED",
                ],
                "population": 0,
                "percentage": 0,
                "economic_impact": "न्यून-मध्यम",
            },
            "personal_services": {
                "name": "व्यक्तिगत सेवा",
                "skills": [
                    "SEWING_RELATED",
                    "JWELLERY_MAKING_RELATED",
                    "SELF_PROTECTION_RELATED",
                ],
                "population": 0,
                "percentage": 0,
                "economic_impact": "न्यून",
            },
            "others": {
                "name": "अन्य र अपरिभाषित",
                "skills": ["OTHER", "NONE"],
                "population": 0,
                "percentage": 0,
                "economic_impact": "अनुसन्धान आवश्यक",
            },
        }

        # Calculate population for each category
        for category_key, category_info in categories.items():
            for skill_code in category_info["skills"]:
                if skill_code in skill_data:
                    category_info["population"] += skill_data[skill_code]["population"]

            # Calculate percentage
            if total_population > 0:
                category_info["percentage"] = (
                    category_info["population"] / total_population
                ) * 100

        return categories

    def generate_analysis_text(self, data):
        """Generate comprehensive analysis text for major skills"""
        if not data or data["total_population"] == 0:
            return "मुख्य सीपको तथ्याङ्क उपलब्ध छैन।"

        total_population = data["total_population"]
        municipality_data = data["municipality_data"]
        ward_data = data["ward_data"]
        skill_categories = data["skill_categories"]

        analysis_parts = []

        # Overall summary
        analysis_parts.append(
            f"लुङ्ग्री गाउँपालिकामा कुल {format_nepali_number(total_population)} जना दक्ष जनशक्तिको विविध सीपको विश्लेषण गर्दा विभिन्न क्षेत्रहरूमा विशेषज्ञता देखिन्छ।"
        )

        # Dominant skill analysis
        if municipality_data:
            # Find the most common skill
            dominant_skill = max(
                municipality_data.items(), key=lambda x: x[1]["population"]
            )
            analysis_parts.append(
                f"सीपको आधारमा विश्लेषण गर्दा, {dominant_skill[1]['name_nepali']} सबैभन्दा बढी "
                f"{format_nepali_number(dominant_skill[1]['population'])} जना "
                f"({format_nepali_percentage(dominant_skill[1]['percentage'])}) मा देखिन्छ।"
            )

            # Professional and technical skills analysis
            professional_skills = [
                "TEACHING_RELATED",
                "ENGINEERING_DESIGN_RELATED",
                "COMPUTER_SCIENCE_RELATED",
                "HUMAN_HEALTH_RELATED",
                "ANIMAL_HEALTH_RELATED",
            ]
            professional_population = sum(
                municipality_data.get(skill, {}).get("population", 0)
                for skill in professional_skills
            )
            professional_percentage = (
                (professional_population / total_population * 100)
                if total_population > 0
                else 0
            )

            if professional_percentage > 0:
                analysis_parts.append(
                    f"व्यावसायिक र प्राविधिक सीप क्षेत्रमा {format_nepali_number(professional_population)} जना "
                    f"({format_nepali_percentage(professional_percentage)}) शिक्षण, इन्जिनियरिङ, कम्प्युटर, स्वास्थ्य "
                    f"जस्ता उच्च गुणस्तरका सीपहरूमा दक्ष छन्। यसले ज्ञानमा आधारित अर्थतन्त्रको विकासमा योगदान पुर्‍याउँछ।"
                )

            # Skilled trades analysis
            trades_skills = [
                "CARPENTERY_RELATED",
                "PLUMBING",
                "ELECTRICITY_INSTALLMENT_RELATED",
                "MECHANICS_RELATED",
                "FURNITURE_RELATED",
            ]
            trades_population = sum(
                municipality_data.get(skill, {}).get("population", 0)
                for skill in trades_skills
            )
            trades_percentage = (
                (trades_population / total_population * 100)
                if total_population > 0
                else 0
            )

            if trades_percentage > 0:
                analysis_parts.append(
                    f"दक्ष शिल्पकारी क्षेत्रमा {format_nepali_number(trades_population)} जना "
                    f"({format_nepali_percentage(trades_percentage)}) सिकर्मी, प्लम्बिंग, बिजुली, मेकानिक्स "
                    f"जस्ता निर्माण र मर्मत सम्बन्धी काममा दक्ष छन्। यसले स्थानीय पूर्वाधार विकासमा सहयोग पुर्‍याउँछ।"
                )

            # Agriculture related skills
            if "AGRICULTURE_RELATED" in municipality_data:
                agri_population = municipality_data["AGRICULTURE_RELATED"]["population"]
                agri_percentage = municipality_data["AGRICULTURE_RELATED"]["percentage"]
                analysis_parts.append(
                    f"कृषि सम्बन्धी सीपमा {format_nepali_number(agri_population)} जना "
                    f"({format_nepali_percentage(agri_percentage)}) दक्ष छन्। यसले खाद्य सुरक्षा र "
                    f"कृषि उत्पादनमा गुणात्मक सुधारको संभावना देखाउँछ।"
                )

            # Service sector skills
            service_skills = [
                "DRIVING_RELATED",
                "HOTEL_RESTAURANT_RELATED",
                "PHOTOGRAPHY_RELATED",
            ]
            service_population = sum(
                municipality_data.get(skill, {}).get("population", 0)
                for skill in service_skills
            )
            service_percentage = (
                (service_population / total_population * 100)
                if total_population > 0
                else 0
            )

            if service_percentage > 0:
                analysis_parts.append(
                    f"सेवा उद्योग क्षेत्रमा {format_nepali_number(service_population)} जना "
                    f"({format_nepali_percentage(service_percentage)}) चालक, होटल, फोटोग्राफी "
                    f"जस्ता सेवामुखी व्यापारमा सक्षम छन्। यसले पर्यटन र सेवा क्षेत्रको विकासमा योगदान पुर्‍याउँछ।"
                )

            # Creative and cultural skills
            creative_skills = [
                "MUSIC_DRAMA_RELATED",
                "HANDICRAFT_RELATED",
                "SEWING_RELATED",
            ]
            creative_population = sum(
                municipality_data.get(skill, {}).get("population", 0)
                for skill in creative_skills
            )
            creative_percentage = (
                (creative_population / total_population * 100)
                if total_population > 0
                else 0
            )

            if creative_percentage > 0:
                analysis_parts.append(
                    f"सिर्जनशील र सांस्कृतिक सीपमा {format_nepali_number(creative_population)} जना "
                    f"({format_nepali_percentage(creative_percentage)}) संगीत, हस्तकला, सिलाई "
                    f"जस्ता कलात्मक कार्यमा निपुण छन्। यसले सांस्कृतिक पर्यटन र स्थानीय उत्पादनमा योगदान पुर्‍याउँछ।"
                )

        # Ward-wise comparative analysis
        if ward_data and len(ward_data) > 1:
            # Find wards with highest and lowest skilled population
            ward_skill_counts = {}
            for ward_num, ward_info in ward_data.items():
                ward_skill_counts[ward_num] = ward_info["total_population"]

            highest_ward = max(ward_skill_counts.items(), key=lambda x: x[1])
            lowest_ward = min(ward_skill_counts.items(), key=lambda x: x[1])

            if highest_ward[0] != lowest_ward[0]:
                analysis_parts.append(
                    f"वडागत विश्लेषणमा, वडा नं. {highest_ward[0]} मा सबैभन्दा बढी "
                    f"{format_nepali_number(highest_ward[1])} दक्ष जनशक्ति छ "
                    f"भने वडा नं. {lowest_ward[0]} मा सबैभन्दा कम "
                    f"{format_nepali_number(lowest_ward[1])} दक्ष जनशक्ति छ।"
                )

            # Skill diversity analysis
            ward_diversity = {}
            for ward_num, ward_info in ward_data.items():
                ward_diversity[ward_num] = len(ward_info["skill_types"])

            most_diverse_ward = max(ward_diversity.items(), key=lambda x: x[1])
            analysis_parts.append(
                f"सीप विविधताको दृष्टिकोणले हेर्दा, वडा नं. {most_diverse_ward[0]} मा सबैभन्दा बढी "
                f"{format_nepali_number(most_diverse_ward[1])} प्रकारका सीपहरू देखिन्छन्।"
            )

        # Economic impact analysis
        analysis_parts.append(
            "दक्ष जनशक्तिको उपस्थितिले स्थानीय अर्थतन्त्रमा सकारात्मक प्रभाव पारेको छ। "
            "विविध सीपहरूले रोजगारी सिर्जना, उत्पादकत्व वृद्धि र आय आर्जनमा योगदान पुर्‍याएको छ।"
        )

        # Gender implications
        analysis_parts.append(
            "सिलाई, सौन्दर्य, हस्तकला जस्ता सीपहरूले महिला सशक्तिकरणमा विशेष योगदान पुर्‍याएको छ। "
            "यसले लैङ्गिक समानता र आर्थिक स्वावलम्बनमा सहयोग पुर्‍याएको छ।"
        )

        # Employment and entrepreneurship
        analysis_parts.append(
            "दक्ष जनशक्तिले स्वरोजगार र साना उद्यमहरूको विकासमा महत्वपूर्ण भूमिका खेलेको छ। "
            "यसले बेरोजगारी न्यूनीकरण र आर्थिक गतिविधि बृद्धिमा योगदान पुर्‍याएको छ।"
        )

        # Technology and modernization
        if "COMPUTER_SCIENCE_RELATED" in municipality_data:
            analysis_parts.append(
                "कम्प्युटर र सूचना प्रविधि सम्बन्धी सीपले डिजिटल साक्षरता र आधुनिकीकरणमा योगदान पुर्‍याएको छ। "
                "यसले ई-गभर्नेन्स र डिजिटल अर्थतन्त्रको विकासमा सहयोग पुर्‍याउँछ।"
            )

        # Future development recommendations
        analysis_parts.append(
            "भविष्यमा सीप विकास कार्यक्रमहरू, व्यावसायिक तालिम र नवाचार केन्द्रहरूको स्थापना गरी "
            "दक्ष जनशक्ति उत्पादनमा वृद्धि गर्नुपर्छ।"
        )

        # Market linkage importance
        analysis_parts.append(
            "दक्ष जनशक्तिको उत्पादन र सेवालाई बजारसँग जोड्न उद्यमशीलता विकास, वित्तीय पहुँच र "
            "मार्केटिङ सहयोग आवश्यक छ।"
        )

        return " ".join(analysis_parts)

    def generate_pie_chart(self, data, title="मुख्य सीप अनुसार दक्ष जनशक्ति वितरण"):
        """Generate pie chart for major skills data"""
        return self.chart_generator.generate_pie_chart_svg(
            data,
            include_title=False,
            title_nepali=title,
            title_english="Skilled Workforce Distribution by Major Skills",
        )

    def process_for_pdf(self):
        """Process major skills data for PDF generation including charts"""
        # Get raw data
        data = self.get_data()

        # Generate analysis text
        coherent_analysis = self.generate_analysis_text(data)

        # Generate and save charts
        charts = self.generate_and_save_charts(data)

        # Calculate total population
        total_count = data.get("total_population", 0)

        return {
            "municipality_data": data.get("municipality_data", {}),
            "ward_data": data.get("ward_data", {}),
            "total_population": total_count,
            "top_skills": data.get("top_skills", []),
            "skill_categories": data.get("skill_categories", {}),
            "coherent_analysis": coherent_analysis,
            "pdf_charts": {"major_skills": charts},
            "section_title": self.get_section_title(),
            "section_number": self.get_section_number(),
        }


class MajorSkillsReportFormatter(BaseEconomicsReportFormatter):
    """Report formatter for major skills economics data"""

    def __init__(self, processor_data):
        super().__init__(processor_data)

    def format_for_html(self):
        """Format data for HTML template rendering"""
        return {
            "municipality_data": self.data["municipality_data"],
            "ward_data": self.data["ward_data"],
            "total_population": self.data["total_population"],
            "top_skills": self.data["top_skills"],
            "skill_categories": self.data["skill_categories"],
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
                "skill_types": len(self.data["municipality_data"]),
                "wards": len(self.data["ward_data"]),
            },
            "skills_breakdown": self.data["municipality_data"],
            "ward_breakdown": self.data["ward_data"],
            "skill_categories": self.data["skill_categories"],
            "analysis": self.data["coherent_analysis"],
        }
