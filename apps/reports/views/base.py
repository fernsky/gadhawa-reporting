from django.utils import timezone
from ..models import ReportCategory, ReportSection, ReportDownload, PublicationSettings
from ..utils.nepali_numbers import to_nepali_digits


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


class ReportContextMixin:
    """Mixin to provide common context for all report views"""
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all categories with their sections for sidebar navigation
        categories = ReportCategory.objects.filter(
            is_active=True
        ).prefetch_related(
            'sections'
        ).order_by('order')
        
        # Add current page context
        current_category = None
        current_section = None
        
        # Try to get current category and section from the view
        if hasattr(self, 'object'):
            if isinstance(self.object, ReportCategory):
                current_category = self.object
            elif isinstance(self.object, ReportSection):
                current_section = self.object
                current_category = self.object.category
        
        # Alternative: get from URL kwargs
        if not current_category and 'category_slug' in self.kwargs:
            try:
                current_category = ReportCategory.objects.get(
                    slug=self.kwargs['category_slug'],
                    is_active=True
                )
            except ReportCategory.DoesNotExist:
                pass
        
        if not current_section and 'section_slug' in self.kwargs and current_category:
            try:
                current_section = ReportSection.objects.get(
                    slug=self.kwargs['section_slug'],
                    category=current_category,
                    is_published=True
                )
            except ReportSection.DoesNotExist:
                pass
        
        # Municipality name - make dynamic
        municipality_name = "गढवा गाउँपालिका"
        municipality_name_english = "Gadhawa Rural Municipality"
        
        # Get publication settings
        publication_settings = PublicationSettings.objects.first()
        
        context.update({
            'categories': categories,
            'current_category': current_category,
            'current_section': current_section,
            'municipality_name': municipality_name,
            'municipality_name_english': municipality_name_english,
            'publication_settings': publication_settings,
        })
        
        return context
