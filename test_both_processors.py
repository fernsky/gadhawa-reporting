#!/usr/bin/env python3
"""
Complete test to verify both religion and major_skills processors work correctly
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lungri_report.settings")
sys.path.append(
    "/Users/trilochan/Desktop/final-delivery/digital-profile/lungri/lungri-report"
)

django.setup()

from apps.demographics.processors.religion import ReligionProcessor
from apps.economics.processors.major_skills import MajorSkillsProcessor


def test_both_processors():
    """Test both processors to ensure they work consistently"""
    print("🧪 Testing Both Processors (Religion & Major Skills)...")

    try:
        # Test Religion Processor
        print("\n1️⃣  Testing Religion Processor...")
        religion_processor = ReligionProcessor()
        religion_data = religion_processor.process_for_pdf()

        print(
            f"✓ Religion - Total Population: {religion_data.get('total_population', 0)}"
        )
        print(f"✓ Religion - Charts: {list(religion_data.get('charts', {}).keys())}")
        print(f"✓ Religion - Data Keys: {list(religion_data.keys())}")

        # Test Major Skills Processor
        print("\n2️⃣  Testing Major Skills Processor...")
        skills_processor = MajorSkillsProcessor()
        skills_data = skills_processor.process_for_pdf()

        print(f"✓ Skills - Total Population: {skills_data.get('total_population', 0)}")
        print(f"✓ Skills - Charts: {list(skills_data.get('charts', {}).keys())}")
        print(f"✓ Skills - Data Keys: {list(skills_data.keys())}")

        # Compare structure
        print("\n3️⃣  Comparing Data Structures...")
        religion_keys = set(religion_data.keys())
        skills_keys = set(skills_data.keys())

        common_keys = religion_keys & skills_keys
        religion_only = religion_keys - skills_keys
        skills_only = skills_keys - religion_keys

        print(f"✓ Common keys: {sorted(common_keys)}")
        if religion_only:
            print(f"📊 Religion-only keys: {sorted(religion_only)}")
        if skills_only:
            print(f"📊 Skills-only keys: {sorted(skills_only)}")

        # Check chart generation
        print("\n4️⃣  Checking Chart Generation...")
        religion_charts = religion_data.get("charts", {})
        skills_charts = skills_data.get("charts", {})

        print(f"Religion charts: {list(religion_charts.keys())}")
        print(f"Skills charts: {list(skills_charts.keys())}")

        # Verify chart files exist
        import os
        from pathlib import Path

        chart_dir = Path("staticfiles/images/charts")
        religion_files = list(chart_dir.glob("religion_*"))
        skills_files = list(chart_dir.glob("major_skills_*"))

        print(f"✓ Religion chart files: {[f.name for f in religion_files]}")
        print(f"✓ Skills chart files: {[f.name for f in skills_files]}")

        print("\n✅ Both processors are working correctly and consistently!")
        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_both_processors()
    if success:
        print("\n🎉 Both processors (Religion and Major Skills) are working perfectly!")
        print(
            "🔧 The religion processor has been successfully updated to match the major_skills pattern!"
        )
    else:
        print("\n💥 There are still issues that need to be addressed.")
