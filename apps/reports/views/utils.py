from django.views.generic import TemplateView

from ..models import ReportCategory, ReportSection


class ReportSitemapView(TemplateView):
    template_name = "reports/sitemap.xml"
    content_type = "application/xml"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Municipality name - make dynamic
        municipality_name = "गढवा गाउँपालिका"
        municipality_name_english = "Lungri Rural Municipality"

        # Get all published content
        categories = ReportCategory.objects.filter(is_active=True)
        sections = ReportSection.objects.filter(is_published=True).select_related(
            "category"
        )

        context.update(
            {
                "municipality_name": municipality_name,
                "municipality_name_english": municipality_name_english,
                "categories": categories,
                "sections": sections,
                "base_url": self.request.build_absolute_uri("/"),
            }
        )

        return context


class RobotsView(TemplateView):
    template_name = "reports/robots.txt"
    content_type = "text/plain"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(
            {
                "base_url": self.request.build_absolute_uri("/"),
                "sitemap_url": self.request.build_absolute_uri("/sitemap.xml"),
            }
        )

        return context
