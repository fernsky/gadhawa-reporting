"""
Solid Waste Management Social Processor

Handles solid waste management social data processing, chart generation, and report formatting.
"""

from django.db import models
from .base import BaseSocialProcessor, BaseSocialReportFormatter
from ..models import WardWiseSolidWasteManagement, SolidWasteManagementChoice
from apps.reports.utils.nepali_numbers import (
    format_nepali_number,
    format_nepali_percentage,
    to_nepali_digits,
)


class SolidWasteManagementProcessor(BaseSocialProcessor):
    """Processor for solid waste management social data"""

    def __init__(self):
        super().__init__()
        # Customize chart dimensions for solid waste management
        self.pie_chart_width = 900
        self.pie_chart_height = 450
        self.chart_radius = 140
        # Set solid waste management-specific colors with meaningful associations
        self.chart_generator.colors = {
            "COMPOST_MANURE": "#4CAF50",  # Green - Eco-friendly composting
            "HOME_COLLECTION": "#2196F3",  # Blue - Organized collection
            "WASTE_COLLECTING_PLACE": "#00BCD4",  # Cyan - Designated collection
            "DIGGING": "#795548",  # Brown - Burying/digging
            "BURNING": "#FF5722",  # Deep Orange - Burning (harmful)
            "RIVER": "#3F51B5",  # Indigo - Water bodies (concerning)
            "ROAD_OR_PUBLIC_PLACE": "#F44336",  # Red - Public littering (problematic)
            "OTHER": "#9C27B0",  # Purple - Other methods
        }

    def get_section_title(self):
        return "फोहोरमैला व्यवस्थापन"

    def get_section_number(self):
        return "५.३.५"

    def get_data(self):
        """Get solid waste management data - both municipality-wide and ward-wise"""
        # Municipality-wide summary
        waste_management_data = {}
        total_households = 0

        for waste_choice in SolidWasteManagementChoice.choices:
            waste_code = waste_choice[0]
            waste_name = waste_choice[1]

            waste_households = (
                WardWiseSolidWasteManagement.objects.filter(
                    solid_waste_management=waste_code
                ).aggregate(total=models.Sum("households"))["total"]
                or 0
            )

            print(waste_households)

            if (
                waste_households > 0
            ):  # Only include waste management types with households
                waste_management_data[waste_code] = {
                    "name_english": waste_code,
                    "name_nepali": waste_name,
                    "population": waste_households,  # Using households as population for consistency
                    "percentage": 0,  # Will be calculated below
                }
                total_households += waste_households

        # Calculate percentages
        for waste_code in waste_management_data:
            if total_households > 0:
                waste_management_data[waste_code]["percentage"] = (
                    waste_management_data[waste_code]["population"]
                    / total_households
                    * 100
                )

        # Ward-wise data
        ward_data = {}
        for ward_num in range(1, 8):  # Wards 1-7
            ward_households = (
                WardWiseSolidWasteManagement.objects.filter(
                    ward_number=ward_num
                ).aggregate(total=models.Sum("households"))["total"]
                or 0
            )

            if ward_households > 0:
                ward_data[ward_num] = {
                    "ward_number": ward_num,
                    "ward_name": f"वडा नं. {to_nepali_digits(ward_num)}",
                    "total_population": ward_households,  # Using households
                    "waste_methods": {},
                }

                # Waste management type breakdown for this ward
                for waste_choice in SolidWasteManagementChoice.choices:
                    waste_code = waste_choice[0]
                    waste_name = waste_choice[1]

                    waste_households_ward = (
                        WardWiseSolidWasteManagement.objects.filter(
                            ward_number=ward_num, solid_waste_management=waste_code
                        ).aggregate(total=models.Sum("households"))["total"]
                        or 0
                    )

                    if waste_households_ward > 0:
                        ward_data[ward_num]["waste_methods"][waste_code] = {
                            "name_nepali": waste_name,
                            "population": waste_households_ward,
                            "percentage": (
                                (waste_households_ward / ward_households * 100)
                                if ward_households > 0
                                else 0
                            ),
                        }

        return {
            "municipality_data": waste_management_data,
            "ward_data": ward_data,
            "total_households": total_households,
        }

    def generate_analysis_text(self, data):
        """Generate comprehensive analysis text for solid waste management"""
        if not data or data["total_households"] == 0:
            return "फोहोरमैला व्यवस्थापनको तथ्याङ्क उपलब्ध छैन।"

        total_households = data["total_households"]
        municipality_data = data["municipality_data"]
        ward_data = data["ward_data"]

        analysis_parts = []

        # Overall summary
        analysis_parts.append(
            f"लुङ्ग्री गाउँपालिकामा कुल {format_nepali_number(total_households)} घरपरिवारको ठोस फोहोर व्यवस्थापनको अवस्था विश्लेषण गर्दा विभिन्न विधिहरूको प्रयोग भइरहेको देखिन्छ।"
        )

        # Environmental impact analysis
        if municipality_data:
            # Find the most common waste management method
            dominant_method = max(
                municipality_data.items(), key=lambda x: x[1]["population"]
            )
            analysis_parts.append(
                f"फोहोर व्यवस्थापनको विधिको आधारमा विश्लेषण गर्दा, {dominant_method[1]['name_nepali']} विधि सबैभन्दा बढी प्रयोग हुने "
                f"{format_nepali_number(dominant_method[1]['population'])} घरपरिवार "
                f"({format_nepali_percentage(dominant_method[1]['percentage'])}) ले अपनाएको देखिन्छ।"
            )

            # Environmental sustainability analysis
            eco_friendly_methods = [
                "COMPOST_MANURE",
                "HOME_COLLECTION",
                "WASTE_COLLECTING_PLACE",
            ]
            eco_friendly_households = sum(
                municipality_data.get(method, {}).get("population", 0)
                for method in eco_friendly_methods
            )
            eco_friendly_percentage = (
                (eco_friendly_households / total_households * 100)
                if total_households > 0
                else 0
            )

            if eco_friendly_percentage > 0:
                analysis_parts.append(
                    f"वातावरणमैत्री फोहोर व्यवस्थापनको दृष्टिकोणले हेर्दा, {format_nepali_number(eco_friendly_households)} घरपरिवार "
                    f"({format_nepali_percentage(eco_friendly_percentage)}) ले कम्पोस्ट मल, घर संकलन र फोहोर संकलन ठाउँ जस्ता वातावरणमैत्री विधिहरू अपनाएका छन्।"
                )

            # Composting analysis
            if "COMPOST_MANURE" in municipality_data:
                compost_households = municipality_data["COMPOST_MANURE"]["population"]
                compost_percentage = municipality_data["COMPOST_MANURE"]["percentage"]
                analysis_parts.append(
                    f"विशेष गरी {format_nepali_number(compost_households)} घरपरिवार "
                    f"({format_nepali_percentage(compost_percentage)}) ले कम्पोस्ट मल बनाउने विधि अपनाएर "
                    f"फोहोरलाई उपयोगी खादमा रूपान्तरण गरिरहेका छन् जुन दिगो विकासको उत्कृष्ट उदाहरण हो।"
                )

            # Environmental concerns
            harmful_methods = ["BURNING", "RIVER", "ROAD_OR_PUBLIC_PLACE"]
            harmful_households = sum(
                municipality_data.get(method, {}).get("population", 0)
                for method in harmful_methods
            )
            harmful_percentage = (
                (harmful_households / total_households * 100)
                if total_households > 0
                else 0
            )

            if harmful_percentage > 0:
                analysis_parts.append(
                    f"तर, {format_nepali_number(harmful_households)} घरपरिवार "
                    f"({format_nepali_percentage(harmful_percentage)}) ले जलाउने, नदीमा फाल्ने र सार्वजनिक ठाउँमा फाल्ने जस्ता "
                    f"वातावरणका लागि हानिकारक विधिहरू प्रयोग गरिरहेका छन् जसले वातावरणीय प्रदूषण निम्त्याउन सक्छ।"
                )

            # Burning analysis (specific environmental concern)
            if "BURNING" in municipality_data:
                burning_households = municipality_data["BURNING"]["population"]
                burning_percentage = municipality_data["BURNING"]["percentage"]
                analysis_parts.append(
                    f"फोहोर जलाउने विधि अपनाउने {format_nepali_number(burning_households)} घरपरिवार "
                    f"({format_nepali_percentage(burning_percentage)}) को कारण वायु प्रदूषण र स्वास्थ्यमा नकारात्मक प्रभाव पर्न सक्छ।"
                )

        # Ward-wise comparative analysis
        if ward_data and len(ward_data) > 1:
            # Find wards with best and worst practices
            best_ward = None
            worst_ward = None
            best_eco_percentage = 0
            worst_eco_percentage = 100

            for ward_num, ward_info in ward_data.items():
                # Calculate eco-friendly percentage for this ward
                eco_friendly_count = sum(
                    ward_info["waste_methods"].get(method, {}).get("population", 0)
                    for method in [
                        "COMPOST_MANURE",
                        "HOME_COLLECTION",
                        "WASTE_COLLECTING_PLACE",
                    ]
                )
                eco_percentage = (
                    (eco_friendly_count / ward_info["total_population"] * 100)
                    if ward_info["total_population"] > 0
                    else 0
                )

                if eco_percentage > best_eco_percentage:
                    best_eco_percentage = eco_percentage
                    best_ward = ward_num

                if eco_percentage < worst_eco_percentage:
                    worst_eco_percentage = eco_percentage
                    worst_ward = ward_num

            if best_ward and worst_ward and best_ward != worst_ward:
                analysis_parts.append(
                    f"वडागत विश्लेषणमा, वडा नं. {best_ward} मा सबैभन्दा राम्रो वातावरणमैत्री फोहोर व्यवस्थापन "
                    f"({format_nepali_percentage(best_eco_percentage)} घरपरिवारले वातावरणमैत्री विधि अपनाएको) छ "
                    f"भने वडा नं. {worst_ward} मा सुधारको आवश्यकता "
                    f"({format_nepali_percentage(worst_eco_percentage)} घरपरिवारले मात्र वातावरणमैत्री विधि अपनाएको) देखिन्छ।"
                )

        # Health and sanitation implications
        analysis_parts.append(
            "उचित फोहोर व्यवस्थापनले सार्वजनिक स्वास्थ्य र वातावरणीय स्वच्छतामा महत्वपूर्ण भूमिका खेल्छ। "
            "अव्यवस्थित फोहोर व्यवस्थापनले रोगजनक किटाणुहरूको फैलावट र वातावरणीय प्रदूषण निम्त्याउन सक्छ।"
        )

        # Economic benefits of proper waste management
        if (
            "COMPOST_MANURE" in municipality_data
            and municipality_data["COMPOST_MANURE"]["population"] > 0
        ):
            analysis_parts.append(
                "कम्पोस्ट मल बनाउने प्रक्रियाले न केवल फोहोरको समस्या समाधान गर्छ बल्कि कृषि उत्पादकतामा वृद्धि गरी आर्थिक फाइदा पनि दिन्छ।"
            )

        # Future development recommendations
        if harmful_percentage > 30:  # If more than 30% use harmful methods
            analysis_parts.append(
                "भविष्यमा फोहोर व्यवस्थापन सुधारका लागि सामुदायिक सचेतना कार्यक्रम, कम्पोस्ट बनाउने तालिम र संगठित फोहोर संकलन प्रणालीको विकास आवश्यक छ।"
            )

        # Community awareness importance
        analysis_parts.append(
            "समुदायिक सहभागिता र सचेतनाले फोहोर व्यवस्थापनमा आमूल परिवर्तन ल्याउन सक्छ र दिगो विकासमा योगदान पुर्‍याउन सक्छ।"
        )

        return " ".join(analysis_parts)

    def generate_pie_chart(
        self, data, title="फोहोरमैला व्यवस्थापन विधि अनुसार घरपरिवार वितरण"
    ):
        """Generate pie chart for solid waste management data"""
        return self.chart_generator.generate_pie_chart_svg(
            data,
            include_title=False,
            title_nepali=title,
            title_english="Household Distribution by Solid Waste Management Method",
        )

    def process_for_pdf(self):
        """Process solid waste management data for PDF generation including charts"""
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
            "pdf_charts": {"solid_waste_management": charts},
            "section_title": self.get_section_title(),
            "section_number": self.get_section_number(),
        }


class SolidWasteManagementReportFormatter(BaseSocialReportFormatter):
    """Report formatter for solid waste management social data"""

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
                "waste_management_methods": len(self.data["municipality_data"]),
                "wards": len(self.data["ward_data"]),
            },
            "waste_management_breakdown": self.data["municipality_data"],
            "ward_breakdown": self.data["ward_data"],
            "analysis": self.data["coherent_analysis"],
        }
