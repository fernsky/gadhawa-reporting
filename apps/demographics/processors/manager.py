"""
Demographics Manager

Coordinates all demographic processors and provides unified interface for PDF generation.
"""

from .religion import ReligionProcessor
from .language import LanguageProcessor
from .caste import CasteProcessor
from .househead import HouseheadProcessor
from .occupation import OccupationProcessor
from .economically_active import EconomicallyActiveProcessor
from .occupation import OccupationProcessor


class DemographicsManager:
    """Manager for all demographic processors"""
    
    def __init__(self):
        self.processors = {
            'religion': ReligionProcessor(),
            'language': LanguageProcessor(),
            'caste': CasteProcessor(),
            'househead': HouseheadProcessor(),
            'occupation': OccupationProcessor(),
            'economically_active': EconomicallyActiveProcessor(),
        }

    def get_processor(self, category):
        """Get processor for specific category"""
        return self.processors.get(category)

    def process_all_for_pdf(self):
        """Process all demographic categories for PDF generation with charts"""
        results = {}
        for category, processor in self.processors.items():
            results[category] = processor.process_for_pdf()
        return results

    def process_category_for_pdf(self, category):
        """Process specific category for PDF with charts"""
        processor = self.get_processor(category)
        if processor:
            return processor.process_for_pdf()
        return None

    def generate_all_charts(self):
        """Generate and save all charts for all categories"""
        chart_urls = {}
        for category, processor in self.processors.items():
            data = processor.get_data()
            charts = processor.generate_and_save_charts(data)
            chart_urls[category] = charts
        return chart_urls

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
        for category, processed_data in all_data.items():
            if processed_data and 'report_content' in processed_data:
                combined_content.append(processed_data['report_content'])

        # Overall conclusion
        combined_content.append("""

समग्रमा, यस गाउँपालिकामा रहेको जनसांख्यिकीय विविधता नेपाली समाजको समृद्ध सांस्कृतिक परम्पराको झलक हो । विभिन्न समुदायहरूबीचको सद्भावना र एकताले यस क्षेत्रको सामाजिक स्थिरता र विकासमा महत्वपूर्ण योगदान पुर्‍याइरहेको छ । घरमुखियाको लिङ्गीय वितरणले लिङ्गीय समानताको दिशामा प्रगति भएको संकेत गर्छ ।""")

        return ' '.join(combined_content)


# Convenience function for easy access
def get_demographics_manager():
    """Get configured demographics manager instance"""
    return DemographicsManager()
