"""
Language Demographics Processor

Handles mother tongue/language demographic data processing, chart generation, and report formatting.
"""

from .base import BaseDemographicsProcessor, BaseChartGenerator, BaseReportFormatter, DEMOGRAPHIC_COLORS
from ..models import MunicipalityWideMotherTonguePopulation, LanguageTypeChoice


class LanguageProcessor(BaseDemographicsProcessor):
    """Processor for language demographics"""
    
    def get_section_title(self):
        return "मातृभाषाको आधारमा जनसंख्या विवरण"
    
    def get_section_number(self):
        return "३.४"
    
    def get_data(self):
        """Get language population data"""
        language_data = {}
        
        # Initialize all languages
        for choice in LanguageTypeChoice.choices:
            language_data[choice[0]] = {
                'code': choice[0],
                'name_nepali': choice[1],
                'population': 0,
                'percentage': 0.0,
            }
        
        # Get actual data from database
        total_population = 0
        for language_obj in MunicipalityWideMotherTonguePopulation.objects.all():
            language_type = language_obj.language_type
            if language_type in language_data:
                language_data[language_type]['population'] = language_obj.population
                total_population += language_obj.population
        
        # Calculate percentages
        if total_population > 0:
            for language_type, data in language_data.items():
                if data['population'] > 0:
                    data['percentage'] = (data['population'] / total_population * 100)
        
        return language_data
    
    def generate_report_content(self, data):
        """Generate language-specific report content"""
        formatter = LanguageReportFormatter()
        return formatter.generate_formal_report(data)
    
    def generate_chart_svg(self, data, chart_type="pie"):
        """Generate language chart SVG"""
        generator = LanguageChartGenerator()
        if chart_type == "pie":
            return generator.generate_pie_chart_svg(data)
        elif chart_type == "bar":
            return generator.generate_bar_chart_svg(data)
        return None


class LanguageChartGenerator(BaseChartGenerator):
    """Language-specific chart generator"""
    
    def generate_pie_chart_svg(self, language_data):
        """Generate language pie chart"""
        colors = DEMOGRAPHIC_COLORS['language']
        return self.generate_simple_pie_chart(language_data, colors)
    
    def generate_bar_chart_svg(self, language_data):
        """Generate language bar chart (placeholder)"""
        return self._generate_no_data_svg(400, 300)


class LanguageReportFormatter(BaseReportFormatter):
    """Language-specific report formatter"""
    
    def generate_formal_report(self, language_data):
        """Generate language formal report content"""
        total_population = sum(data['population'] for data in language_data.values())
        
        # Find major languages
        major_languages = []
        for language_type, data in language_data.items():
            if data['population'] > 0 and data['percentage'] >= 5.0:
                major_languages.append((data['name_nepali'], data['population'], data['percentage']))
        
        major_languages.sort(key=lambda x: x[1], reverse=True)
        
        # Build coherent analysis
        content = []
        
        # Introduction
        content.append(f"""{self.municipality_name}मा भाषिक विविधता रहेको छ । कुल {total_population:,} जनसंख्या मध्ये विभिन्न मातृभाषी समुदायहरूको बसोबास रहेको छ ।""")
        
        # Major languages
        if major_languages:
            major_text = f"""यस गाउँपालिकामा {major_languages[0][0]} मातृभाषी समुदायको संख्या सबैभन्दा बढी छ जसको संख्या {major_languages[0][1]:,} ({major_languages[0][2]:.1f}%) रहेको छ ।"""
            if len(major_languages) > 1:
                major_text += f""" त्यसैगरी {major_languages[1][0]} मातृभाषी समुदायको संख्या {major_languages[1][1]:,} ({major_languages[1][2]:.1f}%) रहेको छ ।"""
            content.append(major_text)
        
        # Constitutional context
        content.append("""नेपालको संविधान २०७२ ले सबै मातृभाषाहरूलाई राष्ट्रिय सम्पदाको रुपमा मान्यता दिएको छ । प्रत्येक समुदायले आफ्नो मातृभाषा बोल्ने, पढ्ने, लेख्ने र संरक्षण गर्ने संवैधानिक अधिकार प्राप्त गरेको छ ।""")
        
        # Diversity analysis
        active_languages = len([d for d in language_data.values() if d['population'] > 0])
        content.append(self.generate_diversity_analysis(active_languages, total_population))
        
        # Language preservation
        content.append("""स्थानीय तहले सबै मातृभाषाहरूको संरक्षण र सम्वर्धनमा विशेष ध्यान दिएको छ । शिक्षाका क्षेत्रमा मातृभाषामा शिक्षा प्रदान गर्ने व्यवस्था मिलाइएको छ । सांस्कृतिक कार्यक्रमहरूमा सबै भाषाहरूको प्रयोग र प्रवर्धनलाई प्रोत्साहन गरिएको छ ।""")
        
        # Conclusion
        content.append(self.generate_harmony_conclusion())
        
        return ' '.join(content)
