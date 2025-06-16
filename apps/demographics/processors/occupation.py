"""
Occupation Demographics Processor

Handles occupation demographic data processing, chart generation, and report formatting.
"""

import subprocess
from .base import BaseDemographicsProcessor, BaseReportFormatter
from ..models import WardWiseMajorOccupation
from ..utils.svg_chart_generator import DEFAULT_COLORS
from apps.reports.utils.nepali_numbers import format_nepali_number, format_nepali_percentage


class OccupationProcessor(BaseDemographicsProcessor):
    """Processor for occupation demographics"""
    
    def __init__(self):
        super().__init__()
        # Customize chart dimensions for occupation
        self.pie_chart_width = 900
        self.pie_chart_height = 450
        self.bar_chart_width = 1000
        self.bar_chart_height = 600
        self.chart_radius = 130
        # Set occupation-specific colors
        self.chart_generator.colors = {
            'ANIMAL_HUSBANDRY': '#8B4513',      # Brown
            'BUSINESS': '#FFD700',              # Gold
            'DAILY_WAGE': '#FF6347',            # Tomato
            'FOREIGN_EMPLOYMENT': '#4169E1',    # Royal Blue
            'GOVERNMENT_SERVICE': '#32CD32',    # Lime Green
            'HOUSEHOLD_WORK': '#FF69B4',        # Hot Pink
            'INDUSTRY': '#808080',              # Gray
            'NON_GOVERNMENT_SERVICE': '#20B2AA', # Light Sea Green
            'OTHER': '#DDA0DD',                 # Plum
            'OTHER_SELF_EMPLOYMENT': '#F0E68C', # Khaki
            'OTHER_UNEMPLOYMENT': '#DC143C',    # Crimson
            'STUDENT': '#00CED1'                # Dark Turquoise
        }
    
    def get_section_title(self):
        return "पेशाका आधारमा जनसंख्या विवरण"
    
    def get_section_number(self):
        return "३.८"
    
    def get_data(self):
        """Get occupation population data - both municipality-wide and ward-wise"""
        # Municipality-wide summary
        occupation_data = {}
        
        # Initialize all occupations
        occupation_types = {
            'ANIMAL_HUSBANDRY': 'पशुपालन',
            'BUSINESS': 'व्यापार/व्यवसाय',
            'DAILY_WAGE': 'दैनिक ज्यालादारी',
            'FOREIGN_EMPLOYMENT': 'वैदेशिक रोजगारी',
            'GOVERNMENT_SERVICE': 'सरकारी सेवा',
            'HOUSEHOLD_WORK': 'घरेलु काम',
            'INDUSTRY': 'उद्योग',
            'NON_GOVERNMENT_SERVICE': 'गैरसरकारी सेवा',
            'OTHER': 'अन्य',
            'OTHER_SELF_EMPLOYMENT': 'अन्य स्वरोजगार',
            'OTHER_UNEMPLOYMENT': 'अन्य बेरोजगार',
            'STUDENT': 'विद्यार्थी'
        }
        
        for occ_code, occ_name in occupation_types.items():
            occupation_data[occ_code] = {
                'population': 0,
                'percentage': 0.0,
                'name_nepali': occ_name,
            }

        # Ward-wise data for bar chart and detailed table
        ward_data = {}
        for ward_num in range(1, 8):  # Wards 1-7 based on sample data
            ward_data[ward_num] = {
                'ward_name': f"वडा नं. {ward_num}",
                'demographics': {}
            }
            # Initialize occupations for each ward
            for occ_code, occ_name in occupation_types.items():
                ward_data[ward_num]['demographics'][occ_code] = {
                    'population': 0,
                    'name_nepali': occ_name,
                }

        # Get actual data from database
        total_population = 0
        for occupation_obj in WardWiseMajorOccupation.objects.all():
            occupation = occupation_obj.occupation
            ward_num = occupation_obj.ward_number
            population = occupation_obj.population
            
            # Add to municipality-wide totals
            if occupation in occupation_data:
                occupation_data[occupation]['population'] += population
                total_population += population
            
            # Add to ward-wise data
            if ward_num in ward_data and occupation in ward_data[ward_num]['demographics']:
                ward_data[ward_num]['demographics'][occupation]['population'] = population

        # Calculate percentages for municipality-wide data
        if total_population > 0:
            for occupation, data in occupation_data.items():
                data['percentage'] = (data['population'] / total_population) * 100

        # Calculate ward totals and percentages
        for ward_num, ward_info in ward_data.items():
            ward_total = sum(demo['population'] for demo in ward_info['demographics'].values())
            ward_info['total_population'] = ward_total
            
            # Calculate percentages within each ward
            if ward_total > 0:
                for occupation, demo in ward_info['demographics'].items():
                    demo['percentage'] = (demo['population'] / ward_total) * 100 if ward_total > 0 else 0

        return {
            'municipality_data': occupation_data,
            'ward_data': ward_data,
            'total_population': total_population
        }
    
    def generate_report_content(self, data):
        """Generate occupation-specific report content"""
        formatter = self.OccupationReportFormatter()
        return formatter.generate_formal_report(data['municipality_data'], data['ward_data'], data['total_population'])
    
    def generate_chart_svg(self, data, chart_type="pie"):
        """Generate occupation chart SVG using SVGChartGenerator"""
        if chart_type == "pie":
            return self.chart_generator.generate_pie_chart_svg(
                data['municipality_data'], 
                include_title=False,
                title_nepali="पेशाका आधारमा जनसंख्या वितरण",
                title_english="Population Distribution by Occupation"
            )
        elif chart_type == "bar":
            return self.chart_generator.generate_bar_chart_svg(
                data['ward_data'], 
                include_title=False,
                title_nepali="वडा अनुसार पेशाका आधारमा जनसंख्या वितरण",
                title_english="Occupation Distribution by Ward"
            )
        return None

    def generate_and_save_charts(self, data):
        """Generate and save both pie and bar charts for occupation data"""
        charts_info = {}
        
        try:
            # Generate pie chart for municipality-wide data
            pie_svg = self.generate_chart_svg(data, chart_type="pie")
            if pie_svg:
                pie_path = self.static_charts_dir / "occupation_pie_chart.svg"
                with open(pie_path, 'w', encoding='utf-8') as f:
                    f.write(pie_svg)
                charts_info['pie_chart_svg'] = f"images/{pie_path.name}"
                
                # Try to convert to PNG
                try:
                    png_path = self.static_charts_dir / "occupation_pie_chart.png"
                    subprocess.run([
                        'inkscape', '--export-filename', str(png_path),
                        '--export-width', '900', '--export-height', '450',
                        str(pie_path)
                    ], check=True, timeout=30)
                    if png_path.exists():
                        charts_info['pie_chart_png'] = f"images/{png_path.name}"
                except:
                    pass  # Use SVG fallback
            
            # Generate bar chart for ward-wise data
            bar_svg = self.generate_chart_svg(data, chart_type="bar")
            if bar_svg:
                bar_path = self.static_charts_dir / "occupation_bar_chart.svg"
                with open(bar_path, 'w', encoding='utf-8') as f:
                    f.write(bar_svg)
                charts_info['bar_chart_svg'] = f"images/{bar_path.name}"
                
                # Try to convert to PNG
                try:
                    png_path = self.static_charts_dir / "occupation_bar_chart.png"
                    subprocess.run([
                        'inkscape', '--export-filename', str(png_path),
                        '--export-width', '1000', '--export-height', '600',
                        str(bar_path)
                    ], check=True, timeout=30)
                    if png_path.exists():
                        charts_info['bar_chart_png'] = f"images/{png_path.name}"
                except:
                    pass  # Use SVG fallback
                    
        except Exception as e:
            print(f"Error generating occupation charts: {e}")
        
        return charts_info

    class OccupationReportFormatter(BaseReportFormatter):
        """Occupation-specific report formatter"""
        
        def generate_formal_report(self, occupation_data, ward_data, total_population):
            """Generate occupation formal report content"""
            
            # Find major occupations
            major_occupations = []
            for occupation_type, data in occupation_data.items():
                if data['population'] > 0:
                    major_occupations.append((data['name_nepali'], data['population'], data['percentage']))
            
            major_occupations.sort(key=lambda x: x[1], reverse=True)
            
            # Build comprehensive analysis
            content = []
            
            # Introduction
            nepali_total = format_nepali_number(total_population)
            content.append(f"""{self.municipality_name}मा कुल {nepali_total} जनसंख्या विभिन्न पेशामा संलग्न रहेका छन् । पेशाका आधारमा जनसंख्याको वितरण गर्दा गाउँपालिकाको आर्थिक संरचना र रोजगारीको अवस्था देखिन्छ ।""")
            
            # Top occupations analysis
            if len(major_occupations) >= 3:
                top_three = major_occupations[:3]
                first_occ = top_three[0]
                second_occ = top_three[1]
                third_occ = top_three[2]
                
                first_pop = format_nepali_number(first_occ[1])
                first_pct = format_nepali_percentage(first_occ[2])
                second_pop = format_nepali_number(second_occ[1])
                second_pct = format_nepali_percentage(second_occ[2])
                third_pop = format_nepali_number(third_occ[1])
                third_pct = format_nepali_percentage(third_occ[2])
                
                content.append(f"""सबैभन्दा बढी {first_pop} जना अर्थात {first_pct} प्रतिशत जनसंख्या {first_occ[0]}मा संलग्न छन् भने दोस्रोमा {second_pop} जना अर्थात {second_pct} प्रतिशत {second_occ[0]}मा र तेस्रोमा {third_pop} जना अर्थात {third_pct} प्रतिशत {third_occ[0]}मा संलग्न रहेका छन् ।""")
            
            # Foreign employment analysis
            foreign_emp_data = next((occ for occ in major_occupations if 'वैदेशिक' in occ[0]), None)
            if foreign_emp_data:
                foreign_pop = format_nepali_number(foreign_emp_data[1])
                foreign_pct = format_nepali_percentage(foreign_emp_data[2])
                content.append(f"""वैदेशिक रोजगारीमा {foreign_pop} जना ({foreign_pct} प्रतिशत) संलग्न रहेको देखिन्छ जसले गाउँपालिकाको अर्थतन्त्रमा रेमिटेन्सको महत्वपूर्ण योगदान रहेको संकेत गर्छ ।""")
            
            # Agriculture and livestock
            agriculture_data = next((occ for occ in major_occupations if 'पशुपालन' in occ[0]), None)
            if agriculture_data:
                agri_pop = format_nepali_number(agriculture_data[1])
                agri_pct = format_nepali_percentage(agriculture_data[2])
                content.append(f"""कृषि तथा पशुपालनमा {agri_pop} जना ({agri_pct} प्रतिशत) संलग्न रहेका छन् जसले गाउँपालिकामा कृषिप्रधान अर्थतन्त्रको संकेत गर्छ ।""")
            
            # Service sector analysis
            govt_service = next((occ for occ in major_occupations if 'सरकारी सेवा' in occ[0]), None)
            non_govt_service = next((occ for occ in major_occupations if 'गैरसरकारी सेवा' in occ[0]), None)
            
            if govt_service or non_govt_service:
                service_text = "सेवा क्षेत्रमा "
                if govt_service:
                    govt_pop = format_nepali_number(govt_service[1])
                    govt_pct = format_nepali_percentage(govt_service[2])
                    service_text += f"सरकारी सेवामा {govt_pop} जना ({govt_pct} प्रतिशत) "
                if non_govt_service:
                    non_govt_pop = format_nepali_number(non_govt_service[1])
                    non_govt_pct = format_nepali_percentage(non_govt_service[2])
                    service_text += f"र गैरसरकारी सेवामा {non_govt_pop} जना ({non_govt_pct} प्रतिशत) "
                service_text += "संलग्न रहेका छन् ।"
                content.append(service_text)
            
            # Business and entrepreneurship
            business_data = next((occ for occ in major_occupations if 'व्यापार' in occ[0]), None)
            self_employment = next((occ for occ in major_occupations if 'स्वरोजगार' in occ[0]), None)
            
            if business_data or self_employment:
                business_text = "उद्यमशीलता क्षेत्रमा "
                if business_data:
                    business_pop = format_nepali_number(business_data[1])
                    business_pct = format_nepali_percentage(business_data[2])
                    business_text += f"व्यापार/व्यवसायमा {business_pop} जना ({business_pct} प्रतिशत) "
                if self_employment:
                    self_emp_pop = format_nepali_number(self_employment[1])
                    self_emp_pct = format_nepali_percentage(self_employment[2])
                    business_text += f"र स्वरोजगारमा {self_emp_pop} जना ({self_emp_pct} प्रतिशत) "
                business_text += "संलग्न रहेका छन् ।"
                content.append(business_text)
            
            # Daily wage labor analysis
            daily_wage = next((occ for occ in major_occupations if 'ज्यालादारी' in occ[0]), None)
            if daily_wage:
                wage_pop = format_nepali_number(daily_wage[1])
                wage_pct = format_nepali_percentage(daily_wage[2])
                content.append(f"""दैनिक ज्यालादारीमा {wage_pop} जना ({wage_pct} प्रतिशत) संलग्न रहेका छन् जसले श्रमिक वर्गको उपस्थिति देखाउँछ ।""")
            
            # Student population
            student_data = next((occ for occ in major_occupations if 'विद्यार्थी' in occ[0]), None)
            if student_data:
                student_pop = format_nepali_number(student_data[1])
                student_pct = format_nepali_percentage(student_data[2])
                content.append(f"""विद्यार्थीहरूको संख्या {student_pop} ({student_pct} प्रतिशत) रहेको छ जसले शिक्षाको क्षेत्रमा सकारात्मक संकेत दिन्छ ।""")
            
            # Industry and manufacturing
            industry_data = next((occ for occ in major_occupations if 'उद्योग' in occ[0]), None)
            if industry_data:
                industry_pop = format_nepali_number(industry_data[1])
                industry_pct = format_nepali_percentage(industry_data[2])
                content.append(f"""उद्योग क्षेत्रमा {industry_pop} जना ({industry_pct} प्रतिशत) संलग्न रहेका छन् जसले औद्योगिकीकरणको सम्भावना देखाउँछ ।""")
            
            # Economic policy implications
            content.append("""गाउँपालिकाको आर्थिक नीति निर्माणमा यी पेशागत तथ्याङ्कहरूले महत्वपूर्ण भूमिका खेल्छन् । कृषि, पशुपालन र वैदेशिक रोजगारीमा बढी जनसंख्या संलग्न भएकोले यी क्षेत्रहरूमा विशेष ध्यान दिनुपर्ने देखिन्छ ।""")
            
            # Employment and development strategy
            content.append("""स्थानीय रोजगारी सिर्जना, कौशल विकास र उद्यमशीलता प्रवर्धनका कार्यक्रमहरू सञ्चालन गरी विदेशमा गएका जनशक्तिलाई स्वदेशमै रोजगारीको अवसर प्रदान गर्ने नीति अपनाइएको छ ।""")
            
            # Ward-wise diversity
            content.append("""वडागत रूपमा पेशागत विविधता रहेको देखिन्छ । कुनै वडामा कृषि प्रधान भने कुनैमा उद्योग वा सेवा क्षेत्रको प्रधानता रहेको छ । यसले गाउँपालिकाको समग्र आर्थिक विकासमा सन्तुलित योगदान पुर्याएको छ ।""")
            
            # Future prospects and challenges
            content.append("""भविष्यमा प्रविधिमैत्री कृषि, उत्पादनमूलक उद्योग, पर्यटन र सेवा क्षेत्रको विकासमार्फत थप रोजगारीका अवसरहरू सिर्जना गर्ने योजना रहेको छ । युवाहरूलाई सीप विकास तालिम प्रदान गरी उत्पादनशील कार्यमा संलग्न गराउने कार्यक्रम सञ्चालन गरिएको छ ।""")
            
            # Social security and protection
            content.append("""सबै पेशामा संलग्न व्यक्तिहरूको सामाजिक सुरक्षा र श्रमिक अधिकारको संरक्षणमा गाउँपालिका प्रतिबद्ध छ । कार्यक्षेत्रको सुरक्षा, उचित पारिश्रमिक र सामाजिक सुरक्षाका कार्यक्रमहरू सञ्चालन गरिएको छ ।""")
            
            return ' '.join(content)
