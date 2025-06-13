from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
import uuid
from ckeditor.fields import RichTextField
from PIL import Image
import io
from django.core.files.base import ContentFile
import os

User = get_user_model()


class ReportCategory(models.Model):
    """
    Report categories like Demographics, Economics, Social, etc.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, verbose_name="Category Name")
    name_nepali = models.CharField(max_length=200, verbose_name="Category Name (Nepali)")
    slug = models.SlugField(unique=True, max_length=200)
    description = models.TextField(blank=True, verbose_name="Description")
    description_nepali = models.TextField(blank=True, verbose_name="Description (Nepali)")
    order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    icon = models.CharField(max_length=50, blank=True, verbose_name="Icon Class")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Report Category"
        verbose_name_plural = "Report Categories"

    def __str__(self):
        return f"{self.name} ({self.name_nepali})"

    def get_absolute_url(self):
        return reverse('reports:category', kwargs={'slug': self.slug})


class ReportSection(models.Model):
    """
    Individual sections within a category (e.g., 1.1, 1.2, etc.)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(ReportCategory, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=300, verbose_name="Section Title")
    title_nepali = models.CharField(max_length=300, verbose_name="Section Title (Nepali)")
    slug = models.SlugField(max_length=200)
    section_number = models.CharField(max_length=20, verbose_name="Section Number (e.g., 1.1)")
    content = RichTextField(blank=True, verbose_name="Content")
    content_nepali = RichTextField(blank=True, verbose_name="Content (Nepali)")
    summary = models.TextField(blank=True, verbose_name="Summary")
    summary_nepali = models.TextField(blank=True, verbose_name="Summary (Nepali)")
    order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    meta_title = models.CharField(max_length=200, blank=True, verbose_name="SEO Title")
    meta_description = models.TextField(max_length=500, blank=True, verbose_name="SEO Description")
    meta_keywords = models.CharField(max_length=500, blank=True, verbose_name="SEO Keywords")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['category__order', 'order', 'section_number']
        unique_together = ['category', 'slug']
        verbose_name = "Report Section"
        verbose_name_plural = "Report Sections"

    def __str__(self):
        return f"{self.section_number} - {self.title}"

    def get_absolute_url(self):
        return reverse('reports:section', kwargs={
            'category_slug': self.category.slug,
            'section_slug': self.slug
        })

    def save(self, *args, **kwargs):
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)


class ReportFigure(models.Model):
    """
    Figures/Charts within report sections
    """
    FIGURE_TYPES = [
        ('chart', 'Chart'),
        ('graph', 'Graph'),
        ('image', 'Image'),
        ('diagram', 'Diagram'),
        ('map', 'Map'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    section = models.ForeignKey(ReportSection, on_delete=models.CASCADE, related_name='figures')
    title = models.CharField(max_length=300, verbose_name="Figure Title")
    title_nepali = models.CharField(max_length=300, verbose_name="Figure Title (Nepali)")
    figure_type = models.CharField(max_length=20, choices=FIGURE_TYPES, default='chart')
    figure_number = models.CharField(max_length=20, verbose_name="Figure Number")
    description = models.TextField(blank=True, verbose_name="Description")
    description_nepali = models.TextField(blank=True, verbose_name="Description (Nepali)")
    image = models.ImageField(upload_to='reports/figures/', blank=True, null=True)
    data_source = models.TextField(blank=True, verbose_name="Data Source")
    chart_data = models.JSONField(blank=True, null=True, verbose_name="Chart Data (JSON)")
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['section__category__order', 'section__order', 'order']
        verbose_name = "Report Figure"
        verbose_name_plural = "Report Figures"

    def __str__(self):
        return f"{self.figure_number} - {self.title}"

    def save(self, *args, **kwargs):
        # Optimize image if uploaded
        if self.image:
            img = Image.open(self.image)
            if img.height > 800 or img.width > 1200:
                output_size = (1200, 800)
                img.thumbnail(output_size, Image.Resampling.LANCZOS)
                
                # Save optimized image
                output = io.BytesIO()
                img.save(output, format='JPEG', quality=85, optimize=True)
                output.seek(0)
                
                # Replace the original image
                self.image.save(
                    self.image.name,
                    ContentFile(output.read()),
                    save=False
                )
        super().save(*args, **kwargs)


class ReportTable(models.Model):
    """
    Data tables within report sections
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    section = models.ForeignKey(ReportSection, on_delete=models.CASCADE, related_name='tables')
    title = models.CharField(max_length=300, verbose_name="Table Title")
    title_nepali = models.CharField(max_length=300, verbose_name="Table Title (Nepali)")
    table_number = models.CharField(max_length=20, verbose_name="Table Number")
    description = models.TextField(blank=True, verbose_name="Description")
    description_nepali = models.TextField(blank=True, verbose_name="Description (Nepali)")
    data = models.JSONField(verbose_name="Table Data (JSON)")
    data_source = models.TextField(blank=True, verbose_name="Data Source")
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['section__category__order', 'section__order', 'order']
        verbose_name = "Report Table"
        verbose_name_plural = "Report Tables"

    def __str__(self):
        return f"{self.table_number} - {self.title}"


class PublicationSettings(models.Model):
    """
    Global settings for report publication
    """
    municipality_name = models.CharField(max_length=200, default="गढवा गाउँपालिका")
    municipality_name_english = models.CharField(max_length=200, default="Gadhawa Rural Municipality")
    report_title = models.CharField(max_length=300, default="डिजिटल प्रोफाइल प्रतिवेदन")
    report_title_english = models.CharField(max_length=300, default="Digital Profile Report")
    publication_date = models.DateField(default=timezone.now)
    version = models.CharField(max_length=20, default="1.0")
    logo = models.ImageField(upload_to='reports/logo/', blank=True, null=True)
    address = models.TextField(blank=True)
    address_nepali = models.TextField(blank=True)
    contact_phone = models.CharField(max_length=50, blank=True)
    contact_email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    
    # SEO Settings
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(max_length=500, blank=True)
    meta_keywords = models.CharField(max_length=500, blank=True)
    
    # Social Media
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    
    # Analytics
    google_analytics_id = models.CharField(max_length=50, blank=True)
    facebook_pixel_id = models.CharField(max_length=50, blank=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Publication Settings"
        verbose_name_plural = "Publication Settings"

    def __str__(self):
        return f"{self.municipality_name} - {self.report_title}"

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and PublicationSettings.objects.exists():
            raise ValueError("Only one PublicationSettings instance is allowed")
        super().save(*args, **kwargs)


class ReportDownload(models.Model):
    """
    Track report downloads for analytics
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    section = models.ForeignKey(ReportSection, on_delete=models.CASCADE, null=True, blank=True)
    download_type = models.CharField(max_length=20, choices=[
        ('pdf', 'PDF'),
        ('full_report', 'Full Report'),
        ('section', 'Section'),
    ])
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    downloaded_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Report Download"
        verbose_name_plural = "Report Downloads"

    def __str__(self):
        return f"{self.download_type} - {self.downloaded_at}"
