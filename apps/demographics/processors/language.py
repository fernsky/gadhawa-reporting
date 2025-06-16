"""
Language Demographics Processor

Handles mother tongue/language demographic data processing, chart generation, and report formatting.
"""

from .base import BaseDemographicsProcessor, BaseReportFormatter
from ..models import MunicipalityWideMotherTonguePopulation, LanguageTypeChoice
from ..utils.svg_chart_generator import LANGUAGE_COLORS
from apps.reports.utils.nepali_numbers import format_nepali_number, format_nepali_percentage


class LanguageProcessor(BaseDemographicsProcessor):
    """Processor for language demographics"""
    
    def __init__(self):
        super().__init__()
        # Customize chart dimensions for language
        self.pie_chart_width = 950
        self.pie_chart_height = 450
        self.chart_radius = 125
        # Set language-specific colors
        self.chart_generator.colors = LANGUAGE_COLORS
    
    def get_section_title(self):
        return "मातृभाषाको आधारमा जनसंख्या विवरण"
    
    def get_section_number(self):
        return "३.४"
    
    def get_data(self):
        """Get language population data"""
        language_data = {}

        # Initialize all languages
        for choice in LanguageTypeChoice.choices:
            language_data[choice[0]] = {
                'population': 0,
                'percentage': 0.0,
                'name_nepali': choice[1],
            }

        # Get actual data from database
        total_population = 0
        for language_obj in MunicipalityWideMotherTonguePopulation.objects.all():
            language = language_obj.language  # Correct attribute based on models.py
            if language in language_data:
                language_data[language]['population'] += language_obj.population
                total_population += language_obj.population

        # Calculate percentages
        if total_population > 0:
            for language, data in language_data.items():
                data['percentage'] = round((data['population'] / total_population) * 100, 2)

        return language_data
    
    def generate_report_content(self, data):
        """Generate language-specific report content"""
        formatter = self.LanguageReportFormatter()
        return formatter.generate_formal_report(data)
    
    def generate_chart_svg(self, data, chart_type="pie"):
        """Generate language chart SVG using SVGChartGenerator"""
        if chart_type == "pie":
            return self.chart_generator.generate_pie_chart_svg(
                data, 
                include_title=False,
                title_nepali="मातृभाषाको आधारमा जनसंख्या वितरण",
                title_english="Population Distribution by Mother Tongue"
            )
        elif chart_type == "bar":
            return self.chart_generator.generate_bar_chart_svg(
                data, 
                include_title=False,
                title_nepali="मातृभाषाको आधारमा जनसंख्या वितरण",
                title_english="Population Distribution by Mother Tongue"
            )
        return None

    class LanguageReportFormatter(BaseReportFormatter):
        """Language-specific report formatter"""
        
        def generate_formal_report(self, language_data):
            """Generate language formal report content"""
            total_population = sum(data['population'] for data in language_data.values())
            
            # Find major languages
            major_languages = []
            for language_type, data in language_data.items():
                if data['population'] > 0 and data['percentage'] >= 1.0:  # Lower threshold for rural areas
                    major_languages.append((data['name_nepali'], data['population'], data['percentage']))
            
            major_languages.sort(key=lambda x: x[1], reverse=True)
            
            # Build comprehensive analysis
            content = []
            
            # Introduction with national context
            nepali_total = format_nepali_number(total_population)
            content.append("""नेपाल एक बहु–जाति, बहु–भाषा र बहु–साँस्कृतिक विशेषता बोकेको राष्ट्र हो ।""")
            content.append(f"""{self.municipality_name}मा पनि भाषिक विविधता रहेको देखिन्छ । गाउँपालिकामा रहेका कुल {nepali_total} जनसंख्या मध्ये""")
            
            # Detailed language breakdown with statistics
            if major_languages:
                # Primary language
                primary_lang = major_languages[0]
                primary_pop = format_nepali_number(primary_lang[1])
                primary_pct = format_nepali_percentage(primary_lang[2])
                
                if len(major_languages) >= 4:
                    # Comprehensive breakdown for multiple languages
                    second_lang = major_languages[1]
                    third_lang = major_languages[2]
                    fourth_lang = major_languages[3]
                    
                    second_pop = format_nepali_number(second_lang[1])
                    second_pct = format_nepali_percentage(second_lang[2])
                    third_pop = format_nepali_number(third_lang[1])
                    third_pct = format_nepali_percentage(third_lang[2])
                    fourth_pop = format_nepali_number(fourth_lang[1])
                    fourth_pct = format_nepali_percentage(fourth_lang[2])
                    
                    content.append(f"""सबैभन्दा बढी {primary_pop} अर्थात {primary_pct} प्रतिशतले {primary_lang[0]} भाषा बोल्छन् भने {second_pop} अर्थात {second_pct} प्रतिशतले {second_lang[0]} भाषा, {third_pop} अर्थात {third_pct} प्रतिशतले {third_lang[0]} भाषा, {fourth_pop} अर्थात {fourth_pct} प्रतिशतले {fourth_lang[0]} भाषा र बाँकी अन्य नगण्य संख्याले अन्य भाषाहरू बोल्छन् ।""")
                else:
                    # Simple breakdown for fewer languages
                    content.append(f"""{primary_lang[0]} मातृभाषी समुदायको संख्या सबैभन्दा बढी छ जसको संख्या {primary_pop} ({primary_pct}) रहेको छ ।""")
                    if len(major_languages) > 1:
                        other_langs = []
                        for lang in major_languages[1:]:
                            lang_pop = format_nepali_number(lang[1])
                            lang_pct = format_nepali_percentage(lang[2])
                            other_langs.append(f"""{lang[0]} {lang_pop} ({lang_pct})""")
                        content.append(f"""त्यसैगरी {', '.join(other_langs)} जनसंख्या रहेको छ ।""")
            
            # Constitutional framework
            content.append("""संविधानको धारा ३२ मा भाषा तथा संस्कृतिको हकलाई मौलिक हकको रुपमा स्थापित गरेको र धारा ३१ को शिक्षासम्बन्धी हकको उपधारा ५ बमोजिम "नेपालमा बसोबास गर्ने प्रत्येक नेपाली समुदायलाई कानुन बमोजिम आफ्नो मातृभाषामा शिक्षा पाउने र त्यसका लागि विद्यालय तथा शैक्षिक संस्था खोल्ने र संचालन गर्ने हक हुनेछ ।" भनी स्पष्ट किटान गरेको छ ।""")
            
            # Local initiatives and provisions
            content.append("""आफ्नो मातृभाषामा पढ्न चाहने विद्यार्थीहरूलाई गाउँपालिकाले विशेष व्यवस्था गर्न सक्ने प्रावधान रहेको छ ।""")
            
            # Indigenous communities section
            content.append(self._generate_indigenous_analysis(language_data, total_population))
            
            # Marginalized communities section
            content.append(self._generate_marginalized_analysis(language_data, total_population))
            
            # Language preservation and development
            content.append("""स्थानीय तहले सबै मातृभाषाहरूको संरक्षण र सम्वर्धनमा विशेष ध्यान दिएको छ । शिक्षाका क्षेत्रमा मातृभाषामा शिक्षा प्रदान गर्ने व्यवस्था मिलाइएको छ । सांस्कृतिक कार्यक्रमहरूमा सबै भाषाहरूको प्रयोग र प्रवर्धनलाई प्रोत्साहन गरिएको छ ।""")
            
            # Future prospects
            content.append("""भाषिक विविधताले गाउँपालिकाको सांस्कृतिक सम्पदालाई समृद्ध बनाएको छ । सबै मातृभाषी समुदायहरूको भाषिक अधिकारको संरक्षण र संवर्धनमा गाउँपालिका प्रतिबद्ध छ ।""")
            
            return ' '.join(content)
        
        def _generate_indigenous_analysis(self, language_data, total_population):
            """Generate analysis for indigenous communities"""
            content = []
            
            content.append("""<strong>(क) आदिवासी</strong>""")
            content.append("""आदिवासी/जनजाति उत्थान राष्ट्रिय प्रतिष्ठान ऐन, २०५८ अनुसार आदिवासी जनजाति भन्नाले आफ्नो मातृभाषा र परम्परागत रीतिरिवाज, छुट्टै साँस्कृतिक पहिचान, छुट्टै सामाजिक संरचना र लिखित वा अलिखित इतिहास भएका जाति वा समुदायलाई बुझिन्छ ।""")
            
            # Calculate indigenous population
            indigenous_languages = ['MAGAR', 'GURUNG', 'TAMANG', 'NEWAR', 'RAI', 'LIMBU', 'SHERPA']
            indigenous_total = 0
            indigenous_breakdown = []
            
            total_pop_nepali = format_nepali_number(total_population)
            
            for lang_code in indigenous_languages:
                if lang_code in language_data and language_data[lang_code]['population'] > 0:
                    pop = language_data[lang_code]['population']
                    pct = language_data[lang_code]['percentage']
                    name = language_data[lang_code]['name_nepali']
                    indigenous_total += pop
                    
                    pop_nepali = format_nepali_number(pop)
                    pct_nepali = format_nepali_percentage(pct)
                    indigenous_breakdown.append(f"""{pct_nepali} प्रतिशत ({pop_nepali} जना) {name}""")
            
            if indigenous_breakdown:
                indigenous_total_pct = (indigenous_total / total_population * 100) if total_population > 0 else 0
                indigenous_total_nepali = format_nepali_number(indigenous_total)
                indigenous_total_pct_nepali = format_nepali_percentage(indigenous_total_pct)
                
                content.append(f"""यस गाउँपालिकाको कुल जनसंख्या {total_pop_nepali} मध्ये {indigenous_total_nepali} जना अर्थात {indigenous_total_pct_nepali} प्रतिशत आदिवासी समुदाय बसोबास गर्दछन् ।""")
                content.append(f"""यसैगरी गाउँपालिकामा {', '.join(indigenous_breakdown[:2])} समुदायका व्यक्तिहरू रहेका छन् ।""")
            
            content.append("""यी समुदायद्वारा गाउँपालिकाको मौलिक संस्कृतिलाई जीवन्त राख्न सहयोग पुगेको छ । गाउँपालिकाको विकासको लागि यो समुदायलाई अहिलेको अवस्थाबाट माथि उठाउन क्षमता विकास, सशक्तिकरण जस्ता विशेष कार्यक्रमहरू सञ्चालन गर्नुपर्ने देखिन्छ ।""")
            
            return ' '.join(content)
        
        def _generate_marginalized_analysis(self, language_data, total_population):
            """Generate analysis for marginalized communities"""
            content = []
            
            content.append("""<strong>(ख) उत्पीडित तथा सीमान्तकृत समुदाय</strong>""")
            content.append("""नेपालको संविधानको भाग ३४ अन्तर्गत धारा ३०६ को (ड) मा सीमान्तकृत समुदाय भन्नाले राजनीतिक, आर्थिक र सामाजिक रूपले पछाडि पारिएका विभेद र उत्पीडन तथा भौगोलिक विकटताको कारणले सेवा सुविधाको उपभोग गर्न नसकेका वा त्यसबाट वञ्चित रहेका संघीय कानून बमोजिमको मानव विकासको स्तर भन्दा न्यून स्थितिमा रहेका समुदाय सम्झनु पर्दछ भनी उल्लेख गरेको छ ।""")
            
            content.append("""सामाजिक विभेदका रूपमा छुवाछुत जस्तो अमानवीय भेदभाव भोगिरहेको यो समुदायले राजनैतिक, आर्थिक र सामाजिक क्षेत्रमा समेत उपेक्षाको अनुभूति गर्नु परेको छ । परम्परागत सिपको धनी यो समुदायले आफ्नो सिपलाई आर्थिक विपन्नता र सामाजिक उपेक्षाका कारण पनि अघि बढाउन नसकेको पाइन्छ ।""")
            
            content.append("""निजामती सेवा र गैरसरकारी सेवामा पनि यो समुदायको उपस्थिति अत्यन्तै न्यून छ । त्यसै गरी राजनीतिक क्षेत्रमा २०४६ साल यता यो समुदायले आफ्ना सामुदायिक संगठनहरू समेत निर्माण गरेको पाइन्छ । राजनीतिक नेतृत्वमा भने सीमित व्यक्तिहरूले मात्र यस समुदायको प्रतिनिधित्व गरिरहेका छन् ।""")
            
            content.append("""यस समुदायका अधिकांश व्यक्तिहरू अदक्ष र अर्धदक्ष जनशक्तिकै रूपमा ज्याला, मजदुरी गरेर जीवनयापन गरिरहेको पाइन्छ । यस गाउँपालिकाको विकासका लागि यो समुदायलाई अहिलेको अवस्थाबाट माथि उठाउन विशेष अभियानको थालनी गर्नुपर्ने अवस्था देखिन्छ ।""")
            
            return ' '.join(content)
