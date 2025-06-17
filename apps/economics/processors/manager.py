"""
Economics Manager

Centralized manager for all economics-related data processors in Lungri Rural Municipality.
"""

from .remittance_expenses import RemittanceExpensesProcessor
from .major_skills import MajorSkillsProcessor


class EconomicsManager:
    """Manager for all economics processors"""

    def __init__(self):
        # Initialize all processors
        self.remittance_expenses_processor = RemittanceExpensesProcessor()
        self.major_skills_processor = MajorSkillsProcessor()

        # Registry of all processors
        self.processors = {
            "remittance_expenses": self.remittance_expenses_processor,
            "major_skills": self.major_skills_processor,
        }

    def generate_all_charts(self):
        """Generate all charts for all economics processors"""
        for processor_name, processor in self.processors.items():
            try:
                data = processor.get_data()
                processor.generate_and_save_charts(data)
                print(f"Generated charts for {processor_name}")
            except Exception as e:
                print(f"Error generating charts for {processor_name}: {e}")

    def process_all_for_pdf(self):
        """Process all economics data for PDF generation"""
        pdf_data = {}

        for processor_name, processor in self.processors.items():
            try:
                pdf_data[processor_name] = processor.process_for_pdf()
                print(f"Processed {processor_name} for PDF")
            except Exception as e:
                print(f"Error processing {processor_name} for PDF: {e}")
                pdf_data[processor_name] = {}

        return pdf_data

    def get_remittance_expenses_data(self):
        """Get remittance expenses data"""
        return self.remittance_expenses_processor.process_for_pdf()

    def get_major_skills_data(self):
        """Get major skills data"""
        return self.major_skills_processor.process_for_pdf()

    def get_all_section_data(self):
        """Get all section data for web views"""
        return {
            "remittance_expenses": self.get_remittance_expenses_data(),
            "major_skills": self.get_major_skills_data(),
        }


def get_economics_manager():
    """Get the economics manager instance"""
    return EconomicsManager()
