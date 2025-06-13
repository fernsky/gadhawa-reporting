from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.http import HttpResponse, JsonResponse, Http404
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.gzip import gzip_page
from django.db.models import Q, Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core.paginator import Paginator
from django.utils import timezone
from django.urls import reverse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
import json
from datetime import datetime
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

from .models import (
    ReportCategory, ReportSection, ReportFigure, 
    ReportTable, PublicationSettings, ReportDownload
)
from .serializers import (
    ReportCategoryListSerializer, ReportCategoryDetailSerializer,
    ReportSectionListSerializer, ReportSectionDetailSerializer,
    SearchResultSerializer, PublicationSettingsSerializer
)


# Utility function to track downloads
def track_download(request, download_type, section=None):
    """Track download for analytics"""
    try:
        ReportDownload.objects.create(
            section=section,
            download_type=download_type,
            ip_address=request.META.get('REMOTE_ADDR', ''),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
    except Exception:
        pass  # Don't fail if tracking fails


# Public Documentation Views
@method_decorator([cache_page(60 * 15), gzip_page], name='dispatch')
class ReportHomeView(TemplateView):
    template_name = 'reports/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all active categories with sections
        categories = ReportCategory.objects.filter(
            is_active=True
        ).prefetch_related('sections').order_by('order')
        
        # Get publication settings
        publication_settings = PublicationSettings.objects.first()
        
        # Municipality name - make dynamic
        municipality_name = "गढवा गाउँपालिका"  # Updated to correct name
        municipality_name_english = "Gadhawa Rural Municipality"
        
        # Quick stats (can be made dynamic later)
        stats = [
            {
                'title': 'कुल जनसंख्या',
                'value': '१२,३४५',
                'icon': 'fas fa-users',
                'description': 'गत जनगणना अनुसार'
            },
            {
                'title': 'कुल वडा संख्या',
                'value': '९',
                'icon': 'fas fa-map-marker-alt',
                'description': 'प्रशासनिक वडाहरू'
            },
            {
                'title': 'कुल क्षेत्रफल',
                'value': '१२३.४५ वर्ग कि.मी.',
                'icon': 'fas fa-globe',
                'description': 'भौगोलिक क्षेत्रफल'
            },
            {
                'title': 'साक्षरता दर',
                'value': '७८.५%',
                'icon': 'fas fa-graduation-cap',
                'description': 'कुल साक्षरता दर'
            }
        ]
        
        context.update({
            'categories': categories,
            'publication_settings': publication_settings,
            'municipality_name': municipality_name,
            'municipality_name_english': municipality_name_english,
            'stats': stats,
            'total_categories': categories.count(),
            'total_sections': sum(cat.sections.count() for cat in categories),
        })
        
        return context


@method_decorator([cache_page(60 * 10), gzip_page], name='dispatch')
class ReportCategoryView(DetailView):
    model = ReportCategory
    template_name = 'reports/category_detail.html'
    context_object_name = 'category'
    
    def get_queryset(self):
        return ReportCategory.objects.filter(
            is_active=True
        ).prefetch_related(
            'sections__figures',
            'sections__tables'
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Municipality name - make dynamic
        municipality_name = "गधावा गाउँपालिका"
        municipality_name_english = "Gadhawa Rural Municipality"
        
        # Get publication settings
        publication_settings = PublicationSettings.objects.first()
        
        # Get category figures and tables
        category_figures = ReportFigure.objects.filter(
            section__category=self.object
        ).order_by('figure_number')
        
        category_tables = ReportTable.objects.filter(
            section__category=self.object
        ).order_by('table_number')
        
        # Navigation
        categories = ReportCategory.objects.filter(is_active=True).order_by('order')
        category_list = list(categories)
        
        try:
            current_index = category_list.index(self.object)
            prev_category = category_list[current_index - 1] if current_index > 0 else None
            next_category = category_list[current_index + 1] if current_index < len(category_list) - 1 else None
        except (ValueError, IndexError):
            prev_category = None
            next_category = None
        
        context.update({
            'municipality_name': municipality_name,
            'municipality_name_english': municipality_name_english,
            'publication_settings': publication_settings,
            'category_figures': category_figures,
            'category_tables': category_tables,
            'prev_category': prev_category,
            'next_category': next_category,
        })
        
        return context


@method_decorator([cache_page(60 * 5), gzip_page], name='dispatch')
class ReportSectionView(DetailView):
    model = ReportSection
    template_name = 'reports/section_detail.html'
    context_object_name = 'section'
    slug_field = 'slug'
    slug_url_kwarg = 'section_slug'
    
    def get_queryset(self):
        return ReportSection.objects.filter(
            is_published=True,
            category__slug=self.kwargs['category_slug']
        ).select_related('category').prefetch_related('figures', 'tables')
    
    def get_object(self, queryset=None):
        """Override to handle both category_slug and section_slug"""
        if queryset is None:
            queryset = self.get_queryset()
        
        category_slug = self.kwargs.get('category_slug')
        section_slug = self.kwargs.get('section_slug')
        
        if not category_slug or not section_slug:
            raise Http404("Section not found")
        
        try:
            obj = queryset.get(
                category__slug=category_slug,
                slug=section_slug
            )
        except self.model.DoesNotExist:
            raise Http404("Section not found")
        
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Municipality name - make dynamic
        municipality_name = "गधावा गाउँपालिका"
        municipality_name_english = "Gadhawa Rural Municipality"
        
        # Get publication settings
        publication_settings = PublicationSettings.objects.first()
        
        # Add category to context
        context['category'] = self.object.category
        
        # Navigation within category
        sections = list(self.object.category.sections.filter(is_published=True).order_by('order'))
        
        try:
            current_index = sections.index(self.object)
            prev_section = sections[current_index - 1] if current_index > 0 else None
            next_section = sections[current_index + 1] if current_index < len(sections) - 1 else None
        except (ValueError, IndexError):
            prev_section = None
            next_section = None
        
        context.update({
            'municipality_name': municipality_name,
            'municipality_name_english': municipality_name_english,
            'publication_settings': publication_settings,
            'prev_section': prev_section,
            'next_section': next_section,
        })
        
        return context


class TableOfContentsView(TemplateView):
    template_name = 'reports/table_of_contents.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Municipality name - make dynamic
        municipality_name = "गधावा गाउँपालिका"
        municipality_name_english = "Gadhawa Rural Municipality"
        
        # Get publication settings
        publication_settings = PublicationSettings.objects.first()
        
        # Get all categories and sections for TOC
        categories = ReportCategory.objects.filter(
            is_active=True
        ).prefetch_related(
            'sections__figures',
            'sections__tables'
        ).order_by('order')
        
        # Statistics
        total_sections = sum(cat.sections.filter(is_published=True).count() for cat in categories)
        total_figures = ReportFigure.objects.count()
        total_tables = ReportTable.objects.count()
        
        context.update({
            'municipality_name': municipality_name,
            'municipality_name_english': municipality_name_english,
            'publication_settings': publication_settings,
            'categories': categories,
            'total_sections': total_sections,
            'total_figures': total_figures,
            'total_tables': total_tables,
        })
        
        return context


class FigureListView(TemplateView):
    template_name = 'reports/figures_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Municipality name - make dynamic
        municipality_name = "गधावा गाउँपालिका"
        municipality_name_english = "Gadhawa Rural Municipality"
        
        # Get publication settings
        publication_settings = PublicationSettings.objects.first()
        
        # Get all figures
        figures = ReportFigure.objects.select_related(
            'section__category'
        ).order_by('section__category__order', 'figure_number')
        
        # Filter by category if specified
        category_filter = self.request.GET.get('category')
        if category_filter:
            figures = figures.filter(section__category__slug=category_filter)
        
        # Pagination
        paginator = Paginator(figures, 20)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Categories for filter
        categories = ReportCategory.objects.filter(
            is_active=True,
            sections__figures__isnull=False
        ).distinct().order_by('order')
        
        context.update({
            'municipality_name': municipality_name,
            'municipality_name_english': municipality_name_english,
            'publication_settings': publication_settings,
            'figures': page_obj,
            'categories': categories,
            'total_figures': figures.count(),
            'current_category': category_filter,
        })
        
        return context


class TableListView(TemplateView):
    template_name = 'reports/tables_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Municipality name - make dynamic
        municipality_name = "गधावा गाउँपालिका"
        municipality_name_english = "Gadhawa Rural Municipality"
        
        # Get publication settings
        publication_settings = PublicationSettings.objects.first()
        
        # Get all tables
        tables = ReportTable.objects.select_related(
            'section__category'
        ).order_by('section__category__order', 'table_number')
        
        # Filter by category if specified
        category_filter = self.request.GET.get('category')
        if category_filter:
            tables = tables.filter(section__category__slug=category_filter)
        
        # Pagination
        paginator = Paginator(tables, 20)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Categories for filter
        categories = ReportCategory.objects.filter(
            is_active=True,
            sections__tables__isnull=False
        ).distinct().order_by('order')
        
        context.update({
            'municipality_name': municipality_name,
            'municipality_name_english': municipality_name_english,
            'publication_settings': publication_settings,
            'tables': page_obj,
            'categories': categories,
            'total_tables': tables.count(),
            'current_category': category_filter,
        })
        
        return context


class ReportSearchView(TemplateView):
    template_name = 'reports/search.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Municipality name - make dynamic
        municipality_name = "गधावा गाउँपालिका"
        municipality_name_english = "Gadhawa Rural Municipality"
        
        # Get publication settings
        publication_settings = PublicationSettings.objects.first()
        
        # Get search query
        query = self.request.GET.get('q', '').strip()
        category_filter = self.request.GET.get('category', '')
        
        results = []
        page_obj = None
        
        if query:
            # Search in sections
            section_results = ReportSection.objects.filter(
                Q(title__icontains=query) |
                Q(title_nepali__icontains=query) |
                Q(content__icontains=query) |
                Q(content_nepali__icontains=query) |
                Q(summary__icontains=query) |
                Q(summary_nepali__icontains=query),
                is_published=True
            ).select_related('category')
            
            if category_filter:
                section_results = section_results.filter(category__slug=category_filter)
            
            # Convert to search results format
            for section in section_results:
                results.append({
                    'type': 'section',
                    'title': section.title_nepali or section.title,
                    'title_english': section.title,
                    'url': section.get_absolute_url(),
                    'category': section.category.name_nepali or section.category.name,
                    'summary': section.summary_nepali or section.summary or '',
                    'section_number': section.section_number,
                })
            
            # Pagination
            paginator = Paginator(results, 10)
            page_number = self.request.GET.get('page', 1)
            page_obj = paginator.get_page(page_number)
        
        # Categories for filter
        categories = ReportCategory.objects.filter(is_active=True).order_by('order')
        
        context.update({
            'municipality_name': municipality_name,
            'municipality_name_english': municipality_name_english,
            'publication_settings': publication_settings,
            'query': query,
            'results': page_obj.object_list if page_obj else [],
            'page_obj': page_obj,
            'categories': categories,
            'current_category': category_filter,
            'total_results': len(results) if results else 0,
        })
        
        return context


class TableOfContentsView(TemplateView):
    template_name = 'reports/table_of_contents.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        categories = ReportCategory.objects.filter(
            is_active=True,
            sections__is_published=True
        ).distinct().prefetch_related(
            'sections__figures',
            'sections__tables'
        ).order_by('order')
        
        context.update({
            'categories': categories,
            'page_title': 'विषय सूची - गढवा गाउँपालिका',
        })
        
        return context


class FigureListView(TemplateView):
    template_name = 'reports/figures_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        figures = ReportFigure.objects.filter(
            section__is_published=True
        ).select_related('section', 'section__category').order_by(
            'section__category__order', 'section__order', 'order'
        )
        
        context.update({
            'figures': figures,
            'page_title': 'चित्रहरूको सूची - गढवा गाउँपालिका',
        })
        
        return context


class TableListView(TemplateView):
    template_name = 'reports/tables_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        tables = ReportTable.objects.filter(
            section__is_published=True
        ).select_related('section', 'section__category').order_by(
            'section__category__order', 'section__order', 'order'
        )
        
        context.update({
            'tables': tables,
            'page_title': 'तालिकाहरूको सूची - गढवा गाउँपालिका',
        })
        
        return context


class ReportSearchView(TemplateView):
    template_name = 'reports/search.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '')
        
        results = []
        if query and len(query) >= 2:
            # Search in sections
            section_results = ReportSection.objects.filter(
                Q(title__icontains=query) |
                Q(title_nepali__icontains=query) |
                Q(content__icontains=query) |
                Q(content_nepali__icontains=query) |
                Q(summary__icontains=query) |
                Q(summary_nepali__icontains=query),
                is_published=True
            ).select_related('category')
            
            results = section_results[:20]
        
        context.update({
            'query': query,
            'results': results,
            'page_title': f'खोज परिणाम: {query}' if query else 'खोज - गढवा गाउँपालिका',
        })
        
        return context


# PDF Generation Views
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
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.units import inch
        
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


# API Views
class CategoryListAPIView(generics.ListAPIView):
    serializer_class = ReportCategoryListSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        return ReportCategory.objects.filter(is_active=True).order_by('order')


class CategoryDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ReportCategoryDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    
    def get_queryset(self):
        return ReportCategory.objects.filter(is_active=True).prefetch_related(
            'sections__figures',
            'sections__tables'
        )


class SectionListAPIView(generics.ListAPIView):
    serializer_class = ReportSectionListSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = ReportSection.objects.filter(is_published=True).select_related('category')
        
        # Filter by category
        category_slug = self.request.query_params.get('category', None)
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Filter by featured
        featured = self.request.query_params.get('featured', None)
        if featured and featured.lower() == 'true':
            queryset = queryset.filter(is_featured=True)
        
        return queryset.order_by('category__order', 'order', 'section_number')


class SectionDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ReportSectionDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'
    
    def get_queryset(self):
        return ReportSection.objects.filter(is_published=True).select_related('category').prefetch_related(
            'figures',
            'tables'
        )


class ReportSearchAPIView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        query = request.query_params.get('q', '')
        
        if not query or len(query) < 2:
            return Response({'results': [], 'count': 0})
        
        results = []
        
        # Search sections
        sections = ReportSection.objects.filter(
            Q(title__icontains=query) |
            Q(title_nepali__icontains=query) |
            Q(content__icontains=query) |
            Q(content_nepali__icontains=query),
            is_published=True
        ).select_related('category')[:10]
        
        for section in sections:
            results.append({
                'type': 'section',
                'title': section.title,
                'title_nepali': section.title_nepali,
                'content': section.summary or section.content[:200] + '...',
                'url': section.get_absolute_url(),
                'section_number': section.section_number,
                'category': section.category.name,
            })
        
        serializer = SearchResultSerializer(results, many=True)
        return Response({
            'results': serializer.data,
            'count': len(results)
        })


class DownloadStatsAPIView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        from django.db.models import Count
        from datetime import timedelta
        
        # Get download stats for last 30 days
        thirty_days_ago = timezone.now() - timedelta(days=30)
        
        stats = ReportDownload.objects.filter(
            downloaded_at__gte=thirty_days_ago
        ).aggregate(
            total_downloads=Count('id'),
            pdf_downloads=Count('id', filter=Q(download_type='pdf')),
            full_report_downloads=Count('id', filter=Q(download_type='full_report')),
        )
        
        return Response(stats)


# SEO and Utility Views
class ReportSitemapView(TemplateView):
    template_name = 'reports/sitemap.xml'
    content_type = 'application/xml'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Municipality name - make dynamic
        municipality_name = "गधावा गाउँपालिका"
        municipality_name_english = "Gadhawa Rural Municipality"
        
        # Get all published content
        categories = ReportCategory.objects.filter(is_active=True)
        sections = ReportSection.objects.filter(is_published=True).select_related('category')
        
        context.update({
            'municipality_name': municipality_name,
            'municipality_name_english': municipality_name_english,
            'categories': categories,
            'sections': sections,
            'base_url': self.request.build_absolute_uri('/'),
        })
        
        return context


class RobotsView(TemplateView):
    template_name = 'reports/robots.txt'
    content_type = 'text/plain'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context.update({
            'base_url': self.request.build_absolute_uri('/'),
            'sitemap_url': self.request.build_absolute_uri('/sitemap.xml'),
        })
        
        return context
        context = super().get_context_data(**kwargs)
        context['domain'] = self.request.get_host()
        return context
