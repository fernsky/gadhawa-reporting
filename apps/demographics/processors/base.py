"""
Base Demographics Processor

Common functionality for processing demographic data across all categories.
"""

from abc import ABC, abstractmethod
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from pathlib import Path
from apps.demographics.utils.svg_chart_generator import SVGChartGenerator


class BaseDemographicsProcessor(ABC):
    """Base class for all demographic data processors"""

    def __init__(self):
        # Use proper static directory path
        from django.conf import settings

        # Use staticfiles directory if available, fallback to STATIC_ROOT
        if hasattr(settings, "STATICFILES_DIRS") and settings.STATICFILES_DIRS:
            self.static_charts_dir = (
                Path(settings.STATICFILES_DIRS[0]) / "images" / "charts"
            )
        else:
            self.static_charts_dir = Path(settings.STATIC_ROOT) / "images" / "charts"

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
        """Return the section title for the demographic category"""
        pass

    @abstractmethod
    def get_section_number(self):
        """Return the section number for the demographic category"""
        pass

    @abstractmethod
    def get_data(self):
        """Fetch and process data specific to the demographic category"""
        pass

    @abstractmethod
    def generate_report_content(self, data):
        """Generate report content specific to the demographic category"""
        pass

    def generate_chart_svg(self, data, chart_type="pie"):
        """Generate chart SVG using SVGChartGenerator"""
        if chart_type == "pie":
            return self.chart_generator.generate_pie_chart_svg(
                data, include_title=False
            )
        elif chart_type == "bar":
            return self.chart_generator.generate_bar_chart_svg(
                data, include_title=False
            )
        else:
            return None

    def process_for_pdf(self):
        """Process category data for PDF generation including charts"""
        # Get raw data
        data = self.get_data()
        # Generate report content
        report_content = self.generate_report_content(data)

        # Generate and save charts
        charts = self.generate_and_save_charts(data)  # Calculate total population
        if isinstance(data, dict) and "total_population" in data:
            # Househead format already has total_population
            total_population = data["total_population"]
        elif isinstance(data, dict) and "municipality_data" in data:
            # Househead format - calculate from municipality_data
            total_population = sum(
                item["population"]
                for item in data["municipality_data"].values()
                if isinstance(item, dict) and "population" in item
            )
        else:
            # Simple format
            total_population = sum(
                item["population"]
                for item in data.values()
                if isinstance(item, dict) and "population" in item
            )

        return {
            "data": data,
            "report_content": report_content,
            "charts": charts,
            "total_population": total_population,
            "section_title": self.get_section_title(),
            "section_number": self.get_section_number(),
        }

    def generate_and_save_charts(self, data):
        """Generate charts using SVGChartGenerator and save them as PNG files"""
        charts = {}
        category_name = self.__class__.__name__.lower().replace("processor", "")

        # Determine data structure - check if it's househead format or simple format
        if (
            isinstance(data, dict)
            and "municipality_data" in data
            and "ward_data" in data
        ):
            # Househead format with both municipality and ward data
            pie_data = data["municipality_data"]
            bar_data = data["ward_data"]
        else:
            # Simple format - use the data as is for pie chart
            pie_data = data
            bar_data = None  # No ward data available for bar chart

        # Generate pie chart using SVGChartGenerator
        success, png_path, svg_path = self.chart_generator.generate_chart_image(
            demographic_data=pie_data,
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
        if bar_data:
            success, png_path, svg_path = self.chart_generator.generate_chart_image(
                demographic_data=bar_data,
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


class BaseReportFormatter(ABC):
    """Base report formatter with common functionality"""

    def __init__(self):
        self.municipality_name = "लुङ्ग्री गाउँपालिका"

    @abstractmethod
    def generate_formal_report(self, data):
        """Generate formal report content"""
        pass

    def generate_diversity_analysis(self, active_count, total_population):
        """Generate diversity analysis text"""
        return f"""यस गाउँपालिकामा कुल {active_count} वटा विभिन्न समुदायहरूको बसोबास रहेको छ जसले सामाजिक विविधताको झलक दिन्छ । यस्तो विविधताले स्थानीय सांस्कृतिक धनलाई समृद्ध बनाउँदै एकताको भावना विकास गर्न सहयोग पुर्‍याएको छ ।"""

    def generate_harmony_conclusion(self):
        """Generate harmony conclusion text"""
        return """सबै समुदायहरू बीचको सद्भावना र पारस्परिक सहयोगले यस गाउँपालिकाको सामाजिक एकता र शान्तिमा महत्वपूर्ण योगदान पुर्‍याइरहेको छ । विविधतामा एकताको यो उदाहरणले भविष्यका पुस्ताहरूका लागि सकारात्मक सन्देश दिन्छ ।"""
