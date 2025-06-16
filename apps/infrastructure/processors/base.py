"""
Base Infrastructure Processor

Common functionality for processing infrastructure data across all categories.
"""

from abc import ABC, abstractmethod
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from pathlib import Path
from apps.demographics.utils.svg_chart_generator import SVGChartGenerator


class BaseInfrastructureProcessor(ABC):
    """Base class for all infrastructure data processors"""
    
    def __init__(self):
        # Use proper static directory path
        self.static_charts_dir = Path("static/images/charts")
        self.static_charts_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize SVG chart generator
        self.chart_generator = SVGChartGenerator()
        
        # Default chart dimensions - can be overridden by subclasses
        self.pie_chart_width = 700
        self.pie_chart_height = 450
        self.bar_chart_width = 900
        self.bar_chart_height = 500
        self.chart_radius = 120
    
    @abstractmethod
    def get_section_title(self):
        """Return the section title in Nepali"""
        pass
    
    @abstractmethod
    def get_section_number(self):
        """Return the section number (e.g., '७.१.६', '७.१.७')"""
        pass
    
    @abstractmethod
    def get_data(self):
        """Get and process the data for this infrastructure category"""
        pass
    
    @abstractmethod
    def generate_analysis_text(self, data):
        """Generate coherent analysis text based on data"""
        pass
    
    def generate_pie_chart(self, data, title="Infrastructure Distribution"):
        """Generate pie chart for infrastructure data"""
        if not data:
            return None
        
        # Prepare data for chart - generic implementation
        chart_data = []
        for key, info in data.items():
            if isinstance(info, dict) and 'households' in info and info['households'] > 0:
                chart_data.append({
                    'label': info.get('name_nepali', key),
                    'value': info['households'],
                    'percentage': info.get('percentage', 0)
                })
        
        if not chart_data:
            return None
        
        return self.chart_generator.generate_pie_chart(
            data=chart_data,
            title=title,
            width=self.pie_chart_width,
            height=self.pie_chart_height,
            radius=self.chart_radius
        )
    
    def generate_bar_chart(self, data, title="Ward-wise Infrastructure Distribution"):
        """Generate bar chart for ward-wise infrastructure data"""
        if not data or 'ward_data' not in data:
            return None
        
        # Prepare data for ward-wise bar chart in the format expected by SVGChartGenerator
        ward_data = {}
        for ward_num, ward_info in data['ward_data'].items():
            ward_data[f"ward_{ward_num}"] = {
                'name_nepali': f"वडा {ward_num}",
                'population': ward_info.get('total_population', ward_info.get('total_households', 0)),
                'percentage': 0  # Calculate if needed
            }
        
        if not ward_data:
            return None
        
        return self.chart_generator.generate_bar_chart_svg(
            ward_data=ward_data,
            include_title=True,
            title_nepali=title,
            title_english="Ward-wise Distribution"
        )
    
    def process_for_pdf(self):
        """Process data for PDF generation"""
        data = self.get_data()
        
        # Generate analysis text
        coherent_analysis = self.generate_analysis_text(data)
        
        # Generate charts
        pie_chart_svg = self.generate_pie_chart(data.get('category_data', {}))
        bar_chart_svg = self.generate_bar_chart(data)
        
        # Prepare chart data for template
        pdf_charts = {
            self.get_chart_key(): {
                'pie_chart_svg': pie_chart_svg,
                'bar_chart_svg': bar_chart_svg,
                'pie_chart_png': None,  # Can be generated if needed
                'bar_chart_png': None   # Can be generated if needed
            }
        }
        
        return {
            'category_data': data.get('category_data', {}),
            'ward_data': data.get('ward_data', {}),
            'total_households': data.get('total_households', 0),
            'coherent_analysis': coherent_analysis,
            'pdf_charts': pdf_charts,
            'section_title': self.get_section_title(),
            'section_number': self.get_section_number()
        }
    
    def get_chart_key(self):
        """Get the key for storing charts in PDF context"""
        return self.get_section_number().lower().replace('.', '_')
    
    def generate_and_save_charts(self, data):
        """Generate and save charts to static directory"""
        charts = {}
        
        # Generate pie chart
        pie_chart = self.generate_pie_chart(data.get('category_data', {}))
        if pie_chart:
            pie_filename = f"{self.get_chart_key()}_pie_chart.svg"
            pie_path = self.static_charts_dir / pie_filename
            with open(pie_path, 'w', encoding='utf-8') as f:
                f.write(pie_chart)
            charts['pie_chart_svg'] = f"images/charts/{pie_filename}"
        
        # Generate bar chart
        bar_chart = self.generate_bar_chart(data)
        if bar_chart:
            bar_filename = f"{self.get_chart_key()}_bar_chart.svg"
            bar_path = self.static_charts_dir / bar_filename
            with open(bar_path, 'w', encoding='utf-8') as f:
                f.write(bar_chart)
            charts['bar_chart_svg'] = f"images/charts/{bar_filename}"
        
        return charts


class BaseInfrastructureReportFormatter(ABC):
    """Base report formatter for infrastructure data with common functionality"""
    
    def __init__(self, processor_data):
        self.data = processor_data
    
    @abstractmethod
    def format_for_html(self):
        """Format data for HTML template rendering"""
        pass
    
    def format_for_api(self):
        """Format data for API response"""
        return {
            'section': self.data['section_number'],
            'title': self.data['section_title'],
            'summary': {
                'total_households': self.data['total_households'],
                'categories': len(self.data['category_data']),
                'wards': len(self.data['ward_data'])
            },
            'category_breakdown': self.data['category_data'],
            'ward_breakdown': self.data['ward_data'],
            'analysis': self.data['coherent_analysis']
        }
    
    def generate_accessibility_analysis(self, good_access_percentage, total_households):
        """Generate accessibility analysis text"""
        if good_access_percentage >= 80:
            return f"यस क्षेत्रमा {good_access_percentage:.1f}% घरपरिवारको राम्रो पहुँच छ, जुन उत्कृष्ट मानिन्छ।"
        elif good_access_percentage >= 60:
            return f"यस क्षेत्रमा {good_access_percentage:.1f}% घरपरिवारको राम्रो पहुँच छ, जुन सन्तोषजनक मानिन्छ।"
        elif good_access_percentage >= 40:
            return f"यस क्षेत्रमा {good_access_percentage:.1f}% घरपरिवारको राम्रो पहुँच छ, जुन सुधार आवश्यक छ।"
        else:
            return f"यस क्षेत्रमा केवल {good_access_percentage:.1f}% घरपरिवारको मात्र राम्रो पहुँच छ, जुन तत्काल सुधार आवश्यक छ।"
    
    def generate_improvement_recommendation(self, poor_access_count):
        """Generate improvement recommendations"""
        if poor_access_count > 0:
            return f"यस क्षेत्रमा {poor_access_count} घरपरिवारको पहुँच सुधार गर्न आवश्यक छ। उचित योजना र लगानीको माध्यमबाट यो समस्या समाधान गर्न सकिन्छ।"
        else:
            return "यस क्षेत्रमा सबै घरपरिवारको राम्रो पहुँच छ।"
