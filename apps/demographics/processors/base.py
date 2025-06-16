"""
Base Demographics Processor

Common functionality for processing demographic data across all categories.
"""

from abc import ABC, abstractmethod
import xml.etree.ElementTree as ET
from django.utils.translation import gettext_lazy as _
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


class BaseDemographicsProcessor(ABC):
    """Base class for all demographic data processors"""
    
    def __init__(self):
        self.municipality_name = "लुङ्ग्री गाउँपालिका"
        self.font_family = "Arial, sans-serif"
    
    @abstractmethod
    def get_data(self):
        """Get processed data for this demographic category"""
        pass
    
    @abstractmethod
    def generate_report_content(self, data):
        """Generate formal report content"""
        pass
    
    @abstractmethod
    def generate_chart_svg(self, data, chart_type="pie"):
        """Generate SVG chart for the data"""
        pass
    
    def get_section_title(self):
        """Override in subclasses to provide section title"""
        return "Demographics Section"
    
    def get_section_number(self):
        """Override in subclasses to provide section number"""
        return "3.X"
    
    def process_for_pdf(self):
        """Main method to process all data for PDF generation"""
        data = self.get_data()
        return {
            'data': data,
            'report_content': self.generate_report_content(data),
            'charts': {
                'pie_chart': self.generate_chart_svg(data, 'pie'),
                'bar_chart': self.generate_chart_svg(data, 'bar'),
            },
            'section_title': self.get_section_title(),
            'section_number': self.get_section_number(),
            'total_population': self._calculate_total_population(data),
            'summary_stats': self._generate_summary_stats(data)
        }
    
    def _calculate_total_population(self, data):
        """Calculate total population from data"""
        if isinstance(data, dict):
            return sum(item.get('population', 0) for item in data.values() if isinstance(item, dict))
        return 0
    
    def _generate_summary_stats(self, data):
        """Generate summary statistics"""
        total = self._calculate_total_population(data)
        if not total:
            return {}
        
        stats = {'total': total}
        if isinstance(data, dict):
            # Find top categories
            sorted_items = sorted(
                [(k, v) for k, v in data.items() if isinstance(v, dict) and v.get('population', 0) > 0],
                key=lambda x: x[1].get('population', 0),
                reverse=True
            )
            stats['top_categories'] = sorted_items[:3]
            stats['diversity_count'] = len([item for item in data.values() if isinstance(item, dict) and item.get('population', 0) > 0])
        
        return stats


class BaseChartGenerator:
    """Base SVG chart generator with common functionality"""
    
    def __init__(self):
        self.font_family = "Arial, sans-serif"
        self.font_size_title = 18
        self.font_size_labels = 14
        self.font_size_legend = 12
        
    def _create_svg(self, width, height):
        """Create basic SVG element"""
        return ET.Element('svg', {
            'width': str(width),
            'height': str(height),
            'xmlns': 'http://www.w3.org/2000/svg'
        })
    
    def _add_text(self, parent, x, y, text, font_size=12, color="#000", anchor="start"):
        """Add text element to SVG"""
        text_elem = ET.SubElement(parent, 'text', {
            'x': str(x),
            'y': str(y),
            'font-family': self.font_family,
            'font-size': str(font_size),
            'fill': color,
            'text-anchor': anchor
        })
        text_elem.text = str(text)
        return text_elem
    
    def _add_rectangle(self, parent, x, y, width, height, fill="#000", stroke="#000"):
        """Add rectangle to SVG"""
        return ET.SubElement(parent, 'rect', {
            'x': str(x),
            'y': str(y),
            'width': str(width),
            'height': str(height),
            'fill': fill,
            'stroke': stroke
        })
    
    def generate_simple_pie_chart(self, data, colors, width=400, height=300):
        """Generate a simple pie chart SVG"""
        if not data:
            return self._generate_no_data_svg(width, height)
        
        svg = self._create_svg(width, height)
        center_x, center_y = width // 2, height // 2
        radius = min(width, height) // 3
        
        # Calculate total and angles
        total = sum(item.get('population', 0) for item in data.values() if isinstance(item, dict))
        if total == 0:
            return self._generate_no_data_svg(width, height)
        
        start_angle = 0
        legend_y = 20
        
        for i, (key, item) in enumerate(data.items()):
            if not isinstance(item, dict) or item.get('population', 0) == 0:
                continue
                
            population = item['population']
            angle = (population / total) * 360
            color = colors.get(key, '#cccccc')
            
            # Draw pie slice (simplified)
            if angle > 0:
                self._draw_pie_slice(svg, center_x, center_y, radius, start_angle, angle, color)
                
                # Add legend
                self._add_rectangle(svg, 10, legend_y, 15, 15, color)
                label = item.get('name_nepali', key)
                self._add_text(svg, 30, legend_y + 12, f"{label}: {population}", 10)
                legend_y += 20
                
                start_angle += angle
        
        return ET.tostring(svg, encoding='unicode')
    
    def _draw_pie_slice(self, svg, cx, cy, radius, start_angle, angle, color):
        """Draw a pie slice (simplified implementation)"""
        # For simplicity, just draw a circle section - full implementation would need proper arc paths
        circle = ET.SubElement(svg, 'circle', {
            'cx': str(cx),
            'cy': str(cy),
            'r': str(radius),
            'fill': color,
            'stroke': '#fff',
            'stroke-width': '2',
            'opacity': '0.8'
        })
    
    def _generate_no_data_svg(self, width, height):
        """Generate SVG for no data scenario"""
        svg = self._create_svg(width, height)
        self._add_text(svg, width//2, height//2, "कुनै डाटा उपलब्ध छैन", 16, "#666", "middle")
        return ET.tostring(svg, encoding='unicode')


class BaseReportFormatter:
    """Base report formatter with common functionality"""
    
    def __init__(self):
        self.municipality_name = "लुङ्ग्री गाउँपालिका"
    
    def generate_introduction(self, section_name):
        """Generate standard introduction"""
        return f"""{self.municipality_name}मा {section_name}को विविधता रहेको छ । यस गाउँपालिकामा विभिन्न समुदायका मानिसहरूको बसोबास रहेको हुनाले {section_name}गत रुपमा पनि विविधता देखिन्छ । यहाँ प्रस्तुत तथ्याङ्कले {section_name}को वितरणको स्पष्ट चित्र प्रदान गर्छ ।"""
    
    def generate_constitutional_context(self):
        """Generate constitutional context"""
        return """नेपालको संविधान २०७२ ले विविधतामा एकताको सिद्धान्तलाई अपनाएको छ । सबै नागरिकहरूलाई समान अधिकार र अवसर प्रदान गर्ने संवैधानिक व्यवस्था रहेको छ । यस गाउँपालिकामा पनि यही संवैधानिक व्यवस्था अनुरुप सबै समुदायका मानिसहरूले आ-आफ्नो पहिचान कायम राख्दै एकताबद्ध भएर बसोबास गरिरहेका छन् ।"""
    
    def generate_diversity_analysis(self, total_categories, total_population):
        """Generate diversity analysis"""
        return f"""गाउँपालिकामा कुल {total_categories} प्रकारका समुदायहरू बसोबास गर्छन् । कुल {total_population:,} जनसंख्या मध्ये विभिन्न समुदायहरूको उपस्थितिले यस क्षेत्रको सामाजिक विविधतालाई झल्काउँछ । यो विविधता नेपाली समाजको बहुजातीय, बहुसांस्कृतिक विशेषताको प्रतिनिधित्व गर्छ ।"""
    
    def generate_harmony_conclusion(self):
        """Generate harmony and conclusion"""
        return """विभिन्न समुदायका मानिसहरूबीच पारस्परिक सम्मान, सहयोग र सद्भावनापूर्ण सम्बन्ध कायम रहेको छ । सामुदायिक एकता र सामाजिक सद्भावना यस गाउँपालिकाको विशेषता हो । यसले समुदायिक विकास र सामाजिक प्रगतिमा सकारात्मक योगदान पुर्‍याइरहेको छ ।"""


# Color palettes for different demographic categories
DEMOGRAPHIC_COLORS = {
    'religion': {
        'HINDU': '#FF6B35',
        'BUDDHIST': '#F7931E',
        'KIRANT': '#1f77b4',
        'CHRISTIAN': '#2ca02c',
        'ISLAM': '#17becf',
        'NATURE': '#8c564b',
        'BON': '#e377c2',
        'JAIN': '#bcbd22',
        'BAHAI': '#9467bd',
        'SIKH': '#ff7f0e',
        'OTHER': '#7f7f7f'
    },
    'language': {
        'NEPALI': '#1f77b4',
        'LIMBU': '#ff7f0e',
        'RAI': '#2ca02c',
        'HINDI': '#d62728',
        'NEWARI': '#9467bd',
        'SHERPA': '#8c564b',
        'TAMANG': '#e377c2',
        'MAITHILI': '#7f7f7f',
        'BHOJPURI': '#bcbd22',
        'THARU': '#17becf',
        'OTHER': '#aec7e8'
    },
    'caste': {
        'BRAHMIN': '#1f77b4',
        'CHHETRI': '#ff7f0e',
        'MAGAR': '#2ca02c',
        'TAMANG': '#d62728',
        'NEWAR': '#9467bd',
        'THARU': '#8c564b',
        'GURUNG': '#e377c2',
        'RAI': '#7f7f7f',
        'LIMBU': '#bcbd22',
        'SHERPA': '#17becf',
        'DALIT': '#ffbb78',
        'MADHESI': '#98df8a',
        'MUSLIM': '#ff9896',
        'OTHER': '#c5b0d5'
    }
}
