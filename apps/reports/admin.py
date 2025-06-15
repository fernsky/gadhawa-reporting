from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    ReportCategory,
    ReportSection,
    ReportFigure,
    ReportTable,
    PublicationSettings,
    ReportDownload,
)


@admin.register(ReportCategory)
class ReportCategoryAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "name_nepali",
        "order",
        "sections_count",
        "is_active",
        "created_at",
    ]
    list_filter = ["is_active", "created_at"]
    search_fields = ["name", "name_nepali", "description"]
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["order", "name"]
    list_editable = ["order", "is_active"]

    def sections_count(self, obj):
        count = obj.sections.count()
        if count > 0:
            url = (
                reverse("admin:reports_reportsection_changelist")
                + f"?category__id__exact={obj.id}"
            )
            return format_html('<a href="{}">{} sections</a>', url, count)
        return "0 sections"

    sections_count.short_description = "Sections"


class ReportFigureInline(admin.TabularInline):
    model = ReportFigure
    extra = 0
    fields = ["figure_number", "title", "figure_type", "image", "order"]
    readonly_fields = ["created_at"]


class ReportTableInline(admin.TabularInline):
    model = ReportTable
    extra = 0
    fields = ["table_number", "title", "order"]
    readonly_fields = ["created_at"]


@admin.register(ReportSection)
class ReportSectionAdmin(admin.ModelAdmin):
    list_display = [
        "section_number",
        "title",
        "category",
        "is_published",
        "figures_count",
        "tables_count",
        "author",
        "updated_at",
    ]
    list_filter = ["category", "is_published", "is_featured", "created_at", "author"]
    search_fields = ["title", "title_nepali", "content", "section_number"]
    prepopulated_fields = {"slug": ("title",)}
    ordering = ["category__order", "order", "section_number"]
    list_editable = ["is_published"]
    inlines = [ReportFigureInline, ReportTableInline]

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("category", "section_number", "title", "title_nepali", "slug")},
        ),
        (
            "Content",
            {"fields": ("summary", "summary_nepali", "content", "content_nepali")},
        ),
        (
            "Publication",
            {
                "fields": ("is_published", "is_featured", "author", "order"),
                "classes": ("collapse",),
            },
        ),
        (
            "SEO",
            {
                "fields": ("meta_title", "meta_description", "meta_keywords"),
                "classes": ("collapse",),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)

    def figures_count(self, obj):
        count = obj.figures.count()
        if count > 0:
            url = (
                reverse("admin:reports_reportfigure_changelist")
                + f"?section__id__exact={obj.id}"
            )
            return format_html('<a href="{}">{} figures</a>', url, count)
        return "0 figures"

    figures_count.short_description = "Figures"

    def tables_count(self, obj):
        count = obj.tables.count()
        if count > 0:
            url = (
                reverse("admin:reports_reporttable_changelist")
                + f"?section__id__exact={obj.id}"
            )
            return format_html('<a href="{}">{} tables</a>', url, count)
        return "0 tables"

    tables_count.short_description = "Tables"


@admin.register(ReportFigure)
class ReportFigureAdmin(admin.ModelAdmin):
    list_display = [
        "figure_number",
        "title",
        "section",
        "figure_type",
        "image_preview",
        "order",
        "created_at",
    ]
    list_filter = ["figure_type", "section__category", "created_at"]
    search_fields = ["title", "title_nepali", "description", "figure_number"]
    ordering = ["section__category__order", "section__order", "order"]
    list_editable = ["order"]

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "section",
                    "figure_number",
                    "title",
                    "title_nepali",
                    "figure_type",
                )
            },
        ),
        (
            "Content",
            {"fields": ("description", "description_nepali", "image", "data_source")},
        ),
        (
            "Chart Data",
            {
                "fields": ("chart_data",),
                "classes": ("collapse",),
                "description": "JSON data for generating charts programmatically",
            },
        ),
        ("Display", {"fields": ("order",)}),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover;" />',
                obj.image.url,
            )
        return "No image"

    image_preview.short_description = "Preview"


@admin.register(ReportTable)
class ReportTableAdmin(admin.ModelAdmin):
    list_display = [
        "table_number",
        "title",
        "section",
        "data_preview",
        "order",
        "created_at",
    ]
    list_filter = ["section__category", "created_at"]
    search_fields = ["title", "title_nepali", "description", "table_number"]
    ordering = ["section__category__order", "section__order", "order"]
    list_editable = ["order"]

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("section", "table_number", "title", "title_nepali")},
        ),
        (
            "Content",
            {"fields": ("description", "description_nepali", "data", "data_source")},
        ),
        ("Display", {"fields": ("order",)}),
    )

    def data_preview(self, obj):
        if obj.data:
            # Show first few keys/values
            data_str = str(obj.data)[:100]
            if len(str(obj.data)) > 100:
                data_str += "..."
            return data_str
        return "No data"

    data_preview.short_description = "Data Preview"


@admin.register(PublicationSettings)
class PublicationSettingsAdmin(admin.ModelAdmin):
    list_display = [
        "municipality_name",
        "report_title",
        "version",
        "publication_date",
        "updated_at",
    ]

    fieldsets = (
        (
            "Municipality Information",
            {
                "fields": (
                    "municipality_name",
                    "municipality_name_english",
                    "address",
                    "address_nepali",
                )
            },
        ),
        (
            "Report Information",
            {
                "fields": (
                    "report_title",
                    "report_title_english",
                    "publication_date",
                    "version",
                    "logo",
                )
            },
        ),
        (
            "Contact Information",
            {"fields": ("contact_phone", "contact_email", "website")},
        ),
        (
            "SEO Settings",
            {
                "fields": ("meta_title", "meta_description", "meta_keywords"),
                "classes": ("collapse",),
            },
        ),
        (
            "Social Media",
            {
                "fields": ("facebook_url", "twitter_url", "youtube_url"),
                "classes": ("collapse",),
            },
        ),
        (
            "Analytics",
            {
                "fields": ("google_analytics_id", "facebook_pixel_id"),
                "classes": ("collapse",),
            },
        ),
    )

    def has_add_permission(self, request):
        # Only allow one instance
        return not PublicationSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion
        return False


@admin.register(ReportDownload)
class ReportDownloadAdmin(admin.ModelAdmin):
    list_display = ["download_type", "section", "ip_address", "downloaded_at"]
    list_filter = ["download_type", "downloaded_at"]
    search_fields = ["ip_address"]
    ordering = ["-downloaded_at"]
    readonly_fields = ["id", "downloaded_at"]

    def has_add_permission(self, request):
        # Downloads are tracked automatically
        return False

    def has_change_permission(self, request, obj=None):
        # Downloads should not be modified
        return False


# Customize admin site
admin.site.site_header = "lungri Digital Profile Admin"
admin.site.site_title = "LungriAdmin"
admin.site.index_title = "Digital Profile Management"
