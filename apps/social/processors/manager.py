"""
Social Manager

Coordinates all social processors and provides unified interface for PDF generation.
"""

from .toilet_type import ToiletTypeProcessor
from .solid_waste_management import SolidWasteManagementProcessor
from .old_age_and_single_women import OldAgeAndSingleWomenProcessor
from .major_subject import MajorSubjectProcessor
from .literacy_status import LiteracyStatusProcessor
from .school_dropout import SchoolDropoutProcessor
from .educational_institution import EducationalInstitutionProcessor
from .teacher_staffing import TeacherStaffingProcessor


class SocialManager:
    """Manager for all social processors"""

    def __init__(self):
        self.processors = {
            "literacy_status": LiteracyStatusProcessor(),
            "educational_institution": EducationalInstitutionProcessor(),
            "teacher_staffing": TeacherStaffingProcessor(),
            "major_subject": MajorSubjectProcessor(),
            "school_dropout": SchoolDropoutProcessor(),
            "toilet_type": ToiletTypeProcessor(),
            "solid_waste_management": SolidWasteManagementProcessor(),
            "old_age_and_single_women": OldAgeAndSingleWomenProcessor(),
        }

    def get_processor(self, category):
        """Get processor for specific category"""
        return self.processors.get(category)

    def process_all_for_pdf(self):
        """Process all social categories for PDF generation with charts"""
        results = {}
        for category, processor in self.processors.items():
            try:
                results[category] = processor.process_for_pdf()
            except Exception as e:
                print(f"Error processing {category} for PDF: {e}")
                results[category] = {
                    "data": {},
                    "municipality_data": {},
                    "ward_data": {},
                    "total_population": 0,
                    "report_content": f"Error processing {category} data",
                    "charts": {},
                }
        return results

    def process_category_for_pdf(self, category):
        """Process specific category for PDF with charts"""
        processor = self.get_processor(category)
        if processor:
            try:
                return processor.process_for_pdf()
            except Exception as e:
                print(f"Error processing {category} for PDF: {e}")
                return {
                    "data": {},
                    "municipality_data": {},
                    "ward_data": {},
                    "total_population": 0,
                    "report_content": f"Error processing {category} data",
                    "charts": {},
                }
        return None

    def generate_all_charts(self):
        """Generate and save all charts for all categories"""
        chart_urls = {}
        for category, processor in self.processors.items():
            try:
                data = processor.get_data()
                charts = processor.generate_and_save_charts(data)
                chart_urls[category] = charts
            except Exception as e:
                print(f"Error generating charts for {category}: {e}")
                chart_urls[category] = {}
        return chart_urls

    def get_available_categories(self):
        """Get list of available social categories"""
        return list(self.processors.keys())

    def get_combined_report_content(self):
        """Get combined report content for all social categories"""
        all_data = self.process_all_for_pdf()

        return {
            "all_social_data": all_data,
            "available_categories": self.get_available_categories(),
            "combined_analysis": self._generate_combined_analysis(all_data),
        }

    def _generate_combined_analysis(self, all_data):
        """Generate combined analysis for all social categories"""
        total_coverage = 0
        categories_with_data = 0

        for category, data in all_data.items():
            if data.get("total_population", 0) > 0:
                categories_with_data += 1
                total_coverage += data.get("total_population", 0)

        return f"""लुङ्ग्री गाउँपालिकाको सामाजिक क्षेत्रको समग्र विश्लेषणले देखाउँछ कि {categories_with_data} वटा मुख्य सामाजिक सूचकहरूमा व्यापक डाटा उपलब्ध छ । 
        यी सूचकहरूले गाउँपालिकाको सामाजिक विकासको स्थिति, चुनौतीहरू र सम्भावनाहरूको स्पष्ट चित्र प्रस्तुत गर्छन् । 
        शिक्षा, स्वास्थ्य, खानेपानी तथा सरसफाई, र महिला तथा बालबालिकाको अवस्थाले समग्र सामाजिक कल्याणको स्तर निर्धारण गर्छ ।"""


def get_social_manager():
    """Factory function to get SocialManager instance"""
    return SocialManager()
