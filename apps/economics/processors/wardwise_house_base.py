"""
Ward Wise House Base Economics Processor

Handles ward wise house base type data processing, chart generation, and report formatting.
"""

from .base import BaseEconomicsProcessor, BaseEconomicsReportFormatter
from ..models import WardWiseHouseholdBase, HouseholdBaseTypeChoice
from apps.demographics.utils.svg_chart_generator import DEFAULT_COLORS
from apps.reports.utils.nepali_numbers import (
    format_nepali_number,
    format_nepali_percentage,
)


class WardWiseHouseBaseProcessor(BaseEconomicsProcessor):
    """Processor for ward wise house base type data"""

    def __init__(self):
        super().__init__()
        self.pie_chart_width = 900
        self.pie_chart_height = 450
        self.bar_chart_width = 1000
        self.bar_chart_height = 600
        self.chart_radius = 130
        self.chart_generator.colors = {
            "CEMENT_JOINED": "#4CAF50",
            "CONCRETE_PILLAR": "#2196F3",
            "MUD_JOINED": "#FFC107",
            "WOOD_POLE": "#795548",
            "OTHER": "#9E9E9E",
        }

    def get_section_title(self):
        return "जगको आधारमा घरधुरीको विवरण"

    def get_section_number(self):
        return "४.१.८"

    def get_data(self):
        municipality_data = {}
        base_types = dict(HouseholdBaseTypeChoice.choices)
        nepali_names = {code: name for code, name in base_types.items()}
        for code, name in base_types.items():
            municipality_data[code] = {"name": name, "households": 0, "percentage": 0}
        # Dynamically determine all ward numbers from the data
        all_wards = sorted(
            set(WardWiseHouseholdBase.objects.values_list("ward_number", flat=True))
        )
        ward_data = {}
        for ward_num in all_wards:
            ward_data[ward_num] = {
                code: {"name": name, "households": 0, "percentage": 0}
                for code, name in base_types.items()
            }
        total_households = 0
        for obj in WardWiseHouseholdBase.objects.all():
            municipality_data[obj.base_type]["households"] += obj.households
            ward_data[obj.ward_number][obj.base_type]["households"] += obj.households
            total_households += obj.households
        if total_households > 0:
            for code in base_types:
                if municipality_data[code]["households"] > 0:
                    municipality_data[code]["percentage"] = (
                        municipality_data[code]["households"] / total_households * 100
                    )
            for ward_num in ward_data:
                ward_total = sum(
                    ward_data[ward_num][code]["households"] for code in base_types
                )
                for code in base_types:
                    if ward_total > 0:
                        ward_data[ward_num][code]["percentage"] = (
                            ward_data[ward_num][code]["households"] / ward_total * 100
                        )
                ward_data[ward_num]["total_households"] = ward_total
        # For charting: use Nepali names as keys
        pie_chart_data = {
            v["name"]: v["households"] for k, v in municipality_data.items()
        }
        bar_chart_data = {}
        for ward_num, ward_info in ward_data.items():
            bar_chart_data[str(ward_num)] = {
                v["name"]: v["households"]
                for k, v in ward_info.items()
                if k in base_types
            }
        return {
            "municipality_data": municipality_data,
            "ward_data": ward_data,
            "total_households": total_households,
            "pie_chart_data": pie_chart_data,
            "bar_chart_data": bar_chart_data,
        }

    def generate_report_content(self, data):
        formatter = self.WardWiseHouseBaseReportFormatter()
        return formatter.generate_formal_report(
            data["municipality_data"], data["ward_data"], data["total_households"]
        )

    def get_chart_key(self):
        return "wardwise_house_base"

    def generate_chart_svg(self, data, chart_type="pie"):
        if chart_type == "pie":
            return self.chart_generator.generate_chart_svg(
                demographic_data=data["pie_chart_data"],
                chart_type="pie",
                width=self.pie_chart_width,
                height=self.pie_chart_height,
                radius=self.chart_radius,
            )
        elif chart_type == "bar":
            return self.chart_generator.generate_chart_svg(
                demographic_data=data["bar_chart_data"],
                chart_type="bar",
                width=self.bar_chart_width,
                height=self.bar_chart_height,
            )
        return None

    def generate_and_save_charts(self, data):
        charts = {}
        category_name = "wardwise_house_base"
        # Use Nepali names for chart keys
        pie_data = data["pie_chart_data"]
        bar_data = data["bar_chart_data"]
        # Pie chart
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
        # Bar chart
        if bar_data:
            success, png_path, svg_path = self.chart_generator.generate_chart_image(
                demographic_data=bar_data,
                output_name=f"{category_name}_bar_chart",
                static_dir=str(self.static_charts_dir),
                chart_type="bar",
                include_title=False,
            )
            if success and png_path:
                charts["bar"] = png_path
            elif svg_path:
                charts["bar"] = svg_path
        return charts

    class WardWiseHouseBaseReportFormatter(BaseEconomicsReportFormatter):
        def generate_formal_report(
            self, municipality_data, ward_data, total_households
        ):
            cement = municipality_data.get("CEMENT_JOINED", {})
            concrete = municipality_data.get("CONCRETE_PILLAR", {})
            mud = municipality_data.get("MUD_JOINED", {})
            wood = municipality_data.get("WOOD_POLE", {})
            other = municipality_data.get("OTHER", {})
            cement_count = cement.get("households", 0)
            concrete_count = concrete.get("households", 0)
            mud_count = mud.get("households", 0)
            wood_count = wood.get("households", 0)
            other_count = other.get("households", 0)
            cement_pct = format_nepali_percentage(
                (cement_count / total_households * 100) if total_households else 0
            )
            concrete_pct = format_nepali_percentage(
                (concrete_count / total_households * 100) if total_households else 0
            )
            mud_pct = format_nepali_percentage(
                (mud_count / total_households * 100) if total_households else 0
            )
            wood_pct = format_nepali_percentage(
                (wood_count / total_households * 100) if total_households else 0
            )
            other_pct = format_nepali_percentage(
                (other_count / total_households * 100) if total_households else 0
            )
            lines = [
                "यस गाउँपालिकामा घरको जगको आधारमा विभिन्न प्रकारका संरचनाहरू निर्माण भएका छन् । सिमेन्ट जोडिएको जगमा रहेका घरधुरी {0} ({1}), कङ्क्रिट पिलरमा आधारित {2} ({3}), माटो जोडिएको जगमा {4} ({5}), काठ/डाँडाको जगमा {6} ({7}) र अन्यमा {8} ({9}) घरधुरी रहेका छन् ।".format(
                    format_nepali_number(cement_count),
                    cement_pct,
                    format_nepali_number(concrete_count),
                    concrete_pct,
                    format_nepali_number(mud_count),
                    mud_pct,
                    format_nepali_number(wood_count),
                    wood_pct,
                    format_nepali_number(other_count),
                    other_pct,
                )
                + " "
                + "माटो जोडिएको जगमा घर बनाउने परम्परा अझै प्रचलित देखिन्छ, जसले भूकम्पीय जोखिम बढाउँछ । सिमेन्ट र कङ्क्रिट पिलरमा आधारित जगको प्रयोग बढ्दै गएको छ, जसले सुरक्षित आवास निर्माणमा सकारात्मक संकेत दिन्छ । "
                + "काठ/डाँडाको जग तथा अन्य प्रकारका जगमा रहेका घरधुरीको संख्या न्यून भए पनि, यी घरपरिवारका लागि सुरक्षित आवास प्रवर्द्धन गर्न आवश्यक छ । "
                + "भूकम्प प्रतिरोधात्मक प्रविधिको प्रयोग, सरकारी अनुदान तथा प्रवर्द्धन कार्यक्रमद्वारा सुरक्षित आवास निर्माणमा जोड दिनुपर्ने देखिन्छ । "
                + "स्थानीय तहले आवास सुरक्षामा प्राथमिकता दिँदै, माटो जोडिएको जगमा बसोबास गर्ने घरधुरीका लागि लक्षित कार्यक्रम सञ्चालन गर्नुपर्ने आवश्यकता छ । "
                + "आवासको जगको विविधता स्थानीय स्रोत, परम्परा र आर्थिक अवस्थासँग सम्बन्धित छ । दीर्घकालीन आवास सुरक्षाका लागि सुरक्षित र दिगो प्रविधिको प्रवर्द्धन गर्नुपर्छ ।"
            ]
            return "\n\n".join(lines)
