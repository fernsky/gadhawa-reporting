from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, TemplateView
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.gzip import gzip_page
from django.db.models import Q
from django.core.paginator import Paginator
import datetime

from .base import ReportContextMixin
from ..models import (
    ReportCategory,
    ReportSection,
    ReportFigure,
    ReportTable,
    PublicationSettings,
)
from ..utils.nepali_numbers import to_nepali_digits
from apps.demographics.processors.manager import get_demographics_manager
from apps.social.processors.manager import get_social_manager
from apps.infrastructure.processors.manager import get_infrastructure_manager
from apps.economics.processors.manager import get_economics_manager


@method_decorator([cache_page(60 * 15), gzip_page], name="dispatch")
class ReportHomeView(ReportContextMixin, TemplateView):
    template_name = "reports/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get all active categories with sections for homepage
        categories = context["categories"]

        # Quick stats (can be made dynamic later)
        stats = [
            {
                "title": "कुल जनसंख्या",
                "value": "१२,३४५",
                "icon": "fas fa-users",
                "description": "गत जनगणना अनुसार",
            },
            {
                "title": "कुल वडा संख्या",
                "value": "९",
                "icon": "fas fa-map-marker-alt",
                "description": "प्रशासनिक वडाहरू",
            },
            {
                "title": "कुल क्षेत्रफल",
                "value": "१२३.४५ वर्ग कि.मी.",
                "icon": "fas fa-globe",
                "description": "भौगोलिक क्षेत्रफल",
            },
            {
                "title": "साक्षरता दर",
                "value": "७८.५%",
                "icon": "fas fa-graduation-cap",
                "description": "कुल साक्षरता दर",
            },
        ]

        total_categories = categories.count()
        total_sections = sum(
            cat.sections.filter(is_published=True).count() for cat in categories
        )

        context.update(
            {
                "stats": stats,
                "total_categories": total_categories,
                "total_categories_nepali": to_nepali_digits(str(total_categories)),
                "total_sections": total_sections,
                "total_sections_nepali": to_nepali_digits(str(total_sections)),
            }
        )

        return context


@method_decorator([cache_page(60 * 10), gzip_page], name="dispatch")
class ReportCategoryView(ReportContextMixin, DetailView):
    model = ReportCategory
    template_name = "reports/category_detail.html"
    context_object_name = "category"

    def get_queryset(self):
        return ReportCategory.objects.filter(is_active=True).prefetch_related(
            "sections__figures", "sections__tables"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get category figures and tables
        category_figures = ReportFigure.objects.filter(
            section__category=self.object
        ).order_by("figure_number")

        category_tables = ReportTable.objects.filter(
            section__category=self.object
        ).order_by("table_number")

        # Navigation
        categories = context["categories"]
        category_list = list(categories)

        try:
            current_index = category_list.index(self.object)
            prev_category = (
                category_list[current_index - 1] if current_index > 0 else None
            )
            next_category = (
                category_list[current_index + 1]
                if current_index < len(category_list) - 1
                else None
            )
        except (ValueError, IndexError):
            prev_category = None
            next_category = None

        context.update(
            {
                "category_figures": category_figures,
                "category_tables": category_tables,
                "prev_category": prev_category,
                "next_category": next_category,
            }
        )

        return context


@method_decorator([cache_page(60 * 5), gzip_page], name="dispatch")
class ReportSectionView(ReportContextMixin, DetailView):
    model = ReportSection
    template_name = "reports/section_detail.html"
    context_object_name = "section"
    slug_field = "slug"
    slug_url_kwarg = "section_slug"

    def get_queryset(self):
        return (
            ReportSection.objects.filter(
                is_published=True, category__slug=self.kwargs["category_slug"]
            )
            .select_related("category")
            .prefetch_related("figures", "tables")
        )

    def get_object(self, queryset=None):
        """Override to handle both category_slug and section_slug"""
        if queryset is None:
            queryset = self.get_queryset()

        category_slug = self.kwargs.get("category_slug")
        section_slug = self.kwargs.get("section_slug")

        if not category_slug or not section_slug:
            raise Http404("Section not found")

        try:
            obj = queryset.get(category__slug=category_slug, slug=section_slug)
        except self.model.DoesNotExist:
            raise Http404("Section not found")

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add category to context (already handled by mixin, but keeping for compatibility)
        context["category"] = self.object.category

        # Navigation within category
        sections = list(
            self.object.category.sections.filter(is_published=True).order_by("order")
        )

        try:
            current_index = sections.index(self.object)
            prev_section = sections[current_index - 1] if current_index > 0 else None
            next_section = (
                sections[current_index + 1]
                if current_index < len(sections) - 1
                else None
            )
        except (ValueError, IndexError):
            prev_section = None
            next_section = None

        context.update(
            {
                "prev_section": prev_section,
                "next_section": next_section,
            }
        )

        return context


class TableOfContentsView(ReportContextMixin, TemplateView):
    template_name = "reports/table_of_contents.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        categories = (
            context["categories"]
            .filter(sections__is_published=True)
            .distinct()
            .prefetch_related("sections__figures", "sections__tables")
        )

        # Statistics
        total_sections = sum(
            cat.sections.filter(is_published=True).count() for cat in categories
        )
        total_figures = ReportFigure.objects.count()
        total_tables = ReportTable.objects.count()

        context.update(
            {
                "categories": categories,
                "total_sections": total_sections,
                "total_sections_nepali": to_nepali_digits(str(total_sections)),
                "total_figures": total_figures,
                "total_figures_nepali": to_nepali_digits(str(total_figures)),
                "total_tables": total_tables,
                "total_tables_nepali": to_nepali_digits(str(total_tables)),
            }
        )

        return context


class FigureListView(ReportContextMixin, TemplateView):
    template_name = "reports/figures_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get all figures
        figures = ReportFigure.objects.select_related("section__category").order_by(
            "section__category__order", "figure_number"
        )

        # Filter by category if specified
        category_filter = self.request.GET.get("category")
        if category_filter:
            figures = figures.filter(section__category__slug=category_filter)

        # Pagination
        paginator = Paginator(figures, 20)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        # Categories for filter
        filter_categories = (
            ReportCategory.objects.filter(
                is_active=True, sections__figures__isnull=False
            )
            .distinct()
            .order_by("order")
        )

        context.update(
            {
                "figures": page_obj,
                "filter_categories": filter_categories,
                "total_figures": figures.count(),
                "current_category": category_filter,
            }
        )

        return context


class TableListView(ReportContextMixin, TemplateView):
    template_name = "reports/tables_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get all tables
        tables = ReportTable.objects.select_related("section__category").order_by(
            "section__category__order", "table_number"
        )

        # Filter by category if specified
        category_filter = self.request.GET.get("category")
        if category_filter:
            tables = tables.filter(section__category__slug=category_filter)

        # Pagination
        paginator = Paginator(tables, 20)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        # Categories for filter
        filter_categories = (
            ReportCategory.objects.filter(
                is_active=True, sections__tables__isnull=False
            )
            .distinct()
            .order_by("order")
        )

        context.update(
            {
                "tables": page_obj,
                "filter_categories": filter_categories,
                "total_tables": tables.count(),
                "current_category": category_filter,
            }
        )

        return context


class ReportSearchView(ReportContextMixin, TemplateView):
    template_name = "reports/search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get search query
        query = self.request.GET.get("q", "").strip()
        category_filter = self.request.GET.get("category", "")

        results = []
        page_obj = None

        if query:
            # Search in sections
            section_results = ReportSection.objects.filter(
                Q(title__icontains=query)
                | Q(title_nepali__icontains=query)
                | Q(content__icontains=query)
                | Q(content_nepali__icontains=query)
                | Q(summary__icontains=query)
                | Q(summary_nepali__icontains=query),
                is_published=True,
            ).select_related("category")

            if category_filter:
                section_results = section_results.filter(category__slug=category_filter)

            # Convert to search results format
            for section in section_results:
                results.append(
                    {
                        "type": "section",
                        "title": section.title_nepali or section.title,
                        "title_english": section.title,
                        "url": section.get_absolute_url(),
                        "category": section.category.name_nepali
                        or section.category.name,
                        "summary": section.summary_nepali or section.summary or "",
                        "section_number": section.section_number,
                    }
                )

            # Pagination
            paginator = Paginator(results, 10)
            page_number = self.request.GET.get("page", 1)
            page_obj = paginator.get_page(page_number)

        context.update(
            {
                "query": query,
                "results": page_obj.object_list if page_obj else [],
                "page_obj": page_obj,
                "current_category": category_filter,
                "total_results": len(results) if results else 0,
            }
        )

        return context


class FullReportView(ReportContextMixin, TemplateView):
    template_name = "reports/web_full_report.html"

    def get_publication_settings(self):
        """Get publication settings from the database"""
        try:
            return PublicationSettings.objects.first()
        except PublicationSettings.DoesNotExist:
            return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Municipality name - make dynamic
        municipality_name = "लुङ्ग्री गाउँपालिका"
        municipality_name_english = "Lungri Rural Municipality"

        # Get publication settings (optional)
        publication_settings = self.get_publication_settings()

        # Get all data using processor system
        demographics_manager = get_demographics_manager()
        social_manager = get_social_manager()
        infrastructure_manager = get_infrastructure_manager()
        economics_manager = get_economics_manager()

        # Generate all charts before processing data
        demographics_manager.generate_all_charts()
        social_manager.generate_all_charts()
        infrastructure_manager.generate_all_charts()
        economics_manager.generate_all_charts()

        # Get processed data with charts
        all_demographics_data = demographics_manager.process_all_for_pdf()
        all_social_data = social_manager.process_all_for_pdf()
        all_infrastructure_data = infrastructure_manager.process_all_for_pdf()
        all_economics_data = economics_manager.process_all_for_pdf()

        # Extract chart URLs for template use
        pdf_charts = {}
        for category, data in all_demographics_data.items():
            if "charts" in data:
                pdf_charts[category] = data["charts"]

        for category, data in all_social_data.items():
            if "pdf_charts" in data and data["pdf_charts"]:
                pdf_charts.update(data["pdf_charts"])

        for category, data in all_infrastructure_data.items():
            if "pdf_charts" in data and data["pdf_charts"]:
                pdf_charts.update(data["pdf_charts"])

        for category, data in all_economics_data.items():
            if "pdf_charts" in data and data["pdf_charts"]:
                pdf_charts.update(data["pdf_charts"])

        context.update(
            {
                "municipality_name": municipality_name,
                "municipality_name_english": municipality_name_english,
                "publication_settings": publication_settings,
                "generated_date": datetime.datetime.now(),
                "all_demographics_data": all_demographics_data,
                "all_social_data": all_social_data,
                "all_infrastructure_data": all_infrastructure_data,
                "all_economics_data": all_economics_data,
                "pdf_charts": pdf_charts,
            }
        )

        return context
