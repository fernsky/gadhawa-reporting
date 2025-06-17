"""
Road Status Infrastructure Processor - Complete Implementation

Handles road status infrastructure data processing, chart generation, and report formatting.
"""

from django.db import models
from .base import BaseInfrastructureProcessor, BaseInfrastructureReportFormatter
from ..models import WardWiseRoadStatus, RoadStatusChoice
from apps.reports.utils.nepali_numbers import (
    format_nepali_number,
    format_nepali_percentage,
    to_nepali_digits,
)


class RoadStatusProcessor(BaseInfrastructureProcessor):
    """Processor for road status infrastructure data"""

    def __init__(self):
        super().__init__()
        # Customize chart dimensions for road status
        self.pie_chart_width = 950
        self.pie_chart_height = 500
        self.chart_radius = 150
        # Set road status-specific colors with meaningful associations
        self.chart_generator.colors = {
            "BLACKTOPPED": "#2E7D32",  # Dark Green - Best quality
            "GRAVELED": "#4CAF50",  # Green - Good quality
            "EARTHEN": "#FF9800",  # Orange - Basic quality
            "NO_ROAD": "#F44336",  # Red - No access
        }

    def get_section_title(self):
        return "सडकको अवस्था अनुसार घरपरिवार विवरण"

    def get_section_number(self):
        return "७.१.१"

    def get_data(self):
        """Get road status data - both municipality-wide and ward-wise"""
        # Municipality-wide summary
        road_data = {}
        total_households = 0

        for road_choice in RoadStatusChoice.choices:
            road_code = road_choice[0]
            road_name = road_choice[1]

            road_households = (
                WardWiseRoadStatus.objects.filter(road_status=road_code).aggregate(
                    total=models.Sum("households")
                )["total"]
                or 0
            )

            if road_households > 0:  # Only include road statuses with households
                road_data[road_code] = {
                    "name_english": road_code,
                    "name_nepali": road_name,
                    "population": road_households,  # Using households as population for consistency
                    "percentage": 0,  # Will be calculated below
                }
                total_households += road_households

        # Calculate percentages
        for road_code in road_data:
            if total_households > 0:
                road_data[road_code]["percentage"] = (
                    road_data[road_code]["population"] / total_households * 100
                )

        # Ward-wise data
        ward_data = {}
        for ward_num in range(1, 8):  # Wards 1-7
            ward_households = (
                WardWiseRoadStatus.objects.filter(ward_number=ward_num).aggregate(
                    total=models.Sum("households")
                )["total"]
                or 0
            )

            if ward_households > 0:
                ward_data[ward_num] = {
                    "ward_number": ward_num,
                    "ward_name": f"वडा नं. {to_nepali_digits(ward_num)}",
                    "total_population": ward_households,  # Using households
                    "road_statuses": {},
                }

                # Road status breakdown for this ward
                for road_choice in RoadStatusChoice.choices:
                    road_code = road_choice[0]
                    road_name = road_choice[1]

                    road_households_ward = (
                        WardWiseRoadStatus.objects.filter(
                            ward_number=ward_num, road_status=road_code
                        ).aggregate(total=models.Sum("households"))["total"]
                        or 0
                    )

                    if road_households_ward > 0:
                        ward_data[ward_num]["road_statuses"][road_code] = {
                            "name_nepali": road_name,
                            "population": road_households_ward,
                            "percentage": (
                                (road_households_ward / ward_households * 100)
                                if ward_households > 0
                                else 0
                            ),
                        }

        return {
            "municipality_data": road_data,
            "ward_data": ward_data,
            "total_households": total_households,
        }

    def generate_analysis_text(self, data):
        """Generate comprehensive analysis text for road status"""
        if not data or data["total_households"] == 0:
            return "सडकको अवस्थाको तथ्याङ्क उपलब्ध छैन।"

        total_households = data["total_households"]
        municipality_data = data["municipality_data"]
        ward_data = data["ward_data"]

        analysis_parts = []

        # Overall summary
        analysis_parts.append(
            f"लुङ्ग्री गाउँपालिकामा कुल {format_nepali_number(total_households)} घरपरिवारको सडकको अवस्था विश्लेषण गर्दा विभिन्न प्रकारका सडक सुविधा उपलब्ध रहेको देखिन्छ।"
        )

        # Road quality analysis
        if municipality_data:
            # Calculate road quality levels
            blacktopped = municipality_data.get("BLACKTOPPED", {}).get("population", 0)
            graveled = municipality_data.get("GRAVELED", {}).get("population", 0)
            earthen = municipality_data.get("EARTHEN", {}).get("population", 0)
            no_road = municipality_data.get("NO_ROAD", {}).get("population", 0)

            # Combined good road access (blacktopped + graveled)
            good_road_access = blacktopped + graveled
            good_road_percentage = (
                (good_road_access / total_households * 100)
                if total_households > 0
                else 0
            )

            # Find the most common road type
            if municipality_data:
                dominant_road = max(
                    municipality_data.items(), key=lambda x: x[1]["population"]
                )
                analysis_parts.append(
                    f"सडकको अवस्थाको आधारमा विश्लेषण गर्दा, {dominant_road[1]['name_nepali']} सडकमा पहुँच भएका घरपरिवारको संख्या सबैभन्दा बढी "
                    f"{format_nepali_number(dominant_road[1]['population'])} "
                    f"({format_nepali_percentage(dominant_road[1]['percentage'])}) रहेको छ।"
                )

            # Road quality analysis
            if good_road_access > 0:
                analysis_parts.append(
                    f"सडकको गुणस्तरको दृष्टिकोणले हेर्दा, {format_nepali_number(good_road_access)} घरपरिवार "
                    f"({format_nepali_percentage(good_road_percentage)}) ले कालोपत्रे वा ढुंगामाटो सडकमा पहुँच पाएका छन् जुन राम्रो सडक सुविधाको सूचक हो।"
                )

            # High quality road analysis
            if blacktopped > 0:
                blacktopped_percentage = blacktopped / total_households * 100
                analysis_parts.append(
                    f"विशेष गरी {format_nepali_number(blacktopped)} घरपरिवार "
                    f"({format_nepali_percentage(blacktopped_percentage)}) ले कालोपत्रे सडकमा पहुँच पाएका छन् जुन उत्कृष्ट सडक सुविधाको सूचक हो।"
                )

            # Graveled road analysis
            if graveled > 0:
                graveled_percentage = graveled / total_households * 100
                analysis_parts.append(
                    f"{format_nepali_number(graveled)} घरपरिवार "
                    f"({format_nepali_percentage(graveled_percentage)}) ले ढुंगामाटो सडकमा पहुँच पाएका छन्।"
                )

            # Basic road analysis
            if earthen > 0:
                earthen_percentage = earthen / total_households * 100
                analysis_parts.append(
                    f"{format_nepali_number(earthen)} घरपरिवार "
                    f"({format_nepali_percentage(earthen_percentage)}) ले कच्ची सडकमा पहुँच पाएका छन्।"
                )

            # No road access analysis
            if no_road > 0:
                no_road_percentage = no_road / total_households * 100
                analysis_parts.append(
                    f"तर, {format_nepali_number(no_road)} घरपरिवार "
                    f"({format_nepali_percentage(no_road_percentage)}) को सडक पहुँच नभएको अवस्था छ जसले सडक पूर्वाधारमा सुधारको आवश्यकता देखाउँछ।"
                )

        # Ward-wise comparative analysis
        if ward_data and len(ward_data) > 1:
            best_ward, worst_ward = self.find_best_worst_wards_road(ward_data)

            if best_ward and worst_ward and best_ward != worst_ward:
                best_road_access = self.calculate_ward_road_access(ward_data[best_ward])
                worst_road_access = self.calculate_ward_road_access(
                    ward_data[worst_ward]
                )

                analysis_parts.append(
                    f"वडागत विश्लेषणमा, वडा नं. {best_ward} मा सबैभन्दा राम्रो सडक पहुँच "
                    f"({format_nepali_percentage(best_road_access)} घरपरिवारले गुणस्तरीय सडकमा पहुँच) छ "
                    f"भने वडा नं. {worst_ward} मा केही सुधारको आवश्यकता "
                    f"({format_nepali_percentage(worst_road_access)} घरपरिवारले मात्र गुणस्तरीय सडकमा पहुँच) देखिन्छ।"
                )

        # Economic and social implications
        if good_road_percentage > 70:
            analysis_parts.append(
                "सडक पूर्वाधारमा राम्रो अवस्थाले स्थानीय आर्थिक गतिविधि, स्वास्थ्य सेवा र शिक्षामा पहुँचमा सकारात्मक प्रभाव पारेको छ।"
            )
        else:
            analysis_parts.append(
                "सडक पूर्वाधारमा सुधार भएमा स्थानीय विकासमा महत्वपूर्ण योगदान पुग्ने अपेक्षा गर्न सकिन्छ।"
            )

        # Connectivity and accessibility impact
        analysis_parts.append(
            "सडक संजालको विकासले न केवल यातायातमा सुविधा बल्कि शिक्षा, स्वास्थ्य र बजार पहुँचमा पनि सुधार गर्दछ।"
        )

        # Future development recommendations
        if no_road > total_households * 0.2:  # If more than 20% have no road access
            analysis_parts.append(
                "भविष्यमा सडक पूर्वाधार विकासमा प्राथमिकता दिएर सबै घरपरिवारलाई सडक सुविधा उपलब्ध गराउने नीति अपनाउनुपर्छ।"
            )
        elif (
            earthen > total_households * 0.3
        ):  # If more than 30% have only earthen roads
            analysis_parts.append(
                "कच्ची सडकलाई ढुंगामाटो वा कालोपत्रे सडकमा स्तरोन्नति गर्ने कार्यक्रमलाई प्राथमिकता दिनुपर्छ।"
            )

        return " ".join(analysis_parts)

    def calculate_ward_road_access(self, ward_info):
        """Calculate good road access percentage for a ward"""
        blacktopped = (
            ward_info["road_statuses"].get("BLACKTOPPED", {}).get("population", 0)
        )
        graveled = ward_info["road_statuses"].get("GRAVELED", {}).get("population", 0)
        good_road_access = blacktopped + graveled
        return (
            (good_road_access / ward_info["total_population"] * 100)
            if ward_info["total_population"] > 0
            else 0
        )

    def find_best_worst_wards_road(self, ward_data):
        """Find wards with best and worst road access"""
        best_ward = None
        worst_ward = None
        best_access = 0
        worst_access = 100

        for ward_num, ward_info in ward_data.items():
            access_percentage = self.calculate_ward_road_access(ward_info)

            if access_percentage > best_access:
                best_access = access_percentage
                best_ward = ward_num

            if access_percentage < worst_access:
                worst_access = access_percentage
                worst_ward = ward_num

        return best_ward, worst_ward

    def generate_pie_chart(self, data, title="सडकको अवस्था अनुसार घरपरिवार वितरण"):
        """Generate pie chart for road status distribution"""
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
        for road_code, road_info in municipality_data.items():
            if road_info["population"] > 0:
                chart_data[road_code] = {
                    "name_nepali": road_info["name_nepali"],
                    "population": road_info["population"],
                    "percentage": road_info["percentage"],
                }

        if not chart_data:
            return None

        return self.chart_generator.generate_pie_chart_svg(
            demographic_data=chart_data,
            include_title=True,
            title_nepali=title,
            title_english="Household Distribution by Road Status",
        )

    def process_for_pdf(self):
        """Process road status data for PDF generation including charts"""
        # Get raw data
        data = self.get_data()

        # Generate analysis text
        coherent_analysis = self.generate_analysis_text(data)

        # Generate and save charts
        charts = self.generate_and_save_charts(data)

        # Calculate total households
        total_households = data["total_households"]

        return {
            "section_number": self.get_section_number(),
            "section_title": self.get_section_title(),
            "municipality_data": data["municipality_data"],
            "ward_data": data["ward_data"],
            "total_households": total_households,
            "coherent_analysis": coherent_analysis,
            "pdf_charts": charts,
        }


class RoadStatusReportFormatter(BaseInfrastructureReportFormatter):
    """Report formatter for road status infrastructure data"""

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
                "road_categories": len(self.data["municipality_data"]),
                "wards": len(self.data["ward_data"]),
            },
            "road_status_breakdown": self.data["municipality_data"],
            "ward_breakdown": self.data["ward_data"],
            "analysis": self.data["coherent_analysis"],
        }
