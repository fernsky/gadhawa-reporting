"""
Enhanced Base Processor with Chart Management Integration

Provides improved chart generation with caching and tracking capabilities.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Tuple
from pathlib import Path
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apps.chart_management.services import get_chart_service
from apps.chart_management.models import ChartTypeChoice


class EnhancedChartProcessor(ABC):
    """
    Enhanced base processor with integrated chart management
    """

    def __init__(self):
        self.chart_service = get_chart_service()
        # Default chart dimensions - can be overridden by subclasses
        self.pie_chart_width = 800
        self.pie_chart_height = 400
        self.bar_chart_width = 900
        self.bar_chart_height = 500
        self.chart_radius = 130

    @abstractmethod
    def get_section_title(self):
        """Return the section title"""
        pass

    @abstractmethod
    def get_section_number(self):
        """Return the section number"""
        pass

    @abstractmethod
    def get_data(self):
        """Return processed data for the section"""
        pass

    @abstractmethod
    def get_chart_key(self):
        """Return unique chart key for this processor"""
        pass

    def generate_pie_chart(
        self, data: Dict[str, Any], title: str, **kwargs
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Generate pie chart with caching

        Returns:
            Tuple of (svg_url, png_url)
        """
        chart_key = f"{self.get_chart_key()}_pie"

        return self.chart_service.get_or_generate_chart(
            chart_key=chart_key,
            chart_type=ChartTypeChoice.PIE,
            data=data,
            title=title,
            width=kwargs.get("width", self.pie_chart_width),
            height=kwargs.get("height", self.pie_chart_height),
            radius=kwargs.get("radius", self.chart_radius),
            **kwargs,
        )

    def generate_bar_chart(
        self, data: Dict[str, Any], title: str, **kwargs
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Generate bar chart with caching

        Returns:
            Tuple of (svg_url, png_url)
        """
        chart_key = f"{self.get_chart_key()}_bar"

        return self.chart_service.get_or_generate_chart(
            chart_key=chart_key,
            chart_type=ChartTypeChoice.BAR,
            data=data,
            title=title,
            width=kwargs.get("width", self.bar_chart_width),
            height=kwargs.get("height", self.bar_chart_height),
            **kwargs,
        )

    def generate_chart_urls(self, data: Dict[str, Any]) -> Dict[str, Dict[str, str]]:
        """
        Generate all chart URLs for this processor

        Returns:
            Dict with chart types as keys and URL dicts as values
        """
        urls = {}

        # Generate pie chart if applicable
        if self.supports_pie_chart():
            pie_title = self.get_pie_chart_title()
            svg_url, png_url = self.generate_pie_chart(data, pie_title)
            urls["pie"] = {
                "svg": svg_url or "",
                "png": png_url or "",
                "title": pie_title,
            }

        # Generate bar chart if applicable
        if self.supports_bar_chart():
            bar_title = self.get_bar_chart_title()
            svg_url, png_url = self.generate_bar_chart(data, bar_title)
            urls["bar"] = {
                "svg": svg_url or "",
                "png": png_url or "",
                "title": bar_title,
            }

        return urls

    def supports_pie_chart(self) -> bool:
        """Override in subclass to enable pie chart generation"""
        return True

    def supports_bar_chart(self) -> bool:
        """Override in subclass to enable bar chart generation"""
        return False

    def get_pie_chart_title(self) -> str:
        """Get title for pie chart - override in subclass"""
        return self.get_section_title()

    def get_bar_chart_title(self) -> str:
        """Get title for bar chart - override in subclass"""
        return self.get_section_title()

    def process_for_pdf(self) -> Dict[str, Any]:
        """
        Process data for PDF generation with charts

        Returns:
            Dict containing processed data and chart URLs
        """
        data = self.get_data()
        chart_urls = self.generate_chart_urls(data)

        return {
            "section_title": self.get_section_title(),
            "section_number": self.get_section_number(),
            "data": data,
            "charts": chart_urls,
            "html_content": self.generate_html_content(data, chart_urls),
        }

    def generate_html_content(
        self, data: Dict[str, Any], chart_urls: Dict[str, Dict[str, str]]
    ) -> str:
        """
        Generate HTML content for the section
        Override in subclass for custom HTML generation
        """
        return ""

    def get_template_context(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get template context for rendering

        Returns:
            Dict with context variables for template rendering
        """
        chart_urls = self.generate_chart_urls(data)

        return {
            "section_title": self.get_section_title(),
            "section_number": self.get_section_number(),
            "data": data,
            "charts": chart_urls,
        }


class EnhancedReportFormatter(ABC):
    """Enhanced report formatter with chart integration"""

    def __init__(self, processor_data: Dict[str, Any]):
        self.processor_data = processor_data
        self.data = processor_data.get("data", {})
        self.charts = processor_data.get("charts", {})

    @abstractmethod
    def format_for_html(self) -> str:
        """Format data for HTML output"""
        pass

    def format_for_api(self) -> Dict[str, Any]:
        """Format data for API response"""
        return {
            "section_title": self.processor_data.get("section_title", ""),
            "section_number": self.processor_data.get("section_number", ""),
            "data": self.data,
            "charts": self.charts,
        }

    def get_chart_html(
        self, chart_type: str, css_class: str = "chart-container"
    ) -> str:
        """
        Get HTML for displaying chart

        Args:
            chart_type: Type of chart ('pie', 'bar', etc.)
            css_class: CSS class for the container

        Returns:
            HTML string for chart display
        """
        if chart_type not in self.charts:
            return ""

        chart_info = self.charts[chart_type]
        png_url = chart_info.get("png", "")
        svg_url = chart_info.get("svg", "")
        title = chart_info.get("title", "")

        if png_url:
            return f"""
            <div class="{css_class}">
                <img src="{png_url}" alt="{title}" class="chart-image chart-png" 
                     onerror="this.style.display='none'; this.nextElementSibling.style.display='block';" />
                {f'<img src="{svg_url}" alt="{title}" class="chart-image chart-svg" style="display: none;" />' if svg_url else ''}
            </div>
            """
        elif svg_url:
            return f"""
            <div class="{css_class}">
                <img src="{svg_url}" alt="{title}" class="chart-image chart-svg" />
            </div>
            """
        else:
            return f"""
            <div class="{css_class}">
                <div class="chart-error">चार्ट लोड गर्न सकिएन: {title}</div>
            </div>
            """
