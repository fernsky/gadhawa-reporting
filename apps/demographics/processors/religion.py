"""
Religion Demographics Processor

Handles religion demographic data processing, chart generation, and report formatting.
"""

from .base import BaseDemographicsProcessor, BaseReportFormatter
from ..models import MunicipalityWideReligionPopulation, ReligionTypeChoice
from ..utils.svg_chart_generator import RELIGION_COLORS
from apps.reports.utils.nepali_numbers import format_nepali_number, format_nepali_percentage


class ReligionProcessor(BaseDemographicsProcessor):
    """Processor for religion demographics"""
    
    def __init__(self):
        super().__init__()
        # Customize chart dimensions for religion
        self.pie_chart_width = 900
        self.pie_chart_height = 450
        self.chart_radius = 130
        # Set religion-specific colors
        self.chart_generator.colors = RELIGION_COLORS
    
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
                'population': 0,
                'percentage': 0.0,
                'name_nepali': choice[1],
            }

        # Get actual data from database
        total_population = 0
        for religion_obj in MunicipalityWideReligionPopulation.objects.all():
            religion = religion_obj.religion  # Correct attribute based on models.py
            if religion in religion_data:
                religion_data[religion]['population'] += religion_obj.population
                total_population += religion_obj.population

        # Calculate percentages
        if total_population > 0:
            for religion, data in religion_data.items():
                data['percentage'] = round((data['population'] / total_population) * 100, 2)

        return religion_data
    
    def generate_report_content(self, data):
        """Generate religion-specific report content"""
        formatter = self.ReligionReportFormatter()
        return formatter.generate_formal_report(data)
    
    def generate_chart_svg(self, data, chart_type="pie"):
        """Generate religion chart SVG using SVGChartGenerator"""
        if chart_type == "pie":
            return self.chart_generator.generate_pie_chart_svg(
                data, 
                include_title=False,
                title_nepali="धर्म अनुसार जनसंख्या वितरण",
                title_english="Population Distribution by Religion"
            )
        elif chart_type == "bar":
            return self.chart_generator.generate_bar_chart_svg(
                data, 
                include_title=False,
                title_nepali="वडा अनुसार धार्मिक जनसंख्या वितरण",
                title_english="Religious Population by Ward"
            )
        return None

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
            nepali_total = format_nepali_number(total_population)
            content.append(f"""{self.municipality_name}मा धार्मिक विविधता रहेको छ । कुल {nepali_total} जनसंख्या मध्ये विभिन्न धर्मावलम्बीहरूको बसोबास रहेको छ ।""")
            
            # Major religions
            if major_religions:
                major_pop = format_nepali_number(major_religions[0][1])
                major_pct = format_nepali_percentage(major_religions[0][2])
                major_text = f"""यस गाउँपालिकामा {major_religions[0][0]} धर्मावलम्बीहरूको संख्या सबैभन्दा बढी छ जसको संख्या {major_pop} ({major_pct}) रहेको छ ।"""
                if len(major_religions) > 1:
                    second_pop = format_nepali_number(major_religions[1][1])
                    second_pct = format_nepali_percentage(major_religions[1][2])
                    major_text += f""" त्यसैगरी {major_religions[1][0]} धर्मावलम्बीहरूको संख्या {second_pop} ({second_pct}) रहेको छ ।"""
                content.append(major_text)
            
            # Constitutional context
            content.append("""नेपालको संविधान २०७२ ले धर्मिक स्वतन्त्रताको ग्यारेन्टी गरेको छ । सबै नागरिकहरूलाई आफ्नो धर्म मान्ने, त्यसको प्रचार प्रसार गर्ने र धार्मिक क्रियाकलाप गर्ने अधिकार छ । धर्मनिरपेक्षताको सिद्धान्त अनुसार राज्यले कुनै पनि धर्मलाई राज्य धर्मको रूपमा स्थापना गर्दैन ।""")
            
            # Diversity analysis
            active_religions = len([d for d in religion_data.values() if d['population'] > 0])
            content.append(self.generate_diversity_analysis(active_religions, total_population))
            
            # Religious harmony
            content.append("""स्थानीय तहले सबै धर्मावलम्बीहरूको धार्मिक स्वतन्त्रता र अधिकारको संरक्षणमा विशेष ध्यान दिएको छ । धार्मिक सद्भावना र पारस्परिक सहिष्णुताको वातावरण निर्माण गरी सबै समुदायहरूबीच मेलमिलापको भावना विकास गर्न कार्यक्रमहरू सञ्चालन गरिएको छ । धार्मिक पर्वहरूमा सबै समुदायको सहभागिता र सहयोगले सामाजिक एकताको परिचय दिन्छ ।""")
            
            # Conclusion
            content.append(self.generate_harmony_conclusion())
            
            return ' '.join(content)
