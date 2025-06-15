"""
Create sample data for testing the PDF report system
"""

from django.core.management.base import BaseCommand
from apps.reports.models import ReportCategory, ReportSection


class Command(BaseCommand):
    help = "Create sample data for PDF report testing"

    def handle(self, *args, **options):
        self.stdout.write("Creating sample data...")

        # Create categories with Nepali content
        categories_data = [
            {
                "name": "Introduction",
                "name_nepali": "परिचय",
                "category_number": "1",
                "slug": "introduction",
                "order": 1,
                "is_active": True,
            },
            {
                "name": "Demographics",
                "name_nepali": "जनसांख्यिकी",
                "category_number": "2",
                "slug": "demographics",
                "order": 2,
                "is_active": True,
            },
            {
                "name": "Economic Status",
                "name_nepali": "आर्थिक स्थिति",
                "category_number": "3",
                "slug": "economic-status",
                "order": 3,
                "is_active": True,
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
                    "slug": f'background-{cat_data["slug"]}',
                    "content_nepali": f"""यस खण्डमा {cat_data["name_nepali"]}को पृष्ठभूमिको विस्तृत विवरण प्रस्तुत गरिएको छ।
                    
लुङ्ग्री गाउँपालिकाको {cat_data["name_nepali"]} सम्बन्धी मुख्य विशेषताहरू यहाँ उल्लेख गरिएको छ। यो विषयमा विभिन्न आयामहरूको समावेश छ।

मुख्य बिन्दुहरू:
• पहिलो मुख्य बिन्दु
• दोस्रो मुख्य बिन्दु  
• तेस्रो महत्वपूर्ण बिन्दु
• चौथो विशेष बिन्दु

यी सबै बिन्दुहरूले {cat_data["name_nepali"]}को समग्र चित्र प्रस्तुत गर्दछ।""",
                    "order": 1,
                    "is_published": True,
                },
                {
                    "title": "Current Status",
                    "title_nepali": "हालको अवस्था",
                    "section_number": f'{cat_data["category_number"]}.2',
                    "slug": f'current-status-{cat_data["slug"]}',
                    "content_nepali": f"""{cat_data["name_nepali"]}को हालको अवस्था निम्नलिखित छ:

वर्तमान स्थिति:
१. मुख्य उपलब्धिहरू
२. चुनौतीहरू र समस्याहरू
३. अवसरहरू र सम्भावनाहरू
४. सुधारका क्षेत्रहरू

विस्तृत विश्लेषण:
गाउँपालिकामा {cat_data["name_nepali"]}को क्षेत्रमा उल्लेखनीय प्रगति भएको छ। तर अझै धेरै काम गर्न बाँकी छ। यसका लागि समुदायिक सहभागिता र सरकारी प्रतिबद्धता आवश्यक छ।""",
                    "order": 2,
                    "is_published": True,
                },
                {
                    "title": "Future Plans",
                    "title_nepali": "भविष्यका योजनाहरू",
                    "section_number": f'{cat_data["category_number"]}.3',
                    "slug": f'future-plans-{cat_data["slug"]}',
                    "content_nepali": f"""{cat_data["name_nepali"]}का भविष्यका योजनाहरू:

अल्पकालीन योजनाहरू (१ वर्ष):
• तत्काल प्राथमिकताहरू
• आपातकालीन कार्यहरू
• द्रुत परिणाम ल्याउने गतिविधिहरू

मध्यकालीन योजनाहरू (३ वर्ष):
• संरचनागत सुधारहरू
• क्षमता विकास कार्यक्रमहरू
• दिगो विकासका आधारहरू

दीर्घकालीन योजनाहरू (५ वर्ष):
• दूरदर्शी लक्ष्यहरू
• ठूला पूर्वाधार परियोजनाहरू
• आर्थिक रूपान्तरण

यी योजनाहरूको सफल कार्यान्वयनले गाउँपालिकाको {cat_data["name_nepali"]}मा महत्वपूर्ण सुधार ल्याउनेछ।""",
                    "order": 3,
                    "is_published": True,
                },
            ]

            for sec_data in sections_data:
                section, created = ReportSection.objects.get_or_create(
                    category=category, slug=sec_data["slug"], defaults=sec_data
                )
                if created:
                    self.stdout.write(f"  Created section: {section.title}")

        self.stdout.write(self.style.SUCCESS("Sample data created successfully!"))
