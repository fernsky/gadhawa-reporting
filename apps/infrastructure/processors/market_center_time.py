"""
Market Center Time Infrastructure Processor

Handles market center time infrastructure data processing, chart generation, and report formatting.
"""

from django.db import models
from .base import BaseInfrastructureProcessor, BaseInfrastructureReportFormatter
from ..models import WardWiseTimeToMarketCenter, TimeDurationChoice
from apps.reports.utils.nepali_numbers import format_nepali_number, format_nepali_percentage


class MarketCenterTimeProcessor(BaseInfrastructureProcessor):
    """Processor for market center accessibility time data"""
    
    def __init__(self):
        super().__init__()
        # Customize chart dimensions for market center time
        self.pie_chart_width = 850
        self.pie_chart_height = 400
        self.chart_radius = 130
        # Set time duration-specific colors with professional gradient
        self.chart_generator.colors = {
            'UNDER_15_MIN': '#4CAF50',      # Green - Excellent access
            'UNDER_30_MIN': '#8BC34A',      # Light Green - Good access
            'UNDER_1_HOUR': '#FF9800',      # Orange - Moderate access
            '1_HOUR_OR_MORE': '#F44336'     # Red - Poor access
        }
    
    def get_section_title(self):
        return "बजार केन्द्रमा पुग्न लाग्ने समयको विवरण"
    
    def get_section_number(self):
        return "७.१.६"
    
    def get_data(self):
        """Get market center time data - both municipality-wide and ward-wise"""
        # Municipality-wide summary
        time_duration_data = {}
        total_households = 0
        
        for time_choice in TimeDurationChoice.choices:
            time_code = time_choice[0]
            time_name = time_choice[1]
            
            time_households = WardWiseTimeToMarketCenter.objects.filter(
                time_duration=time_code
            ).aggregate(total=models.Sum('households'))['total'] or 0
            
            if time_households > 0:  # Only include time durations with households
                time_duration_data[time_code] = {
                    'name_english': time_code,
                    'name_nepali': time_name,
                    'population': time_households,  # Using households as population for consistency
                    'percentage': 0  # Will be calculated below
                }
                total_households += time_households
        
        # Calculate percentages
        for time_code in time_duration_data:
            if total_households > 0:
                time_duration_data[time_code]['percentage'] = (
                    time_duration_data[time_code]['population'] / total_households * 100
                )
        
        # Ward-wise data
        ward_data = {}
        for ward_num in range(1, 8):  # Wards 1-7
            ward_households = WardWiseTimeToMarketCenter.objects.filter(
                ward_number=ward_num
            ).aggregate(total=models.Sum('households'))['total'] or 0
            
            if ward_households > 0:
                ward_data[ward_num] = {
                    'ward_number': ward_num,
                    'ward_name': f'वडा नं. {ward_num}',
                    'total_population': ward_households,  # Using households
                    'time_durations': {}
                }
                
                # Time duration breakdown for this ward
                for time_choice in TimeDurationChoice.choices:
                    time_code = time_choice[0]
                    time_name = time_choice[1]
                    
                    time_households_ward = WardWiseTimeToMarketCenter.objects.filter(
                        ward_number=ward_num, time_duration=time_code
                    ).aggregate(total=models.Sum('households'))['total'] or 0
                    
                    if time_households_ward > 0:
                        ward_data[ward_num]['time_durations'][time_code] = {
                            'name_nepali': time_name,
                            'population': time_households_ward,
                            'percentage': (time_households_ward / ward_households * 100) if ward_households > 0 else 0
                        }
        
        return {
            'municipality_data': time_duration_data,
            'ward_data': ward_data,
            'total_households': total_households
        }
    
    def generate_analysis_text(self, data):
        """Generate comprehensive analysis text for market center accessibility"""
        if not data or data['total_households'] == 0:
            return "बजार केन्द्रमा पुग्न लाग्ने समयको तथ्याङ्क उपलब्ध छैन।"
        
        total_households = data['total_households']
        municipality_data = data['municipality_data']
        ward_data = data['ward_data']
        
        analysis_parts = []
        
        # Overall summary
        analysis_parts.append(
            f"लुङ्ग्री गाउँपालिकामा कुल {format_nepali_number(total_households)} घरपरिवारको बजार केन्द्रमा पहुँचको अवस्था विश्लेषण गर्दा विभिन्न समयावधिमा बजार पुग्ने सुविधा उपलब्ध रहेको देखिन्छ।"
        )
        
        # Accessibility analysis
        if municipality_data:
            # Calculate accessibility levels
            excellent_access = municipality_data.get('UNDER_15_MIN', {}).get('population', 0)
            good_access = municipality_data.get('UNDER_30_MIN', {}).get('population', 0)
            moderate_access = municipality_data.get('UNDER_1_HOUR', {}).get('population', 0)
            poor_access = municipality_data.get('1_HOUR_OR_MORE', {}).get('population', 0)
            
            # Combined good accessibility (under 30 minutes)
            good_accessibility = excellent_access + good_access
            good_accessibility_percentage = (good_accessibility / total_households * 100) if total_households > 0 else 0
            
            # Find the most common time duration
            dominant_time = max(municipality_data.items(), key=lambda x: x[1]['population'])
            analysis_parts.append(
                f"समयावधिको आधारमा विश्लेषण गर्दा, {dominant_time[1]['name_nepali']} समयमा बजार पुग्ने घरपरिवारको संख्या सबैभन्दा बढी "
                f"{format_nepali_number(dominant_time[1]['population'])} "
                f"({format_nepali_percentage(dominant_time[1]['percentage'])}) रहेको छ।"
            )
            
            # Accessibility quality analysis
            if good_accessibility > 0:
                analysis_parts.append(
                    f"बजार पहुँचको गुणस्तरको दृष्टिकोणले हेर्दा, {format_nepali_number(good_accessibility)} घरपरिवार "
                    f"({format_nepali_percentage(good_accessibility_percentage)}) ले ३० मिनेट भित्रमा बजार केन्द्र पुग्न सक्छन् जुन राम्रो पहुँचको सूचक हो।"
                )
            
            # Distance and connectivity analysis
            if excellent_access > 0:
                excellent_percentage = (excellent_access / total_households * 100)
                analysis_parts.append(
                    f"विशेष गरी {format_nepali_number(excellent_access)} घरपरिवार "
                    f"({format_nepali_percentage(excellent_percentage)}) ले १५ मिनेट भित्रमा बजार पुग्न सक्ने उत्कृष्ट अवस्था छ।"
                )
            
            # Challenge analysis
            if poor_access > 0:
                poor_percentage = (poor_access / total_households * 100)
                analysis_parts.append(
                    f"तर, {format_nepali_number(poor_access)} घरपरिवार "
                    f"({format_nepali_percentage(poor_percentage)}) लाई बजार पुग्न एक घण्टा वा सो भन्दा बढी समय लाग्छ जसले यातायात पूर्वाधारमा सुधारको आवश्यकता देखाउँछ।"
                )
        
        # Ward-wise comparative analysis
        if ward_data and len(ward_data) > 1:
            # Find wards with best and worst market accessibility
            best_ward = None
            worst_ward = None
            best_accessibility = 0
            worst_accessibility = 100
            
            for ward_num, ward_info in ward_data.items():
                # Calculate good accessibility (under 30 minutes)
                excellent = ward_info['time_durations'].get('UNDER_15_MIN', {}).get('population', 0)
                good = ward_info['time_durations'].get('UNDER_30_MIN', {}).get('population', 0)
                good_access_ward = excellent + good
                accessibility_percentage = (good_access_ward / ward_info['total_population'] * 100) if ward_info['total_population'] > 0 else 0
                
                if accessibility_percentage > best_accessibility:
                    best_accessibility = accessibility_percentage
                    best_ward = ward_num
                
                if accessibility_percentage < worst_accessibility:
                    worst_accessibility = accessibility_percentage
                    worst_ward = ward_num
            
            if best_ward and worst_ward and best_ward != worst_ward:
                analysis_parts.append(
                    f"वडागत विश्लेषणमा, वडा नं. {best_ward} मा सबैभन्दा राम्रो बजार पहुँच "
                    f"({format_nepali_percentage(best_accessibility)} घरपरिवारले ३० मिनेट भित्रमा पहुँच) छ "
                    f"भने वडा नं. {worst_ward} मा केही सुधारको आवश्यकता "
                    f"({format_nepali_percentage(worst_accessibility)} घरपरिवारले मात्र ३० मिनेट भित्रमा पहुँच) देखिन्छ।"
                )
        
        # Economic implications
        if good_accessibility_percentage > 70:
            analysis_parts.append(
                "बजारमा राम्रो पहुँचले स्थानीय अर्थतन्त्रमा सकारात्मक प्रभाव पारेको छ । यसले कृषि उत्पादनको बिक्री, दैनिक आवश्यकताको खरिदारी र व्यापारिक गतिविधिमा सहजता प्रदान गरेको छ।"
            )
        else:
            analysis_parts.append(
                "बजार पहुँचमा सुधार भएमा स्थानीय अर्थतन्त्रको विकासमा महत्वपूर्ण योगदान पुग्ने अपेक्षा गर्न सकिन्छ।"
            )
        
        # Social and development impact
        analysis_parts.append(
            "बजार केन्द्रसँगको जोडाइले न केवल आर्थिक गतिविधि बल्कि शिक्षा, स्वास्थ्य र सामाजिक सेवाहरूमा पनि पहुँच सुधार गर्दछ।"
        )
        
        # Future development recommendations
        if poor_access > total_households * 0.2:  # If more than 20% have poor access
            analysis_parts.append(
                "भविष्यमा सडक पूर्वाधार विकास र सार्वजनिक यातायात सेवाको विस्तारले बजार पहुँचमा उल्लेखनीय सुधार ल्याउन सक्छ।"
            )
        
        return " ".join(analysis_parts)
    
    def generate_pie_chart(self, data, title="बजार केन्द्रमा पुग्न लाग्ने समयको आधारमा घरपरिवार वितरण"):
        """Generate pie chart for market center time distribution"""
        if not data or not data['municipality_data']:
            return None
        
        # Prepare data for chart in the format expected by SVGChartGenerator
        chart_data = {}
        for time_code, time_info in data['municipality_data'].items():
            if time_info['population'] > 0:
                chart_data[time_code] = {
                    'name_nepali': time_info['name_nepali'],
                    'population': time_info['population'],
                    'percentage': time_info['percentage']
                }
        
        if not chart_data:
            return None
        
        return self.chart_generator.generate_pie_chart_svg(
            demographic_data=chart_data,
            include_title=True,
            title_nepali=title,
            title_english="Household Distribution by Time to Market Center"
        )


class MarketCenterTimeReportFormatter(BaseInfrastructureReportFormatter):
    """Report formatter for market center time infrastructure data"""
    
    def __init__(self, processor_data):
        super().__init__(processor_data)
    
    def format_for_html(self):
        """Format data for HTML template rendering"""
        return {
            'municipality_data': self.data['municipality_data'],
            'ward_data': self.data['ward_data'],
            'total_households': self.data['total_households'],
            'coherent_analysis': self.data['coherent_analysis'],
            'pdf_charts': self.data['pdf_charts']
        }
    
    def format_for_api(self):
        """Format data for API response"""
        return {
            'section': self.data['section_number'],
            'title': self.data['section_title'],
            'summary': {
                'total_households': self.data['total_households'],
                'time_categories': len(self.data['municipality_data']),
                'wards': len(self.data['ward_data'])
            },
            'time_duration_breakdown': self.data['municipality_data'],
            'ward_breakdown': self.data['ward_data'],
            'analysis': self.data['coherent_analysis']
        }
