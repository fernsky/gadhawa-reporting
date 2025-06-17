"""
Social Manager

Coordinates all social processors and provides unified interface for PDF generation.
"""

from .toilet_type import ToiletTypeProcessor
from .solid_waste_management import SolidWasteManagementProcessor
from .old_age_and_single_women import OldAgeAndSingleWomenProcessor
from .major_subject import MajorSubjectProcessor
from .literacy_status import LiteracyStatusProcessor


class SocialManager:
    """Manager for all social processors"""

    def __init__(self):
        self.processors = {
            "toilet_type": ToiletTypeProcessor(),
            "solid_waste_management": SolidWasteManagementProcessor(),
            "old_age_and_single_women": OldAgeAndSingleWomenProcessor(),
            "major_subject": MajorSubjectProcessor(),
            "literacy_status": LiteracyStatusProcessor(),
        }

    def get_processor(self, category):
        """Get processor for specific category"""
        return self.processors.get(category)

    def process_all_for_pdf(self):
        """Process all social categories for PDF generation with charts"""
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


def get_social_manager():
    """Factory function to get SocialManager instance"""
    return SocialManager()
