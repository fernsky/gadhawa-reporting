"""
Literacy Status Processor for Social Domain

This processor handles Ward Wise Literacy Status data (५.१.१) providing:
- Municipality-wide and ward-wise literacy statistics
- Detailed Nepali language analysis
- Chart generation using base class functionality
- Literacy rate calculations and comparisons
"""

from collections import defaultdict
from typing import Dict, Any

from django.db import models
from apps.social.models import WardWiseLiteracyStatus, LiteracyTypeChoice
from .base import BaseSocialProcessor


class LiteracyStatusProcessor(BaseSocialProcessor):
    """Processor for Ward Wise Literacy Status"""

    def __init__(self):
        super().__init__()

    def get_section_title(self):
        """Return the section title for literacy status"""
        return "५.१.१ पाँच वर्षभन्दा माथि र १५ बर्षभन्दा माथिको साक्षरता विवरण"

    def get_section_number(self):
        """Return the section number for literacy status"""
        return "5.1.1"

    def get_data(self) -> Dict[str, Any]:
        """Get literacy status data aggregated by municipality and ward"""
        try:
            all_records = WardWiseLiteracyStatus.objects.all().order_by(
                "ward_number", "literacy_type"
            )

            if not all_records.exists():
                return self._empty_data_structure()

            # Municipality-wide summary
            municipality_data = {}
            total_population = 0

            for literacy_choice in LiteracyTypeChoice.choices:
                literacy_code = literacy_choice[0]
                literacy_name = literacy_choice[1]

                literacy_population = (
                    WardWiseLiteracyStatus.objects.filter(
                        literacy_type=literacy_code
                    ).aggregate(total=models.Sum("population"))["total"]
                    or 0
                )

                if literacy_population > 0:
                    municipality_data[literacy_code] = {
                        "name_english": literacy_code,
                        "name_nepali": literacy_name,
                        "population": literacy_population,
                        "percentage": 0,  # Will be calculated below
                    }
                    total_population += literacy_population

            # Calculate percentages
            for literacy_code in municipality_data:
                if total_population > 0:
                    municipality_data[literacy_code]["percentage"] = (
                        municipality_data[literacy_code]["population"]
                        / total_population
                        * 100
                    )

            # Ward-wise data
            ward_data = {}
            for ward_num in range(1, 8):  # Wards 1-7
                ward_population = (
                    WardWiseLiteracyStatus.objects.filter(
                        ward_number=ward_num
                    ).aggregate(total=models.Sum("population"))["total"]
                    or 0
                )

                if ward_population > 0:
                    ward_data[ward_num] = {
                        "ward_number": ward_num,
                        "ward_name": f"वडा नं. {ward_num}",
                        "total_population": ward_population,
                        "literacy_types": {},
                    }

                    # Literacy type breakdown for this ward
                    for literacy_choice in LiteracyTypeChoice.choices:
                        literacy_code = literacy_choice[0]
                        literacy_name = literacy_choice[1]

                        literacy_population_ward = (
                            WardWiseLiteracyStatus.objects.filter(
                                ward_number=ward_num, literacy_type=literacy_code
                            ).aggregate(total=models.Sum("population"))["total"]
                            or 0
                        )

                        if literacy_population_ward > 0:
                            ward_data[ward_num]["literacy_types"][literacy_code] = {
                                "name_nepali": literacy_name,
                                "population": literacy_population_ward,
                                "percentage": (
                                    (literacy_population_ward / ward_population * 100)
                                    if ward_population > 0
                                    else 0
                                ),
                            }

            return {
                "municipality_data": municipality_data,
                "ward_data": ward_data,
                "total_population": total_population,
                "literacy_types": [choice.value for choice in LiteracyTypeChoice],
            }

        except Exception as e:
            print(f"Error in get_data: {e}")
            return self._empty_data_structure()

    def _empty_data_structure(self) -> Dict[str, Any]:
        """Return empty data structure when no data available"""
        return {
            "municipality_data": {},
            "ward_data": {},
            "total_population": 0,
            "literacy_types": [choice.value for choice in LiteracyTypeChoice],
        }

    def generate_analysis_text(self, data: Dict[str, Any]) -> str:
        """Generate comprehensive analysis text for literacy status"""
        if not data or data["total_population"] == 0:
            return "साक्षरता अवस्थाको तथ्याङ्क उपलब्ध छैन।"

        municipality_data = data["municipality_data"]
        total_population = data["total_population"]

        # Import necessary formatting functions
        from apps.reports.utils.nepali_numbers import (
            format_nepali_number,
            format_nepali_percentage,
        )

        # Find major literacy categories
        major_literacy = []
        for literacy_type, data_item in municipality_data.items():
            if data_item["population"] > 0:
                major_literacy.append(
                    (
                        data_item["name_nepali"],
                        data_item["population"],
                        data_item["percentage"],
                    )
                )

        major_literacy.sort(key=lambda x: x[1], reverse=True)

        # Build comprehensive analysis
        content = []

        # Introduction
        nepali_total = format_nepali_number(total_population)
        content.append(
            f"""लुङ्ग्री गाउँपालिकामा कुल {nepali_total} जनसंख्याको साक्षरता अवस्थाको विश्लेषण गर्दा शैक्षिक विकासको स्थिति र भविष्यका चुनौतीहरू स्पष्ट देखिन्छन् । साक्षरताका विभिन्न स्तरमा जनसंख्याको वितरणले गाउँपालिकाको मानव संसाधन विकासको अवस्थालाई प्रतिबिम्बित गर्छ ।"""
        )

        # Calculate overall literacy rates
        full_literate = municipality_data.get("BOTH_READING_AND_WRITING", {}).get(
            "population", 0
        )
        reading_only = municipality_data.get("READING_ONLY", {}).get("population", 0)
        writing_only = municipality_data.get("WRITING_ONLY", {}).get("population", 0)
        illiterate = municipality_data.get("ILLITERATE", {}).get("population", 0)

        total_literate = full_literate + reading_only + writing_only
        literacy_rate = (
            (total_literate / total_population * 100) if total_population > 0 else 0
        )
        illiteracy_rate = (
            (illiterate / total_population * 100) if total_population > 0 else 0
        )

        # Overall literacy status
        if full_literate > 0:
            full_literate_nepali = format_nepali_number(full_literate)
            full_literate_pct = format_nepali_percentage(
                (full_literate / total_population * 100)
            )
            content.append(
                f"""सम्पूर्ण साक्षर (पढ्न र लेख्न दुवै सक्ने) जनसंख्या {full_literate_nepali} ({full_literate_pct} प्रतिशत) रहेको छ जसले गाउँपालिकामा गुणस्तरीय शिक्षाको पहुँचलाई जनाउँछ ।"""
            )

        # Reading only literacy
        if reading_only > 0:
            reading_only_nepali = format_nepali_number(reading_only)
            reading_only_pct = format_nepali_percentage(
                (reading_only / total_population * 100)
            )
            content.append(
                f"""केवल पढ्न सक्ने जनसंख्या {reading_only_nepali} ({reading_only_pct} प्रतिशत) रहेको छ जसले आंशिक साक्षरताको अवस्थालाई देखाउँछ र लेखन सीप विकासको आवश्यकतालाई संकेत गर्छ ।"""
            )

        # Illiteracy analysis
        if illiterate > 0:
            illiterate_nepali = format_nepali_number(illiterate)
            illiterate_pct = format_nepali_percentage(illiteracy_rate)
            content.append(
                f"""निरक्षर जनसंख्या {illiterate_nepali} ({illiterate_pct} प्रतिशत) रहेको छ जसले शिक्षाको पहुँच र गुणस्तरमा सुधारको तत्काल आवश्यकतालाई देखाउँछ ।"""
            )

        # Overall literacy achievement
        if literacy_rate > 0:
            literacy_rate_nepali = format_nepali_percentage(literacy_rate)
            content.append(
                f"""समग्र साक्षरता दर {literacy_rate_nepali} प्रतिशत रहेको छ जसले गाउँपालिकाको शैक्षिक उपलब्धिको स्थितिलाई प्रतिबिम्बित गर्छ ।"""
            )

        # Gender and age analysis implications
        content.append(
            """साक्षरताको यो अवस्थाले विभिन्न उमेर समूह र लिङ्गीय भिन्नताको प्रभावलाई संकेत गर्छ । पुराना पुस्ताहरूमा निरक्षरता बढी हुनु स्वाभाविक छ भने युवा पुस्तामा साक्षरता दरमा सुधार आएको देखिन्छ ।"""
        )

        # Educational infrastructure and access
        content.append(
            """साक्षरताको अवस्थाले गाउँपालिकामा शैक्षिक पूर्वाधार र शिक्षाको पहुँचको स्थितिलाई प्रतिबिम्बित गर्छ । स्कूल, शिक्षक र शैक्षिक सामग्रीको उपलब्धताले साक्षरता दरमा प्रत्यक्ष प्रभाव पारेको छ ।"""
        )

        # Socio-economic implications
        content.append(
            """साक्षरताको स्तरले सामाजिक र आर्थिक विकासमा गहिरो प्रभाव पार्छ । साक्षर जनसंख्याले बेहतर रोजगारीका अवसर, स्वास्थ्य सेवाको उपयोग र सामाजिक सहभागितामा वृद्धि ल्याउँछ ।"""
        )

        # Challenges and barriers
        if illiteracy_rate > 20:  # If illiteracy is significantly high
            content.append(
                """साक्षरता बृद्धिमा भौगोलिक बाधा, आर्थिक कमजोरी, सामाजिक मान्यता र शैक्षिक संस्थानको पहुँचमा कमीले मुख्य चुनौती खडा गरेको देखिन्छ । विशेष गरी दुर्गम क्षेत्र र सीमान्तकृत समुदायमा यो समस्या बढी गम्भीर छ ।"""
            )

        # Development strategies
        content.append(
            """साक्षरता बृद्धिका लागि औपचारिक शिक्षाको साथै वयस्क साक्षरता कार्यक्रम, सामुदायिक शिक्षा र वैकल्पिक शिक्षा प्रणालीको विकास गर्नुपर्छ । डिजिटल साक्षरता र कार्यात्मक साक्षरतामा विशेष जोड दिनुपर्छ ।"""
        )

        # Technology and modern education
        content.append(
            """आधुनिक प्रविधिको प्रयोगले साक्षरता कार्यक्रमहरूलाई प्रभावकारी बनाउन सकिन्छ । मोबाइल शिक्षा, अनलाइन सामग्री र डिजिटल माध्यमहरूले पहुँच बढाउन र गुणस्तर सुधार गर्न योगदान पुर्याउन सक्छ ।"""
        )

        # Community participation
        content.append(
            """समुदायिक सहभागितामार्फत साक्षरता कार्यक्रमहरूको प्रभावकारिता बढाउन सकिन्छ । स्थानीय भाषा र संस्कृतिलाई समेटेर शिक्षा प्रदान गर्दा सिकाइमा सुधार आउँछ ।"""
        )

        # Future prospects and goals
        content.append(
            """दिगो विकास लक्ष्य अनुसार सबै उमेरका मानिसहरूका लागि समावेशी र न्यायसंगत गुणस्तरीय शिक्षा सुनिश्चित गर्न साक्षरता दर उल्लेखनीय रूपमा बृद्धि गर्नुपर्छ । वडागत भिन्नतालाई कम गरी समान पहुँच सुनिश्चित गर्नुपर्छ ।"""
        )

        # Economic impact
        content.append(
            """साक्षरता बृद्धिले गाउँपालिकाको आर्थिक विकासमा प्रत्यक्ष योगदान पुर्याउँछ । शिक्षित जनशक्तिले उत्पादकता बृद्धि, नवाचार र उद्यमशीलताको विकासमा महत्वपूर्ण भूमिका खेल्छ ।"""
        )

        # Conclusion and call for action
        content.append(
            """समग्रमा साक्षरताको वर्तमान अवस्थालाई आधार मानेर व्यापक शैक्षिक सुधार कार्यक्रम सञ्चालन गर्नुपर्छ । सबै नागरिकको साक्षरता अधिकार सुनिश्चित गरी गाउँपालिकालाई ज्ञानमा आधारित समाजमा रूपान्तरण गर्नुपर्छ ।"""
        )

        return " ".join(content)
