"""
Demographics Manager

Coordinates all demographic processors and provides unified interface for PDF generation.
"""

from .religion import ReligionProcessor
from .language import LanguageProcessor
from .caste import CasteProcessor


class DemographicsManager:
    """Manager for all demographic processors"""
    
    def __init__(self):
        self.processors = {
            'religion': ReligionProcessor(),
            'language': LanguageProcessor(),
            'caste': CasteProcessor(),
            # Add more processors here as needed
        }
    
    def get_processor(self, category):
        """Get processor for specific category"""
        return self.processors.get(category)
    
    def process_all_for_pdf(self):
        """Process all demographic categories for PDF generation"""
        results = {}
        
        for category, processor in self.processors.items():
            try:
                results[category] = processor.process_for_pdf()
            except Exception as e:
                print(f"Error processing {category}: {e}")
                results[category] = {
                    'data': {},
                    'report_content': f"डाटा प्रशोधनमा समस्या: {category}",
                    'charts': {'pie_chart': None, 'bar_chart': None},
                    'section_title': f"{category} विवरण",
                    'section_number': "३.X",
                    'total_population': 0,
                    'summary_stats': {}
                }
        
        return results
    
    def process_category_for_pdf(self, category):
        """Process specific category for PDF"""
        processor = self.get_processor(category)
        if processor:
            return processor.process_for_pdf()
        return None
    
    def get_available_categories(self):
        """Get list of available demographic categories"""
        return list(self.processors.keys())
    
    def get_combined_report_content(self):
        """Get combined report content for all categories"""
        all_data = self.process_all_for_pdf()
        
        combined_content = []
        
        # Introduction
        combined_content.append("""लुङ्ग्री गाउँपालिकामा जनसांख्यिकीय विविधताको स्पष्ट चित्र देखिन्छ । विभिन्न धर्म, मातृभाषा र जातजातिका मानिसहरूको बसोबास रहेको यस गाउँपालिकाले नेपाली समाजको बहुआयामिक विशेषताहरूको प्रतिनिधित्व गर्छ ।""")
        
        # Add each category's content
        for category, data in all_data.items():
            if data.get('report_content'):
                section_header = f"""\n\n{data.get('section_number', '३.X')} {data.get('section_title', 'विवरण')}\n"""
                combined_content.append(section_header)
                combined_content.append(data['report_content'])
        
        # Overall conclusion
        combined_content.append("""\n\nसमग्रमा, यस गाउँपालिकामा रहेको जनसांख्यिकीय विविधता नेपाली समाजको समृद्ध सांस्कृतिक परम्पराको झलक हो । विभिन्न समुदायहरूबीचको सद्भावना र एकताले यस क्षेत्रको सामाजिक स्थिरता र विकासमा महत्वपूर्ण योगदान पुर्‍याइरहेको छ ।""")
        
        return ' '.join(combined_content)


# Convenience function for easy access
def get_demographics_manager():
    """Get configured demographics manager instance"""
    return DemographicsManager()
