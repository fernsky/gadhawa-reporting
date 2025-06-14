from rest_framework import serializers
from .models import (
    ReportCategory, ReportSection, ReportFigure, 
    ReportTable, PublicationSettings
)
from .utils.nepali_numbers import to_nepali_digits


class ReportFigureSerializer(serializers.ModelSerializer):
    figure_number_nepali = serializers.SerializerMethodField()
    
    class Meta:
        model = ReportFigure
        fields = [
            'id', 'title', 'title_nepali', 'figure_type', 'figure_number', 'figure_number_nepali',
            'description', 'description_nepali', 'image', 'data_source',
            'chart_data', 'order'
        ]
    
    def get_figure_number_nepali(self, obj):
        return to_nepali_digits(str(obj.figure_number)) if obj.figure_number else None


class ReportTableSerializer(serializers.ModelSerializer):
    table_number_nepali = serializers.SerializerMethodField()
    
    class Meta:
        model = ReportTable
        fields = [
            'id', 'title', 'title_nepali', 'table_number', 'table_number_nepali',
            'description', 'description_nepali', 'data', 'data_source', 'order'
        ]
    
    def get_table_number_nepali(self, obj):
        return to_nepali_digits(str(obj.table_number)) if obj.table_number else None


class ReportSectionListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_name_nepali = serializers.CharField(source='category.name_nepali', read_only=True)
    absolute_url = serializers.CharField(source='get_absolute_url', read_only=True)
    section_number_nepali = serializers.SerializerMethodField()
    
    class Meta:
        model = ReportSection
        fields = [
            'id', 'title', 'title_nepali', 'slug', 'section_number', 'section_number_nepali',
            'summary', 'summary_nepali', 'category_name', 'category_name_nepali',
            'absolute_url', 'is_published', 'is_featured', 'published_at'
        ]
    
    def get_section_number_nepali(self, obj):
        return to_nepali_digits(str(obj.section_number)) if obj.section_number else None


class ReportSectionDetailSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only=True)
    figures = ReportFigureSerializer(many=True, read_only=True)
    tables = ReportTableSerializer(many=True, read_only=True)
    absolute_url = serializers.CharField(source='get_absolute_url', read_only=True)
    section_number_nepali = serializers.SerializerMethodField()
    
    class Meta:
        model = ReportSection
        fields = [
            'id', 'title', 'title_nepali', 'slug', 'section_number', 'section_number_nepali',
            'content', 'content_nepali', 'summary', 'summary_nepali',
            'category', 'figures', 'tables', 'absolute_url',
            'is_published', 'is_featured', 'published_at', 'created_at', 'updated_at'
        ]
    
    def get_section_number_nepali(self, obj):
        return to_nepali_digits(str(obj.section_number)) if obj.section_number else None


class ReportCategoryListSerializer(serializers.ModelSerializer):
    sections_count = serializers.SerializerMethodField()
    sections_count_nepali = serializers.SerializerMethodField()
    absolute_url = serializers.CharField(source='get_absolute_url', read_only=True)
    
    class Meta:
        model = ReportCategory
        fields = [
            'id', 'name', 'name_nepali', 'slug', 'description', 'description_nepali',
            'icon', 'order', 'sections_count', 'sections_count_nepali', 'absolute_url', 'is_active'
        ]
    
    def get_sections_count(self, obj):
        return obj.sections.filter(is_published=True).count()
    
    def get_sections_count_nepali(self, obj):
        count = obj.sections.filter(is_published=True).count()
        return to_nepali_digits(str(count))


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
    section_number_nepali = serializers.SerializerMethodField()
    category = serializers.CharField(required=False)
    relevance_score = serializers.FloatField(required=False)
    
    def get_section_number_nepali(self, obj):
        section_number = obj.get('section_number')
        return to_nepali_digits(str(section_number)) if section_number else None
