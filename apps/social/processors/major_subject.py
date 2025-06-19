"""
Ward Wise Major Subject Social Processor

Handles ward wise major subject educational data processing, chart generation, and report formatting.
"""

from django.db import models
from .base import BaseSocialProcessor, BaseSocialReportFormatter
from ..models import WardWiseMajorSubject, MajorSubjectTypeChoice
from apps.reports.utils.nepali_numbers import (
    format_nepali_number,
    format_nepali_percentage,
    to_nepali_digits,
)


class MajorSubjectProcessor(BaseSocialProcessor):
    """Processor for ward wise major subject educational data"""

    def __init__(self):
        super().__init__()
        # Customize chart dimensions for major subject analysis
        self.pie_chart_width = 1000
        self.pie_chart_height = 600
        self.bar_chart_width = 1200
        self.bar_chart_height = 700
        self.chart_radius = 180

        # Set subject-specific colors with meaningful associations
        self.chart_generator.colors = {
            # Science & Technology
            "SCIENCE": "#2196F3",  # Blue - Pure Science
            "PHYSICS": "#1976D2",  # Dark Blue - Physics
            "CHEMISTRY": "#4CAF50",  # Green - Chemistry
            "BIOLOGY": "#8BC34A",  # Light Green - Biology
            "BOTANY": "#66BB6A",  # Green variant - Botany
            "ENGINEERING": "#FF9800",  # Orange - Engineering
            "MEDICINE": "#F44336",  # Red - Medicine
            "INFORMATION_TECHNOLOGY": "#9C27B0",  # Purple - IT
            "STATISTICS": "#795548",  # Brown - Statistics
            # Social Sciences & Humanities
            "NEPALI": "#E91E63",  # Pink - Nepali Language
            "ENGLISH": "#3F51B5",  # Indigo - English
            "HINDI": "#FF5722",  # Deep Orange - Hindi
            "SANSKRIT": "#FFC107",  # Amber - Sanskrit
            "HISTORY": "#607D8B",  # Blue Grey - History
            "GEOGRAPHY": "#00BCD4",  # Cyan - Geography
            "POLITICAL_SCIENCE": "#9E9E9E",  # Grey - Political Science
            "SOCIAL_SCIENCES": "#CDDC39",  # Lime - Social Sciences
            "PSYCHOLOGY": "#E1BEE7",  # Light Purple - Psychology
            "HUMANITIES": "#FFCDD2",  # Light Red - Humanities
            # Applied Sciences & Professional
            "ECONOMICS": "#4CAF50",  # Green - Economics
            "COMMERCE": "#2E7D32",  # Dark Green - Commerce
            "MANAGEMENT": "#1B5E20",  # Very Dark Green - Management
            "EDUCATION": "#FF6F00",  # Dark Orange - Education
            "EDUCATIONAL_SCIENCE": "#FF8F00",  # Orange variant - Educational Science
            "FORESTRY_AND_AGRICULTURE": "#689F38",  # Olive Green - Forestry & Agriculture
            "RURAL_DEVELOPMENT": "#827717",  # Dark Lime - Rural Development
            "HOME_ECONOMICS": "#E65100",  # Dark Orange - Home Economics
            "TOURISM": "#00695C",  # Dark Teal - Tourism
            "POPULATION_STUDY": "#5D4037",  # Brown - Population Study
            # Arts & Others
            "ARTS": "#8E24AA",  # Purple - Arts
            "OTHER": "#757575",  # Medium Grey - Other
        }

    def get_section_title(self):
        return "पाँच वर्ष र सोभन्दा माथिको शैक्षिक अवस्था (मुख्य विषय)"

    def get_section_number(self):
        return "५.१.२"

    def get_data(self):
        """Get ward wise major subject data"""
        # Municipality-wide summary
        subject_data = {}
        total_population = 0

        for subject_choice in MajorSubjectTypeChoice.choices:
            subject_code = subject_choice[0]
            subject_name = subject_choice[1]

            subject_population = (
                WardWiseMajorSubject.objects.filter(
                    subject_type=subject_code
                ).aggregate(total=models.Sum("population"))["total"]
                or 0
            )

            if subject_population > 0:  # Only include subjects with population
                subject_data[subject_code] = {
                    "name_english": subject_code,
                    "name_nepali": subject_name,
                    "population": subject_population,
                    "percentage": 0,  # Will be calculated below
                }
                total_population += subject_population

        # Calculate percentages
        for subject_code in subject_data:
            if total_population > 0:
                subject_data[subject_code]["percentage"] = (
                    subject_data[subject_code]["population"] / total_population * 100
                )

        # Ward-wise data
        ward_data = {}
        for ward_num in range(1, 8):  # Wards 1-7
            ward_population = (
                WardWiseMajorSubject.objects.filter(ward_number=ward_num).aggregate(
                    total=models.Sum("population")
                )["total"]
                or 0
            )

            if ward_population > 0:
                ward_data[ward_num] = {
                    "ward_number": ward_num,
                    "ward_name": f"वडा नं. {to_nepali_digits(ward_num)}",
                    "total_population": ward_population,
                    "subjects": {},
                }

                # Subject type breakdown for this ward
                for subject_choice in MajorSubjectTypeChoice.choices:
                    subject_code = subject_choice[0]
                    subject_name = subject_choice[1]

                    subject_population_ward = (
                        WardWiseMajorSubject.objects.filter(
                            ward_number=ward_num, subject_type=subject_code
                        ).aggregate(total=models.Sum("population"))["total"]
                        or 0
                    )

                    if subject_population_ward > 0:
                        ward_data[ward_num]["subjects"][subject_code] = {
                            "name_nepali": subject_name,
                            "population": subject_population_ward,
                            "percentage": (
                                (subject_population_ward / ward_population * 100)
                                if ward_population > 0
                                else 0
                            ),
                        }

        # Prepare top subjects list
        top_subjects = []
        for subject_code, subject_info in subject_data.items():
            top_subjects.append(
                {
                    "subject_code": subject_code,
                    "subject_name": subject_info["name_nepali"],
                    "population": subject_info["population"],
                    "percentage": subject_info["percentage"],
                }
            )

        # Sort by population (descending)
        top_subjects.sort(key=lambda x: x["population"], reverse=True)

        # Categorize subjects by field
        field_categories = self._categorize_subjects_by_field(
            subject_data, total_population
        )

        return {
            "municipality_data": subject_data,
            "ward_data": ward_data,
            "total_population": total_population,
            "top_subjects": top_subjects,
            "field_categories": field_categories,
        }

    def _categorize_subjects_by_field(self, subject_data, total_population):
        """Categorize subjects into educational fields"""
        categories = {
            "science_tech": {
                "name": "विज्ञान र प्रविधि",
                "subjects": [
                    "SCIENCE",
                    "PHYSICS",
                    "CHEMISTRY",
                    "BIOLOGY",
                    "ENGINEERING",
                    "MEDICINE",
                    "INFORMATION_TECHNOLOGY",
                    "STATISTICS",
                ],
                "population": 0,
                "percentage": 0,
                "priority": "उत्पादकत्व र नवाचार",
            },
            "language_literature": {
                "name": "भाषा र साहित्य",
                "subjects": ["NEPALI", "ENGLISH", "HINDI", "SANSKRIT"],
                "population": 0,
                "percentage": 0,
                "priority": "सांस्कृतिक संरक्षण",
            },
            "social_humanities": {
                "name": "सामाजिक विज्ञान",
                "subjects": [
                    "HISTORY",
                    "GEOGRAPHY",
                    "POLITICAL_SCIENCE",
                    "SOCIAL_SCIENCES",
                    "PSYCHOLOGY",
                    "HUMANITIES",
                ],
                "population": 0,
                "percentage": 0,
                "priority": "सामुदायिक नेतृत्व",
            },
            "professional": {
                "name": "व्यावसायिक विषयहरू",
                "subjects": ["ECONOMICS", "COMMERCE", "MANAGEMENT", "EDUCATION"],
                "population": 0,
                "percentage": 0,
                "priority": "आर्थिक विकास",
            },
            "agriculture_forestry": {
                "name": "कृषि र वन",
                "subjects": ["FORESTRY_AND_AGRICULTURE", "RURAL_DEVELOPMENT", "BOTANY"],
                "population": 0,
                "percentage": 0,
                "priority": "स्थानीय विकास",
            },
            "arts_others": {
                "name": "कला र अन्य",
                "subjects": ["ARTS", "TOURISM", "HOME_ECONOMICS", "OTHER"],
                "population": 0,
                "percentage": 0,
                "priority": "सामुदायिक विविधता",
            },
        }

        # Calculate population for each category
        for category_key, category_info in categories.items():
            for subject_code in category_info["subjects"]:
                if subject_code in subject_data:
                    category_info["population"] += subject_data[subject_code][
                        "population"
                    ]

            # Calculate percentage
            if total_population > 0:
                category_info["percentage"] = (
                    category_info["population"] / total_population
                ) * 100

        return categories

    def generate_analysis_text(self, data):
        """Generate comprehensive analysis text for major subject distribution"""
        if not data or data["total_population"] == 0:
            return "मुख्य विषयको तथ्याङ्क उपलब्ध छैन।"

        total_population = data["total_population"]
        municipality_data = data["municipality_data"]
        ward_data = data["ward_data"]

        analysis_parts = []

        # Overall summary
        analysis_parts.append(
            f"लुङ्ग्री गाउँपालिकामा पाँच वर्ष र सोभन्दा माथिका कुल {format_nepali_number(total_population)} जना जनसंख्याको शैक्षिक योग्यताको विश्लेषण गर्दा विभिन्न विषयहरूमा शिक्षा ग्रहण गरेको पाइन्छ।"
        )

        # Subject distribution analysis
        if municipality_data:
            # Find the most common subject
            dominant_subject = max(
                municipality_data.items(), key=lambda x: x[1]["population"]
            )
            analysis_parts.append(
                f"मुख्य विषयको आधारमा विश्लेषण गर्दा, {dominant_subject[1]['name_nepali']} विषयमा सबैभन्दा बढी "
                f"{format_nepali_number(dominant_subject[1]['population'])} जना "
                f"({format_nepali_percentage(dominant_subject[1]['percentage'])}) शिक्षा ग्रहण गरेको देखिन्छ।"
            )

            # Science and Technology subjects analysis
            science_tech_subjects = [
                "SCIENCE",
                "PHYSICS",
                "CHEMISTRY",
                "BIOLOGY",
                "BOTANY",
                "ENGINEERING",
                "MEDICINE",
                "INFORMATION_TECHNOLOGY",
                "STATISTICS",
            ]
            science_tech_population = sum(
                municipality_data.get(subject, {}).get("population", 0)
                for subject in science_tech_subjects
            )
            science_tech_percentage = (
                (science_tech_population / total_population * 100)
                if total_population > 0
                else 0
            )

            if science_tech_percentage > 0:
                analysis_parts.append(
                    f"विज्ञान र प्रविधि क्षेत्रमा {format_nepali_number(science_tech_population)} जना "
                    f"({format_nepali_percentage(science_tech_percentage)}) ले शिक्षा ग्रहण गरेका छन्। "
                    f"यसले आधुनिक शिक्षाप्रति बढ्दो चासो र प्राविधिक क्षेत्रको विकासमा योगदान देखाउँछ।"
                )

            # Language subjects analysis
            language_subjects = ["NEPALI", "ENGLISH", "HINDI", "SANSKRIT"]
            language_population = sum(
                municipality_data.get(subject, {}).get("population", 0)
                for subject in language_subjects
            )
            language_percentage = (
                (language_population / total_population * 100)
                if total_population > 0
                else 0
            )

            if language_percentage > 0:
                analysis_parts.append(
                    f"भाषा शिक्षामा {format_nepali_number(language_population)} जना "
                    f"({format_nepali_percentage(language_percentage)}) संलग्न छन्। "
                    f"नेपाली, अंग्रेजी र अन्य भाषाहरूको अध्ययनले भाषिक दक्षता विकासमा योगदान पुर्‍याएको छ।"
                )

            # Social Sciences and Humanities analysis
            social_humanities_subjects = [
                "HISTORY",
                "GEOGRAPHY",
                "POLITICAL_SCIENCE",
                "SOCIAL_SCIENCES",
                "PSYCHOLOGY",
                "HUMANITIES",
                "POPULATION_STUDY",
            ]
            social_humanities_population = sum(
                municipality_data.get(subject, {}).get("population", 0)
                for subject in social_humanities_subjects
            )
            social_humanities_percentage = (
                (social_humanities_population / total_population * 100)
                if total_population > 0
                else 0
            )

            if social_humanities_percentage > 0:
                analysis_parts.append(
                    f"सामाजिक विज्ञान र मानविकी क्षेत्रमा {format_nepali_number(social_humanities_population)} जना "
                    f"({format_nepali_percentage(social_humanities_percentage)}) ले अध्ययन गरेका छन्। "
                    f"यसले समाजको सामाजिक-सांस्कृतिक विकासमा योगदान पुर्‍याउने जनशक्ति तयार भएको देखाउँछ।"
                )

            # Professional and Applied subjects analysis
            professional_subjects = [
                "ECONOMICS",
                "COMMERCE",
                "MANAGEMENT",
                "EDUCATION",
                "EDUCATIONAL_SCIENCE",
                "FORESTRY_AND_AGRICULTURE",
                "RURAL_DEVELOPMENT",
                "HOME_ECONOMICS",
                "TOURISM",
            ]
            professional_population = sum(
                municipality_data.get(subject, {}).get("population", 0)
                for subject in professional_subjects
            )
            professional_percentage = (
                (professional_population / total_population * 100)
                if total_population > 0
                else 0
            )

            if professional_percentage > 0:
                analysis_parts.append(
                    f"व्यावसायिक र उपयोगी शिक्षामा {format_nepali_number(professional_population)} जना "
                    f"({format_nepali_percentage(professional_percentage)}) संलग्न छन्। "
                    f"यसले रोजगारीमुखी शिक्षाको महत्त्व बुझिएको र आर्थिक विकासमा योगदान पुर्‍याउने संकेत गर्छ।"
                )

            # Specific subject analysis
            # Medicine analysis
            if "MEDICINE" in municipality_data:
                medicine_population = municipality_data["MEDICINE"]["population"]
                medicine_percentage = municipality_data["MEDICINE"]["percentage"]
                analysis_parts.append(
                    f"चिकित्सा शिक्षामा {format_nepali_number(medicine_population)} जना "
                    f"({format_nepali_percentage(medicine_percentage)}) ले योग्यता हासिल गरेका छन्। "
                    f"यसले स्वास्थ्य सेवाको क्षेत्रमा स्थानीय जनशक्ति विकासको सकारात्मक संकेत दिन्छ।"
                )

            # Engineering analysis
            if "ENGINEERING" in municipality_data:
                engineering_population = municipality_data["ENGINEERING"]["population"]
                engineering_percentage = municipality_data["ENGINEERING"]["percentage"]
                analysis_parts.append(
                    f"इन्जिनियरिङ शिक्षामा {format_nepali_number(engineering_population)} जना "
                    f"({format_nepali_percentage(engineering_percentage)}) ले शिक्षा ग्रहण गरेका छन्। "
                    f"यसले पूर्वाधार विकास र प्राविधिक क्षेत्रको विकासमा योगदान पुर्‍याउने जनशक्ति उत्पादन भएको देखाउँछ।"
                )

            # Education analysis
            if "EDUCATION" in municipality_data:
                education_population = municipality_data["EDUCATION"]["population"]
                education_percentage = municipality_data["EDUCATION"]["percentage"]
                analysis_parts.append(
                    f"शिक्षा विषयमा {format_nepali_number(education_population)} जना "
                    f"({format_nepali_percentage(education_percentage)}) ले अध्ययन गरेका छन्। "
                    f"यसले शिक्षक तयारी र शैक्षिक गुणस्तर सुधारमा योगदान पुर्‍याउने जनशक्ति विकास भएको संकेत गर्छ।"
                )

            # Agriculture and Forestry analysis
            if "FORESTRY_AND_AGRICULTURE" in municipality_data:
                agri_population = municipality_data["FORESTRY_AND_AGRICULTURE"][
                    "population"
                ]
                agri_percentage = municipality_data["FORESTRY_AND_AGRICULTURE"][
                    "percentage"
                ]
                analysis_parts.append(
                    f"वन तथा कृषि शिक्षामा {format_nepali_number(agri_population)} जना "
                    f"({format_nepali_percentage(agri_percentage)}) ले योग्यता हासिल गरेका छन्। "
                    f"यसले स्थानीय प्राकृतिक संसाधनको दिगो उपयोग र कृषि उत्पादनमा सुधारको संभावना देखाउँछ।"
                )

        # Ward-wise comparative analysis
        if ward_data and len(ward_data) > 1:
            # Find wards with highest and lowest educational diversity
            ward_diversity = {}
            for ward_num, ward_info in ward_data.items():
                ward_diversity[ward_num] = len(ward_info["subjects"])

            highest_diversity_ward = max(ward_diversity.items(), key=lambda x: x[1])
            lowest_diversity_ward = min(ward_diversity.items(), key=lambda x: x[1])

            if highest_diversity_ward[0] != lowest_diversity_ward[0]:
                analysis_parts.append(
                    f"वडागत विश्लेषणमा, वडा नं. {highest_diversity_ward[0]} मा सबैभन्दा बढी "
                    f"{highest_diversity_ward[1]} विषयहरूमा शिक्षा ग्रहण गरेको विविधता देखिन्छ "
                    f"भने वडा नं. {lowest_diversity_ward[0]} मा {lowest_diversity_ward[1]} विषयहरूमा मात्र शिक्षा ग्रहण गरेको छ।"
                )

            # Population distribution analysis
            ward_populations = {}
            for ward_num, ward_info in ward_data.items():
                ward_populations[ward_num] = ward_info["total_population"]

            highest_pop_ward = max(ward_populations.items(), key=lambda x: x[1])
            lowest_pop_ward = min(ward_populations.items(), key=lambda x: x[1])

            if highest_pop_ward[0] != lowest_pop_ward[0]:
                analysis_parts.append(
                    f"शैक्षिक जनसंख्याको वितरणमा, वडा नं. {highest_pop_ward[0]} मा सबैभन्दा बढी "
                    f"{format_nepali_number(highest_pop_ward[1])} जना शिक्षित जनसंख्या छ "
                    f"भने वडा नं. {lowest_pop_ward[0]} मा {format_nepali_number(lowest_pop_ward[1])} जना मात्र छ।"
                )

        # Human resource development implications
        analysis_parts.append(
            "विविध विषयहरूमा शिक्षित जनशक्तिको उपस्थितिले गाउँपालिकाको मानव संशाधन विकासमा सकारात्मक प्रभाव पारेको छ। "
            "यसले विभिन्न क्षेत्रहरूमा दक्ष जनशक्तिको उपलब्धता सुनिश्चित गरेको छ।"
        )

        # Economic development potential
        analysis_parts.append(
            "व्यावसायिक र प्राविधिक शिक्षामा शिक्षित जनशक्तिले स्थानीय आर्थिक विकास, उद्यमशीलता र रोजगारी सिर्जनामा महत्वपूर्ण भूमिका खेल्न सक्छ।"
        )

        # Quality of education reflection
        analysis_parts.append(
            "उच्च शिक्षामा विविध विषयहरूको उपस्थितिले शैक्षिक गुणस्तर र पहुँचमा सुधार भएको र भविष्यका लागि आशाजनक मानव संशाधन तयार भएको संकेत गर्छ।"
        )

        # Future development recommendations
        analysis_parts.append(
            "भविष्यमा विज्ञान, प्रविधि र व्यावसायिक शिक्षालाई प्रोत्साहन गर्दै स्थानीय आवश्यकता अनुसारको शिक्षा नीति निर्माण गर्नुपर्छ।"
        )

        # Skills utilization importance
        analysis_parts.append(
            "शिक्षित जनशक्तिको उपयोगी प्रयोग र स्थानीय विकासमा संलग्नताले गाउँपालिकाको दिगो विकासमा योगदान पुर्‍याउन सक्छ।"
        )

        return " ".join(analysis_parts)

    def generate_pie_chart(self, data, title="मुख्य विषय अनुसार जनसंख्या वितरण"):
        """Generate pie chart for major subject distribution"""
        if not data.get("municipality_data"):
            return None

        # For pie chart, we'll focus on top subjects to avoid overcrowding
        chart_data = {}
        sorted_subjects = sorted(
            data["municipality_data"].items(),
            key=lambda x: x[1]["population"],
            reverse=True,
        )

        # Take top 10 subjects and group others
        top_subjects = sorted_subjects[:10]
        other_population = sum(item[1]["population"] for item in sorted_subjects[10:])

        for subject_code, subject_info in top_subjects:
            chart_data[subject_code] = {
                "name_nepali": subject_info["name_nepali"],
                "population": subject_info["population"],
            }

        if other_population > 0:
            chart_data["OTHER_COMBINED"] = {
                "name_nepali": "अन्य विषयहरू",
                "population": other_population,
            }

        return self.chart_generator.generate_pie_chart_svg(
            chart_data,
            include_title=False,
            title_nepali=title,
            title_english="Population Distribution by Major Subject",
        )

    def generate_bar_chart(self, data, title="वडागत मुख्य विषय वितरण"):
        """Generate bar chart for ward-wise major subject distribution"""
        if not data.get("ward_data"):
            return None

        chart_data = {}
        for ward_num, ward_info in data["ward_data"].items():
            # Find top 3 subjects in each ward
            sorted_ward_subjects = sorted(
                ward_info["subjects"].items(),
                key=lambda x: x[1]["population"],
                reverse=True,
            )[:3]

            chart_data[f"ward_{ward_num}"] = {
                "name_nepali": f"वडा {ward_num}",
                "total_population": ward_info["total_population"],
                "subjects": {
                    subject_code: subject_info["population"]
                    for subject_code, subject_info in sorted_ward_subjects
                },
            }

        return self.chart_generator.generate_bar_chart_svg(
            chart_data,
            include_title=False,
            title_nepali=title,
            title_english="Ward-wise Major Subject Distribution",
        )

    def process_for_pdf(self):
        """Process major subject data for PDF generation including charts"""
        # Get raw data
        data = self.get_data()

        # Generate analysis text
        coherent_analysis = self.generate_analysis_text(data)

        # Generate and save charts
        charts = self.generate_and_save_charts(data)

        return {
            "municipality_data": data.get("municipality_data", {}),
            "ward_data": data.get("ward_data", {}),
            "total_population": data.get("total_population", 0),
            "coherent_analysis": coherent_analysis,
            "pdf_charts": {"major_subject": charts},
            "section_title": self.get_section_title(),
            "section_number": self.get_section_number(),
        }


class MajorSubjectReportFormatter(BaseSocialReportFormatter):
    """Report formatter for major subject educational data"""

    def __init__(self, processor_data):
        super().__init__(processor_data)

    def format_for_html(self):
        """Format data for HTML template rendering"""
        return {
            "municipality_data": self.data["municipality_data"],
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
                "subjects": len(self.data["municipality_data"]),
                "wards": len(self.data["ward_data"]),
            },
            "subject_breakdown": self.data["municipality_data"],
            "ward_breakdown": self.data["ward_data"],
            "analysis": self.data["coherent_analysis"],
        }
