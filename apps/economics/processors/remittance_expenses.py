"""
Remittance Expenses Economics Processor

Handles remittance expenses data processing, chart generation, and report formatting.
"""

from .base import BaseEconomicsProcessor, BaseEconomicsReportFormatter
from ..models import WardWiseRemittanceExpenses
from apps.demographics.utils.svg_chart_generator import DEFAULT_COLORS
from apps.reports.utils.nepali_numbers import (
    format_nepali_number,
    format_nepali_percentage,
)


class RemittanceExpensesProcessor(BaseEconomicsProcessor):
    """Processor for remittance expenses data"""

    def __init__(self):
        super().__init__()
        # Customize chart dimensions for remittance expenses
        self.pie_chart_width = 900
        self.pie_chart_height = 450
        self.bar_chart_width = 1000
        self.bar_chart_height = 600
        self.chart_radius = 130
        # Set remittance expenses-specific colors
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
        }

    def get_section_title(self):
        return "रेमिटेन्स खर्च"

    def get_section_number(self):
        return "४.२"

    def get_data(self):
        """Get remittance expenses data - both municipality-wide and ward-wise"""
        # Municipality-wide summary
        municipality_data = {}

        # Initialize all expense categories
        from apps.economics.models import RemittanceExpenseTypeChoice

        expense_types = dict(RemittanceExpenseTypeChoice.choices)

        for expense_code, expense_name in expense_types.items():
            municipality_data[expense_code] = {
                "households": 0,
                "percentage": 0.0,
                "name_nepali": expense_name,
            }

        # Ward-wise data for bar chart and detailed table
        ward_data = {}
        for ward_num in range(1, 9):  # Wards 1-8 based on new sample data
            ward_data[ward_num] = {
                "ward_name": f"वडा नं. {ward_num}",
                "expense_types": {},
            }
            # Initialize expenses for each ward
            for expense_code, expense_name in expense_types.items():
                ward_data[ward_num]["expense_types"][expense_code] = {
                    "households": 0,
                    "percentage": 0.0,
                    "name_nepali": expense_name,
                }

        # Get actual data from database
        total_households = 0
        for expense_obj in WardWiseRemittanceExpenses.objects.all():
            expense = expense_obj.remittance_expense
            ward_num = expense_obj.ward_number
            households = expense_obj.households

            # Add to municipality-wide totals
            if expense in municipality_data:
                municipality_data[expense]["households"] += households
                total_households += households

            # Add to ward-wise data
            if (
                ward_num in ward_data
                and expense in ward_data[ward_num]["expense_types"]
            ):
                ward_data[ward_num]["expense_types"][expense][
                    "households"
                ] += households

        # Calculate percentages for municipality-wide data
        if total_households > 0:
            for expense, data in municipality_data.items():
                data["percentage"] = (data["households"] / total_households) * 100

        # Calculate ward totals and percentages
        for ward_num, ward_info in ward_data.items():
            ward_total = sum(
                demo["households"] for demo in ward_info["expense_types"].values()
            )
            ward_info["total_households"] = ward_total

            # Calculate percentages within each ward
            if ward_total > 0:
                for expense, demo in ward_info["expense_types"].items():
                    demo["percentage"] = (demo["households"] / ward_total) * 100

        return {
            "municipality_data": municipality_data,
            "ward_data": ward_data,
            "total_households": total_households,
        }

    def generate_report_content(self, data):
        """Generate remittance expenses-specific report content"""
        formatter = self.RemittanceExpensesReportFormatter()
        return formatter.generate_formal_report(
            data["municipality_data"], data["ward_data"], data["total_households"]
        )

    def get_chart_key(self):
        """Get the key for storing charts in PDF context"""
        return "remittance_expenses"

    def generate_chart_svg(self, data, chart_type="pie"):
        """Generate remittance expenses chart SVG using SVGChartGenerator"""
        if chart_type == "pie":
            return self.chart_generator.generate_pie_chart_svg(
                data["municipality_data"],
                include_title=False,
                title_nepali="रेमिटेन्स खर्चका आधारमा वितरण",
                title_english="Distribution by Remittance Expenses",
            )
        elif chart_type == "bar":
            return self.chart_generator.generate_bar_chart_svg(
                data["ward_data"],
                include_title=False,
                title_nepali="वडा अनुसार रेमिटेन्स खर्चका आधारमा वितरण",
                title_english="Remittance Expenses Distribution by Ward",
            )
        return None

    def generate_and_save_charts(self, data):
        """Generate and save both pie and bar charts for remittance expenses data"""
        charts = {}
        category_name = "remittance_expenses"

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

        # Transform data for chart generator (households -> population)
        transformed_pie_data = {}
        for key, value in pie_data.items():
            if isinstance(value, dict) and value.get("households", 0) > 0:
                transformed_pie_data[key] = {
                    "population": value[
                        "households"
                    ],  # Transform households to population
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
                # Transform expense_types to demographics with population
                if "expense_types" in ward_info:
                    for expense_type, expense_data in ward_info[
                        "expense_types"
                    ].items():
                        if (
                            isinstance(expense_data, dict)
                            and expense_data.get("households", 0) > 0
                        ):
                            transformed_bar_data[ward_num]["demographics"][
                                expense_type
                            ] = {
                                "population": expense_data[
                                    "households"
                                ],  # Transform households to population
                                "name_nepali": expense_data.get(
                                    "name_nepali", expense_type
                                ),
                                "percentage": expense_data.get("percentage", 0),
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

    class RemittanceExpensesReportFormatter(BaseEconomicsReportFormatter):
        """Remittance expenses-specific report formatter"""

        def generate_formal_report(self, expenses_data, ward_data, total_households):
            """Generate remittance expenses formal report content"""

            # Find major expense categories
            major_expenses = []
            for expense_type, data in expenses_data.items():
                if data["households"] > 0:
                    major_expenses.append(
                        (data["name_nepali"], data["households"], data["percentage"])
                    )

            major_expenses.sort(key=lambda x: x[1], reverse=True)

            # Build comprehensive analysis
            content = []

            # Introduction
            nepali_total = format_nepali_number(total_households)
            content.append(
                f"""लुङ्गी गाउँपालिकामा कुल {nepali_total} घरपरिवारहरूले विभिन्न कार्यक्षेत्रहरूमा रेमिटेन्स प्राप्त गरेको रकम खर्च गरेका छन् । रेमिटेन्स खर्चको आधारमा घरपरिवारको वितरण गर्दा गाउँपालिकाको आर्थिक प्राथमिकता र पारिवारिक आवश्यकताको अवस्था देखिन्छ ।"""
            )

            # Top expense categories analysis
            if len(major_expenses) >= 3:
                top_three = major_expenses[:3]
                first_exp = top_three[0]
                second_exp = top_three[1]
                third_exp = top_three[2]

                first_hh = format_nepali_number(first_exp[1])
                first_pct = format_nepali_percentage(first_exp[2])
                second_hh = format_nepali_number(second_exp[1])
                second_pct = format_nepali_percentage(second_exp[2])
                third_hh = format_nepali_number(third_exp[1])
                third_pct = format_nepali_percentage(third_exp[2])

                content.append(
                    f"""सबैभन्दा बढी {first_hh} घरपरिवार अर्थात् {first_pct} प्रतिशत घरपरिवारले {first_exp[0]}मा रेमिटेन्स रकम खर्च गरेका छन् भने दोस्रोमा {second_hh} घरपरिवार अर्थात् {second_pct} प्रतिशत {second_exp[0]}मा र तेस्रोमा {third_hh} घरपरिवार अर्थात् {third_pct} प्रतिशत {third_exp[0]}मा खर्च गरेका छन् ।"""
                )

            # Essential services analysis
            essential_keywords = ["शिक्षा", "स्वास्थ्य", "घरेलु"]
            essential_exp = []
            for expense in major_expenses:
                if any(keyword in expense[0] for keyword in essential_keywords):
                    essential_exp.append(expense)

            if essential_exp:
                essential_total = sum(exp[1] for exp in essential_exp)
                essential_pct = (
                    (essential_total / total_households * 100)
                    if total_households > 0
                    else 0
                )
                content.append(
                    f"""आधारभूत आवश्यकताहरूमा {format_nepali_number(essential_total)} घरपरिवार ({format_nepali_percentage(essential_pct)} प्रतिशत) ले शिक्षा, स्वास्थ्य र घरेलु प्रयोगमा रेमिटेन्स रकम खर्च गरेका छन् जसले मानव पूँजी विकासमा रेमिटेन्सको महत्वपूर्ण योगदान रहेको देखाउँछ ।"""
                )

            # Investment and asset building
            investment_keywords = ["घर निर्माण", "जमिन", "व्यापार", "बचत"]
            investment_exp = []
            for expense in major_expenses:
                if any(keyword in expense[0] for keyword in investment_keywords):
                    investment_exp.append(expense)

            if investment_exp:
                investment_total = sum(exp[1] for exp in investment_exp)
                investment_pct = (
                    (investment_total / total_households * 100)
                    if total_households > 0
                    else 0
                )
                content.append(
                    f"""पूंजी निर्माण र लगानीमा {format_nepali_number(investment_total)} घरपरिवार ({format_nepali_percentage(investment_pct)} प्रतिशत) ले घर निर्माण, जमिन खरिद, व्यापार र बचतमा रेमिटेन्स रकम खर्च गरेका छन् जसले दीर्घकालीन आर्थिक सुरक्षाको चेतना देखाउँछ ।"""
                )

            # Financial obligations
            debt_exp = next((exp for exp in major_expenses if "ऋण" in exp[0]), None)
            if debt_exp:
                debt_hh = format_nepali_number(debt_exp[1])
                debt_pct = format_nepali_percentage(debt_exp[2])
                content.append(
                    f"""वित्तीय दायित्वमा {debt_hh} घरपरिवार ({debt_pct} प्रतिशत) ले ऋण भुक्तानीमा रेमिटेन्स रकम प्रयोग गरेका छन् जसले पारिवारिक आर्थिक बोझको अवस्थालाई संकेत गर्छ ।"""
                )

            # Social and cultural expenses
            social_exp = next(
                (
                    exp
                    for exp in major_expenses
                    if "चाडपर्व" in exp[0] or "गहना" in exp[0]
                ),
                None,
            )
            if social_exp:
                social_hh = format_nepali_number(social_exp[1])
                social_pct = format_nepali_percentage(social_exp[2])
                content.append(
                    f"""सामाजिक र सांस्कृतिक खर्चमा {social_hh} घरपरिवार ({social_pct} प्रतिशत) ले चाडपर्व र गहना गरगहनामा रेमिटेन्स रकम प्रयोग गरेका छन् जसले सामाजिक मूल्य मान्यता र संस्कृति संरक्षणको प्रवृत्ति देखाउँछ ।"""
                )

            # Economic impact and development strategy
            content.append(
                """रेमिटेन्स रकमको उपयोगले गाउँपालिकाको आर्थिक विकासमा महत्वपूर्ण भूमिका खेलेको छ । शिक्षा र स्वास्थ्यमा लगानीले मानव संसाधन विकासमा योगदान पुर्याएको छ भने घर निर्माण र व्यापारिक लगानीले स्थानीय अर्थतन्त्रलाई गतिशील बनाएको छ ।"""
            )

            # Policy implications
            content.append(
                """गाउँपालिकाको आर्थिक नीति निर्माणमा यी रेमिटेन्स खर्चका तथ्याङ्कहरूले महत्वपूर्ण भूमिका खेल्छन् । आधारभूत सेवाहरूमा बढी खर्च भएकोले यी क्षेत्रहरूको गुणस्तर र पहुँचमा सुधार गर्नुपर्ने देखिन्छ ।"""
            )

            # Productivity enhancement recommendations
            content.append(
                """भविष्यमा रेमिटेन्स रकमको अझ उत्पादनशील उपयोगका लागि कृषि व्यावसायीकरण, साना उद्योग स्थापना र सीप विकास कार्यक्रमहरूमा लगानी प्रोत्साहन गर्ने नीति अपनाइनुपर्छ ।"""
            )

            # Financial literacy and planning
            content.append(
                """आर्थिक साक्षरता र वित्तीय योजना बनाउने क्षमता विकास गरी रेमिटेन्स रकमको दीर्घकालीन र उत्पादनशील उपयोगमा वृद्धि गर्न सकिन्छ । सहकारी संस्थाहरूको भूमिकालाई बलियो बनाएर बचत र लगानी प्रवर्द्धन गर्नुपर्छ ।"""
            )

            # Future prospects
            content.append(
                """वडागत रूपमा रेमिटेन्स खर्चको ढाँचामा भिन्नता रहेको देखिन्छ । यो विविधताले गाउँपालिकामा आर्थिक गतिविधिको संतुलित विकासमा योगदान पुर्याएको छ र स्थानीय अर्थतन्त्रको लचकदारतालाई बढाएको छ ।"""
            )

            return " ".join(content)
