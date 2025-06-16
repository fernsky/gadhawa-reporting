"""
Religion Demographics Views for Lungri Rural Municipality

This module provides views for religion-based population analysis including:
- Ward-wise religion distribution
- Religion population summaries
- Dynamic chart generation
- Formal report content generation
"""

from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum, Count, Q
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _

from ..models import WardWiseReligionPopulation, ReligionTypeChoice
from ..utils.chart_generator import ReligionChartGenerator
from ..utils.report_formatter import ReligionReportFormatter


class ReligionDemographicsView(TemplateView):
    """Main view for religion demographics analysis"""
    
    template_name = 'demographics/religion/religion_analysis.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get religion population data
        religion_data = self.get_religion_population_data()
        ward_data = self.get_ward_wise_religion_data()
        
        # Generate charts
        chart_generator = ReligionChartGenerator()
        charts = {
            'overall_pie_chart': chart_generator.generate_overall_pie_chart(religion_data),
            'ward_comparison_bar': chart_generator.generate_ward_comparison_bar(ward_data),
            'religion_trend_chart': chart_generator.generate_religion_trend_chart(religion_data),
        }
        
        # Generate formal report content
        report_formatter = ReligionReportFormatter()
        report_content = report_formatter.generate_formal_report(religion_data, ward_data)
        
        context.update({
            'religion_data': religion_data,
            'ward_data': ward_data,
            'charts': charts,
            'report_content': report_content,
            'total_population': sum(data['population'] for data in religion_data.values()),
            'total_religions': len([r for r in religion_data.values() if r['population'] > 0]),
            'major_religions': self.get_major_religions(religion_data),
            'ward_summary': self.get_ward_summary(ward_data),
        })
        
        return context
    
    def get_religion_population_data(self):
        """Get overall religion population data"""
        religion_data = {}
        
        # Initialize all religions
        for choice in ReligionTypeChoice.choices:
            religion_data[choice[0]] = {
                'code': choice[0],
                'name_nepali': choice[1],
                'population': 0,
                'percentage': 0.0,
                'wards_present': 0
            }
        
        # Get actual data from database
        queryset = WardWiseReligionPopulation.objects.values('religion_type').annotate(
            total_population=Sum('population'),
            ward_count=Count('ward_number', distinct=True)
        )
        
        total_population = sum(item['total_population'] for item in queryset)
        
        for item in queryset:
            religion_type = item['religion_type']
            if religion_type in religion_data:
                religion_data[religion_type]['population'] = item['total_population']
                religion_data[religion_type]['wards_present'] = item['ward_count']
                if total_population > 0:
                    religion_data[religion_type]['percentage'] = (
                        item['total_population'] / total_population * 100
                    )
        
        return religion_data
    
    def get_ward_wise_religion_data(self):
        """Get ward-wise religion distribution"""
        ward_data = {}
        
        # Get all ward religion data
        queryset = WardWiseReligionPopulation.objects.select_related().order_by(
            'ward_number', 'religion_type'
        )
        
        for item in queryset:
            ward_num = item.ward_number
            if ward_num not in ward_data:
                ward_data[ward_num] = {
                    'ward_number': ward_num,
                    'total_population': 0,
                    'religions': {},
                    'major_religion': None,
                    'religious_diversity_index': 0.0
                }
            
            ward_data[ward_num]['religions'][item.religion_type] = {
                'population': item.population,
                'percentage': 0.0,
                'name_nepali': item.get_religion_type_display()
            }
            ward_data[ward_num]['total_population'] += item.population
        
        # Calculate percentages and find major religion
        for ward_num, data in ward_data.items():
            total = data['total_population']
            if total > 0:
                max_population = 0
                major_religion = None
                
                for religion_type, religion_info in data['religions'].items():
                    percentage = religion_info['population'] / total * 100
                    religion_info['percentage'] = percentage
                    
                    if religion_info['population'] > max_population:
                        max_population = religion_info['population']
                        major_religion = religion_type
                
                data['major_religion'] = major_religion
                data['religious_diversity_index'] = self.calculate_diversity_index(
                    data['religions'], total
                )
        
        return ward_data
    
    def calculate_diversity_index(self, religions, total_population):
        """Calculate religious diversity index (Shannon diversity index)"""
        if total_population == 0:
            return 0.0
        
        diversity_index = 0.0
        for religion_info in religions.values():
            if religion_info['population'] > 0:
                proportion = religion_info['population'] / total_population
                diversity_index -= proportion * (proportion ** 0.5)  # Simplified Shannon index
        
        return round(diversity_index, 3)
    
    def get_major_religions(self, religion_data):
        """Get major religions (above 5% threshold)"""
        major_religions = []
        for religion_type, data in religion_data.items():
            if data['percentage'] >= 5.0:  # 5% threshold
                major_religions.append({
                    'type': religion_type,
                    'name_nepali': data['name_nepali'],
                    'population': data['population'],
                    'percentage': data['percentage']
                })
        
        return sorted(major_religions, key=lambda x: x['percentage'], reverse=True)
    
    def get_ward_summary(self, ward_data):
        """Get summary statistics for wards"""
        if not ward_data:
            return {}
        
        total_wards = len(ward_data)
        avg_diversity = sum(data['religious_diversity_index'] for data in ward_data.values()) / total_wards
        
        # Find most and least diverse wards
        most_diverse = max(ward_data.items(), key=lambda x: x[1]['religious_diversity_index'])
        least_diverse = min(ward_data.items(), key=lambda x: x[1]['religious_diversity_index'])
        
        return {
            'total_wards': total_wards,
            'average_diversity_index': round(avg_diversity, 3),
            'most_diverse_ward': {
                'number': most_diverse[0],
                'diversity_index': most_diverse[1]['religious_diversity_index']
            },
            'least_diverse_ward': {
                'number': least_diverse[0],
                'diversity_index': least_diverse[1]['religious_diversity_index']
            }
        }


class ReligionDataAPIView(TemplateView):
    """API view for religion data (for AJAX requests)"""
    
    def get(self, request, *args, **kwargs):
        data_type = request.GET.get('type', 'overall')
        
        if data_type == 'overall':
            religion_view = ReligionDemographicsView()
            data = religion_view.get_religion_population_data()
        elif data_type == 'ward_wise':
            religion_view = ReligionDemographicsView()
            data = religion_view.get_ward_wise_religion_data()
        else:
            data = {'error': 'Invalid data type'}
        
        return JsonResponse(data, safe=False)


class ReligionReportPartialView(TemplateView):
    """View for generating religion report content for PDF inclusion"""
    
    template_name = 'demographics/religion/religion_report_partial.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the same data as main view
        religion_view = ReligionDemographicsView()
        religion_data = religion_view.get_religion_population_data()
        ward_data = religion_view.get_ward_wise_religion_data()
        
        # Generate charts for PDF
        chart_generator = ReligionChartGenerator()
        pdf_charts = {
            'overall_pie_chart': chart_generator.generate_pdf_chart(religion_data, 'pie'),
            'ward_comparison_bar': chart_generator.generate_pdf_chart(ward_data, 'bar'),
        }
        
        # Generate formal report content
        report_formatter = ReligionReportFormatter()
        report_content = report_formatter.generate_formal_report(religion_data, ward_data)
        
        context.update({
            'religion_data': religion_data,
            'ward_data': ward_data,
            'pdf_charts': pdf_charts,
            'report_content': report_content,
            'total_population': sum(data['population'] for data in religion_data.values()),
            'major_religions': religion_view.get_major_religions(religion_data),
            'ward_summary': religion_view.get_ward_summary(ward_data),
        })
        
        return context
