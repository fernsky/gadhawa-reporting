"""
Test Chart Management System

Simple tests to verify the chart management functionality.
"""

import tempfile
import json
from pathlib import Path
from django.test import TestCase, override_settings
from django.conf import settings
from apps.chart_management.models import (
    ChartCache,
    ChartGenerationLog,
    ChartStatusChoice,
)
from apps.chart_management.services import get_chart_service


class ChartManagementTestCase(TestCase):
    """Test cases for chart management system"""

    def setUp(self):
        """Set up test environment"""
        self.chart_service = get_chart_service()
        self.test_data = {
            "HINDU": {"population": 1000, "percentage": 60.0, "name_nepali": "हिन्दू"},
            "BUDDHIST": {"population": 400, "percentage": 24.0, "name_nepali": "बौद्ध"},
            "CHRISTIAN": {
                "population": 200,
                "percentage": 12.0,
                "name_nepali": "क्रिस्चियन",
            },
            "MUSLIM": {"population": 67, "percentage": 4.0, "name_nepali": "मुस्लिम"},
        }

    def test_chart_cache_creation(self):
        """Test chart cache model creation"""
        chart_cache = ChartCache.objects.create(
            chart_key="test_chart",
            chart_type="pie",
            content_hash="test_hash",
            svg_content_hash="svg_hash",
            title="Test Chart",
            width=800,
            height=400,
            status=ChartStatusChoice.COMPLETED,
        )

        self.assertEqual(chart_cache.chart_key, "test_chart")
        self.assertEqual(chart_cache.chart_type, "pie")
        self.assertEqual(chart_cache.status, ChartStatusChoice.COMPLETED)

    def test_content_hash_generation(self):
        """Test content hash generation"""
        hash1 = ChartCache.generate_content_hash(self.test_data)
        hash2 = ChartCache.generate_content_hash(self.test_data)

        # Same data should produce same hash
        self.assertEqual(hash1, hash2)

        # Different data should produce different hash
        different_data = self.test_data.copy()
        different_data["HINDU"]["population"] = 1001
        hash3 = ChartCache.generate_content_hash(different_data)

        self.assertNotEqual(hash1, hash3)

    def test_chart_service_initialization(self):
        """Test chart service initialization"""
        service = get_chart_service()
        self.assertIsNotNone(service)
        self.assertIsNotNone(service.charts_dir)

    def test_chart_generation_caching(self):
        """Test chart generation and caching"""
        # First generation should create new chart
        svg_url1, png_url1 = self.chart_service.get_or_generate_chart(
            chart_key="test_religion",
            chart_type="pie",
            data=self.test_data,
            title="Religion Distribution",
            width=800,
            height=400,
        )

        # Check if chart was created in database
        chart_cache = ChartCache.objects.filter(chart_key="test_religion").first()
        self.assertIsNotNone(chart_cache)

        # Second generation should use cache
        svg_url2, png_url2 = self.chart_service.get_or_generate_chart(
            chart_key="test_religion",
            chart_type="pie",
            data=self.test_data,  # Same data
            title="Religion Distribution",
            width=800,
            height=400,
        )

        # URLs should be the same (from cache)
        self.assertEqual(svg_url1, svg_url2)

        # Access count should increase
        chart_cache.refresh_from_db()
        self.assertGreater(chart_cache.access_count, 0)

    def test_chart_stats(self):
        """Test chart statistics"""
        # Generate a chart
        self.chart_service.get_or_generate_chart(
            chart_key="test_stats",
            chart_type="pie",
            data=self.test_data,
            title="Test Stats Chart",
            width=800,
            height=400,
        )

        stats = self.chart_service.get_chart_stats()

        self.assertIn("total_charts", stats)
        self.assertIn("completed_charts", stats)
        self.assertIn("failed_charts", stats)
        self.assertIn("cache_hit_rate", stats)
        self.assertGreaterEqual(stats["total_charts"], 1)

    def test_chart_cleanup(self):
        """Test chart cleanup functionality"""
        # Create a test chart
        chart_cache = ChartCache.objects.create(
            chart_key="cleanup_test",
            chart_type="pie",
            content_hash="cleanup_hash",
            svg_content_hash="svg_hash",
            title="Cleanup Test Chart",
            width=800,
            height=400,
            status=ChartStatusChoice.COMPLETED,
            access_count=0,  # Low access count for cleanup
        )

        initial_count = ChartCache.objects.count()

        # Test cleanup (should remove low-access charts)
        deleted_count = self.chart_service.cleanup_old_charts(days_old=0)

        # Verify cleanup worked
        self.assertGreater(deleted_count, 0)
        final_count = ChartCache.objects.count()
        self.assertLess(final_count, initial_count)


class ChartProcessorTestCase(TestCase):
    """Test enhanced chart processor functionality"""

    def setUp(self):
        """Set up test environment"""
        from apps.chart_management.processors import EnhancedChartProcessor

        class TestProcessor(EnhancedChartProcessor):
            def get_section_title(self):
                return "Test Section"

            def get_section_number(self):
                return "1.1"

            def get_chart_key(self):
                return "test_processor"

            def get_data(self):
                return {"test": "data"}

        self.processor = TestProcessor()

    def test_processor_initialization(self):
        """Test processor initialization"""
        self.assertIsNotNone(self.processor.chart_service)
        self.assertEqual(self.processor.get_chart_key(), "test_processor")
        self.assertEqual(self.processor.get_section_title(), "Test Section")

    def test_chart_url_generation(self):
        """Test chart URL generation"""
        data = {"test": "data"}
        urls = self.processor.generate_chart_urls(data)

        self.assertIsInstance(urls, dict)
        # Should contain pie chart by default
        if self.processor.supports_pie_chart():
            self.assertIn("pie", urls)
