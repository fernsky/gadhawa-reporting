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
        self.static_charts_dir = Path("static/images")
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
            return self.chart_generator.generate_pie_chart_svg(data, include_title=False)
        elif chart_type == "bar":
            return self.chart_generator.generate_bar_chart_svg(data, include_title=False)
        else:
            return None

    def process_for_pdf(self):
        """Process category data for PDF generation including charts"""
        # Get raw data
        data = self.get_data()
        
        # Generate analysis text
        coherent_analysis = self.generate_analysis_text(data)
        
        # Generate and save charts
        charts = self.generate_and_save_charts(data)
        
        # Calculate total population/households
        total_count = data.get('total_households', 0) or data.get('total_population', 0)
        
        return {
            'municipality_data': data.get('municipality_data', {}),
            'ward_data': data.get('ward_data', {}),
            'total_households': total_count,
            'coherent_analysis': coherent_analysis,
            'pdf_charts': {self.get_category_name(): charts},
            'section_title': self.get_section_title(),
            'section_number': self.get_section_number(),
        }

    def get_category_name(self):
        """Get category name from class name"""
        return self.__class__.__name__.lower().replace('processor', '')

    def generate_and_save_charts(self, data):
        """Generate charts using SVGChartGenerator and save them as PNG files"""
        charts = {}
        category_name = self.get_category_name()
        
        # Use municipality data for charts
        chart_data = data.get('municipality_data', {})
        
        # Generate pie chart using SVGChartGenerator
        success, png_path, svg_path = self.chart_generator.generate_chart_image(
            demographic_data=chart_data,
            output_name=f'{category_name}_pie_chart',
            static_dir=str(self.static_charts_dir),
            chart_type="pie",
            include_title=False
        )
        
        if success and png_path:
            charts['pie_chart_png'] = f'images/{category_name}_pie_chart.png'
            charts['pie_chart_svg'] = f'images/{category_name}_pie_chart.svg'
        elif svg_path:
            # Fallback to SVG if PNG conversion fails
            charts['pie_chart_svg'] = f'images/{category_name}_pie_chart.svg'
        
        # Generate bar chart for ward data if available
        ward_data = data.get('ward_data', {})
        if ward_data:
            success, png_path, svg_path = self.chart_generator.generate_chart_image(
                demographic_data=ward_data,
                output_name=f'{category_name}_bar_chart',
                static_dir=str(self.static_charts_dir),
                chart_type="bar",
                include_title=False
            )
            
            if success and png_path:
                charts['bar_chart_png'] = f'images/{category_name}_bar_chart.png'
                charts['bar_chart_svg'] = f'images/{category_name}_bar_chart.svg'
            elif svg_path:
                # Fallback to SVG if PNG conversion fails
                charts['bar_chart_svg'] = f'images/{category_name}_bar_chart.svg'
        
        return charts


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
