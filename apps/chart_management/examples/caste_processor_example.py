"""
Example: Updated Caste Processor with Chart Management

This shows how to migrate existing processors to use the new chart management system.
"""

from apps.chart_management.processors import (
    EnhancedChartProcessor,
    EnhancedReportFormatter,
)
from ..models import MunicipalityWideCastePopulation, CasteTypeChoice
from apps.reports.utils.nepali_numbers import (
    format_nepali_number,
    format_nepali_percentage,
)


class CasteProcessor(EnhancedChartProcessor):
    """Enhanced Caste Processor with Chart Management"""

    def __init__(self):
        super().__init__()
        # Customize chart dimensions for caste
        self.pie_chart_width = 900
        self.pie_chart_height = 450
        self.chart_radius = 130

    def get_section_title(self):
        return "जातजातीको आधारमा जनसंख्याको विवरण"

    def get_section_number(self):
        return "३.६"

    def get_chart_key(self):
        return "demographics_caste"

    def get_pie_chart_title(self):
        return "जातजातीको आधारमा जनसंख्या वितरण"

    def supports_pie_chart(self):
        return True

    def supports_bar_chart(self):
        return True  # Enable bar chart for caste data

    def get_bar_chart_title(self):
        return "जातजातीको तुलनात्मक वितरण"

    def get_data(self):
        """Get caste population data"""
        caste_data = {}

        # Initialize all castes
        for choice in CasteTypeChoice.choices:
            caste_data[choice[0]] = {
                "population": 0,
                "percentage": 0.0,
                "name_nepali": choice[1],
            }

        # Get actual data from database
        total_population = 0
        for caste_obj in MunicipalityWideCastePopulation.objects.all():
            caste = caste_obj.caste
            if caste in caste_data:
                caste_data[caste]["population"] += caste_obj.population
                total_population += caste_obj.population

        # Calculate percentages
        if total_population > 0:
            for caste in caste_data:
                percentage = (caste_data[caste]["population"] / total_population) * 100
                caste_data[caste]["percentage"] = percentage

        return {
            "caste_data": caste_data,
            "total_population": total_population,
        }

    def generate_html_content(self, data, chart_urls):
        """Generate HTML content with caste analysis"""
        caste_data = data.get("caste_data", {})
        total_population = data.get("total_population", 0)

        # Find dominant castes
        sorted_castes = sorted(
            caste_data.items(), key=lambda x: x[1]["population"], reverse=True
        )

        analysis_text = ""
        if sorted_castes and total_population > 0:
            dominant_caste = sorted_castes[0]
            analysis_text = f"""
            <div class="analysis-section">
                <h4>जातजातीय विविधता विश्लेषण</h4>
                <p>लुङ्ग्री गाउँपालिकामा कुल जनसंख्या {format_nepali_number(total_population)} छ।</p>
                <p>यहाँ {dominant_caste[1]['name_nepali']} जातको जनसंख्या सबैभन्दा बढी छ 
                ({format_nepali_number(dominant_caste[1]['population'])} जना, 
                {format_nepali_percentage(dominant_caste[1]['percentage'])})।</p>
                
                <!-- Diversity metrics -->
                <div class="diversity-metrics">
                    <h5>विविधता सूचकहरू</h5>
            """

            # Calculate diversity metrics
            active_castes = sum(1 for c in caste_data.values() if c["population"] > 0)
            analysis_text += (
                f"<p>कुल सक्रिय जातजाति: {format_nepali_number(active_castes)}</p>"
            )

            analysis_text += "</div></div>"

        return analysis_text


class CasteReportFormatter(EnhancedReportFormatter):
    """Enhanced report formatter for caste demographics"""

    def format_for_html(self):
        """Format caste data for HTML display"""
        caste_data = self.data.get("caste_data", {})
        total_population = self.data.get("total_population", 0)

        # Sort castes by population
        sorted_castes = sorted(
            caste_data.items(), key=lambda x: x[1]["population"], reverse=True
        )

        html_content = f"""
        <div class="caste-report">
            <h3>{self.processor_data.get('section_title', '')}</h3>
            
            <!-- Chart Display -->
            <div class="chart-section">
                <div class="row">
                    <div class="col-md-6">
                        <h4>वितरण चार्ट</h4>
                        {self.get_chart_html('pie', 'caste-pie-chart-container')}
                    </div>
                    <div class="col-md-6">
                        <h4>तुलनात्मक चार्ट</h4>
                        {self.get_chart_html('bar', 'caste-bar-chart-container')}
                    </div>
                </div>
            </div>
            
            <!-- Data Table -->
            <div class="data-table">
                <h4>विस्तृत तथ्याङ्क</h4>
                <table class="table table-bordered table-striped">
                    <thead class="table-dark">
                        <tr>
                            <th>जातजाति</th>
                            <th>जनसंख्या</th>
                            <th>प्रतिशत</th>
                        </tr>
                    </thead>
                    <tbody>
        """

        for caste_code, caste_info in sorted_castes:
            if caste_info["population"] > 0:
                html_content += f"""
                        <tr>
                            <td>{caste_info['name_nepali']}</td>
                            <td class="text-end">{format_nepali_number(caste_info['population'])}</td>
                            <td class="text-end">{format_nepali_percentage(caste_info['percentage'])}</td>
                        </tr>
                """

        html_content += f"""
                    </tbody>
                    <tfoot>
                        <tr class="table-info fw-bold">
                            <th>जम्मा</th>
                            <th class="text-end">{format_nepali_number(total_population)}</th>
                            <th class="text-end">१००.००%</th>
                        </tr>
                    </tfoot>
                </table>
            </div>
            
            <!-- Analysis -->
            {self.processor_data.get('html_content', '')}
        </div>
        """

        return html_content
