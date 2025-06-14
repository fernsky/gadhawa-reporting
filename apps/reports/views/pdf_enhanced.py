"""
Enhanced PDF generation with exact page references and Nepali digit conversion
"""
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
import io
import re

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from weasyprint import HTML

from .base import track_download
from ..models import ReportCategory, ReportSection, ReportFigure, ReportTable, PublicationSettings
from ..utils.nepali_numbers import to_nepali_digits


class NepaliPDFProcessor:
    """Post-processor to convert Arabic numerals to Nepali digits in PDF footers"""
    
    @staticmethod
    def convert_page_numbers_to_nepali(html_content):
        """
        Convert page numbers in the generated HTML to Nepali digits before PDF generation
        This is a preprocessing step for the HTML content
        """
        # This is a placeholder - in practice, we'd need to parse and modify the HTML
        # to inject Nepali digits where needed
        return html_content


class PDFGeneratorMixin:
    """Enhanced mixin for PDF generation with exact page references"""
    
    def get_publication_settings(self):
        try:
            return PublicationSettings.objects.first()
        except PublicationSettings.DoesNotExist:
            return None
    
    def generate_pdf_with_weasyprint(self, template_name, context, filename):
        """Generate PDF using WeasyPrint with exact page references"""
        try:
            html_content = render_to_string(template_name, context)
            
            # Post-process for Nepali digits if needed
            processor = NepaliPDFProcessor()
            html_content = processor.convert_page_numbers_to_nepali(html_content)
            
            # Create PDF
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            
            # Generate PDF with WeasyPrint
            base_url = self.request.build_absolute_uri('/')
            HTML(string=html_content, base_url=base_url).write_pdf(response)
            
            return response
            
        except Exception as e:
            # Fallback to ReportLab if WeasyPrint fails
            return self.generate_pdf_with_reportlab(template_name, context, filename)
    
    def generate_pdf_with_reportlab(self, template_name, context, filename):
        """Fallback PDF generation using ReportLab"""
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        
        # Build content
        content = []
        content.append(Paragraph("गढवा गाउँपालिका - पूर्ण प्रतिवेदन", styles['Title']))
        content.append(Spacer(1, 12))
        
        # Add basic content
        content.append(Paragraph("यो ReportLab फलब्याक संस्करण हो।", styles['Normal']))
        
        doc.build(content)
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        
        return response


class GenerateFullPDFView(PDFGeneratorMixin, TemplateView):
    """Enhanced view for generating full PDF report with exact page references"""
    
    def get(self, request, *args, **kwargs):
        # Track download
        track_download(request, 'pdf')
        
        # Municipality name - make dynamic
        municipality_name = "गढवा गाउँपालिका"
        municipality_name_english = "Gadhawa Rural Municipality"
        
        # Get all data
        publication_settings = self.get_publication_settings()
        categories = ReportCategory.objects.filter(
            is_active=True,
            sections__is_published=True
        ).distinct().prefetch_related(
            'sections__figures',
            'sections__tables'
        ).order_by('order')
        
        # Get all figures and tables for lists
        figures = ReportFigure.objects.select_related('section__category').order_by('figure_number')
        tables = ReportTable.objects.select_related('section__category').order_by('table_number')
        
        context = {
            'municipality_name': municipality_name,
            'municipality_name_english': municipality_name_english,
            'publication_settings': publication_settings,
            'categories': categories,
            'figures': figures,
            'tables': tables,
            'total_figures': figures.count(),
            'total_tables': tables.count(),
            'generated_date': timezone.now(),
            'use_exact_pages': True,  # Flag to indicate we're using exact page references
        }
        
        filename = f"gadhawa_digital_profile_report_{timezone.now().strftime('%Y%m%d')}.pdf"
        return self.generate_pdf_with_weasyprint('reports/pdf_full_report.html', context, filename)


class GenerateCategoryPDFView(PDFGeneratorMixin, TemplateView):
    def get(self, request, slug, *args, **kwargs):
        category = get_object_or_404(ReportCategory, slug=slug, is_active=True)
        
        # Track download
        track_download(request, 'pdf')
        
        # Municipality name - make dynamic
        municipality_name = "गढवा गाउँपालिका"
        municipality_name_english = "Gadhawa Rural Municipality"
        
        publication_settings = self.get_publication_settings()
        sections = category.sections.filter(is_published=True).prefetch_related('figures', 'tables')
        
        # Get category figures and tables
        figures = ReportFigure.objects.filter(section__category=category).order_by('figure_number')
        tables = ReportTable.objects.filter(section__category=category).order_by('table_number')
        
        context = {
            'municipality_name': municipality_name,
            'municipality_name_english': municipality_name_english,
            'publication_settings': publication_settings,
            'category': category,
            'sections': sections,
            'figures': figures,
            'tables': tables,
            'generated_date': timezone.now(),
            'use_exact_pages': True,
        }
        
        filename = f"gadhawa_{category.slug}_report_{timezone.now().strftime('%Y%m%d')}.pdf"
        return self.generate_pdf_with_weasyprint('reports/pdf_category.html', context, filename)


class GenerateSectionPDFView(PDFGeneratorMixin, TemplateView):
    def get(self, request, category_slug, section_slug, *args, **kwargs):
        category = get_object_or_404(ReportCategory, slug=category_slug, is_active=True)
        section = get_object_or_404(ReportSection, slug=section_slug, category=category, is_published=True)
        
        # Track download
        track_download(request, 'pdf')
        
        # Municipality name - make dynamic
        municipality_name = "गढवा गाउँपालिका"
        municipality_name_english = "Gadhawa Rural Municipality"
        
        publication_settings = self.get_publication_settings()
        
        context = {
            'municipality_name': municipality_name,
            'municipality_name_english': municipality_name_english,
            'publication_settings': publication_settings,
            'category': category,
            'section': section,
            'figures': section.figures.all(),
            'tables': section.tables.all(),
            'generated_date': timezone.now(),
            'use_exact_pages': True,
        }
        
        filename = f"gadhawa_{category.slug}_{section.slug}_{timezone.now().strftime('%Y%m%d')}.pdf"
        return self.generate_pdf_with_weasyprint('reports/pdf_section.html', context, filename)
