"""
Simple Chart Management Tests

Basic tests for the chart file tracking system.
"""

from django.test import TestCase
from apps.chart_management.models import ChartFile
from apps.chart_management.services import get_chart_service


class ChartFileTestCase(TestCase):
    """Test chart file model"""

    def test_chart_file_creation(self):
        """Test creating a chart file record"""
        chart_file = ChartFile.objects.create(
            chart_key="test_chart",
            chart_type="pie",
            file_path="test_chart.svg",
            title="Test Chart",
        )

        self.assertEqual(chart_file.chart_key, "test_chart")
        self.assertEqual(chart_file.chart_type, "pie")
        self.assertEqual(chart_file.title, "Test Chart")


class SimpleChartServiceTestCase(TestCase):
    """Test simple chart service"""

    def setUp(self):
        self.chart_service = get_chart_service()

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
            file_path="test_chart.svg",
            title="Test Chart",
        )

        # Check if record was created
        chart_file = ChartFile.objects.filter(chart_key="test_chart").first()
        self.assertIsNotNone(chart_file)
        self.assertEqual(chart_file.chart_type, "pie")

    def test_chart_existence_check(self):
        """Test checking if chart exists"""
        # Create a chart record
        ChartFile.objects.create(
            chart_key="test_chart",
            chart_type="pie",
            file_path="test_chart.svg",
            title="Test Chart",
        )

        # Should not exist because file doesn't exist on filesystem
        exists = self.chart_service.chart_exists("test_chart")
        self.assertFalse(exists)  # False because file doesn't exist

        # Should need generation
        needs_gen = self.chart_service.needs_generation("test_chart")
        self.assertTrue(needs_gen)
