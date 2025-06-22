"""
Disability Cause Demographics Processor

Handles disability cause demographic data processing, chart generation, and report formatting.
"""

import subprocess
from pathlib import Path
from .base import BaseDemographicsProcessor, BaseReportFormatter
from ..models import WardWiseDisabilityCause, DisabilityCauseChoice
from ..utils.svg_chart_generator import DEFAULT_COLORS
from apps.reports.utils.nepali_numbers import (
    format_nepali_number,
    format_nepali_percentage,
)
from apps.chart_management.processors import SimpleChartProcessor


class DisabilityCauseProcessor(BaseDemographicsProcessor, SimpleChartProcessor):
    """Processor for disability cause demographics"""

    def __init__(self):
        super().__init__()
        SimpleChartProcessor.__init__(self)

        # Ensure we use the same directory as the chart service
        from django.conf import settings

        if hasattr(settings, "STATICFILES_DIRS") and settings.STATICFILES_DIRS:
            # Use same directory as chart management service
            self.static_charts_dir = (
                Path(settings.STATICFILES_DIRS[0]) / "images" / "charts"
            )
        else:
            # Fallback to STATIC_ROOT
            self.static_charts_dir = Path(settings.STATIC_ROOT) / "images" / "charts"

        self.static_charts_dir.mkdir(parents=True, exist_ok=True)

        # Customize chart dimensions for disability cause
        self.pie_chart_width = 900
        self.pie_chart_height = 450
        self.bar_chart_width = 1000
        self.bar_chart_height = 600
        self.chart_radius = 130
        # Set disability cause-specific colors
        self.chart_generator.colors = {
            "CONGENITAL": "#FF6B6B",  # Red
            "ACCIDENT": "#4ECDC4",  # Teal
            "DISEASE": "#45B7D1",  # Blue
            "MALNUTRITION": "#96CEB4",  # Green
            "CONFLICT": "#FFEAA7",  # Yellow
            "OTHER": "#DDA0DD",  # Plum
        }

    def get_chart_key(self):
        """Return unique chart key for this processor"""
        return "demographics_disability_cause"

    def get_section_title(self):
        return "अपाङ्गताका आधारमा जनसंख्याको विवरण"

    def get_section_number(self):
        return "३.१०"

    def get_data(self):
        """Get disability cause population data - both municipality-wide and ward-wise"""
        # Municipality-wide summary
        disability_data = {}

        # Initialize all disability causes
        disability_types = {
            "CONGENITAL": "जन्मजात",
            "ACCIDENT": "दुर्घटना",
            "DISEASE": "रोगको कारण",
            "MALNUTRITION": "कुपोषण",
            "CONFLICT": "द्वन्द्वको कारण",
            "OTHER": "अन्य",
        }

        for dis_code, dis_name in disability_types.items():
            disability_data[dis_code] = {
                "population": 0,
                "percentage": 0.0,
                "name_nepali": dis_name,
            }

        # Ward-wise data for bar chart and detailed table
        ward_data = {}
        for ward_num in range(1, 8):  # Wards 1-7 based on sample data
            ward_data[ward_num] = {
                "ward_name": f"वडा नं. {ward_num}",
                "demographics": {},
            }
            # Initialize disability causes for each ward
            for dis_code, dis_name in disability_types.items():
                ward_data[ward_num]["demographics"][dis_code] = {
                    "population": 0,
                    "name_nepali": dis_name,
                }

        # Get actual data from database
        total_population = 0
        try:
            for disability_obj in WardWiseDisabilityCause.objects.all():
                disability = disability_obj.disability_cause
                ward_num = disability_obj.ward_number
                population = disability_obj.population

                # Add to municipality-wide totals
                if disability in disability_data:
                    disability_data[disability]["population"] += population
                    total_population += population

                # Add to ward-wise data
                if (
                    ward_num in ward_data
                    and disability in ward_data[ward_num]["demographics"]
                ):
                    ward_data[ward_num]["demographics"][disability][
                        "population"
                    ] = population
        except Exception as e:
            print(f"Error fetching disability cause data: {e}")
            # Return empty data structure if database error
            return {
                "municipality_data": disability_data,
                "ward_data": ward_data,
                "total_population": 0,
            }

        # Calculate percentages for municipality-wide data
        if total_population > 0:
            for disability, data in disability_data.items():
                data["percentage"] = (data["population"] / total_population) * 100

        # Calculate ward totals and percentages
        for ward_num, ward_info in ward_data.items():
            ward_total = sum(
                demo["population"] for demo in ward_info["demographics"].values()
            )
            ward_info["total_population"] = ward_total

            # Calculate percentages within each ward
            if ward_total > 0:
                for disability, demo in ward_info["demographics"].items():
                    demo["percentage"] = (
                        (demo["population"] / ward_total) * 100 if ward_total > 0 else 0
                    )

        return {
            "municipality_data": disability_data,
            "ward_data": ward_data,
            "total_population": total_population,
        }

    def generate_report_content(self, data):
        """Generate disability cause-specific report content"""
        formatter = self.DisabilityCauseReportFormatter()
        return formatter.generate_formal_report(
            data["municipality_data"], data["ward_data"], data["total_population"]
        )

    def generate_chart_svg(self, data, chart_type="pie"):
        """Generate disability cause chart SVG using SVGChartGenerator"""
        if chart_type == "pie":
            return self.chart_generator.generate_pie_chart_svg(
                data["municipality_data"],
                include_title=False,
                title_nepali="अपाङ्गताका कारण अनुसार जनसंख्या वितरण",
                title_english="Population Distribution by Disability Cause",
            )
        elif chart_type == "bar":
            return self.chart_generator.generate_bar_chart_svg(
                data["ward_data"],
                include_title=False,
                title_nepali="वडा अनुसार अपाङ्गताका कारण अनुसार जनसंख्या वितरण",
                title_english="Disability Cause Distribution by Ward",
            )
        return None

    def generate_and_track_charts(self, data):
        """Generate charts only if they don't exist and track them using simplified chart management"""
        charts = {}

        # Ensure static charts directory exists
        self.static_charts_dir.mkdir(parents=True, exist_ok=True)

        # Check and generate pie chart only if needed
        if self.needs_generation("pie"):
            print(f"🔄 Generating disability cause pie chart...")
            success, png_path, svg_path = self.chart_generator.generate_chart_image(
                demographic_data=data.get("municipality_data", {}),
                output_name="disability_cause_pie_chart",
                static_dir=str(self.static_charts_dir),
                chart_type="pie",
                include_title=False,
            )

            if success and png_path:
                charts["pie_chart_png"] = f"images/charts/{Path(png_path).name}"
                charts["pie_chart_url"] = f"images/charts/{Path(png_path).name}"
                self.mark_generated("pie")
                print(
                    f"✅ Disability cause pie chart generated successfully: {png_path}"
                )
            elif svg_path:
                charts["pie_chart_svg"] = f"images/charts/{Path(svg_path).name}"
                charts["pie_chart_url"] = f"images/charts/{Path(svg_path).name}"
                self.mark_generated("pie")
                print(f"✅ Disability cause pie chart SVG generated: {svg_path}")
        else:
            # Chart already exists, get the URL
            charts["pie_chart_url"] = f"images/charts/disability_cause_pie_chart.png"
            print(f"✅ Disability cause pie chart already exists")

        # Check and generate bar chart only if needed
        if self.needs_generation("bar"):
            print(f"🔄 Generating disability cause bar chart...")
            success, png_path, svg_path = self.chart_generator.generate_chart_image(
                demographic_data=data.get("ward_data", {}),
                output_name="disability_cause_bar_chart",
                static_dir=str(self.static_charts_dir),
                chart_type="bar",
                include_title=False,
            )

            if success and png_path:
                charts["bar_chart_png"] = f"images/charts/{Path(png_path).name}"
                charts["bar_chart_url"] = f"images/charts/{Path(png_path).name}"
                self.mark_generated("bar")
                print(
                    f"✅ Disability cause bar chart generated successfully: {png_path}"
                )
            elif svg_path:
                charts["bar_chart_svg"] = f"images/charts/{Path(svg_path).name}"
                charts["bar_chart_url"] = f"images/charts/{Path(svg_path).name}"
                self.mark_generated("bar")
                print(f"✅ Disability cause bar chart SVG generated: {svg_path}")
        else:
            # Chart already exists, get the URL
            charts["bar_chart_url"] = f"images/charts/disability_cause_bar_chart.png"
            print(f"✅ Disability cause bar chart already exists")

        return charts

    def generate_and_save_charts(self, data):
        """Legacy method - calls new chart management method"""
        return self.generate_and_track_charts(data)

    def process_for_pdf(self):
        """Process disability cause data for PDF generation with simplified chart management"""
        # Get raw data
        data = self.get_data()

        # Generate report content
        report_content = self.generate_report_content(data)

        # Generate charts only if needed
        charts = self.generate_and_track_charts(data)

        # Calculate total population
        total_population = data.get("total_population", 0)

        return {
            "data": data,
            "report_content": report_content,
            "charts": charts,
            "total_population": total_population,
            "section_title": self.get_section_title(),
            "section_number": self.get_section_number(),
        }

    def process_for_template(self):
        """Process disability cause data for template rendering"""
        # Get raw data
        data = self.get_data()

        # Generate report content
        report_content = self.generate_report_content(data)

        # Generate charts
        charts = self.generate_and_track_charts(data)

        return {
            "municipality_data": data.get("municipality_data", {}),
            "ward_data": data.get("ward_data", {}),
            "total_population": data.get("total_population", 0),
            "coherent_analysis": report_content,
            "charts": charts,
        }

    class DisabilityCauseReportFormatter(BaseReportFormatter):
        """Disability cause-specific report formatter"""

        def generate_formal_report(self, disability_data, ward_data, total_population):
            """Generate disability cause formal report content"""

            # Find major disability causes
            major_disabilities = []
            for disability_type, data in disability_data.items():
                if data["population"] > 0:
                    major_disabilities.append(
                        (data["name_nepali"], data["population"], data["percentage"])
                    )

            major_disabilities.sort(key=lambda x: x[1], reverse=True)

            # Build comprehensive analysis
            content = []

            # Introduction
            nepali_total = format_nepali_number(total_population)
            content.append(
                f"""शरीरका अङ्गहरू र शारीरिक प्रणालीमा भएको समस्याका कारण भौतिक, सामाजिक, सांस्कृतिक वातावरणका साथै सञ्चार समेतबाट सिर्जना भएको अवरोध समेतले दैनिक क्रियाकलाप सामान्य रूपमा सञ्चालन गर्न एवं सामाजिक जीवनमा पूर्ण सहभागी हुन कठिनाई हुने अवस्थालाई अपाङ्गता भनिन्छ । विशेषगरी व्यक्तिहरूमा अपाङ्गता हुने कारण जन्मजात, दुर्घटना, रोगको कारण, द्वन्द्वको कारण, कुपोषण आदि देखिएका छन् । जसलाई घटाउन प्रतिरोधात्मक र उपचारात्मक दुवै कार्यहरू गरिनुपर्दछ । गाउँपालिकाले अपाङ्गता सञ्जाल गठन निर्देशिका २०७८, अनुसार अपाङ्गता भएका व्यक्तिको परिचय पत्र वितरण कार्यविधि तयार गरी कार्यान्वयनमा ल्याएको छ ।"""
            )

            # Top disability causes analysis
            if len(major_disabilities) >= 3:
                top_three = major_disabilities[:3]
                first_dis = top_three[0]
                second_dis = top_three[1]
                third_dis = top_three[2]

                first_pop = format_nepali_number(first_dis[1])
                first_pct = format_nepali_percentage(first_dis[2])
                second_pop = format_nepali_number(second_dis[1])
                second_pct = format_nepali_percentage(second_dis[2])
                third_pop = format_nepali_number(third_dis[1])
                third_pct = format_nepali_percentage(third_dis[2])

                content.append(
                    f"""घरधुरी तथ्याङ्क संकलन, २०८१ को तथ्याङ्क अनुसार गाउँपालिकामा रहेको कूल {nepali_total} जनसंख्या मध्ये सबैभन्दा बढी {first_pop} जना अर्थात {first_pct} प्रतिशत {first_dis[0]} अपाङ्गता रहेका छन् भने दोस्रोमा {second_pop} जना अर्थात {second_pct} प्रतिशत {second_dis[0]} अपाङ्गता र तेस्रोमा {third_pop} जना अर्थात {third_pct} प्रतिशत {third_dis[0]} अपाङ्गता रहेका छन् ।"""
                )

            # Congenital disability analysis
            congenital_data = next(
                (dis for dis in major_disabilities if "जन्मजात" in dis[0]), None
            )
            if congenital_data:
                congenital_pop = format_nepali_number(congenital_data[1])
                congenital_pct = format_nepali_percentage(congenital_data[2])
                content.append(
                    f"""जन्मजात अपाङ्गतामा {congenital_pop} जना ({congenital_pct} प्रतिशत) रहेको देखिन्छ जसले गर्भावस्थाको स्वास्थ्य सेवा र जन्मपूर्व देखभालको महत्वपूर्णता देखाउँछ ।"""
                )

            # Accident-related disability
            accident_data = next(
                (dis for dis in major_disabilities if "दुर्घटना" in dis[0]), None
            )
            if accident_data:
                accident_pop = format_nepali_number(accident_data[1])
                accident_pct = format_nepali_percentage(accident_data[2])
                content.append(
                    f"""दुर्घटना अपाङ्गतामा {accident_pop} जना ({accident_pct} प्रतिशत) रहेका छन् जसले सुरक्षा जागरूकता र दुर्घटना निवारणका कार्यक्रमहरूको आवश्यकता देखाउँछ ।"""
                )

            # Disease-related disability
            disease_data = next(
                (dis for dis in major_disabilities if "रोगको कारण" in dis[0]), None
            )
            if disease_data:
                disease_pop = format_nepali_number(disease_data[1])
                disease_pct = format_nepali_percentage(disease_data[2])
                content.append(
                    f"""रोगको कारण अपाङ्गतामा {disease_pop} जना ({disease_pct} प्रतिशत) रहेका छन् जसले स्वास्थ्य सेवा र रोग निवारणका कार्यक्रमहरूको महत्व देखाउँछ ।"""
                )

            # Malnutrition-related disability
            malnutrition_data = next(
                (dis for dis in major_disabilities if "कुपोषण" in dis[0]), None
            )
            if malnutrition_data:
                malnutrition_pop = format_nepali_number(malnutrition_data[1])
                malnutrition_pct = format_nepali_percentage(malnutrition_data[2])
                content.append(
                    f"""कुपोषणका कारण अपाङ्गतामा {malnutrition_pop} जना ({malnutrition_pct} प्रतिशत) रहेका छन् जसले पोषण कार्यक्रम र खानपान जागरूकताको आवश्यकता देखाउँछ ।"""
                )

            # Conflict-related disability
            conflict_data = next(
                (dis for dis in major_disabilities if "द्वन्द्वको कारण" in dis[0]), None
            )
            if conflict_data:
                conflict_pop = format_nepali_number(conflict_data[1])
                conflict_pct = format_nepali_percentage(conflict_data[2])
                content.append(
                    f"""द्वन्द्वको कारण अपाङ्गतामा {conflict_pop} जना ({conflict_pct} प्रतिशत) रहेका छन् जसले शान्ति र सुरक्षाको महत्व देखाउँछ ।"""
                )

            # Other causes
            other_data = next(
                (dis for dis in major_disabilities if "अन्य" in dis[0]), None
            )
            if other_data:
                other_pop = format_nepali_number(other_data[1])
                other_pct = format_nepali_percentage(other_data[2])
                content.append(
                    f"""अन्य कारणहरूबाट अपाङ्गतामा {other_pop} जना ({other_pct} प्रतिशत) रहेका छन् ।"""
                )

            # Prevention and intervention strategies
            content.append(
                """अपाङ्गता निवारण र हस्तक्षेपका लागि गाउँपालिकाले विभिन्न कार्यक्रमहरू सञ्चालन गरेको छ । जन्मपूर्व देखभाल, सुरक्षित जन्म, बाल स्वास्थ्य कार्यक्रम, रोग निवारण र उपचार, सुरक्षा जागरूकता र पोषण कार्यक्रमहरू मार्फत अपाङ्गता निवारण गर्ने प्रयास गरिएको छ ।"""
            )

            # Social inclusion and support
            content.append(
                """अपाङ्गता भएका व्यक्तिहरूको सामाजिक समावेशीकरण र सहयोगका लागि विशेष शिक्षा, व्यावसायिक तालिम, रोजगारीको अवसर र सामाजिक सुरक्षा कार्यक्रमहरू सञ्चालन गरिएको छ । अपाङ्गता भएका व्यक्तिहरूलाई समान अधिकार र अवसर प्रदान गर्ने नीति अपनाइएको छ ।"""
            )

            # Infrastructure and accessibility
            content.append(
                """अपाङ्गता भएका व्यक्तिहरूको लागि सुलभ पूर्वाधार निर्माण र सेवा प्रदान गर्ने कार्य गरिएको छ । सडक, भवन, शैक्षिक संस्था र स्वास्थ्य सेवा केन्द्रहरूमा अपाङ्गता मैत्री सुविधाहरू थप गर्ने योजना रहेको छ ।"""
            )

            # Ward-wise analysis
            content.append(
                """वडागत विश्लेषणले अपाङ्गताका कारणहरूको भौगोलिक विविधता देखाउँछ । कुनै वडामा दुर्घटना अपाङ्गता बढी भने कुनैमा जन्मजात वा रोगको कारण अपाङ्गता बढी रहेको छ । यसले स्थानीय स्तरमा विशेष कार्यक्रमहरूको आवश्यकता देखाउँछ ।"""
            )

            # Future prospects and challenges
            content.append(
                """भविष्यमा अपाङ्गता निवारण र पुनर्स्थापनका कार्यक्रमहरू थप विस्तार गर्ने योजना रहेको छ । अपाङ्गता भएका व्यक्तिहरूको सशक्तिकरण र स्वावलम्बनका कार्यक्रमहरू सञ्चालन गरी तिनलाई समाजको मुख्य धारामा ल्याउने प्रयास गरिनेछ ।"""
            )

            # Policy and legal framework
            content.append(
                """अपाङ्गता भएका व्यक्तिहरूको अधिकार र सुरक्षाको लागि कानूनी ढाँचा र नीतिहरू कार्यान्वयन गरिएको छ । अपाङ्गता सञ्जाल गठन निर्देशिका २०७८ अनुसार अपाङ्गता भएका व्यक्तिको परिचय पत्र वितरण कार्यविधि तयार गरी कार्यान्वयनमा ल्याएको छ ।"""
            )

            return " ".join(content)
