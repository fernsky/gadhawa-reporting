"""
Base Economics Processor

Common functionality for processing economics data across all categories.
"""

from abc import ABC, abstractmethod
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from pathlib import Path
from apps.demographics.utils.svg_chart_generator import SVGChartGenerator


class BaseEconomicsProcessor(ABC):
    """Base class for all economics data processors"""

    def __init__(self):
        self.chart_generator = SVGChartGenerator()
        # Default chart dimensions
        self.pie_chart_width = 800
        self.pie_chart_height = 400
        self.bar_chart_width = 900
        self.bar_chart_height = 400
        self.chart_radius = 140

        # Economics-specific colors for different categories
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

    @abstractmethod
    def get_section_title(self):
        """Return the section title in Nepali"""
        pass

    @abstractmethod
    def get_section_number(self):
        """Return the section number"""
        pass

    @abstractmethod
    def get_data(self):
        """Get processed data for the section"""
        pass

    @abstractmethod
    def generate_analysis_text(self, data):
        """Generate comprehensive Nepali analysis text"""
        pass

    def generate_pie_chart(self, data, title="Economics Distribution"):
        """Generate pie chart for economics data"""
        if not data:
            return ""

        # Prepare data for chart - convert to format expected by SVGChartGenerator
        chart_data = {}
        for key, info in data.items():
            if info.get("households", 0) > 0:
                chart_data[key] = {
                    "population": info.get("households", 0),
                    "name_nepali": info.get("name_nepali", key),
                }

        if not chart_data:
            return ""

        return self.chart_generator.generate_pie_chart_svg(
            chart_data, include_title=False, title_nepali=title, title_english=""
        )

    def generate_bar_chart(self, data, title="Ward-wise Economics Distribution"):
        """Generate bar chart for ward-wise economics data"""
        if not data:
            return ""

        # Prepare ward-wise data in the format expected by SVGChartGenerator
        ward_data = {}
        for ward_num, ward_info in data.items():
            if isinstance(ward_info, dict) and "total_households" in ward_info:
                ward_data[ward_num] = {
                    "total_population": ward_info["total_households"],
                    "ward_name": f"वडा {ward_num}",
                }

        if not ward_data:
            return ""

        return self.chart_generator.generate_bar_chart_svg(
            ward_data, include_title=False, title_nepali=title, title_english=""
        )

    def process_for_pdf(self):
        """Process economics data for PDF generation including charts"""
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
            "pdf_charts": {self.get_chart_key(): charts},
            "section_title": self.get_section_title(),
            "section_number": self.get_section_number(),
        }

    def get_chart_key(self):
        """Get the chart key for this processor"""
        return self.__class__.__name__.lower().replace("processor", "")

    def generate_and_save_charts(self, data):
        """Generate and save charts, return paths"""
        charts = {}

        # Generate pie chart
        if data.get("municipality_data"):
            pie_chart = self.generate_pie_chart(data["municipality_data"])
            if pie_chart:
                charts["pie_chart_svg"] = pie_chart

        # Generate bar chart for ward data
        if data.get("ward_data"):
            bar_chart = self.generate_bar_chart(data["ward_data"])
            if bar_chart:
                charts["bar_chart_svg"] = bar_chart

        return charts


class BaseEconomicsReportFormatter(ABC):
    """Base report formatter for economics data with common functionality"""

    def __init__(self, processor_data):
        self.data = processor_data

    @abstractmethod
    def format_for_html(self):
        """Format data for HTML template rendering"""
        pass

    def format_for_api(self):
        """Format data for API response with common structure"""
        return {
            "section": self.data.get("section_number", ""),
            "title": self.data.get("section_title", ""),
            "summary": {
                "total_households": self.data.get("total_households", 0),
                "categories": len(self.data.get("municipality_data", {})),
                "wards": len(self.data.get("ward_data", {})),
            },
            "municipality_breakdown": self.data.get("municipality_data", {}),
            "ward_breakdown": self.data.get("ward_data", {}),
            "analysis": self.data.get("coherent_analysis", ""),
            "charts": self.data.get("pdf_charts", {}),
        }

    def generate_economic_impact_analysis(self, total_households, essential_percentage):
        """Generate economic impact analysis"""
        impact_level = (
            "उच्च"
            if essential_percentage > 60
            else "मध्यम" if essential_percentage > 30 else "न्यून"
        )

        return {
            "total_affected": total_households,
            "essential_services_percentage": essential_percentage,
            "impact_level": impact_level,
            "priority_areas": self._identify_priority_areas(),
        }

    def _identify_priority_areas(self):
        """Identify priority areas based on data"""
        priority_areas = []
        municipality_data = self.data.get("municipality_data", {})

        # Check for high education expenses
        if municipality_data.get("education", {}).get("percentage", 0) > 20:
            priority_areas.append("शिक्षा क्षेत्रमा उच्च खर्च")

        # Check for health expenses
        if municipality_data.get("health", {}).get("percentage", 0) > 15:
            priority_areas.append("स्वास्थ्य सेवामा उच्च खर्च")

        # Check for loan burden
        if municipality_data.get("loan_payment", {}).get("percentage", 0) > 25:
            priority_areas.append("ऋण भुक्तानीको उच्च बोझ")

        return priority_areas
