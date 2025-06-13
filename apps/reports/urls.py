from django.urls import path, include
from . import views

app_name = 'reports'

urlpatterns = [
    # Public documentation site
    path('', views.ReportHomeView.as_view(), name='home'),
    path('category/<slug:slug>/', views.ReportCategoryView.as_view(), name='category'),
    path('section/<slug:category_slug>/<slug:section_slug>/', views.ReportSectionView.as_view(), name='section'),
    
    # PDF Generation
    path('pdf/full/', views.GenerateFullReportPDFView.as_view(), name='pdf_full'),
    path('pdf/category/<slug:slug>/', views.GenerateCategoryPDFView.as_view(), name='pdf_category'),
    path('pdf/section/<slug:category_slug>/<slug:section_slug>/', views.GenerateSectionPDFView.as_view(), name='pdf_section'),
    
    # API endpoints
    path('api/', include([
        path('categories/', views.CategoryListAPIView.as_view(), name='api_categories'),
        path('categories/<slug:slug>/', views.CategoryDetailAPIView.as_view(), name='api_category_detail'),
        path('sections/', views.SectionListAPIView.as_view(), name='api_sections'),
        path('sections/<uuid:id>/', views.SectionDetailAPIView.as_view(), name='api_section_detail'),
        path('search/', views.ReportSearchAPIView.as_view(), name='api_search'),
        path('download-stats/', views.DownloadStatsAPIView.as_view(), name='api_download_stats'),
    ])),
    
    # SEO and utility routes
    path('sitemap.xml', views.ReportSitemapView.as_view(), name='sitemap'),
    path('robots.txt', views.RobotsView.as_view(), name='robots'),
    path('search/', views.ReportSearchView.as_view(), name='search'),
    
    # Table of Contents and Lists
    path('toc/', views.TableOfContentsView.as_view(), name='toc'),
    path('figures/', views.FigureListView.as_view(), name='figures'),
    path('tables/', views.TableListView.as_view(), name='tables'),
]
