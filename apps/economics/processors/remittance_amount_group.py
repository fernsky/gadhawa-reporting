"""
Remittance Amount Group Economics Processor

Handles remittance amount group data processing, chart generation, and report formatting.
"""

from .base import BaseEconomicsProcessor, BaseEconomicsReportFormatter
from ..models import WardWiseRemittance, RemittanceAmountGroupChoice
from apps.demographics.utils.svg_chart_generator import DEFAULT_COLORS
from apps.reports.utils.nepali_numbers import (
    format_nepali_number,
    format_nepali_percentage,
)


class RemittanceAmountGroupProcessor(BaseEconomicsProcessor):
    """Processor for remittance amount group data"""

    def __init__(self):
        super().__init__()
        self.pie_chart_width = 900
        self.pie_chart_height = 450
        self.bar_chart_width = 1000
        self.bar_chart_height = 600
        self.chart_radius = 130
        self.chart_generator.colors = {
            "RS_0_TO_49999": "#BDBDBD",
            "RS_50000_TO_99999": "#2196F3",
            "RS_100000_TO_149999": "#4CAF50",
            "RS_150000_TO_199999": "#FFC107",
            "RS_200000_TO_249999": "#F44336",
            "RS_250000_TO_299999": "#9C27B0",
            "RS_300000_TO_349999": "#00BCD4",
            "RS_350000_TO_399999": "#795548",
            "RS_400000_TO_449999": "#607D8B",
            "RS_450000_TO_499999": "#8BC34A",
            "RS_500000_PLUS": "#3F51B5",
        }

    def get_section_title(self):
        return (
            "विगत १२ महिनामा वैदेशिक रोजगारीमा गएका मध्येबाट आम्दानी गरी रकम पठाउनेको विवरण"
        )

    def get_section_number(self):
        return "४.३"

    def get_data(self):
        municipality_data = {}
        group_choices = dict(RemittanceAmountGroupChoice.choices)
        for group_code, group_name in group_choices.items():
            municipality_data[group_code] = {
                "sending_population": 0,
                "percentage": 0.0,
                "name_nepali": group_name,
            }

        # Dynamically determine all ward numbers from the data
        all_wards = sorted(
            set(WardWiseRemittance.objects.values_list("ward_number", flat=True))
        )
        ward_data = {}
        for ward_num in all_wards:
            ward_data[ward_num] = {
                "ward_name": f"वडा नं. {ward_num}",
                "amount_groups": {},
            }
            for group_code, group_name in group_choices.items():
                ward_data[ward_num]["amount_groups"][group_code] = {
                    "sending_population": 0,
                    "name_nepali": group_name,
                }

        total_sending_population = 0
        for obj in WardWiseRemittance.objects.all():
            group = obj.amount_group
            ward_num = obj.ward_number
            sending_population = obj.sending_population

            if group in municipality_data:
                municipality_data[group]["sending_population"] += sending_population
            if ward_num in ward_data and group in ward_data[ward_num]["amount_groups"]:
                ward_data[ward_num]["amount_groups"][group][
                    "sending_population"
                ] += sending_population

            total_sending_population += sending_population

        if total_sending_population > 0:
            for group, data in municipality_data.items():
                data["percentage"] = (
                    data["sending_population"] / total_sending_population
                ) * 100

        for ward_num, ward_info in ward_data.items():
            ward_total = sum(
                group["sending_population"]
                for group in ward_info["amount_groups"].values()
            )
            ward_info["total_sending_population"] = ward_total

        return {
            "municipality_data": municipality_data,
            "ward_data": ward_data,
            "total_sending_population": total_sending_population,
        }

    def generate_report_content(self, data):
        formatter = self.RemittanceAmountGroupReportFormatter()
        return formatter.generate_formal_report(
            data["municipality_data"],
            data["ward_data"],
            data["total_sending_population"],
        )

    def get_chart_key(self):
        return "remittance_amount_group"

    def generate_chart_svg(self, data, chart_type="pie"):
        if chart_type == "pie":
            pie_data = {
                k: v["sending_population"] for k, v in data["municipality_data"].items()
            }
            return self.chart_generator.generate_pie_chart_svg(
                pie_data, include_title=False
            )
        elif chart_type == "bar":
            bar_data = {}
            for ward_num, ward_info in data["ward_data"].items():
                for group, group_data in ward_info["amount_groups"].items():
                    if group not in bar_data:
                        bar_data[group] = []
                    bar_data[group].append(group_data["sending_population"])
            return self.chart_generator.generate_bar_chart_svg(
                bar_data, include_title=False
            )
        return None

    def generate_and_save_charts(self, data):
        charts = {}
        category_name = "remittance_amount_group"
        pie_data = {
            k: v["sending_population"] for k, v in data["municipality_data"].items()
        }
        bar_data = {}
        for group in data["municipality_data"].keys():
            bar_data[group] = [
                data["ward_data"][ward_num]["amount_groups"][group][
                    "sending_population"
                ]
                for ward_num in sorted(data["ward_data"].keys())
            ]
        success, png_path, svg_path = self.chart_generator.generate_chart_image(
            demographic_data=pie_data,
            output_name=f"{category_name}_pie_chart",
            static_dir=str(self.static_charts_dir),
            chart_type="pie",
            include_title=False,
        )
        if success and png_path:
            charts["pie_chart"] = png_path
        elif svg_path:
            charts["pie_chart"] = svg_path
        if bar_data:
            success, png_path, svg_path = self.chart_generator.generate_chart_image(
                demographic_data=bar_data,
                output_name=f"{category_name}_bar_chart",
                static_dir=str(self.static_charts_dir),
                chart_type="bar",
                include_title=False,
            )
            if success and png_path:
                charts["bar_chart"] = png_path
            elif svg_path:
                charts["bar_chart"] = svg_path
        return charts

    class RemittanceAmountGroupReportFormatter(BaseEconomicsReportFormatter):
        def generate_formal_report(
            self, municipality_data, ward_data, total_sending_population
        ):
            if total_sending_population == 0:
                return "गत वर्ष कुनै पनि वडाबाट रकम पठाउने जनसंख्या छैन।"
            # Find the group with the highest sending population
            max_group = max(
                municipality_data.items(), key=lambda x: x[1]["sending_population"]
            )
            min_group = min(
                (
                    g
                    for g in municipality_data.items()
                    if g[1]["sending_population"] > 0
                ),
                key=lambda x: x[1]["sending_population"],
            )
            # Find the ward with the highest sending population in the highest group
            max_ward = None
            max_ward_count = 0
            for ward_num, ward_info in ward_data.items():
                count = ward_info["amount_groups"][max_group[0]]["sending_population"]
                if count > max_ward_count:
                    max_ward = ward_num
                    max_ward_count = count
            # Find the most common group overall
            sorted_groups = sorted(
                municipality_data.items(),
                key=lambda x: x[1]["sending_population"],
                reverse=True,
            )
            top_groups = [g for g in sorted_groups if g[1]["sending_population"] > 0][
                :3
            ]
            # Compose analysis
            analysis = []
            analysis.append(
                f"गत १२ महिनामा वैदेशिक रोजगारीमा गएका मध्येबाट रकम पठाउने जनसंख्या जम्मा {format_nepali_number(total_sending_population)} जना रहेका छन्।"
            )
            if max_ward:
                analysis.append(
                    f"सबैभन्दा बढी '{max_group[1]['name_nepali']}' पठाउने वडा नं. {format_nepali_number(max_ward)} मा {format_nepali_number(max_ward_count)} जना रहेका छन्।"
                )
            if min_group[1]["sending_population"] > 0:
                analysis.append(
                    f"सबैभन्दा कम '{min_group[1]['name_nepali']}' पठाउने जम्मा {format_nepali_number(min_group[1]['sending_population'])} जना रहेका छन्।"
                )
            if top_groups:
                group_lines = []
                for group_code, group_data in top_groups:
                    group_lines.append(
                        f"{group_data['name_nepali']} ({format_nepali_number(group_data['sending_population'])} जना, {format_nepali_percentage(group_data['percentage'])})"
                    )
                analysis.append(
                    "मुख्य तीन रकम समूहहरू: " + ", ".join(group_lines) + " रहेका छन्।"
                )
            return " ".join(analysis)
