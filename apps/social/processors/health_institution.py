"""
Health Institution Processor for Social Domain

This processor handles Ward Wise Health Institution data (५.२.१) providing:
- Municipality-wide and ward-wise health institution statistics
- Detailed institution type analysis
- Chart generation using base class functionality
- Health facility distribution and access analysis
"""

from collections import defaultdict
from typing import Dict, Any

from django.db import models
from apps.social.models import WardWiseHealthInstitution, HealthInstitutionTypeChoice
from .base import BaseSocialProcessor


class HealthInstitutionProcessor(BaseSocialProcessor):
    """Processor for Ward Wise Health Institution"""

    def __init__(self):
        super().__init__()

    def get_section_title(self):
        """Return the section title for health institution"""
        return "५.२.१ स्वास्थ्य संस्था (अस्पताल, प्राथमिक स्वास्थ्य केन्द्र, स्वास्थ्य चौकी र आयुर्वेद केन्द्र) को विवरण"

    def get_section_number(self):
        """Return the section number for health institution"""
        return "5.2.1"

    def get_data(self) -> Dict[str, Any]:
        """Get health institution data aggregated by municipality and ward"""
        try:
            # Get all health institution data
            queryset = WardWiseHealthInstitution.objects.all().order_by(
                "ward_number", "name"
            )

            if not queryset.exists():
                return self._empty_data_structure()

            # Initialize data structures
            municipality_data = defaultdict(int)
            ward_data = defaultdict(lambda: defaultdict(int))
            detailed_data = []
            total_institutions = 0

            # Process each health institution
            for institution in queryset:
                institution_type = institution.institution_type
                ward_num = institution.ward_number

                # Municipality-wide aggregation
                municipality_data[institution_type] += 1
                total_institutions += 1

                # Ward-wise aggregation
                ward_data[ward_num][institution_type] += 1

                # Detailed institution data
                detailed_data.append(
                    {
                        "ward_number": ward_num,
                        "name": institution.name,
                        "type": institution.institution_type,
                        "type_display": institution.get_institution_type_display(),
                    }
                )

            # Convert defaultdicts to regular dicts
            municipality_data = dict(municipality_data)
            ward_data = {ward: dict(types) for ward, types in ward_data.items()}

            return {
                "municipality_data": municipality_data,
                "ward_data": ward_data,
                "detailed_data": detailed_data,
                "total_institutions": total_institutions,
                "institution_types": [
                    choice.value for choice in HealthInstitutionTypeChoice
                ],
            }

        except Exception as e:
            print(f"Error in HealthInstitutionProcessor.get_data: {str(e)}")
            return self._empty_data_structure()

    def _empty_data_structure(self) -> Dict[str, Any]:
        """Return empty data structure when no data available"""
        return {
            "municipality_data": {},
            "ward_data": {},
            "detailed_data": [],
            "total_institutions": 0,
            "institution_types": [
                choice.value for choice in HealthInstitutionTypeChoice
            ],
        }

    def generate_analysis_text(self, data: Dict[str, Any]) -> str:
        """Generate comprehensive analysis text for health institution"""
        if not data or data["total_institutions"] == 0:
            return """लुङ्ग्री गाउँपालिकामा स्वास्थ्य संस्थाको विवरण सम्बन्धी पर्याप्त तथ्यांक उपलब्ध छैन । स्वास्थ्य सेवाको पहुँच र गुणस्तर सुधारका लागि विस्तृत अध्ययन र तथ्यांक संकलन आवश्यक छ ।"""

        municipality_data = data["municipality_data"]
        ward_data = data["ward_data"]
        detailed_data = data["detailed_data"]
        total_institutions = data["total_institutions"]

        # Import necessary formatting functions
        from apps.reports.utils.nepali_numbers import (
            format_nepali_number,
            format_nepali_percentage,
        )

        # Find major institution types
        major_institution_types = []
        for institution_type, count in municipality_data.items():
            percentage = (count / total_institutions) * 100
            type_display = dict(HealthInstitutionTypeChoice.choices)[institution_type]
            major_institution_types.append((type_display, count, percentage))

        major_institution_types.sort(key=lambda x: x[1], reverse=True)

        # Build comprehensive analysis
        content = []

        # Introduction
        nepali_total = format_nepali_number(total_institutions)
        content.append(
            f"""लुङ्ग्री गाउँपालिकामा कुल {nepali_total} स्वास्थ्य संस्थाहरूको विश्लेषण गर्दा स्वास्थ्य सेवाको पहुँच र वितरणको स्थिति स्पष्ट देखिन्छ । यी संस्थाहरूले गाउँपालिकाका नागरिकहरूलाई प्राथमिक देखि विशेषीकृत स्वास्थ्य सेवासम्म प्रदान गर्ने महत्वपूर्ण भूमिका खेल्छन् ।"""
        )

        # Institution type analysis
        if major_institution_types:
            content.append("**संस्था प्रकार अनुसार विश्लेषण:**")

            # Top institution type
            top_type, top_count, top_percentage = major_institution_types[0]
            nepali_count = format_nepali_number(top_count)
            nepali_percentage = format_nepali_percentage(top_percentage)

            content.append(
                f"""गाउँपालिकामा सबैभन्दा धेरै {top_type} रहेका छन् जुन कुल संस्थाहरूको {nepali_percentage} ({nepali_count} संस्था) हो । यसले गाउँपालिकामा यस प्रकारको स्वास्थ्य सेवाको महत्व र प्राथमिकतालाई झल्काउँछ ।"""
            )

            # Other significant types
            if len(major_institution_types) > 1:
                other_types = []
                for type_display, count, percentage in major_institution_types[
                    1:4
                ]:  # Top 3 excluding first
                    nepali_count = format_nepali_number(count)
                    nepali_percentage = format_nepali_percentage(percentage)
                    other_types.append(
                        f"{type_display} {nepali_percentage} ({nepali_count} संस्था)"
                    )

                if other_types:
                    content.append(
                        f"""अन्य प्रमुख स्वास्थ्य संस्थाहरूमा {', '.join(other_types)} रहेका छन् । यसले स्वास्थ्य सेवाको विविधीकरण र बहुस्तरीय सेवा प्रणालीलाई जनाउँछ ।"""
                    )

        # Ward-wise distribution analysis
        content.append("**वडागत वितरण विश्लेषण:**")

        # Find wards with most/least institutions
        ward_totals = {}
        for ward_num, types in ward_data.items():
            ward_totals[ward_num] = sum(types.values())

        if ward_totals:
            max_ward = max(ward_totals, key=ward_totals.get)
            min_ward = min(ward_totals, key=ward_totals.get)
            max_count = ward_totals[max_ward]
            min_count = ward_totals[min_ward]

            nepali_max_ward = format_nepali_number(max_ward)
            nepali_min_ward = format_nepali_number(min_ward)
            nepali_max_count = format_nepali_number(max_count)
            nepali_min_count = format_nepali_number(min_count)

            content.append(
                f"""वडा नं. {nepali_max_ward} मा सबैभन्दा धेरै {nepali_max_count} स्वास्थ्य संस्थाहरू रहेका छन् भने वडा नं. {nepali_min_ward} मा सबैभन्दा कम {nepali_min_count} स्वास्थ्य संस्थाहरू छन् । यसले वडाहरूबीच स्वास्थ्य सेवा पहुँचमा भिन्नतालाई देखाउँछ ।"""
            )

        # Service coverage analysis
        content.append("**सेवा क्षेत्र र पहुँच विश्लेषण:**")

        # Count different types of institutions
        health_posts = municipality_data.get(HealthInstitutionTypeChoice.HEALTH_POST, 0)
        community_units = municipality_data.get(
            HealthInstitutionTypeChoice.COMMUNITY_HEALTH_UNIT, 0
        )
        primary_centers = municipality_data.get(
            HealthInstitutionTypeChoice.PRIMARY_HEALTH_CENTER, 0
        )

        nepali_health_posts = format_nepali_number(health_posts)
        nepali_community_units = format_nepali_number(community_units)
        nepali_primary_centers = format_nepali_number(primary_centers)

        content.append(
            f"""गाउँपालिकामा {nepali_health_posts} स्वास्थ्य चौकी, {nepali_community_units} सामुदायिक स्वास्थ्य इकाइ र {nepali_primary_centers} प्राथमिक स्वास्थ्य केन्द्रहरू रहेकाले प्राथमिक स्वास्थ्य सेवाको पहुँच राम्रो देखिन्छ । यी संस्थाहरूले आधारभूत स्वास्थ्य सेवा, निवारक उपचार र स्वास्थ्य शिक्षामा महत्वपूर्ण योगदान पुर्‍याइरहेका छन् ।"""
        )

        # Challenges and opportunities
        content.append("**चुनौती र अवसरहरू:**")

        ward_count = len(ward_data)
        wards_without_institutions = 7 - ward_count  # Assuming 7 wards total

        if wards_without_institutions > 0:
            nepali_wards_without = format_nepali_number(wards_without_institutions)
            content.append(
                f"""केही वडाहरूमा स्वास्थ्य संस्थाको अभाव देखिएको छ जसले स्वास्थ्य सेवा पहुँचमा असमानता सिर्जना गरेको छ । सबै वडामा कम्तिमा एक स्वास्थ्य सेवा केन्द्र स्थापना गर्नु आवश्यक छ ।"""
            )

        # Recommendations
        content.append("**सिफारिसहरू:**")
        content.append(
            """स्वास्थ्य सेवाको गुणस्तर सुधारका लागि आधुनिक उपकरण र दक्ष जनशक्तिको व्यवस्था गर्नुपर्छ । टेलिमेडिसिन सेवा, मोबाइल हेल्थ क्लिनिक र आपतकालीन स्वास्थ्य सेवाको विस्तार गरी सबै नागरिकहरूको स्वास्थ्य सेवामा पहुँच सुनिश्चित गर्नुपर्छ । स्वास्थ्य संस्थाहरूबीच समन्वय र रेफरल प्रणालीलाई सुदृढ बनाउनु आवश्यक छ ।"""
        )

        return "\n\n".join(content)

    def process_for_pdf(self):
        """Process health institution data for PDF generation"""
        try:
            data = self.get_data()
            coherent_analysis = self.generate_analysis_text(data)

            # Generate municipality-wide pie chart
            municipality_chart_data = []
            if data["municipality_data"]:
                for institution_type, count in data["municipality_data"].items():
                    type_display = dict(HealthInstitutionTypeChoice.choices)[
                        institution_type
                    ]
                    municipality_chart_data.append(
                        {
                            "label": type_display,
                            "value": count,
                            "color": self._get_institution_type_color(institution_type),
                        }
                    )

            municipality_chart_path = None
            if municipality_chart_data:
                municipality_chart_path = self.create_pie_chart(
                    data=municipality_chart_data,
                    title="गाउँपालिकामा स्वास्थ्य संस्थाको प्रकार अनुसार वितरण",
                    filename="health_institution_municipality_distribution",
                )

            # Generate ward-wise bar chart
            ward_chart_data = []
            if data["ward_data"]:
                ward_numbers = sorted(data["ward_data"].keys())

                # Get all institution types present
                all_types = set()
                for ward_types in data["ward_data"].values():
                    all_types.update(ward_types.keys())
                all_types = sorted(all_types)

                for institution_type in all_types:
                    type_display = dict(HealthInstitutionTypeChoice.choices)[
                        institution_type
                    ]
                    series_data = []
                    for ward_num in ward_numbers:
                        count = data["ward_data"][ward_num].get(institution_type, 0)
                        series_data.append(count)

                    ward_chart_data.append(
                        {
                            "name": type_display,
                            "data": series_data,
                            "color": self._get_institution_type_color(institution_type),
                        }
                    )

            ward_chart_path = None
            if ward_chart_data:
                ward_chart_path = self.create_bar_chart(
                    series_data=ward_chart_data,
                    categories=[f"वडा {w}" for w in sorted(data["ward_data"].keys())],
                    title="वडागत स्वास्थ्य संस्थाको वितरण",
                    filename="health_institution_ward_distribution",
                )

            return {
                "coherent_analysis": coherent_analysis,
                "municipality_data": data["municipality_data"],
                "ward_data": data["ward_data"],
                "detailed_data": data["detailed_data"],
                "total_institutions": data["total_institutions"],
                "municipality_chart_path": municipality_chart_path,
                "ward_chart_path": ward_chart_path,
            }

        except Exception as e:
            print(f"Error in HealthInstitutionProcessor.process_for_pdf: {str(e)}")
            return {
                "coherent_analysis": "स्वास्थ्य संस्था विश्लेषणमा त्रुटि भएको छ।",
                "municipality_data": {},
                "ward_data": {},
                "detailed_data": [],
                "total_institutions": 0,
                "municipality_chart_path": None,
                "ward_chart_path": None,
            }

    def _get_institution_type_color(self, institution_type: str) -> str:
        """Get color for institution type for consistent visualization"""
        color_map = {
            HealthInstitutionTypeChoice.HOSPITAL: "#e74c3c",  # Red
            HealthInstitutionTypeChoice.PRIMARY_HEALTH_CENTER: "#3498db",  # Blue
            HealthInstitutionTypeChoice.HEALTH_POST: "#2ecc71",  # Green
            HealthInstitutionTypeChoice.AYURVEDA_CENTER: "#f39c12",  # Orange
            HealthInstitutionTypeChoice.COMMUNITY_HEALTH_UNIT: "#9b59b6",  # Purple
            HealthInstitutionTypeChoice.SUB_HEALTH_POST: "#1abc9c",  # Teal
            HealthInstitutionTypeChoice.BIRTHING_CENTER: "#e67e22",  # Dark Orange
            HealthInstitutionTypeChoice.CLINIC: "#34495e",  # Dark Gray
            HealthInstitutionTypeChoice.OTHER: "#95a5a6",  # Gray
        }
        return color_map.get(institution_type, "#bdc3c7")  # Light Gray as default
