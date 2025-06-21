"""
Demographic Summary Processor

Handles demographic summary data processing and report formatting for section ३.२.
This section provides an overview of population distribution status.
"""

from pathlib import Path
from .base import BaseDemographicsProcessor, BaseReportFormatter
from ..models import DemographicSummary
from apps.reports.utils.nepali_numbers import (
    format_nepali_number,
    format_nepali_percentage,
)


class DemographicSummaryProcessor(BaseDemographicsProcessor):
    """Processor for demographic summary - population distribution status"""

    def __init__(self):
        super().__init__()

    def get_section_title(self):
        return "जनसंख्या वितरणको अवस्था"

    def get_section_number(self):
        return "३.२"

    def get_data(self):
        """Get demographic summary data"""
        try:
            return DemographicSummary.objects.get(id="singleton")
        except DemographicSummary.DoesNotExist:
            return None

    def generate_report_content(self, data):
        """Generate comprehensive report content for demographic summary"""
        if not data:
            return "<p>डेटा उपलब्ध छैन।</p>"

        # Calculate derived statistics
        male_percentage = (
            (data.population_male / data.total_population * 100)
            if data.total_population
            else 0
        )
        female_percentage = (
            (data.population_female / data.total_population * 100)
            if data.total_population
            else 0
        )

        # Age group percentages
        child_percentage = (
            (data.population_0_to_14 / data.total_population * 100)
            if data.total_population
            else 0
        )
        working_age_percentage = (
            (data.population_15_to_59 / data.total_population * 100)
            if data.total_population
            else 0
        )
        elderly_percentage = (
            (data.population_60_and_above / data.total_population * 100)
            if data.total_population
            else 0
        )

        content = f"""
        <div class="content-section demographic-summary-section">
            <div class="content-paragraph">
                <p>कुनै पनि स्थानको जनसंख्या, विकासको साधन र साध्य दुवैको रुपमा रहेको हुन्छ । विकासको लागि आवश्यक अन्य आर्थिक, भौतिक साधनहरूको परिचालन मानव श्रोतबाट नै हुने भएकाले विकास योजना तर्जुमा गर्दा यसको बनावटको विविध पक्षहरूको अध्ययन र विश्लेषण हुनु आवश्यक हुन्छ । नेपालमा जनसंख्याको विविध पक्षको तथ्याङ्क प्रत्येक १० वर्षमा हुने राष्ट्रिय जनगणनाको साथै गाउँपालिका स्तरमा घरधुरी सर्वेक्षण मार्फत् समेत प्राप्त हुने गरेको छ । यहाँ गाउँपालिकाको घरधुरी तथ्याङ्क संकलन, २०८१ बाट प्राप्त नतिजाको आधारमा जनसंख्याका विविध पक्षहरूको विश्लेषण गरिएको छ ।</p>
            </div>
            
            <div class="table-section">
                <h4 class="table-title">तालिका: लुङ्ग्री गाउँपालिकाको जनसांख्यिकीय सूचकहरू</h4>
                <table class="pdf-data-table demographic-summary-table">
                    <thead>
                        <tr>
                            <th>सूचकहरू</th>
                            <th>मान</th>
                            <th>प्रतिशत</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>कुल जनसंख्या</strong></td>
                            <td>{format_nepali_number(data.total_population)}</td>
                            <td>१००.००%</td>
                        </tr>
                        <tr>
                            <td>&nbsp;&nbsp;पुरुष जनसंख्या</td>
                            <td>{format_nepali_number(data.population_male)}</td>
                            <td>{format_nepali_percentage(male_percentage)}</td>
                        </tr>
                        <tr>
                            <td>&nbsp;&nbsp;महिला जनसंख्या</td>
                            <td>{format_nepali_number(data.population_female)}</td>
                            <td>{format_nepali_percentage(female_percentage)}</td>
                        </tr>
                        {f'''<tr>
                            <td>&nbsp;&nbsp;अन्य जनसंख्या</td>
                            <td>{format_nepali_number(data.population_other)}</td>
                            <td>{format_nepali_percentage((data.population_other / data.total_population * 100) if data.total_population else 0)}</td>
                        </tr>''' if data.population_other and data.population_other > 0 else ''}
                        <tr>
                            <td><strong>लिङ्ग अनुपात</strong></td>
                            <td>{format_nepali_number(data.sex_ratio)}</td>
                            <td>-</td>
                        </tr>
                        <tr>
                            <td><strong>कुल घरपरिवार</strong></td>
                            <td>{format_nepali_number(data.total_households)}</td>
                            <td>-</td>
                        </tr>
                        <tr>
                            <td><strong>औसत घरपरिवार आकार</strong></td>
                            <td>{format_nepali_number(data.average_household_size)}</td>
                            <td>-</td>
                        </tr>
                        <tr>
                            <td><strong>जनसंख्या घनत्व (प्रति वर्ग कि.मी.)</strong></td>
                            <td>{format_nepali_number(data.population_density)}</td>
                            <td>-</td>
                        </tr>
                        <tr class="age-group-header">
                            <td><strong>उमेर समूह अनुसार</strong></td>
                            <td><strong>जनसंख्या</strong></td>
                            <td><strong>प्रतिशत</strong></td>
                        </tr>
                        <tr>
                            <td>&nbsp;&nbsp;०-१४ वर्ष (बालबालिका)</td>
                            <td>{format_nepali_number(data.population_0_to_14)}</td>
                            <td>{format_nepali_percentage(child_percentage)}</td>
                        </tr>
                        <tr>
                            <td>&nbsp;&nbsp;१५-५९ वर्ष (कार्यशील उमेर)</td>
                            <td>{format_nepali_number(data.population_15_to_59)}</td>
                            <td>{format_nepali_percentage(working_age_percentage)}</td>
                        </tr>
                        <tr>
                            <td>&nbsp;&nbsp;६० वर्षभन्दा माथि (जेष्ठ नागरिक)</td>
                            <td>{format_nepali_number(data.population_60_and_above)}</td>
                            <td>{format_nepali_percentage(elderly_percentage)}</td>
                        </tr>
                        {f'''<tr>
                            <td><strong>वृद्धि दर</strong></td>
                            <td>{format_nepali_percentage(data.growth_rate)}</td>
                            <td>-</td>
                        </tr>''' if data.growth_rate is not None else ''}
                        {f'''<tr>
                            <td><strong>१५ वर्षभन्दा माथि साक्षरता दर</strong></td>
                            <td>{format_nepali_percentage(data.literacy_rate_above_15)}</td>
                            <td>-</td>
                        </tr>''' if data.literacy_rate_above_15 is not None else ''}
                        {f'''<tr>
                            <td><strong>१५-२४ वर्ष साक्षरता दर</strong></td>
                            <td>{format_nepali_percentage(data.literacy_rate_15_to_24)}</td>
                            <td>-</td>
                        </tr>''' if data.literacy_rate_15_to_24 is not None else ''}
                    </tbody>
                </table>
            </div>

            <div class="content-paragraph">
                <p>माथिको तालिकामा लुङ्ग्री गाउँपालिकाको जनसंख्याको विस्तृत विवरण प्रस्तुत गरिएको छ । घरधुरी तथ्याङ्क संकलन, २०८१ अनुसार यहाँको कुल जनसंख्या {format_nepali_number(data.total_population)} रहेको छ जसमध्ये पुरुष {format_nepali_number(data.population_male)} अर्थात् {format_nepali_percentage(male_percentage)} प्रतिशत र महिला {format_nepali_number(data.population_female)} अर्थात् {format_nepali_percentage(female_percentage)} प्रतिशत रहेका छन् । सोही अनुसार लैङ्गिक अनुपात (Sex Ratio) {format_nepali_number(data.sex_ratio)} रहेको छ, जसको अर्थ प्रत्येक १०० जना महिलामा {format_nepali_number(data.sex_ratio)} जना पुरुष रहेको देखाउँछ । जनघनत्व (प्रति वर्ग किलोमिटरमा रहेको जनसंख्या) {format_nepali_number(data.population_density)} जना प्रति वर्ग किलोमिटर रहेको छ । कुल {format_nepali_number(data.total_households)} घरपरिवार रहेको यस गाउँपालिकामा प्रति परिवार औसत {format_nepali_number(data.average_household_size)} जना सदस्य रहेको देखिन्छ । यो नेपालको राष्ट्रिय औसत घरपरिवार आकारसँग तुलना गर्दा {"उच्च" if data.average_household_size > 4.5 else "मध्यम" if data.average_household_size > 4.0 else "न्यून"} रहेको छ ।</p>
                
                <p>उमेर समूहको आधारमा हेर्दा, ०-१४ वर्ष उमेर समूहमा {format_nepali_number(data.population_0_to_14)} जना ({format_nepali_percentage(child_percentage)} प्रतिशत) बालबालिकाहरू छन् । यो समूह भविष्यका मानव संसाधनको प्रतिनिधित्व गर्छ र शिक्षा, स्वास्थ्य तथा पोषणका क्षेत्रमा विशेष ध्यान दिनुपर्ने देखाउँछ । १५-५९ वर्ष उमेर समूहमा {format_nepali_number(data.population_15_to_59)} जना ({format_nepali_percentage(working_age_percentage)} प्रतिशत) कार्यशील उमेरका व्यक्तिहरू छन् । यो समूह आर्थिक गतिविधिको मुख्य आधार हो र रोजगारी सिर्जना तथा उत्पादनशीलता वृद्धिमा महत्वपूर्ण भूमिका खेल्छ । ६० वर्षभन्दा माथिका जेष्ठ नागरिकहरूको संख्या {format_nepali_number(data.population_60_and_above)} जना ({format_nepali_percentage(elderly_percentage)} प्रतिशत) रहेको छ । यो समूहका लागि स्वास्थ्य सेवा, सामाजिक सुरक्षा र जेष्ठ नागरिक कल्याणका कार्यक्रमहरूमा विशेष ध्यान दिनुपर्दछ ।</p>
                
                <p>यी तथ्याङ्कहरूले लुङ्ग्री गाउँपालिकाको जनसांख्यिकीय संरचनालाई स्पष्ट पार्छ र स्थानीय विकास योजना निर्माण, संसाधन विनियोजन र सेवा प्रवाहका लागि महत्वपूर्ण आधार प्रदान गर्छ । जनसंख्याको यो विवरणले गाउँपालिकाले आगामी दिनमा गर्नुपर्ने नीतिगत प्राथमिकता र कार्यक्रम निर्धारणमा सहयोग पुर्‍याउनेछ ।</p>
            </div>
        </div>
        """

        return content

    def process_for_pdf(self):
        """Process demographic summary data for PDF generation - override base method"""
        # Get raw data (DemographicSummary model object)
        data = self.get_data()

        # Generate report content
        report_content = self.generate_report_content(data)

        # Generate and save charts (no charts for this section)
        charts = self.generate_and_save_charts(data)

        # Get total population from the model object
        total_population = data.total_population if data else 0

        return {
            "data": data,
            "report_content": report_content,
            "charts": charts,
            "total_population": total_population,
            "section_title": self.get_section_title(),
            "section_number": self.get_section_number(),
        }

    def generate_chart_svg(self, data, chart_type="pie"):
        """No chart generation needed for this section"""
        return None

    def generate_and_save_charts(self, data):
        """No charts to generate for this section"""
        return {}
