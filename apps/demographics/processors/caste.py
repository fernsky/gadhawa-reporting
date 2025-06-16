"""
Caste Demographics Processor

Handles caste demographic data processing, chart generation, and report formatting.
"""

from .base import BaseDemographicsProcessor, BaseChartGenerator, BaseReportFormatter, DEMOGRAPHIC_COLORS
from ..models import MunicipalityWideCastePopulation, CasteTypeChoice


class CasteProcessor(BaseDemographicsProcessor):
    """Processor for caste demographics"""
    
    def get_section_title(self):
        return "जातिगत आधारमा जनसंख्या विवरण"
    
    def get_section_number(self):
        return "३.६"
    
    def get_data(self):
        """Get caste population data"""
        caste_data = {}
        
        # Initialize all castes
        for choice in CasteTypeChoice.choices:
            caste_data[choice[0]] = {
                'code': choice[0],
                'name_nepali': choice[1],
                'population': 0,
                'percentage': 0.0,
            }
        
        # Get actual data from database
        total_population = 0
        for caste_obj in MunicipalityWideCastePopulation.objects.all():
            caste_type = caste_obj.caste_type
            if caste_type in caste_data and caste_obj.population:
                caste_data[caste_type]['population'] = caste_obj.population
                total_population += caste_obj.population
        
        # Calculate percentages
        if total_population > 0:
            for caste_type, data in caste_data.items():
                if data['population'] > 0:
                    data['percentage'] = (data['population'] / total_population * 100)
        
        return caste_data
    
    def generate_report_content(self, data):
        """Generate caste-specific report content"""
        formatter = CasteReportFormatter()
        return formatter.generate_formal_report(data)
    
    def generate_chart_svg(self, data, chart_type="pie"):
        """Generate caste chart SVG"""
        generator = CasteChartGenerator()
        if chart_type == "pie":
            return generator.generate_pie_chart_svg(data)
        elif chart_type == "bar":
            return generator.generate_bar_chart_svg(data)
        return None


class CasteChartGenerator(BaseChartGenerator):
    """Caste-specific chart generator"""
    
    def generate_pie_chart_svg(self, caste_data):
        """Generate caste pie chart"""
        colors = DEMOGRAPHIC_COLORS['caste']
        return self.generate_simple_pie_chart(caste_data, colors)
    
    def generate_bar_chart_svg(self, caste_data):
        """Generate caste bar chart (placeholder)"""
        return self._generate_no_data_svg(400, 300)


class CasteReportFormatter(BaseReportFormatter):
    """Caste-specific report formatter"""
    
    def generate_formal_report(self, caste_data):
        """Generate caste formal report content"""
        total_population = sum(data['population'] for data in caste_data.values())
        
        # Find major castes
        major_castes = []
        for caste_type, data in caste_data.items():
            if data['population'] > 0 and data['percentage'] >= 3.0:  # Lower threshold for caste
                major_castes.append((data['name_nepali'], data['population'], data['percentage']))
        
        major_castes.sort(key=lambda x: x[1], reverse=True)
        
        # Build coherent analysis
        content = []
        
        # Introduction
        content.append(f"""{self.municipality_name}मा जातीय विविधता रहेको छ । कुल {total_population:,} जनसंख्या मध्ये विभिन्न जातजातिका मानिसहरूको बसोबास रहेको छ ।""")
        
        # Major castes
        if major_castes:
            major_text = f"""यस गाउँपालिकामा {major_castes[0][0]} जातिको संख्या सबैभन्दा बढी छ जसको संख्या {major_castes[0][1]:,} ({major_castes[0][2]:.1f}%) रहेको छ ।"""
            if len(major_castes) > 1:
                major_text += f""" त्यसैगरी {major_castes[1][0]} जातिको संख्या {major_castes[1][1]:,} ({major_castes[1][2]:.1f}%) रहेको छ ।"""
            content.append(major_text)
        
        # Constitutional context
        content.append("""नेपालको संविधान २०७२ ले जातीय छुवाछूत र भेदभावको अन्त्य गर्ने संकल्प गरेको छ । समानुपातिक समावेशी र सहभागितामूलक सिद्धान्तका आधारमा समतामूलक समाजको निर्माण गर्ने नीति अपनाइएको छ । सबै जातजातिका नागरिकहरूलाई समान अधिकार र अवसर प्रदान गर्ने व्यवस्था छ ।""")
        
        # Diversity analysis
        active_castes = len([d for d in caste_data.values() if d['population'] > 0])
        content.append(self.generate_diversity_analysis(active_castes, total_population))
        
        # Social inclusion
        content.append("""स्थानीय तहले सबै जातजातिका नागरिकहरूको सामाजिक, आर्थिक र राजनीतिक सशक्तिकरणमा विशेष ध्यान दिएको छ । समावेशी विकासका कार्यक्रमहरू सञ्चालन गरी सबै वर्गका मानिसहरूलाई मुख्य धारामा ल्याउने प्रयास गरिएको छ । जातीय एकता र सामाजिक सद्भावना कायम राख्न समुदायिक संवाद र सहकार्यलाई प्रोत्साहन गरिएको छ ।""")
        
        # Conclusion
        content.append(self.generate_harmony_conclusion())
        
        return ' '.join(content)
