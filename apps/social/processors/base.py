"""
Base Social Processor

Common functionality for processing social data across all categories.
"""

from abc import ABC, abstractmethod
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from pathlib import Path
from apps.demographics.utils.svg_chart_generator import SVGChartGenerator


class BaseSocialProcessor(ABC):
    """Base class for all social data processors"""

    def __init__(self):
        # Use proper static directory path
        self.static_charts_dir = Path("static/images/charts")
        self.static_charts_dir.mkdir(parents=True, exist_ok=True)

        # Initialize SVG chart generator
        self.chart_generator = SVGChartGenerator()
        # Default chart dimensions - can be overridden by subclasses
        self.pie_chart_width = 600
        self.pie_chart_height = 450
        self.bar_chart_width = 800
        self.bar_chart_height = 500

    @abstractmethod
    def get_section_title(self):
        """Return the section title for the social category"""
        pass

    @abstractmethod
    def get_section_number(self):
        """Return the section number for the social category"""
        pass

    @abstractmethod
    def get_data(self):
        """Fetch and process data specific to the social category"""
        pass

    @abstractmethod
    def generate_analysis_text(self, data):
        """Generate analysis text specific to the social category"""
        pass

    def generate_chart_svg(self, data, chart_type="pie"):
        """Generate chart SVG using SVGChartGenerator"""
        if chart_type == "pie":
            # Format municipality data for pie chart
            formatted_data = self._format_municipality_data_for_pie_chart(
                data.get("municipality_data", {})
            )
            return self.chart_generator.generate_pie_chart_svg(
                formatted_data,
                include_title=False,
                title_nepali=self.get_section_title(),
                title_english="Social Data Distribution",
            )
        elif chart_type == "bar":
            # Format ward data for bar chart
            formatted_data = self._format_ward_data_for_bar_chart(
                data.get("ward_data", {})
            )
            return self.chart_generator.generate_bar_chart_svg(
                formatted_data,
                include_title=False,
                title_nepali=f"वडा अनुसार {self.get_section_title()}",
                title_english="Ward-wise Social Data Distribution",
            )
        return None

    def _format_municipality_data_for_pie_chart(self, municipality_data):
        """Format municipality data for pie chart generation"""
        if not municipality_data:
            return {}

        formatted_data = {}
        for key, value in municipality_data.items():
            if isinstance(value, dict):
                # If value is already properly formatted with name_nepali and population
                if "name_nepali" in value and "population" in value:
                    formatted_data[key] = value
                else:
                    # Try to extract population from various possible fields
                    population = (
                        value.get("population", 0)
                        or value.get("households", 0)
                        or value.get("total", 0)
                    )
                    if population > 0:
                        formatted_data[key] = {
                            "name_nepali": value.get("name_nepali", key),
                            "population": population,
                            "percentage": value.get("percentage", 0),
                        }
            elif isinstance(value, (int, float)) and value > 0:
                # If value is just a number
                formatted_data[key] = {
                    "name_nepali": key,
                    "population": value,
                    "percentage": 0,
                }

        return formatted_data

    def _format_ward_data_for_bar_chart(self, ward_data):
        """Format ward data for bar chart generation"""
        if not ward_data:
            return {}

        formatted_data = {}
        for ward_key, ward_info in ward_data.items():
            if isinstance(ward_info, dict):
                ward_num = str(ward_key)
                total_population = ward_info.get(
                    "total_population", 0
                ) or ward_info.get("total_households", 0)

                if total_population > 0:
                    formatted_data[ward_num] = {
                        "ward_name": f"वडा नं. {ward_num}",
                        "total_population": total_population,
                        "demographics": self._extract_demographics_from_ward(ward_info),
                    }

        return formatted_data

    def _extract_demographics_from_ward(self, ward_info):
        """Extract demographic breakdown from ward info"""
        demographics = {}

        # Look for various possible demographic data structures
        if "toilet_types" in ward_info:
            for toilet_type, toilet_data in ward_info["toilet_types"].items():
                demographics[toilet_type] = {
                    "name_nepali": toilet_data.get("name_nepali", toilet_type),
                    "population": toilet_data.get("population", 0),
                    "percentage": toilet_data.get("percentage", 0),
                }
        elif "waste_methods" in ward_info:
            for method, method_data in ward_info["waste_methods"].items():
                demographics[method] = {
                    "name_nepali": method_data.get("name_nepali", method),
                    "population": method_data.get("population", 0),
                    "percentage": method_data.get("percentage", 0),
                }
        elif "subjects" in ward_info:
            for subject, subject_data in ward_info["subjects"].items():
                demographics[subject] = {
                    "name_nepali": subject_data.get("name_nepali", subject),
                    "population": subject_data.get("population", 0),
                    "percentage": subject_data.get("percentage", 0),
                }
        elif "dropout_causes" in ward_info:
            for cause, cause_data in ward_info["dropout_causes"].items():
                demographics[cause] = {
                    "name_nepali": cause_data.get("name_nepali", cause),
                    "population": cause_data.get("population", 0),
                    "percentage": cause_data.get("percentage", 0),
                }
        elif "literacy_types" in ward_info:
            for literacy_type, literacy_data in ward_info["literacy_types"].items():
                demographics[literacy_type] = {
                    "name_nepali": literacy_data.get("name_nepali", literacy_type),
                    "population": literacy_data.get("population", 0),
                    "percentage": literacy_data.get("percentage", 0),
                }
        elif "old_age_data" in ward_info:
            for age_type, age_data in ward_info["old_age_data"].items():
                demographics[age_type] = {
                    "name_nepali": age_data.get("name_nepali", age_type),
                    "population": age_data.get("population", 0),
                    "percentage": age_data.get("percentage", 0),
                }
        else:
            # Generic extraction - look for any field that looks like demographic data
            for key, value in ward_info.items():
                if key not in [
                    "ward_number",
                    "ward_name",
                    "total_population",
                    "total_households",
                ] and isinstance(value, dict):
                    if "population" in value or "households" in value:
                        pop = value.get("population", 0) or value.get("households", 0)
                        if pop > 0:
                            demographics[key] = {
                                "name_nepali": value.get("name_nepali", key),
                                "population": pop,
                                "percentage": value.get("percentage", 0),
                            }

        return demographics

    def generate_report_content(self, data):
        """Generate report content - can be overridden by subclasses"""
        return self.generate_analysis_text(data)

    def process_for_pdf(self):
        """Process category data for PDF generation including charts"""
        # Get raw data
        data = self.get_data()

        # Generate analysis text
        coherent_analysis = self.generate_report_content(data)

        # Generate and save charts
        charts = self.generate_and_save_charts(data)

        # Calculate total population/households
        total_count = data.get("total_households", 0) or data.get("total_population", 0)

        # Format ward data for template use (ensure demographics field exists)
        formatted_ward_data = self._format_ward_data_for_template(
            data.get("ward_data", {})
        )

        return {
            "data": data,
            "municipality_data": data.get("municipality_data", {}),
            "ward_data": formatted_ward_data,
            "total_households": total_count,
            "total_population": total_count,
            "report_content": coherent_analysis,
            "charts": charts,
            "section_title": self.get_section_title(),
            "section_number": self.get_section_number(),
        }

    def _format_ward_data_for_template(self, ward_data):
        """Format ward data for template use - ensures demographics field exists"""
        if not ward_data:
            return {}

        formatted_data = {}
        for ward_key, ward_info in ward_data.items():
            if isinstance(ward_info, dict):
                ward_num = str(ward_key)
                total_population = ward_info.get(
                    "total_population", 0
                ) or ward_info.get("total_households", 0)

                # Create formatted ward data with demographics field
                formatted_ward_info = {
                    "ward_number": ward_num,
                    "ward_name": f"वडा नं. {ward_num}",
                    "total_population": total_population,
                    "demographics": self._extract_demographics_from_ward(ward_info),
                }

                # Also preserve the original structure for backward compatibility
                formatted_ward_info.update(ward_info)

                formatted_data[ward_key] = formatted_ward_info

        return formatted_data

    def get_category_name(self):
        """Get category name from class name"""
        return self.__class__.__name__.lower().replace("processor", "")

    def generate_and_save_charts(self, data):
        """Generate and save both pie and bar charts"""
        import subprocess
        import os

        charts_info = {}
        category_name = self.get_category_name()

        try:
            # Generate pie chart for municipality-wide data
            pie_svg_path = self.static_charts_dir / f"{category_name}_pie_chart.svg"
            pie_png_path = self.static_charts_dir / f"{category_name}_pie_chart.png"

            # Only generate if PNG doesn't exist
            if not pie_png_path.exists():
                pie_svg = self.generate_chart_svg(data, chart_type="pie")
                if pie_svg:
                    with open(pie_svg_path, "w", encoding="utf-8") as f:
                        f.write(pie_svg)
                    charts_info["pie_chart_svg"] = (
                        f"images/charts/{category_name}_pie_chart.svg"
                    )

                    # Try to convert to PNG using subprocess
                    try:
                        subprocess.run(
                            [
                                "inkscape",
                                "--export-filename",
                                str(pie_png_path),
                                "--export-dpi=600",
                                str(pie_svg_path),
                            ],
                            check=True,
                            timeout=30,
                        )
                        if pie_png_path.exists():
                            charts_info["pie_chart_png"] = (
                                f"images/charts/{category_name}_pie_chart.png"
                            )
                    except:
                        pass  # Use SVG fallback
            else:
                # PNG exists, just add paths to charts_info
                charts_info["pie_chart_png"] = (
                    f"images/charts/{category_name}_pie_chart.png"
                )
                if pie_svg_path.exists():
                    charts_info["pie_chart_svg"] = (
                        f"images/charts/{category_name}_pie_chart.svg"
                    )

            # Generate bar chart for ward-wise data
            print(category_name)
            if data.get("ward_data"):
                bar_svg_path = self.static_charts_dir / f"{category_name}_bar_chart.svg"
                bar_png_path = self.static_charts_dir / f"{category_name}_bar_chart.png"

                # Only generate if PNG doesn't exist
                if not bar_png_path.exists():
                    bar_svg = self.generate_chart_svg(data, chart_type="bar")
                    if category_name == "majorsubject" or category_name == "toilettype":
                        print(bar_svg)
                        print(data)
                    if bar_svg:
                        with open(bar_svg_path, "w", encoding="utf-8") as f:
                            f.write(bar_svg)
                        charts_info["bar_chart_svg"] = (
                            f"images/charts/{category_name}_bar_chart.svg"
                        )

                        # Try to convert to PNG using subprocess
                        try:
                            subprocess.run(
                                [
                                    "inkscape",
                                    "--export-filename",
                                    str(bar_png_path),
                                    "--export-dpi=600",
                                    str(bar_svg_path),
                                ],
                                check=True,
                                timeout=30,
                            )
                            if bar_png_path.exists():
                                charts_info["bar_chart_png"] = (
                                    f"images/charts/{category_name}_bar_chart.png"
                                )
                        except:
                            pass  # Use SVG fallback
                else:
                    # PNG exists, just add paths to charts_info
                    charts_info["bar_chart_png"] = (
                        f"images/charts/{category_name}_bar_chart.png"
                    )
                    if bar_svg_path.exists():
                        charts_info["bar_chart_svg"] = (
                            f"images/charts/{category_name}_bar_chart.svg"
                        )

        except Exception as e:
            print(f"Error generating {category_name} charts: {e}")

        return charts_info


class BaseSocialReportFormatter(ABC):
    """Base report formatter for social categories with common functionality"""

    def __init__(self, processor_data):
        self.data = processor_data
        self.municipality_name = "लुङ्ग्री गाउँपालिका"

    @abstractmethod
    def format_for_html(self):
        """Format data for HTML template rendering"""
        pass

    @abstractmethod
    def format_for_api(self):
        """Format data for API response"""
        pass

    def generate_diversity_analysis(self, active_count, total_count, unit="घरपरिवार"):
        """Generate diversity analysis text"""
        return f"""यस गाउँपालिकामा कुल {active_count} वटा विभिन्न प्रकारका सुविधाहरूको प्रयोग भइरहेको छ जसले सामाजिक विकासको झलक दिन्छ । यस्तो विविधताले स्थानीय जीवनयात्राको गुणस्तरमा सुधार ल्याउन सहयोग पुर्‍याएको छ ।"""

    def generate_improvement_conclusion(self):
        """Generate improvement conclusion text"""
        return """सबै {unit} हरूमा उपलब्ध सुविधाहरूको सुधार र विस्तारले यस गाउँपालिकाको जीवनयात्राको गुणस्तरमा महत्वपूर्ण योगदान पुर्‍याइरहेको छ । भविष्यमा थप सुधारका लागि निरन्तर प्रयास आवश्यक छ ।"""
