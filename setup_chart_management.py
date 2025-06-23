#!/usr/bin/env python3
"""
Chart Management Setup and Test Script

This script helps set up the chart management system and test its functionality.
"""

import os
import sys
import django
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gadhawa_report.settings.development")
django.setup()

from apps.chart_management.services import get_chart_service
from apps.demographics.processors.religion import ReligionProcessor


def test_chart_generation():
    """Test the chart generation system"""
    print("🔄 Testing Chart Management System...")

    try:
        # Initialize religion processor
        religion_processor = ReligionProcessor()

        # Get data
        print("📊 Getting religion data...")
        data = religion_processor.get_data()
        print(f"✅ Data retrieved: {len(data.get('religion_data', {}))} religions")

        # Test chart generation
        print("🎨 Generating charts...")
        chart_urls = religion_processor.generate_chart_urls(data)

        if chart_urls.get("pie"):
            pie_chart = chart_urls["pie"]
            print(f"✅ Pie chart generated:")
            print(f"   SVG: {pie_chart.get('svg', 'Not available')}")
            print(f"   PNG: {pie_chart.get('png', 'Not available')}")
        else:
            print("❌ Pie chart generation failed")

        # Test chart service stats
        print("📈 Chart service statistics:")
        chart_service = get_chart_service()
        stats = chart_service.get_chart_stats()

        for key, value in stats.items():
            print(f"   {key}: {value}")

        print("✅ Chart management system test completed successfully!")

    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback

        traceback.print_exc()


def setup_chart_directories():
    """Set up required directories for chart storage"""
    print("📁 Setting up chart directories...")

    try:
        from django.conf import settings

        # Create charts directory
        charts_dir = Path(settings.STATICFILES_DIRS[0]) / "images" / "charts"
        charts_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ Charts directory created: {charts_dir}")

        # Create media directory if needed
        media_dir = Path(settings.MEDIA_ROOT)
        media_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ Media directory ensured: {media_dir}")

    except Exception as e:
        print(f"❌ Error setting up directories: {e}")


def check_dependencies():
    """Check if required dependencies are available"""
    print("🔍 Checking dependencies...")

    try:
        # Check for Inkscape
        import subprocess

        result = subprocess.run(
            ["inkscape", "--version"], capture_output=True, text=True
        )
        if result.returncode == 0:
            print("✅ Inkscape is available")
            print(f"   Version: {result.stdout.strip()}")
        else:
            print("❌ Inkscape not available - PNG conversion will fail")

    except FileNotFoundError:
        print("❌ Inkscape not found - please install Inkscape for PNG conversion")
        print("   Ubuntu/Debian: sudo apt-get install inkscape")
        print("   macOS: brew install inkscape")
        print("   Windows: Download from https://inkscape.org/")
    except Exception as e:
        print(f"❌ Error checking Inkscape: {e}")


def main():
    """Main function"""
    print("🚀 Chart Management System Setup")
    print("=" * 50)

    check_dependencies()
    print()

    setup_chart_directories()
    print()

    test_chart_generation()
    print()

    print("🎉 Setup completed!")
    print()
    print("Next steps:")
    print("1. Run migrations: python manage.py migrate")
    print("2. Create superuser: python manage.py createsuperuser")
    print("3. Test in admin: python manage.py runserver")
    print("4. Clean up old charts: python manage.py cleanup_charts --days 7")


if __name__ == "__main__":
    main()
