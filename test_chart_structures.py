#!/usr/bin/env python3
"""
Compare Demographics vs Infrastructure Chart Structure

This script compares the chart structure returned by demographics vs infrastructure processors.
"""

import os
import sys
import django
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lungri_report.settings.development")
django.setup()

from apps.demographics.processors.manager import get_demographics_manager
from apps.infrastructure.processors.manager import get_infrastructure_manager


def compare_structures():
    """Compare the data structures returned by both systems"""
    print("Comparing Demographics vs Infrastructure Chart Structures")
    print("=" * 60)

    # Test demographics (religion)
    print("\n1. DEMOGRAPHICS (Religion) Structure:")
    print("-" * 40)
    demo_manager = get_demographics_manager()
    demo_result = demo_manager.process_category_for_pdf("religion")

    if demo_result:
        print("Keys in demo_result:")
        for key in demo_result.keys():
            print(f"  - {key}")

        charts = demo_result.get("charts", {})
        print(f"\nCharts structure: {type(charts)}")
        for chart_key, chart_path in charts.items():
            print(f"  - {chart_key}: {chart_path}")

    # Test infrastructure (road_status)
    print("\n2. INFRASTRUCTURE (Road Status) Structure:")
    print("-" * 40)
    infra_manager = get_infrastructure_manager()
    infra_result = infra_manager.process_category_for_pdf("road_status")

    if infra_result:
        print("Keys in infra_result:")
        for key in infra_result.keys():
            print(f"  - {key}")

        pdf_charts = infra_result.get("pdf_charts", {})
        print(f"\nPDF Charts structure: {type(pdf_charts)}")
        for category_key, charts in pdf_charts.items():
            print(f"  Category '{category_key}':")
            if isinstance(charts, dict):
                for chart_key, chart_path in charts.items():
                    print(f"    - {chart_key}: {chart_path}")
            else:
                print(f"    - Value: {charts}")


if __name__ == "__main__":
    compare_structures()
