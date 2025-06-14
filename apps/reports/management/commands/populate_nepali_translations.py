"""
Management command to populate Nepali translations for report categories and sections
"""
from django.core.management.base import BaseCommand
from apps.reports.models import ReportCategory, ReportSection

class Command(BaseCommand):
    help = 'Populate Nepali translations for report categories and sections'

    def handle(self, *args, **options):
        self.stdout.write("🔄 Populating Nepali translations for categories and sections...")
        
        # Mapping of English category names to Nepali translations
        category_translations = {
            'Background': 'पृष्ठभूमि',
            'Objectives': 'उद्देश्यहरू', 
            'Legal and Policy Framework': 'कानूनी र नीतिगत ढाँचा',
            'Preparation Phases': 'तयारी चरणहरू',
            'Format, Tools and Procedure Preparation': 'ढाँचा, उपकरण र प्रक्रिया तयारी',
            'Preparation Workshop': 'तयारी कार्यशाला',
            'Facilitator and Volunteer Selection and Orientation': 'सहजकर्ता र स्वयंसेवक छनोट र अभिमुखीकरण',
            'Data Collection': 'डेटा संकलन',
            'Data Processing and Analysis': 'डेटा प्रशोधन र विश्लेषण',
            'Draft Report Preparation': 'मस्यौदा प्रतिवेदन तयारी',
            'Feedback Collection': 'प्रतिक्रिया संकलन',
            'Final Report Preparation': 'अन्तिम प्रतिवेदन तयारी',
            'Scope of Status Report': 'स्थिति प्रतिवेदनको दायरा',
            'Demographics': 'जनसांख्यिकी',
            'Economics': 'आर्थिक अवस्था',
            'Social': 'सामाजिक क्षेत्र',
            'Environment': 'वातावरण',
            'Infrastructure': 'पूर्वाधार',
            'Governance': 'सुशासन',
            'Introduction': 'परिचय',
            'Methodology': 'कार्यविधि',
            'Analysis': 'विश्लेषण',
            'Conclusion': 'निष्कर्ष',
            'Recommendations': 'सिफारिसहरू',
        }
        
        # Mapping of English section titles to Nepali translations
        section_translations = {
            'Background': 'पृष्ठभूमि',
            'Population Overview': 'जनसंख्या सिंहावलोकन',
            'Age Distribution': 'उमेर वितरण',
            'Gender Statistics': 'लिङ्गीय तथ्याङ्क',
            'Education Levels': 'शिक्षाको स्तर',
            'Economic Activities': 'आर्थिक गतिविधिहरू',
            'Agriculture': 'कृषि',
            'Industry': 'उद्योग',
            'Services': 'सेवा क्षेत्र',
            'Employment': 'रोजगारी',
            'Income Distribution': 'आय वितरण',
            'Poverty Statistics': 'गरिबी तथ्याङ्क',
            'Health Services': 'स्वास्थ्य सेवाहरू',
            'Education System': 'शिक्षा प्रणाली',
            'Social Welfare': 'सामाजिक कल्याण',
            'Cultural Heritage': 'सांस्कृतिक सम्पदा',
            'Environmental Status': 'वातावरणीय अवस्था',
            'Natural Resources': 'प्राकृतिक स्रोतहरू',
            'Biodiversity': 'जैविक विविधता',
            'Climate': 'जलवायु',
            'Pollution': 'प्रदूषण',
            'Transportation': 'यातायात',
            'Communication': 'सञ्चार',
            'Energy': 'ऊर्जा',
            'Water Supply': 'खानेपानी आपूर्ति',
            'Sanitation': 'सरसफाई',
            'Local Government': 'स्थानीय सरकार',
            'Administrative Structure': 'प्रशासनिक संरचना',
            'Budget and Finance': 'बजेट र वित्त',
            'Service Delivery': 'सेवा प्रवाह',
            'Citizen Participation': 'नागरिक सहभागिता',
        }
        
        # Update categories
        categories_updated = 0
        for category in ReportCategory.objects.all():
            if category.name in category_translations:
                nepali_name = category_translations[category.name]
                if not category.name_nepali or category.name_nepali != nepali_name:
                    category.name_nepali = nepali_name
                    category.save()
                    categories_updated += 1
                    self.stdout.write(f"✅ Updated category: {category.name} → {nepali_name}")
        
        # Update sections
        sections_updated = 0
        for section in ReportSection.objects.all():
            if section.title in section_translations:
                nepali_title = section_translations[section.title]
                if not section.title_nepali or section.title_nepali != nepali_title:
                    section.title_nepali = nepali_title
                    section.save()
                    sections_updated += 1
                    self.stdout.write(f"✅ Updated section: {section.title} → {nepali_title}")
        
        # Create sample categories if none exist
        if not ReportCategory.objects.exists():
            self.stdout.write("📝 Creating sample categories...")
            sample_categories = [
                ('Introduction', 'परिचय', 'गढवा गाउँपालिकाको सामान्य परिचय र यस प्रतिवेदनको उद्देश्य', 'fas fa-home'),
                ('Demographics', 'जनसांख्यिकी', 'जनसंख्या, उमेर, लिङ्ग र शैक्षिक तथ्याङ्कहरू', 'fas fa-users'),
                ('Economics', 'आर्थिक अवस्था', 'आर्थिक गतिविधि, कृषि, उद्योग र रोजगारीको अवस्था', 'fas fa-chart-line'),
                ('Social', 'सामाजिक क्षेत्र', 'स्वास्थ्य, शिक्षा र सामाजिक कल्याणका कार्यक्रमहरू', 'fas fa-heart'),
                ('Environment', 'वातावरण', 'प्राकृतिक स्रोत, जैविक विविधता र वातावरण संरक्षण', 'fas fa-leaf'),
                ('Infrastructure', 'पूर्वाधार', 'यातायात, सञ्चार, ऊर्जा र खानेपानीको अवस्था', 'fas fa-building'),
                ('Governance', 'सुशासन', 'स्थानीय शासन, प्रशासन र नागरिक सेवाको अवस्था', 'fas fa-gavel'),
            ]
            
            for i, (name_en, name_np, desc_np, icon) in enumerate(sample_categories, 1):
                category = ReportCategory.objects.create(
                    name=name_en,
                    name_nepali=name_np,
                    description=f"Information about {name_en}",
                    description_nepali=desc_np,
                    category_number=str(i),
                    order=i,
                    icon=icon,
                    is_active=True
                )
                categories_updated += 1
                self.stdout.write(f"✅ Created category: {name_en} → {name_np}")
        
        self.stdout.write(
            self.style.SUCCESS(
                f"\n🎉 Translation update completed!\n"
                f"📊 Categories updated: {categories_updated}\n"
                f"📝 Sections updated: {sections_updated}\n"
                f"\nNow the table of contents should display Nepali titles!"
            )
        )
