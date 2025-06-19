"""
Religion Demographics Processor

Handles religion demographic data processing, chart generation, and report formatting.
"""

from pathlib import Path
from .base import BaseDemographicsProcessor, BaseReportFormatter
from ..models import MunicipalityWideReligionPopulation, ReligionTypeChoice
from ..utils.svg_chart_generator import RELIGION_COLORS
from apps.reports.utils.nepali_numbers import (
    format_nepali_number,
    format_nepali_percentage,
)
from apps.chart_management.processors import SimpleChartProcessor


class ReligionProcessor(BaseDemographicsProcessor, SimpleChartProcessor):
    """Processor for religion demographics"""

    def __init__(self):
        super().__init__()
        SimpleChartProcessor.__init__(self)

        # Ensure we use the same directory as the chart service
        from django.conf import settings

        if hasattr(settings, "STATICFILES_DIRS") and settings.STATICFILES_DIRS:
            # Use same directory as chart management service
            self.static_charts_dir = (
                Path(settings.STATICFILES_DIRS[0]) / "images" / "charts"
            )
        else:
            # Fallback to STATIC_ROOT
            self.static_charts_dir = Path(settings.STATIC_ROOT) / "images" / "charts"

        self.static_charts_dir.mkdir(parents=True, exist_ok=True)

        # Customize chart dimensions for religion
        self.pie_chart_width = 900
        self.pie_chart_height = 450
        self.chart_radius = 130
        # Set religion-specific colors
        self.chart_generator.colors = RELIGION_COLORS

    def get_chart_key(self):
        """Return unique chart key for this processor"""
        return "demographics_religion"

    def get_section_title(self):
        return "धर्म अनुसार जनसंख्याको विवरण"

    def get_section_number(self):
        return "३.५"

    def get_data(self):
        """Get religion population data"""
        religion_data = {}

        # Initialize all religions
        for choice in ReligionTypeChoice.choices:
            religion_data[choice[0]] = {
                "population": 0,
                "percentage": 0.0,
                "name_nepali": choice[1],
            }

        # Get actual data from database
        total_population = 0
        for religion_obj in MunicipalityWideReligionPopulation.objects.all():
            religion = religion_obj.religion  # Correct attribute based on models.py
            if religion in religion_data:
                religion_data[religion]["population"] += religion_obj.population
                total_population += religion_obj.population

        # Calculate percentages
        if total_population > 0:
            for religion, data in religion_data.items():
                data["percentage"] = round(
                    (data["population"] / total_population) * 100, 2
                )

        return religion_data

    def generate_report_content(self, data):
        """Generate religion-specific report content"""
        formatter = self.ReligionReportFormatter()
        return formatter.generate_formal_report(data)

    def generate_chart_svg(self, data, chart_type="pie"):
        """Generate religion chart SVG using SVGChartGenerator"""
        if chart_type == "pie":
            return self.chart_generator.generate_pie_chart_svg(
                data,
                include_title=False,
                title_nepali="धर्म अनुसार जनसंख्या वितरण",
                title_english="Population Distribution by Religion",
            )
        elif chart_type == "bar":
            return self.chart_generator.generate_bar_chart_svg(
                data,
                include_title=False,
                title_nepali="धर्म अनुसार जनसंख्या वितरण",
                title_english="Population Distribution by Religion",
            )
        return None

    def generate_and_track_charts(self, data):
        """Generate charts and track them using chart management system with high-quality output"""
        charts = {}

        # Ensure static charts directory exists
        self.static_charts_dir.mkdir(parents=True, exist_ok=True)

        # Generate pie chart using the full chart generation pipeline
        print("🎨 Generating pie chart with high-quality output...")
        success_pie, png_path_pie, svg_path_pie = (
            self.chart_generator.generate_chart_image(
                demographic_data=data,
                output_name="religion_pie_chart",
                static_dir=str(self.static_charts_dir),
                chart_type="pie",
                include_title=False,
                title_nepali="धर्म अनुसार जनसंख्या वितरण",
                title_english="Population Distribution by Religion",
            )
        )

        if success_pie and png_path_pie:
            # Use PNG file for high quality
            pie_file_path = "religion_pie_chart.png"
            print(f"✓ Generated high-quality pie chart: {png_path_pie}")

            # Track with chart management system
            pie_url = self.track_chart_file(
                chart_type="pie",
                data=data,
                file_path=pie_file_path,
                title="धर्म अनुसार जनसंख्या वितरण (पाई चार्ट)",
            )
            if pie_url:
                charts["pie_chart_url"] = pie_url
                charts["pie_chart_png"] = pie_file_path
                print(f"✓ Pie chart URL: {pie_url}")

        elif svg_path_pie:
            # Fallback to SVG if PNG generation failed
            pie_file_path = "religion_pie_chart.svg"
            print(f"⚠ Using SVG fallback for pie chart: {svg_path_pie}")

            pie_url = self.track_chart_file(
                chart_type="pie",
                data=data,
                file_path=pie_file_path,
                title="धर्म अनुसार जनसंख्या वितरण (पाई चार्ट)",
            )
            if pie_url:
                charts["pie_chart_url"] = pie_url
                charts["pie_chart_svg"] = pie_file_path
        else:
            print("❌ Failed to generate pie chart")

        # Generate bar chart using the full chart generation pipeline
        print("🎨 Generating bar chart with high-quality output...")
        success_bar, png_path_bar, svg_path_bar = (
            self.chart_generator.generate_chart_image(
                demographic_data=data,
                output_name="religion_bar_chart",
                static_dir=str(self.static_charts_dir),
                chart_type="bar",
                include_title=False,
                title_nepali="धर्म अनुसार जनसंख्या वितरण",
                title_english="Population Distribution by Religion",
            )
        )

        if success_bar and png_path_bar:
            # Use PNG file for high quality
            bar_file_path = "religion_bar_chart.png"
            print(f"✓ Generated high-quality bar chart: {png_path_bar}")

            # Track with chart management system
            bar_url = self.track_chart_file(
                chart_type="bar",
                data=data,
                file_path=bar_file_path,
                title="धर्म अनुसार जनसंख्या वितरण (बार चार्ट)",
            )
            if bar_url:
                charts["bar_chart_url"] = bar_url
                charts["bar_chart_png"] = bar_file_path
                print(f"✓ Bar chart URL: {bar_url}")

        elif svg_path_bar:
            # Fallback to SVG if PNG generation failed
            bar_file_path = "religion_bar_chart.svg"
            print(f"⚠ Using SVG fallback for bar chart: {svg_path_bar}")

            bar_url = self.track_chart_file(
                chart_type="bar",
                data=data,
                file_path=bar_file_path,
                title="धर्म अनुसार जनसंख्या वितरण (बार चार्ट)",
            )
            if bar_url:
                charts["bar_chart_url"] = bar_url
                charts["bar_chart_svg"] = bar_file_path
        else:
            print("❌ Failed to generate bar chart")

        return charts

    def check_charts_current(self, data):
        """Check if existing charts are still current"""
        pie_current = self.is_chart_current("pie", data)
        bar_current = self.is_chart_current("bar", data)
        return {
            "pie_current": pie_current,
            "bar_current": bar_current,
            "all_current": pie_current and bar_current,
        }

    def process_for_pdf(self):
        """Process religion data for PDF generation with chart management"""
        # Get raw data
        data = self.get_data()

        # Generate report content
        report_content = self.generate_report_content(data)

        # Check if charts need to be regenerated
        chart_status = self.check_charts_current(data)

        # Generate charts only if needed or get existing URLs
        if not chart_status["all_current"]:
            charts = self.generate_and_track_charts(data)
        else:
            # Get existing chart URLs - check for both PNG and SVG
            charts = {}

            pie_url = self.get_chart_url("pie")
            if pie_url:
                charts["pie_chart_url"] = pie_url
                # Determine file type from URL
                if pie_url.endswith(".png"):
                    charts["pie_chart_png"] = "religion_pie_chart.png"
                else:
                    charts["pie_chart_svg"] = "religion_pie_chart.svg"

            bar_url = self.get_chart_url("bar")
            if bar_url:
                charts["bar_chart_url"] = bar_url
                # Determine file type from URL
                if bar_url.endswith(".png"):
                    charts["bar_chart_png"] = "religion_bar_chart.png"
                else:
                    charts["bar_chart_svg"] = "religion_bar_chart.svg"

        # Calculate total population
        total_population = sum(
            item["population"]
            for item in data.values()
            if isinstance(item, dict) and "population" in item
        )

        return {
            "data": data,
            "report_content": report_content,
            "charts": charts,
            "chart_management_status": chart_status,
            "total_population": total_population,
            "section_title": self.get_section_title(),
            "section_number": self.get_section_number(),
        }

    class ReligionReportFormatter(BaseReportFormatter):
        """Religion-specific report formatter"""

        def generate_formal_report(self, religion_data):
            """Generate religion formal report content"""
            total_population = sum(
                data["population"] for data in religion_data.values()
            )

            # Find major religions
            major_religions = []
            for religion_type, data in religion_data.items():
                if data["population"] > 0:
                    major_religions.append(
                        (data["name_nepali"], data["population"], data["percentage"])
                    )

            major_religions.sort(key=lambda x: x[1], reverse=True)

            # Build content based on provided text
            content = []

            # Constitutional and historical context
            content.append(
                """नेपालमा धार्मिक स्वतन्त्रता र विविधता रहेको छ । अझै विधिवत रुपमा नेपालको अन्तरिम संविधान २०६३, ले मिति २०६३ जेठ ४ मा पुर्नस्थापित संसदको ऐतिहासिक घोषणाले नेपाललाई एक धर्म निरपेक्ष राष्ट्रको रुपमा घोषणा गर्यो । त्यस्तै नेपालको संविधान, २०७२ को प्रस्तावनामा नेपाललाई एक बहुजातीय, बहुभाषिक, बहुधार्मिक, बहुसांस्कृतिक तथा भौगोलिक विविधतायुक्त विशेषतालाई आत्मसात् गरी विविधता बिचको एकता, सामाजिक सांस्कृतिक ऐक्यबद्धता, सहिष्णुता र सद्भावलाई संरक्षण एवं प्रवर्धन गर्दै, वर्गीय, जातीय, क्षेत्रीय, भाषिक, धार्मिक, लैङ्गिक विभेद र सबै प्रकारका जातीय छुवाछूतको अन्त्य गरी आर्थिक समानता, समृद्धि र सामाजिक न्याय सुनिश्चित गर्न समानुपातिक समावेशी र सहभागितामूलक सिद्धान्तका आधारमा समतामूलक समाजको निर्माण गर्ने संकल्प उल्लेख गरिएको छ । फलस्वरुप नेपालमा धार्मिक स्वतन्त्रता र सौहार्दता रहेको पाईन्छ ।"""
            )

            # Festivals and cultural practices
            content.append(
                """यहाँ विभिन्न समुदायका मानिसहरूको बसोबास रहेको हुनाले उनीहरूका आ–आफ्नै चाडपर्वहरू छन् । पालिकाबासीले दशैँ, तिहार, तिज, ल्होसार, माघे संक्रान्ति, फागु पूर्णिमा, चण्डी पूर्णिमा, जनैपूर्णिमा, बुद्ध जयन्ती, क्रिसमस पर्व आदि मनाउने गर्दछन् ।"""
            )

            # Population statistics
            nepali_total = format_nepali_number(total_population)
            if major_religions:
                # Get Hindu percentage (assuming it's the major religion)
                hindu_data = next((r for r in major_religions if "हिन्दु" in r[0]), None)
                buddhist_data = next(
                    (r for r in major_religions if "बौद्ध" in r[0]), None
                )
                kirant_data = next(
                    (r for r in major_religions if "किराँत" in r[0]), None
                )
                christian_data = next(
                    (
                        r
                        for r in major_religions
                        if "क्रिश्चियन" in r[0] or "ईसाई" in r[0]
                    ),
                    None,
                )

                stats_text = f"""गाउँपालिकामा रहेका कुल {nepali_total} जनसंख्या मध्ये"""

                if hindu_data:
                    hindu_pop = format_nepali_number(hindu_data[1])
                    hindu_pct = format_nepali_percentage(hindu_data[2])
                    stats_text += f""" {hindu_pop} अर्थात {hindu_pct} प्रतिशत जनसंख्याले हिन्दु धर्म मान्दछन्"""

                if buddhist_data:
                    buddhist_pop = format_nepali_number(buddhist_data[1])
                    buddhist_pct = format_nepali_percentage(buddhist_data[2])
                    stats_text += f""" भने दोस्रोमा बौद्ध धर्म मान्नेको संख्या {buddhist_pop} अर्थात {buddhist_pct} प्रतिशत रहेका छन् ।"""

                other_religions = []
                if kirant_data:
                    kirant_pop = format_nepali_number(kirant_data[1])
                    kirant_pct = format_nepali_percentage(kirant_data[2])
                    other_religions.append(
                        f"""{kirant_pop} अर्थात {kirant_pct} प्रतिशत किराँत"""
                    )

                if christian_data:
                    christian_pct = format_nepali_percentage(christian_data[2])
                    other_religions.append(f"""क्रिश्चियन {christian_pct} प्रतिशत""")

                if other_religions:
                    stats_text += (
                        f""" त्यसैगरी {' भने '.join(other_religions)} रहेका छन् ।"""
                    )

                content.append(stats_text)

            # Religious diversity and tolerance
            content.append(
                """गाउँपालिकामा धार्मिक विविधता रहेता पनि हिन्दु र बौद्ध धर्मावलम्बीहरूको प्रधानता रहेको तथ्याङ्कले देखाउँछ । नेपालमा सदियौंदेखि रहि आएको धार्मिक सहिष्णुता यस गाउँपालिकामा पनि कायमै रहेको देखिन्छ ।"""
            )

            return " ".join(content)
