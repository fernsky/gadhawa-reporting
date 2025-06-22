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
from .ward_settlement import WardSettlementProcessor
from .ward_household import WardHouseholdProcessor
from .demographic_summary import DemographicSummaryProcessor
from .age_gender import AgeGenderProcessor
from .female_property_ownership import FemalePropertyOwnershipProcessor
from .disability_cause import DisabilityCauseProcessor


class DemographicsManager:
    """Manager for all demographic processors"""

    def __init__(self):
        self.processors = {
            "demographic_summary": DemographicSummaryProcessor(),
            "ward_settlement": WardSettlementProcessor(),
            "ward_household": WardHouseholdProcessor(),
            "age_gender": AgeGenderProcessor(),
            "religion": ReligionProcessor(),
            "language": LanguageProcessor(),
            "caste": CasteProcessor(),
            "househead": HouseheadProcessor(),
            "occupation": OccupationProcessor(),
            "economically_active": EconomicallyActiveProcessor(),
            "female_property_ownership": FemalePropertyOwnershipProcessor(),
            "disability_cause": DisabilityCauseProcessor(),
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
        """Generate and save charts only if they don't exist using simple chart management"""
        chart_urls = {}

        for category, processor in self.processors.items():
            print(f"\n📊 Processing charts for {category}...")

            # Check if processor supports chart management
            if hasattr(processor, "needs_generation") and hasattr(
                processor, "generate_and_track_charts"
            ):
                # Get data first to check what charts are needed
                data = processor.get_data()
                charts_needed = []

                # Check what chart types this processor supports
                chart_types = ["pie", "bar"]  # Most processors support these

                for chart_type in chart_types:
                    if processor.needs_generation(chart_type):
                        charts_needed.append(chart_type)
                        print(f"  📈 {chart_type} chart needs generation")
                    else:
                        print(f"  ✓ {chart_type} chart already exists")

                # Generate only needed charts
                if charts_needed:
                    print(f"  🎨 Generating {len(charts_needed)} charts...")
                    charts = processor.generate_and_track_charts(data)
                else:
                    # Get existing chart URLs
                    charts = {}
                    for chart_type in chart_types:
                        url = processor.get_chart_url(chart_type)
                        if url:
                            chart_key = f"{chart_type}_chart_url"
                            charts[chart_key] = url
                    print(f"  ✓ Using existing charts")

            elif hasattr(processor, "generate_and_save_charts"):
                # Fallback to original method for processors without chart management
                print(f"  📈 Using fallback chart generation...")
                data = processor.get_data()
                charts = processor.generate_and_save_charts(data)
            else:
                print(f"  ⚠ No chart generation method available")
                charts = {}

            chart_urls[category] = charts

        print(f"\n✅ Chart generation completed for all categories")
        return chart_urls

    def get_available_categories(self):
        """Get list of available demographic categories"""
        return list(self.processors.keys())

    def get_combined_report_content(self):
        """Get combined report content for all categories"""
        all_data = self.process_all_for_pdf()
        combined_content = []

        # Introduction
        combined_content.append(
            """लुङ्ग्री गाउँपालिकामा जनसांख्यिकीय विविधताको स्पष्ट चित्र देखिन्छ । विभिन्न धर्म, मातृभाषा र जातजातिका मानिसहरूको बसोबास रहेको यस गाउँपालिकाले नेपाली समाजको बहुआयामिक विशेषताहरूको प्रतिनिधित्व गर्छ ।"""
        )

        # Add each category's content
        for category, processed_data in all_data.items():
            if processed_data and "report_content" in processed_data:
                combined_content.append(processed_data["report_content"])

        # Overall conclusion
        combined_content.append(
            """

समग्रमा, यस गाउँपालिकामा रहेको जनसांख्यिकीय विविधता नेपाली समाजको समृद्ध सांस्कृतिक परम्पराको झलक हो । विभिन्न समुदायहरूबीचको सद्भावना र एकताले यस क्षेत्रको सामाजिक स्थिरता र विकासमा महत्वपूर्ण योगदान पुर्‍याइरहेको छ । घरमुखियाको लिङ्गीय वितरणले लिङ्गीय समानताको दिशामा प्रगति भएको संकेत गर्छ ।"""
        )

        return " ".join(combined_content)


# Convenience function for easy access
def get_demographics_manager():
    """Get configured demographics manager instance"""
    return DemographicsManager()
