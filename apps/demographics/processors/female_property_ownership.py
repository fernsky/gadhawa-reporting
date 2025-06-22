"""
Female Property Ownership Demographics Processor

Handles female property ownership demographic data processing, chart generation, and report formatting.
"""

import subprocess
from pathlib import Path
from .base import BaseDemographicsProcessor, BaseReportFormatter
from ..models import WardWiseFemalePropertyOwnership, PropertyTypeChoice
from ..utils.svg_chart_generator import DEFAULT_COLORS
from apps.reports.utils.nepali_numbers import (
    format_nepali_number,
    format_nepali_percentage,
)
from apps.chart_management.processors import SimpleChartProcessor


class FemalePropertyOwnershipProcessor(BaseDemographicsProcessor, SimpleChartProcessor):
    """Processor for female property ownership demographics"""

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

        # Customize chart dimensions for female property ownership
        self.pie_chart_width = 900
        self.pie_chart_height = 450
        self.bar_chart_width = 1000
        self.bar_chart_height = 600
        self.chart_radius = 130

        # Set female property ownership-specific colors
        self.chart_generator.colors = {
            "HOUSE_ONLY": "#FF6B6B",  # Red
            "LAND_ONLY": "#4ECDC4",  # Teal
            "BOTH_HOUSE_AND_LAND": "#45B7D1",  # Blue
            "NEITHER_HOUSE_NOR_LAND": "#96CEB4",  # Green
        }

    def get_chart_key(self):
        """Return unique chart key for this processor"""
        return "demographics_female_property_ownership"

    def get_section_title(self):
        return "महिला सम्पत्ति स्वामित्व सम्बन्धी विवरण"

    def get_section_number(self):
        return "३.१३"

    def get_data(self):
        """Get female property ownership data - both municipality-wide and ward-wise"""
        # Municipality-wide summary
        property_data = {}
        municipality_totals = {}
        property_type_names = {}
        municipality_percentages = {}

        # Initialize all property types
        property_types = {
            "HOUSE_ONLY": "घर मात्र",
            "LAND_ONLY": "जग्गा मात्र",
            "BOTH_HOUSE_AND_LAND": "घर र जग्गा दुवै",
            "NEITHER_HOUSE_NOR_LAND": "घर र जग्गा कुनै पनि छैन",
        }

        for prop_code, prop_name in property_types.items():
            property_data[prop_code] = {
                "population": 0,
                "percentage": 0.0,
                "name_nepali": prop_name,
            }
            municipality_totals[prop_code] = 0
            property_type_names[prop_code] = prop_name
            municipality_percentages[prop_code] = 0.0

        # Initialize ward data dictionary (will be populated with actual data)
        ward_data = {}

        # Get actual data from database
        total_population = 0
        for property_obj in WardWiseFemalePropertyOwnership.objects.all():
            property_type = property_obj.property_type
            ward_num = property_obj.ward_number
            population = property_obj.population

            # Add to municipality-wide totals
            if property_type in property_data:
                property_data[property_type]["population"] += population
                municipality_totals[property_type] += population
                total_population += population

            # Initialize ward data if not exists
            if ward_num not in ward_data:
                ward_data[ward_num] = {
                    "ward_name": f"वडा नं. {ward_num}",
                    "demographics": {},
                    "property_types": {},
                }
                # Initialize property types for this ward
                for prop_code, prop_name in property_types.items():
                    ward_data[ward_num]["demographics"][prop_code] = {
                        "population": 0,
                        "name_nepali": prop_name,
                    }
                    ward_data[ward_num]["property_types"][prop_code] = {
                        "population": 0,
                    }

            # Add to ward-wise data
            if property_type in ward_data[ward_num]["demographics"]:
                ward_data[ward_num]["demographics"][property_type][
                    "population"
                ] = population
                ward_data[ward_num]["property_types"][property_type][
                    "population"
                ] = population

        # Calculate percentages for municipality-wide data
        if total_population > 0:
            for property_type, data in property_data.items():
                data["percentage"] = (data["population"] / total_population) * 100
                municipality_percentages[property_type] = (
                    data["population"] / total_population
                ) * 100

        # Calculate ward totals and percentages
        for ward_num, ward_info in ward_data.items():
            ward_total = sum(
                demo["population"] for demo in ward_info["demographics"].values()
            )
            ward_info["total_population"] = ward_total

            # Calculate percentages within each ward
            if ward_total > 0:
                for property_type, demo in ward_info["demographics"].items():
                    demo["percentage"] = (
                        (demo["population"] / ward_total) * 100 if ward_total > 0 else 0
                    )

        return {
            "municipality_data": property_data,
            "municipality_totals": municipality_totals,
            "property_type_names": property_type_names,
            "municipality_percentages": municipality_percentages,
            "ward_data": ward_data,
            "total_population": total_population,
        }

    def generate_report_content(self, data):
        """Generate female property ownership-specific report content"""
        formatter = self.FemalePropertyOwnershipReportFormatter()
        return formatter.generate_formal_report(
            data["municipality_data"], data["ward_data"], data["total_population"]
        )

    def generate_chart_svg(self, data, chart_type="pie"):
        """Generate female property ownership chart SVG using SVGChartGenerator"""
        if chart_type == "pie":
            return self.chart_generator.generate_pie_chart_svg(
                data["municipality_data"],
                include_title=False,
                title_nepali="महिला सम्पत्ति स्वामित्व - सम्पत्तिको प्रकार अनुसार",
                title_english="Female Property Ownership by Type",
            )
        elif chart_type == "bar":
            return self.chart_generator.generate_bar_chart_svg(
                data["ward_data"],
                include_title=False,
                title_nepali="वडागत महिला सम्पत्ति स्वामित्व तुलना",
                title_english="Female Property Ownership by Ward",
            )
        return None

    def generate_and_save_charts(self, data):
        """Generate and save both pie and bar charts for female property ownership data only if they don't exist"""
        charts_info = {}

        try:
            # Check if pie chart already exists
            pie_png_path = (
                self.static_charts_dir / "female_property_ownership_pie_chart.png"
            )
            pie_svg_path = (
                self.static_charts_dir / "female_property_ownership_pie_chart.svg"
            )

            if not pie_png_path.exists():
                # Generate pie chart for municipality-wide data
                pie_svg = self.generate_chart_svg(data, chart_type="pie")
                if pie_svg:
                    with open(pie_svg_path, "w", encoding="utf-8") as f:
                        f.write(pie_svg)
                    charts_info["pie_chart_svg"] = (
                        f"images/charts/female_property_ownership_pie_chart.svg"
                    )

                    # Try to convert to PNG using subprocess
                    try:
                        subprocess.run(
                            [
                                "inkscape",
                                "--export-filename",
                                str(pie_png_path),
                                "--export-dpi=600",  # High quality for PDF
                                str(pie_svg_path),
                            ],
                            check=True,
                            timeout=30,
                        )
                        if pie_png_path.exists():
                            charts_info["pie_chart_png"] = (
                                f"images/charts/female_property_ownership_pie_chart.png"
                            )
                    except:
                        pass  # Use SVG fallback
            else:
                # PNG exists, just add paths to charts_info
                charts_info["pie_chart_png"] = (
                    f"images/charts/female_property_ownership_pie_chart.png"
                )
                if pie_svg_path.exists():
                    charts_info["pie_chart_svg"] = (
                        f"images/charts/female_property_ownership_pie_chart.svg"
                    )

            # Check if bar chart already exists
            bar_png_path = (
                self.static_charts_dir / "female_property_ownership_bar_chart.png"
            )
            bar_svg_path = (
                self.static_charts_dir / "female_property_ownership_bar_chart.svg"
            )

            if not bar_png_path.exists():
                # Generate bar chart for ward-wise data
                bar_svg = self.generate_chart_svg(data, chart_type="bar")
                if bar_svg:
                    with open(bar_svg_path, "w", encoding="utf-8") as f:
                        f.write(bar_svg)
                    charts_info["bar_chart_svg"] = (
                        f"images/charts/female_property_ownership_bar_chart.svg"
                    )

                    # Try to convert to PNG using subprocess
                    try:
                        subprocess.run(
                            [
                                "inkscape",
                                "--export-filename",
                                str(bar_png_path),
                                "--export-dpi=600",  # High quality for PDF
                                str(bar_svg_path),
                            ],
                            check=True,
                            timeout=30,
                        )
                        if bar_png_path.exists():
                            charts_info["bar_chart_png"] = (
                                f"images/charts/female_property_ownership_bar_chart.png"
                            )
                    except:
                        pass  # Use SVG fallback
            else:
                # PNG exists, just add paths to charts_info
                charts_info["bar_chart_png"] = (
                    f"images/charts/female_property_ownership_bar_chart.png"
                )
                if bar_svg_path.exists():
                    charts_info["bar_chart_svg"] = (
                        f"images/charts/female_property_ownership_bar_chart.svg"
                    )

        except Exception as e:
            print(f"Error generating female property ownership charts: {e}")

        return charts_info

    def generate_and_track_charts(self, data):
        """Generate charts only if they don't exist and track them using simplified chart management"""
        charts = {}

        # Ensure static charts directory exists
        self.static_charts_dir.mkdir(parents=True, exist_ok=True)

        # Check and generate pie chart only if needed
        if self.needs_generation("pie"):
            print(f"🔄 Generating female property ownership pie chart...")
            success, png_path, svg_path = self.chart_generator.generate_chart_image(
                demographic_data=data.get("municipality_data", {}),
                output_name="female_property_ownership_pie_chart",
                static_dir=str(self.static_charts_dir),
                chart_type="pie",
                include_title=False,
            )

            if success and png_path:
                charts["pie_chart_png"] = f"images/charts/{Path(png_path).name}"
                charts["pie_chart_url"] = f"images/charts/{Path(png_path).name}"
                self.mark_generated("pie")
                print(
                    f"✅ Female property ownership pie chart generated successfully: {png_path}"
                )
            elif svg_path:
                charts["pie_chart_svg"] = f"images/charts/{Path(svg_path).name}"
                charts["pie_chart_url"] = f"images/charts/{Path(svg_path).name}"
                self.mark_generated("pie")
                print(
                    f"✅ Female property ownership pie chart SVG generated: {svg_path}"
                )
        else:
            # Chart already exists, get the URL
            charts["pie_chart_url"] = (
                f"images/charts/female_property_ownership_pie_chart.png"
            )
            print(f"✅ Female property ownership pie chart already exists")

        # Check and generate bar chart only if needed
        if self.needs_generation("bar"):
            print(f"🔄 Generating female property ownership bar chart...")
            success, png_path, svg_path = self.chart_generator.generate_chart_image(
                demographic_data=data.get("ward_data", {}),
                output_name="female_property_ownership_bar_chart",
                static_dir=str(self.static_charts_dir),
                chart_type="bar",
                include_title=False,
            )

            if success and png_path:
                charts["bar_chart_png"] = f"images/charts/{Path(png_path).name}"
                charts["bar_chart_url"] = f"images/charts/{Path(png_path).name}"
                self.mark_generated("bar")
                print(
                    f"✅ Female property ownership bar chart generated successfully: {png_path}"
                )
            elif svg_path:
                charts["bar_chart_svg"] = f"images/charts/{Path(svg_path).name}"
                charts["bar_chart_url"] = f"images/charts/{Path(svg_path).name}"
                self.mark_generated("bar")
                print(
                    f"✅ Female property ownership bar chart SVG generated: {svg_path}"
                )
        else:
            # Chart already exists, get the URL
            charts["bar_chart_url"] = (
                f"images/charts/female_property_ownership_bar_chart.png"
            )
            print(f"✅ Female property ownership bar chart already exists")

        return charts

    def process_for_pdf(self):
        """Process female property ownership data for PDF generation with simplified chart management"""
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

    class FemalePropertyOwnershipReportFormatter(BaseReportFormatter):
        """Female property ownership-specific report formatter"""

        def generate_formal_report(self, property_data, ward_data, total_population):
            """Generate female property ownership formal report content"""

            # Find major property ownership types
            major_property_types = []
            for property_type, data in property_data.items():
                if data["population"] > 0:
                    major_property_types.append(
                        (data["name_nepali"], data["population"], data["percentage"])
                    )

            major_property_types.sort(key=lambda x: x[1], reverse=True)

            # Build comprehensive analysis
            content = []

            # Introduction
            nepali_total = format_nepali_number(total_population)
            content.append(
                f"""{self.municipality_name}मा कुल {nepali_total} महिलाको सम्पत्ति स्वामित्वको विश्लेषणले समाजमा महिलाको आर्थिक स्थिति र स्वतन्त्रताको महत्वपूर्ण तस्विर प्रस्तुत गर्दछ।"""
            )

            # Top property ownership types analysis
            if len(major_property_types) >= 3:
                top_three = major_property_types[:3]
                first_type = top_three[0]
                second_type = top_three[1]
                third_type = top_three[2]

                first_pop = format_nepali_number(first_type[1])
                first_pct = format_nepali_percentage(first_type[2])
                second_pop = format_nepali_number(second_type[1])
                second_pct = format_nepali_percentage(second_type[2])
                third_pop = format_nepali_number(third_type[1])
                third_pct = format_nepali_percentage(third_type[2])

                content.append(
                    f"""सबैभन्दा धेरै महिला ({first_pct} प्रतिशत) {first_pop} जना {first_type[0].lower()}को स्थितिमा छन् भने दोस्रोमा {second_pop} जना ({second_pct} प्रतिशत) {second_type[0].lower()}को स्थितिमा र तेस्रोमा {third_pop} जना ({third_pct} प्रतिशत) {third_type[0].lower()}को स्थितिमा छन्।"""
                )

            # Property ownership rate analysis
            property_owners = (
                property_data.get("HOUSE_ONLY", {}).get("population", 0)
                + property_data.get("LAND_ONLY", {}).get("population", 0)
                + property_data.get("BOTH_HOUSE_AND_LAND", {}).get("population", 0)
            )
            property_ownership_rate = (
                (property_owners / total_population * 100)
                if total_population > 0
                else 0
            )
            nepali_ownership_rate = format_nepali_percentage(property_ownership_rate)
            nepali_property_owners = format_nepali_number(property_owners)

            content.append(
                f"""सम्पत्ति स्वामित्वको दृष्टिकोणबाट हेर्दा, कुल महिलाको {nepali_ownership_rate} प्रतिशत ({nepali_property_owners} जना) ले कुनै न कुनै रूपमा सम्पत्ति स्वामित्व राख्छन्। यो आंकडाले महिला सशक्तिकरणको लागि सम्पत्ति स्वामित्वको महत्व देखाउँछ।"""
            )

            # No property ownership analysis
            no_property = property_data.get("NEITHER_HOUSE_NOR_LAND", {}).get(
                "population", 0
            )
            no_property_rate = (
                (no_property / total_population * 100) if total_population > 0 else 0
            )
            nepali_no_property = format_nepali_number(no_property)
            nepali_no_property_rate = format_nepali_percentage(no_property_rate)

            content.append(
                f"""सबैभन्दा धेरै महिला ({nepali_no_property_rate} प्रतिशत) {nepali_no_property} जना ले घर र जग्गा कुनै पनि नराख्ने हुनाले समाजमा महिलाको आर्थिक निर्भरताको गम्भीर समस्या देखिन्छ।"""
            )

            # Both house and land ownership analysis
            both_property = property_data.get("BOTH_HOUSE_AND_LAND", {}).get(
                "population", 0
            )
            both_property_rate = (
                (both_property / total_population * 100) if total_population > 0 else 0
            )
            nepali_both_property = format_nepali_number(both_property)
            nepali_both_property_rate = format_nepali_percentage(both_property_rate)

            content.append(
                f"""यसको विपरीत, मात्र {nepali_both_property_rate} प्रतिशत {nepali_both_property} महिलाले घर र जग्गा दुवै स्वामित्व राख्छन्, जसले महिलाको पूर्ण आर्थिक स्वतन्त्रताको चुनौती देखाउँछ।"""
            )

            # Ward-wise analysis
            highest_property_ward = None
            highest_property_rate = 0
            lowest_property_ward = None
            lowest_property_rate = 100

            for ward_num, ward_info in ward_data.items():
                total_ward_pop = ward_info["total_population"]
                ward_property_owners = (
                    ward_info["demographics"].get("HOUSE_ONLY", {}).get("population", 0)
                    + ward_info["demographics"]
                    .get("LAND_ONLY", {})
                    .get("population", 0)
                    + ward_info["demographics"]
                    .get("BOTH_HOUSE_AND_LAND", {})
                    .get("population", 0)
                )

                if total_ward_pop > 0:
                    ward_property_rate = (ward_property_owners / total_ward_pop) * 100

                    if ward_property_rate > highest_property_rate:
                        highest_property_rate = ward_property_rate
                        highest_property_ward = ward_num

                    if ward_property_rate < lowest_property_rate:
                        lowest_property_rate = ward_property_rate
                        lowest_property_ward = ward_num

            if highest_property_ward and lowest_property_ward:
                nepali_highest_rate = format_nepali_percentage(highest_property_rate)
                nepali_lowest_rate = format_nepali_percentage(lowest_property_rate)

                content.append(
                    f"""वडागत विश्लेषणले महिला सम्पत्ति स्वामित्वको भौगोलिक विविधता देखाउँछ। वडा {format_nepali_number(highest_property_ward)} मा सबैभन्दा धेरै महिला ({nepali_highest_rate} प्रतिशत) ले सम्पत्ति स्वामित्व राख्छन्, जसले यस वडाको महिला सशक्तिकरणको सकारात्मक चित्र देखाउँछ।"""
                )

                content.append(
                    f"""यसको विपरीत, वडा {format_nepali_number(lowest_property_ward)} मा मात्र {nepali_lowest_rate} प्रतिशत महिलाले सम्पत्ति स्वामित्व राख्छन्, जसले यस क्षेत्रमा महिला सशक्तिकरणको लागि विशेष ध्यान दिनुपर्ने आवश्यकता देखाउँछ।"""
                )

            # Policy implications
            content.append(
                """यी आंकडाहरूको आधारमा निम्न नीतिगत निहितार्थहरू निकाल्न सकिन्छ: महिला सशक्तिकरण कार्यक्रम, सम्पत्ति स्वामित्व प्रोत्साहन, कानूनी सुधार, शैक्षिक कार्यक्रम र वित्तीय सहायता कार्यक्रमहरूको आवश्यकता देखिन्छ।"""
            )

            # Social and economic implications
            content.append(
                """महिला सम्पत्ति स्वामित्वले महिलालाई आर्थिक स्वतन्त्रता र सामाजिक स्थिति प्रदान गर्दछ। यसको लागि सरकार, स्थानीय निकाय र समाजको संयुक्त प्रयास आवश्यक छ। महिला सशक्तिकरणले नै समाजको समग्र विकास र सामाजिक सद्भाव सुनिश्चित गर्न सकिन्छ।"""
            )

            # Future prospects
            content.append(
                """भविष्यमा महिला सम्पत्ति स्वामित्वलाई प्रोत्साहन दिन कानूनी सुधारहरू, शैक्षिक कार्यक्रमहरू र वित्तीय सहायता कार्यक्रमहरू सञ्चालन गर्ने योजना रहेको छ। यसले महिला सशक्तिकरण र सामाजिक विकासमा महत्वपूर्ण योगदान पुर्याउनेछ।"""
            )

            return " ".join(content)
