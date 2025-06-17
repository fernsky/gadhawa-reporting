"""
Infrastructure Manager

Coordinates all infrastructure processors and provides unified interface for PDF generation.
"""

from .public_transport import PublicTransportProcessor
from .market_center_time import MarketCenterTimeProcessor
from .road_status import RoadStatusProcessor


class InfrastructureManager:
    """Manager for all infrastructure processors"""

    def __init__(self):
        self.processors = {
            "public_transport": PublicTransportProcessor(),
            "market_center_time": MarketCenterTimeProcessor(),
            "road_status": RoadStatusProcessor(),
        }

    def get_processor(self, category):
        """Get processor for specific category"""
        return self.processors.get(category)

    def process_all_for_pdf(self):
        """Process all infrastructure categories for PDF generation with charts"""
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
        """Get list of available infrastructure categories"""
        return list(self.processors.keys())

    def get_category_titles(self):
        """Get mapping of category keys to their titles"""
        titles = {}
        for category, processor in self.processors.items():
            titles[category] = {
                "section_number": processor.get_section_number(),
                "title": processor.get_section_title(),
            }
        return titles


def get_infrastructure_manager():
    """Factory function to get infrastructure manager instance"""
    return InfrastructureManager()
