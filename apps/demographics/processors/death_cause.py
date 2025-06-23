"""
Death Cause Demographics Processor

Handles death cause demographic data processing, chart generation, and report formatting.
"""

from pathlib import Path
from .base import BaseDemographicsProcessor, BaseReportFormatter
from ..models import WardWiseDeathCause, DeathCauseChoice
from collections import defaultdict
from apps.chart_management.processors import SimpleChartProcessor
from ..utils.svg_chart_generator import (
    CASTE_COLORS,
)  # Use a color palette or define DEATH_CAUSE_COLORS if needed


class DeathCauseProcessor(BaseDemographicsProcessor, SimpleChartProcessor):
    """Processor for death cause demographics"""

    def __init__(self):
        super().__init__()
        SimpleChartProcessor.__init__(self)
        from django.conf import settings

        if hasattr(settings, "STATICFILES_DIRS") and settings.STATICFILES_DIRS:
            self.static_charts_dir = (
                Path(settings.STATICFILES_DIRS[0]) / "images" / "charts"
            )
        else:
            self.static_charts_dir = Path(settings.STATIC_ROOT) / "images" / "charts"
        self.static_charts_dir.mkdir(parents=True, exist_ok=True)
        self.pie_chart_width = 900
        self.pie_chart_height = 450
        self.bar_chart_width = 1000
        self.bar_chart_height = 600
        self.chart_radius = 130
        self.chart_generator.colors = CASTE_COLORS  # Or DEATH_CAUSE_COLORS if defined

    def get_section_title(self):
        return "मृत्युको कारण अनुसार मृतकको संख्या"

    def get_section_number(self):
        return "३.१२.घ"

    def get_data(self):
        # Municipality-wide summary
        cause_types = {k: v for k, v in DeathCauseChoice.choices}
        cause_data = {}
        for cause_code, cause_name in cause_types.items():
            cause_data[cause_code] = {
                "population": 0,
                "percentage": 0.0,
                "name_nepali": cause_name,
                "ward_populations": [],  # Will be filled after ward_data is built
            }
        # Ward-wise data for bar chart and detailed table
        ward_data = {}
        ward_numbers = sorted(
            set(WardWiseDeathCause.objects.values_list("ward_number", flat=True))
        )
        for ward_num in ward_numbers:
            ward_data[ward_num] = {
                "ward_name": f"वडा नं. {ward_num}",
                "demographics": {},
                "total_population": 0,
            }
            for cause_code, cause_name in cause_types.items():
                ward_data[ward_num]["demographics"][cause_code] = {
                    "population": 0,
                    "name_nepali": cause_name,
                    "percentage": 0.0,
                }
        total_population = 0
        for obj in WardWiseDeathCause.objects.all():
            cause = obj.death_cause
            ward_num = obj.ward_number
            population = obj.population
            nepali_name = cause_types.get(cause, cause)
            # Municipality-wide
            if cause in cause_data:
                cause_data[cause]["population"] += population
            else:
                cause_data[cause] = {
                    "population": population,
                    "name_nepali": nepali_name,
                    "percentage": 0.0,
                    "ward_populations": [],
                }
            # Ward-wise
            if ward_num in ward_data:
                ward_data[ward_num]["demographics"][cause]["population"] += population
                ward_data[ward_num]["total_population"] += population
            total_population += population
        # Calculate percentages for municipality-wide data
        if total_population > 0:
            for cause, data in cause_data.items():
                data["percentage"] = (
                    (data["population"] / total_population) * 100
                    if total_population
                    else 0
                )
        # Calculate ward totals and percentages
        for ward_num, ward_info in ward_data.items():
            ward_total = ward_info["total_population"]
            for cause, data in ward_info["demographics"].items():
                data["percentage"] = (
                    (data["population"] / ward_total) * 100 if ward_total else 0
                )
        # Precompute ward_populations for each cause for easy template rendering
        for cause_code in cause_data:
            cause_data[cause_code]["ward_populations"] = [
                ward_data[ward_num]["demographics"][cause_code]["population"]
                for ward_num in ward_numbers
            ]
        # Limit to top 10 causes, aggregate others as 'अन्य'
        sorted_causes = sorted(
            cause_data.items(), key=lambda x: x[1]["population"], reverse=True
        )
        top_causes = sorted_causes[:10]
        other_causes = sorted_causes[10:]
        if other_causes:
            other_population = sum(c[1]["population"] for c in other_causes)
            other_ward_populations = [0 for _ in ward_numbers]
            for idx, ward_num in enumerate(ward_numbers):
                other_ward_populations[idx] = sum(
                    c[1]["ward_populations"][idx] for c in other_causes
                )
            other_percentage = (
                (other_population / total_population) * 100 if total_population else 0
            )
            other_entry = {
                "population": other_population,
                "percentage": other_percentage,
                "name_nepali": "अन्य",
                "ward_populations": other_ward_populations,
            }
            top_causes.append(("OTHER", other_entry))
        # Rebuild cause_data with only top 10 + 'अन्य'
        cause_data_limited = {k: v for k, v in top_causes}
        return {
            "municipality_data": cause_data_limited,
            "ward_data": ward_data,
            "ward_numbers": ward_numbers,
            "total_population": total_population,
        }

    def generate_report_content(self, data):
        formatter = self.DeathCauseReportFormatter()
        return formatter.generate_formal_report(
            data["municipality_data"], data["ward_data"], data["total_population"]
        )

    class DeathCauseReportFormatter(BaseReportFormatter):
        def generate_formal_report(self, cause_data, ward_data, total_population):
            from apps.reports.utils.nepali_numbers import (
                format_nepali_number,
                format_nepali_percentage,
            )

            lines = []
            nepali_total = format_nepali_number(total_population)
            sorted_causes = sorted(
                cause_data.items(), key=lambda x: x[1]["population"], reverse=True
            )
            major_causes = [
                (data["name_nepali"], data["population"], data["percentage"])
                for cause, data in sorted_causes
                if data["population"] > 0
            ]
            # Compose a continuous, formal Nepali analysis
            if not major_causes:
                return "गत १२ महिनामा मृत्युको कारणसम्बन्धी कुनै तथ्याङ्क उपलब्ध छैन ।"
            # Top 3 causes
            intro = f"गढवा गाउँपालिकामा विगत १२ महिनामा जम्मा {nepali_total} जनाको मृत्यु भएको छ । मृत्युका प्रमुख कारणहरूमा "
            if len(major_causes) >= 3:
                first, second, third = major_causes[:3]
                intro += f"{first[0]} ({format_nepali_number(first[1])} जना, {format_nepali_percentage(first[2])}%), {second[0]} ({format_nepali_number(second[1])} जना, {format_nepali_percentage(second[2])}%) र {third[0]} ({format_nepali_number(third[1])} जना, {format_nepali_percentage(third[2])}%) रहेका छन् । "
            elif len(major_causes) == 2:
                first, second = major_causes[:2]
                intro += f"{first[0]} ({format_nepali_number(first[1])} जना, {format_nepali_percentage(first[2])}%) र {second[0]} ({format_nepali_number(second[1])} जना, {format_nepali_percentage(second[2])}%) रहेका छन् । "
            else:
                first = major_causes[0]
                intro += f"{first[0]} ({format_nepali_number(first[1])} जना, {format_nepali_percentage(first[2])}%) प्रमुख रहेको छ । "
            # Other causes
            if len(major_causes) > 3:
                intro += "अन्य कारणहरूमा "
                intro += " ".join(
                    [
                        f"{name} ({format_nepali_number(pop)} जना, {format_nepali_percentage(pct)}%)"
                        for name, pop, pct in major_causes[3:]
                    ]
                )
                intro += " समेत रहेका छन् । "
            lines.append(intro)
            # Trend and interpretation
            lines.append(
                "समग्र तथ्याङ्कको विश्लेषण गर्दा दीर्घरोग, उमेरजन्य कारण, सरुवा रोग, दुर्घटना, र अन्य स्वास्थ्यसम्बन्धी समस्याहरू मृत्युका मुख्य कारकका रूपमा देखिएका छन् । दीर्घरोग तथा उमेरजन्य कारणले मृत्यु हुनेको संख्या उच्च हुनुमा अस्वस्थकर जीवनशैली, खानपानको असन्तुलन, नियमित व्यायामको अभाव, मानसिक स्वास्थ्यमा सजगताको कमी, वंशाणुगत कारण तथा समयमै स्वास्थ्य जाँच नगराउने परिपाटी जस्ता पक्षहरू जिम्मेवार देखिन्छन् । सरुवा रोगका कारण बालबालिका तथा युवा उमेर समूहमा मृत्यु भएको पाइन्छ, जसको मुख्य कारण व्यक्तिगत, पारिवारिक तथा सामुदायिक सरसफाई, पोषण, खोप, नियमित स्वास्थ्य जाँच, उपचार पहुँच र स्वास्थ्य सेवाको उपलब्धतामा कमी हुनसक्छ । दुर्घटनाका घटनाहरूले पनि मृत्युको दरमा उल्लेख्य योगदान पुर्याएको छ, जसमा सडक दुर्घटना, घरेलु दुर्घटना, डुबान, आगलागी आदि समावेश छन् ।"
            )
            # Ward-wise diversity
            lines.append(
                "वडागत रूपमा मृत्युका कारणमा विविधता देखिन्छ । केही वडामा दीर्घरोग तथा उमेरजन्य कारण प्रमुख देखिएका छन् भने अन्य वडामा सरुवा रोग, दुर्घटना वा अन्य कारणले मृत्यु भएको छ । यसले स्वास्थ्य सेवा पहुँच, जनचेतना, जीवनशैली, तथा जोखिम न्यूनीकरणका उपायहरूमा वडागत भिन्नता रहेको संकेत गर्छ ।"
            )
            # Policy implication
            lines.append(
                "मृत्यु न्यूनीकरणका लागि गाउँपालिकाले नियमित स्वास्थ्य परीक्षण, पोषणयुक्त आहार, सरसफाई, खोप, व्यायाम, मानसिक स्वास्थ्यमा ध्यान, समयमै उपचारको पहुँच, जोखिम न्यूनीकरण, र स्वास्थ्य शिक्षा प्रवर्द्धनमा विशेष ध्यान दिनुपर्ने देखिन्छ ।"
            )
            # Social protection
            lines.append(
                "स्वास्थ्य बीमा, सामाजिक सुरक्षा तथा जोखिम न्यूनीकरणका कार्यक्रमहरू सञ्चालन गरी मृत्युका कारण घटाउने रणनीति अवलम्बन गर्नुपर्ने आवश्यकता छ । दीर्घरोग तथा सरुवा रोगको रोकथाम, दुर्घटनाको न्यूनीकरण, र स्वास्थ्य सेवाको पहुँच अभिवृद्धि गर्न सामुदायिक सहभागिता र सरकारी नीति प्रभावकारी रूपमा कार्यान्वयन गर्नुपर्ने देखिन्छ ।"
            )
            # Table reference
            lines.append("मृत्युको कारणसम्बन्धी विस्तृत विवरण निम्न तालिकामा प्रस्तुत गरिएको छ ।")
            return " ".join(lines)

    def get_chart_key(self):
        return "demographics_death_cause"

    def _get_chart_data(self, municipality_data):
        """
        Returns a dict of {Nepali name: population} for top 10 causes plus 'अन्य' (Other),
        suitable for pie/bar chart rendering. Ensures 'अन्य' is always at the end if present.
        """
        # Sort by population descending
        sorted_items = sorted(
            municipality_data.items(), key=lambda x: x[1]["population"], reverse=True
        )
        chart_data = {}
        count = 0
        for cause, info in sorted_items:
            if cause == "OTHER":
                continue  # Add at the end
            if count < 10:
                chart_data[info["name_nepali"]] = info["population"]
                count += 1
        # Add 'अन्य' if present
        for cause, info in sorted_items:
            if cause == "OTHER":
                chart_data[info["name_nepali"]] = info["population"]
        return chart_data

    def generate_chart_svg(self, data, chart_type="pie"):
        chart_data = self._get_chart_data(data["municipality_data"])
        if chart_type == "pie":
            return self.chart_generator.generate_pie_chart_svg(
                chart_data,
                include_title=False,
                title_nepali="मृत्युको कारण अनुसार मृतकको जनसंख्या वितरण",
                title_english="Population Distribution by Death Cause",
            )
        elif chart_type == "bar":
            return self.chart_generator.generate_bar_chart_svg(
                chart_data,
                include_title=False,
                title_nepali="मृत्युको कारण अनुसार मृतकको जनसंख्या वितरण",
                title_english="Population Distribution by Death Cause",
            )
        return None

    def generate_and_track_charts(self, data):
        charts = {}
        self.static_charts_dir.mkdir(parents=True, exist_ok=True)
        chart_data = self._get_chart_data(data["municipality_data"])
        if self.needs_generation("pie"):
            print(f"🔄 Generating death cause pie chart...")
            success, png_path, svg_path = self.chart_generator.generate_chart_image(
                demographic_data=chart_data,
                output_name="death_cause_pie_chart",
                static_dir=str(self.static_charts_dir),
                chart_type="pie",
                include_title=False,
            )
            if success and png_path:
                charts["pie_chart_url"] = f"images/charts/death_cause_pie_chart.png"
            elif svg_path:
                charts["pie_chart_url"] = f"images/charts/death_cause_pie_chart.svg"
        else:
            charts["pie_chart_url"] = f"images/charts/death_cause_pie_chart.png"
            print(f"✅ Death cause pie chart already exists")
        if self.needs_generation("bar"):
            print(f"🔄 Generating death cause bar chart...")
            success, png_path, svg_path = self.chart_generator.generate_chart_image(
                demographic_data=chart_data,
                output_name="death_cause_bar_chart",
                static_dir=str(self.static_charts_dir),
                chart_type="bar",
                include_title=False,
            )
            if success and png_path:
                charts["bar_chart_url"] = f"images/charts/death_cause_bar_chart.png"
            elif svg_path:
                charts["bar_chart_url"] = f"images/charts/death_cause_bar_chart.svg"
        else:
            charts["bar_chart_url"] = f"images/charts/death_cause_bar_chart.png"
            print(f"✅ Death cause bar chart already exists")
        return charts

    def generate_and_save_charts(self, data):
        return self.generate_and_track_charts(data)

    def process_for_pdf(self):
        data = self.get_data()
        report_content = self.generate_report_content(data)
        charts = self.generate_and_track_charts(data)
        total_population = data.get("total_population", 0)
        return {
            "data": data,
            "municipality_data": data["municipality_data"],
            "ward_data": data["ward_data"],
            "report_content": report_content,
            "coherent_analysis": report_content,
            "charts": charts,
            "total_population": total_population,
            "section_title": self.get_section_title(),
            "section_number": self.get_section_number(),
        }
