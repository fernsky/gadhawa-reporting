"""
Ward Wise House Outer Wall Economics Processor

Handles ward wise house outer wall type data processing, chart generation, and report formatting.
"""

from .base import BaseEconomicsProcessor, BaseEconomicsReportFormatter
from ..models import WardWiseHouseholdOuterWall, OuterWallTypeChoice
from apps.demographics.utils.svg_chart_generator import DEFAULT_COLORS
from apps.reports.utils.nepali_numbers import (
    format_nepali_number,
    format_nepali_percentage,
)


class WardWiseHouseOuterWallProcessor(BaseEconomicsProcessor):
    """Processor for ward wise house outer wall type data"""

    def __init__(self):
        super().__init__()
        self.pie_chart_width = 900
        self.pie_chart_height = 450
        self.bar_chart_width = 1000
        self.bar_chart_height = 600
        self.chart_radius = 130
        self.chart_generator.colors = {
            "CEMENT_JOINED": "#2196F3",
            "UNBAKED_BRICK": "#B22222",
            "MUD_JOINED": "#FFC107",
            "TIN": "#8B4513",
            "BAMBOO": "#8BC34A",
            "WOOD": "#4CAF50",
            "PREFAB": "#9C27B0",
            "OTHER": "#607D8B",
        }

    def get_section_title(self):
        return "बाहिरी गारोको आधारमा घरधुरीको विवरण"

    def get_section_number(self):
        return "४.१.९"

    def get_data(self):
        municipality_data = {}
        wall_types = dict(OuterWallTypeChoice.choices)
        nepali_names = {code: name for code, name in wall_types.items()}
        for code, name in wall_types.items():
            municipality_data[code] = {"name": name, "households": 0, "percentage": 0}
        ward_data = {}
        for ward_num in range(1, 8):
            ward_data[ward_num] = {
                code: {"name": name, "households": 0, "percentage": 0}
                for code, name in wall_types.items()
            }
        total_households = 0
        for obj in WardWiseHouseholdOuterWall.objects.all():
            municipality_data[obj.wall_type]["households"] += obj.households
            ward_data[obj.ward_number][obj.wall_type]["households"] += obj.households
            total_households += obj.households
        if total_households > 0:
            for code in wall_types:
                municipality_data[code]["percentage"] = round(
                    municipality_data[code]["households"] * 100 / total_households, 1
                )
            for ward_num in ward_data:
                ward_total = sum(
                    ward_data[ward_num][code]["households"] for code in wall_types
                )
                for code in wall_types:
                    if ward_total > 0:
                        ward_data[ward_num][code]["percentage"] = round(
                            ward_data[ward_num][code]["households"] * 100 / ward_total,
                            1,
                        )
                    else:
                        ward_data[ward_num][code]["percentage"] = 0
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
                if k in wall_types
            }
        return {
            "municipality_data": municipality_data,
            "ward_data": ward_data,
            "total_households": total_households,
            "pie_chart_data": pie_chart_data,
            "bar_chart_data": bar_chart_data,
        }

    def generate_report_content(self, data):
        formatter = self.WardWiseHouseOuterWallReportFormatter()
        return formatter.generate_formal_report(
            data["municipality_data"], data["ward_data"], data["total_households"]
        )

    def get_chart_key(self):
        return "wardwise_house_outer_wall"

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
        category_name = "wardwise_house_outer_wall"
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

    class WardWiseHouseOuterWallReportFormatter(BaseEconomicsReportFormatter):
        def generate_formal_report(
            self, municipality_data, ward_data, total_households
        ):
            wall_types = [
                ("CEMENT_JOINED", "सिमेन्ट जोडिएको"),
                ("UNBAKED_BRICK", "काच्ची इँट"),
                ("MUD_JOINED", "माटो जोडिएको"),
                ("TIN", "पाता"),
                ("BAMBOO", "बाँस"),
                ("WOOD", "काठ"),
                ("PREFAB", "प्रिफ्याब"),
                ("OTHER", "अन्य"),
            ]
            used_types = []
            for code, nepali in wall_types:
                count = municipality_data.get(code, {}).get("households", 0)
                percent = municipality_data.get(code, {}).get("percentage", 0)
                if count > 0:
                    used_types.append((nepali, count, percent, code))
            # Compose the main sentence
            if used_types:
                type_strs = [
                    f"{nepali} गारो भएका {format_nepali_number(count)} ({format_nepali_percentage(percent)}) घरधुरी"
                    for nepali, count, percent, code in used_types
                ]
                main_sentence = (
                    f"लुङ्ग्री गाउँपालिकामा बाहिरी गारोको आधारमा घरधुरीको विवरण हेर्दा, कुल {format_nepali_number(total_households)} घरधुरीमध्ये "
                    + "; ".join(type_strs)
                    + " रहेका छन् ।"
                )
            else:
                main_sentence = (
                    f"लुङ्ग्री गाउँपालिकामा बाहिरी गारोको आधारमा कुनै घरधुरी विवरण उपलब्ध छैन ।"
                )
            # Compose analysis
            traditional = [
                c
                for c in used_types
                if c[3] in ("MUD_JOINED", "BAMBOO", "WOOD", "UNBAKED_BRICK")
            ]
            modern = [
                c for c in used_types if c[3] in ("CEMENT_JOINED", "PREFAB", "TIN")
            ]
            analysis = ""
            if traditional:
                analysis += " परम्परागत निर्माण सामग्री (जस्तै माटो, काठ, बाँस, काच्ची इँट) को प्रयोग अझै प्रचलनमा रहेको देखिन्छ, जसले स्थानीय स्रोत र परम्परागत सीपको निरन्तरता जनाउँछ।"
            if modern:
                analysis += " आधुनिक सामग्री (सिमेन्ट, प्रिफ्याब, पाता) को प्रयोग बढ्दो छ, जसले सुरक्षित र दिगो आवास निर्माणमा सकारात्मक संकेत दिन्छ।"
            if any(c[3] == "MUD_JOINED" for c in used_types):
                analysis += " माटो जोडिएको गारो भएका घरधुरीको उच्च प्रतिशतले भूकम्पीय जोखिम बढाउने सम्भावना देखिन्छ, त्यसैले सुरक्षित आवास प्रवर्द्धनका लागि सरकारी तथा स्थानीय तहको ध्यान आवश्यक छ।"
            if any(c[3] == "CEMENT_JOINED" for c in used_types):
                analysis += " सिमेन्ट जोडिएको गारो भएका घरधुरीको संख्या उल्लेख्य छ, जसले सुरक्षित आवास निर्माणमा सकारात्मक प्रवृत्ति देखाउँछ।"
            analysis += " स्थानीय स्रोत, परम्परा र आर्थिक अवस्थाका आधारमा गारोको विविधता देखिन्छ। दीर्घकालीन आवास सुरक्षाका लागि सुरक्षित र दिगो प्रविधिको प्रवर्द्धन गर्नुपर्छ।"
            return main_sentence + "\n\n" + analysis

    def process_for_pdf(self):
        data = self.get_data()
        report_content = self.generate_report_content(data)
        charts = self.generate_and_save_charts(data)
        return {
            "data": data,
            "report_content": report_content,
            "charts": charts,
            "total_households": data["total_households"],
            "section_title": self.get_section_title(),
            "section_number": self.get_section_number(),
        }
