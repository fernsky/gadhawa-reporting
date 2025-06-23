"""
Ward Household Demographics Processor

Handles ward-wise household demographic data processing, chart generation, and report formatting.
This covers section ३.१.२ घरपरिवारको विवरण (Household Details).
"""

from pathlib import Path
from django.db import models
from .base import BaseDemographicsProcessor, BaseReportFormatter
from ..models import WardTimeSeriesPopulation
from ..utils.svg_chart_generator import DEFAULT_COLORS
from apps.reports.utils.nepali_numbers import (
    format_nepali_number,
    format_nepali_percentage,
)
from apps.chart_management.processors import SimpleChartProcessor


class WardHouseholdProcessor(BaseDemographicsProcessor, SimpleChartProcessor):
    """Processor for ward-wise household demographics"""

    def __init__(self):
        super().__init__()
        SimpleChartProcessor.__init__(self)

        # Ensure we use the same directory as the chart service
        from django.conf import settings

        if hasattr(settings, "STATICFILES_DIRS") and settings.STATICFILES_DIRS:
            self.static_charts_dir = Path(settings.STATICFILES_DIRS[0]) / "charts"
        else:
            self.static_charts_dir = Path(settings.STATIC_ROOT or "static") / "charts"

        self.static_charts_dir.mkdir(parents=True, exist_ok=True)

        # Customize chart dimensions for ward household data
        self.pie_chart_width = 900
        self.pie_chart_height = 500
        self.bar_chart_width = 1000
        self.bar_chart_height = 600
        self.chart_radius = 140

        # Set ward-specific colors
        self.chart_generator.colors = {
            "ward_1": "#1f77b4",  # Blue
            "ward_2": "#ff7f0e",  # Orange
            "ward_3": "#2ca02c",  # Green
            "ward_4": "#d62728",  # Red
            "ward_5": "#9467bd",  # Purple
            "ward_6": "#8c564b",  # Brown
            "ward_7": "#e377c2",  # Pink
            "population": "#1f77b4",
            "households": "#ff7f0e",
            "density": "#2ca02c",
        }

    def get_section_title(self):
        return "घरपरिवारको विवरण"

    def get_section_number(self):
        return "३.१.२"

    def get_chart_key(self):
        """Return unique chart key for this processor"""
        return "demographics_ward_household"

    def get_data(self):
        """Get ward-wise household population data with time series analysis"""

        # Get all ward time series data, ordered by year and ward
        all_data = WardTimeSeriesPopulation.objects.all().order_by(
            "year", "ward_number"
        )

        if not all_data.exists():
            return {
                "ward_data": {},
                "time_series_data": {},
                "summary_stats": {},
                "latest_year": None,
                "comparison_years": [],
            }

        # Organize data by year and ward
        time_series_data = {}
        ward_data = {}
        years = set()

        for record in all_data:
            year = record.year
            ward_num = record.ward_number
            years.add(year)

            if year not in time_series_data:
                time_series_data[year] = {}

            # Calculate sex ratio (males per 100 females)
            sex_ratio = 0
            if record.female_population and record.female_population > 0:
                sex_ratio = (
                    (record.male_population or 0) / record.female_population * 100
                )

            # Calculate population density (rounded to nearest integer)
            density = 0
            if record.area_sq_km and record.area_sq_km > 0:
                density = round(
                    (record.total_population or 0) / float(record.area_sq_km)
                )

            ward_info = {
                "ward_number": ward_num,
                "ward_name": record.ward_name or f"वडा नं. {ward_num}",
                "year": year,
                "total_population": record.total_population or 0,
                "male_population": record.male_population or 0,
                "female_population": record.female_population or 0,
                "other_population": record.other_population or 0,
                "total_households": record.total_households or 0,
                "average_household_size": float(record.average_household_size or 0),
                "area_sq_km": float(record.area_sq_km or 0),
                "population_density": density,
                "sex_ratio": sex_ratio,
                "growth_rate": float(record.growth_rate or 0),
                "literacy_rate": float(record.literacy_rate or 0),
                "male_literacy_rate": float(record.male_literacy_rate or 0),
                "female_literacy_rate": float(record.female_literacy_rate or 0),
                "population_0_to_14": record.population_0_to_14 or 0,
                "population_15_to_59": record.population_15_to_59 or 0,
                "population_60_and_above": record.population_60_and_above or 0,
            }

            time_series_data[year][ward_num] = ward_info

            # Keep latest data in ward_data for easy access
            if ward_num not in ward_data or year > ward_data[ward_num]["year"]:
                ward_data[ward_num] = ward_info

        # Get latest year
        latest_year = max(years) if years else None
        comparison_years = sorted(years, reverse=True)

        # Calculate summary statistics
        summary_stats = self._calculate_summary_stats(
            ward_data, time_series_data, latest_year
        )

        return {
            "ward_data": ward_data,
            "time_series_data": time_series_data,
            "summary_stats": summary_stats,
            "latest_year": latest_year,
            "comparison_years": comparison_years,
        }

    def _calculate_summary_stats(self, ward_data, time_series_data, latest_year):
        """Calculate summary statistics for analysis"""
        if not ward_data or not latest_year:
            return {}

        # Get latest year data for calculations
        latest_data = time_series_data.get(latest_year, {})

        # Population statistics
        total_population = sum(
            w.get("total_population", 0) for w in latest_data.values()
        )
        total_households = sum(
            w.get("total_households", 0) for w in latest_data.values()
        )

        # Find ward with highest/lowest population
        max_pop_ward = max(
            latest_data.values(), key=lambda x: x.get("total_population", 0), default={}
        )
        min_pop_ward = min(
            latest_data.values(), key=lambda x: x.get("total_population", 0), default={}
        )

        # Find ward with highest/lowest density
        max_density_ward = max(
            latest_data.values(),
            key=lambda x: x.get("population_density", 0),
            default={},
        )
        min_density_ward = min(
            latest_data.values(),
            key=lambda x: x.get("population_density", 0),
            default={},
        )

        # Calculate average household size
        total_avg_household_size = 0
        ward_count = 0
        for ward in latest_data.values():
            if ward.get("average_household_size", 0) > 0:
                total_avg_household_size += ward.get("average_household_size", 0)
                ward_count += 1

        overall_avg_household_size = (
            total_avg_household_size / ward_count if ward_count > 0 else 0
        )

        # Gender distribution
        total_male = sum(w.get("male_population", 0) for w in latest_data.values())
        total_female = sum(w.get("female_population", 0) for w in latest_data.values())
        overall_sex_ratio = (total_male / total_female * 100) if total_female > 0 else 0

        return {
            "total_population": total_population,
            "total_households": total_households,
            "overall_avg_household_size": overall_avg_household_size,
            "total_male": total_male,
            "total_female": total_female,
            "overall_sex_ratio": overall_sex_ratio,
            "max_pop_ward": max_pop_ward,
            "min_pop_ward": min_pop_ward,
            "max_density_ward": max_density_ward,
            "min_density_ward": min_density_ward,
            "ward_count": len(latest_data),
        }

    def generate_report_content(self, data):
        """Generate ward household-specific report content with comprehensive analysis"""
        formatter = self.WardHouseholdReportFormatter()
        return formatter.generate_formal_report(data)

    def generate_chart_svg(self, data, chart_type="bar"):
        """Generate ward household chart SVG using SVGChartGenerator"""
        if chart_type == "bar" and data.get("ward_data"):
            # Population comparison chart - format data for SVGChartGenerator
            ward_data = data["ward_data"]
            formatted_ward_data = {}

            for ward_num in sorted(ward_data.keys()):
                ward_info = ward_data[ward_num]
                formatted_ward_data[ward_num] = {
                    "ward_name": ward_info.get("ward_name", f"वडा नं. {ward_num}"),
                    "total_population": ward_info.get("total_population", 0),
                    "demographics": {
                        "population": {
                            "population": ward_info.get("total_population", 0),
                            "name_nepali": "जनसंख्या",
                        }
                    },
                }

            return self.chart_generator.generate_bar_chart_svg(
                ward_data=formatted_ward_data,
                include_title=False,
                title_nepali="वडागत जनसंख्या तुलना",
                title_english="Ward-wise Population Comparison",
            )

        elif chart_type == "density_bar" and data.get("ward_data"):
            # Population density comparison chart - format data for SVGChartGenerator
            ward_data = data["ward_data"]
            formatted_ward_data = {}

            for ward_num in sorted(ward_data.keys()):
                ward_info = ward_data[ward_num]
                formatted_ward_data[ward_num] = {
                    "ward_name": ward_info.get("ward_name", f"वडा नं. {ward_num}"),
                    "total_population": round(ward_info.get("population_density", 0)),
                    "demographics": {
                        "density": {
                            "population": round(ward_info.get("population_density", 0)),
                            "name_nepali": "जनघनत्व",
                        }
                    },
                }

            return self.chart_generator.generate_bar_chart_svg(
                ward_data=formatted_ward_data,
                include_title=False,
                title_nepali="वडागत जनसंख्या घनत्व तुलना",
                title_english="Ward-wise Population Density Comparison",
            )

        return None

    def generate_and_save_charts(self, data):
        """Generate and save charts for ward household demographics"""
        charts = {}

        # Ensure static charts directory exists
        self.static_charts_dir.mkdir(parents=True, exist_ok=True)

        # Generate population comparison bar chart
        ward_data = data["ward_data"]
        formatted_population_data = {}

        for ward_num in sorted(ward_data.keys()):
            ward_info = ward_data[ward_num]
            formatted_population_data[ward_num] = {
                "ward_name": ward_info.get("ward_name", f"वडा नं. {ward_num}"),
                "total_population": ward_info.get("total_population", 0),
                "demographics": {
                    "population": {
                        "population": ward_info.get("total_population", 0),
                        "name_nepali": "जनसंख्या",
                    }
                },
            }

        # Generate population bar chart
        success, png_path, svg_path = self.chart_generator.generate_chart_image(
            demographic_data=formatted_population_data,
            output_name="ward_household_population_bar",
            static_dir=str(self.static_charts_dir),
            chart_type="bar",
            include_title=False,
            title_nepali="वडागत जनसंख्या तुलना",
            title_english="Ward-wise Population Comparison",
        )

        if success and png_path:
            charts["population_bar_chart_png"] = (
                f"/static/charts/ward_household_population_bar.png"
            )
            charts["population_bar_chart_svg"] = (
                f"/static/charts/ward_household_population_bar.svg"
            )
            charts["population_bar_chart_url"] = (
                f"/static/charts/ward_household_population_bar.png"
            )
        elif svg_path:
            charts["population_bar_chart_svg"] = (
                f"/static/charts/ward_household_population_bar.svg"
            )
            charts["population_bar_chart_url"] = (
                f"/static/charts/ward_household_population_bar.svg"
            )

        # Generate density comparison bar chart
        formatted_density_data = {}

        for ward_num in sorted(ward_data.keys()):
            ward_info = ward_data[ward_num]
            formatted_density_data[ward_num] = {
                "ward_name": ward_info.get("ward_name", f"वडा नं. {ward_num}"),
                "total_population": round(ward_info.get("population_density", 0)),
                "demographics": {
                    "density": {
                        "population": round(ward_info.get("population_density", 0)),
                        "name_nepali": "जनघनत्व",
                    }
                },
            }

        # Generate density bar chart
        success, png_path, svg_path = self.chart_generator.generate_chart_image(
            demographic_data=formatted_density_data,
            output_name="ward_household_density_bar",
            static_dir=str(self.static_charts_dir),
            chart_type="bar",
            include_title=False,
            title_nepali="वडागत जनसंख्या घनत्व तुलना",
            title_english="Ward-wise Population Density Comparison",
        )

        if success and png_path:
            charts["density_bar_chart_png"] = (
                f"/static/charts/ward_household_density_bar.png"
            )
            charts["density_bar_chart_svg"] = (
                f"/static/charts/ward_household_density_bar.svg"
            )
            charts["density_bar_chart_url"] = (
                f"/static/charts/ward_household_density_bar.png"
            )
        elif svg_path:
            charts["density_bar_chart_svg"] = (
                f"/static/charts/ward_household_density_bar.svg"
            )
            charts["density_bar_chart_url"] = (
                f"/static/charts/ward_household_density_bar.svg"
            )

        return charts

    def process_for_pdf(self):
        """Process ward household data for PDF generation"""
        # Get raw data
        data = self.get_data()

        # Generate report content
        report_content = self.generate_report_content(data)

        # Generate charts
        charts = self.generate_and_save_charts(data)

        # Calculate summary statistics
        summary_stats = data.get("summary_stats", {})

        return {
            "data": data,
            "report_content": report_content,
            "charts": charts,
            "summary_stats": summary_stats,
            "section_title": self.get_section_title(),
            "section_number": self.get_section_number(),
        }

    class WardHouseholdReportFormatter(BaseReportFormatter):
        """Formatter for ward household reports"""

        def generate_formal_report(self, data):
            """Generate comprehensive formal ward household report with detailed analysis"""
            if not data or not data.get("ward_data"):
                return "गढवा गाउँपालिकाको वडागत घरपरिवारको तथ्याङ्क उपलब्ध छैन।"

            ward_data = data["ward_data"]
            summary_stats = data.get("summary_stats", {})
            latest_year = data.get("latest_year")

            if not summary_stats:
                return "गढवा गाउँपालिकाको वडागत घरपरिवारको विश्लेषणका लागि पर्याप्त तथ्याङ्क उपलब्ध छैन।"

            analysis_parts = []

            # Overall introduction
            analysis_parts.append(
                f"गढवा गाउँपालिकाका {format_nepali_number(len(ward_data))} वडामा वर्ष {format_nepali_number(latest_year)} को तथ्याङ्क अनुसार कुल "
                f"{format_nepali_number(summary_stats.get('total_population', 0))} जनसंख्या, "
                f"{format_nepali_number(summary_stats.get('total_households', 0))} घरपरिवार, "
                f"औसत घरपरिवार आकार {format_nepali_number(round(summary_stats.get('overall_avg_household_size', 2), 2))} व्यक्ति रहेको छ।"
            )

            # Literacy analysis (if available)
            if any(w.get("literacy_rate") for w in ward_data.values()):
                avg_lit = sum(
                    [
                        w.get("literacy_rate", 0) or 0
                        for w in ward_data.values()
                        if w.get("literacy_rate") is not None
                    ]
                ) / max(
                    1,
                    len(
                        [
                            w
                            for w in ward_data.values()
                            if w.get("literacy_rate") is not None
                        ]
                    ),
                )
                analysis_parts.append(
                    f"औसत साक्षरता दर {format_nepali_number(round(avg_lit, 2))}% रहेको छ।"
                )

            # Age group analysis (if available)
            if any(w.get("population_0_to_14") for w in ward_data.values()):
                total_0_14 = sum(
                    [w.get("population_0_to_14", 0) or 0 for w in ward_data.values()]
                )
                total_15_59 = sum(
                    [w.get("population_15_to_59", 0) or 0 for w in ward_data.values()]
                )
                total_60p = sum(
                    [
                        w.get("population_60_and_above", 0) or 0
                        for w in ward_data.values()
                    ]
                )
                analysis_parts.append(
                    f"बालबालिका (०-१४ वर्ष): {format_nepali_number(total_0_14)}, युवा तथा प्रौढ (१५-५९ वर्ष): {format_nepali_number(total_15_59)}, जेष्ठ नागरिक (६० वर्ष+) : {format_nepali_number(total_60p)} जना रहेका छन्।"
                )

            # Population distribution analysis
            max_pop_ward = summary_stats.get("max_pop_ward", {})
            min_pop_ward = summary_stats.get("min_pop_ward", {})
            if max_pop_ward and min_pop_ward:
                analysis_parts.append(
                    f"सबैभन्दा बढी जनसंख्या वडा नं. {format_nepali_number(max_pop_ward.get('ward_number'))} ({max_pop_ward.get('ward_name','')}) मा {format_nepali_number(max_pop_ward.get('total_population', 0))} जना रहेको छ। "
                    f"सबैभन्दा कम जनसंख्या वडा नं. {format_nepali_number(min_pop_ward.get('ward_number'))} ({min_pop_ward.get('ward_name','')}) मा {format_nepali_number(min_pop_ward.get('total_population', 0))} जना रहेको छ।"
                )

            # Gender composition analysis
            total_male = summary_stats.get("total_male", 0)
            total_female = summary_stats.get("total_female", 0)
            sex_ratio = summary_stats.get("overall_sex_ratio", 0)
            if total_male > 0 and total_female > 0:
                analysis_parts.append(
                    f"लिङ्ग अनुपात {format_nepali_number(round(sex_ratio, 2))} (प्रति १०० महिलामा {format_nepali_number(round(sex_ratio, 1))} पुरुष) रहेको छ।"
                )

            # Household size analysis
            household_sizes = [
                w.get("average_household_size", 0)
                for w in ward_data.values()
                if w.get("average_household_size", 0) > 0
            ]
            if household_sizes:
                max_household_size = max(household_sizes)
                min_household_size = min(household_sizes)
                analysis_parts.append(
                    f"सबैभन्दा ठूलो घरपरिवारको औसत आकार {format_nepali_number(round(max_household_size, 2))} व्यक्ति र सबैभन्दा सानो घरपरिवारको औसत आकार {format_nepali_number(round(min_household_size, 2))} व्यक्ति रहेको छ।"
                )

            # Growth and development trends (if time series data available)
            time_series_data = data.get("time_series_data", {})
            comparison_years = data.get("comparison_years", [])
            if len(comparison_years) >= 2:
                latest_year = comparison_years[0]
                previous_year = comparison_years[1]
                latest_total = sum(
                    w.get("total_population", 0)
                    for w in time_series_data.get(latest_year, {}).values()
                )
                previous_total = sum(
                    w.get("total_population", 0)
                    for w in time_series_data.get(previous_year, {}).values()
                )
                if previous_total > 0:
                    growth_rate = (
                        (latest_total - previous_total) / previous_total
                    ) * 100
                    analysis_parts.append(
                        f"वर्ष {format_nepali_number(previous_year)} देखि {format_nepali_number(latest_year)} सम्म जनसंख्या वृद्धि दर {format_nepali_number(round(growth_rate, 2))}% रहेको छ।"
                    )

            analysis_parts.append(
                f"समग्रमा, गढवा गाउँपालिकाको वडागत घरपरिवार र जनसंख्या संरचनाले स्थानीय विकास, सेवा प्रवाह र योजना निर्माणमा महत्वपूर्ण आधार प्रदान गर्दछ। विस्तृत विवरण तलको तालिका र चित्रमा प्रस्तुत गरिएको छ।"
            )
            return " ".join(analysis_parts)
