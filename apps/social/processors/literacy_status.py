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
            all_records = WardWiseLiteracyStatus.objects.all().order_by("ward_number", "literacy_type")

            if not all_records.exists():
                return self._empty_data_structure()

            municipality_data = defaultdict(int)
            ward_data = defaultdict(lambda: defaultdict(int))
            total_population = 0

            for record in all_records:
                municipality_data[record.literacy_type] += record.population
                ward_data[record.ward_number][record.literacy_type] += record.population
                total_population += record.population

            municipality_data = dict(municipality_data)
            ward_data = {ward: dict(literacy_types) for ward, literacy_types in ward_data.items()}

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
        """Generate analysis text for literacy status"""
        if not data or data["total_population"] == 0:
            return "साक्षरता अवस्थाको तथ्याङ्क उपलब्ध छैन।"

        municipality_data = data["municipality_data"]
        total_population = data["total_population"]

        # Calculate literacy rates
        literate_population = municipality_data.get("BOTH_READING_AND_WRITING", 0) + municipality_data.get("READING_ONLY", 0)
        literacy_rate = (literate_population / total_population * 100) if total_population > 0 else 0

        return f"""
        <div class="analysis-content">
            <h3>साक्षरता अवस्थाको विश्लेषण</h3>
            <p>लुङ्ग्री गाउँपालिकाको कुल जनसंख्या {total_population} मध्ये साक्षरता दर {literacy_rate:.1f}% रहेको छ।</p>
        </div>
        """
