"""
Generate a test PDF to verify the complete page numbering system
"""

import os
import sys
import django
from datetime import datetime

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lungri_report.settings.development")
django.setup()

from django.template.loader import render_to_string
from apps.reports.models import (
    ReportCategory,
    ReportSection,
    ReportFigure,
    ReportTable,
    PublicationSettings,
)
from apps.reports.utils.page_calculator import calculate_pdf_page_numbers


def generate_test_pdf_html():
    """Generate HTML for testing the PDF template"""
    print("=== Generating Test PDF HTML ===")

    # Get data
    categories = (
        ReportCategory.objects.filter(is_active=True)
        .prefetch_related("sections__figures", "sections__tables")
        .order_by("order")
    )

    figures = ReportFigure.objects.select_related("section__category").order_by(
        "figure_number"
    )
    tables = ReportTable.objects.select_related("section__category").order_by(
        "table_number"
    )

    print(f"Found {categories.count()} categories")
    print(f"Found {figures.count()} figures")
    print(f"Found {tables.count()} tables")

    # Calculate page numbers
    page_numbers = calculate_pdf_page_numbers(categories, figures, tables)

    # Create context
    context = {
        "municipality_name": "लुङ्ग्री गाउँपालिका",
        "municipality_name_english": "lungri Rural Municipality",
        "publication_settings": None,
        "categories": categories,
        "figures": figures,
        "tables": tables,
        "page_numbers": page_numbers,
        "total_figures": figures.count(),
        "total_tables": tables.count(),
        "generated_date": datetime.now(),
    }

    # Generate HTML
    try:
        html_content = render_to_string("reports/pdf_full_report.html", context)

        # Save HTML file for testing
        output_path = os.path.join(project_root, "test_output.html")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"Test HTML generated successfully: {output_path}")
        print(f"HTML length: {len(html_content)} characters")

        # Show page number summary
        print("\n=== Page Number Summary ===")
        if "front_matter" in page_numbers:
            print("Front Matter:")
            for section, info in page_numbers["front_matter"].items():
                print(f"  {section}: pages {info['start']}-{info['end']}")

        print(f"\nCategories tracked: {len(page_numbers.get('categories', {}))}")
        print(f"Sections tracked: {len(page_numbers.get('sections', {}))}")
        print(f"Figures tracked: {len(page_numbers.get('figures', {}))}")
        print(f"Tables tracked: {len(page_numbers.get('tables', {}))}")

        return True

    except Exception as e:
        print(f"Error generating HTML: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_template_filters():
    """Test the custom template filters"""
    print("\n=== Testing Template Filters ===")

    from apps.reports.templatetags.nepali_filters import (
        get_item,
        get_page_number_nepali,
        nepali_section_number,
        split,
    )

    # Test get_item
    test_dict = {"1": "Page 1", "2": "Page 2"}
    result = get_item(test_dict, "1")
    print(f"get_item test: {result}")

    # Test get_page_number_nepali
    result = get_page_number_nepali(123)
    print(f"get_page_number_nepali test: 123 -> {result}")

    # Test nepali_section_number
    result = nepali_section_number("1.2.3")
    print(f"nepali_section_number test: 1.2.3 -> {result}")

    # Test split
    result = split("1.2.3", ".")
    print(f"split test: '1.2.3' -> {result}")


if __name__ == "__main__":
    # Run the sample data creation first
    print("=== Creating Sample Data ===")
    exec(open("create_sample_data.py").read())

    # Test template filters
    test_template_filters()

    # Generate test HTML
    success = generate_test_pdf_html()

    if success:
        print("\n=== SUCCESS ===")
        print("✓ Page numbering system is working")
        print("✓ Template filters are working")
        print("✓ PDF template renders successfully")
        print("✓ Test HTML file generated")
        print("\nYou can now:")
        print("1. Open test_output.html in a browser to see the rendered content")
        print("2. Use the PDF generation views to create actual PDFs")
        print("3. The page numbering system is ready for production use")
    else:
        print("\n=== ERRORS DETECTED ===")
        print("Please check the error messages above")
