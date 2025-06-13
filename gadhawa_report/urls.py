"""
Main URL configuration for Gadhawa Report System.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

# Main URL patterns
urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    
    # API URLs
    path('api/v1/', include('apps.core.urls')),
    path('api/v1/auth/', include('apps.users.urls')),
    path('api/v1/demographics/', include('apps.demographics.urls')),
    path('api/v1/economics/', include('apps.economics.urls')),
    path('api/v1/social/', include('apps.social.urls')),
    path('api/v1/environment/', include('apps.environment.urls')),
    path('api/v1/infrastructure/', include('apps.infrastructure.urls')),
    path('api/v1/governance/', include('apps.governance.urls')),
    path('api/v1/reports/', include('apps.reports.urls')),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # Web interface (templates)
    path('', include('apps.core.web_urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # Add Django Debug Toolbar URLs in development
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns

# Customize admin site
admin.site.site_header = "गधावा गाउँपालिका - डिजिटल प्रोफाइल प्रतिवेदन"
admin.site.site_title = "Gadhawa Report Admin"
admin.site.index_title = "प्रतिवेदन व्यवस्थापन"
