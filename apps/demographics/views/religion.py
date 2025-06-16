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

from ..models import MunicipalityWideReligionPopulation, ReligionTypeChoice
from ..utils.svg_chart_generator import SVGChartGenerator
from ..utils.report_formatter import ReligionReportFormatter


class ReligionDemographicsView(TemplateView):
    """Main view for religion demographics analysis"""
    
    template_name = 'demographics/religion/religion_analysis.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get religion population data
        religion_data = self.get_religion_population_data()
        
        # Generate charts using SVG chart generator
        svg_chart_generator = SVGChartGenerator()
        charts = {
            'overall_pie_chart': svg_chart_generator.generate_pie_chart_svg(religion_data),
            'overall_bar_chart': svg_chart_generator.generate_bar_chart_svg({}),  # For ward data if needed
        }
        
        # Generate formal report content
        report_formatter = ReligionReportFormatter()
        report_content = report_formatter.generate_formal_report(religion_data)
        
        context.update({
            'religion_data': religion_data,
            'charts': charts,
            'report_content': report_content,
            'total_population': sum(data['population'] for data in religion_data.values()),
            'total_religions': len([r for r in religion_data.values() if r['population'] > 0]),
            'major_religions': self.get_major_religions(religion_data),
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
            }
        
        # Get actual data from database
        total_population = 0
        for religion_obj in MunicipalityWideReligionPopulation.objects.all():
            religion_type = religion_obj.religion_type
            if religion_type in religion_data:
                religion_data[religion_type]['population'] = religion_obj.population
                total_population += religion_obj.population
        
        # Calculate percentages
        if total_population > 0:
            for religion_type, data in religion_data.items():
                if data['population'] > 0:
                    data['percentage'] = (data['population'] / total_population * 100)
        
        return religion_data
    
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


class ReligionDataAPIView(TemplateView):
    """API view for religion data (for AJAX requests)"""
    
    def get(self, request, *args, **kwargs):
        data_type = request.GET.get('type', 'overall')
        
        religion_view = ReligionDemographicsView()
        data = religion_view.get_religion_population_data()
        
        return JsonResponse(data, safe=False)


class ReligionReportPartialView(TemplateView):
    """View for generating religion report content for PDF inclusion"""
    
    template_name = 'demographics/religion/religion_report_partial.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the same data as main view
        religion_view = ReligionDemographicsView()
        religion_data = religion_view.get_religion_population_data()
        
        # Generate charts for PDF using SVG chart generator
        svg_chart_generator = SVGChartGenerator()
        pdf_charts = {
            'overall_pie_chart': svg_chart_generator.generate_pie_chart_svg(religion_data),
        }
        
        # Generate formal report content
        report_formatter = ReligionReportFormatter()
        report_content = report_formatter.generate_formal_report(religion_data)
        
        context.update({
            'religion_data': religion_data,
            'pdf_charts': pdf_charts,
            'report_content': report_content,
            'total_population': sum(data['population'] for data in religion_data.values()),
            'major_religions': religion_view.get_major_religions(religion_data),
        })
        
        return context
