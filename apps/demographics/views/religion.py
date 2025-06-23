"""
Religion Demographics Views for Gadhawa Rural Municipality

This module provides views for religion-based population analysis including:
- Ward-wise religion distribution
- Religion population summaries
- Dynamic chart generation
- Formal report content generation
- Detailed religious diversity analysis
- Constitutional context and religious harmony assessment
"""

from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum, Count, Q
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _

from ..models import MunicipalityWideReligionPopulation, ReligionTypeChoice
from ..utils.svg_chart_generator import SVGChartGenerator, RELIGION_COLORS
from ..utils.report_formatter import ReligionReportFormatter


class ReligionDemographicsView(TemplateView):
    """Main view for religion demographics analysis with detailed constitutional and social context"""

    template_name = "demographics/religion/religion_analysis.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get comprehensive religion population data
        religion_data = self.get_religion_population_data()
        ward_wise_data = self.get_ward_wise_religion_data()

        # Generate charts using SVG chart generator with religion-specific colors
        svg_chart_generator = SVGChartGenerator(colors=RELIGION_COLORS)
        charts = {
            "overall_pie_chart": svg_chart_generator.generate_pie_chart_svg(
                religion_data,
                include_title=True,
                title_nepali="धर्म अनुसार जनसंख्या वितरण",
                title_english="Population Distribution by Religion",
            ),
            "ward_wise_bar_chart": svg_chart_generator.generate_bar_chart_svg(
                ward_wise_data,
                include_title=True,
                title_nepali="वडागत धार्मिक जनसंख्या",
                title_english="Ward-wise Religious Population",
            ),
        }

        # Generate detailed analysis
        detailed_analysis = self.generate_detailed_analysis(
            religion_data, ward_wise_data
        )

        # Generate formal report content
        report_formatter = ReligionReportFormatter()
        report_content = report_formatter.generate_formal_report(religion_data)

        context.update(
            {
                "religion_data": religion_data,
                "ward_wise_data": ward_wise_data,
                "charts": charts,
                "report_content": report_content,
                "detailed_analysis": detailed_analysis,
                "total_population": sum(
                    data["population"] for data in religion_data.values()
                ),
                "total_religions": len(
                    [r for r in religion_data.values() if r["population"] > 0]
                ),
                "major_religions": self.get_major_religions(religion_data),
                "religious_diversity_index": self.calculate_religious_diversity_index(
                    religion_data
                ),
                "constitutional_context": self.get_constitutional_context(),
                "cultural_festivals": self.get_cultural_festivals_info(),
            }
        )

        return context

    def get_religion_population_data(self):
        """Get overall religion population data"""
        religion_data = {}

        # Initialize all religions
        for choice in ReligionTypeChoice.choices:
            religion_data[choice[0]] = {
                "code": choice[0],
                "name_nepali": choice[1],
                "population": 0,
                "percentage": 0.0,
            }

        # Get actual data from database
        total_population = 0
        for religion_obj in MunicipalityWideReligionPopulation.objects.all():
            religion_type = religion_obj.religion_type
            if religion_type in religion_data:
                religion_data[religion_type]["population"] = religion_obj.population
                total_population += religion_obj.population

        # Calculate percentages
        if total_population > 0:
            for religion_type, data in religion_data.items():
                if data["population"] > 0:
                    data["percentage"] = data["population"] / total_population * 100

        return religion_data

    def get_ward_wise_religion_data(self):
        """Get ward-wise religion distribution data"""
        # This would typically come from a ward-wise religion model
        # For now, creating a structure that matches expected format
        ward_data = {}

        # Sample structure - in real implementation, this would query the database
        # ward_data[ward_number] = {
        #     'ward_name': f'वडा नं. {ward_number}',
        #     'demographics': {
        #         'HINDU': {'population': X, 'name_nepali': 'हिन्दु'},
        #         'BUDDHIST': {'population': Y, 'name_nepali': 'बौद्ध'},
        #         # ... other religions
        #     }
        # }

        return ward_data

    def generate_detailed_analysis(self, religion_data, ward_wise_data):
        """Generate comprehensive religious analysis with dynamic data"""
        total_population = sum(data["population"] for data in religion_data.values())

        # Convert numbers to Nepali numerals
        def to_nepali_number(num):
            nepali_digits = {
                "0": "०",
                "1": "१",
                "2": "२",
                "3": "३",
                "4": "४",
                "5": "५",
                "6": "६",
                "7": "७",
                "8": "८",
                "9": "९",
            }
            result = str(num)
            for eng, nep in nepali_digits.items():
                result = result.replace(eng, nep)
            return result

        # Get major religions with dynamic data
        hindu_data = religion_data.get("HINDU", {"population": 0, "percentage": 0})
        buddhist_data = religion_data.get(
            "BUDDHIST", {"population": 0, "percentage": 0}
        )
        kirant_data = religion_data.get("KIRANT", {"population": 0, "percentage": 0})
        christian_data = religion_data.get(
            "CHRISTIAN", {"population": 0, "percentage": 0}
        )

        analysis = {
            "introduction_text": f"""नेपालमा धार्मिक स्वतन्त्रता र विविधता रहेको छ । अझै विधिवत रुपमा नेपालको अन्तरिम संविधान २०६३, ले मिति २०६३ जेठ ४ मा पुर्नस्थापित संसदको ऐतिहासिक घोषणाले नेपाल्लाई एक धर्म निरपेक्ष राष्ट्रको रुपमा घोषणा गर्‍यो । त्यस्तै नेपालको संविधान, २०७२ को प्रस्तावनामा नेपाललाई एक बहुजातीय, बहुभाषिक, बहुधार्मिक, बहुसांस्कृतिक तथा भौगोलिक विविधतायुक्त विशेषतालाई आत्मसात् गरी विविधता बिचको एकता, सामाजिक सांस्कृतिक ऐक्यबद्धता, सहिष्णुता र सद्भावलाई संरक्षण एवं प्रवद्र्धन गर्दै, वर्गीय, जातीय, क्षेत्रीय, भाषिक, धार्मिक, लैङ्गिक विभेद र सबै प्रकारका जातीय छुवाछूतको अन्त्य गरी आर्थिक समानता, समृद्धि र सामाजिक न्याय सुनिश्चित गर्न समानुपातिक समावेशी र सहभागितामूलक सिद्धान्तका आधारमा समतामूलक समाजको निर्माण गर्ने संकल्प उल्लेख गरिएको छ । फलस्वरुप नेपालमा धार्मिक स्वतन्त्रता र सौहार्दता रहेको पाईन्छ ।""",
            "cultural_harmony_text": """यहाँ विभिन्न समुदायका मानिसहरूको बसोबास रहेको हुनाले उनीहरूका आ–आफ्नै चाडपर्वहरू छन् । पालिकाबासीले दशैँ, तिहार, तिज, ल्होसार, माघे संक्रान्ति, फागु पूर्णिमा, चण्डी पूर्णिमा, जनैपूर्णिमा, बुद्ध जयन्ती, क्रिसमस पर्व आदि मनाउने गर्दछन् ।""",
            "population_analysis_text": f"""गाउँपालिकामा रहेका कुल {to_nepali_number(total_population)} जनसंख्या मध्ये {to_nepali_number(hindu_data['population'])} अर्थात {to_nepali_number(f"{hindu_data['percentage']:.2f}")} प्रतिशत जनसंख्याले हिन्दु धर्म मान्दछन् भने दोस्रोमा बौद्ध धर्म मान्नेको संख्या {to_nepali_number(buddhist_data['population'])} अर्थात {to_nepali_number(f"{buddhist_data['percentage']:.2f}")} प्रतिशत रहेका छन् । त्यसैगरी {to_nepali_number(kirant_data['population'])} अर्थात {to_nepali_number(f"{kirant_data['percentage']:.2f}")} प्रतिशत किराँत रहेका छन् भने क्रिश्चियन {to_nepali_number(f"{christian_data['percentage']:.1f}")} प्रतिशत रहेका छन् ।""",
            "conclusion_text": """गाउँपालिकामा धार्मिक विविधता रहेता पनि हिन्दु र बौद्ध धर्मावलम्बीहरूको प्रधानता रहेको तथ्याङ्कले देखाउँछ । नेपालमा सदियौंदेखि रहि आएको धार्मिक सहिष्णुता यस गाउँपालिकामा पनि कायमै रहेको देखिन्छ । वडागत रुपमा विभिन्न धर्मावलम्बीहरूको विस्तृत विवरण तालिकामा प्रस्तुत गरिएको छ ।""",
            "statistical_summary": {
                "total_population_nepali": to_nepali_number(total_population),
                "dominant_religion": self.get_dominant_religion(religion_data),
                "religious_diversity_score": self.calculate_religious_diversity_index(
                    religion_data
                ),
                "minority_religions_count": len(
                    [r for r in religion_data.values() if 0 < r["percentage"] < 5.0]
                ),
            },
        }

        return analysis

    def get_dominant_religion(self, religion_data):
        """Get the dominant religion information"""
        max_religion = max(religion_data.items(), key=lambda x: x[1]["population"])
        return {
            "code": max_religion[0],
            "name_nepali": max_religion[1]["name_nepali"],
            "population": max_religion[1]["population"],
            "percentage": max_religion[1]["percentage"],
        }

    def calculate_religious_diversity_index(self, religion_data):
        """Calculate Simpson's Diversity Index for religious diversity"""
        total_pop = sum(data["population"] for data in religion_data.values())
        if total_pop == 0:
            return 0

        diversity_sum = 0
        for data in religion_data.values():
            if data["population"] > 0:
                proportion = data["population"] / total_pop
                diversity_sum += proportion * proportion

        # Simpson's Diversity Index (1 - sum of squares of proportions)
        diversity_index = 1 - diversity_sum
        return round(diversity_index, 4)

    def get_constitutional_context(self):
        """Get constitutional and legal context for religious freedom"""
        return {
            "secular_declaration_date": "२०६३ जेठ ४",
            "constitution_year": "२०७२",
            "key_principles": [
                "धर्म निरपेक्षता",
                "धार्मिक स्वतन्त्रता",
                "बहुधार्मिक समाज",
                "धार्मिक सहिष्णुता",
                "सामाजिक सांस्कृतिक ऐक्यबद्धता",
            ],
            "constitutional_commitment": "विविधता बिचको एकता, सामाजिक सांस्कृतिक ऐक्यबद्धता, सहिष्णुता र सद्भावको संरक्षण",
        }

    def get_cultural_festivals_info(self):
        """Get information about cultural festivals celebrated in the municipality"""
        return {
            "major_festivals": [
                {"name": "दशैँ", "type": "हिन्दु"},
                {"name": "तिहार", "type": "हिन्दु"},
                {"name": "तिज", "type": "हिन्दु"},
                {"name": "ल्होसार", "type": "बौद्ध/तिब्बती"},
                {"name": "माघे संक्रान्ति", "type": "हिन्दु"},
                {"name": "फागु पूर्णिमा", "type": "हिन्दु"},
                {"name": "चण्डी पूर्णिमा", "type": "हिन्दु"},
                {"name": "जनैपूर्णिमा", "type": "हिन्दु"},
                {"name": "बुद्ध जयन्ती", "type": "बौद्ध"},
                {"name": "क्रिसमस पर्व", "type": "क्रिश्चियन"},
            ],
            "cultural_significance": "पालिकामा विभिन्न समुदायका मानिसहरूको बसोबास रहेको हुनाले सबै धर्मका चाडपर्वहरू मनाइन्छ",
        }

    # ...existing code...


class ReligionDataAPIView(TemplateView):
    """API view for religion data (for AJAX requests)"""

    def get(self, request, *args, **kwargs):
        data_type = request.GET.get("type", "overall")

        religion_view = ReligionDemographicsView()
        data = religion_view.get_religion_population_data()

        return JsonResponse(data, safe=False)


class ReligionReportPartialView(TemplateView):
    """View for generating religion report content for PDF inclusion"""

    template_name = "demographics/religion/religion_report_partial.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Use the new religion processor with chart management
        from ..processors.religion import ReligionProcessor

        processor = ReligionProcessor()
        pdf_data = processor.process_for_pdf()

        context.update(
            {
                "religion_data": pdf_data["data"],
                "total_population": pdf_data["total_population"],
                "coherent_analysis": pdf_data["report_content"],
                "charts": pdf_data["charts"],
                "chart_management_status": pdf_data["chart_management_status"],
                "pdf_charts": {
                    "religion": pdf_data["charts"]  # For backward compatibility
                },
                "section_title": pdf_data["section_title"],
                "section_number": pdf_data["section_number"],
            }
        )

        return context
