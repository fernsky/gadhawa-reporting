"""
Municipality Wide Foreign Employment Countries Processor

Handles municipality-wide foreign employment country data processing, pie chart generation, and report formatting.
"""

from .base import BaseEconomicsProcessor, BaseEconomicsReportFormatter
from ..models import MunicipalityWideForeignEmploymentCountries
from apps.demographics.utils.svg_chart_generator import DEFAULT_COLORS
from apps.reports.utils.nepali_numbers import (
    format_nepali_number,
    format_nepali_percentage,
)


class MunicipalityWideForeignEmploymentCountriesProcessor(BaseEconomicsProcessor):
    """Processor for municipality-wide foreign employment countries data"""

    def __init__(self):
        super().__init__()
        self.pie_chart_width = 900
        self.pie_chart_height = 450
        self.chart_radius = 130
        self.chart_generator.colors = DEFAULT_COLORS

    def get_section_title(self):
        return "वैदेशिक रोजगारीमा गएका देश अनुसार जनसंख्या विवरण"

    def get_section_number(self):
        return "४.१.१०"

    def get_data(self):
        country_data = {}
        total_population = 0
        nepali_names = {
            "AZERBAIJAN": "अजरबैजान",
            "BAHRAIN": "बहराइन",
            "BELGIUM": "बेल्जियम",
            "BRUNEI": "ब्रुनाइ",
            "BULGARIA": "बुल्गेरिया",
            "CAMEROON": "क्यामरुन",
            "CANADA": "क्यानाडा",
            "CECILS": "सेसिल्स",
            "COSTA_RICA": "कोस्टारिका",
            "CROATIA": "क्रोएसिया",
            "CYPRUS": "साइप्रस",
            "DUBAI": "दुबई",
            "GREECE": "ग्रीस",
            "INDIA": "भारत",
            "JAPAN": "जापान",
            "KATHMANDU": "काठमाडौं",
            "KOSOVO": "कोसोभो",
            "MALAYSIA": "मलेसिया",
            "MALDIVES": "माल्दिभ्स",
            "MALTA": "माल्टा",
            "MAURITIUS": "मौरिसस",
            "MEXICO": "मेक्सिको",
            "MYANMAR": "म्यानमार",
            "NIGER": "नाइजर",
            "NORTH_KOREA": "उत्तर कोरिया",
            "NORWAY": "नर्वे",
            "OTHER": "अन्य",
            "PAKISTAN": "पाकिस्तान",
            "PERU": "पेरु",
            "POLAND": "पोल्याण्ड",
            "PORTUGAL": "पोर्चुगल",
            "QATAR": "कतार",
            "ROMANIA": "रोमानिया",
            "SAN_MARINO": "सान मारिनो",
            "SAUDI_ARABIA": "साउदी अरेबिया",
            "SOUTH_AFRICA": "दक्षिण अफ्रिका",
            "SOUTH_KOREA": "दक्षिण कोरिया",
            "TURKEY": "टर्की",
            "UKRAINE": "युक्रेन",
            "UNITED_ARAB_EMIRATES": "संयुक्त अरब इमिरेट्स",
            "UNITED_KINGDOM_OF_GREAT_BRITAIN": "संयुक्त अधिराज्य",
            "UNITED_STATES_OF_AMERICA": "संयुक्त राज्य अमेरिका",
            "YEMEN": "येमेन",
        }
        # Collect and sort all data
        all_objs = list(MunicipalityWideForeignEmploymentCountries.objects.all())
        all_objs.sort(key=lambda x: -x.population)
        # Top 10 + sum rest as 'अन्य'
        top_objs = all_objs[:10]
        other_objs = all_objs[10:]
        # Prepare data
        for obj in top_objs:
            nep_name = nepali_names.get(obj.country, obj.country)
            country_data[nep_name] = {
                "country": nep_name,
                "population": obj.population,
                "percentage": 0,
            }
            total_population += obj.population
        other_population = sum(obj.population for obj in other_objs)
        if other_population > 0:
            country_data["अन्य"] = {
                "country": "अन्य",
                "population": other_population,
                "percentage": 0,
            }
            total_population += other_population
        # Calculate percentages
        if total_population > 0:
            for v in country_data.values():
                v["percentage"] = v["population"] * 100 / total_population
        # Pie chart data
        pie_chart_data = {k: v["population"] for k, v in country_data.items()}
        return {
            "country_data": country_data,
            "total_population": total_population,
            "pie_chart_data": pie_chart_data,
        }

    def generate_report_content(self, data):
        formatter = self.MunicipalityWideForeignEmploymentCountriesReportFormatter()
        return formatter.generate_formal_report(
            data["country_data"], data["total_population"]
        )

    def get_chart_key(self):
        return "municipality_wide_foreign_employment_countries"

    def generate_chart_svg(self, data, chart_type="pie"):
        if chart_type == "pie":
            return self.chart_generator.generate_chart_svg(
                demographic_data=data["pie_chart_data"],
                chart_type="pie",
                width=self.pie_chart_width,
                height=self.pie_chart_height,
                radius=self.chart_radius,
            )
        return None

    def generate_and_save_charts(self, data):
        charts = {}
        category_name = "municipality_wide_foreign_employment_countries"
        pie_data = data["pie_chart_data"]
        success, png_path, svg_path = self.chart_generator.generate_chart_image(
            demographic_data=pie_data,
            output_name=f"{category_name}_pie_chart",
            static_dir=str(self.static_charts_dir),
            chart_type="pie",
            include_title=False,
        )
        if success and png_path:
            charts["pie"] = png_path
        elif svg_path:
            charts["pie"] = svg_path
        return charts

    class MunicipalityWideForeignEmploymentCountriesReportFormatter(
        BaseEconomicsReportFormatter
    ):
        def generate_formal_report(self, country_data, total_population):
            """Generate a comprehensive and verbose analysis of foreign employment destinations"""

            # Handle case where no data is available
            if not country_data:
                return (
                    "यस खण्डमा कुनै वैदेशिक रोजगारीको तथ्यांक उपलब्ध छैन। लुङ्ग्री गाउँपालिकाका "
                    "नागरिकहरूको वैदेशिक रोजगारीको विवरण सङ्कलन गर्न सकिएको छैन।"
                )

            # Sort countries by population in descending order
            sorted_countries = sorted(
                country_data.values(), key=lambda x: -x["population"]
            )

            if not sorted_countries:
                return "वैदेशिक रोजगारीको तथ्यांक उपलब्ध छैन।"

            # Start building comprehensive analysis
            analysis_parts = []

            # Introduction with total overview
            analysis_parts.append(
                f"लुङ्ग्री गाउँपालिकाको जनसंख्या तथ्यांक विश्लेषण गर्दा वैदेशिक रोजगारीको क्षेत्रमा "
                f"महत्त्वपूर्ण गतिविधि देखिन्छ। यस गाउँपालिकाबाट कुल {format_nepali_number(total_population)} "
                f"जना नागरिकहरूले विभिन्न देशहरूमा रोजगारीको अवसर खोजेका छन्। यो तथ्यांकले "
                f"स्थानीय जनसंख्याको आर्थिक गतिविधि र श्रम बजारको अवस्थालाई प्रतिबिम्बित गर्दछ।"
            )

            # Primary destination analysis
            top_country = sorted_countries[0]
            analysis_parts.append(
                f"वैदेशिक रोजगारीको प्रमुख गन्तव्य देशको रूपमा {top_country['country']} अग्रणी स्थानमा "
                f"रहेको छ, जहाँ {format_nepali_number(top_country['population'])} जना नागरिकहरूले "
                f"रोजगारी प्राप्त गरेका छन्। यसले कुल वैदेशिक रोजगारीमा गएका जनसंख्याको "
                f"{format_nepali_percentage(top_country['percentage'])} भाग ओगटेको छ। यो उच्च अनुपातले "
                f"{top_country['country']}को श्रम बजारमा नेपाली कामदारहरूको माग र पहुँचलाई "
                f"संकेत गर्दछ।"
            )

            # Secondary destinations analysis
            if len(sorted_countries) > 1:
                second_country = sorted_countries[1]
                analysis_parts.append(
                    f"दोस्रो प्रमुख गन्तव्य देशको रूपमा {second_country['country']}ले महत्त्वपूर्ण भूमिका "
                    f"खेलेको छ, जहाँ {format_nepali_number(second_country['population'])} जना "
                    f"({format_nepali_percentage(second_country['percentage'])}) नागरिकहरूले रोजगारी "
                    f"पाएका छन्। यसले वैदेशिक रोजगारीमा गन्तव्य देशहरूको विविधीकरणलाई दर्शाउँछ।"
                )

            # Top 5 destinations comprehensive overview
            if len(sorted_countries) >= 5:
                top_5_countries = sorted_countries[:5]
                top_5_population = sum(c["population"] for c in top_5_countries)
                top_5_percentage = (
                    (top_5_population * 100) / total_population
                    if total_population > 0
                    else 0
                )

                # Create a coherent paragraph listing countries and stats
                country_details = []
                for country in top_5_countries:
                    country_details.append(
                        f"{country['country']} - {format_nepali_number(country['population'])} जना ({format_nepali_percentage(country['percentage'])})"
                    )
                joined_details = "; ".join(country_details)

                analysis_parts.append(
                    f"शीर्ष पाँच गन्तव्य देशहरूको विस्तृत विवरण निम्नानुसार छ: {joined_details}। यी पाँच देशहरूमा मात्रै कुल वैदेशिक रोजगारीमा गएका जनसंख्याको "
                    f"{format_nepali_percentage(top_5_percentage)} भाग केन्द्रित छ, जसले केही "
                    f"विशेष देशहरूमा रोजगारीको अवसरको एकाग्रतालाई देखाउँछ।"
                )

            # Regional/geographical analysis
            gulf_countries = [
                "बहराइन",
                "कतार",
                "साउदी अरेबिया",
                "संयुक्त अरब इमिरेट्स",
                "दुबई",
            ]
            gulf_population = sum(
                c["population"]
                for c in sorted_countries
                if c["country"] in gulf_countries
            )

            if gulf_population > 0:
                gulf_percentage = (
                    (gulf_population * 100) / total_population
                    if total_population > 0
                    else 0
                )
                analysis_parts.append(
                    f"भौगोलिक दृष्टिकोणबाट विश्लेषण गर्दा खाडी देशहरूमा रोजगारीको महत्त्वपूर्ण उपस्थिति "
                    f"देखिन्छ। खाडी क्षेत्रका देशहरूमा कुल {format_nepali_number(gulf_population)} जना "
                    f"({format_nepali_percentage(gulf_percentage)}) नागरिकहरूले रोजगारी पाएका छन्। "
                    f"यसले परम्परागत श्रम गन्तव्यको रूपमा खाडी देशहरूको निरन्तर महत्त्वलाई प्रमाणित गर्दछ।"
                )

            # Diversity analysis
            total_countries = len(country_data)
            if total_countries > 10:
                other_countries_data = country_data.get("अन्य", {})
                other_population = other_countries_data.get("population", 0)
                other_percentage = other_countries_data.get("percentage", 0)

                analysis_parts.append(
                    f"वैदेशिक रोजगारी गन्तव्यको विविधताको सन्दर्भमा, लुङ्ग्री गाउँपालिकाका नागरिकहरूले "
                    f"विश्वभरका {total_countries} भन्दा बढी देशहरूमा रोजगारी प्राप्त गरेका छन्। "
                    f"शीर्ष १० देशहरू बाहेकका अन्य देशहरूमा {format_nepali_number(other_population)} जना "
                    f"({format_nepali_percentage(other_percentage)}) नागरिकहरूको उपस्थिति छ। यसले "
                    f"वैदेशिक रोजगारीमा गन्तव्य देशहरूको व्यापक विविधीकरण र नेपाली कामदारहरूको "
                    f"अन्तर्राष्ट्रिय पहुँचलाई प्रदर्शन गर्दछ।"
                )

            # Economic implications
            analysis_parts.append(
                f"यो वैदेशिक रोजगारीको तथ्यांकले लुङ्ग्री गाउँपालिकाको आर्थिक संरचनामा महत्त्वपूर्ण प्रभाव "
                f"पारेको छ। वैदेशिक रोजगारीबाट प्राप्त हुने रेमिट्यान्सले स्थानीय अर्थतन्त्रमा तरलतारा "
                f"वृद्धि गरेको छ। साथै, यसले स्थानीय श्रमशक्तिको कुशलता विकास र अन्तर्राष्ट्रिय "
                f"अनुभवको आदानप्रदानमा योगदान पुर्‍याएको छ।"
            )

            # Concluding remarks
            analysis_parts.append(
                f"समग्रमा, लुङ्ग्री गाउँपालिकाको वैदेशिक रोजगारीको अवस्थाले नेपालको राष्ट्रिय श्रम "
                f"निर्यातको ढाँचालाई प्रतिबिम्बित गर्दै, विविधीकृत गन्तव्य देशहरूमा कुशल र अकुशल "
                f"दुवै प्रकारका कामदारहरूको सहभागितालाई देखाउँछ। भविष्यमा यस क्षेत्रको थप विकासका "
                f"लागि सीप विकास, सुरक्षित बसाइसराइ र श्रमिक कल्याणका कार्यक्रमहरूलाई प्राथमिकता "
                f"दिनु आवश्यक छ।"
            )

            # Join all parts with proper spacing
            return " ".join(analysis_parts)

    def process_for_pdf(self):
        data = self.get_data()
        report_content = self.generate_report_content(data)
        charts = self.generate_and_save_charts(data)
        return {
            "data": data,
            "report_content": report_content,
            "charts": charts,
            "total_population": data["total_population"],
            "section_title": self.get_section_title(),
            "section_number": self.get_section_number(),
        }
