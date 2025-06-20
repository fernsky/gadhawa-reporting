"""
Caste Demographics Processor

Handles caste demographic data processing, chart generation, and report formatting.
"""

from pathlib import Path
from .base import BaseDemographicsProcessor, BaseReportFormatter
from ..models import MunicipalityWideCastePopulation, CasteTypeChoice
from ..utils.svg_chart_generator import CASTE_COLORS
from apps.reports.utils.nepali_numbers import (
    format_nepali_number,
    format_nepali_percentage,
)
from apps.chart_management.processors import SimpleChartProcessor


class CasteProcessor(BaseDemographicsProcessor, SimpleChartProcessor):
    """Processor for caste demographics"""

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

        # Customize chart dimensions for caste
        self.pie_chart_width = 900
        self.pie_chart_height = 450
        self.chart_radius = 130
        # Set caste-specific colors
        self.chart_generator.colors = CASTE_COLORS

    def get_chart_key(self):
        """Return unique chart key for this processor"""
        return "demographics_caste"

    def get_section_title(self):
        return "जातजातीको आधारमा जनसंख्याको विवरण"

    def get_section_number(self):
        return "३.६"

    def get_data(self):
        """Get caste population data"""
        caste_data = {}

        # Initialize all castes
        for choice in CasteTypeChoice.choices:
            caste_data[choice[0]] = {
                "code": choice[0],
                "name_nepali": choice[1],
                "population": 0,
                "percentage": 0.0,
            }

        # Get actual data from database
        total_population = 0
        for caste_obj in MunicipalityWideCastePopulation.objects.all():
            caste = caste_obj.caste  # Correct attribute based on models.py
            if caste in caste_data and caste_obj.population:
                caste_data[caste]["population"] = caste_obj.population
                total_population += caste_obj.population

        # Calculate percentages
        if total_population > 0:
            for caste, data in caste_data.items():
                if data["population"] > 0:
                    data["percentage"] = data["population"] / total_population * 100

        return caste_data

    def generate_report_content(self, data):
        """Generate caste-specific report content"""
        formatter = self.CasteReportFormatter()
        return formatter.generate_formal_report(data)

    def generate_chart_svg(self, data, chart_type="pie"):
        """Generate caste chart SVG using SVGChartGenerator"""
        if chart_type == "pie":
            return self.chart_generator.generate_pie_chart_svg(
                data,
                include_title=False,
                title_nepali="जातजातीको आधारमा जनसंख्या वितरण",
                title_english="Population Distribution by Caste",
            )
        elif chart_type == "bar":
            return self.chart_generator.generate_bar_chart_svg(
                data,
                include_title=False,
                title_nepali="जातजातीको आधारमा जनसंख्या वितरण",
                title_english="Population Distribution by Caste",
            )
        return None

    def generate_and_track_charts(self, data):
        """Generate charts only if they don't exist and track them using simplified chart management"""
        charts = {}

        # Ensure static charts directory exists
        self.static_charts_dir.mkdir(parents=True, exist_ok=True)

        # Check and generate pie chart only if needed
        if self.needs_generation("pie"):
            print(f"🔄 Generating caste pie chart...")
            success, png_path, svg_path = self.chart_generator.generate_chart_image(
                demographic_data=data,
                output_name="caste_pie_chart",
                static_dir=str(self.static_charts_dir),
                chart_type="pie",
                include_title=False,
            )

            if success and png_path:
                charts["pie_chart_png"] = f"images/charts/{Path(png_path).name}"
                charts["pie_chart_url"] = f"images/charts/{Path(png_path).name}"
                self.mark_generated("pie")
                print(f"✅ Caste pie chart generated successfully: {png_path}")
            elif svg_path:
                charts["pie_chart_svg"] = f"images/charts/{Path(svg_path).name}"
                charts["pie_chart_url"] = f"images/charts/{Path(svg_path).name}"
                self.mark_generated("pie")
                print(f"✅ Caste pie chart SVG generated: {svg_path}")
        else:
            # Chart already exists, get the URL
            charts["pie_chart_url"] = f"images/charts/caste_pie_chart.png"
            print(f"✅ Caste pie chart already exists")

        # Check and generate bar chart only if needed
        if self.needs_generation("bar"):
            print(f"🔄 Generating caste bar chart...")
            success, png_path, svg_path = self.chart_generator.generate_chart_image(
                demographic_data=data,
                output_name="caste_bar_chart",
                static_dir=str(self.static_charts_dir),
                chart_type="bar",
                include_title=False,
            )

            if success and png_path:
                charts["bar_chart_png"] = f"images/charts/{Path(png_path).name}"
                charts["bar_chart_url"] = f"images/charts/{Path(png_path).name}"
                self.mark_generated("bar")
                print(f"✅ Caste bar chart generated successfully: {png_path}")
            elif svg_path:
                charts["bar_chart_svg"] = f"images/charts/{Path(svg_path).name}"
                charts["bar_chart_url"] = f"images/charts/{Path(svg_path).name}"
                self.mark_generated("bar")
                print(f"✅ Caste bar chart SVG generated: {svg_path}")
        else:
            # Chart already exists, get the URL
            charts["bar_chart_url"] = f"images/charts/caste_bar_chart.png"
            print(f"✅ Caste bar chart already exists")

        return charts

    def generate_and_save_charts(self, data):
        """Legacy method - calls new chart management method"""
        return self.generate_and_track_charts(data)

    def process_for_pdf(self):
        """Process caste data for PDF generation with simplified chart management"""
        # Get raw data
        data = self.get_data()

        # Generate report content
        report_content = self.generate_report_content(data)

        # Generate charts only if needed
        charts = self.generate_and_track_charts(data)

        # Calculate total population
        total_population = sum(caste_data["population"] for caste_data in data.values())

        return {
            "data": data,
            "report_content": report_content,
            "charts": charts,
            "total_population": total_population,
            "section_title": self.get_section_title(),
            "section_number": self.get_section_number(),
        }

    class CasteReportFormatter(BaseReportFormatter):
        """Caste-specific report formatter"""

        def generate_formal_report(self, caste_data):
            """Generate caste formal report content"""
            total_population = sum(data["population"] for data in caste_data.values())

            # Find major castes
            major_castes = []
            for caste_type, data in caste_data.items():
                if data["population"] > 0:
                    major_castes.append(
                        (data["name_nepali"], data["population"], data["percentage"])
                    )

            major_castes.sort(key=lambda x: x[1], reverse=True)

            # Build content based on provided format
            content = []

            # Main population breakdown
            nepali_total = format_nepali_number(total_population)
            content.append(f"""गाउँपालिकामा जातजातिका आधारमा जनसंख्याको विवरणलाई हेर्दा""")

            # Top 5 castes detailed breakdown
            if len(major_castes) >= 5:
                first = major_castes[0]
                second = major_castes[1]
                third = major_castes[2]
                fourth = major_castes[3]
                fifth = major_castes[4]

                first_pop = format_nepali_number(first[1])
                first_pct = format_nepali_percentage(first[2])
                second_pop = format_nepali_number(second[1])
                second_pct = format_nepali_percentage(second[2])
                third_pop = format_nepali_number(third[1])
                third_pct = format_nepali_percentage(third[2])
                fourth_pct = format_nepali_percentage(fourth[2])
                fifth_pct = format_nepali_percentage(fifth[2])

                content.append(
                    f"""सबैभन्दा धेरै {first_pop} अर्थात {first_pct} प्रतिशत {first[0]}, दोस्रोमा {second_pop} अर्थात {second_pct} प्रतिशत {second[0]}, तेस्रोमा {third[0]} {third_pop} अर्थात {third_pct} प्रतिशत रहेका छन् भने चौथो र पाचौमा क्र.म.श. {fourth_pct} प्रतिशत {fourth[0]} र {fifth_pct} प्रतिशत {fifth[0]} रहेका छन् ।"""
                )
            elif major_castes:
                # Flexible breakdown for available data
                breakdown_parts = []
                positions = ["सबैभन्दा धेरै", "दोस्रोमा", "तेस्रोमा", "चौथोमा", "पाचौमा"]

                for i, (name, pop, pct) in enumerate(major_castes[:5]):
                    pop_nepali = format_nepali_number(pop)
                    pct_nepali = format_nepali_percentage(pct)
                    if i < len(positions):
                        breakdown_parts.append(
                            f"""{positions[i]} {pop_nepali} अर्थात {pct_nepali} प्रतिशत {name}"""
                        )

                if breakdown_parts:
                    content.append(" र ".join(breakdown_parts) + " रहेका छन् ।")

            # Other castes present
            if len(major_castes) > 5:
                other_castes = [
                    str(caste[0]) for caste in major_castes[5:10]
                ]  # Next 5 castes
                if other_castes:
                    content.append(
                        f"""त्यसैगरी यहाँ {', '.join(other_castes)} लगायतका जातजातिहरूको बसोबास रहेको छ ।"""
                    )

            # Social tolerance and diversity analysis
            content.append(
                """यसरी जातीय हिसाबले विविधतायुक्त समाजमा स्थानीयहरू सामाजिक सहिष्णुताका साथ बसेको पाइन्छ ।"""
            )

            # Cultural preservation and identity
            content.append(
                """आफ्नो छुट्टै भाषा, संस्कृति र रहनसहन भएका नेपालको सिमान्तकृत जाति लगायत गाउँपालिकामा बसोबास गर्ने विभिन्न जातजातिको मौलिक संस्कृति, परम्परा, भाषा र रहनसहनलाई संरक्षण गरी उनीहरूको पहिचान कायम राख्ने कार्यक्रमहरूको निर्माण गर्नु आवश्यक छ ।"""
            )

            # Constitutional and social framework
            content.append(
                """नेपालको संविधान २०७२ ले जातीय छुवाछूत र भेदभावको अन्त्य गर्ने संकल्प गरेको छ । समानुपातिक समावेशी र सहभागितामूलक सिद्धान्तका आधारमा समतामूलक समाजको निर्माण गर्ने नीति अपनाइएको छ ।"""
            )

            # Local government initiatives
            content.append(
                """स्थानीय तहले सबै जातजातिका नागरिकहरूको सामाजिक, आर्थिक र राजनीतिक सशक्तिकरणमा विशेष ध्यान दिएको छ । समावेशी विकासका कार्यक्रमहरू सञ्चालन गरी सबै वर्गका मानिसहरूलाई मुख्य धारामा ल्याउने प्रयास गरिएको छ ।"""
            )

            # Social harmony and unity
            content.append(
                """जातीय एकता र सामाजिक सद्भावना कायम राख्न समुदायिक संवाद र सहकार्यलाई प्रोत्साहन गरिएको छ । विविधतामा एकताको सिद्धान्त अनुसार सबै जातजातिले मिलेर गाउँपालिकाको समग्र विकासमा योगदान पुर्याइरहेका छन् ।"""
            )

            # Future commitment
            content.append(
                """भविष्यमा पनि सबै जातजातिको सांस्कृतिक पहिचान र मौलिकताको संरक्षण गर्दै समग्र समुदायको कल्याणमा गाउँपालिका प्रतिबद्ध रहनेछ ।"""
            )

            return " ".join(content)
