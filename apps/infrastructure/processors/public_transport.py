"""
Public Transport Access Processor - Complete Implementation

Handles public transport accessibility data processing, chart generation, and report formatting.
"""

from django.db import models
from .base import BaseInfrastructureProcessor, BaseInfrastructureReportFormatter
from ..models import WardWiseTimeToPublicTransport, TimeDurationChoice
from apps.reports.utils.nepali_numbers import (
    format_nepali_number,
    format_nepali_percentage,
    to_nepali_digits,
)


class PublicTransportProcessor(BaseInfrastructureProcessor):
    """Processor for public transport accessibility data"""

    def __init__(self):
        super().__init__()
        # Customize chart dimensions for public transport
        self.pie_chart_width = 800
        self.pie_chart_height = 450
        self.bar_chart_width = 1000
        self.bar_chart_height = 600
        self.chart_radius = 130
        # Set time duration-specific colors
        self.chart_generator.colors = {
            "UNDER_15_MIN": "#22C55E",  # Green - Excellent access
            "UNDER_30_MIN": "#84CC16",  # Light Green - Good access
            "UNDER_1_HOUR": "#F59E0B",  # Amber - Moderate access
            "1_HOUR_OR_MORE": "#EF4444",  # Red - Poor access
        }

    def get_chart_key(self):
        """Get the key for storing charts in PDF context"""
        return "public_transport"

    def get_section_title(self):
        return "सार्वजनिक यातायातमा पहुँचको अवस्था"

    def get_section_number(self):
        return "७.१.७"

    def get_data(self):
        """Get public transport accessibility data - both municipality-wide and ward-wise"""
        # Municipality-wide summary by time duration
        time_duration_data = {}
        total_households = 0

        for time_choice in TimeDurationChoice.choices:
            time_code = time_choice[0]
            time_name = time_choice[1]

            time_households = (
                WardWiseTimeToPublicTransport.objects.filter(
                    time_duration=time_code
                ).aggregate(total=models.Sum("households"))["total"]
                or 0
            )

            if time_households > 0:  # Only include time durations with households
                time_duration_data[time_code] = {
                    "name_english": time_code,
                    "name_nepali": time_name,
                    "population": time_households,  # Using households as population for consistency
                    "percentage": 0,  # Will be calculated below
                }
                total_households += time_households

        # Calculate percentages
        for time_code in time_duration_data:
            if total_households > 0:
                time_duration_data[time_code]["percentage"] = (
                    time_duration_data[time_code]["population"] / total_households * 100
                )

        # Ward-wise data
        ward_data = {}
        for ward_num in range(1, 9):  # Wards 1-8
            ward_households = (
                WardWiseTimeToPublicTransport.objects.filter(
                    ward_number=ward_num
                ).aggregate(total=models.Sum("households"))["total"]
                or 0
            )

            if ward_households > 0:
                ward_data[ward_num] = {
                    "ward_number": ward_num,
                    "ward_name": f"वडा नं. {to_nepali_digits(ward_num)}",
                    "total_population": ward_households,  # Using households
                    "time_durations": {},
                }

                # Time duration breakdown for this ward
                for time_choice in TimeDurationChoice.choices:
                    time_code = time_choice[0]
                    time_name = time_choice[1]

                    time_households_ward = (
                        WardWiseTimeToPublicTransport.objects.filter(
                            ward_number=ward_num, time_duration=time_code
                        ).aggregate(total=models.Sum("households"))["total"]
                        or 0
                    )

                    if time_households_ward > 0:
                        ward_data[ward_num]["time_durations"][time_code] = {
                            "name_nepali": time_name,
                            "population": time_households_ward,
                            "percentage": (
                                (time_households_ward / ward_households * 100)
                                if ward_households > 0
                                else 0
                            ),
                        }

        return {
            "municipality_data": time_duration_data,
            "ward_data": ward_data,
            "total_households": total_households,
        }

    def generate_analysis_text(self, data):
        """Generate comprehensive analysis text for public transport accessibility"""
        if not data or data["total_households"] == 0:
            return "सार्वजनिक यातायातमा पहुँचको तथ्याङ्क उपलब्ध छैन।"

        total_households = data["total_households"]
        municipality_data = data["municipality_data"]
        ward_data = data["ward_data"]

        analysis_parts = []

        # Overall summary
        analysis_parts.append(
            f"गढवा गाउँपालिकामा कुल {format_nepali_number(total_households)} घरपरिवारको सार्वजनिक यातायातमा पहुँचको अवस्था विश्लेषण गर्दा विभिन्न समयावधिमा सार्वजनिक यातायात पुग्ने सुविधा उपलब्ध रहेको देखिन्छ।"
        )

        # Accessibility analysis
        if municipality_data:
            # Calculate accessibility levels
            excellent_access = municipality_data.get("UNDER_15_MIN", {}).get(
                "population", 0
            )
            good_access = municipality_data.get("UNDER_30_MIN", {}).get("population", 0)
            moderate_access = municipality_data.get("UNDER_1_HOUR", {}).get(
                "population", 0
            )
            poor_access = municipality_data.get("1_HOUR_OR_MORE", {}).get(
                "population", 0
            )

            # Combined good accessibility (under 30 minutes)
            good_accessibility = excellent_access + good_access
            good_accessibility_percentage = (
                (good_accessibility / total_households * 100)
                if total_households > 0
                else 0
            )

            # Find the most common time duration
            if municipality_data:
                dominant_time = max(
                    municipality_data.items(), key=lambda x: x[1]["population"]
                )
                analysis_parts.append(
                    f"समयावधिको आधारमा विश्लेषण गर्दा, {dominant_time[1]['name_nepali']} समयमा सार्वजनिक यातायात पुग्ने घरपरिवारको संख्या सबैभन्दा बढी "
                    f"{format_nepali_number(dominant_time[1]['population'])} "
                    f"({format_nepali_percentage(dominant_time[1]['percentage'])}) रहेको छ।"
                )

            # Accessibility quality analysis
            if good_accessibility > 0:
                analysis_parts.append(
                    f"सार्वजनिक यातायातमा पहुँचको गुणस्तरको दृष्टिकोणले हेर्दा, {format_nepali_number(good_accessibility)} घरपरिवार "
                    f"({format_nepali_percentage(good_accessibility_percentage)}) ले ३० मिनेट भित्रमा सार्वजनिक यातायात पुग्न सक्छन् जुन राम्रो पहुँचको सूचक हो।"
                )

            # Distance and connectivity analysis
            if excellent_access > 0:
                excellent_percentage = excellent_access / total_households * 100
                analysis_parts.append(
                    f"विशेष गरी {format_nepali_number(excellent_access)} घरपरिवार "
                    f"({format_nepali_percentage(excellent_percentage)}) ले १५ मिनेट भित्रमा सार्वजनिक यातायात पुग्न सक्ने उत्कृष्ट अवस्था छ।"
                )

            # Challenge analysis
            if poor_access > 0:
                poor_percentage = poor_access / total_households * 100
                analysis_parts.append(
                    f"तर, {format_nepali_number(poor_access)} घरपरिवार "
                    f"({format_nepali_percentage(poor_percentage)}) लाई सार्वजनिक यातायात पुग्न एक घण्टा वा सो भन्दा बढी समय लाग्छ जसले यातायात सेवामा सुधारको आवश्यकता देखाउँछ।"
                )

        # Ward-wise comparative analysis
        if ward_data and len(ward_data) > 1:
            best_ward, worst_ward = self.find_best_worst_wards(ward_data)

            if best_ward and worst_ward and best_ward != worst_ward:
                best_accessibility = self.calculate_ward_accessibility(
                    ward_data[best_ward]
                )
                worst_accessibility = self.calculate_ward_accessibility(
                    ward_data[worst_ward]
                )

                analysis_parts.append(
                    f"वडागत विश्लेषणमा, वडा नं. {to_nepali_digits(best_ward)} मा सबैभन्दा राम्रो सार्वजनिक यातायात पहुँच "
                    f"({format_nepali_percentage(best_accessibility)} घरपरिवारले ३० मिनेट भित्रमा पहुँच) छ "
                    f"भने वडा नं. {to_nepali_digits(worst_ward)} मा केही सुधारको आवश्यकता "
                    f"({format_nepali_percentage(worst_accessibility)} घरपरिवारले मात्र ३० मिनेट भित्रमा पहुँच) देखिन्छ।"
                )

        # Economic and social implications
        if good_accessibility_percentage > 70:
            analysis_parts.append(
                "सार्वजनिक यातायातमा राम्रो पहुँचले स्थानीय आर्थिक गतिविधि, शिक्षा र स्वास्थ्य सेवामा पहुँचमा सकारात्मक प्रभाव पारेको छ।"
            )
        else:
            analysis_parts.append(
                "सार्वजनिक यातायात सेवामा सुधार भएमा स्थानीय विकासमा महत्वपूर्ण योगदान पुग्ने अपेक्षा गर्न सकिन्छ।"
            )

        # Future development recommendations
        if poor_access > total_households * 0.3:  # If more than 30% have poor access
            analysis_parts.append(
                "भविष्यमा सार्वजनिक यातायात सेवाको विस्तार र नियमितता सुधारले यातायातमा पहुँचमा उल्लेखनीय सुधार ल्याउन सक्छ।"
            )

        return " ".join(analysis_parts)

    def calculate_ward_accessibility(self, ward_info):
        """Calculate good accessibility percentage for a ward"""
        excellent = (
            ward_info["time_durations"].get("UNDER_15_MIN", {}).get("population", 0)
        )
        good = ward_info["time_durations"].get("UNDER_30_MIN", {}).get("population", 0)
        good_access_ward = excellent + good
        return (
            (good_access_ward / ward_info["total_population"] * 100)
            if ward_info["total_population"] > 0
            else 0
        )

    def find_best_worst_wards(self, ward_data):
        """Find wards with best and worst public transport accessibility"""
        best_ward = None
        worst_ward = None
        best_accessibility = 0
        worst_accessibility = 100

        for ward_num, ward_info in ward_data.items():
            accessibility_percentage = self.calculate_ward_accessibility(ward_info)

            if accessibility_percentage > best_accessibility:
                best_accessibility = accessibility_percentage
                best_ward = ward_num

            if accessibility_percentage < worst_accessibility:
                worst_accessibility = accessibility_percentage
                worst_ward = ward_num

        return best_ward, worst_ward

    def generate_accessibility_assessment(self, good_access_percentage):
        """Generate accessibility assessment text"""
        if good_access_percentage >= 80:
            return "उत्कृष्ट पहुँच - अधिकांश घरपरिवारहरूको सार्वजनिक यातायातमा राम्रो पहुँच छ।"
        elif good_access_percentage >= 60:
            return "राम्रो पहुँच - धेरैजसो घरपरिवारहरूको सार्वजनिक यातायातमा स्वीकार्य पहुँच छ।"
        elif good_access_percentage >= 40:
            return "मध्यम पहुँच - सार्वजनिक यातायात सेवामा केही सुधारको आवश्यकता छ।"
        else:
            return "कमजोर पहुँच - सार्वजनिक यातायात सेवामा महत्वपूर्ण सुधारको आवश्यकता छ।"

    def find_ward_with_best_access(self, ward_data):
        """Find ward with best public transport access"""
        best_ward = None
        best_accessibility = 0

        for ward_num, ward_info in ward_data.items():
            accessibility_percentage = self.calculate_ward_accessibility(ward_info)
            if accessibility_percentage > best_accessibility:
                best_accessibility = accessibility_percentage
                best_ward = ward_num

        return best_ward

    def find_ward_with_worst_access(self, ward_data):
        """Find ward with worst public transport access"""
        worst_ward = None
        worst_accessibility = 100

        for ward_num, ward_info in ward_data.items():
            accessibility_percentage = self.calculate_ward_accessibility(ward_info)
            if accessibility_percentage < worst_accessibility:
                worst_accessibility = accessibility_percentage
                worst_ward = ward_num

        return worst_ward

    def generate_pie_chart(self, data, title="सार्वजनिक यातायातमा पहुँचको समय वितरण"):
        """Generate pie chart for public transport time distribution"""
        # Handle both direct municipality_data and full data structure
        if isinstance(data, dict) and "municipality_data" in data:
            municipality_data = data["municipality_data"]
        else:
            # data is already the municipality_data
            municipality_data = data

        if not municipality_data:
            return None

        # Prepare data for chart in the format expected by SVGChartGenerator
        chart_data = {}
        for time_code, time_info in municipality_data.items():
            if time_info["population"] > 0:
                chart_data[time_code] = {
                    "name_nepali": time_info["name_nepali"],
                    "population": time_info["population"],
                    "percentage": time_info["percentage"],
                }

        if not chart_data:
            return None

        return self.chart_generator.generate_pie_chart_svg(
            demographic_data=chart_data,
            include_title=True,
            title_nepali=title,
            title_english="Household Distribution by Time to Public Transport",
        )


class PublicTransportReportFormatter(BaseInfrastructureReportFormatter):
    """Report formatter for public transport accessibility data"""

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
                "time_categories": len(self.data["municipality_data"]),
                "wards": len(self.data["ward_data"]),
            },
            "time_duration_breakdown": self.data["municipality_data"],
            "ward_breakdown": self.data["ward_data"],
            "analysis": self.data["coherent_analysis"],
        }
