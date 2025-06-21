"""
School Dropout Social Processor

Handles school dropout social data processing, chart generation, and report formatting.
"""

from django.db import models
from .base import BaseSocialProcessor, BaseSocialReportFormatter
from ..models import WardWiseSchoolDropout, SchoolDropoutCauseTypeChoice
from apps.reports.utils.nepali_numbers import (
    format_nepali_number,
    format_nepali_percentage,
    to_nepali_digits,
)


class SchoolDropoutProcessor(BaseSocialProcessor):
    """Processor for school dropout social data"""

    def __init__(self):
        super().__init__()
        # Customize chart dimensions for school dropout
        self.pie_chart_width = 950
        self.pie_chart_height = 500
        self.chart_radius = 150
        # Set school dropout-specific colors with meaningful associations
        self.chart_generator.colors = {
            "UNKNOWN": "#9E9E9E",  # Grey - Unknown reasons
            "MARRIAGE": "#E91E63",  # Pink - Marriage (cultural factor)
            "HOUSE_HELP": "#FF9800",  # Orange - House help (economic)
            "EMPLOYMENT": "#2196F3",  # Blue - Employment (economic necessity)
            "OTHER": "#9C27B0",  # Purple - Other reasons
            "WANTED_STUDY_COMPLETED": "#4CAF50",  # Green - Completed desired study
            "EXPENSIVE": "#F44336",  # Red - Financial constraint
            "UNWILLING_PARENTS": "#795548",  # Brown - Parental attitude
            "FAR": "#607D8B",  # Blue Grey - Distance barrier
            "LIMITED_SPACE": "#FF5722",  # Deep Orange - Infrastructure
        }

    def get_section_title(self):
        return "विद्यालय वाहिर रहेका तथा विद्यालय छाडेका बालबालिकाहरुको विवरण"

    def get_section_number(self):
        return "५.१.६"

    def get_data(self):
        """Get school dropout data - both municipality-wide and ward-wise"""
        # Municipality-wide summary
        dropout_data = {}
        total_children = 0

        for dropout_choice in SchoolDropoutCauseTypeChoice.choices:
            dropout_code = dropout_choice[0]
            dropout_name = dropout_choice[1]

            dropout_population = (
                WardWiseSchoolDropout.objects.filter(cause=dropout_code).aggregate(
                    total=models.Sum("population")
                )["total"]
                or 0
            )

            if dropout_population > 0:  # Only include dropout causes with children
                dropout_data[dropout_code] = {
                    "name_english": dropout_code,
                    "name_nepali": dropout_name,
                    "population": dropout_population,
                    "percentage": 0,  # Will be calculated below
                }
                total_children += dropout_population

        # Calculate percentages
        for dropout_code in dropout_data:
            if total_children > 0:
                dropout_data[dropout_code]["percentage"] = (
                    dropout_data[dropout_code]["population"] / total_children * 100
                )

        # Ward-wise data
        ward_data = {}
        for ward_num in range(1, 8):  # Wards 1-7
            ward_children = (
                WardWiseSchoolDropout.objects.filter(ward_number=ward_num).aggregate(
                    total=models.Sum("population")
                )["total"]
                or 0
            )

            if ward_children > 0:
                ward_data[ward_num] = {
                    "ward_number": ward_num,
                    "ward_name": f"वडा नं. {to_nepali_digits(ward_num)}",
                    "total_population": ward_children,
                    "dropout_causes": {},
                }

                # Dropout cause breakdown for this ward
                for dropout_choice in SchoolDropoutCauseTypeChoice.choices:
                    dropout_code = dropout_choice[0]
                    dropout_name = dropout_choice[1]

                    dropout_population_ward = (
                        WardWiseSchoolDropout.objects.filter(
                            ward_number=ward_num, cause=dropout_code
                        ).aggregate(total=models.Sum("population"))["total"]
                        or 0
                    )

                    if dropout_population_ward > 0:
                        ward_data[ward_num]["dropout_causes"][dropout_code] = {
                            "name_nepali": dropout_name,
                            "population": dropout_population_ward,
                            "percentage": (
                                (dropout_population_ward / ward_children * 100)
                                if ward_children > 0
                                else 0
                            ),
                        }

        return {
            "municipality_data": dropout_data,
            "ward_data": ward_data,
            "total_children": total_children,
        }

    def generate_analysis_text(self, data):
        """Generate comprehensive analysis text for school dropout"""
        if not data or data["total_children"] == 0:
            return "विद्यालय छाड्ने बालबालिकाहरूको तथ्याङ्क उपलब्ध छैन।"

        total_children = data["total_children"]
        municipality_data = data["municipality_data"]
        ward_data = data["ward_data"]

        analysis_parts = []

        # Overall summary
        analysis_parts.append(
            f"लुङ्ग्री गाउँपालिकामा कुल {format_nepali_number(total_children)} बालबालिकाहरूले विभिन्न कारणहरूले गर्दा विद्यालय छाडेका वा विद्यालय वाहिर रहेका छन्।"
        )

        # Dominant cause analysis
        if municipality_data:
            # Find the most common dropout cause
            dominant_cause = max(
                municipality_data.items(), key=lambda x: x[1]["population"]
            )
            analysis_parts.append(
                f"विद्यालय छाड्नुको मुख्य कारणको आधारमा विश्लेषण गर्दा, {dominant_cause[1]['name_nepali']} सबैभन्दा बढी "
                f"{format_nepali_number(dominant_cause[1]['population'])} बालबालिकाहरूले "
                f"({format_nepali_percentage(dominant_cause[1]['percentage'])}) यस कारणले विद्यालय छाडेको देखिन्छ।"
            )

            # Economic factors analysis
            economic_causes = ["EXPENSIVE", "EMPLOYMENT", "HOUSE_HELP"]
            economic_children = sum(
                municipality_data.get(cause, {}).get("population", 0)
                for cause in economic_causes
            )
            economic_percentage = (
                (economic_children / total_children * 100) if total_children > 0 else 0
            )

            if economic_percentage > 0:
                analysis_parts.append(
                    f"आर्थिक कारणहरूको दृष्टिकोणले हेर्दा, {format_nepali_number(economic_children)} बालबालिकाहरू "
                    f"({format_nepali_percentage(economic_percentage)}) ले महंगो लाग्ने, रोजगारी र घरको काममा सहयोग जस्ता "
                    f"आर्थिक कारणहरूले गर्दा विद्यालय छाडेका छन्।"
                )

            # Marriage analysis (especially concerning for girls)
            if "MARRIAGE" in municipality_data:
                marriage_children = municipality_data["MARRIAGE"]["population"]
                marriage_percentage = municipality_data["MARRIAGE"]["percentage"]
                analysis_parts.append(
                    f"सामाजिक कारणहरूमध्ये विवाहले गर्दा {format_nepali_number(marriage_children)} बालबालिकाहरू "
                    f"({format_nepali_percentage(marriage_percentage)}) ले विद्यालय छाडेको देखिन्छ। "
                    f"यसले बालविवाहको समस्या र बालिकाहरूको शिक्षामा बाधाको संकेत गर्छ।"
                )

            # Infrastructure and access barriers
            access_causes = ["FAR", "LIMITED_SPACE"]
            access_children = sum(
                municipality_data.get(cause, {}).get("population", 0)
                for cause in access_causes
            )
            access_percentage = (
                (access_children / total_children * 100) if total_children > 0 else 0
            )

            if access_percentage > 0:
                analysis_parts.append(
                    f"पहुँच र पूर्वाधारको समस्याले गर्दा {format_nepali_number(access_children)} बालबालिकाहरू "
                    f"({format_nepali_percentage(access_percentage)}) ले विद्यालय टाढा भएको र सीमित ठाउँको कारणले "
                    f"शिक्षाबाट वञ्चित भएका छन्।"
                )

            # Parental attitude analysis
            if "UNWILLING_PARENTS" in municipality_data:
                unwilling_children = municipality_data["UNWILLING_PARENTS"][
                    "population"
                ]
                unwilling_percentage = municipality_data["UNWILLING_PARENTS"][
                    "percentage"
                ]
                analysis_parts.append(
                    f"अभिभावकहरूको अनिच्छाका कारण {format_nepali_number(unwilling_children)} बालबालिकाहरू "
                    f"({format_nepali_percentage(unwilling_percentage)}) ले शिक्षाको अवसरबाट वञ्चित भएका छन्। "
                    f"यसले शिक्षाको महत्त्वबारे सामुदायिक चेतनाको आवश्यकतालाई देखाउँछ।"
                )

            # Positive completion analysis
            if "WANTED_STUDY_COMPLETED" in municipality_data:
                completed_children = municipality_data["WANTED_STUDY_COMPLETED"][
                    "population"
                ]
                completed_percentage = municipality_data["WANTED_STUDY_COMPLETED"][
                    "percentage"
                ]
                analysis_parts.append(
                    f"सकारात्मक पक्षमा, {format_nepali_number(completed_children)} बालबालिकाहरूले "
                    f"({format_nepali_percentage(completed_percentage)}) आफूले चाहेको अध्ययन पूरा गरेपछि विद्यालय छाडेका छन्। "
                    f"यसले उनीहरूको शैक्षिक लक्ष्य पूरा भएको संकेत गर्छ।"
                )

        # Ward-wise comparative analysis
        if ward_data and len(ward_data) > 1:
            # Find wards with highest and lowest dropout rates
            ward_dropout_rates = {}
            for ward_num, ward_info in ward_data.items():
                ward_dropout_rates[ward_num] = ward_info["total_population"]

            highest_ward = max(ward_dropout_rates.items(), key=lambda x: x[1])
            lowest_ward = min(ward_dropout_rates.items(), key=lambda x: x[1])

            if highest_ward[0] != lowest_ward[0]:
                analysis_parts.append(
                    f"वडागत विश्लेषणमा, वडा नं. {to_nepali_digits(highest_ward[0])} मा सबैभन्दा बढी "
                    f"{format_nepali_number(highest_ward[1])} बालबालिकाहरूले विद्यालय छाडेका छन् "
                    f"भने वडा नं. {to_nepali_digits(lowest_ward[0])} मा सबैभन्दा कम "
                    f"{format_nepali_number(lowest_ward[1])} बालबालिकाहरूले विद्यालय छाडेका छन्।"
                )

        # Educational implications
        analysis_parts.append(
            "विद्यालय छाड्ने बालबालिकाहरूको उच्च संख्याले मानव संशाधन विकास र साक्षरता दरमा नकारात्मक प्रभाव पारेको छ। "
            "यसले गरिबीको दुष्चक्र निरन्तरता दिन सक्छ।"
        )

        # Gender implications (especially for marriage-related dropouts)
        if (
            "MARRIAGE" in municipality_data
            and municipality_data["MARRIAGE"]["population"] > 0
        ):
            analysis_parts.append(
                "विवाहका कारण विद्यालय छाड्ने बालबालिकाहरूको संख्याले बालविवाहको समस्या र महिला शिक्षामा अवरोधको संकेत गर्छ। "
                "यसले लैङ्गिक समानतामा चुनौती खडा गरेको छ।"
            )

        # Economic burden analysis
        if economic_percentage > 30:  # If more than 30% dropout due to economic reasons
            analysis_parts.append(
                "आर्थिक कारणहरूले गर्दा धेरै बालबालिकाहरूले विद्यालय छाडेको तथ्यले गरिबी निवारण र शिक्षामा आर्थिक सहायताको आवश्यकतालाई देखाउँछ।"
            )

        # Future recommendations
        analysis_parts.append(
            "भविष्यमा विद्यालय छाड्ने दर घटाउन छात्रवृत्ति कार्यक्रम, विद्यालयहरूको पहुँच सुधार, सामुदायिक सचेतना अभियान र "
            "बालविवाह रोकथाम कार्यक्रमहरू आवश्यक छन्।"
        )

        # Quality education importance
        analysis_parts.append(
            "गुणस्तरीय शिक्षाको पहुँच र सबै बालबालिकाहरूको शैक्षिक अधिकार सुनिश्चित गर्नु दिगो विकासको आधार हो।"
        )

        return " ".join(analysis_parts)

    def generate_pie_chart(
        self, data, title="विद्यालय छाड्नुको कारण अनुसार बालबालिका वितरण"
    ):
        """Generate pie chart for school dropout data"""
        return self.chart_generator.generate_pie_chart_svg(
            data,
            include_title=False,
            title_nepali=title,
            title_english="Child Distribution by School Dropout Causes",
        )

    def process_for_pdf(self):
        """Process school dropout data for PDF generation including charts"""
        # Get raw data
        data = self.get_data()

        # Generate analysis text
        coherent_analysis = self.generate_analysis_text(data)

        # Generate and save charts
        charts = self.generate_and_save_charts(data)

        # Calculate total children
        total_count = data.get("total_children", 0)

        return {
            "municipality_data": data.get("municipality_data", {}),
            "ward_data": data.get("ward_data", {}),
            "total_children": total_count,
            "coherent_analysis": coherent_analysis,
            "pdf_charts": {"school_dropout": charts},
            "section_title": self.get_section_title(),
            "section_number": self.get_section_number(),
        }


class SchoolDropoutReportFormatter(BaseSocialReportFormatter):
    """Report formatter for school dropout social data"""

    def __init__(self, processor_data):
        super().__init__(processor_data)

    def format_for_html(self):
        """Format data for HTML template rendering"""
        return {
            "municipality_data": self.data["municipality_data"],
            "ward_data": self.data["ward_data"],
            "total_children": self.data["total_children"],
            "coherent_analysis": self.data["coherent_analysis"],
            "pdf_charts": self.data["pdf_charts"],
        }

    def format_for_api(self):
        """Format data for API response"""
        return {
            "section": self.data["section_number"],
            "title": self.data["section_title"],
            "summary": {
                "total_children": self.data["total_children"],
                "dropout_causes": len(self.data["municipality_data"]),
                "wards": len(self.data["ward_data"]),
            },
            "dropout_breakdown": self.data["municipality_data"],
            "ward_breakdown": self.data["ward_data"],
            "analysis": self.data["coherent_analysis"],
        }
