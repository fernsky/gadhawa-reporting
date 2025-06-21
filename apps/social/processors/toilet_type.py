"""
Toilet Type Social Processor

Handles toilet type social data processing, chart generation, and report formatting.
"""

from django.db import models
from .base import BaseSocialProcessor, BaseSocialReportFormatter
from ..models import WardWiseToiletType, ToiletTypeChoice
from apps.reports.utils.nepali_numbers import (
    format_nepali_number,
    format_nepali_percentage,
    to_nepali_digits,
)


class ToiletTypeProcessor(BaseSocialProcessor):
    """Processor for toilet type social data"""

    def __init__(self):
        super().__init__()
        # Customize chart dimensions for toilet type
        self.pie_chart_width = 800
        self.pie_chart_height = 400
        self.chart_radius = 120
        # Set toilet type-specific colors
        self.chart_generator.colors = {
            "FLUSH_WITH_SEPTIC_TANK": "#4CAF50",  # Green
            "NORMAL": "#2196F3",  # Blue
            "PUBLIC_EILANI": "#FF9800",  # Orange
            "NO_TOILET": "#F44336",  # Red
            "OTHER": "#9C27B0",  # Purple
        }

    def get_section_title(self):
        return "शौचालय प्रयोगको अवस्था"

    def get_section_number(self):
        return "५.३.३"

    def get_data(self):
        """Get toilet type data - both municipality-wide and ward-wise"""
        # Municipality-wide summary
        toilet_type_data = {}
        total_households = 0

        for toilet_choice in ToiletTypeChoice.choices:
            toilet_code = toilet_choice[0]
            toilet_name = toilet_choice[1]

            toilet_households = (
                WardWiseToiletType.objects.filter(toilet_type=toilet_code).aggregate(
                    total=models.Sum("households")
                )["total"]
                or 0
            )

            if toilet_households > 0:  # Only include toilet types with households
                toilet_type_data[toilet_code] = {
                    "name_english": toilet_code,
                    "name_nepali": toilet_name,
                    "population": toilet_households,  # Using households as population for consistency
                    "percentage": 0,  # Will be calculated below
                }
                total_households += toilet_households

        # Calculate percentages
        for toilet_code in toilet_type_data:
            if total_households > 0:
                toilet_type_data[toilet_code]["percentage"] = (
                    toilet_type_data[toilet_code]["population"] / total_households * 100
                )

        # Ward-wise data
        ward_data = {}
        for ward_num in range(1, 8):  # Wards 1-7
            ward_households = (
                WardWiseToiletType.objects.filter(ward_number=ward_num).aggregate(
                    total=models.Sum("households")
                )["total"]
                or 0
            )

            if ward_households > 0:
                ward_data[ward_num] = {
                    "ward_number": ward_num,
                    "ward_name": f"वडा नं. {ward_num}",
                    "total_population": ward_households,  # Using households
                    "toilet_types": {},
                }

                # Toilet type breakdown for this ward
                for toilet_choice in ToiletTypeChoice.choices:
                    toilet_code = toilet_choice[0]
                    toilet_name = toilet_choice[1]

                    toilet_households_ward = (
                        WardWiseToiletType.objects.filter(
                            ward_number=ward_num, toilet_type=toilet_code
                        ).aggregate(total=models.Sum("households"))["total"]
                        or 0
                    )

                    if toilet_households_ward > 0:
                        ward_data[ward_num]["toilet_types"][toilet_code] = {
                            "name_nepali": toilet_name,
                            "population": toilet_households_ward,
                            "percentage": (
                                (toilet_households_ward / ward_households * 100)
                                if ward_households > 0
                                else 0
                            ),
                        }

        return {
            "municipality_data": toilet_type_data,
            "ward_data": ward_data,
            "total_households": total_households,
        }

    def generate_analysis_text(self, data):
        """Generate coherent analysis text for toilet type"""
        if not data or data["total_households"] == 0:
            return "शौचालय प्रयोगको तथ्याङ्क उपलब्ध छैन।"

        total_households = data["total_households"]
        municipality_data = data["municipality_data"]
        ward_data = data["ward_data"]

        analysis_parts = []

        # Overall summary
        analysis_parts.append(
            f"लुङ्ग्री गाउँपालिकामा कुल {format_nepali_number(total_households)} घरपरिवारमा विभिन्न प्रकारका शौचालयहरूको प्रयोग भइरहेको छ।"
        )

        # Dominant toilet type analysis
        if municipality_data:
            # Find the most used toilet type
            dominant_toilet = max(
                municipality_data.items(), key=lambda x: x[1]["population"]
            )
            analysis_parts.append(
                f"शौचालयको प्रकारको आधारमा हेर्दा, {dominant_toilet[1]['name_nepali']} शौचालयको प्रयोग सबैभन्दा बढी "
                f"{format_nepali_number(dominant_toilet[1]['population'])} घरपरिवारमा "
                f"({format_nepali_percentage(dominant_toilet[1]['percentage'])}) भइरहेको छ।"
            )

            # Sanitation coverage analysis
            if "NO_TOILET" in municipality_data:
                no_toilet = municipality_data["NO_TOILET"]
                sanitation_coverage = 100 - no_toilet["percentage"]
                analysis_parts.append(
                    f"सरसफाइको दृष्टिकोणले हेर्दा, {format_nepali_percentage(sanitation_coverage)} घरपरिवारमा "
                    f"शौचालयको सुविधा उपलब्ध छ भने {format_nepali_number(no_toilet['population'])} घरपरिवारमा "
                    f"({format_nepali_percentage(no_toilet['percentage'])}) शौचालयको सुविधा छैन।"
                )
            else:
                analysis_parts.append(
                    f"सकारात्मक पक्षको रूपमा, गाउँपालिकाका सबै घरपरिवारमा शौचालयको सुविधा उपलब्ध छ।"
                )

            # Improved sanitation analysis
            improved_toilets = 0
            if "FLUSH_WITH_SEPTIC_TANK" in municipality_data:
                improved_toilets += municipality_data["FLUSH_WITH_SEPTIC_TANK"][
                    "population"
                ]

            if improved_toilets > 0:
                improved_percentage = improved_toilets / total_households * 100
                analysis_parts.append(
                    f"सुधारिएको सरसफाइको मापदण्डअनुसार, {format_nepali_number(improved_toilets)} घरपरिवारमा "
                    f"({format_nepali_percentage(improved_percentage)}) फ्लस शौचालय र सेप्टिक ट्याङ्कको सुविधा छ।"
                )

        # Ward-wise analysis
        if ward_data:
            # Find wards with best and worst sanitation
            best_ward = None
            worst_ward = None
            best_sanitation = 0
            worst_sanitation = 100

            for ward_num, ward_info in ward_data.items():
                # Calculate sanitation coverage (exclude NO_TOILET)
                no_toilet_households = (
                    ward_info["toilet_types"].get("NO_TOILET", {}).get("population", 0)
                )
                sanitation_coverage = (
                    (
                        (ward_info["total_population"] - no_toilet_households)
                        / ward_info["total_population"]
                        * 100
                    )
                    if ward_info["total_population"] > 0
                    else 0
                )

                if sanitation_coverage > best_sanitation:
                    best_sanitation = sanitation_coverage
                    best_ward = ward_num

                if sanitation_coverage < worst_sanitation:
                    worst_sanitation = sanitation_coverage
                    worst_ward = ward_num

            if best_ward and worst_ward:
                analysis_parts.append(
                    f"वडाको आधारमा हेर्दा, वडा नं. {to_nepali_digits(best_ward)} मा सबैभन्दा राम्रो सरसफाइको अवस्था "
                    f"({format_nepali_percentage(best_sanitation)} घरपरिवारमा शौचालय सुविधा) छ "
                    f"भने वडा नं. {worst_ward} मा अझै सुधारको आवश्यकता "
                    f"({format_nepali_percentage(worst_sanitation)} घरपरिवारमा शौचालय सुविधा) छ।"
                )

        # Health and development implications
        analysis_parts.append(
            "शौचालयको उपलब्धता र प्रयोगले समुदायिक स्वास्थ्य, वातावरणीय सरसफाइ र सामाजिक मर्यादामा प्रत्यक्ष प्रभाव पार्छ।"
        )

        # Future recommendations
        if (
            "NO_TOILET" in municipality_data
            and municipality_data["NO_TOILET"]["population"] > 0
        ):
            analysis_parts.append(
                "भविष्यमा शौचालयविहीन घरपरिवारहरूलाई प्राथमिकताका साथ शौचालय निर्माणमा सहयोग गर्नुपर्ने देखिन्छ।"
            )

        return " ".join(analysis_parts)

    def generate_pie_chart(self, data, title="शौचालयको प्रकार अनुसार घरपरिवार वितरण"):
        """Generate pie chart for toilet type distribution"""
        if not data or not data["municipality_data"]:
            return None

        # Prepare data for chart
        chart_data = []
        for toilet_code, toilet_info in data["municipality_data"].items():
            if toilet_info["population"] > 0:
                chart_data.append(
                    {
                        "label": toilet_info["name_nepali"],
                        "value": toilet_info["population"],
                        "percentage": toilet_info["percentage"],
                    }
                )

        if not chart_data:
            return None

        return self.chart_generator.generate_pie_chart(
            data=chart_data,
            title=title,
            width=self.pie_chart_width,
            height=self.pie_chart_height,
            radius=self.chart_radius,
        )


class ToiletTypeReportFormatter(BaseSocialReportFormatter):
    """Report formatter for toilet type social data"""

    def __init__(self, processor_data):
        super().__init__(processor_data)

    def format_for_html(self):
        """Format data for HTML template rendering"""
        return {
            "municipality_data": self.data["municipality_data"],
            "ward_data": self.data["ward_data"],
            "total_households": self.data["total_households"],
            "coherent_analysis": self.data["coherent_analysis"],
            "pdf_charts": self.data["pdf_charts"],
        }

    def format_for_api(self):
        """Format data for API response"""
        return {
            "section": self.data["section_number"],
            "title": self.data["section_title"],
            "summary": {
                "total_households": self.data["total_households"],
                "toilet_types": len(self.data["municipality_data"]),
                "wards": len(self.data["ward_data"]),
            },
            "toilet_type_breakdown": self.data["municipality_data"],
            "ward_breakdown": self.data["ward_data"],
            "analysis": self.data["coherent_analysis"],
        }
