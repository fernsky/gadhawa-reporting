from rest_framework import serializers
from .models import (
    ReportCategory, ReportSection, ReportFigure, 
    ReportTable, PublicationSettings
)


class ReportFigureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportFigure
        fields = [
            'id', 'title', 'title_nepali', 'figure_type', 'figure_number',
            'description', 'description_nepali', 'image', 'data_source',
            'chart_data', 'order'
        ]


class ReportTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportTable
        fields = [
            'id', 'title', 'title_nepali', 'table_number',
            'description', 'description_nepali', 'data', 'data_source', 'order'
        ]


class ReportSectionListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_name_nepali = serializers.CharField(source='category.name_nepali', read_only=True)
    absolute_url = serializers.CharField(source='get_absolute_url', read_only=True)
    
    class Meta:
        model = ReportSection
        fields = [
            'id', 'title', 'title_nepali', 'slug', 'section_number',
            'summary', 'summary_nepali', 'category_name', 'category_name_nepali',
            'absolute_url', 'is_published', 'is_featured', 'published_at'
        ]


class ReportSectionDetailSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only=True)
    figures = ReportFigureSerializer(many=True, read_only=True)
    tables = ReportTableSerializer(many=True, read_only=True)
    absolute_url = serializers.CharField(source='get_absolute_url', read_only=True)
    
    class Meta:
        model = ReportSection
        fields = [
            'id', 'title', 'title_nepali', 'slug', 'section_number',
            'content', 'content_nepali', 'summary', 'summary_nepali',
            'category', 'figures', 'tables', 'absolute_url',
            'is_published', 'is_featured', 'published_at', 'created_at', 'updated_at'
        ]


class ReportCategoryListSerializer(serializers.ModelSerializer):
    sections_count = serializers.SerializerMethodField()
    absolute_url = serializers.CharField(source='get_absolute_url', read_only=True)
    
    class Meta:
        model = ReportCategory
        fields = [
            'id', 'name', 'name_nepali', 'slug', 'description', 'description_nepali',
            'icon', 'order', 'sections_count', 'absolute_url', 'is_active'
        ]
    
    def get_sections_count(self, obj):
        return obj.sections.filter(is_published=True).count()


class ReportCategoryDetailSerializer(serializers.ModelSerializer):
    sections = ReportSectionListSerializer(many=True, read_only=True)
    absolute_url = serializers.CharField(source='get_absolute_url', read_only=True)
    
    class Meta:
        model = ReportCategory
        fields = [
            'id', 'name', 'name_nepali', 'slug', 'description', 'description_nepali',
            'icon', 'order', 'sections', 'absolute_url', 'is_active', 'created_at', 'updated_at'
        ]


class PublicationSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicationSettings
        fields = [
            'municipality_name', 'municipality_name_english',
            'report_title', 'report_title_english',
            'publication_date', 'version', 'logo',
            'address', 'address_nepali',
            'contact_phone', 'contact_email', 'website',
            'meta_title', 'meta_description', 'meta_keywords',
            'facebook_url', 'twitter_url', 'youtube_url'
        ]


class SearchResultSerializer(serializers.Serializer):
    type = serializers.CharField()  # 'section', 'figure', 'table'
    title = serializers.CharField()
    title_nepali = serializers.CharField(required=False)
    content = serializers.CharField(required=False)
    url = serializers.CharField()
    section_number = serializers.CharField(required=False)
    category = serializers.CharField(required=False)
    relevance_score = serializers.FloatField(required=False)
