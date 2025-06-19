"""
Simple Chart Management Tests

Basic tests for the chart file tracking system.
"""

from django.test import TestCase
from apps.chart_management.models import ChartFile
from apps.chart_management.services import get_chart_service


class ChartFileTestCase(TestCase):
    """Test chart file model"""

    def setUp(self):
        self.test_data = {
            "category_a": {"count": 100, "percentage": 50.0},
            "category_b": {"count": 100, "percentage": 50.0},
        }

    def test_chart_file_creation(self):
        """Test creating a chart file record"""
        chart_file = ChartFile.objects.create(
            chart_key="test_chart",
            chart_type="pie",
            content_hash="test_hash",
            file_path="test_chart.svg",
            title="Test Chart",
        )

        self.assertEqual(chart_file.chart_key, "test_chart")
        self.assertEqual(chart_file.chart_type, "pie")
        self.assertEqual(chart_file.title, "Test Chart")

    def test_content_hash_generation(self):
        """Test content hash generation"""
        hash1 = ChartFile.generate_content_hash(self.test_data)
        hash2 = ChartFile.generate_content_hash(self.test_data)

        # Same data should produce same hash
        self.assertEqual(hash1, hash2)

        # Different data should produce different hash
        different_data = self.test_data.copy()
        different_data["category_a"]["count"] = 101
        hash3 = ChartFile.generate_content_hash(different_data)

        self.assertNotEqual(hash1, hash3)


class SimpleChartServiceTestCase(TestCase):
    """Test simple chart service"""

    def setUp(self):
        self.chart_service = get_chart_service()
        self.test_data = {
            "category_a": {"count": 100, "percentage": 50.0},
            "category_b": {"count": 100, "percentage": 50.0},
        }

    def test_service_initialization(self):
        """Test service initialization"""
        service = get_chart_service()
        self.assertIsNotNone(service)

    def test_chart_tracking(self):
        """Test chart file tracking"""
        # This would normally return None since file doesn't exist
        url = self.chart_service.track_chart(
            chart_key="test_chart",
            chart_type="pie",
            data=self.test_data,
            file_path="test_chart.svg",
            title="Test Chart",
        )

        # Check if record was created
        chart_file = ChartFile.objects.filter(chart_key="test_chart").first()
        self.assertIsNotNone(chart_file)
        self.assertEqual(chart_file.chart_type, "pie")

    def test_chart_currency_check(self):
        """Test checking if chart is current"""
        # Create a chart record
        ChartFile.objects.create(
            chart_key="test_chart",
            chart_type="pie",
            content_hash=ChartFile.generate_content_hash(self.test_data),
            file_path="test_chart.svg",
            title="Test Chart",
        )

        # Should be current with same data (but file doesn't exist)
        is_current = self.chart_service.is_chart_current("test_chart", self.test_data)
        self.assertFalse(is_current)  # False because file doesn't exist

        # Different data should not be current
        different_data = self.test_data.copy()
        different_data["category_a"]["count"] = 101
        is_current = self.chart_service.is_chart_current("test_chart", different_data)
        self.assertFalse(is_current)
