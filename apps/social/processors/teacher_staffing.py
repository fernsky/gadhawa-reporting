"""
Teacher Staffing Processor for Social Domain

This processor handles Ward Wise Teacher Staffing data (५.१.५) providing:
- Municipality-wide and ward-wise teacher statistics
- Detailed analysis by level and position type
- Chart generation using base class functionality
- Teacher distribution and staffing pattern analysis
"""

from collections import defaultdict
from typing import Dict, Any

from django.db import models
from apps.social.models import (
    WardWiseTeacherStaffing,
    WardWiseTeacherSummary,
    TeacherLevelChoice,
    TeacherPositionTypeChoice,
)
from .base import BaseSocialProcessor


class TeacherStaffingProcessor(BaseSocialProcessor):
    """Processor for Ward Wise Teacher Staffing"""

    def __init__(self):
        super().__init__()
        # Customize chart dimensions for teacher staffing
        self.pie_chart_width = 800
        self.pie_chart_height = 600
        self.bar_chart_width = 1200
        self.bar_chart_height = 700
        self.chart_radius = 200

        # Set teacher-specific colors with meaningful associations
        self.chart_generator.colors = {
            "CHILD_DEVELOPMENT": "#FF9800",  # Orange for early childhood
            "BASIC_1_5": "#4CAF50",  # Green for primary
            "BASIC_6_8": "#2196F3",  # Blue for lower secondary
            "BASIC_9_10": "#9C27B0",  # Purple for secondary
            "BASIC_11_12": "#F44336",  # Red for higher secondary
            "APPROVED_QUOTA": "#4CAF50",  # Green for permanent positions
            "RELIEF": "#FF9800",  # Orange for relief positions
            "FEDERAL_GRANT": "#2196F3",  # Blue for federal funded
            "RM_GRANT": "#9C27B0",  # Purple for municipality funded
            "PRIVATE_SOURCE": "#795548",  # Brown for private funded
        }

    def get_section_title(self):
        """Return the section title for teacher staffing"""
        return "५.१.५ शिक्षक तथा शैक्षिक जनशक्ति सम्बन्धी विवरण"

    def get_section_number(self):
        """Return the section number for teacher staffing"""
        return "5.1.5"

    def get_data(self) -> Dict[str, Any]:
        """Get teacher staffing data aggregated by municipality and ward"""
        try:
            # Municipality-wide summary by teacher level
            municipality_data_by_level = {}
            total_teachers = 0

            for level_choice in TeacherLevelChoice.choices:
                level_code = level_choice[0]
                level_name = level_choice[1]

                level_total = (
                    WardWiseTeacherStaffing.objects.filter(
                        teacher_level=level_code
                    ).aggregate(total=models.Sum("teacher_count"))["total"]
                    or 0
                )

                if level_total > 0:
                    municipality_data_by_level[level_code] = {
                        "name_nepali": level_name,
                        "teacher_count": level_total,
                        "percentage": 0,  # Will be calculated later
                    }
                    total_teachers += level_total

            # Calculate percentages for levels
            for level_data in municipality_data_by_level.values():
                if total_teachers > 0:
                    level_data["percentage"] = (
                        level_data["teacher_count"] / total_teachers
                    ) * 100

            # Municipality-wide summary by position type
            municipality_data_by_position = {}

            for position_choice in TeacherPositionTypeChoice.choices:
                position_code = position_choice[0]
                position_name = position_choice[1]

                position_total = (
                    WardWiseTeacherStaffing.objects.filter(
                        position_type=position_code
                    ).aggregate(total=models.Sum("teacher_count"))["total"]
                    or 0
                )

                if position_total > 0:
                    municipality_data_by_position[position_code] = {
                        "name_nepali": position_name,
                        "teacher_count": position_total,
                        "percentage": (
                            (position_total / total_teachers) * 100
                            if total_teachers > 0
                            else 0
                        ),
                    }

            # Ward-wise data
            ward_data = {}
            for ward_num in range(1, 8):
                ward_teachers = WardWiseTeacherStaffing.objects.filter(
                    ward_number=ward_num
                )

                if ward_teachers.exists():
                    ward_total = (
                        ward_teachers.aggregate(total=models.Sum("teacher_count"))[
                            "total"
                        ]
                        or 0
                    )

                    # Group by school
                    schools = defaultdict(
                        lambda: {
                            "institution_level": "",
                            "levels": defaultdict(lambda: defaultdict(int)),
                            "total_teachers": 0,
                        }
                    )

                    for teacher_record in ward_teachers:
                        school_name = teacher_record.school_name
                        schools[school_name][
                            "institution_level"
                        ] = teacher_record.get_institution_level_display()
                        schools[school_name]["levels"][teacher_record.teacher_level][
                            teacher_record.position_type
                        ] += teacher_record.teacher_count
                        schools[school_name][
                            "total_teachers"
                        ] += teacher_record.teacher_count

                    ward_data[ward_num] = {
                        "total_teachers": ward_total,
                        "schools": dict(schools),
                    }

            # Detailed breakdown by level and position
            detailed_breakdown = {}
            for level_choice in TeacherLevelChoice.choices:
                level_code = level_choice[0]
                level_name = level_choice[1]

                level_positions = {}
                for position_choice in TeacherPositionTypeChoice.choices:
                    position_code = position_choice[0]
                    position_name = position_choice[1]

                    count = (
                        WardWiseTeacherStaffing.objects.filter(
                            teacher_level=level_code, position_type=position_code
                        ).aggregate(total=models.Sum("teacher_count"))["total"]
                        or 0
                    )

                    if count > 0:
                        level_positions[position_code] = {
                            "name_nepali": position_name,
                            "count": count,
                        }

                if level_positions:
                    detailed_breakdown[level_code] = {
                        "name_nepali": level_name,
                        "positions": level_positions,
                        "total": sum(pos["count"] for pos in level_positions.values()),
                    }

            return {
                "municipality_data_by_level": municipality_data_by_level,
                "municipality_data_by_position": municipality_data_by_position,
                "ward_data": ward_data,
                "detailed_breakdown": detailed_breakdown,
                "total_teachers": total_teachers,
            }

        except Exception as e:
            print(f"Error in TeacherStaffingProcessor.get_data: {e}")
            return self._empty_data_structure()

    def _empty_data_structure(self) -> Dict[str, Any]:
        """Return empty data structure when no data available"""
        return {
            "municipality_data_by_level": {},
            "municipality_data_by_position": {},
            "ward_data": {},
            "detailed_breakdown": {},
            "total_teachers": 0,
        }

    def generate_analysis_text(self, data: Dict[str, Any]) -> str:
        """Generate comprehensive analysis text for teacher staffing"""
        if not data or data["total_teachers"] == 0:
            return "<p>शिक्षक तथा शैक्षिक जनशक्ति सम्बन्धी तथ्याङ्क उपलब्ध छैन।</p>"

        total_teachers = data["total_teachers"]
        level_data = data["municipality_data_by_level"]
        position_data = data["municipality_data_by_position"]
        detailed_breakdown = data["detailed_breakdown"]

        # Import necessary formatting functions
        from apps.reports.utils.nepali_numbers import (
            format_nepali_number,
            format_nepali_percentage,
        )

        # Build comprehensive analysis
        content = []

        # Introduction based on provided text
        content.append(
            f"<p>आर्थिक वर्ष २०८०÷०८१ को अन्त्य सम्ममा गाउँपालिकामा रहेका शिक्षक तथा शैक्षिक जनशक्तिको "
            f"अध्ययन गर्दा कुल {format_nepali_number(total_teachers)} जना शिक्षक÷शिक्षिका रहेका छन्।</p>"
        )

        # Level-wise breakdown
        if TeacherLevelChoice.CHILD_DEVELOPMENT in level_data:
            child_dev_count = level_data[TeacherLevelChoice.CHILD_DEVELOPMENT][
                "teacher_count"
            ]
            content.append(
                f"<p>बाल विकासमा पठनपाठन गराउने {format_nepali_number(child_dev_count)} जना, "
            )

        if TeacherLevelChoice.BASIC_1_5 in level_data:
            basic_1_5_count = level_data[TeacherLevelChoice.BASIC_1_5]["teacher_count"]
            content.append(
                f"आधारभुत विद्यालय (१–५) मा पठनपाठन गराउने {format_nepali_number(basic_1_5_count)} जना रहेका छन्।"
            )

        if TeacherLevelChoice.BASIC_6_8 in level_data:
            basic_6_8_count = level_data[TeacherLevelChoice.BASIC_6_8]["teacher_count"]
            content.append(
                f" यसैगरी आधारभुत विद्यालय ६–८ मा पठनपाठन गराउने शिक्षक÷शिक्षिका "
                f"{format_nepali_number(basic_6_8_count)} जना रहेका छन्"
            )

        if TeacherLevelChoice.BASIC_9_10 in level_data:
            basic_9_10_count = level_data[TeacherLevelChoice.BASIC_9_10][
                "teacher_count"
            ]
            content.append(
                f" भने मा. वि. (९–१०) मा {format_nepali_number(basic_9_10_count)} जना रहेका छन्"
            )

        if TeacherLevelChoice.BASIC_11_12 in level_data:
            basic_11_12_count = level_data[TeacherLevelChoice.BASIC_11_12][
                "teacher_count"
            ]
            content.append(
                f" भने मा.वि.(११–१२) मा पठनपाठन गराउने {format_nepali_number(basic_11_12_count)} जना रहेका छन्।"
            )

        content.append("</p>")

        # Position type analysis
        content.append("<p>")
        if TeacherPositionTypeChoice.APPROVED_QUOTA in position_data:
            quota_count = position_data[TeacherPositionTypeChoice.APPROVED_QUOTA][
                "teacher_count"
            ]
            quota_percent = position_data[TeacherPositionTypeChoice.APPROVED_QUOTA][
                "percentage"
            ]
            content.append(
                f"स्वीकृत दरबन्दीमा {format_nepali_number(quota_count)} जना "
                f"({format_nepali_percentage(quota_percent)}%), "
            )

        if TeacherPositionTypeChoice.RM_GRANT in position_data:
            rm_grant_count = position_data[TeacherPositionTypeChoice.RM_GRANT][
                "teacher_count"
            ]
            rm_grant_percent = position_data[TeacherPositionTypeChoice.RM_GRANT][
                "percentage"
            ]
            content.append(
                f"गाउँपालिका अनुदानमा {format_nepali_number(rm_grant_count)} जना "
                f"({format_nepali_percentage(rm_grant_percent)}%), "
            )

        if TeacherPositionTypeChoice.FEDERAL_GRANT in position_data:
            federal_count = position_data[TeacherPositionTypeChoice.FEDERAL_GRANT][
                "teacher_count"
            ]
            federal_percent = position_data[TeacherPositionTypeChoice.FEDERAL_GRANT][
                "percentage"
            ]
            content.append(
                f"संघीय अनुदानमा {format_nepali_number(federal_count)} जना "
                f"({format_nepali_percentage(federal_percent)}%) रहेका छन्।"
            )

        content.append("</p>")

        # Summary conclusion
        content.append(
            "<p>जसको विस्तृत विवरण तलको तालिकामा प्रस्तुत गरिएको छ। शैक्षिक गुणस्तर सुधारका लागि "
            "उपयुक्त संख्यामा दक्ष शिक्षक÷शिक्षिका आवश्यक छ।</p>"
        )

        return "".join(content)

    def _format_municipality_data_for_pie_chart(self, municipality_data_by_level):
        """Format municipality data for pie chart generation"""
        if not municipality_data_by_level:
            return {}

        formatted_data = {}
        for level_code, level_data in municipality_data_by_level.items():
            if isinstance(level_data, dict) and level_data.get("teacher_count", 0) > 0:
                formatted_data[level_code] = {
                    "name_nepali": level_data.get("name_nepali", level_code),
                    "population": level_data.get("teacher_count", 0),
                    "percentage": level_data.get("percentage", 0),
                }
        return formatted_data

    def _format_ward_data_for_bar_chart(self, ward_data):
        """Format ward data for bar chart generation"""
        if not ward_data:
            return {}

        formatted_data = {}
        for ward_num, ward_info in ward_data.items():
            if isinstance(ward_info, dict) and ward_info.get("total_teachers", 0) > 0:
                formatted_data[str(ward_num)] = {
                    "ward_name": f"वडा नं. {ward_num}",
                    "total_population": ward_info.get("total_teachers", 0),
                    "demographics": {
                        "total_teachers": {
                            "name_nepali": "कुल शिक्षक",
                            "population": ward_info.get("total_teachers", 0),
                            "percentage": 100,
                        }
                    },
                }
        return formatted_data

    def process_for_pdf(self):
        """Process teacher staffing data for PDF generation with charts"""
        data = self.get_data()

        # Generate analysis text
        analysis_text = self.generate_analysis_text(data)

        # Generate and save charts
        charts = self.generate_and_save_charts(data)

        return {
            "section_title": self.get_section_title(),
            "section_number": self.get_section_number(),
            "municipality_data_by_level": data["municipality_data_by_level"],
            "municipality_data_by_position": data["municipality_data_by_position"],
            "ward_data": data["ward_data"],
            "detailed_breakdown": data["detailed_breakdown"],
            "total_teachers": data["total_teachers"],
            "coherent_analysis": analysis_text,
            "pdf_charts": {"teacher_staffing": charts},
        }


class TeacherStaffingReportFormatter:
    """Report formatter for teacher staffing data"""

    def __init__(self, processor_data):
        self.processor_data = processor_data

    def format_for_html(self):
        """Format teacher staffing data for HTML display"""
        return {
            "section_title": self.processor_data["section_title"],
            "municipality_data_by_level": self.processor_data[
                "municipality_data_by_level"
            ],
            "municipality_data_by_position": self.processor_data[
                "municipality_data_by_position"
            ],
            "ward_data": self.processor_data["ward_data"],
            "detailed_breakdown": self.processor_data["detailed_breakdown"],
            "total_teachers": self.processor_data["total_teachers"],
            "coherent_analysis": self.processor_data["coherent_analysis"],
            "pdf_charts": self.processor_data["pdf_charts"],
        }

    def format_for_api(self):
        """Format teacher staffing data for API response"""
        return {
            "section": self.processor_data["section_number"],
            "title": self.processor_data["section_title"],
            "summary": {
                "total_teachers": self.processor_data["total_teachers"],
                "levels": len(self.processor_data["municipality_data_by_level"]),
                "wards": len(self.processor_data["ward_data"]),
            },
            "teacher_breakdown_by_level": self.processor_data[
                "municipality_data_by_level"
            ],
            "teacher_breakdown_by_position": self.processor_data[
                "municipality_data_by_position"
            ],
            "ward_breakdown": self.processor_data["ward_data"],
            "detailed_breakdown": self.processor_data["detailed_breakdown"],
            "analysis": self.processor_data["coherent_analysis"],
        }
