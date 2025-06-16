"""
Public Transport Access Processor

Handles public transport accessibility data processing, chart generation, and report formatting.
"""

from django.db import models
from .base import BaseInfrastructureProcessor, BaseInfrastructureReportFormatter
from ..models import WardWiseTimeToPublicTransport, TimeDurationChoice
from apps.reports.utils.nepali_numbers import format_nepali_number, format_nepali_percentage


class PublicTransportProcessor(BaseInfrastructureProcessor):
    """Processor for public transport accessibility data"""
    
    def __init__(self):
        super().__init__()
        # Customize chart dimensions for public transport
        self.pie_chart_width = 800
        self.pie_chart_height = 450
        self.bar_chart_width = 1000
        self.bar_chart_height = 600
        self.chart_radius = 130
        # Set time duration-specific colors
        self.chart_generator.colors = {
            'UNDER_15_MIN': '#22C55E',      # Green - Excellent access
            'UNDER_30_MIN': '#84CC16',      # Lime - Good access
            'UNDER_1_HOUR': '#F59E0B',      # Amber - Moderate access
            '1_HOUR_OR_MORE': '#EF4444'     # Red - Poor access
        }
    
    def get_section_title(self):
        return "सार्वजनिक यातायातमा पहुँचको अवस्था"
    
    def get_section_number(self):
        return "७.१.६"
    
    def get_data(self):
        """Get public transport accessibility data - both municipality-wide and ward-wise"""
        # Municipality-wide summary by time duration
        time_duration_data = {}
        total_households = 0
        
        for time_choice in TimeDurationChoice.choices:
            time_code = time_choice[0]
            time_name = time_choice[1]
            
            time_households = WardWiseTimeToPublicTransport.objects.filter(
                time_duration=time_code
            ).aggregate(total=models.Sum('households'))['total'] or 0
            
            time_duration_data[time_code] = {
                'name_english': time_code,
                'name_nepali': time_name,
                'households': time_households,
                'percentage': 0  # Will be calculated below
            }
            total_households += time_households
        
        # Calculate percentages
        for time_code in time_duration_data:
            if total_households > 0:
                time_duration_data[time_code]['percentage'] = (
                    time_duration_data[time_code]['households'] / total_households * 100
                )
        
        # Ward-wise data
        ward_data = {}
        for ward_num in range(1, 8):  # Wards 1-7
            ward_households = WardWiseTimeToPublicTransport.objects.filter(
                ward_number=ward_num
            ).aggregate(total=models.Sum('households'))['total'] or 0
            
            if ward_households > 0:
                ward_data[ward_num] = {
                    'ward_number': ward_num,
                    'ward_name': f'वडा नं. {ward_num}',
                    'total_households': ward_households,
                    'time_durations': {}
                }
                
                # Time duration breakdown for this ward
                for time_choice in TimeDurationChoice.choices:
                    time_code = time_choice[0]
                    time_name = time_choice[1]
                    
                    time_households = WardWiseTimeToPublicTransport.objects.filter(
                        ward_number=ward_num, time_duration=time_code
                    ).aggregate(total=models.Sum('households'))['total'] or 0
                    
                    if time_households > 0:
                        ward_data[ward_num]['time_durations'][time_code] = {
                            'name_nepali': time_name,
                            'households': time_households,
                            'percentage': (time_households / ward_households * 100) if ward_households > 0 else 0
                        }
        
        return {
            'category_data': time_duration_data,
            'ward_data': ward_data,
            'total_households': total_households
        }
    
    def generate_analysis_text(self, data):
        """Generate coherent analysis text for public transport accessibility"""
        if not data or data['total_households'] == 0:
            return "सार्वजनिक यातायातमा पहुँचको तथ्याङ्क उपलब्ध छैन।"
        
        total_households = data['total_households']
        time_duration_data = data['category_data']
        ward_data = data['ward_data']
        
        analysis_parts = []
        
        # Overall summary
        analysis_parts.append(
            f"लुङ्ग्री गाउँपालिकामा कुल {format_nepali_number(total_households)} घरपरिवारको सार्वजनिक यातायातमा पहुँचको विश्लेषण गरिएको छ।"
        )
        
        # Accessibility analysis
        excellent_access = time_duration_data.get('UNDER_15_MIN', {}).get('households', 0)
        good_access = time_duration_data.get('UNDER_30_MIN', {}).get('households', 0)
        moderate_access = time_duration_data.get('UNDER_1_HOUR', {}).get('households', 0)
        poor_access = time_duration_data.get('1_HOUR_OR_MORE', {}).get('households', 0)
        
        # Calculate combined good access (under 30 minutes)
        combined_good_access = excellent_access + good_access
        good_access_percentage = (combined_good_access / total_households * 100) if total_households > 0 else 0
        
        # Detailed time duration analysis
        if excellent_access > 0:
            analysis_parts.append(
                f"१५ मिनेट भन्दा कममा सार्वजनिक यातायातमा पुग्न सक्ने घरपरिवारको संख्या {format_nepali_number(excellent_access)} "
                f"({format_nepali_percentage(time_duration_data['UNDER_15_MIN']['percentage'])}) छ, जुन उत्कृष्ट पहुँच मानिन्छ।"
            )
        
        if good_access > 0:
            analysis_parts.append(
                f"३० मिनेट भन्दा कममा पुग्न सक्ने घरपरिवारको संख्या {format_nepali_number(good_access)} "
                f"({format_nepali_percentage(time_duration_data['UNDER_30_MIN']['percentage'])}) छ।"
            )
        
        if moderate_access > 0:
            analysis_parts.append(
                f"१ घण्टा भन्दा कममा पुग्न सक्ने घरपरिवारको संख्या {format_nepali_number(moderate_access)} "
                f"({format_nepali_percentage(time_duration_data['UNDER_1_HOUR']['percentage'])}) छ, जुन मध्यम पहुँच मानिन्छ।"
            )
        
        if poor_access > 0:
            analysis_parts.append(
                f"१ घण्टा वा सो भन्दा बढी समय लाग्ने घरपरिवारको संख्या {format_nepali_number(poor_access)} "
                f"({format_nepali_percentage(time_duration_data['1_HOUR_OR_MORE']['percentage'])}) छ, जसलाई कमजोर पहुँच मानिन्छ।"
            )
        
        # Overall accessibility assessment
        analysis_parts.append(self.generate_accessibility_assessment(good_access_percentage))
        
        # Ward-wise analysis
        if ward_data:
            # Find ward with best and worst access
            best_ward_data = self.find_ward_with_best_access(ward_data)
            worst_ward_data = self.find_ward_with_worst_access(ward_data)
            
            if best_ward_data and worst_ward_data:
                analysis_parts.append(
                    f"वडाको आधारमा हेर्दा, वडा नं. {best_ward_data['ward_number']} मा सबैभन्दा राम्रो पहुँच "
                    f"({format_nepali_number(best_ward_data['good_access_households'])} घरपरिवार) छ "
                    f"भने वडा नं. {worst_ward_data['ward_number']} मा सबैभन्दा कमजोर पहुँच "
                    f"({format_nepali_number(worst_ward_data['poor_access_households'])} घरपरिवार) छ।"
                )
        
        # Recommendations
        if poor_access > 0:
            analysis_parts.append(
                f"कमजोर पहुँच भएका {format_nepali_number(poor_access)} घरपरिवारका लागि सार्वजनिक यातायात सेवा विस्तार गर्न आवश्यक छ।"
            )
        
        # Industry standard conclusion
        analysis_parts.append(
            "अन्तर्राष्ट्रिय मापदण्ड अनुसार ३०% घरपरिवारको सार्वजनिक यातायातमा १५ मिनेट भित्र पहुँच हुनुपर्छ र ८०% घरपरिवारको १ घण्टा भित्र पहुँच हुनुपर्छ।"
        )
        
        return " ".join(analysis_parts)
    
    def generate_accessibility_assessment(self, good_access_percentage):
        """Generate accessibility assessment based on industry standards"""
        if good_access_percentage >= 80:
            return f"कुल मिलाएर {format_nepali_percentage(good_access_percentage)} घरपरिवारको राम्रो पहुँच छ, जुन अन्तर्राष्ट्रिय मापदण्ड अनुसार उत्कृष्ट मानिन्छ।"
        elif good_access_percentage >= 60:
            return f"कुल मिलाएर {format_nepali_percentage(good_access_percentage)} घरपरिवारको राम्रो पहुँच छ, जुन सन्तोषजनक तर सुधार आवश्यक छ।"
        elif good_access_percentage >= 40:
            return f"कुल मिलाएर {format_nepali_percentage(good_access_percentage)} घरपरिवारको राम्रो पहुँच छ, जुन मध्यम तर महत्वपूर्ण सुधार आवश्यक छ।"
        else:
            return f"कुल मिलाएर केवल {format_nepali_percentage(good_access_percentage)} घरपरिवारको मात्र राम्रो पहुँच छ, जुन तत्काल सुधार आवश्यक छ।"
    
    def find_ward_with_best_access(self, ward_data):
        """Find ward with best public transport access"""
        best_ward = None
        best_score = -1
        
        for ward_num, ward_info in ward_data.items():
            # Calculate good access score (under 30 minutes)
            good_access = 0
            good_access += ward_info['time_durations'].get('UNDER_15_MIN', {}).get('households', 0)
            good_access += ward_info['time_durations'].get('UNDER_30_MIN', {}).get('households', 0)
            
            if good_access > best_score:
                best_score = good_access
                best_ward = {
                    'ward_number': ward_num,
                    'good_access_households': good_access,
                    'total_households': ward_info['total_households']
                }
        
        return best_ward
    
    def find_ward_with_worst_access(self, ward_data):
        """Find ward with worst public transport access"""
        worst_ward = None
        worst_score = float('inf')
        
        for ward_num, ward_info in ward_data.items():
            # Calculate poor access score (1 hour or more)
            poor_access = ward_info['time_durations'].get('1_HOUR_OR_MORE', {}).get('households', 0)
            
            if poor_access < worst_score:
                worst_score = poor_access
                worst_ward = {
                    'ward_number': ward_num,
                    'poor_access_households': poor_access,
                    'total_households': ward_info['total_households']
                }
        
        return worst_ward
    
    def generate_pie_chart(self, data, title="सार्वजनिक यातायातमा पहुँचको समय वितरण"):
        """Generate pie chart for time duration distribution"""
        if not data:
            return None
        
        # Prepare data for chart
        chart_data = []
        for time_code, time_info in data.items():
            if time_info['households'] > 0:
                chart_data.append({
                    'label': time_info['name_nepali'],
                    'value': time_info['households'],
                    'percentage': time_info['percentage']
                })
        
        if not chart_data:
            return None
        
        return self.chart_generator.generate_pie_chart(
            data=chart_data,
            title=title,
            width=self.pie_chart_width,
            height=self.pie_chart_height,
            radius=self.chart_radius
        )


class PublicTransportReportFormatter(BaseInfrastructureReportFormatter):
    """Report formatter for public transport accessibility data"""
    
    def __init__(self, processor_data):
        super().__init__(processor_data)
    
    def format_for_html(self):
        """Format data for HTML template rendering"""
        return {
            'time_duration_data': self.data['category_data'],
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
                'time_categories': len(self.data['category_data']),
                'wards': len(self.data['ward_data'])
            },
            'time_duration_breakdown': self.data['category_data'],
            'ward_breakdown': self.data['ward_data'],
            'analysis': self.data['coherent_analysis']
        }
