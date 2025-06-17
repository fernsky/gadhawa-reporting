"""
Remittance Expenses Economics Processor

Handles remittance expenses economics data processing, chart generation, and report formatting.
"""

from django.db import models
from .base import BaseEconomicsProcessor, BaseEconomicsReportFormatter
from ..models import WardWiseRemittanceExpenses, RemittanceExpenseTypeChoice
from apps.reports.utils.nepali_numbers import (
    format_nepali_number,
    format_nepali_percentage,
)


class RemittanceExpensesProcessor(BaseEconomicsProcessor):
    """Processor for remittance expenses economics data"""

    def __init__(self):
        super().__init__()
        # Customize chart dimensions for remittance expenses
        self.pie_chart_width = 950
        self.pie_chart_height = 500
        self.chart_radius = 150
        # Set remittance-specific colors with meaningful associations
        self.chart_generator.colors = {
            "education": "#2196F3",  # Blue - Educational investment
            "health": "#F44336",  # Red - Health expenses
            "household_use": "#4CAF50",  # Green - Basic household needs
            "festivals": "#FF9800",  # Orange - Cultural/social expenses
            "loan_payment": "#9C27B0",  # Purple - Financial obligations
            "loaned_others": "#E91E63",  # Pink - Financial assistance
            "saving": "#00BCD4",  # Cyan - Financial security
            "house_construction": "#795548",  # Brown - Infrastructure
            "land_ownership": "#607D8B",  # Blue Grey - Assets
            "jwellery_purchase": "#FFC107",  # Amber - Luxury/investment
            "goods_purchase": "#8BC34A",  # Light Green - Consumer goods
            "business_investment": "#3F51B5",  # Indigo - Business growth
            "other": "#9E9E9E",  # Grey - Other expenses
            "unknown": "#757575",  # Dark Grey - Unknown
        }

    def get_section_title(self):
        return "रेमिटेन्स प्राप्त गरेको र खर्चको विवरण"

    def get_section_number(self):
        return "६.२.५"

    def get_data(self):
        """Get remittance expenses data - both municipality-wide and ward-wise"""
        # Municipality-wide summary
        expenses_data = {}
        total_households = 0

        for expense_choice in RemittanceExpenseTypeChoice.choices:
            expense_code = expense_choice[0]
            expense_name = expense_choice[1]

            expense_households = (
                WardWiseRemittanceExpenses.objects.filter(
                    remittance_expense=expense_code
                ).aggregate(total=models.Sum("households"))["total"]
                or 0
            )

            if expense_households > 0:  # Only include expense types with households
                expenses_data[expense_code] = {
                    "name_english": expense_code,
                    "name_nepali": expense_name,
                    "households": expense_households,
                    "percentage": 0,  # Will be calculated below
                }
                total_households += expense_households

        # Calculate percentages
        for expense_code in expenses_data:
            if total_households > 0:
                expenses_data[expense_code]["percentage"] = (
                    expenses_data[expense_code]["households"] / total_households * 100
                )

        # Ward-wise data
        ward_data = {}
        for ward_num in range(1, 8):  # Wards 1-7
            ward_households = (
                WardWiseRemittanceExpenses.objects.filter(
                    ward_number=ward_num
                ).aggregate(total=models.Sum("households"))["total"]
                or 0
            )

            if ward_households > 0:
                ward_data[ward_num] = {
                    "ward_number": ward_num,
                    "ward_name": f"वडा नं. {ward_num}",
                    "total_households": ward_households,
                    "expense_types": {},
                }

                # Expense type breakdown for this ward
                for expense_choice in RemittanceExpenseTypeChoice.choices:
                    expense_code = expense_choice[0]
                    expense_name = expense_choice[1]

                    expense_households_ward = (
                        WardWiseRemittanceExpenses.objects.filter(
                            ward_number=ward_num, remittance_expense=expense_code
                        ).aggregate(total=models.Sum("households"))["total"]
                        or 0
                    )

                    if expense_households_ward > 0:
                        ward_data[ward_num]["expense_types"][expense_code] = {
                            "name_nepali": expense_name,
                            "households": expense_households_ward,
                            "percentage": (
                                (expense_households_ward / ward_households * 100)
                                if ward_households > 0
                                else 0
                            ),
                        }

        return {
            "municipality_data": expenses_data,
            "ward_data": ward_data,
            "total_households": total_households,
        }

    def generate_analysis_text(self, data):
        """Generate comprehensive analysis text for remittance expenses"""
        if not data or data["total_households"] == 0:
            return "रेमिटेन्स खर्चको तथ्याङ्क उपलब्ध छैन।"

        total_households = data["total_households"]
        municipality_data = data["municipality_data"]
        ward_data = data["ward_data"]

        analysis_parts = []

        # Overall summary
        analysis_parts.append(
            f"लुङ्ग्री गाउँपालिकामा कुल {format_nepali_number(total_households)} घरपरिवारहरूले विभिन्न कार्यहरूमा रेमिटेन्स प्राप्त गरेको रकम खर्च गरेका छन्।"
        )

        # Dominant expense analysis
        if municipality_data:
            # Find the most common expense type
            dominant_expense = max(
                municipality_data.items(), key=lambda x: x[1]["households"]
            )
            analysis_parts.append(
                f"रेमिटेन्स खर्चको मुख्य कार्यक्षेत्रको आधारमा विश्लेषण गर्दा, {dominant_expense[1]['name_nepali']} सबैभन्दा बढी "
                f"{format_nepali_number(dominant_expense[1]['households'])} घरपरिवारहरूले "
                f"({format_nepali_percentage(dominant_expense[1]['percentage'])}) यस कार्यमा रेमिटेन्स रकम खर्च गरेको देखिन्छ।"
            )

            # Essential services analysis
            essential_services = ["education", "health", "household_use"]
            essential_households = sum(
                municipality_data.get(service, {}).get("households", 0)
                for service in essential_services
            )
            essential_percentage = (
                (essential_households / total_households * 100)
                if total_households > 0
                else 0
            )

            if essential_percentage > 0:
                analysis_parts.append(
                    f"आधारभूत सेवाहरूको दृष्टिकोणले हेर्दा, {format_nepali_number(essential_households)} घरपरिवारहरू "
                    f"({format_nepali_percentage(essential_percentage)}) ले शिक्षा, स्वास्थ्य र घरेलु प्रयोगजस्ता "
                    f"आधारभूत आवश्यकताहरूमा रेमिटेन्स रकम खर्च गरेका छन्।"
                )

            # Education investment analysis
            if "education" in municipality_data:
                education_households = municipality_data["education"]["households"]
                education_percentage = municipality_data["education"]["percentage"]
                analysis_parts.append(
                    f"शिक्षा क्षेत्रमा {format_nepali_number(education_households)} घरपरिवारहरू "
                    f"({format_nepali_percentage(education_percentage)}) ले रेमिटेन्स रकम खर्च गरेको देखिन्छ। "
                    f"यसले मानव पूँजी विकासमा रेमिटेन्सको महत्वपूर्ण भूमिकालाई देखाउँछ।"
                )

            # Health expenses analysis
            if "health" in municipality_data:
                health_households = municipality_data["health"]["households"]
                health_percentage = municipality_data["health"]["percentage"]
                analysis_parts.append(
                    f"स्वास्थ्य सेवामा {format_nepali_number(health_households)} घरपरिवारहरू "
                    f"({format_nepali_percentage(health_percentage)}) ले रेमिटेन्स रकम खर्च गरेका छन्। "
                    f"यसले स्वास्थ्य सेवाको पहुँच र गुणस्तरमा सुधारको आवश्यकतालाई संकेत गर्छ।"
                )

            # Infrastructure and asset building
            asset_building = [
                "house_construction",
                "land_ownership",
                "business_investment",
            ]
            asset_households = sum(
                municipality_data.get(asset, {}).get("households", 0)
                for asset in asset_building
            )
            asset_percentage = (
                (asset_households / total_households * 100)
                if total_households > 0
                else 0
            )

            if asset_percentage > 0:
                analysis_parts.append(
                    f"पूर्वाधार र सम्पत्ति निर्माणमा {format_nepali_number(asset_households)} घरपरिवारहरू "
                    f"({format_nepali_percentage(asset_percentage)}) ले घर निर्माण, जमिन खरिद र व्यापारिक लगानीमा "
                    f"रेमिटेन्स रकम खर्च गरेका छन्। यसले दीर्घकालीन आर्थिक सुरक्षाको दृष्टिकोणलाई देखाउँछ।"
                )

            # Financial obligations analysis
            if "loan_payment" in municipality_data:
                loan_households = municipality_data["loan_payment"]["households"]
                loan_percentage = municipality_data["loan_payment"]["percentage"]
                analysis_parts.append(
                    f"ऋण भुक्तानीमा {format_nepali_number(loan_households)} घरपरिवारहरू "
                    f"({format_nepali_percentage(loan_percentage)}) ले रेमिटेन्स रकम प्रयोग गरेका छन्। "
                    f"यसले आर्थिक दायित्वको बोझ र ऋणको प्रभावलाई संकेत गर्छ।"
                )

            # Savings analysis
            if "saving" in municipality_data:
                saving_households = municipality_data["saving"]["households"]
                saving_percentage = municipality_data["saving"]["percentage"]
                analysis_parts.append(
                    f"सकारात्मक पक्षमा, {format_nepali_number(saving_households)} घरपरिवारहरूले "
                    f"({format_nepali_percentage(saving_percentage)}) रेमिटेन्स रकम बचतमा राखेका छन्। "
                    f"यसले भविष्यको आर्थिक सुरक्षाको चेतनालाई देखाउँछ।"
                )

            # Cultural and social expenses
            if "festivals" in municipality_data:
                festival_households = municipality_data["festivals"]["households"]
                festival_percentage = municipality_data["festivals"]["percentage"]
                analysis_parts.append(
                    f"सांस्कृतिक र सामाजिक गतिविधिहरूमा {format_nepali_number(festival_households)} घरपरिवारहरू "
                    f"({format_nepali_percentage(festival_percentage)}) ले चाडपर्वमा रेमिटेन्स रकम खर्च गरेका छन्। "
                    f"यसले सामाजिक सम्बन्ध र सांस्कृतिक मूल्यहरूको संरक्षणलाई देखाउँछ।"
                )

        # Ward-wise comparative analysis
        if ward_data and len(ward_data) > 1:
            # Find wards with highest and lowest remittance usage
            ward_remittance_usage = {}
            for ward_num, ward_info in ward_data.items():
                ward_remittance_usage[ward_num] = ward_info["total_households"]

            highest_ward = max(ward_remittance_usage.items(), key=lambda x: x[1])
            lowest_ward = min(ward_remittance_usage.items(), key=lambda x: x[1])

            if highest_ward[0] != lowest_ward[0]:
                analysis_parts.append(
                    f"वडागत विश्लेषणमा, वडा नं. {highest_ward[0]} मा सबैभन्दा बढी "
                    f"{format_nepali_number(highest_ward[1])} घरपरिवारहरूले रेमिटेन्स रकम विभिन्न कार्यमा खर्च गरेका छन् "
                    f"भने वडा नं. {lowest_ward[0]} मा सबैभन्दा कम "
                    f"{format_nepali_number(lowest_ward[1])} घरपरिवारहरूले रेमिटेन्स रकम खर्च गरेका छन्।"
                )

        # Economic impact analysis
        analysis_parts.append(
            "रेमिटेन्स रकमको उपयोगले स्थानीय अर्थतन्त्रमा सकारात्मक प्रभाव पारेको छ। "
            "शिक्षा र स्वास्थ्यमा लगानीले मानव पूँजी विकासमा योगदान पुर्याएको छ।"
        )

        # Development implications
        if essential_percentage > 50:
            analysis_parts.append(
                "आधारभूत सेवाहरूमा उच्च खर्चले स्थानीय सेवाहरूको गुणस्तर र पहुँचमा सुधारको आवश्यकतालाई देखाउँछ।"
            )

        # Future recommendations
        analysis_parts.append(
            "भविष्यमा रेमिटेन्स रकमको अझ प्रभावकारी उपयोगका लागि उत्पादनमूलक क्षेत्र, "
            "व्यापार र उद्योगमा लगानी प्रोत्साहन गर्ने नीति आवश्यक छ।"
        )

        # Financial literacy importance
        analysis_parts.append(
            "आर्थिक साक्षरता कार्यक्रमहरूले रेमिटेन्स रकमको उत्पादनमूलक उपयोगमा वृद्धि गर्न सक्छ।"
        )

        return " ".join(analysis_parts)

    def generate_pie_chart(
        self, data, title="रेमिटेन्स खर्चको कार्यक्षेत्र अनुसार घरपरिवार वितरण"
    ):
        """Generate pie chart for remittance expenses data"""
        return self.chart_generator.generate_pie_chart_svg(
            data,
            include_title=False,
            title_nepali=title,
            title_english="Household Distribution by Remittance Expense Categories",
        )

    def process_for_pdf(self):
        """Process remittance expenses data for PDF generation including charts"""
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
            "pdf_charts": {"remittance_expenses": charts},
            "section_title": self.get_section_title(),
            "section_number": self.get_section_number(),
        }


class RemittanceExpensesReportFormatter(BaseEconomicsReportFormatter):
    """Report formatter for remittance expenses economics data"""

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
                "expense_categories": len(self.data["municipality_data"]),
                "wards": len(self.data["ward_data"]),
            },
            "expense_breakdown": self.data["municipality_data"],
            "ward_breakdown": self.data["ward_data"],
            "analysis": self.data["coherent_analysis"],
        }
