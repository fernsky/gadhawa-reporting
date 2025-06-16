"""
Base Demographics Processor

Common functionality for processing demographic data across all categories.
"""

from abc import ABC, abstractmethod
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
import xml.etree.ElementTree as ET
import os


class BaseDemographicsProcessor(ABC):
    """Base class for all demographic data processors"""
    
    def __init__(self):
        self.static_charts_dir = Path(settings.STATIC_ROOT or settings.STATICFILES_DIRS[0]) / 'images' / 'charts'
        self.static_charts_dir.mkdir(parents=True, exist_ok=True)
    
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

    @abstractmethod
    def generate_chart_svg(self, data, chart_type="pie"):
        """Generate chart SVG specific to the demographic category"""
        pass

    def process_for_pdf(self):
        """Process category data for PDF generation including charts"""
        # Get raw data
        data = self.get_data()
        
        # Generate report content
        report_content = self.generate_report_content(data)
        
        # Generate and save charts
        charts = self.generate_and_save_charts(data)
        
        # Calculate total population
        total_population = sum(item['population'] for item in data.values() if isinstance(item, dict) and 'population' in item)
        
        return {
            'data': data,
            'report_content': report_content,
            'charts': charts,
            'total_population': total_population,
            'section_title': self.get_section_title(),
            'section_number': self.get_section_number(),
        }

    def generate_and_save_charts(self, data):
        """Generate charts and save them to static files"""
        charts = {}
        category_name = self.__class__.__name__.lower().replace('processor', '')
        
        # Generate pie chart
        pie_chart_svg = self.generate_chart_svg(data, chart_type="pie")
        if pie_chart_svg:
            pie_chart_path = self.static_charts_dir / f'{category_name}_pie_chart.svg'
            self.save_svg_to_file(pie_chart_svg, pie_chart_path)
            charts['pie_chart'] = pie_chart_svg
            charts['pie_chart_url'] = f'images/charts/{category_name}_pie_chart.svg'
        
        # Generate bar chart
        bar_chart_svg = self.generate_chart_svg(data, chart_type="bar")
        if bar_chart_svg:
            bar_chart_path = self.static_charts_dir / f'{category_name}_bar_chart.svg'
            self.save_svg_to_file(bar_chart_svg, bar_chart_path)
            charts['bar_chart'] = bar_chart_svg
            charts['bar_chart_url'] = f'images/charts/{category_name}_bar_chart.svg'
        
        return charts

    def save_svg_to_file(self, svg_content, file_path):
        """Save SVG content to file"""
        try:
            if isinstance(svg_content, str):
                Path(file_path).write_text(svg_content, encoding='utf-8')
            elif hasattr(svg_content, 'tag'):  # ET.Element
                ET.ElementTree(svg_content).write(file_path, encoding='utf-8', xml_declaration=True)
            return True
        except Exception as e:
            print(f"Error saving SVG to file: {e}")
            return False


class BaseChartGenerator(ABC):
    """Base SVG chart generator with common functionality"""
    
    def __init__(self):
        self.font_family = "Arial, sans-serif"
        self.font_size_title = 16
        self.font_size_labels = 12
        self.font_size_legend = 10

    @abstractmethod
    def generate_pie_chart_svg(self, data):
        """Generate pie chart SVG"""
        pass

    @abstractmethod
    def generate_bar_chart_svg(self, data):
        """Generate bar chart SVG"""
        pass

    def generate_simple_pie_chart(self, data, colors):
        """Generate a simple pie chart SVG"""
        # Filter data with population > 0
        filtered_data = {k: v for k, v in data.items() if isinstance(v, dict) and v.get('population', 0) > 0}
        
        if not filtered_data:
            return self._generate_no_data_svg(400, 400)
        
        # Calculate total
        total = sum(item['population'] for item in filtered_data.values())
        if total == 0:
            return self._generate_no_data_svg(400, 400)
        
        # Create SVG
        svg = ET.Element('svg', {
            'width': '400',
            'height': '400',
            'xmlns': 'http://www.w3.org/2000/svg'
        })
        
        # Chart parameters
        center_x, center_y = 200, 180
        radius = 100
        
        # Generate pie slices
        angle = 0
        for key, item in filtered_data.items():
            if item['population'] > 0:
                slice_angle = (item['population'] / total) * 360
                color = colors.get(key, '#cccccc')
                
                # Create pie slice path
                start_angle = angle
                end_angle = angle + slice_angle
                
                # Convert to radians
                import math
                start_rad = math.radians(start_angle - 90)
                end_rad = math.radians(end_angle - 90)
                
                # Calculate path points
                x1 = center_x + radius * math.cos(start_rad)
                y1 = center_y + radius * math.sin(start_rad)
                x2 = center_x + radius * math.cos(end_rad)
                y2 = center_y + radius * math.sin(end_rad)
                
                large_arc = 1 if slice_angle > 180 else 0
                
                path_data = f"M {center_x} {center_y} L {x1} {y1} A {radius} {radius} 0 {large_arc} 1 {x2} {y2} Z"
                
                path = ET.SubElement(svg, 'path', {
                    'd': path_data,
                    'fill': color,
                    'stroke': '#ffffff',
                    'stroke-width': '2'
                })
                
                angle += slice_angle
        
        # Add legend
        legend_y = 320
        legend_x = 50
        col_width = 120
        col = 0
        
        for key, item in filtered_data.items():
            if item['population'] > 0:
                color = colors.get(key, '#cccccc')
                percentage = (item['population'] / total) * 100
                
                # Legend color box
                ET.SubElement(svg, 'rect', {
                    'x': str(legend_x + col * col_width),
                    'y': str(legend_y),
                    'width': '12',
                    'height': '12',
                    'fill': color
                })
                
                # Legend text
                label = getattr(item, 'name_nepali', key) if hasattr(item, 'name_nepali') else key
                text = f"{label} ({percentage:.1f}%)"
                ET.SubElement(svg, 'text', {
                    'x': str(legend_x + col * col_width + 18),
                    'y': str(legend_y + 10),
                    'font-family': self.font_family,
                    'font-size': str(self.font_size_legend),
                    'fill': '#333333'
                }).text = text
                
                col = (col + 1) % 3
                if col == 0:
                    legend_y += 20
        
        return ET.tostring(svg, encoding='unicode')

    def _generate_no_data_svg(self, width, height):
        """Generate no data available SVG"""
        svg = ET.Element('svg', {
            'width': str(width),
            'height': str(height),
            'xmlns': 'http://www.w3.org/2000/svg'
        })
        
        # Background
        ET.SubElement(svg, 'rect', {
            'width': str(width),
            'height': str(height),
            'fill': '#f8f9fa'
        })
        
        # Text
        ET.SubElement(svg, 'text', {
            'x': str(width//2),
            'y': str(height//2),
            'text-anchor': 'middle',
            'font-family': self.font_family,
            'font-size': '16',
            'fill': '#6c757d'
        }).text = 'डाटा उपलब्ध छैन'
        
        return ET.tostring(svg, encoding='unicode')


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
