"""
Road Status Infrastructure Processor

Handles road status infrastructure data processing, chart generation, and report formatting.
"""

from django.db import models
from .base import BaseInfrastructureProcessor, BaseInfrastructureReportFormatter
from ..models import WardWiseRoadStatus, RoadStatusChoice
from apps.reports.utils.nepali_numbers import (
    format_nepali_number,
    format_nepali_percentage,
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
            "EARTHEN": "#FF9800",  # Orange - Basic access
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

            if road_households > 0:  # Only include road types with households
                road_data[road_code] = {
                    "name_english": road_code,
                    "name_nepali": road_name,
                    "population": road_households,
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
                    "ward_name": f"वडा नं. {ward_num}",
                    "total_population": ward_households,
                    "road_types": {},
                }

                # Road type breakdown for this ward
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
                        ward_data[ward_num]["road_types"][road_code] = {
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
            f"लुङ्ग्री गाउँपालिकामा कुल {format_nepali_number(total_households)} घरपरिवारको सडक पहुँचको अवस्था विश्लेषण गर्दा विभिन्न प्रकारका सडक सुविधा उपलब्ध रहेको देखिन्छ।"
        )

        # Dominant road type analysis
        if municipality_data:
            # Find the most common road type
            dominant_road = max(
                municipality_data.items(), key=lambda x: x[1]["population"]
            )
            analysis_parts.append(
                f"सडकको प्रकारको आधारमा विश्लेषण गर्दा, {dominant_road[1]['name_nepali']} सडकको पहुँच भएका घरपरिवारको संख्या सबैभन्दा बढी "
                f"{format_nepali_number(dominant_road[1]['population'])} "
                f"({format_nepali_percentage(dominant_road[1]['percentage'])}) रहेको छ।"
            )

            # Quality road access analysis
            quality_roads = ["BLACKTOPPED", "GRAVELED"]
            quality_households = sum(
                municipality_data.get(road, {}).get("population", 0)
                for road in quality_roads
            )
            quality_percentage = (
                (quality_households / total_households * 100)
                if total_households > 0
                else 0
            )

            if quality_percentage > 0:
                analysis_parts.append(
                    f"गुणस्तरीय सडक पहुँचको दृष्टिकोणले हेर्दा, {format_nepali_number(quality_households)} घरपरिवारहरू "
                    f"({format_nepali_percentage(quality_percentage)}) को कालोपत्रे र ढुंगामाटो सडकको पहुँच रहेको छ। "
                    f"यसले उत्कृष्ट र राम्रो यातायात सुविधाको संकेत गर्छ।"
                )

            # Basic road access analysis
            if "EARTHEN" in municipality_data:
                earthen_households = municipality_data["EARTHEN"]["population"]
                earthen_percentage = municipality_data["EARTHEN"]["percentage"]
                analysis_parts.append(
                    f"कच्ची सडकको पहुँच भएका {format_nepali_number(earthen_households)} घरपरिवारहरू "
                    f"({format_nepali_percentage(earthen_percentage)}) को आधारभूत यातायात सुविधा उपलब्ध छ। "
                    f"यी सडकहरूको गुणस्तर सुधार गर्न सकिने सम्भावना छ।"
                )

            # No road access analysis
            if "NO_ROAD" in municipality_data:
                no_road_households = municipality_data["NO_ROAD"]["population"]
                no_road_percentage = municipality_data["NO_ROAD"]["percentage"]
                analysis_parts.append(
                    f"सडक पहुँच नभएका {format_nepali_number(no_road_households)} घरपरिवारहरू "
                    f"({format_nepali_percentage(no_road_percentage)}) लाई तत्काल सडक जडान गर्न आवश्यक छ। "
                    f"यसले यातायात सुविधामा गम्भीर बाधाको संकेत गर्छ।"
                )

            # Blacktopped road analysis
            if "BLACKTOPPED" in municipality_data:
                blacktopped_households = municipality_data["BLACKTOPPED"]["population"]
                blacktopped_percentage = municipality_data["BLACKTOPPED"]["percentage"]
                analysis_parts.append(
                    f"कालोपत्रे सडकको पहुँच भएका {format_nepali_number(blacktopped_households)} घरपरिवारहरू "
                    f"({format_nepali_percentage(blacktopped_percentage)}) लाई उत्कृष्ट यातायात सुविधा प्राप्त छ। "
                    f"यसले आधुनिक पूर्वाधारको विकासको संकेत गर्छ।"
                )

        # Ward-wise comparative analysis
        if ward_data and len(ward_data) > 1:
            # Find wards with best and worst road infrastructure
            ward_quality_scores = {}
            for ward_num, ward_info in ward_data.items():
                # Calculate quality score based on road types
                quality_score = 0
                total_ward_households = ward_info["total_population"]

                if "BLACKTOPPED" in ward_info["road_types"]:
                    quality_score += (
                        (
                            ward_info["road_types"]["BLACKTOPPED"]["population"]
                            / total_ward_households
                        )
                        * 100
                        * 4
                    )
                if "GRAVELED" in ward_info["road_types"]:
                    quality_score += (
                        (
                            ward_info["road_types"]["GRAVELED"]["population"]
                            / total_ward_households
                        )
                        * 100
                        * 3
                    )
                if "EARTHEN" in ward_info["road_types"]:
                    quality_score += (
                        (
                            ward_info["road_types"]["EARTHEN"]["population"]
                            / total_ward_households
                        )
                        * 100
                        * 2
                    )

                ward_quality_scores[ward_num] = quality_score

            best_ward = max(ward_quality_scores.items(), key=lambda x: x[1])
            worst_ward = min(ward_quality_scores.items(), key=lambda x: x[1])

            if best_ward[0] != worst_ward[0]:
                analysis_parts.append(
                    f"वडागत विश्लेषणमा, वडा नं. {best_ward[0]} मा सबैभन्दा राम्रो सडक पूर्वाधार रहेको छ "
                    f"भने वडा नं. {worst_ward[0]} मा सडक पूर्वाधारमा सुधारको आवश्यकता छ।"
                )

        # Economic and social implications
        if quality_percentage > 50:
            analysis_parts.append(
                "गुणस्तरीय सडक पहुँचले स्थानीय अर्थतन्त्र, पर्यटन विकास र सामाजिक सेवाहरूको पहुँचमा सकारात्मक प्रभाव पारेको छ।"
            )
        else:
            analysis_parts.append(
                "सडक पूर्वाधार विकासले आर्थिक गतिविधि बृद्धि, रोजगारी सिर्जना र जीवनस्तर सुधारमा महत्वपूर्ण भूमिका खेल्न सक्छ।"
            )

        # Accessibility and connectivity
        if (
            "NO_ROAD" in municipality_data
            and municipality_data["NO_ROAD"]["percentage"] > 20
        ):
            analysis_parts.append(
                "सडक पहुँच नभएका क्षेत्रहरूमा शिक्षा, स्वास्थ्य र आपतकालीन सेवाहरूको पहुँचमा गम्भीर बाधा छ।"
            )

        # Development opportunities
        if (
            "EARTHEN" in municipality_data
            and municipality_data["EARTHEN"]["percentage"] > 30
        ):
            analysis_parts.append(
                "कच्ची सडकको उच्च प्रतिशतले सडक गुणस्तर सुधारको व्यापक अवसरहरू देखाउँछ।"
            )

        # Future recommendations
        analysis_parts.append(
            "भविष्यमा सडक पूर्वाधार विकासका लागि व्यापक योजना, बजेट विनियोजन र चरणबद्ध कार्यान्वयन आवश्यक छ।"
        )

        # Regional connectivity importance
        analysis_parts.append(
            "क्षेत्रीय र राष्ट्रिय सडक सञ्जालसँगको जडानले व्यापार, उद्योग र सेवा क्षेत्रको विकासमा महत्वपूर्ण योगदान पुर्याउँछ।"
        )

        # Maintenance and sustainability
        analysis_parts.append(
            "निर्मित सडकहरूको नियमित मर्मतसम्भार र दिगो व्यवस्थापनले दीर्घकालीन सडक गुणस्तर कायम राख्न आवश्यक छ।"
        )

        return " ".join(analysis_parts)

    def generate_pie_chart(self, data, title="सडकको अवस्था अनुसार घरपरिवार वितरण"):
        """Generate pie chart for road status data"""
        return self.chart_generator.generate_pie_chart_svg(
            data,
            include_title=False,
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
        total_count = data.get("total_households", 0)

        return {
            "municipality_data": data.get("municipality_data", {}),
            "ward_data": data.get("ward_data", {}),
            "total_households": total_count,
            "coherent_analysis": coherent_analysis,
            "pdf_charts": {"road_status": charts},
            "section_title": self.get_section_title(),
            "section_number": self.get_section_number(),
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
                "road_types": len(self.data["municipality_data"]),
                "wards": len(self.data["ward_data"]),
            },
            "road_status_breakdown": self.data["municipality_data"],
            "ward_breakdown": self.data["ward_data"],
            "analysis": self.data["coherent_analysis"],
        }
