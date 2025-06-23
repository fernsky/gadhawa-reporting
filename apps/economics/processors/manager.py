"""
Economics Manager

Coordinates all economics processors and provides unified interface for PDF generation.
"""

from .remittance_expenses import RemittanceExpensesProcessor
from .major_skills import MajorSkillsProcessor
from .wardwise_house_ownership import WardWiseHouseOwnershipProcessor
from .wardwise_house_base import WardWiseHouseBaseProcessor
from .wardwise_house_outer_wall import WardWiseHouseOuterWallProcessor
from .municipality_wide_foreign_employment_countries import (
    MunicipalityWideForeignEmploymentCountriesProcessor,
)
from .remittance_amount_group import RemittanceAmountGroupProcessor


class EconomicsManager:
    """Manager for all economics processors"""

    def __init__(self):
        self.processors = {
            "remittance_expenses": RemittanceExpensesProcessor(),
            "major_skills": MajorSkillsProcessor(),
            "wardwise_house_ownership": WardWiseHouseOwnershipProcessor(),
            "wardwise_house_base": WardWiseHouseBaseProcessor(),
            "wardwise_house_outer_wall": WardWiseHouseOuterWallProcessor(),
            "municipality_wide_foreign_employment_countries": MunicipalityWideForeignEmploymentCountriesProcessor(),
            "remittance_amount_group": RemittanceAmountGroupProcessor(),
        }

    def get_processor(self, category):
        """Get processor for specific category"""
        return self.processors.get(category)

    def process_all_for_pdf(self):
        """Process all economics categories for PDF generation with charts"""
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
        """Get list of available economics categories"""
        return list(self.processors.keys())

    def get_combined_report_content(self):
        """Get combined report content for all categories"""
        all_data = self.process_all_for_pdf()
        combined_content = []

        # Introduction
        combined_content.append(
            """गढवा गाउँपालिकामा आर्थिक क्रियाकलापहरूको स्पष्ट चित्र देखिन्छ । विभिन्न आर्थिक क्षेत्रहरूमा स्थानीय जनताको सहभागिता र रेमिटेन्स खर्चको ढाँचाले गाउँपालिकाको आर्थिक संरचनाको प्रतिनिधित्व गर्छ ।"""
        )

        # Add each category's content
        for category, processed_data in all_data.items():
            if processed_data and "report_content" in processed_data:
                combined_content.append(processed_data["report_content"])

        # Overall conclusion
        combined_content.append(
            """

समग्रमा, यस गाउँपालिकामा रहेको आर्थिक विविधता नेपाली ग्रामीण अर्थतन्त्रको समृद्ध परम्पराको झलक हो । विभिन्न आर्थिक क्षेत्रहरूबीचको सहकार्य र एकताले यस क्षेत्रको आर्थिक स्थिरता र विकासमा महत्वपूर्ण योगदान पुर्‍याइरहेको छ । रेमिटेन्स खर्चको ढाँचाले आर्थिक प्राथमिकता र भविष्यको दिशाको संकेत गर्छ ।"""
        )

        return " ".join(combined_content)


# Convenience function for easy access
def get_economics_manager():
    """Get configured economics manager instance"""
    return EconomicsManager()
