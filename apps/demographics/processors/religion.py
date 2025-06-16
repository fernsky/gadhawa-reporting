"""
Religion Demographics Processor

Handles religion demographic data processing, chart generation, and report formatting.
"""

from .base import BaseDemographicsProcessor, BaseChartGenerator, BaseReportFormatter, DEMOGRAPHIC_COLORS
from ..models import MunicipalityWideReligionPopulation, ReligionTypeChoice


class ReligionProcessor(BaseDemographicsProcessor):
    """Processor for religion demographics"""
    
    def get_section_title(self):
        return "धर्म अनुसार जनसंख्याको विवरण"
    
    def get_section_number(self):
        return "३.५"
    
    def get_data(self):
        """Get religion population data"""
        religion_data = {}
        
        # Initialize all religions
        for choice in ReligionTypeChoice.choices:
            religion_data[choice[0]] = {
                'code': choice[0],
                'name_nepali': choice[1],
                'population': 0,
                'percentage': 0.0,
            }
        
        # Get actual data from database
        total_population = 0
        for religion_obj in MunicipalityWideReligionPopulation.objects.all():
            religion_type = religion_obj.religion_type
            if religion_type in religion_data:
                religion_data[religion_type]['population'] = religion_obj.population
                total_population += religion_obj.population
        
        # Calculate percentages
        if total_population > 0:
            for religion_type, data in religion_data.items():
                if data['population'] > 0:
                    data['percentage'] = (data['population'] / total_population * 100)
        
        return religion_data
    
    def generate_report_content(self, data):
        """Generate religion-specific report content"""
        formatter = ReligionReportFormatter()
        return formatter.generate_formal_report(data)
    
    def generate_chart_svg(self, data, chart_type="pie"):
        """Generate religion chart SVG"""
        generator = ReligionChartGenerator()
        if chart_type == "pie":
            return generator.generate_pie_chart_svg(data)
        elif chart_type == "bar":
            return generator.generate_bar_chart_svg(data)
        return None


class ReligionChartGenerator(BaseChartGenerator):
    """Religion-specific chart generator"""
    
    def generate_pie_chart_svg(self, religion_data):
        """Generate religion pie chart"""
        colors = DEMOGRAPHIC_COLORS['religion']
        return self.generate_simple_pie_chart(religion_data, colors)
    
    def generate_bar_chart_svg(self, religion_data):
        """Generate religion bar chart (placeholder)"""
        return self._generate_no_data_svg(400, 300)


class ReligionReportFormatter(BaseReportFormatter):
    """Religion-specific report formatter"""
    
    def generate_formal_report(self, religion_data):
        """Generate religion formal report content"""
        total_population = sum(data['population'] for data in religion_data.values())
        
        # Find major religions
        major_religions = []
        for religion_type, data in religion_data.items():
            if data['population'] > 0 and data['percentage'] >= 5.0:
                major_religions.append((data['name_nepali'], data['population'], data['percentage']))
        
        major_religions.sort(key=lambda x: x[1], reverse=True)
        
        # Build coherent analysis
        content = []
        
        # Introduction
        content.append(f"""{self.municipality_name}मा धार्मिक विविधता रहेको छ । कुल {total_population:,} जनसंख्या मध्ये विभिन्न धर्मावलम्बीहरूको बसोबास रहेको छ ।""")
        
        # Major religions
        if major_religions:
            major_text = f"""यस गाउँपालिकामा {major_religions[0][0]} धर्मावलम्बीहरूको संख्या सबैभन्दा बढी छ जसको संख्या {major_religions[0][1]:,} ({major_religions[0][2]:.1f}%) रहेको छ ।"""
            if len(major_religions) > 1:
                major_text += f""" त्यसैगरी {major_religions[1][0]} धर्मावलम्बीहरूको संख्या {major_religions[1][1]:,} ({major_religions[1][2]:.1f}%) रहेको छ ।"""
            content.append(major_text)
        
        # Constitutional context
        content.append(self.generate_constitutional_context())
        
        # Diversity analysis
        active_religions = len([d for d in religion_data.values() if d['population'] > 0])
        content.append(self.generate_diversity_analysis(active_religions, total_population))
        
        # Religious harmony
        content.append("""गाउँपालिकामा धार्मिक सामाजिक सद्भावना र एकताको उदाहरणीय अवस्था रहेको छ । विभिन्न धर्मका मानिसहरूबीच पारस्परिक सम्मान, सहयोग र मित्रतापूर्ण सम्बन्ध कायम रहेको छ । धार्मिक पर्वहरूमा सबै समुदायको सहभागिता रहने गर्छ जसले सामुदायिक एकताको परिचय दिन्छ ।""")
        
        # Conclusion
        content.append(self.generate_harmony_conclusion())
        
        return ' '.join(content)
