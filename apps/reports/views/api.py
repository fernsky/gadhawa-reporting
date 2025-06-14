from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from ..models import ReportCategory, ReportSection, ReportDownload
from ..serializers import (
    ReportCategoryListSerializer, ReportCategoryDetailSerializer,
    ReportSectionListSerializer, ReportSectionDetailSerializer,
    SearchResultSerializer
)


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
