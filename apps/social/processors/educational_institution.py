"""
Educational Institution Processor for Social Domain

This processor handles Ward Wise Educational Institution data (५.१.२) providing:
- Municipality-wide and ward-wise institutional statistics
- Student enrollment analysis by gender and year
- Chart generation using base class functionality
- Educational trends and institution type analysis
"""

from collections import defaultdict
from typing import Dict, Any
from django.db import models
from django.db.models import Sum, Count, Q
import os
import json

from apps.social.models import WardWiseEducationalInstitution, SchoolLevelChoice
from .base import BaseSocialProcessor


class EducationalInstitutionProcessor(BaseSocialProcessor):
    """Processor for Ward Wise Educational Institution data"""

    def __init__(self):
        super().__init__()
        # Customize chart dimensions for educational data
        self.pie_chart_width = 800
        self.pie_chart_height = 500
        self.bar_chart_width = 1000
        self.bar_chart_height = 600
        self.chart_radius = 160

        # Set educational-specific colors
        self.chart_generator.colors = {
            "SECONDARY": "#1976D2",  # Secondary schools (मा.वि.)
            "PRIMARY": "#4CAF50",  # Primary schools (प्रा.वि.)
            "LOWER_SECONDARY": "#FF9800",  # Lower secondary (आ.वि.)
            "EARLY_CHILDHOOD": "#9C27B0",  # Early childhood (बा.वि.के.)
            "OTHER": "#607D8B",
            "male_students": "#2196F3",
            "female_students": "#E91E63",
            "total_students": "#4CAF50",
        }

    def get_section_title(self):
        """Return the section title for educational institutions"""
        return "५.१.२ तहगत रुपमा शैक्षिक संस्था/विद्यालय र विद्यार्थी विवरण"

    def get_section_number(self):
        """Return the section number for educational institutions"""
        return "5.1.2"

    def get_category_name(self):
        """Return category name for file naming"""
        return "educational_institution"

    def get_data(self) -> Dict[str, Any]:
        """Get educational institution data aggregated from new JSON fixtures (per-year, per-school, per-grade, per-gender)"""
        try:
            fixtures_dir = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), "fixtures"
            )
            years = ["2079", "2080", "2081"]
            all_years_data = {}
            for year in years:
                file_path = os.path.join(
                    fixtures_dir, f"educational_institution_{year}.json"
                )
                if os.path.exists(file_path):
                    with open(file_path, "r", encoding="utf-8") as f:
                        all_years_data[year] = json.load(f)
                else:
                    all_years_data[year] = []

            # Aggregate data
            municipality_data = {}
            ward_data = {}
            total_institutions = 0
            total_male_students = 0
            total_female_students = 0
            per_grade_data = {}
            per_school_data = {}

            latest_year = years[-1]
            latest_data = all_years_data[latest_year]

            # --- Municipality-wide and ward-wise aggregation ---
            for entry in latest_data:
                ward = entry.get("ward_number")
                school_level = entry.get("school_level")
                school_type = entry.get("school_type", "OTHER")
                institution_name = entry.get("institution_name")
                student_counts = entry.get("student_counts", {})
                if not ward:
                    continue
                # Per-school aggregation
                if ward not in ward_data:
                    ward_data[ward] = {
                        "institution_count": 0,
                        "male_students": 0,
                        "female_students": 0,
                        "total_students": 0,
                        "gender_ratio": 0,
                        "institutions": [],
                        "per_grade": {},
                    }
                ward_data[ward]["institution_count"] += 1
                school_male = 0
                school_female = 0
                school_total = 0
                school_per_grade = {}
                for grade, gdata in student_counts.items():
                    boys = gdata.get("boys", 0)
                    girls = gdata.get("girls", 0)
                    total = gdata.get("total", boys + girls)
                    school_male += boys
                    school_female += girls
                    school_total += total
                    # Per-grade aggregation (municipality)
                    if grade not in per_grade_data:
                        per_grade_data[grade] = {"male": 0, "female": 0, "total": 0}
                    per_grade_data[grade]["male"] += boys
                    per_grade_data[grade]["female"] += girls
                    per_grade_data[grade]["total"] += total
                    # Per-grade per-school
                    school_per_grade[grade] = {
                        "male": boys,
                        "female": girls,
                        "total": total,
                    }
                ward_data[ward]["male_students"] += school_male
                ward_data[ward]["female_students"] += school_female
                ward_data[ward]["total_students"] += school_total
                # Per-school data
                school_info = {
                    "name": institution_name,
                    "level": school_level,
                    "type": school_type,
                    "male_students": school_male,
                    "female_students": school_female,
                    "total_students": school_total,
                    "per_grade": school_per_grade,
                }
                ward_data[ward]["institutions"].append(school_info)
                # Per-school (municipality)
                per_school_data[institution_name] = school_info
                # Municipality-wide by level
                if school_level not in municipality_data:
                    municipality_data[school_level] = {
                        "institution_count": 0,
                        "male_students": 0,
                        "female_students": 0,
                        "total_students": 0,
                        "name_nepali": self._get_level_name_nepali(school_level),
                    }
                municipality_data[school_level]["institution_count"] += 1
                municipality_data[school_level]["male_students"] += school_male
                municipality_data[school_level]["female_students"] += school_female
                municipality_data[school_level]["total_students"] += school_total
                total_institutions += 1
                total_male_students += school_male
                total_female_students += school_female

            # Calculate gender ratios and percentages
            total_students = total_male_students + total_female_students
            for ward in ward_data:
                w = ward_data[ward]
                if w["total_students"] > 0:
                    w["gender_ratio"] = round(
                        (w["female_students"] / w["total_students"]) * 100, 1
                    )
            for level in municipality_data:
                l = municipality_data[level]
                if total_students > 0:
                    l["percentage"] = round(
                        (l["total_students"] / total_students) * 100, 1
                    )
                else:
                    l["percentage"] = 0
                l["gender_ratio"] = (
                    round((l["female_students"] / l["total_students"]) * 100, 1)
                    if l["total_students"] > 0
                    else 0
                )

            # Historical data for trend analysis
            historical_data = {}
            for year in years:
                ydata = all_years_data[year]
                y_male = 0
                y_female = 0
                y_institutions = 0
                for entry in ydata:
                    grades = entry.get("grades", {})
                    for g in grades.values():
                        y_male += g.get("male", 0)
                        y_female += g.get("female", 0)
                    y_institutions += 1
                y_total = y_male + y_female
                historical_data[year] = {
                    "male_students": y_male,
                    "female_students": y_female,
                    "total_students": y_total,
                    "total_institutions": y_institutions,
                    "gender_ratio": (
                        round((y_female / y_total) * 100, 1) if y_total > 0 else 0
                    ),
                }

            return {
                "municipality_data": municipality_data,
                "ward_data": ward_data,
                "per_grade_data": per_grade_data,
                "per_school_data": per_school_data,
                "historical_data": historical_data,
                "total_institutions": total_institutions,
                "total_students": total_students,
                "total_male_students": total_male_students,
                "total_female_students": total_female_students,
                "gender_ratio": (
                    round((total_female_students / total_students) * 100, 1)
                    if total_students > 0
                    else 0
                ),
                "years_available": years,
                "latest_year": latest_year,
            }
        except Exception as e:
            print(f"Error in educational institution data processing: {e}")
            return self._empty_data_structure()

    def _empty_data_structure(self) -> Dict[str, Any]:
        """Return empty data structure when no data available"""
        return {
            "municipality_data": {},
            "ward_data": {},
            "historical_data": {},
            "total_institutions": 0,
            "total_students": 0,
            "total_male_students": 0,
            "total_female_students": 0,
            "gender_ratio": 0,
            "years_available": [],
            "latest_year": "2081",
        }

    def _get_level_name_nepali(self, level_code):
        """Get Nepali name for school level"""
        level_names = {
            SchoolLevelChoice.SECONDARY: "माध्यमिक विद्यालय",
            SchoolLevelChoice.PRIMARY: "प्राथमिक विद्यालय",
            SchoolLevelChoice.LOWER_SECONDARY: "निम्न माध्यमिक विद्यालय",
            SchoolLevelChoice.EARLY_CHILDHOOD: "बाल विकास केन्द्र",
            SchoolLevelChoice.OTHER: "अन्य",
        }
        return level_names.get(level_code, "अज्ञात")

    def _get_historical_trends(self):
        """Get historical enrollment trends"""
        historical = {}
        years = ["2079", "2080", "2081"]

        for year in years:
            year_stats = WardWiseEducationalInstitution.objects.filter(
                data_year=year
            ).aggregate(
                total_male=Sum("male_students"),
                total_female=Sum("female_students"),
                total_institutions=Count("institution_name", distinct=True),
            )

            male = year_stats["total_male"] or 0
            female = year_stats["total_female"] or 0
            total = male + female
            institutions = year_stats["total_institutions"] or 0

            historical[year] = {
                "male_students": male,
                "female_students": female,
                "total_students": total,
                "total_institutions": institutions,
                "gender_ratio": round((female / total) * 100, 1) if total > 0 else 0,
            }

        return historical

    def generate_analysis_text(self, data: Dict[str, Any]) -> str:
        """Generate comprehensive analysis text for educational institutions"""
        if not data or data["total_students"] == 0:
            return (
                "यस गाउँपालिकामा शैक्षिक संस्थाहरूको विस्तृत तथ्याङ्क उपलब्ध छैन। "
                "शैक्षिक क्षेत्रको विकासका लागि थप अध्ययन र सर्वेक्षण आवश्यक छ।"
            )

        from apps.reports.utils.nepali_numbers import (
            format_nepali_number,
            format_nepali_percentage,
        )

        # Build comprehensive analysis
        content = []

        # Introduction based on provided content
        content.append(
            "यस गाउँपालिकाको शैक्षिक अवस्थालाई हेर्दा यहाँ ४३ वटा सामुदायिक विद्यालयहरु सञ्चालनमा रहेका छन्। "
            "यस बाहेक यहाँ कुनैपनि किसिमका धार्मिक विद्यालय, प्राविधिक विद्यालय, सामुदायिक सिकाई केन्द्रहरु "
            "सञ्चालनमा रहेका छैनन्। उच्च शिक्षा प्राप्तिका लागि यहाँबाट अन्य स्थानहरुमा जानुपर्ने बाध्यता रहेको छ। "
            "यसैले स्थानीय शैक्षिक संस्थाहरूको सुदृढीकरण र विकास नीतिगत प्राथमिकताको रूपमा देखिन्छ। "
        )

        # Current statistics
        total_students = data["total_students"]
        total_institutions = data["total_institutions"]
        male_students = data["total_male_students"]
        female_students = data["total_female_students"]
        gender_ratio = data["gender_ratio"]

        content.append(
            f"वर्तमानमा यस गाउँपालिकामा कुल {format_nepali_number(total_institutions)} वटा शैक्षिक संस्थाहरूमा "
            f"{format_nepali_number(total_students)} जना विद्यार्थीहरू अध्ययनरत छन्। "
            f"यसमध्ये {format_nepali_number(male_students)} जना पुरुष र "
            f"{format_nepali_number(female_students)} जना महिला विद्यार्थीहरू छन्। "
            f"महिला विद्यार्थीहरूको अनुपात {format_nepali_percentage(gender_ratio)} रहेको छ। "
            f"यो तथ्याङ्कले गाउँपालिकामा शैक्षिक पहुँच र भागीदारीको स्थितिलाई स्पष्ट रूपमा देखाउँछ।<br>"
        )

        # School level analysis
        municipality_data = data["municipality_data"]
        if municipality_data:
            # Find dominant school level
            sorted_levels = sorted(
                municipality_data.items(),
                key=lambda x: x[1]["total_students"],
                reverse=True,
            )

            if sorted_levels:
                top_level = sorted_levels[0]
                level_name = top_level[1]["name_nepali"]
                level_students = top_level[1]["total_students"]
                level_percentage = top_level[1]["percentage"]
                level_institutions = top_level[1]["institution_count"]

                content.append(
                    f"शैक्षिक संस्थाहरूको तहगत वितरणलाई विश्लेषण गर्दा {level_name}हरूको संख्या सबैभन्दा बढी रहेको देखिन्छ। "
                    f"यस तहका {format_nepali_number(level_institutions)} वटा संस्थामा "
                    f"{format_nepali_number(level_students)} जना विद्यार्थीहरू अध्ययन गरिरहेका छन्। "
                    f"यो कुल विद्यार्थी संख्याको {format_nepali_percentage(level_percentage)} प्रतिनिधित्व गर्छ। "
                    f"यसले शैक्षिक संरचनामा यो तहको प्रभुत्व र महत्त्वलाई स्पष्ट पार्छ। "
                )

            # Analyze second most common level
            if len(sorted_levels) > 1:
                second_level = sorted_levels[1]
                second_name = second_level[1]["name_nepali"]
                second_students = second_level[1]["total_students"]
                second_percentage = second_level[1]["percentage"]
                second_institutions = second_level[1]["institution_count"]

                content.append(
                    f"दोस्रो स्थानमा {second_name}हरू छन् जसमा {format_nepali_number(second_institutions)} वटा संस्थामा "
                    f"{format_nepali_number(second_students)} जना विद्यार्थीहरू अध्ययनरत छन्। "
                    f"यो कुल विद्यार्थी संख्याको {format_nepali_percentage(second_percentage)} हो। "
                    f"यसले शैक्षिक संरचनामा विविधता र विभिन्न तहको आवश्यकतालाई दर्शाउँछ।<br>"
                )

            # Analyze all levels comprehensively
            primary_count = 0
            secondary_count = 0
            early_childhood_count = 0

            for level_code, level_data in municipality_data.items():
                if level_data["total_students"] > 0:
                    if "प्राथमिक" in level_data["name_nepali"]:
                        primary_count += level_data["total_students"]
                    elif "माध्यमिक" in level_data["name_nepali"]:
                        secondary_count += level_data["total_students"]
                    elif "बाल" in level_data["name_nepali"]:
                        early_childhood_count += level_data["total_students"]

            content.append(
                f"शैक्षिक पिरामिडको संरचनालाई हेर्दा प्राथमिक तहमा {format_nepali_number(primary_count)} जना, "
                f"माध्यमिक तहमा {format_nepali_number(secondary_count)} जना र "
                f"बाल विकास तहमा {format_nepali_number(early_childhood_count)} जना विद्यार्थीहरू छन्। "
                f"यसले शैक्षिक पहुँचको क्रमिक विकास र विभिन्न उमेर समूहका बालबालिकाहरूको शिक्षामा पहुँचको स्थितिलाई प्रकट गर्छ। "
            )

        # Ward-wise distribution analysis
        ward_data = data["ward_data"]
        if ward_data:
            # Find ward with most students
            max_ward = max(ward_data.items(), key=lambda x: x[1]["total_students"])
            ward_num = max_ward[0]
            ward_students = max_ward[1]["total_students"]
            ward_institutions = max_ward[1]["institution_count"]
            ward_gender_ratio = max_ward[1]["gender_ratio"]

            # Find ward with least students
            min_ward = min(ward_data.items(), key=lambda x: x[1]["total_students"])
            min_ward_num = min_ward[0]
            min_ward_students = min_ward[1]["total_students"]
            min_ward_institutions = min_ward[1]["institution_count"]

            content.append(
                f"वडागत शैक्षिक वितरणको विश्लेषण गर्दा वडा नं. {format_nepali_number(ward_num)} मा सबैभन्दा बढी "
                f"{format_nepali_number(ward_students)} जना विद्यार्थीहरू "
                f"{format_nepali_number(ward_institutions)} वटा शैक्षिक संस्थामा अध्ययनरत छन्। "
                f"यस वडामा महिला विद्यार्थीहरूको अनुपात {format_nepali_percentage(ward_gender_ratio)} रहेको छ। "
                f"अर्कोतर्फ वडा नं. {format_nepali_number(min_ward_num)} मा सबैभन्दा कम "
                f"{format_nepali_number(min_ward_students)} जना विद्यार्थीहरू "
                f"{format_nepali_number(min_ward_institutions)} वटा संस्थामा अध्ययनरत छन्। "
                f"यसले वडाहरूबीच शैक्षिक पहुँच र संस्थागत क्षमतामा असमानता रहेको संकेत गर्छ। "
            )

            # Analyze geographic distribution
            ward_count = len(ward_data)
            avg_students_per_ward = total_students / ward_count if ward_count > 0 else 0
            above_avg_wards = sum(
                1
                for w in ward_data.values()
                if w["total_students"] > avg_students_per_ward
            )

            content.append(
                f"गाउँपालिकाका {format_nepali_number(ward_count)} वटा वडामा शैक्षिक संस्थाहरू फैलिएका छन्। "
                f"प्रति वडा औसत {format_nepali_number(int(avg_students_per_ward))} जना विद्यार्थीहरू छन्। "
                f"{format_nepali_number(above_avg_wards)} वटा वडामा औसतभन्दा बढी विद्यार्थीहरू छन्। "
                f"यसले शैक्षिक संसाधनको वितरण र पहुँचमा क्षेत्रीय भिन्नतालाई देखाउँछ।<br>"
            )

        # Historical trends analysis
        historical_data = data["historical_data"]
        if len(historical_data) >= 2:
            years = sorted(historical_data.keys())
            if len(years) >= 2:
                first_year = years[0]
                last_year = years[-1]
                first_total = historical_data[first_year]["total_students"]
                last_total = historical_data[last_year]["total_students"]
                first_institutions = historical_data[first_year]["total_institutions"]
                last_institutions = historical_data[last_year]["total_institutions"]

                if first_total > 0:
                    change_percent = ((last_total - first_total) / first_total) * 100
                    trend = "वृद्धि" if change_percent > 0 else "कमी"

                    inst_change = last_institutions - first_institutions
                    inst_trend = "वृद्धि" if inst_change > 0 else "कमी"

                    content.append(
                        f"ऐतिहासिक प्रवृत्तिको विश्लेषण गर्दा वि.सं. {format_nepali_number(first_year)} देखि {format_nepali_number(last_year)} सम्मको अवधिमा "
                        f"विद्यार्थी संख्यामा {format_nepali_percentage(abs(change_percent))} को {trend} देखिएको छ। "
                        f"यो प्रवृत्तिले गाउँपालिकामा शैक्षिक क्षेत्रको विकास र परिवर्तनको गतिलाई स्पष्ट पार्छ। "
                    )

                    if inst_change > 0:
                        content.append(
                            f"यसैगरी शैक्षिक संस्थाहरूको संख्यामा {format_nepali_number(abs(inst_change))} को {inst_trend} भएको छ। "
                        )

                # Gender ratio trends
                first_gender_ratio = historical_data[first_year]["gender_ratio"]
                last_gender_ratio = historical_data[last_year]["gender_ratio"]
                gender_change = last_gender_ratio - first_gender_ratio

                if abs(gender_change) > 1:
                    gender_trend = "सुधार" if gender_change > 0 else "गिरावट"
                    content.append(
                        f"लैङ्गिक समानताको दृष्टिकोणले हेर्दा यस अवधिमा महिला विद्यार्थीहरूको अनुपातमा "
                        f"{format_nepali_percentage(abs(gender_change))} को {gender_trend} देखिएको छ। "
                        f"यसले लैङ्गिक समानताको क्षेत्रमा भएको प्रगति वा चुनौतीलाई प्रकट गर्छ। "
                    )

        # Comprehensive gender equity analysis
        if gender_ratio > 52:
            content.append(
                "लैङ्गिक समानताको विश्लेषण गर्दा महिला विद्यार्थीहरूको अनुपात पुरुषको तुलनामा उच्च रहेको सकारात्मक संकेत छ। "
                "यसले महिला शिक्षामा समुदायको सकारात्मक दृष्टिकोण र नीतिगत प्रयासहरूको सफलतालाई दर्शाउँछ। "
                "तर यसैसाथ पुरुष विद्यार्थीहरूको कम संख्याको कारण खोजी गरेर सन्तुलित विकास गर्नुपर्ने देखिन्छ। "
            )
        elif gender_ratio >= 45 and gender_ratio <= 52:
            content.append(
                "लैङ्गिक समानताको दृष्टिकोणले हेर्दा यस गाउँपालिकामा पुरुष र महिला विद्यार्थीहरूको संख्यामा उत्कृष्ट सन्तुलन रहेको देखिन्छ। "
                "यो अनुपात राष्ट्रिय र अन्तर्राष्ट्रिय मापदण्डको दृष्टिकोणले आदर्श मानिन्छ। "
                "यसले शैक्षिक पहुँचमा लैङ्गिक भेदभावको न्यूनीकरण र समान अवसरको सुनिश्चितताको प्रमाण हो। "
            )
        else:
            content.append(
                "महिला विद्यार्थीहरूको अनुपात अपेक्षाकृत कम रहेकोले लैङ्गिक समानताका लागि विशेष प्रयासहरू आवश्यक छ। "
                "महिला शिक्षामा विशेष छात्रवृत्ति, सुरक्षित शैक्षिक वातावरण, र सामुदायिक जागरूकता कार्यक्रमहरू सञ्चालन गर्नुपर्ने देखिन्छ। "
                "यसले दीर्घकालीन सामाजिक विकास र लैङ्गिक न्यायमा महत्त्वपूर्ण योगदान गर्नेछ। "
            )

        # Institutional capacity analysis
        if total_institutions > 0 and total_students > 0:
            avg_students_per_institution = total_students / total_institutions
            content.append(
                f"संस्थागत क्षमताको विश्लेषण गर्दा प्रति संस्था औसत {format_nepali_number(int(avg_students_per_institution))} जना विद्यार्थीहरू छन्। "
                f"यो अनुपातले शैक्षिक संस्थाहरूको आकार र शिक्षकदेखि विद्यार्थी अनुपातको सन्दर्भमा महत्त्वपूर्ण जानकारी प्रदान गर्छ। "
                f"गुणस्तरीय शिक्षाका लागि यो अनुपात उपयुक्त छ कि छैन भनेर मूल्याङ्कन गर्नुपर्ने देखिन्छ।<br>"
            )

        # Challenges, opportunities and future recommendations
        content.append(
            "शैक्षिक क्षेत्रका चुनौतीहरूलाई हेर्दा उच्च शिक्षाका लागि स्थानीय सुविधाको अभाव प्रमुख समस्या हो। "
            "यसका साथै प्राविधिक र व्यावसायिक शिक्षाका कार्यक्रमहरूको अभाव, गुणस्तरीय शिक्षकको कमी, र आधुनिक शैक्षिक प्रविधिको पहुँचमा कमी रहेको छ। "
            "तर सामुदायिक विद्यालयहरूको बलियो आधार र बढ्दो साक्षरता दरले भविष्यका लागि आशाजनक सम्भावनाहरू सिर्जना गरेको छ। "
            "भविष्यका लागि उच्च माध्यमिक शिक्षा र व्यावसायिक तालिमका कार्यक्रमहरू स्थापना गर्नुपर्ने देखिन्छ। "
            "डिजिटल साक्षरता कार्यक्रम, शिक्षक क्षमता विकास, र शैक्षिक पूर्वाधार सुधारमा विशेष जोड दिनुपर्छ। "
            "समग्रमा यस गाउँपालिकाको शैक्षिक क्षेत्रले निरन्तर प्रगति गरिरहेको छ र उचित नीतिगत हस्तक्षेप र लगानीमार्फत "
            "यसलाई थप उन्नत बनाउन सकिने सम्भावना छ। "
            "सामुदायिक सहभागिता र स्थानीय सरकारको प्रतिबद्धताले शैक्षिक गुणस्तर र पहुँचमा "
            "उल्लेखनीय सुधार ल्याउन सक्छ।"
        )

        return "".join(content)

    def generate_pie_chart(self, data, title="विद्यालयको तह अनुसार विद्यार्थी वितरण"):
        """Generate pie chart for school level distribution"""
        return self.chart_generator.generate_pie_chart_svg(
            data,
            include_title=False,
            title_nepali=title,
            title_english="Student Distribution by School Level",
        )

    def process_for_pdf(self):
        """Process educational institution data for PDF generation"""
        data = self.get_data()

        # Generate analysis text
        analysis_text = self.generate_analysis_text(data)

        # Generate and save charts
        charts = self.generate_and_save_charts(data)

        return {
            "section_title": self.get_section_title(),
            "section_number": self.get_section_number(),
            "municipality_data": data["municipality_data"],
            "ward_data": data["ward_data"],
            "historical_data": data["historical_data"],
            "total_institutions": data["total_institutions"],
            "total_students": data["total_students"],
            "total_male_students": data["total_male_students"],
            "total_female_students": data["total_female_students"],
            "gender_ratio": data["gender_ratio"],
            "coherent_analysis": analysis_text,
            "charts": charts,
        }

    def generate_chart_svg(self, data, chart_type="pie"):
        """Generate chart SVG based on chart type"""
        if chart_type == "pie":
            # Format data for pie chart - municipality data by school level
            municipality_data = data.get("municipality_data", {})
            formatted_data = {}

            for level_code, level_data in municipality_data.items():
                if (
                    isinstance(level_data, dict)
                    and level_data.get("total_students", 0) > 0
                ):
                    formatted_data[level_code] = {
                        "name_nepali": level_data.get("name_nepali", level_code),
                        "population": level_data.get("total_students", 0),
                        "percentage": level_data.get("percentage", 0),
                    }

            return self.chart_generator.generate_pie_chart_svg(
                formatted_data,
                include_title=False,
                title_nepali="विद्यालयको तह अनुसार विद्यार्थी वितरण",
                title_english="Student Distribution by School Level",
            )

        elif chart_type == "bar":
            # Format data for bar chart - ward-wise data
            ward_data = data.get("ward_data", {})
            formatted_data = {}

            for ward_num, ward_info in ward_data.items():
                if (
                    isinstance(ward_info, dict)
                    and ward_info.get("total_students", 0) > 0
                ):
                    formatted_data[str(ward_num)] = {
                        "ward_name": f"वडा नं. {ward_num}",
                        "total_population": ward_info.get("total_students", 0),
                        "demographics": {
                            "male_students": {
                                "name_nepali": "पुरुष",
                                "population": ward_info.get("male_students", 0),
                                "percentage": round(
                                    (
                                        ward_info.get("male_students", 0)
                                        / ward_info.get("total_students", 1)
                                    )
                                    * 100,
                                    1,
                                ),
                            },
                            "female_students": {
                                "name_nepali": "महिला",
                                "population": ward_info.get("female_students", 0),
                                "percentage": round(
                                    (
                                        ward_info.get("female_students", 0)
                                        / ward_info.get("total_students", 1)
                                    )
                                    * 100,
                                    1,
                                ),
                            },
                        },
                    }

            return self.chart_generator.generate_bar_chart_svg(
                formatted_data,
                include_title=False,
                title_nepali="वडागत शैक्षिक संस्था र विद्यार्थी वितरण",
                title_english="Ward-wise Educational Institution and Student Distribution",
            )

        return None

    def _format_municipality_data_for_pie_chart(self, municipality_data):
        """Format municipality data for pie chart generation"""
        if not municipality_data:
            return {}

        formatted_data = {}
        for level_code, level_data in municipality_data.items():
            if isinstance(level_data, dict) and level_data.get("total_students", 0) > 0:
                formatted_data[level_code] = {
                    "name_nepali": level_data.get("name_nepali", level_code),
                    "population": level_data.get("total_students", 0),
                    "percentage": level_data.get("percentage", 0),
                }
        return formatted_data

    def _format_ward_data_for_bar_chart(self, ward_data):
        """Format ward data for bar chart generation"""
        if not ward_data:
            return {}

        formatted_data = {}
        for ward_num, ward_info in ward_data.items():
            if isinstance(ward_info, dict) and ward_info.get("total_students", 0) > 0:
                formatted_data[str(ward_num)] = {
                    "ward_name": f"वडा नं. {ward_num}",
                    "total_population": ward_info.get("total_students", 0),
                    "demographics": {
                        "male_students": {
                            "name_nepali": "पुरुष",
                            "population": ward_info.get("male_students", 0),
                            "percentage": round(
                                (
                                    ward_info.get("male_students", 0)
                                    / ward_info.get("total_students", 1)
                                )
                                * 100,
                                1,
                            ),
                        },
                        "female_students": {
                            "name_nepali": "महिला",
                            "population": ward_info.get("female_students", 0),
                            "percentage": round(
                                (
                                    ward_info.get("female_students", 0)
                                    / ward_info.get("total_students", 1)
                                )
                                * 100,
                                1,
                            ),
                        },
                    },
                }
        return formatted_data
