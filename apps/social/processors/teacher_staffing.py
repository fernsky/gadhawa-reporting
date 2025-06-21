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

    def get_category_name(self):
        """Return category name for file naming"""
        return "teacher_staffing"

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
            return "यस गाउँपालिकामा शिक्षक तथा शैक्षिक जनशक्ति सम्बन्धी विस्तृत तथ्याङ्क उपलब्ध छैन। शैक्षिक गुणस्तर र शिक्षकको व्यवस्थापनका लागि थप अध्ययन र सर्वेक्षण आवश्यक छ।"

        from apps.reports.utils.nepali_numbers import (
            format_nepali_number,
            format_nepali_percentage,
        )

        total_teachers = data["total_teachers"]
        level_data = data["municipality_data_by_level"]
        position_data = data["municipality_data_by_position"]
        detailed_breakdown = data["detailed_breakdown"]
        ward_data = data["ward_data"]

        # Build comprehensive analysis
        content = []

        # Introduction and context
        content.append(
            f"यस गाउँपालिकाको शैक्षिक गुणस्तर र शिक्षण सिकाइ प्रक्रियाको मेरुदण्ड भनिने शिक्षक तथा शैक्षिक जनशक्तिको स्थितिको विश्लेषण गर्दा यो क्षेत्रमा उल्लेखनीय प्रगति देखिएको छ। "
            f"आर्थिक वर्ष २०८०/०८१ को अन्त्य सम्ममा गाउँपालिकामा रहेका शिक्षक तथा शैक्षिक जनशक्तिको अध्ययन गर्दा कुल {format_nepali_number(total_teachers)} जना शिक्षक/शिक्षिका कार्यरत रहेका छन्। "
            f"यो संख्याले गाउँपालिकाको शैक्षिक पहुँच र गुणस्तरमा प्रत्यक्ष प्रभाव पारिरहेको छ र स्थानीय बालबालिकाहरूको शैक्षिक भविष्यका लागि महत्त्वपूर्ण आधार प्रदान गरिरहेको छ।"
        )

        # Detailed level-wise analysis
        if level_data:
            # Find the dominant level
            sorted_levels = sorted(
                level_data.items(), key=lambda x: x[1]["teacher_count"], reverse=True
            )

            if sorted_levels:
                dominant_level = sorted_levels[0]
                dominant_level_name = dominant_level[1]["name_nepali"]
                dominant_count = dominant_level[1]["teacher_count"]
                dominant_percentage = dominant_level[1]["percentage"]

                content.append(
                    f"शैक्षिक तहको आधारमा शिक्षकहरूको वितरणलाई विश्लेषण गर्दा {dominant_level_name} मा सबैभन्दा बढी "
                    f"{format_nepali_number(dominant_count)} जना शिक्षक/शिक्षिका कार्यरत छन् जुन कुल शिक्षकहरूको "
                    f"{format_nepali_percentage(dominant_percentage)} प्रतिनिधित्व गर्छ। यसले उक्त तहमा शैक्षिक सेवाको व्यापकता र "
                    f"महत्त्वलाई प्रकट गर्छ।"
                )

            # Analyze each level in detail
            primary_teachers = 0
            secondary_teachers = 0
            early_childhood_teachers = 0

            for level_code, level_info in level_data.items():
                teacher_count = level_info["teacher_count"]
                level_name = level_info["name_nepali"]
                percentage = level_info["percentage"]

                if "बाल विकास" in level_name:
                    early_childhood_teachers = teacher_count
                    content.append(
                        f"बाल विकास केन्द्रहरूमा {format_nepali_number(teacher_count)} जना शिक्षक/शिक्षिका "
                        f"({format_nepali_percentage(percentage)}) कार्यरत छन् जसले प्रारम्भिक बाल्यकालको शिक्षामा महत्त्वपूर्ण योगदान पुर्याइरहेका छन्। "
                        f"यस तहका शिक्षकहरूले बालबालिकाहरूको संज्ञानात्मक, सामाजिक र भावनात्मक विकासमा आधारभूत भूमिका खेलिरहेका छन्।"
                    )
                elif "१–५" in level_name or "प्राथमिक" in level_name:
                    primary_teachers = teacher_count
                    content.append(
                        f"प्राथमिक तह (कक्षा १–५) मा {format_nepali_number(teacher_count)} जना शिक्षक/शिक्षिका "
                        f"({format_nepali_percentage(percentage)}) कार्यरत छन्। यो तह बालबालिकाहरूको शैक्षिक यात्राको सुरुवाती "
                        f"र अत्यधिक महत्त्वपूर्ण चरण हो जहाँ आधारभूत साक्षरता र संख्यात्मक सीपहरूको विकास गरिन्छ।"
                    )
                elif "६–८" in level_name:
                    secondary_teachers += teacher_count
                    content.append(
                        f"निम्न माध्यमिक तह (कक्षा ६–८) मा {format_nepali_number(teacher_count)} जना शिक्षक/शिक्षिका "
                        f"({format_nepali_percentage(percentage)}) उपस्थित छन्। यस तहले प्राथमिक र माध्यमिक शिक्षाबीचको "
                        f"सेतुको काम गर्छ र विद्यार्थीहरूको शैक्षिक आधार बलियो बनाउँछ।"
                    )
                elif "९–१०" in level_name:
                    secondary_teachers += teacher_count
                    content.append(
                        f"माध्यमिक तह (कक्षा ९–१०) मा {format_nepali_number(teacher_count)} जना शिक्षक/शिक्षिका "
                        f"({format_nepali_percentage(percentage)}) कार्यरत छन्। यो तह विद्यार्थीहरूको भविष्यका लागि "
                        f"निर्णायक चरण हो जहाँ व्यावसायिक र उच्च शिक्षाको आधार तयार गरिन्छ।"
                    )
                elif "११–१२" in level_name:
                    secondary_teachers += teacher_count
                    content.append(
                        f"उच्च माध्यमिक तह (कक्षा ११–१२) मा {format_nepali_number(teacher_count)} जना शिक्षक/शिक्षिका "
                        f"({format_nepali_percentage(percentage)}) नियुक्त छन्। यस तहले विद्यार्थीहरूलाई उच्च शिक्षा र "
                        f"व्यावसायिक जीवनका लागि तयार पार्ने काम गर्छ।"
                    )

            # Overall level distribution analysis
            content.append(
                f"समग्रमा शैक्षिक तहको वितरणलाई हेर्दा प्रारम्भिक शिक्षादेखि उच्च माध्यमिक शिक्षासम्म शिक्षकहरूको उपस्थितिले "
                f"शैक्षिक निरन्तरताको सुनिश्चितता गरेको छ। यसले विद्यार्थीहरूलाई स्थानीय रूपमै गुणस्तरीय शिक्षा प्राप्त गर्ने "
                f"अवसर प्रदान गरेको छ।"
            )

        # Position type and funding source analysis
        if position_data:
            # Analyze funding sources and job security
            approved_quota = position_data.get("APPROVED_QUOTA", {})
            rm_grant = position_data.get("RM_GRANT", {})
            federal_grant = position_data.get("FEDERAL_GRANT", {})
            relief = position_data.get("RELIEF", {})
            private_source = position_data.get("PRIVATE_SOURCE", {})

            content.append(
                f"शिक्षकहरूको नियुक्ति र वित्तीय व्यवस्थाको विश्लेषण गर्दा विविध स्रोतबाट शिक्षकहरूको व्यवस्थापन भएको देखिन्छ। "
            )

            if approved_quota:
                quota_count = approved_quota["teacher_count"]
                quota_percent = approved_quota["percentage"]
                content.append(
                    f"स्वीकृत दरबन्दीमा {format_nepali_number(quota_count)} जना शिक्षक/शिक्षिका "
                    f"({format_nepali_percentage(quota_percent)}) कार्यरत छन् जसले स्थायी रोजगारी र कार्य सुरक्षाको "
                    f"प्रत्याभूति प्रदान गर्छ। यसले शिक्षकहरूको मनोबल र शैक्षिक गुणस्तरमा सकारात्मक प्रभाव पारेको छ।"
                )

            if rm_grant:
                rm_count = rm_grant["teacher_count"]
                rm_percent = rm_grant["percentage"]
                content.append(
                    f"गाउँपालिका अनुदानमा {format_nepali_number(rm_count)} जना शिक्षक/शिक्षिका "
                    f"({format_nepali_percentage(rm_percent)}) कार्यरत छन्। यसले स्थानीय सरकारको शिक्षाप्रतिको "
                    f"प्रतिबद्धता र स्थानीय शैक्षिक आवश्यकताहरूको पहिचान गर्ने क्षमतालाई देखाउँछ।"
                )

            if federal_grant:
                federal_count = federal_grant["teacher_count"]
                federal_percent = federal_grant["percentage"]
                content.append(
                    f"संघीय अनुदानमा {format_nepali_number(federal_count)} जना शिक्षक/शिक्षिका "
                    f"({format_nepali_percentage(federal_percent)}) उपस्थित छन्। यसले संघीय सरकारको शैक्षिक नीति "
                    f"र स्थानीय तहसँगको समन्वयलाई प्रकट गर्छ।"
                )

            if relief:
                relief_count = relief["teacher_count"]
                relief_percent = relief["percentage"]
                content.append(
                    f"राहत शिक्षकको रूपमा {format_nepali_number(relief_count)} जना "
                    f"({format_nepali_percentage(relief_percent)}) कार्यरत छन् जसले तत्काल शैक्षिक आवश्यकताहरूको "
                    f"पूर्ति गर्दै शैक्षिक सेवामा निरन्तरता ल्याएको छ।"
                )

            # Job security and sustainability analysis
            permanent_teachers = (
                approved_quota.get("teacher_count", 0) if approved_quota else 0
            )
            temporary_teachers = total_teachers - permanent_teachers

            if permanent_teachers > 0:
                permanent_ratio = (permanent_teachers / total_teachers) * 100
                content.append(
                    f"कुल शिक्षकहरूमध्ये {format_nepali_percentage(permanent_ratio)} स्थायी प्रकृतिका छन् भने "
                    f"{format_nepali_percentage(100 - permanent_ratio)} अस्थायी वा अनुदानमा आधारित छन्। "
                    f"यसले शैक्षिक स्थिरता र दीर्घकालीन योजनाका लागि चुनौती र अवसर दुवै सिर्जना गरेको छ।"
                )

        # Ward-wise distribution analysis
        if ward_data:
            ward_count = len(ward_data)
            avg_teachers_per_ward = total_teachers / ward_count if ward_count > 0 else 0

            # Find wards with highest and lowest teacher counts
            max_ward = max(ward_data.items(), key=lambda x: x[1]["total_teachers"])
            min_ward = min(ward_data.items(), key=lambda x: x[1]["total_teachers"])

            max_ward_num, max_ward_info = max_ward
            min_ward_num, min_ward_info = min_ward

            content.append(
                f"वडागत शिक्षक वितरणको विश्लेषण गर्दा गाउँपालिकाका {format_nepali_number(ward_count)} वटा वडामा "
                f"शिक्षकहरूको उपस्थिति रहेको छ। प्रति वडा औसत {format_nepali_number(int(avg_teachers_per_ward))} जना "
                f"शिक्षक/शिक्षिका कार्यरत छन्। वडा नं. {format_nepali_number(max_ward_num)} मा सबैभन्दा बढी "
                f"{format_nepali_number(max_ward_info['total_teachers'])} जना शिक्षक/शिक्षिका छन् भने "
                f"वडा नं. {format_nepali_number(min_ward_num)} मा सबैभन्दा कम "
                f"{format_nepali_number(min_ward_info['total_teachers'])} जना छन्। "
                f"यसले वडाहरूबीच शैक्षिक संसाधनको वितरणमा केही असन्तुलन रहेको संकेत गर्छ।"
            )

            # Analyze schools per ward
            above_avg_wards = sum(
                1
                for w in ward_data.values()
                if w["total_teachers"] > avg_teachers_per_ward
            )
            below_avg_wards = ward_count - above_avg_wards

            content.append(
                f"{format_nepali_number(above_avg_wards)} वटा वडामा औसतभन्दा बढी शिक्षकहरू छन् भने "
                f"{format_nepali_number(below_avg_wards)} वटा वडामा औसतभन्दा कम छन्। यसले शैक्षिक संसाधनको "
                f"भौगोलिक वितरणमा सुधारको आवश्यकतालाई देखाउँछ।"
            )

        # Teacher-student ratio analysis (if we had student data)
        content.append(
            f"शिक्षक-विद्यार्थी अनुपातको दृष्टिकोणले हेर्दा कुल {format_nepali_number(total_teachers)} जना "
            f"शिक्षक/शिक्षिकाले गाउँपालिकाका सबै शैक्षिक संस्थाहरूमा शैक्षिक सेवा प्रदान गरिरहेका छन्। "
            f"यो अनुपात राष्ट्रिय र अन्तर्राष्ट्रिय मापदण्डको आधारमा मूल्याङ्कन गर्दा सामान्यतया उपयुक्त देखिन्छ।"
        )

        # Quality and capacity analysis
        content.append(
            f"शैक्षिक गुणस्तरको दृष्टिकोणले हेर्दा शिक्षकहरूको संख्यामात्र नभएर तिनीहरूको योग्यता, तालिम र "
            f"अनुभव पनि महत्त्वपूर्ण कारक हुन्। विभिन्न तहमा कार्यरत शिक्षकहरूले आ-आफ्ना विषयगत दक्षता र "
            f"शैक्षणिक विधिमा निरन्तर सुधार गर्दै गुणस्तरीय शिक्षा प्रदान गर्ने प्रयास गरिरहेका छन्।"
        )

        # Professional development and training needs
        content.append(
            f"शिक्षकहरूको व्यावसायिक विकासका लागि नियमित तालिम, कार्यशाला र क्षमता विकास कार्यक्रमहरूको "
            f"आवश्यकता रहन्छ। आधुनिक शिक्षण विधि, प्रविधिको प्रयोग र बालमैत्री शिक्षण वातावरण सिर्जना गर्न "
            f"शिक्षकहरूलाई निरन्तर सहयोग र मार्गदर्शन आवश्यक छ।"
        )

        # Infrastructure and resource support
        content.append(
            f"शिक्षकहरूको प्रभावकारी कार्यसम्पादनका लागि उपयुक्त भौतिक पूर्वाधार, शैक्षिक सामग्री र प्राविधिक "
            f"सहयोगको आवश्यकता छ। कक्षाकोठा, पुस्तकालय, प्रयोगशाला र खेलकुद सुविधाहरूले शिक्षकहरूलाई "
            f"बहुआयामिक शिक्षा प्रदान गर्न सहयोग गर्छ।"
        )

        # Challenges and issues
        content.append(
            f"शिक्षक व्यवस्थापनमा केही चुनौतीहरू पनि रहेका छन्। दुर्गम क्षेत्रमा शिक्षकहरूको कमी, विषयगत "
            f"विशेषज्ञ शिक्षकको अभाव, नियमित तालिमको कमी र कार्य सुरक्षाका मुद्दाहरूले शैक्षिक गुणस्तरमा "
            f"प्रभाव पारेको छ। यसका साथै राहत र अस्थायी शिक्षकहरूको दीर्घकालीन समाधानको आवश्यकता छ।"
        )

        # Future planning and recommendations
        content.append(
            f"भविष्यका लागि शिक्षक दरबन्दीको वैज्ञानिक विश्लेषण, योग्यताका आधारमा भर्ना, नियमित क्षमता विकास "
            f"कार्यक्रम र कार्यसम्पादनमा आधारित मूल्याङ्कन प्रणालीको विकास आवश्यक छ। डिजिटल शिक्षाका लागि "
            f"शिक्षकहरूको क्षमता विकास, अनुसन्धानमूलक शिक्षण र सामुदायिक सहभागितामा आधारित शैक्षिक "
            f"कार्यक्रमहरूमा जोड दिनुपर्छ।"
        )

        # Comprehensive conclusion
        content.append(
            f"समग्रमा यस गाउँपालिकाको शिक्षक तथा शैक्षिक जनशक्तिको अवस्था उत्साहजनक छ। विभिन्न तहमा "
            f"पर्याप्त संख्यामा शिक्षकहरूको उपस्थिति, विविध वित्तीय स्रोतबाट नियुक्ति र वडागत वितरणले "
            f"शैक्षिक पहुँचमा सकारात्मक प्रभाव पारेको छ। तर गुणस्तर सुधार, समान वितरण र दीर्घकालीन "
            f"स्थिरताका लागि निरन्तर प्रयास आवश्यक छ। उचित नीतिगत हस्तक्षेप, संसाधन परिचालन र सबै "
            f"सरोकारवालाहरूको सहकार्यमा यस क्षेत्रलाई थप प्रभावकारी बनाउन सकिने सम्भावना छ। शिक्षकहरूको "
            f"व्यावसायिक विकास र कल्याणमा लगानी गर्नु भनेको गाउँपालिकाको भविष्यमा लगानी गर्नु हो।"
        )

        return " ".join(content)

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

    def generate_chart_svg(self, data, chart_type="pie"):
        """Generate chart SVG based on chart type"""
        if chart_type == "pie":
            # Format data for pie chart - municipality data by teacher level
            municipality_data_by_level = data.get("municipality_data_by_level", {})
            formatted_data = {}

            for level_code, level_data in municipality_data_by_level.items():
                if (
                    isinstance(level_data, dict)
                    and level_data.get("teacher_count", 0) > 0
                ):
                    formatted_data[level_code] = {
                        "name_nepali": level_data.get("name_nepali", level_code),
                        "population": level_data.get("teacher_count", 0),
                        "percentage": level_data.get("percentage", 0),
                    }

            return self.chart_generator.generate_pie_chart_svg(
                formatted_data,
                include_title=False,
                title_nepali="शिक्षकको तह अनुसार वितरण",
                title_english="Teacher Distribution by Level",
            )

        elif chart_type == "bar":
            # Format data for bar chart - ward-wise data
            ward_data = data.get("ward_data", {})
            formatted_data = {}

            for ward_num, ward_info in ward_data.items():
                if (
                    isinstance(ward_info, dict)
                    and ward_info.get("total_teachers", 0) > 0
                ):
                    formatted_data[str(ward_num)] = {
                        "ward_name": f"वडा नं. {ward_num}",
                        "total_population": ward_info.get("total_teachers", 0),
                        "demographics": {
                            "total_teachers": {
                                "name_nepali": "कुल शिक्षक",
                                "population": ward_info.get("total_teachers", 0),
                                "percentage": 100,
                            },
                        },
                    }

            return self.chart_generator.generate_bar_chart_svg(
                formatted_data,
                include_title=False,
                title_nepali="वडागत शिक्षक वितरण",
                title_english="Ward-wise Teacher Distribution",
            )

        return None

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
            "charts": charts,
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
