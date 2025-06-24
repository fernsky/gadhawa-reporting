"""
Ward Wise House Ownership Economics Processor

Handles ward wise house ownership data processing, chart generation, and report formatting.
"""

from .base import BaseEconomicsProcessor, BaseEconomicsReportFormatter
from ..models import WardWiseHouseOwnership, HouseOwnershipTypeChoice
from apps.demographics.utils.svg_chart_generator import DEFAULT_COLORS
from apps.reports.utils.nepali_numbers import (
    format_nepali_number,
    format_nepali_percentage,
)


class WardWiseHouseOwnershipProcessor(BaseEconomicsProcessor):
    """Processor for ward wise house ownership data"""

    def __init__(self):
        super().__init__()
        self.pie_chart_width = 900
        self.pie_chart_height = 450
        self.bar_chart_width = 1000
        self.bar_chart_height = 600
        self.chart_radius = 130
        self.chart_generator.colors = {
            "PRIVATE": "#4CAF50",
            "RENT": "#2196F3",
            "INSTITUTIONAL": "#FFC107",
            "OTHER": "#9E9E9E",
        }

    def get_section_title(self):
        return "घरको स्वामित्वको आधारमा घरधुरीको विवरण"

    def get_section_number(self):
        return "४.१.७"

    def get_data(self):
        municipality_data = {}
        ownership_types = dict(HouseOwnershipTypeChoice.choices)
        nepali_names = {code: name for code, name in ownership_types.items()}
        for code, name in ownership_types.items():
            municipality_data[code] = {"name": name, "households": 0, "percentage": 0}
        ward_data = {}
        # Update: support wards 1-8 (not just 1-7)
        for ward_num in range(1, 9):
            ward_data[ward_num] = {
                code: {"name": name, "households": 0, "percentage": 0}
                for code, name in ownership_types.items()
            }
        total_households = 0
        for obj in WardWiseHouseOwnership.objects.all():
            # Only count valid ownership types
            if obj.ownership_type in ownership_types:
                municipality_data[obj.ownership_type]["households"] += obj.households
                ward_data[obj.ward_number][obj.ownership_type][
                    "households"
                ] += obj.households
                total_households += obj.households
        if total_households > 0:
            for code in ownership_types:
                municipality_data[code]["percentage"] = round(
                    (municipality_data[code]["households"] / total_households) * 100, 2
                )
            for ward_num in ward_data:
                ward_total = sum(
                    [
                        ward_data[ward_num][code]["households"]
                        for code in ownership_types
                    ]
                )
                ward_data[ward_num]["total_households"] = ward_total
                if ward_total > 0:
                    for code in ownership_types:
                        ward_data[ward_num][code]["percentage"] = round(
                            (ward_data[ward_num][code]["households"] / ward_total)
                            * 100,
                            2,
                        )
        # For charting: use Nepali names as keys
        pie_chart_data = {
            v["name"]: v["households"] for k, v in municipality_data.items()
        }
        bar_chart_data = {}
        for ward_num, ward_info in ward_data.items():
            bar_chart_data[str(ward_num)] = {
                v["name"]: v["households"]
                for k, v in ward_info.items()
                if k in ownership_types
            }
        return {
            "municipality_data": municipality_data,
            "ward_data": ward_data,
            "total_households": total_households,
            "pie_chart_data": pie_chart_data,
            "bar_chart_data": bar_chart_data,
        }

    def generate_report_content(self, data):
        formatter = self.WardWiseHouseOwnershipReportFormatter()
        return formatter.generate_formal_report(
            data["municipality_data"], data["ward_data"], data["total_households"]
        )

    def get_chart_key(self):
        return "wardwise_house_ownership"

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
        category_name = "wardwise_house_ownership"
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

    class WardWiseHouseOwnershipReportFormatter(BaseEconomicsReportFormatter):
        def generate_formal_report(
            self, municipality_data, ward_data, total_households
        ):
            private = municipality_data.get("PRIVATE", {})
            rent = municipality_data.get("RENT", {})
            institutional = municipality_data.get("INSTITUTIONAL", {})
            other = municipality_data.get("OTHER", {})
            private_count = private.get("households", 0)
            rent_count = rent.get("households", 0)
            institutional_count = institutional.get("households", 0)
            other_count = other.get("households", 0)

            private_pct = format_nepali_percentage(
                (private_count / total_households * 100) if total_households else 0
            )
            rent_pct = format_nepali_percentage(
                (rent_count / total_households * 100) if total_households else 0
            )
            institutional_pct = format_nepali_percentage(
                (institutional_count / total_households * 100)
                if total_households
                else 0
            )

            lines = [
                f"गढवा गाउँपालिकामा घरधुरी स्वामित्वको विश्लेषण गर्दा, कुल घरधुरीमध्ये {format_nepali_number(private_count)} ({private_pct}) निजी स्वामित्वमा रहेका छन्, जुन अत्यधिक बहुमत हो।",
                f"भाडामा बस्ने घरधुरी {format_nepali_number(rent_count)} ({rent_pct}) छन्, जसले शहरीकरण र आवासको पहुँचमा विविधता देखाउँछ।",
                f"संस्थागत स्वामित्वमा रहेका घरधुरी {format_nepali_number(institutional_count)} ({institutional_pct}) मात्र छन्, जुन मुख्यतया केही वडामा सीमित छन्।",
                "अन्य स्वामित्वका घरधुरी हालको तथ्याङ्कमा उल्लेखनीय रूपमा देखिएका छैनन्।",
                "निजी स्वामित्वको उच्च अनुपातले आर्थिक स्थायित्व, दीर्घकालीन लगानी, र स्थानीय स्वामित्वको भावना झल्काउँछ। भाडामा र संस्थागत घरधुरीको उपस्थिति रोजगारी, आवासको आवश्यकता, र सामाजिक गतिशीलतासँग सम्बन्धित छ।",
                "स्थानीय तहले आवास सुरक्षामा जोड दिँदै, सबै वर्गका नागरिकका लागि समावेशी र दिगो आवास नीति निर्माण गर्नुपर्ने आवश्यकता देखिन्छ।",
            ]
            return "\n\n".join(lines)

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
