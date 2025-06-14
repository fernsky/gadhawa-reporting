from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
import io

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from weasyprint import HTML

from .base import track_download
from ..models import ReportCategory, ReportSection, ReportFigure, ReportTable, PublicationSettings


class PDFGeneratorMixin:
    """Mixin for PDF generation functionality"""
    
    def get_publication_settings(self):
        try:
            return PublicationSettings.objects.first()
        except PublicationSettings.DoesNotExist:
            return None
    
    def generate_pdf_with_weasyprint(self, template_name, context, filename):
        """Generate PDF using WeasyPrint for better styling"""
        try:
            html_content = render_to_string(template_name, context)
            
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
        
        # Create PDF document
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Add title
        if 'municipality_name' in context:
            title = Paragraph(context['municipality_name'], styles['Title'])
            story.append(title)
            story.append(Spacer(1, 12))
        
        # Add content based on context
        if 'category' in context and context['category']:
            category_title = Paragraph(f"Category: {context['category'].name}", styles['Heading1'])
            story.append(category_title)
            story.append(Spacer(1, 12))
            
            if hasattr(context['category'], 'description') and context['category'].description:
                desc = Paragraph(context['category'].description, styles['Normal'])
                story.append(desc)
                story.append(Spacer(1, 12))
        
        if 'section' in context and context['section']:
            section_title = Paragraph(f"Section: {context['section'].title}", styles['Heading1'])
            story.append(section_title)
            story.append(Spacer(1, 12))
            
            if context['section'].content:
                content = Paragraph(context['section'].content[:1000] + "...", styles['Normal'])
                story.append(content)
        
        # Build PDF
        doc.build(story)
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        
        return response


class GenerateFullReportPDFView(PDFGeneratorMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        # Track download
        track_download(request, 'full_report')
        
        # Municipality name - make dynamic
        municipality_name = "गधावा गाउँपालिका"
        municipality_name_english = "Gadhawa Rural Municipality"
        
        # Get publication settings (optional)
        publication_settings = self.get_publication_settings()
        
        # Use hardcoded content instead of database data
        context = {
            'municipality_name': municipality_name,
            'municipality_name_english': municipality_name_english,
            'publication_settings': publication_settings,
            'generated_date': timezone.now(),
            # No need for categories, figures, tables since we're using hardcoded partials
        }
        
        filename = f"gadhawa_digital_profile_report_{timezone.now().strftime('%Y%m%d')}.pdf"
        return self.generate_pdf_with_weasyprint('reports/pdf_full_report.html', context, filename)


class GenerateCategoryPDFView(PDFGeneratorMixin, TemplateView):
    def get(self, request, slug, *args, **kwargs):
        category = get_object_or_404(ReportCategory, slug=slug, is_active=True)
        
        # Track download
        track_download(request, 'pdf')
        
        # Municipality name - make dynamic
        municipality_name = "गधावा गाउँपालिका"
        municipality_name_english = "Gadhawa Rural Municipality"
        
        publication_settings = self.get_publication_settings()
        sections = category.sections.filter(is_published=True).prefetch_related('figures', 'tables')
        
        # Get category figures and tables
        category_figures = ReportFigure.objects.filter(section__category=category)
        category_tables = ReportTable.objects.filter(section__category=category)
        
        context = {
            'municipality_name': municipality_name,
            'municipality_name_english': municipality_name_english,
            'publication_settings': publication_settings,
            'category': category,
            'sections': sections,
            'category_figures': category_figures,
            'category_tables': category_tables,
            'generated_date': timezone.now(),
        }
        
        filename = f"gadhawa_{category.slug}_report_{timezone.now().strftime('%Y%m%d')}.pdf"
        return self.generate_pdf_with_weasyprint('reports/pdf_category.html', context, filename)


class GenerateSectionPDFView(PDFGeneratorMixin, TemplateView):
    def get(self, request, category_slug, section_slug, *args, **kwargs):
        section = get_object_or_404(
            ReportSection,
            category__slug=category_slug,
            slug=section_slug,
            is_published=True
        )
        
        # Track download
        track_download(request, 'section', section)
        
        # Municipality name - make dynamic
        municipality_name = "गधावा गाउँपालिका"
        municipality_name_english = "Gadhawa Rural Municipality"
        
        publication_settings = self.get_publication_settings()
        
        context = {
            'municipality_name': municipality_name,
            'municipality_name_english': municipality_name_english,
            'publication_settings': publication_settings,
            'section': section,
            'category': section.category,
            'generated_date': timezone.now(),
        }
        
        filename = f"gadhawa_{section.category.slug}_{section.slug}_{timezone.now().strftime('%Y%m%d')}.pdf"
        return self.generate_pdf_with_weasyprint('reports/pdf_section.html', context, filename)
