"""
Ward Settlement Demographics Processor

Handles ward settlement data processing and report formatting.
"""

from pathlib import Path
from .base import BaseDemographicsProcessor, BaseReportFormatter
from ..models import WardSettlement
from apps.reports.utils.nepali_numbers import format_nepali_number


class WardSettlementProcessor(BaseDemographicsProcessor):
    """Processor for ward settlement demographics"""

    def __init__(self):
        super().__init__()
        # No charts needed for this processor

    def get_section_title(self):
        return "मुख्य बस्ती र घरपरिवारको विवरण"

    def get_section_number(self):
        return "३.१"

    def get_subsection_title(self):
        return "मुख्य बस्ती"

    def get_subsection_number(self):
        return "३.१.१"

    def get_data(self):
        """Get ward settlement data"""
        ward_data = {}

        # Get all ward settlement data
        for ward_settlement in WardSettlement.objects.all().order_by("ward_number"):
            ward_data[ward_settlement.ward_number] = {
                "ward_number": ward_settlement.ward_number,
                "settlement_areas": ward_settlement.settlement_areas,
                "settlement_count": (
                    len(ward_settlement.settlement_areas)
                    if ward_settlement.settlement_areas
                    else 0
                ),
            }

        # Calculate total settlements
        total_settlements = sum(
            len(data["settlement_areas"]) if data["settlement_areas"] else 0
            for data in ward_data.values()
        )

        return {
            "ward_data": ward_data,
            "total_settlements": total_settlements,
            "total_wards": len(ward_data),
        }

    def generate_report_content(self, data):
        """Generate ward settlement-specific report content"""
        formatter = self.WardSettlementReportFormatter()
        return formatter.generate_formal_report(data)

    def generate_chart_svg(self, data, chart_type="pie"):
        """Ward settlement doesn't need charts"""
        return None

    def generate_and_save_charts(self, data):
        """Ward settlement doesn't need charts"""
        return {}

    def process_for_pdf(self):
        """Process ward settlement data for PDF generation without charts"""
        # Get raw data
        data = self.get_data()

        # Generate report content
        report_content = self.generate_report_content(data)

        # No charts needed for ward settlement
        charts = {}

        # Calculate totals for summary
        total_settlements = data.get("total_settlements", 0)
        total_wards = data.get("total_wards", 0)

        return {
            "data": data,
            "report_content": report_content,
            "charts": charts,
            "total_settlements": total_settlements,
            "total_wards": total_wards,
            "section_title": self.get_section_title(),
            "section_number": self.get_section_number(),
            "subsection_title": self.get_subsection_title(),
            "subsection_number": self.get_subsection_number(),
        }

    class WardSettlementReportFormatter(BaseReportFormatter):
        """Formatter for ward settlement reports"""

        def generate_formal_report(self, data):
            """Generate formal ward settlement report"""

            # Analysis text as provided
            analysis_text = """यस गाउँपालिकामा पहाडी क्षेत्रका साना र ठूला बस्ती गरी ९४ भन्दा बढी मुख्य वस्तीहरु रहेका छन् भने घर निर्माण शैली परम्परागत रहेको छ । यस क्षेत्रमा मुख्यतया न्यानो समशितोष्ण देखी ठण्डा समशितोष्ण सम्मको हावापानी भएतापनि आर्थिक रुपमा कृषि र पशुपालनमा राम्रो सम्भावना रहेका कारण बसोबासका लागि मानिसहरुको रोजाइको क्षेत्र पर्दछ । तथापी सेवा, सुविधा तथा अवसरको उपलब्धताका कारण विकटमा रहेका गाउँवाट र अन्य जिल्लाहरुका बजार क्षेत्रमा बसाँइसराई गरेको पाइन्छ ।

गाउँपालिकाका विभिन्न क्षेत्रहरूको व्यवस्थित तवरले विकास गर्न प्रत्येक बस्तीहरुमा आवत जावत गर्न मोटर बाटो, खुल्ला क्षेत्रको प्रावधान, लगायत भौतिक तथा पूर्वाधारको निर्माण सहितको व्यवस्थित बस्तीको विकास गर्न जग्गा एकीकरण वा सेवा सुविधा जस्ता कार्यक्रमहरू संचालन गर्नुपर्दछ । यसरी जग्गा विकास कार्यक्रम संचालन गर्दा बजार क्षेत्र विस्तार प्रस्तावना गरिएका क्षेत्रहरूलाई टेवा पु¥याउने हिसाबले प्राथमिकता दिनुपर्दछ ।"""

            ward_data = data.get("ward_data", {})
            total_settlements = data.get("total_settlements", 0)
            total_wards = data.get("total_wards", 0)

            # Generate summary
            summary = f"""लुङ्ग्री गाउँपालिकामा कुल {format_nepali_number(total_wards)} वडामा {format_nepali_number(total_settlements)} भन्दा बढी मुख्य बस्तीहरु रहेका छन् । """

            # Combine analysis and summary
            report = f"{summary}\n\n{analysis_text}"

            return {
                "coherent_analysis": report,
                "ward_data": ward_data,
                "total_settlements": total_settlements,
                "total_wards": total_wards,
            }
