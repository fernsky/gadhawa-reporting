"""
Househead Demographics Processor

Handles househead demographic data processing, chart generation, and report formatting.
"""

import subprocess
from .base import BaseDemographicsProcessor, BaseReportFormatter
from ..models import WardWiseHouseheadGender, GenderChoice
from ..utils.svg_chart_generator import DEFAULT_COLORS
from apps.reports.utils.nepali_numbers import format_nepali_number, format_nepali_percentage


class HouseheadProcessor(BaseDemographicsProcessor):
    """Processor for househead demographics"""
    
    def __init__(self):
        super().__init__()
        # Customize chart dimensions for househead
        self.pie_chart_width = 800
        self.pie_chart_height = 450
        self.bar_chart_width = 800
        self.bar_chart_height = 500
        self.chart_radius = 130
        # Set househead-specific colors
        self.chart_generator.colors = {
            'MALE': '#1f77b4',      # Blue
            'FEMALE': '#ff7f0e',    # Orange
            'OTHER': '#2ca02c'      # Green
        }
    
    def get_section_title(self):
        return "घरमूलीको विवरण"
    
    def get_section_number(self):
        return "३.७"
    
    def get_data(self):
        """Get househead population data - both municipality-wide and ward-wise"""
        # Municipality-wide summary
        househead_data = {}
        
        # Initialize all genders
        for choice in GenderChoice.choices:
            househead_data[choice[0]] = {
                'population': 0,
                'percentage': 0.0,
                'name_nepali': choice[1],
            }

        # Ward-wise data for bar chart and detailed table
        ward_data = {}
        for ward_num in range(1, 10):  # Wards 1-9
            ward_data[ward_num] = {
                'ward_name': f"वडा नं. {ward_num}",
                'demographics': {}
            }
            # Initialize genders for each ward
            for choice in GenderChoice.choices:
                ward_data[ward_num]['demographics'][choice[0]] = {
                    'population': 0,
                    'name_nepali': choice[1],
                }

        # Get actual data from database
        total_population = 0
        for househead_obj in WardWiseHouseheadGender.objects.all():
            gender = househead_obj.gender
            ward_num = househead_obj.ward_number
            population = househead_obj.population
            
            # Add to municipality-wide totals
            if gender in househead_data:
                househead_data[gender]['population'] += population
                total_population += population
            
            # Add to ward-wise data
            if ward_num in ward_data and gender in ward_data[ward_num]['demographics']:
                ward_data[ward_num]['demographics'][gender]['population'] = population

        # Calculate percentages for municipality-wide data
        if total_population > 0:
            for gender, data in househead_data.items():
                data['percentage'] = (data['population'] / total_population) * 100

        # Calculate ward totals and percentages
        for ward_num, ward_info in ward_data.items():
            ward_total = sum(demo['population'] for demo in ward_info['demographics'].values())
            ward_info['total_population'] = ward_total
            
            # Calculate percentages within each ward
            if ward_total > 0:
                for gender, demo in ward_info['demographics'].items():
                    demo['percentage'] = (demo['population'] / ward_total) * 100 if ward_total > 0 else 0

        return {
            'municipality_data': househead_data,
            'ward_data': ward_data,
            'total_population': total_population
        }
    
    def generate_report_content(self, data):
        """Generate househead-specific report content"""
        formatter = self.HouseheadReportFormatter()
        return formatter.generate_formal_report(data['municipality_data'], data['ward_data'], data['total_population'])
    
    def generate_chart_svg(self, data, chart_type="bar"):
        """Generate househead chart SVG using SVGChartGenerator"""
        if chart_type == "pie":
            return self.chart_generator.generate_pie_chart_svg(
                data['municipality_data'], 
                include_title=False,
                title_nepali="घरमुखियाको लिङ्गको आधारमा घरपरिवार वितरण",
                title_english="Household Distribution by Head Gender"
            )
        elif chart_type == "bar":
            return self.chart_generator.generate_bar_chart_svg(
                data['ward_data'], 
                include_title=False,
                title_nepali="वडा अनुसार घरमुखियाको लिङ्गको वितरण",
                title_english="Head Gender Distribution by Ward"
            )
        return None

    def generate_and_save_charts(self, data):
        """Generate and save both pie and bar charts for househead data"""
        charts_info = {}
        
        try:
            # Generate pie chart for municipality-wide data
            pie_svg = self.generate_chart_svg(data, chart_type="pie")
            if pie_svg:
                pie_path = self.static_charts_dir / "househead_pie_chart.svg"
                with open(pie_path, 'w', encoding='utf-8') as f:
                    f.write(pie_svg)
                charts_info['pie_chart_svg'] = f"images/{pie_path.name}"
                
                # Try to convert to PNG
                try:
                    png_path = self.static_charts_dir / "househead_pie_chart.png"
                    subprocess.run([
                        'inkscape', '--export-filename', str(png_path),
                        '--export-width', '800', '--export-height', '500',
                        str(pie_path)
                    ], check=True, timeout=30)
                    if png_path.exists():
                        charts_info['pie_chart_png'] = f"images/{png_path.name}"
                except:
                    pass  # Use SVG fallback
            
            # Generate bar chart for ward-wise data
            bar_svg = self.generate_chart_svg(data, chart_type="bar")
            if bar_svg:
                bar_path = self.static_charts_dir / "househead_bar_chart.svg"
                with open(bar_path, 'w', encoding='utf-8') as f:
                    f.write(bar_svg)
                charts_info['bar_chart_svg'] = f"images/{bar_path.name}"
                
                # Try to convert to PNG
                try:
                    png_path = self.static_charts_dir / "househead_bar_chart.png"
                    subprocess.run([
                        'inkscape', '--export-filename', str(png_path),
                        '--export-width', '800', '--export-height', '500',
                        str(bar_path)
                    ], check=True, timeout=30)
                    if png_path.exists():
                        charts_info['bar_chart_png'] = f"images/{png_path.name}"
                except:
                    pass  # Use SVG fallback
                    
        except Exception as e:
            print(f"Error generating househead charts: {e}")
        
        return charts_info

    class HouseheadReportFormatter(BaseReportFormatter):
        """Househead-specific report formatter"""
        
        def generate_formal_report(self, househead_data, ward_data, total_population):
            """Generate househead formal report content"""
            
            # Find major genders
            major_genders = []
            for gender_type, data in househead_data.items():
                if data['population'] > 0:
                    major_genders.append((data['name_nepali'], data['population'], data['percentage']))
            
            major_genders.sort(key=lambda x: x[1], reverse=True)
            
            # Build coherent analysis
            content = []
            
            # Introduction
            nepali_total = format_nepali_number(total_population)
            content.append(f"""{self.municipality_name}मा कुल {nepali_total} घरपरिवारहरू छन् । घरमुखियाको लिङ्गको आधारमा यी घरपरिवारहरूको वितरण गर्दा रोचक तथ्यहरू देखिन्छन् ।""")
            
            # Major genders analysis
            if major_genders:
                main_gender = major_genders[0]
                main_percentage = format_nepali_percentage(main_gender[2])
                main_population = format_nepali_number(main_gender[1])
                
                content.append(f"""घरमुखियाको हकमा {main_gender[0]} मुखिया भएका घरपरिवारहरूको संख्या सबैभन्दा बढी छ जुन कुल घरपरिवारको {main_percentage} प्रतिशत ({main_population} घरपरिवार) हो ।""")
                
                if len(major_genders) > 1:
                    second_gender = major_genders[1]
                    second_percentage = format_nepali_percentage(second_gender[2])
                    second_population = format_nepali_number(second_gender[1])
                    
                    content.append(f"""{second_gender[0]} मुखिया भएका घरपरिवारहरूको संख्या {second_percentage} प्रतिशत ({second_population} घरपरिवार) रहेको छ ।""")
            
            # Ward-wise analysis
            content.append("""वडागत रूपमा हेर्दा घरमुखियाको लिङ्गीय वितरणमा केही भिन्नताहरू देखिन्छन् ।""")
            
            # Find ward with highest female head percentage
            highest_female_ward = None
            highest_female_percentage = 0
            for ward_num, ward_info in ward_data.items():
                if 'FEMALE' in ward_info['demographics']:
                    female_percentage = ward_info['demographics']['FEMALE']['percentage']
                    if female_percentage > highest_female_percentage:
                        highest_female_percentage = female_percentage
                        highest_female_ward = ward_num
            
            if highest_female_ward:
                ward_nepali = format_nepali_number(highest_female_ward)
                female_percentage_nepali = format_nepali_percentage(highest_female_percentage)
                content.append(f"""वडा नं. {ward_nepali} मा महिला घरमुखियाको प्रतिशत सबैभन्दा बढी {female_percentage_nepali} प्रतिशत रहेको छ जुन महिला सशक्तिकरणको सकारात्मक संकेत हो ।""")
            
            # Constitutional context
            content.append("""नेपालको संविधान २०७२ ले लिङ्गीय समानताको सिद्धान्त स्थापना गरेको छ । घरमुखियाको जिम्मेवारी पुरुष र महिला दुवैले समान रूपमा वहन गर्न सक्छन् । हालका वर्षहरूमा महिला घरमुखियाको संख्यामा वृद्धि भएको छ जुन सामाजिक परिवर्तनको सकारात्मक संकेत हो ।""")
            
            # Diversity analysis
            active_genders = len([d for d in househead_data.values() if d['population'] > 0])
            if active_genders > 1:
                content.append(f"""यस गाउँपालिकामा घरमुखियाको लिङ्गमा विविधता रहेको छ जसले लिङ्गीय समानताको दिशामा प्रगति भएको संकेत गर्छ । घरपरिवारको नेतृत्वमा विभिन्न लिङ्गका व्यक्तिहरूको सहभागिता सामाजिक न्यायको सूचक हो ।""")
            
            # Social development implications
            content.append("""घरमुखियाको भूमिका घरपरिवारको आर्थिक र सामाजिक निर्णयमा महत्वपूर्ण हुन्छ । लिङ्गीय समानताको सिद्धान्त अनुसार सबै घरमुखियाहरूलाई समान अधिकार र जिम्मेवारी प्राप्त हुनुपर्छ । गाउँपालिकाले घरमुखियाहरूको क्षमता विकास र सशक्तिकरणका लागि विभिन्न कार्यक्रमहरू सञ्चालन गर्दै आएको छ ।""")
            
            # Economic empowerment
            content.append("""महिला घरमुखियाहरूको बढ्दो संख्याले आर्थिक सशक्तिकरणमा महत्वपूर्ण भूमिका खेलेको छ । उनीहरूले घरपरिवारको आर्थिक व्यवस्थापन, बचत र लगानीमा प्रभावकारी नेतृत्व प्रदान गरेका छन् । यसले समुदायिक विकासमा सकारात्मक प्रभाव पारेको छ ।""")
            
            # Future implications
            content.append("""घरमुखियाको लिङ्गीय वितरणले स्थानीय विकास योजना र नीति निर्माणमा महत्वपूर्ण भूमिका खेल्छ । महिला घरमुखियाको संख्यामा वृद्धिले महिला सशक्तिकरण र लिङ्गीय न्यायमा सकारात्मक प्रभाव पार्छ । भविष्यमा थप समानुपातिक वितरणको अपेक्षा गर्न सकिन्छ जुन समुदायको समग्र विकासमा योगदान पुर्याउनेछ ।""")
            
            return ' '.join(content)

        def generate_harmony_conclusion(self):
            """Generate harmony conclusion text"""
            return """घरमुखियाको लिङ्गीय विविधताले समुदायमा लिङ्गीय समानताको वातावरण सिर्जना गरेको छ । यसले सामाजिक न्याय र समानताको दिशामा गाउँपालिका अगाडि बढेको संकेत गर्छ ।"""
