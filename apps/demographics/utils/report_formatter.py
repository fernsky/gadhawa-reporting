"""
Religion Report Formatter Utility

This module generates formal report content for religion demographics
in the style of official Nepali government reports.
"""

from django.utils.translation import gettext_lazy as _
from decimal import Decimal, ROUND_HALF_UP


class ReligionReportFormatter:
    """Generates formal report content for religion demographics"""
    
    def __init__(self):
        self.municipality_name = "लुङ्ग्री गाउँपालिका"
        
    def generate_formal_report(self, religion_data, ward_data):
        """Generate complete formal report content"""
        total_population = sum(data['population'] for data in religion_data.values())
        
        report_content = {
            'introduction': self._generate_introduction(),
            'constitutional_context': self._generate_constitutional_context(),
            'statistical_overview': self._generate_statistical_overview(religion_data, total_population),
            'ward_analysis': self._generate_ward_analysis(ward_data),
            'diversity_analysis': self._generate_diversity_analysis(religion_data, ward_data),
            'cultural_practices': self._generate_cultural_practices(),
            'recommendations': self._generate_recommendations(religion_data, ward_data),
            'conclusion': self._generate_conclusion(religion_data, total_population)
        }
        
        return report_content
    
    def _generate_introduction(self):
        """Generate introduction paragraph"""
        return """नेपालमा धार्मिक स्वतन्त्रता र विविधता रहेको छ । अझै विधिवत रुपमा नेपालको अन्तरिम संविधान २०६३, ले मिति २०६३ जेठ ४ मा पुर्नस्थापित संसदको ऐतिहासिक घोषणाले नेपाललाई एक धर्म निरपेक्ष राष्ट्रको रुपमा घोषणा गर्‍यो । त्यस्तै नेपालको संविधान, २०७२ को प्रस्तावनामा नेपाललाई एक बहुजातीय, बहुभाषिक, बहुधार्मिक, बहुसांस्कृतिक तथा भौगोलिक विविधतायुक्त विशेषतालाई आत्मसात् गरी विविधता बिचको एकता, सामाजिक सांस्कृतिक ऐक्यबद्धता, सहिष्णुता र सद्भावलाई संरक्षण एवं प्रवद्र्धन गर्दै, वर्गीय, जातीय, क्षेत्रीय, भाषिक, धार्मिक, लैङ्गिक विभेद र सबै प्रकारका जातीय छुवाछूतको अन्त्य गरी आर्थिक समानता, समृद्धि र सामाजिक न्याय सुनिश्चित गर्न समानुपातिक समावेशी र सहभागितामूलक सिद्धान्तका आधारमा समतामूलक समाजको निर्माण गर्ने संकल्प उल्लेख गरिएको छ । फलस्वरुप नेपालमा धार्मिक स्वतन्त्रता र सौहार्दता रहेको पाइन्छ ।"""
    
    def _generate_constitutional_context(self):
        """Generate constitutional and legal context"""
        return """संविधानले प्रत्याभूत गरेको धार्मिक स्वतन्त्रताको अधिकार अन्तर्गत प्रत्येक व्यक्तिले आफ्नो पसन्दको धर्म मान्न, अभ्यास गर्न र प्रचार गर्न पाउने अधिकार छ । यस गाउँपालिकामा पनि यही संवैधानिक व्यवस्था अनुरुप सबै नागरिकले आ-आफ्नो धर्म स्वतन्त्र रुपमा पालना गर्न सक्ने वातावरण रहेको छ । धार्मिक सहिष्णुता र आपसी सद्भावना यस क्षेत्रको विशेषता हो ।"""
    
    def _generate_statistical_overview(self, religion_data, total_population):
        """Generate statistical overview with key numbers"""
        # Find major religions
        major_religions = []
        for religion_type, data in religion_data.items():
            if data['population'] > 0:
                # Convert lazy translation objects to strings
                name_nepali = str(data['name_nepali']) if data['name_nepali'] else religion_type
                major_religions.append((name_nepali, data['population'], data['percentage']))
        
        major_religions.sort(key=lambda x: x[1], reverse=True)
        
        # Create overview text
        overview = f"""{self.municipality_name}मा रहेका कुल {total_population:,} जनसंख्या मध्ये """
        
        if len(major_religions) >= 1:
            first_religion = major_religions[0]
            overview += f"""{first_religion[1]:,} अर्थात {first_religion[2]:.2f} प्रतिशत जनसंख्याले {first_religion[0]} धर्म मान्दछन्"""
            
            if len(major_religions) >= 2:
                second_religion = major_religions[1]
                overview += f""" भने दोस्रोमा {second_religion[0]} धर्म मान्नेको संख्या {second_religion[1]:,} अर्थात {second_religion[2]:.2f} प्रतिशत रहेका छन् ।"""
                
                # Add third religion if significant
                if len(major_religions) >= 3 and major_religions[2][2] >= 2.0:
                    third_religion = major_religions[2]
                    overview += f""" त्यसैगरी {third_religion[1]:,} अर्थात {third_religion[2]:.2f} प्रतिशत {third_religion[0]} रहेका छन्"""
        
        overview += f""" गाउँपालिकामा धार्मिक विविधता रहेता पनि {'र '.join([str(r[0]) for r in major_religions[:2]])} धर्मावलम्बीहरूको प्रधानता रहेको तथ्याङ्कले देखाउँछ । नेपालमा सदियौंदेखि रहि आएको धार्मिक सहिष्णुता यस गाउँपालिकामा पनि कायमै रहेको देखिन्छ । वडागत रुपमा विभिन्न धर्मावलम्बीहरूको विस्तृत विवरण तालिकामा प्रस्तुत गरिएको छ ।"""
        
        return overview
    
    def _generate_ward_analysis(self, ward_data):
        """Generate ward-wise analysis"""
        if not ward_data:
            return "वडागत धार्मिक तथ्याङ्क उपलब्ध छैन ।"
        
        total_wards = len(ward_data)
        analysis = f"""गाउँपालिकाका {total_wards} वटा वडाहरूमा धार्मिक वितरणको अवस्था फरक फरक रहेको छ । """
        
        # Find most religiously diverse ward
        most_diverse_ward = max(ward_data.items(), key=lambda x: x[1]['religious_diversity_index'])
        least_diverse_ward = min(ward_data.items(), key=lambda x: x[1]['religious_diversity_index'])
        
        analysis += f"""वडा नं. {most_diverse_ward[0]} मा सबैभन्दा बढी धार्मिक विविधता (विविधता सूचकांक: {most_diverse_ward[1]['religious_diversity_index']:.3f}) रहेको छ भने वडा नं. {least_diverse_ward[0]} मा सबैभन्दा कम धार्मिक विविधता (विविधता सूचकांक: {least_diverse_ward[1]['religious_diversity_index']:.3f}) रहेको छ ।"""
        
        # Analyze ward-wise major religions
        hindu_dominant_wards = []
        buddhist_dominant_wards = []
        other_dominant_wards = []
        
        for ward_num, ward_info in ward_data.items():
            major_religion = ward_info.get('major_religion')
            if major_religion == 'HINDU':
                hindu_dominant_wards.append(ward_num)
            elif major_religion == 'BUDDHIST':
                buddhist_dominant_wards.append(ward_num)
            else:
                other_dominant_wards.append((ward_num, major_religion))
        
        if hindu_dominant_wards:
            analysis += f""" वडा नं. {', '.join(map(str, hindu_dominant_wards))} मा हिन्दू धर्मावलम्बीहरूको बाहुल्यता रहेको छ ।"""
        
        if buddhist_dominant_wards:
            analysis += f""" वडा नं. {', '.join(map(str, buddhist_dominant_wards))} मा बौद्ध धर्मावलम्बीहरूको बाहुल्यता रहेको छ ।"""
        
        return analysis
    
    def _generate_diversity_analysis(self, religion_data, ward_data):
        """Generate diversity analysis"""
        total_religions_present = sum(1 for data in religion_data.values() if data['population'] > 0)
        
        analysis = f"""गाउँपालिकामा कुल {total_religions_present} प्रकारका धर्मावलम्बीहरू बसोबास गर्छन् । """
        
        if ward_data:
            avg_diversity = sum(ward['religious_diversity_index'] for ward in ward_data.values()) / len(ward_data)
            analysis += f"""औसत धार्मिक विविधता सूचकांक {avg_diversity:.3f} रहेको छ जसले गाउँपालिकामा मध्यम स्तरको धार्मिक विविधता रहेको संकेत गर्छ ।"""
        
        # Add harmony statement
        analysis += """ विभिन्न धर्मका मानिसहरूबीच पारस्परिक सम्मान, सहयोग र सद्भावनापूर्ण सम्बन्ध कायम रहेको छ । धार्मिक उत्सवहरूमा सबै समुदायको सहभागिता रहने गर्छ जसले सामुदायिक एकताको परिचय दिन्छ ।"""
        
        return analysis
    
    def _generate_cultural_practices(self):
        """Generate cultural practices description"""
        return """यहाँ विभिन्न समुदायका मानिसहरूको बसोबास रहेको हुनाले उनीहरूका आ–आफ्नै चाडपर्वहरू छन् । पालिकाबासीले दशैँ, तिहार, तिज, ल्होसार, माघे संक्रान्ति, फागु पूर्णिमा, चण्डी पूर्णिमा, जनैपूर्णिमा, बुद्ध जयन्ती, क्रिसमस पर्व आदि मनाउने गर्दछन् । यी पर्वहरूले समुदायिक एकता र सांस्कृतिक विविधतालाई बलियो बनाउने काम गर्छ । धार्मिक स्थलहरूको संरक्षण र संवर्धनमा स्थानीय समुदायको सक्रिय सहभागिता रहेको छ ।"""
    
    def _generate_recommendations(self, religion_data, ward_data):
        """Generate recommendations for religious harmony"""
        recommendations = []
        
        recommendations.append("धार्मिक सद्भावना र सहिष्णुता प्रवर्धनका लागि नियमित अन्तर-धर्म संवाद कार्यक्रमहरू संचालन गर्ने ।")
        recommendations.append("सबै धर्मका पर्व र उत्सवहरूलाई सामुदायिक स्तरमा मनाउने परम्परालाई निरन्तरता दिने ।")
        recommendations.append("धार्मिक अल्पसंख्यकहरूका अधिकार र स्वतन्त्रताको सुनिश्चितता गर्ने ।")
        recommendations.append("धार्मिक स्थलहरूको संरक्षण र विकासका लागि आवश्यक बजेट विनियोजन गर्ने ।")
        recommendations.append("धार्मिक शिक्षा र मूल्य-मान्यताको संरक्षणका लागि उपयुक्त वातावरण सिर्जना गर्ने ।")
        
        return recommendations
    
    def _generate_conclusion(self, religion_data, total_population):
        """Generate conclusion"""
        total_religions = sum(1 for data in religion_data.values() if data['population'] > 0)
        
        return f"""{self.municipality_name} एक धार्मिक रुपमा विविधतापूर्ण क्षेत्र हो जहाँ {total_religions} प्रकारका धर्मावलम्बीहरूको सद्भावनापूर्ण सहअस्तित्व रहेको छ । कुल {total_population:,} जनसंख्या भएको यस गाउँपालिकामा धार्मिक स्वतन्त्रता, सहिष्णुता र आपसी सम्मानको वातावरण कायम छ । यो स्थिति नेपालको संवैधानिक मूल्य र आदर्शहरूको प्रतिबिम्बन हो । भविष्यमा पनि यही सद्भावनाको परम्परालाई निरन्तरता दिँदै धार्मिक विविधतालाई शक्तिका रुपमा उपयोग गर्दै समुदायिक विकास र समृद्धिमा योगदान पुर्याउन सकिनेछ ।"""
    
    def format_number(self, number):
        """Format numbers with Nepali comma separation"""
        return f"{number:,}"
    
    def calculate_percentage(self, part, total):
        """Calculate percentage with proper rounding"""
        if total == 0:
            return 0.0
        return round(Decimal(part) / Decimal(total) * 100, 2)
