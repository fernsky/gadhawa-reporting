"""
Create sample data for testing the PDF report system
"""

from django.core.management.base import BaseCommand
from apps.reports.models import ReportCategory, ReportSection, ReportFigure, ReportTable


class Command(BaseCommand):
    help = "Create sample data for PDF report testing"

    def handle(self, *args, **options):
        self.stdout.write("Creating sample data...")

        # Create categories
        categories_data = [
            {
                "name": "Introduction",
                "name_nepali": "परिचय",
                "category_number": "1",
                "slug": "introduction",
                "order": 1,
            },
            {
                "name": "Demographics",
                "name_nepali": "जनसांख्यिकी",
                "category_number": "2",
                "slug": "demographics",
                "order": 2,
            },
            {
                "name": "Economic Status",
                "name_nepali": "आर्थिक स्थिति",
                "category_number": "3",
                "slug": "economic-status",
                "order": 3,
            },
        ]

        for cat_data in categories_data:
            category, created = ReportCategory.objects.get_or_create(
                slug=cat_data["slug"], defaults=cat_data
            )
            if created:
                self.stdout.write(f"Created category: {category.name}")

            # Create sections for each category
            sections_data = [
                {
                    "title": "Background",
                    "title_nepali": "पृष्ठभूमि",
                    "section_number": f'{cat_data["category_number"]}.1',
                    "slug": "background",
                    "content_nepali": """यस खण्डमा लुङ्ग्री गाउँपालिकाको पृष्ठभूमिको विस्तृत विवरण प्रस्तुत गरिएको छ। गाउँपालिकाको भौगोलिक अवस्थिति, इतिहास, र विकासका मुख्य चरणहरूको बारेमा यहाँ उल्लेख गरिएको छ।
                    
लुङ्ग्री गाउँपालिका लुम्बिनी प्रदेशको नवलपरासी जिल्लामा अवस्थित छ। यो गाउँपालिका कुल ९ वटा वडाहरूमा विभाजित छ र यसको कुल क्षेत्रफल १२३.४५ वर्ग किलोमिटर छ।

मुख्य विशेषताहरू:
• भौगोलिक क्षेत्र: १२३.४५ वर्ग किमी
• कुल वडा संख्या: ९
• जनसंख्या घनत्व: २३४ व्यक्ति प्रति वर्ग किमी
• मुख्य व्यवसाय: कृषि र पशुपालन""",
                    "order": 1,
                },
                {
                    "title": "Objectives",
                    "title_nepali": "उद्देश्यहरू",
                    "section_number": f'{cat_data["category_number"]}.2',
                    "slug": "objectives",
                    "content_nepali": """यस प्रतिवेदनका मुख्य उद्देश्यहरू निम्नलिखित छन्:

१. लुङ्ग्री गाउँपालिकाको समग्र अवस्थाको वस्तुनिष्ठ मूल्याङ्कन गर्नु
२. विकासका क्षेत्रहरूको पहिचान र प्राथमिकीकरण गर्नु
३. स्थानीय सरकारको कार्यसम्पादनको समीक्षा गर्नु
४. भविष्यका नीति र कार्यक्रमहरूका लागि आधार तयार गर्नु

यी उद्देश्यहरू पूरा गर्नका लागि विभिन्न डेटा स्रोतहरूको प्रयोग गरिएको छ।""",
                    "order": 2,
                },
                {
                    "title": "Methodology",
                    "title_nepali": "कार्यविधि",
                    "section_number": f'{cat_data["category_number"]}.3',
                    "slug": "methodology",
                    "content_nepali": """यस अध्ययनमा प्रयोग गरिएको कार्यविधि निम्नलिखित छ:

प्राथमिक डेटा संकलन:
• घरधुरी सर्वेक्षण
• केन्द्रित समूह छलफल (FGD)
• मुख्य व्यक्तिहरूसँग अन्तर्वार्ता

द्वितीयक डेटा संकलन:
• सरकारी रेकर्डहरू
• पूर्व अध्ययनहरू
• स्थानीय निकायका प्रतिवेदनहरू

यी सबै जानकारीहरूलाई व्यवस्थित रूपमा विश्लेषण गरी यो प्रतिवेदन तयार गरिएको हो।""",
                    "order": 3,
                },
            ]

            for i, sec_data in enumerate(sections_data):
                section, created = ReportSection.objects.get_or_create(
                    category=category,
                    slug=sec_data["slug"],
                    defaults={**sec_data, "is_published": True},
                )
                if created:
                    self.stdout.write(f"  Created section: {section.title}")

        self.stdout.write(self.style.SUCCESS("Sample data created successfully!"))
